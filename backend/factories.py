import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from faker import Faker
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

from apps.accounts.models import Institution, Parent, Student, Teacher, ParentStudent
from apps.academics.models import (
    AcademicYear, Level, Class, Subject, ExamType, Trimester,
    ClassSubject, StudentClass, Grade, Attendance
)
from apps.finance.models import Invoice, Payment, Receipt, Expense, FinancialReport
from apps.documents.models import Document, Bulletin, BulletinSubject, Attestation

fake = Faker()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.LazyAttribute(lambda obj: fake.email())
    username = factory.LazyAttribute(lambda obj: fake.user_name()[:20])
    first_name = factory.LazyAttribute(lambda obj: fake.first_name())
    last_name = factory.LazyAttribute(lambda obj: fake.last_name())
    phone = factory.LazyAttribute(lambda obj: fake.phone_number())
    role = factory.Iterator(['parent', 'student', 'teacher', 'administrator', 'manager'])
    preferred_language = factory.Iterator(['fr', 'ar'])
    is_active = True


class InstitutionFactory(DjangoModelFactory):
    class Meta:
        model = Institution
    
    name = factory.LazyAttribute(lambda obj: fake.company())
    name_ar = factory.LazyAttribute(lambda obj: f"مؤسسة {fake.company()}")
    address = factory.LazyAttribute(lambda obj: fake.address())
    phone = factory.LazyAttribute(lambda obj: fake.phone_number())
    email = factory.LazyAttribute(lambda obj: fake.email())


class ParentFactory(DjangoModelFactory):
    class Meta:
        model = Parent
    
    user = factory.SubFactory(UserFactory, role='parent')
    profession = factory.LazyAttribute(lambda obj: fake.job())
    address = factory.LazyAttribute(lambda obj: fake.address())
    emergency_contact = factory.LazyAttribute(lambda obj: fake.phone_number())


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student
    
    user = factory.SubFactory(UserFactory, role='student')
    student_id = factory.LazyAttribute(lambda obj: f"STU{fake.random_number(digits=6)}")
    date_of_birth = factory.LazyAttribute(lambda obj: fake.date_of_birth(minimum_age=6, maximum_age=18))
    gender = factory.Iterator(['M', 'F'])
    address = factory.LazyAttribute(lambda obj: fake.address())
    emergency_contact = factory.LazyAttribute(lambda obj: fake.phone_number())
    medical_info = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    is_archived = False


class TeacherFactory(DjangoModelFactory):
    class Meta:
        model = Teacher
    
    user = factory.SubFactory(UserFactory, role='teacher')
    teacher_id = factory.LazyAttribute(lambda obj: f"TCH{fake.random_number(digits=6)}")
    specialization = factory.LazyAttribute(lambda obj: fake.job())
    hire_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-5y', end_date='today'))
    salary = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=800, max=2000)))
    is_active = True


class ParentStudentFactory(DjangoModelFactory):
    class Meta:
        model = ParentStudent
    
    parent = factory.SubFactory(ParentFactory)
    student = factory.SubFactory(StudentFactory)
    relationship = factory.Iterator(['father', 'mother', 'guardian', 'other'])
    is_primary = factory.LazyAttribute(lambda obj: fake.boolean())


class AcademicYearFactory(DjangoModelFactory):
    class Meta:
        model = AcademicYear
    
    name = factory.LazyAttribute(lambda obj: f"{fake.year()}-{fake.year() + 1}")
    start_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-1y', end_date='today'))
    end_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='today', end_date='+1y'))
    is_current = factory.LazyAttribute(lambda obj: fake.boolean())


class LevelFactory(DjangoModelFactory):
    class Meta:
        model = Level
    
    name = factory.Iterator([
        'Primaire', '6ème', '5ème', '4ème', '3ème', '2ème', '1ère', 'Terminale',
        '3ème section Maths 1', '4ème section Maths 1', '3ème section Sciences'
    ])
    name_ar = factory.LazyAttribute(lambda obj: f"المستوى {obj.name}")
    parent_level = None
    order = factory.LazyAttribute(lambda obj: fake.random_int(min=1, max=10))
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    is_active = True


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = Class
    
    name = factory.LazyAttribute(lambda obj: f"{fake.word().title()} {fake.random_int(min=1, max=5)}")
    name_ar = factory.LazyAttribute(lambda obj: f"الفصل {obj.name}")
    level = factory.SubFactory(LevelFactory)
    academic_year = factory.SubFactory(AcademicYearFactory)
    capacity = factory.LazyAttribute(lambda obj: fake.random_int(min=20, max=35))
    is_active = True


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject
    
    name = factory.Iterator([
        'Mathématiques', 'Français', 'Arabe', 'Anglais', 'Sciences', 'Histoire',
        'Géographie', 'Éducation Physique', 'Informatique', 'Physique', 'Chimie'
    ])
    name_ar = factory.LazyAttribute(lambda obj: f"مادة {obj.name}")
    code = factory.LazyAttribute(lambda obj: f"SUB{fake.random_number(digits=3)}")
    coefficient = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=1, max=4)))
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    is_active = True


