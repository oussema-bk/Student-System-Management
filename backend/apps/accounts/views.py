from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User, Institution, Parent, Student, Teacher, ParentStudent
from .serializers import (
    UserSerializer, InstitutionSerializer, ParentSerializer, 
    StudentSerializer, TeacherSerializer, ParentStudentSerializer,
    CustomTokenObtainPairSerializer, ChangePasswordSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdministrator, IsManager, IsTeacher, IsParentOrStudent


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view with additional user information
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'last_login']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsAdministrator]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        Create user with hashed password
        """
        password = serializer.validated_data.get('password')
        if password:
            serializer.validated_data['password'] = make_password(password)
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """
        Get users by role
        """
        role = request.query_params.get('role')
        if role:
            queryset = self.get_queryset().filter(role=role)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'Role parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class InstitutionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Institution management
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'name_ar', 'email']


class ParentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Parent management
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    def get_permissions(self):
        """
        Custom permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdministrator]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student management
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['gender', 'is_archived']
    search_fields = ['user__first_name', 'user__last_name', 'student_id']
    
    def get_permissions(self):
        """
        Custom permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdministrator]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get active students only
        """
        queryset = self.get_queryset().filter(is_archived=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Teacher management
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active', 'specialization']
    search_fields = ['user__first_name', 'user__last_name', 'teacher_id', 'specialization']
    
    def get_permissions(self):
        """
        Custom permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdministrator]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ParentStudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Parent-Student relationships
    """
    queryset = ParentStudent.objects.all()
    serializer_class = ParentStudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['relationship', 'is_primary']
    
    def get_permissions(self):
        """
        Custom permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdministrator]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProfileView(APIView):
    """
    Get current user profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Change user password
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': _('Password changed successfully')})
            else:
                return Response({'error': _('Old password is incorrect')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)