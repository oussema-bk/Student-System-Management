from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Student, Institution


class Document(models.Model):
    """
    Document model for generated documents
    """
    DOCUMENT_TYPE_CHOICES = [
        ('bulletin', _('Bulletin Scolaire')),
        ('attestation_presence', _('Attestation de Présence')),
        ('attestation_inscription', _('Attestation d\'Inscription')),
        ('receipt', _('Receipt')),
        ('other', _('Other')),
    ]
    
    LANGUAGE_CHOICES = [
        ('fr', _('French')),
        ('ar', _('Arabic')),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(_('Document Type'), max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    language = models.CharField(_('Language'), max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    title = models.CharField(_('Title'), max_length=200)
    file_path = models.CharField(_('File Path'), max_length=500)
    file_size = models.PositiveIntegerField(_('File Size'), null=True, blank=True)
    generated_at = models.DateTimeField(_('Generated at'), auto_now_add=True)
    is_archived = models.BooleanField(_('Archived'), default=False)
    archived_at = models.DateTimeField(_('Archived at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} - {self.student.user.get_full_name()}"


class Bulletin(models.Model):
    """
    Bulletin scolaire model for detailed grade reports
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bulletins')
    academic_year = models.CharField(_('Academic Year'), max_length=20)
    trimester = models.CharField(_('Trimester'), max_length=50)
    class_name = models.CharField(_('Class'), max_length=100)
    language = models.CharField(_('Language'), max_length=2, choices=Document.LANGUAGE_CHOICES, default='fr')
    
    # Academic performance
    total_average = models.DecimalField(_('Total Average'), max_digits=5, decimal_places=2, null=True, blank=True)
    class_rank = models.PositiveIntegerField(_('Class Rank'), null=True, blank=True)
    level_rank = models.PositiveIntegerField(_('Level Rank'), null=True, blank=True)
    
    # Attendance
    total_days = models.PositiveIntegerField(_('Total Days'), default=0)
    present_days = models.PositiveIntegerField(_('Present Days'), default=0)
    absent_days = models.PositiveIntegerField(_('Absent Days'), default=0)
    attendance_rate = models.DecimalField(_('Attendance Rate'), max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Teacher notes
    teacher_notes = models.TextField(_('Teacher Notes'), blank=True)
    principal_notes = models.TextField(_('Principal Notes'), blank=True)
    
    # Document reference
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='bulletin')
    
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Bulletin')
        verbose_name_plural = _('Bulletins')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Bulletin {self.student.user.get_full_name()} - {self.academic_year} {self.trimester}"
    
    def save(self, *args, **kwargs):
        if self.total_days > 0:
            self.attendance_rate = (self.present_days / self.total_days) * 100
        super().save(*args, **kwargs)


class BulletinSubject(models.Model):
    """
    Subject grades within a bulletin
    """
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE, related_name='subjects')
    subject_name = models.CharField(_('Subject Name'), max_length=100)
    subject_name_ar = models.CharField(_('Subject Name (Arabic)'), max_length=100, blank=True)
    coefficient = models.DecimalField(_('Coefficient'), max_digits=3, decimal_places=1)
    average = models.DecimalField(_('Average'), max_digits=5, decimal_places=2)
    teacher_name = models.CharField(_('Teacher Name'), max_length=100, blank=True)
    teacher_notes = models.TextField(_('Teacher Notes'), blank=True)
    
    class Meta:
        verbose_name = _('Bulletin Subject')
        verbose_name_plural = _('Bulletin Subjects')
        ordering = ['subject_name']
    
    def __str__(self):
        return f"{self.subject_name} - {self.average}"


class Attestation(models.Model):
    """
    Attestation model for presence and enrollment confirmations
    """
    ATTESTATION_TYPE_CHOICES = [
        ('presence', _('Attestation de Présence')),
        ('inscription', _('Attestation d\'Inscription')),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attestations')
    attestation_type = models.CharField(_('Attestation Type'), max_length=20, choices=ATTESTATION_TYPE_CHOICES)
    language = models.CharField(_('Language'), max_length=2, choices=Document.LANGUAGE_CHOICES, default='fr')
    
    # Academic information
    academic_year = models.CharField(_('Academic Year'), max_length=20)
    class_name = models.CharField(_('Class'), max_length=100)
    level_name = models.CharField(_('Level'), max_length=100)
    
    # Validity period (for presence attestations)
    valid_from = models.DateField(_('Valid From'), null=True, blank=True)
    valid_until = models.DateField(_('Valid Until'), null=True, blank=True)
    
    # Document reference
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='attestation')
    
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Attestation')
        verbose_name_plural = _('Attestations')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_attestation_type_display()} - {self.student.user.get_full_name()}"