class ExamTypeFactory(DjangoModelFactory):
    class Meta:
        model = ExamType
    
    name = factory.Iterator(['Contrôle', 'Devoir', 'Oral', 'Examen Final', 'Composition'])
    name_ar = factory.LazyAttribute(lambda obj: f"نوع الامتحان {obj.name}")
    percentage = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=10, max=50)))
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    is_active = True


class TrimesterFactory(DjangoModelFactory):
    class Meta:
        model = Trimester
    
    name = factory.Iterator(['1er Trimestre', '2ème Trimestre', '3ème Trimestre'])
    name_ar = factory.LazyAttribute(lambda obj: f"الثلث {obj.name}")
    academic_year = factory.SubFactory(AcademicYearFactory)
    start_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-6m', end_date='today'))
    end_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='today', end_date='+6m'))
    coefficient = factory.LazyAttribute(lambda obj: Decimal('1.0'))
    is_active = True


class ClassSubjectFactory(DjangoModelFactory):
    class Meta:
        model = ClassSubject
    
    class_obj = factory.SubFactory(ClassFactory)
    subject = factory.SubFactory(SubjectFactory)
    teacher = factory.SubFactory(TeacherFactory)
    hours_per_week = factory.LazyAttribute(lambda obj: fake.random_int(min=1, max=6))


class StudentClassFactory(DjangoModelFactory):
    class Meta:
        model = StudentClass
    
    student = factory.SubFactory(StudentFactory)
    class_obj = factory.SubFactory(ClassFactory)
    enrollment_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-1y', end_date='today'))
    is_active = True


class GradeFactory(DjangoModelFactory):
    class Meta:
        model = Grade
    
    student = factory.SubFactory(StudentFactory)
    subject = factory.SubFactory(SubjectFactory)
    exam_type = factory.SubFactory(ExamTypeFactory)
    trimester = factory.SubFactory(TrimesterFactory)
    grade = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=0, max=20)))
    max_grade = factory.LazyAttribute(lambda obj: Decimal('20.00'))
    teacher_notes = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))


class AttendanceFactory(DjangoModelFactory):
    class Meta:
        model = Attendance
    
    student = factory.SubFactory(StudentFactory)
    class_obj = factory.SubFactory(ClassFactory)
    date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-30d', end_date='today'))
    status = factory.Iterator(['present', 'absent', 'late', 'excused'])
    teacher = factory.SubFactory(TeacherFactory)
    notes = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=100))


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice
    
    invoice_number = factory.LazyAttribute(lambda obj: f"INV{fake.random_number(digits=8)}")
    invoice_type = factory.Iterator(['tuition', 'salary', 'expense', 'other'])
    student = factory.SubFactory(StudentFactory)
    amount = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=100, max=2000)))
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    due_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='today', end_date='+30d'))
    status = factory.Iterator(['pending', 'paid', 'overdue', 'cancelled'])
    manager = factory.SubFactory(UserFactory, role='manager')


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment
    
    invoice = factory.SubFactory(InvoiceFactory)
    amount = factory.LazyAttribute(lambda obj: obj.invoice.amount)
    payment_method = factory.Iterator(['cash', 'bank_transfer', 'cheque', 'card'])
    payment_date = factory.LazyAttribute(lambda obj: fake.date_time_between(start_date='-30d', end_date='now'))
    reference_number = factory.LazyAttribute(lambda obj: f"REF{fake.random_number(digits=8)}")
    status = factory.Iterator(['pending', 'completed', 'failed', 'refunded'])
    notes = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=100))


class ReceiptFactory(DjangoModelFactory):
    class Meta:
        model = Receipt
    
    payment = factory.SubFactory(PaymentFactory)
    receipt_number = factory.LazyAttribute(lambda obj: f"RCP{fake.random_number(digits=8)}")
    file_path = factory.LazyAttribute(lambda obj: f"receipts/{obj.receipt_number}.pdf")


