from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Institution, Student, Teacher


class AcademicYear(models.Model):
    """
    Academic year model
    """
    name = models.CharField(_('Academic Year'), max_length=20, unique=True)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    is_current = models.BooleanField(_('Current Year'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Academic Year')
        verbose_name_plural = _('Academic Years')
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class Level(models.Model):
    """
    Hierarchical level model (e.g., Primaire → 3ème section Maths 1)
    """
    name = models.CharField(_('Level Name'), max_length=100)
    name_ar = models.CharField(_('Level Name (Arabic)'), max_length=100, blank=True)
    parent_level = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sublevels')
    order = models.PositiveIntegerField(_('Order'), default=0)
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Class(models.Model):
    """
    Class model belonging to a level and academic year
    """
    name = models.CharField(_('Class Name'), max_length=100)
    name_ar = models.CharField(_('Class Name (Arabic)'), max_length=100, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='classes')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classes')
    capacity = models.PositiveIntegerField(_('Capacity'), default=30)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Class')
        verbose_name_plural = _('Classes')
        ordering = ['level__order', 'name']
        unique_together = ['name', 'academic_year']
    
    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"


class Subject(models.Model):
    """
    Subject model with coefficient
    """
    name = models.CharField(_('Subject Name'), max_length=100)
    name_ar = models.CharField(_('Subject Name (Arabic)'), max_length=100, blank=True)
    code = models.CharField(_('Subject Code'), max_length=10, unique=True)
    coefficient = models.DecimalField(_('Coefficient'), max_digits=3, decimal_places=1, default=1.0)
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (Coef: {self.coefficient})"


class ExamType(models.Model):
    """
    Exam type model with percentage weight
    """
    name = models.CharField(_('Exam Type'), max_length=50)
    name_ar = models.CharField(_('Exam Type (Arabic)'), max_length=50, blank=True)
    percentage = models.DecimalField(_('Percentage'), max_digits=5, decimal_places=2, default=100.00)
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Exam Type')
        verbose_name_plural = _('Exam Types')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Trimester(models.Model):
    """
    Trimester/Semester model with coefficient
    """
    name = models.CharField(_('Trimester Name'), max_length=50)
    name_ar = models.CharField(_('Trimester Name (Arabic)'), max_length=50, blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='trimesters')
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    coefficient = models.DecimalField(_('Coefficient'), max_digits=3, decimal_places=1, default=1.0)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Trimester')
        verbose_name_plural = _('Trimesters')
        ordering = ['academic_year', 'start_date']
    
    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"


class ClassSubject(models.Model):
    """
    Many-to-many relationship between classes and subjects
    """
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='teaching_subjects')
    hours_per_week = models.PositiveIntegerField(_('Hours per Week'), default=1)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Class Subject')
        verbose_name_plural = _('Class Subjects')
        unique_together = ['class_obj', 'subject']
    
    def __str__(self):
        return f"{self.class_obj.name} - {self.subject.name}"


class StudentClass(models.Model):
    """
    Student enrollment in classes
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    enrollment_date = models.DateField(_('Enrollment Date'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Student Class')
        verbose_name_plural = _('Student Classes')
        unique_together = ['student', 'class_obj']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.class_obj.name}"


class Grade(models.Model):
    """
    Grade model for student performance
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='grades')
    trimester = models.ForeignKey(Trimester, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(_('Grade'), max_digits=5, decimal_places=2)
    max_grade = models.DecimalField(_('Maximum Grade'), max_digits=5, decimal_places=2, default=20.00)
    teacher_notes = models.TextField(_('Teacher Notes'), blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Grade')
        verbose_name_plural = _('Grades')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name}: {self.grade}/{self.max_grade}"
    
    @property
    def percentage(self):
        """Calculate percentage grade"""
        return (self.grade / self.max_grade) * 100


class Attendance(models.Model):
    """
    Attendance tracking model
    """
    STATUS_CHOICES = [
        ('present', _('Present')),
        ('absent', _('Absent')),
        ('late', _('Late')),
        ('excused', _('Excused')),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(_('Date'))
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendance_records')
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendance Records')
        ordering = ['-date']
        unique_together = ['student', 'class_obj', 'date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date}: {self.get_status_display()}"