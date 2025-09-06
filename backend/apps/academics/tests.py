import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from apps.academics.models import (
    AcademicYear, Level, Class, Subject, ExamType, Trimester,
    ClassSubject, StudentClass, Grade, Attendance
)
from factories import (
    AcademicYearFactory, LevelFactory, ClassFactory, SubjectFactory,
    ExamTypeFactory, TrimesterFactory, ClassSubjectFactory,
    StudentClassFactory, GradeFactory, AttendanceFactory,
    StudentFactory, TeacherFactory, UserFactory
)


class AcademicYearModelTest(TestCase):
    def setUp(self):
        self.academic_year = AcademicYearFactory()

    def test_academic_year_creation(self):
        self.assertTrue(isinstance(self.academic_year, AcademicYear))
        self.assertIsNotNone(self.academic_year.name)
        self.assertIsNotNone(self.academic_year.start_date)
        self.assertIsNotNone(self.academic_year.end_date)

    def test_academic_year_str_representation(self):
        self.assertEqual(str(self.academic_year), self.academic_year.name)


class LevelModelTest(TestCase):
    def setUp(self):
        self.level = LevelFactory()

    def test_level_creation(self):
        self.assertTrue(isinstance(self.level, Level))
        self.assertIsNotNone(self.level.name)
        self.assertIsNotNone(self.level.order)

    def test_level_str_representation(self):
        self.assertEqual(str(self.level), self.level.name)


class ClassModelTest(TestCase):
    def setUp(self):
        self.level = LevelFactory()
        self.academic_year = AcademicYearFactory()
        self.class_obj = ClassFactory(level=self.level, academic_year=self.academic_year)

    def test_class_creation(self):
        self.assertTrue(isinstance(self.class_obj, Class))
        self.assertEqual(self.class_obj.level, self.level)
        self.assertEqual(self.class_obj.academic_year, self.academic_year)
        self.assertIsNotNone(self.class_obj.capacity)

    def test_class_str_representation(self):
        self.assertEqual(str(self.class_obj), self.class_obj.name)


class SubjectModelTest(TestCase):
    def setUp(self):
        self.subject = SubjectFactory()

    def test_subject_creation(self):
        self.assertTrue(isinstance(self.subject, Subject))
        self.assertIsNotNone(self.subject.name)
        self.assertIsNotNone(self.subject.code)
        self.assertIsNotNone(self.subject.coefficient)

    def test_subject_str_representation(self):
        self.assertEqual(str(self.subject), self.subject.name)


class GradeModelTest(TestCase):
    def setUp(self):
        self.student = StudentFactory()
        self.subject = SubjectFactory()
        self.exam_type = ExamTypeFactory()
        self.trimester = TrimesterFactory()
        self.grade = GradeFactory(
            student=self.student,
            subject=self.subject,
            exam_type=self.exam_type,
            trimester=self.trimester
        )

    def test_grade_creation(self):
        self.assertTrue(isinstance(self.grade, Grade))
        self.assertEqual(self.grade.student, self.student)
        self.assertEqual(self.grade.subject, self.subject)
        self.assertEqual(self.grade.exam_type, self.exam_type)
        self.assertEqual(self.grade.trimester, self.trimester)

    def test_grade_str_representation(self):
        expected = f"{self.grade.student.user.get_full_name()} - {self.grade.subject.name} - {self.grade.grade}"
        self.assertEqual(str(self.grade), expected)

    def test_grade_value(self):
        self.assertGreaterEqual(self.grade.grade, 0)
        self.assertLessEqual(self.grade.grade, self.grade.max_grade)


class AttendanceModelTest(TestCase):
    def setUp(self):
        self.student = StudentFactory()
        self.class_obj = ClassFactory()
        self.teacher = TeacherFactory()
        self.attendance = AttendanceFactory(
            student=self.student,
            class_obj=self.class_obj,
            teacher=self.teacher
        )

    def test_attendance_creation(self):
        self.assertTrue(isinstance(self.attendance, Attendance))
        self.assertEqual(self.attendance.student, self.student)
        self.assertEqual(self.attendance.class_obj, self.class_obj)
        self.assertEqual(self.attendance.teacher, self.teacher)

    def test_attendance_str_representation(self):
        expected = f"{self.attendance.student.user.get_full_name()} - {self.attendance.date} - {self.attendance.status}"
        self.assertEqual(str(self.attendance), expected)

    def test_attendance_status(self):
        valid_statuses = ['present', 'absent', 'late', 'excused']
        self.assertIn(self.attendance.status, valid_statuses)


class AcademicAPITest(APITestCase):
    def setUp(self):
        self.admin_user = UserFactory(role='administrator')
        self.teacher_user = UserFactory(role='teacher')

    def test_level_list_as_administrator(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/academics/levels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_class_list_as_administrator(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/academics/classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subject_list_as_administrator(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/academics/subjects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grade_list_as_teacher(self):
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get('/api/academics/grades/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attendance_list_as_teacher(self):
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get('/api/academics/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GradeCalculationTest(TestCase):
    def setUp(self):
        self.student = StudentFactory()
        self.subject = SubjectFactory(coefficient=Decimal('2.0'))
        self.exam_type1 = ExamTypeFactory(percentage=Decimal('30'))
        self.exam_type2 = ExamTypeFactory(percentage=Decimal('70'))
        self.trimester = TrimesterFactory()

    def test_grade_average_calculation(self):
        # Create grades for the same subject and trimester
        GradeFactory(
            student=self.student,
            subject=self.subject,
            exam_type=self.exam_type1,
            trimester=self.trimester,
            grade=Decimal('12.0')
        )
        GradeFactory(
            student=self.student,
            subject=self.subject,
            exam_type=self.exam_type2,
            trimester=self.trimester,
            grade=Decimal('16.0')
        )

        # Calculate weighted average
        grades = Grade.objects.filter(
            student=self.student,
            subject=self.subject,
            trimester=self.trimester
        )
        
        total_weighted_grade = Decimal('0')
        total_weight = Decimal('0')
        
        for grade in grades:
            weight = grade.exam_type.percentage / Decimal('100')
            total_weighted_grade += grade.grade * weight
            total_weight += weight
        
        if total_weight > 0:
            average = total_weighted_grade / total_weight
            self.assertGreater(average, Decimal('0'))
            self.assertLessEqual(average, Decimal('20'))