class ExpenseFactory(DjangoModelFactory):
    class Meta:
        model = Expense
    
    title = factory.LazyAttribute(lambda obj: fake.sentence(nb_words=4))
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    amount = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=50, max=1000)))
    category = factory.Iterator(['utilities', 'maintenance', 'supplies', 'equipment', 'transportation', 'other'])
    expense_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-30d', end_date='today'))
    manager = factory.SubFactory(UserFactory, role='manager')


class FinancialReportFactory(DjangoModelFactory):
    class Meta:
        model = FinancialReport
    
    title = factory.LazyAttribute(lambda obj: f"Rapport Financier {fake.month_name()} {fake.year()}")
    report_type = factory.Iterator(['monthly', 'yearly', 'custom'])
    start_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-1y', end_date='today'))
    end_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date='today', end_date='+1y'))
    total_income = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=10000, max=100000)))
    total_expenses = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=5000, max=80000)))
    generated_by = factory.SubFactory(UserFactory, role='manager')


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document
    
    student = factory.SubFactory(StudentFactory)
    document_type = factory.Iterator(['bulletin', 'attestation_presence', 'attestation_inscription', 'receipt', 'other'])
    language = factory.Iterator(['fr', 'ar'])
    title = factory.LazyAttribute(lambda obj: f"{obj.document_type.title()} - {obj.student.user.get_full_name()}")
    file_path = factory.LazyAttribute(lambda obj: f"documents/{obj.document_type}_{obj.student.student_id}_{obj.language}.pdf")
    file_size = factory.LazyAttribute(lambda obj: fake.random_int(min=1000, max=1000000))
    is_archived = False


class BulletinFactory(DjangoModelFactory):
    class Meta:
        model = Bulletin
    
    student = factory.SubFactory(StudentFactory)
    academic_year = factory.LazyAttribute(lambda obj: f"{fake.year()}-{fake.year() + 1}")
    trimester = factory.Iterator(['1er Trimestre', '2ème Trimestre', '3ème Trimestre'])
    class_name = factory.LazyAttribute(lambda obj: f"Classe {fake.random_int(min=1, max=5)}")
    language = factory.Iterator(['fr', 'ar'])
    total_average = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=8, max=18)))
    class_rank = factory.LazyAttribute(lambda obj: fake.random_int(min=1, max=30))
    level_rank = factory.LazyAttribute(lambda obj: fake.random_int(min=1, max=100))
    total_days = factory.LazyAttribute(lambda obj: fake.random_int(min=80, max=120))
    present_days = factory.LazyAttribute(lambda obj: fake.random_int(min=70, max=obj.total_days))
    absent_days = factory.LazyAttribute(lambda obj: obj.total_days - obj.present_days)
    teacher_notes = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    principal_notes = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    document = factory.SubFactory(DocumentFactory, document_type='bulletin')


class BulletinSubjectFactory(DjangoModelFactory):
    class Meta:
        model = BulletinSubject
    
    bulletin = factory.SubFactory(BulletinFactory)
    subject_name = factory.LazyAttribute(lambda obj: fake.word().title())
    subject_name_ar = factory.LazyAttribute(lambda obj: f"مادة {obj.subject_name}")
    coefficient = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=1, max=4)))
    average = factory.LazyAttribute(lambda obj: Decimal(fake.random_int(min=8, max=18)))
    teacher_name = factory.LazyAttribute(lambda obj: fake.name())
    teacher_notes = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=100))


class AttestationFactory(DjangoModelFactory):
    class Meta:
        model = Attestation
    
    student = factory.SubFactory(StudentFactory)
    attestation_type = factory.Iterator(['presence', 'inscription'])
    language = factory.Iterator(['fr', 'ar'])
    academic_year = factory.LazyAttribute(lambda obj: f"{fake.year()}-{fake.year() + 1}")
    class_name = factory.LazyAttribute(lambda obj: f"Classe {fake.random_int(min=1, max=5)}")
    level_name = factory.LazyAttribute(lambda obj: fake.word().title())
    valid_from = factory.LazyAttribute(lambda obj: fake.date_between(start_date='-30d', end_date='today'))
    valid_until = factory.LazyAttribute(lambda obj: fake.date_between(start_date='today', end_date='+30d'))
    document = factory.SubFactory(DocumentFactory, document_type='attestation_presence')
