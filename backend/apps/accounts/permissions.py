from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj == request.user


class IsAdministrator(permissions.BasePermission):
    """
    Permission to only allow administrators to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_administrator


class IsManager(permissions.BasePermission):
    """
    Permission to only allow managers to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class IsTeacher(permissions.BasePermission):
    """
    Permission to only allow teachers to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher


class IsParentOrStudent(permissions.BasePermission):
    """
    Permission to allow parents and students to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_parent or request.user.is_student)


class IsParentStudentOrTeacher(permissions.BasePermission):
    """
    Permission to allow parents, students, and teachers to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_parent or 
            request.user.is_student or 
            request.user.is_teacher
        )


class IsManagerOrAdministrator(permissions.BasePermission):
    """
    Permission to allow managers and administrators to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_manager or 
            request.user.is_administrator
        )


class IsTeacherOrAdministrator(permissions.BasePermission):
    """
    Permission to allow teachers and administrators to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_teacher or 
            request.user.is_administrator
        )


class CanViewStudentData(permissions.BasePermission):
    """
    Permission to view student data based on role and relationship.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Administrators and managers can view all student data
        if request.user.is_administrator or request.user.is_manager:
            return True
        
        # Teachers can view students in their classes
        if request.user.is_teacher:
            return True
        
        # Parents can view their own children's data
        if request.user.is_parent:
            return True
        
        # Students can view their own data
        if request.user.is_student:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Administrators and managers can view all student data
        if request.user.is_administrator or request.user.is_manager:
            return True
        
        # Teachers can view students in their classes
        if request.user.is_teacher:
            # Check if student is in teacher's classes
            teacher_profile = getattr(request.user, 'teacher_profile', None)
            if teacher_profile:
                return obj.enrollments.filter(
                    class_obj__subjects__teacher=teacher_profile
                ).exists()
        
        # Parents can view their own children's data
        if request.user.is_parent:
            parent_profile = getattr(request.user, 'parent_profile', None)
            if parent_profile:
                return parent_profile.children.filter(student=obj).exists()
        
        # Students can view their own data
        if request.user.is_student:
            return obj.user == request.user
        
        return False
