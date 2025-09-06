from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import Document, Bulletin, BulletinSubject, Attestation
from .serializers import DocumentSerializer, BulletinSerializer, BulletinSubjectSerializer, AttestationSerializer
from .pdf_generator import BulletinPDFGenerator, AttestationPDFGenerator
from apps.accounts.permissions import IsManagerOrAdministrator, CanViewStudentData
from apps.accounts.models import Student
from apps.academics.models import Grade, Attendance, ClassSubject


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]
    filter_backends = []
    search_fields = ['title', 'student__user__first_name', 'student__user__last_name']
    ordering = ['-generated_at']


class BulletinViewSet(viewsets.ModelViewSet):
    queryset = Bulletin.objects.all()
    serializer_class = BulletinSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]
    filter_backends = []
    search_fields = ['student__user__first_name', 'student__user__last_name', 'academic_year']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download bulletin PDF
        """
        bulletin = self.get_object()
        language = request.query_params.get('language', 'fr')
        
        generator = BulletinPDFGenerator(language=language)
        return generator.generate_bulletin(bulletin.id, language)


class BulletinSubjectViewSet(viewsets.ModelViewSet):
    queryset = BulletinSubject.objects.all()
    serializer_class = BulletinSubjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]


class AttestationViewSet(viewsets.ModelViewSet):
    queryset = Attestation.objects.all()
    serializer_class = AttestationSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]
    filter_backends = []
    search_fields = ['student__user__first_name', 'student__user__last_name', 'academic_year']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download attestation PDF
        """
        attestation = self.get_object()
        language = request.query_params.get('language', 'fr')
        
        generator = AttestationPDFGenerator(language=language)
        
        if attestation.attestation_type == 'presence':
            return generator.generate_presence_attestation(attestation.id, language)
        elif attestation.attestation_type == 'inscription':
            return generator.generate_inscription_attestation(attestation.id, language)
        
        return Response({'error': 'Invalid attestation type'}, status=status.HTTP_400_BAD_REQUEST)


class GeneratePresenceAttestationView(APIView):
    """
    Generate Attestation de Présence
    """
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]
    
    def post(self, request):
        student_id = request.data.get('student_id')
        language = request.data.get('language', 'fr')
        
        if not student_id:
            return Response({'error': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = Student.objects.get(id=student_id)
            
            # Get current enrollment
            current_enrollment = student.enrollments.filter(is_active=True).first()
            if not current_enrollment:
                return Response({'error': 'Student is not currently enrolled'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create attestation
            attestation = Attestation.objects.create(
                student=student,
                attestation_type='presence',
                language=language,
                academic_year=current_enrollment.class_obj.academic_year.name,
                class_name=current_enrollment.class_obj.name,
                level_name=current_enrollment.class_obj.level.name,
                valid_from=request.data.get('valid_from'),
                valid_until=request.data.get('valid_until')
            )
            
            # Create document record
            document = Document.objects.create(
                student=student,
                document_type='attestation_presence',
                language=language,
                title=f"Attestation de Présence - {student.user.get_full_name()}",
                file_path=f"attestations/presence_{student.student_id}_{language}.pdf"
            )
            
            attestation.document = document
            attestation.save()
            
            # Generate PDF
            generator = AttestationPDFGenerator(language=language)
            return generator.generate_presence_attestation(attestation.id, language)
            
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateInscriptionAttestationView(APIView):
    """
    Generate Attestation d'Inscription
    """
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]
    
    def post(self, request):
        student_id = request.data.get('student_id')
        language = request.data.get('language', 'fr')
        
        if not student_id:
            return Response({'error': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = Student.objects.get(id=student_id)
            
            # Get current enrollment
            current_enrollment = student.enrollments.filter(is_active=True).first()
            if not current_enrollment:
                return Response({'error': 'Student is not currently enrolled'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if inscription attestation already exists
            existing_attestation = Attestation.objects.filter(
                student=student,
                attestation_type='inscription'
            ).first()
            
            if existing_attestation:
                return Response({'error': 'Inscription attestation already exists for this student'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create attestation
            attestation = Attestation.objects.create(
                student=student,
                attestation_type='inscription',
                language=language,
                academic_year=current_enrollment.class_obj.academic_year.name,
                class_name=current_enrollment.class_obj.name,
                level_name=current_enrollment.class_obj.level.name
            )
            
            # Create document record
            document = Document.objects.create(
                student=student,
                document_type='attestation_inscription',
                language=language,
                title=f"Attestation d'Inscription - {student.user.get_full_name()}",
                file_path=f"attestations/inscription_{student.student_id}_{language}.pdf"
            )
            
            attestation.document = document
            attestation.save()
            
            # Archive student (mark as archived)
            student.is_archived = True
            student.save()
            
            # Generate PDF
            generator = AttestationPDFGenerator(language=language)
            return generator.generate_inscription_attestation(attestation.id, language)
            
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadBulletinView(APIView):
    """
    Download bulletin PDF
    """
    permission_classes = [permissions.IsAuthenticated, CanViewStudentData]
    
    def get(self, request, bulletin_id):
        language = request.query_params.get('language', 'fr')
        
        try:
            bulletin = Bulletin.objects.get(id=bulletin_id)
            
            # Check permissions
            if not request.user.is_administrator and not request.user.is_manager:
                if request.user.is_parent:
                    # Check if student is child of parent
                    parent_profile = getattr(request.user, 'parent_profile', None)
                    if not parent_profile or not parent_profile.children.filter(student=bulletin.student).exists():
                        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
                elif request.user.is_student:
                    # Check if it's the student's own bulletin
                    if bulletin.student.user != request.user:
                        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            generator = BulletinPDFGenerator(language=language)
            return generator.generate_bulletin(bulletin.id, language)
            
        except Bulletin.DoesNotExist:
            return Response({'error': 'Bulletin not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)