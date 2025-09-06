from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal
import random

from apps.accounts.models import Institution, Parent, Student, Teacher, ParentStudent
from apps.academics.models import (
    AcademicYear, Level, Class, Subject, ExamType, Trimester,
    ClassSubject, StudentClass, Grade, Attendance
)
from apps.finance.models import Invoice, Payment, Receipt, Expense, FinancialReport
from apps.documents.models import Document, Bulletin, BulletinSubject, Attestation

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate fake data for testing and development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--students',
            type=int,
            default=50,
            help='Number of students to create (default: 50)'
        )
        parser.add_argument(
            '--teachers',
            type=int,
            default=10,
            help='Number of teachers to create (default: 10)'
        )
        parser.add_argument(
            '--parents',
            type=int,
            default=30,
            help='Number of parents to create (default: 30)'
        )
        parser.add_argument(
            '--classes',
            type=int,
            default=8,
            help='Number of classes to create (default: 8)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        self.stdout.write('Generating fake data...')
        
        with transaction.atomic():
            # Create institution
            institution = self.create_institution()
            
            # Create academic year
            academic_year = self.create_academic_year()
            
            # Create levels
            levels = self.create_levels()
            
            # Create subjects
            subjects = self.create_subjects()
            
            # Create exam types
            exam_types = self.create_exam_types()
            
            # Create trimesters
            trimesters = self.create_trimesters(academic_year)
            
            # Create classes
            classes = self.create_classes(levels, academic_year, options['classes'])
            
            # Create teachers
            teachers = self.create_teachers(options['teachers'])
            
            # Create students
            students = self.create_students(options['students'])
            
            # Create parents
            parents = self.create_parents(options['parents'])
            
            # Create parent-student relationships
            self.create_parent_student_relationships(parents, students)
            
            # Assign teachers to classes
            self.assign_teachers_to_classes(teachers, classes, subjects)
            
            # Enroll students in classes
            self.enroll_students_in_classes(students, classes)
            
            # Create grades
            self.create_grades(students, subjects, exam_types, trimesters)
            
            # Create attendance records
            self.create_attendance_records(students, classes, teachers)
            
            # Create financial data
            self.create_financial_data(students, teachers)
            
            # Create documents
            self.create_documents(students, classes, academic_year, trimesters)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated fake data:\n'
                f'- {len(students)} students\n'
                f'- {len(teachers)} teachers\n'
                f'- {len(parents)} parents\n'
                f'- {len(classes)} classes\n'
                f'- {len(subjects)} subjects\n'
                f'- {len(levels)} levels\n'
                f'- {len(trimesters)} trimesters\n'
                f'- Financial records and documents'
            )
        )

    def clear_data(self):
        """Clear existing data"""
        models_to_clear = [
            Document, Bulletin, BulletinSubject, Attestation,
            FinancialReport, Expense, Receipt, Payment, Invoice,
            Attendance, Grade, StudentClass, ClassSubject,
            Trimester, ExamType, Subject, Class, Level, AcademicYear,
            ParentStudent, Student, Teacher, Parent, Institution, User
        ]
        
        for model in models_to_clear:
            count = model.objects.count()
            if count > 0:
                model.objects.all().delete()
                self.stdout.write(f'Cleared {count} {model.__name__} records')

    def create_institution(self):
        """Create institution"""
        institution, created = Institution.objects.get_or_create(
            name="École Privée Excellence",
            defaults={
                'name_ar': "مدرسة التميز الخاصة",
                'address': "123 Avenue Habib Bourguiba, Tunis 1000",
                'phone': "+216 71 123 456",
                'email': "contact@excellence.tn"
            }
        )
        if created:
            self.stdout.write(f'Created institution: {institution.name}')
        return institution

    def create_academic_year(self):
        """Create academic year"""
        academic_year, created = AcademicYear.objects.get_or_create(
            name="2024-2025",
            defaults={
                'start_date': '2024-09-15',
                'end_date': '2025-06-30',
                'is_current': True
            }
        )
        if created:
            self.stdout.write(f'Created academic year: {academic_year.name}')
        return academic_year

    def create_levels(self):
        """Create educational levels"""
        level_data = [
            ('Primaire', 'الابتدائي', 1),
            ('6ème', 'السادسة', 2),
            ('5ème', 'الخامسة', 3),
            ('4ème', 'الرابعة', 4),
            ('3ème', 'الثالثة', 5),
            ('2ème', 'الثانية', 6),
            ('1ère', 'الأولى', 7),
            ('Terminale', 'البكالوريا', 8),
        ]
        
        levels = []
        for name, name_ar, order in level_data:
            level, created = Level.objects.get_or_create(
                name=name,
                defaults={
                    'name_ar': name_ar,
                    'order': order,
                    'description': f'Level {name} description',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created level: {level.name}')
            levels.append(level)
        
        return levels

    def create_subjects(self):
        """Create subjects"""
        subject_data = [
            ('Mathématiques', 'الرياضيات', 'MATH', 3),
            ('Français', 'الفرنسية', 'FR', 2),
            ('Arabe', 'العربية', 'AR', 2),
            ('Anglais', 'الإنجليزية', 'EN', 2),
            ('Sciences', 'العلوم', 'SCI', 2),
            ('Histoire', 'التاريخ', 'HIST', 1),
            ('Géographie', 'الجغرافيا', 'GEO', 1),
            ('Éducation Physique', 'التربية البدنية', 'EPS', 1),
            ('Informatique', 'المعلوماتية', 'INFO', 1),
            ('Physique', 'الفيزياء', 'PHY', 2),
            ('Chimie', 'الكيمياء', 'CHIM', 2),
        ]
        
        subjects = []
        for name, name_ar, code, coefficient in subject_data:
            subject, created = Subject.objects.get_or_create(
                name=name,
                defaults={
                    'name_ar': name_ar,
                    'code': code,
                    'coefficient': Decimal(str(coefficient)),
                    'description': f'Subject {name} description',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created subject: {subject.name}')
            subjects.append(subject)
        
        return subjects

    def create_exam_types(self):
        """Create exam types"""
        exam_type_data = [
            ('Contrôle', 'المراقبة', 30),
            ('Devoir', 'الواجب', 25),
            ('Oral', 'الشفوي', 20),
            ('Examen Final', 'الامتحان النهائي', 25),
        ]
        
        exam_types = []
        for name, name_ar, percentage in exam_type_data:
            exam_type, created = ExamType.objects.get_or_create(
                name=name,
                defaults={
                    'name_ar': name_ar,
                    'percentage': Decimal(str(percentage)),
                    'description': f'Exam type {name} description',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created exam type: {exam_type.name}')
            exam_types.append(exam_type)
        
        return exam_types

    def create_trimesters(self, academic_year):
        """Create trimesters"""
        trimester_data = [
            ('1er Trimestre', 'الثلث الأول', '2024-09-15', '2024-12-15'),
            ('2ème Trimestre', 'الثلث الثاني', '2024-12-16', '2025-03-15'),
            ('3ème Trimestre', 'الثلث الثالث', '2025-03-16', '2025-06-30'),
        ]
        
        trimesters = []
        for name, name_ar, start_date, end_date in trimester_data:
            trimester, created = Trimester.objects.get_or_create(
                name=name,
                academic_year=academic_year,
                defaults={
                    'name_ar': name_ar,
                    'start_date': start_date,
                    'end_date': end_date,
                    'coefficient': Decimal('1.0'),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created trimester: {trimester.name}')
            trimesters.append(trimester)
        
        return trimesters

    def create_classes(self, levels, academic_year, num_classes):
        """Create classes"""
        classes = []
        for i in range(num_classes):
            level = random.choice(levels)
            class_name = f"{level.name} {chr(65 + i)}"  # A, B, C, etc.
            
            class_obj, created = Class.objects.get_or_create(
                name=class_name,
                level=level,
                academic_year=academic_year,
                defaults={
                    'name_ar': f"الفصل {class_name}",
                    'capacity': random.randint(20, 35),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created class: {class_obj.name}')
            classes.append(class_obj)
        
        return classes

    def create_teachers(self, num_teachers):
        """Create teachers"""
        teachers = []
        specializations = [
            'Mathématiques', 'Français', 'Arabe', 'Anglais', 'Sciences',
            'Histoire', 'Géographie', 'Éducation Physique', 'Informatique',
            'Physique', 'Chimie'
        ]
        
        for i in range(num_teachers):
            user = User.objects.create_user(
                email=f'teacher{i+1}@excellence.tn',
                username=f'teacher{i+1}',
                first_name=f'Teacher{i+1}',
                last_name=f'LastName{i+1}',
                role='teacher',
                preferred_language='fr',
                phone=f'+216 71 123 {456 + i}'
            )
            
            teacher = Teacher.objects.create(
                user=user,
                teacher_id=f'TCH{i+1:04d}',
                specialization=random.choice(specializations),
                hire_date='2020-09-01',
                salary=Decimal(str(random.randint(1200, 2000))),
                is_active=True
            )
            
            teachers.append(teacher)
            self.stdout.write(f'Created teacher: {teacher.user.get_full_name()}')
        
        return teachers

    def create_students(self, num_students):
        """Create students"""
        students = []
        genders = ['M', 'F']
        
        for i in range(num_students):
            user = User.objects.create_user(
                email=f'student{i+1}@excellence.tn',
                username=f'student{i+1}',
                first_name=f'Student{i+1}',
                last_name=f'LastName{i+1}',
                role='student',
                preferred_language='fr',
                phone=f'+216 71 123 {556 + i}'
            )
            
            student = Student.objects.create(
                user=user,
                student_id=f'STU{i+1:06d}',
                date_of_birth=f'201{random.randint(0, 8)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                gender=random.choice(genders),
                address=f'Address {i+1}, Tunis',
                emergency_contact=f'+216 71 123 {656 + i}',
                medical_info=f'Medical info for student {i+1}',
                is_archived=False
            )
            
            students.append(student)
            if i % 10 == 0:  # Log every 10 students
                self.stdout.write(f'Created {i+1} students...')
        
        self.stdout.write(f'Created {len(students)} students')
        return students

    def create_parents(self, num_parents):
        """Create parents"""
        parents = []
        professions = [
            'Ingénieur', 'Médecin', 'Avocat', 'Enseignant', 'Comptable',
            'Architecte', 'Pharmacien', 'Vétérinaire', 'Journaliste', 'Artiste'
        ]
        
        for i in range(num_parents):
            user = User.objects.create_user(
                email=f'parent{i+1}@excellence.tn',
                username=f'parent{i+1}',
                first_name=f'Parent{i+1}',
                last_name=f'LastName{i+1}',
                role='parent',
                preferred_language='fr',
                phone=f'+216 71 123 {756 + i}'
            )
            
            parent = Parent.objects.create(
                user=user,
                profession=random.choice(professions),
                address=f'Parent Address {i+1}, Tunis',
                emergency_contact=f'+216 71 123 {856 + i}'
            )
            
            parents.append(parent)
            if i % 10 == 0:  # Log every 10 parents
                self.stdout.write(f'Created {i+1} parents...')
        
        self.stdout.write(f'Created {len(parents)} parents')
        return parents

    def create_parent_student_relationships(self, parents, students):
        """Create parent-student relationships"""
        relationships = ['father', 'mother', 'guardian']
        
        for student in students:
            # Assign 1-2 parents per student
            num_parents = random.randint(1, 2)
            selected_parents = random.sample(parents, min(num_parents, len(parents)))
            
            for i, parent in enumerate(selected_parents):
                ParentStudent.objects.create(
                    parent=parent,
                    student=student,
                    relationship=relationships[i] if i < len(relationships) else 'other',
                    is_primary=(i == 0)
                )
        
        self.stdout.write(f'Created parent-student relationships')

    def assign_teachers_to_classes(self, teachers, classes, subjects):
        """Assign teachers to classes and subjects"""
        for class_obj in classes:
            # Assign 3-5 subjects per class
            class_subjects = random.sample(subjects, min(random.randint(3, 5), len(subjects)))
            
            for subject in class_subjects:
                teacher = random.choice(teachers)
                ClassSubject.objects.create(
                    class_obj=class_obj,
                    subject=subject,
                    teacher=teacher,
                    hours_per_week=random.randint(1, 4)
                )
        
        self.stdout.write(f'Assigned teachers to classes and subjects')

    def enroll_students_in_classes(self, students, classes):
        """Enroll students in classes"""
        for student in students:
            # Each student is enrolled in 1 class
            class_obj = random.choice(classes)
            StudentClass.objects.create(
                student=student,
                class_obj=class_obj,
                enrollment_date='2024-09-15',
                is_active=True
            )
        
        self.stdout.write(f'Enrolled students in classes')

    def create_grades(self, students, subjects, exam_types, trimesters):
        """Create grades for students"""
        for student in students:
            student_class = StudentClass.objects.filter(student=student, is_active=True).first()
            if not student_class:
                continue
                
            class_subjects = ClassSubject.objects.filter(class_obj=student_class.class_obj)
            
            for trimester in trimesters:
                for class_subject in class_subjects:
                    # Create 2-4 grades per subject per trimester
                    num_grades = random.randint(2, 4)
                    selected_exam_types = random.sample(exam_types, min(num_grades, len(exam_types)))
                    
                    for exam_type in selected_exam_types:
                        Grade.objects.create(
                            student=student,
                            subject=class_subject.subject,
                            exam_type=exam_type,
                            trimester=trimester,
                            grade=Decimal(str(random.randint(8, 18))),
                            max_grade=Decimal('20.00'),
                            teacher_notes=f'Grade notes for {student.user.get_full_name()}'
                        )
        
        self.stdout.write(f'Created grades for students')

    def create_attendance_records(self, students, classes, teachers):
        """Create attendance records"""
        from datetime import date, timedelta
        
        start_date = date(2024, 9, 15)
        end_date = date(2024, 12, 15)
        
        current_date = start_date
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                for student in students:
                    student_class = StudentClass.objects.filter(student=student, is_active=True).first()
                    if not student_class:
                        continue
                    
                    # 90% attendance rate
                    if random.random() < 0.9:
                        status = 'present'
                    else:
                        status = random.choice(['absent', 'late', 'excused'])
                    
                    teacher = random.choice(teachers)
                    
                    Attendance.objects.create(
                        student=student,
                        class_obj=student_class.class_obj,
                        date=current_date,
                        status=status,
                        teacher=teacher,
                        notes=f'Attendance notes for {current_date}'
                    )
            
            current_date += timedelta(days=1)
        
        self.stdout.write(f'Created attendance records')

    def create_financial_data(self, students, teachers):
        """Create financial data"""
        # Create a manager user if none exists
        manager_user, created = User.objects.get_or_create(
            email='manager@excellence.tn',
            defaults={
                'username': 'manager',
                'first_name': 'Manager',
                'last_name': 'User',
                'role': 'manager',
                'preferred_language': 'fr',
                'phone': '+216 71 123 999'
            }
        )
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
            self.stdout.write(f'Created manager user: {manager_user.get_full_name()}')
        
        # Create invoices for students
        for student in students:
            Invoice.objects.create(
                invoice_number=f'INV{student.student_id}',
                invoice_type='tuition',
                student=student,
                amount=Decimal('1200.00'),
                description=f'Tuition fees for {student.user.get_full_name()}',
                due_date='2024-12-31',
                status=random.choice(['pending', 'paid', 'overdue']),
                manager=manager_user
            )
        
        # Create invoices for teachers
        for teacher in teachers:
            Invoice.objects.create(
                invoice_number=f'SAL{teacher.teacher_id}',
                invoice_type='salary',
                amount=teacher.salary,
                description=f'Salary for {teacher.user.get_full_name()}',
                due_date='2024-12-31',
                status='paid',
                manager=manager_user
            )
        
        # Create some payments
        invoices = Invoice.objects.filter(status='paid')
        for invoice in invoices:
            Payment.objects.create(
                invoice=invoice,
                amount=invoice.amount,
                payment_method=random.choice(['cash', 'bank_transfer', 'cheque']),
                payment_date='2024-11-15',
                reference_number=f'PAY{random.randint(100000, 999999)}',
                status='completed',
                notes=f'Payment for invoice {invoice.invoice_number}'
            )
        
        self.stdout.write(f'Created financial data')

    def create_documents(self, students, classes, academic_year, trimesters):
        """Create documents"""
        for student in students:
            student_class = StudentClass.objects.filter(student=student, is_active=True).first()
            if not student_class:
                continue
            
            # Create document first
            document = Document.objects.create(
                student=student,
                document_type='bulletin',
                language='fr',
                title=f'Bulletin - {student.user.get_full_name()}',
                file_path=f'documents/bulletin_{student.student_id}_fr.pdf',
                file_size=random.randint(1000, 1000000),
                is_archived=False
            )
            
            # Create bulletin
            bulletin = Bulletin.objects.create(
                student=student,
                academic_year=academic_year.name,
                trimester=random.choice(trimesters).name,
                class_name=student_class.class_obj.name,
                language='fr',
                total_average=Decimal(str(random.randint(10, 16))),
                class_rank=random.randint(1, 30),
                level_rank=random.randint(1, 100),
                total_days=random.randint(80, 120),
                present_days=random.randint(70, 120),
                absent_days=random.randint(0, 20),
                teacher_notes=f'Teacher notes for {student.user.get_full_name()}',
                principal_notes=f'Principal notes for {student.user.get_full_name()}',
                document=document
            )
            
            # Create bulletin subjects
            class_subjects = ClassSubject.objects.filter(class_obj=student_class.class_obj)
            for class_subject in class_subjects:
                BulletinSubject.objects.create(
                    bulletin=bulletin,
                    subject_name=class_subject.subject.name,
                    subject_name_ar=class_subject.subject.name_ar,
                    coefficient=class_subject.subject.coefficient,
                    average=Decimal(str(random.randint(8, 18))),
                    teacher_name=class_subject.teacher.user.get_full_name(),
                    teacher_notes=f'Subject notes for {class_subject.subject.name}'
                )
            
            # Create attestation
            attestation_document = Document.objects.create(
                student=student,
                document_type='attestation_presence',
                language='fr',
                title=f'Attestation de Présence - {student.user.get_full_name()}',
                file_path=f'documents/attestation_{student.student_id}_fr.pdf',
                file_size=random.randint(1000, 1000000),
                is_archived=False
            )
            
            Attestation.objects.create(
                student=student,
                attestation_type='presence',
                language='fr',
                academic_year=academic_year.name,
                class_name=student_class.class_obj.name,
                level_name=student_class.class_obj.level.name,
                valid_from='2024-09-15',
                valid_until='2025-06-30',
                document=attestation_document
            )
        
        self.stdout.write(f'Created documents')
