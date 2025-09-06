import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Institution, Parent, Student, Teacher, ParentStudent
from apps.accounts.permissions import IsAdministrator, IsManager, IsTeacher, CanViewStudentData
from factories import (
    UserFactory, InstitutionFactory, ParentFactory, StudentFactory, 
    TeacherFactory, ParentStudentFactory
)

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, self.user.email)
        self.assertTrue(self.user.is_active)

    def test_user_role_properties(self):
        # Test administrator
        admin_user = UserFactory(role='administrator')
        self.assertTrue(admin_user.is_administrator)
        self.assertFalse(admin_user.is_student)

        # Test student
        student_user = UserFactory(role='student')
        self.assertTrue(student_user.is_student)
        self.assertFalse(student_user.is_administrator)

        # Test teacher
        teacher_user = UserFactory(role='teacher')
        self.assertTrue(teacher_user.is_teacher)
        self.assertFalse(teacher_user.is_student)

        # Test parent
        parent_user = UserFactory(role='parent')
        self.assertTrue(parent_user.is_parent)
        self.assertFalse(parent_user.is_teacher)

        # Test manager
        manager_user = UserFactory(role='manager')
        self.assertTrue(manager_user.is_manager)
        self.assertFalse(manager_user.is_parent)


class InstitutionModelTest(TestCase):
    def setUp(self):
        self.institution = InstitutionFactory()

    def test_institution_creation(self):
        self.assertTrue(isinstance(self.institution, Institution))
        self.assertIsNotNone(self.institution.name)
        self.assertIsNotNone(self.institution.address)

    def test_institution_str_representation(self):
        self.assertEqual(str(self.institution), self.institution.name)


class ParentModelTest(TestCase):
    def setUp(self):
        self.parent = ParentFactory()

    def test_parent_creation(self):
        self.assertTrue(isinstance(self.parent, Parent))
        self.assertEqual(self.parent.user.role, 'parent')
        self.assertIsNotNone(self.parent.profession)

    def test_parent_str_representation(self):
        expected = f"{self.parent.user.get_full_name()} (Parent)"
        self.assertEqual(str(self.parent), expected)


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = StudentFactory()

    def test_student_creation(self):
        self.assertTrue(isinstance(self.student, Student))
        self.assertEqual(self.student.user.role, 'student')
        self.assertIsNotNone(self.student.student_id)
        self.assertIsNotNone(self.student.date_of_birth)

    def test_student_str_representation(self):
        expected = f"{self.student.user.get_full_name()} ({self.student.student_id})"
        self.assertEqual(str(self.student), expected)

    def test_student_age_calculation(self):
        from datetime import date
        today = date.today()
        age = today.year - self.student.date_of_birth.year
        self.assertGreaterEqual(age, 6)
        self.assertLessEqual(age, 18)


class TeacherModelTest(TestCase):
    def setUp(self):
        self.teacher = TeacherFactory()

    def test_teacher_creation(self):
        self.assertTrue(isinstance(self.teacher, Teacher))
        self.assertEqual(self.teacher.user.role, 'teacher')
        self.assertIsNotNone(self.teacher.teacher_id)
        self.assertIsNotNone(self.teacher.specialization)

    def test_teacher_str_representation(self):
        expected = f"{self.teacher.user.get_full_name()} ({self.teacher.teacher_id})"
        self.assertEqual(str(self.teacher), expected)


class ParentStudentModelTest(TestCase):
    def setUp(self):
        self.parent_student = ParentStudentFactory()

    def test_parent_student_creation(self):
        self.assertTrue(isinstance(self.parent_student, ParentStudent))
        self.assertIsNotNone(self.parent_student.parent)
        self.assertIsNotNone(self.parent_student.student)
        self.assertIsNotNone(self.parent_student.relationship)

    def test_parent_student_str_representation(self):
        expected = f"{self.parent_student.parent.user.get_full_name()} - {self.parent_student.student.user.get_full_name()}"
        self.assertEqual(str(self.parent_student), expected)


class UserAPITest(APITestCase):
    def setUp(self):
        self.admin_user = UserFactory(role='administrator')
        self.student_user = UserFactory(role='student')

    def test_user_list_as_administrator(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_as_non_administrator(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile_access(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get('/api/accounts/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.student_user.email)


class AuthenticationAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password('testpass123')
        self.user.save()

    def test_login_success(self):
        login_data = {
            'email': self.user.email,
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        login_data = {
            'email': self.user.email,
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionsTest(TestCase):
    def setUp(self):
        self.admin_user = UserFactory(role='administrator')
        self.manager_user = UserFactory(role='manager')
        self.teacher_user = UserFactory(role='teacher')
        self.parent_user = UserFactory(role='parent')
        self.student_user = UserFactory(role='student')

    def test_is_administrator_permission(self):
        permission = IsAdministrator()
        self.assertTrue(permission.has_permission(None, self.admin_user))
        self.assertFalse(permission.has_permission(None, self.student_user))

    def test_is_manager_permission(self):
        permission = IsManager()
        self.assertTrue(permission.has_permission(None, self.manager_user))
        self.assertFalse(permission.has_permission(None, self.student_user))

    def test_is_teacher_permission(self):
        permission = IsTeacher()
        self.assertTrue(permission.has_permission(None, self.teacher_user))
        self.assertFalse(permission.has_permission(None, self.student_user))

    def test_can_view_student_data_permission(self):
        permission = CanViewStudentData()
        
        # Administrators and managers can view all student data
        self.assertTrue(permission.has_permission(None, self.admin_user))
        self.assertTrue(permission.has_permission(None, self.manager_user))
        
        # Teachers can view student data
        self.assertTrue(permission.has_permission(None, self.teacher_user))
        
        # Parents can view student data
        self.assertTrue(permission.has_permission(None, self.parent_user))
        
        # Students can view student data
        self.assertTrue(permission.has_permission(None, self.student_user))
