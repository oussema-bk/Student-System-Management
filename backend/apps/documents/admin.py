from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Document, Bulletin, BulletinSubject, Attestation


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'document_type', 'language', 'generated_at', 'is_archived')
    list_filter = ('document_type', 'language', 'is_archived', 'generated_at')
    search_fields = ('title', 'student__user__first_name', 'student__user__last_name')
    ordering = ('-generated_at',)
    readonly_fields = ('generated_at', 'file_size')


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'trimester', 'class_name', 'total_average', 'class_rank')
    list_filter = ('academic_year', 'trimester', 'language', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'class_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'attendance_rate')


@admin.register(BulletinSubject)
class BulletinSubjectAdmin(admin.ModelAdmin):
    list_display = ('bulletin', 'subject_name', 'coefficient', 'average', 'teacher_name')
    list_filter = ('coefficient', 'bulletin__academic_year')
    search_fields = ('subject_name', 'subject_name_ar', 'teacher_name')
    ordering = ('bulletin', 'subject_name')


@admin.register(Attestation)
class AttestationAdmin(admin.ModelAdmin):
    list_display = ('student', 'attestation_type', 'academic_year', 'class_name', 'valid_from', 'valid_until')
    list_filter = ('attestation_type', 'language', 'academic_year', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'class_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)