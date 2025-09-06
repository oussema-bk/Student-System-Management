from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model with role-based access control
    """
    ROLE_CHOICES = [
        ('parent', _('Parent')),
        ('student', _('Student')),
        ('teacher', _('Teacher')),
        ('administrator', _('Administrator')),
        ('manager', _('Manager')),
    ]
    
    LANGUAGE_CHOICES = [
        ('fr', _('French')),
        ('ar', _('Arabic')),
    ]
    
    email = models.EmailField(_('Email address'), unique=True)
    phone = models.CharField(_('Phone number'), max_length=20, blank=True)
    role = models.CharField(_('Role'), max_length=20, choices=ROLE_CHOICES)
    preferred_language = models.CharField(
        _('Preferred Language'), 
        max_length=2, 
        choices=LANGUAGE_CHOICES, 
        default='fr'
    )
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def is_parent(self):
        return self.role == 'parent'
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_administrator(self):
        return self.role == 'administrator'
    
    @property
    def is_manager(self):
        return self.role == 'manager'


class Institution(models.Model):
    """
    Educational institution model
    """
    name = models.CharField(_('Institution Name'), max_length=200)
    name_ar = models.CharField(_('Institution Name (Arabic)'), max_length=200, blank=True)
    address = models.TextField(_('Address'))
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    logo = models.ImageField(_('Logo'), upload_to='institutions/logos/', blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Parent(models.Model):
    """
    Parent model extending User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    profession = models.CharField(_('Profession'), max_length=100, blank=True)
    address = models.TextField(_('Address'), blank=True)
    emergency_contact = models.CharField(_('Emergency Contact'), max_length=20, blank=True)
    
    class Meta:
        verbose_name = _('Parent')
        verbose_name_plural = _('Parents')
    
    def __str__(self):
        return f"{self.user.get_full_name()} (Parent)"


class Student(models.Model):
    """
    Student model extending User
    """
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(_('Student ID'), max_length=20, unique=True)
    date_of_birth = models.DateField(_('Date of Birth'))
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(_('Address'), blank=True)
    emergency_contact = models.CharField(_('Emergency Contact'), max_length=20, blank=True)
    medical_info = models.TextField(_('Medical Information'), blank=True)
    photo = models.ImageField(_('Photo'), upload_to='students/photos/', blank=True)
    is_archived = models.BooleanField(_('Archived'), default=False)
    archived_at = models.DateTimeField(_('Archived at'), null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"


class Teacher(models.Model):
    """
    Teacher model extending User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(_('Teacher ID'), max_length=20, unique=True)
    specialization = models.CharField(_('Specialization'), max_length=100)
    hire_date = models.DateField(_('Hire Date'))
    salary = models.DecimalField(_('Salary'), max_digits=10, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(_('Photo'), upload_to='teachers/photos/', blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')
        ordering = ['teacher_id']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"


class ParentStudent(models.Model):
    """
    Relationship between parents and students
    """
    RELATIONSHIP_CHOICES = [
        ('father', _('Father')),
        ('mother', _('Mother')),
        ('guardian', _('Guardian')),
        ('other', _('Other')),
    ]
    
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    relationship = models.CharField(_('Relationship'), max_length=20, choices=RELATIONSHIP_CHOICES)
    is_primary = models.BooleanField(_('Primary Contact'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Parent-Student Relationship')
        verbose_name_plural = _('Parent-Student Relationships')
        unique_together = ['parent', 'student']
    
    def __str__(self):
        return f"{self.parent.user.get_full_name()} - {self.student.user.get_full_name()}"