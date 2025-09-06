from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Institution, Parent, Student, Teacher, ParentStudent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'preferred_language')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'name_ar', 'email')
    list_filter = ('created_at',)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession', 'emergency_contact')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    list_filter = ('user__created_at',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'date_of_birth', 'gender', 'is_archived')
    search_fields = ('user__first_name', 'user__last_name', 'student_id')
    list_filter = ('gender', 'is_archived', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id', 'specialization', 'hire_date', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'teacher_id', 'specialization')
    list_filter = ('is_active', 'hire_date', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ParentStudent)
class ParentStudentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'relationship', 'is_primary')
    search_fields = ('parent__user__first_name', 'parent__user__last_name', 'student__user__first_name', 'student__user__last_name')
    list_filter = ('relationship', 'is_primary', 'created_at')