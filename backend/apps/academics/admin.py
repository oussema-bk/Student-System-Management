from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    AcademicYear, Level, Class, Subject, ExamType, Trimester,
    ClassSubject, StudentClass, Grade, Attendance
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'start_date')
    search_fields = ('name',)
    ordering = ('-start_date',)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_level', 'order', 'is_active')
    list_filter = ('is_active', 'parent_level')
    search_fields = ('name', 'name_ar')
    ordering = ('order', 'name')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'academic_year', 'capacity', 'is_active')
    list_filter = ('level', 'academic_year', 'is_active')
    search_fields = ('name', 'name_ar')
    ordering = ('level__order', 'name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'coefficient', 'is_active')
    list_filter = ('is_active', 'coefficient')
    search_fields = ('name', 'name_ar', 'code')
    ordering = ('name',)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'is_active')
    list_filter = ('is_active', 'percentage')
    search_fields = ('name', 'name_ar')
    ordering = ('name',)


@admin.register(Trimester)
class TrimesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'start_date', 'end_date', 'coefficient', 'is_active')
    list_filter = ('academic_year', 'is_active')
    search_fields = ('name', 'name_ar')
    ordering = ('academic_year', 'start_date')


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'subject', 'teacher', 'hours_per_week')
    list_filter = ('class_obj__academic_year', 'subject')
    search_fields = ('class_obj__name', 'subject__name', 'teacher__user__first_name')
    ordering = ('class_obj', 'subject')


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'enrollment_date', 'is_active')
    list_filter = ('class_obj__academic_year', 'is_active', 'enrollment_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'class_obj__name')
    ordering = ('-enrollment_date',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_type', 'trimester', 'grade', 'max_grade', 'created_at')
    list_filter = ('subject', 'exam_type', 'trimester', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'subject__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'date', 'status', 'teacher')
    list_filter = ('status', 'date', 'class_obj__academic_year')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'class_obj__name')
    ordering = ('-date',)
    readonly_fields = ('created_at',)