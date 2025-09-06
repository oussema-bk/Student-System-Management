from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count, Q
from decimal import Decimal

from .models import (
    AcademicYear, Level, Class, Subject, ExamType, Trimester,
    ClassSubject, StudentClass, Grade, Attendance
)
from .serializers import (
    AcademicYearSerializer, LevelSerializer, ClassSerializer, SubjectSerializer,
    ExamTypeSerializer, TrimesterSerializer, ClassSubjectSerializer,
    StudentClassSerializer, GradeSerializer, AttendanceSerializer
)
from apps.accounts.permissions import IsAdministrator, IsTeacherOrAdministrator, CanViewStudentData


class AcademicYearViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Academic Year management
    """
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    ordering = ['-start_date']


class LevelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Level management
    """
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active', 'parent_level']
    search_fields = ['name', 'name_ar']
    ordering = ['order', 'name']


class ClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Class management
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['level', 'academic_year', 'is_active']
    search_fields = ['name', 'name_ar']
    ordering = ['level__order', 'name']


class SubjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Subject management
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'name_ar', 'code']
    ordering = ['name']


class ExamTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Exam Type management
    """
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'name_ar']
    ordering = ['name']


class TrimesterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trimester management
    """
    queryset = Trimester.objects.all()
    serializer_class = TrimesterSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['academic_year', 'is_active']
    search_fields = ['name', 'name_ar']
    ordering = ['academic_year', 'start_date']


class ClassSubjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Class-Subject relationships
    """
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_obj', 'subject', 'teacher']


class StudentClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student-Class enrollments
    """
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'class_obj', 'is_active']


class GradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Grade management
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrAdministrator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['student', 'subject', 'exam_type', 'trimester']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'subject__name']
    ordering = ['-created_at']


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Attendance management
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrAdministrator]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'class_obj', 'status', 'date', 'teacher']
    ordering = ['-date']


class CalculateGradesView(APIView):
    """
    Calculate student averages and rankings
    """
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    
    def post(self, request):
        student_id = request.data.get('student_id')
        trimester_id = request.data.get('trimester_id')
        
        if not student_id or not trimester_id:
            return Response(
                {'error': 'student_id and trimester_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Calculate subject averages
            grades = Grade.objects.filter(
                student_id=student_id, 
                trimester_id=trimester_id
            )
            
            subject_averages = {}
            total_weighted_sum = Decimal('0')
            total_coefficient = Decimal('0')
            
            for grade in grades:
                subject = grade.subject
                if subject.id not in subject_averages:
                    subject_averages[subject.id] = {
                        'subject_name': subject.name,
                        'grades': [],
                        'average': Decimal('0'),
                        'coefficient': subject.coefficient
                    }
                
                # Calculate weighted grade
                weighted_grade = grade.grade * (grade.exam_type.percentage / 100)
                subject_averages[subject.id]['grades'].append({
                    'exam_type': grade.exam_type.name,
                    'grade': grade.grade,
                    'percentage': grade.exam_type.percentage,
                    'weighted_grade': weighted_grade
                })
            
            # Calculate subject averages
            for subject_id, data in subject_averages.items():
                if data['grades']:
                    total_weighted = sum(g['weighted_grade'] for g in data['grades'])
                    data['average'] = total_weighted
                    total_weighted_sum += data['average'] * data['coefficient']
                    total_coefficient += data['coefficient']
            
            # Calculate overall average
            overall_average = total_weighted_sum / total_coefficient if total_coefficient > 0 else Decimal('0')
            
            return Response({
                'student_id': student_id,
                'trimester_id': trimester_id,
                'subject_averages': subject_averages,
                'overall_average': float(overall_average),
                'total_coefficient': float(total_coefficient)
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateBulletinView(APIView):
    """
    Generate student bulletin
    """
    permission_classes = [permissions.IsAuthenticated, CanViewStudentData]
    
    def get(self, request, student_id):
        # This would integrate with the documents app
        # For now, return a placeholder response
        return Response({
            'message': 'Bulletin generation endpoint',
            'student_id': student_id
        })


class PromoteStudentsView(APIView):
    """
    Promote students to next level
    """
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    
    def post(self, request):
        # Implementation for student promotion logic
        return Response({'message': 'Student promotion endpoint'})


class AcademicReportView(APIView):
    """
    Generate academic reports
    """
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    
    def get(self, request):
        # Implementation for academic reports
        return Response({'message': 'Academic report endpoint'})