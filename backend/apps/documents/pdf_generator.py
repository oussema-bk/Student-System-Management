from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime
from decimal import Decimal

from .models import Document, Bulletin, BulletinSubject, Attestation
from apps.accounts.models import Student, Institution
from apps.academics.models import Grade, Attendance


class PDFGenerator:
    """
    Base class for PDF generation
    """
    
    def __init__(self, language='fr'):
        self.language = language
        self.setup_fonts()
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_fonts(self):
        """
        Setup fonts for French and Arabic text
        """
        try:
            # Register fonts for multilingual support
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts')
            
            # French fonts
            if os.path.exists(os.path.join(font_path, 'DejaVuSans.ttf')):
                pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(font_path, 'DejaVuSans.ttf')))
            
            # Arabic fonts
            if os.path.exists(os.path.join(font_path, 'NotoSansArabic.ttf')):
                pdfmetrics.registerFont(TTFont('NotoSansArabic', os.path.join(font_path, 'NotoSansArabic.ttf')))
                
        except Exception as e:
            print(f"Font setup error: {e}")
    
    def setup_custom_styles(self):
        """
        Setup custom paragraph styles
        """
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='DejaVuSans' if self.language == 'fr' else 'NotoSansArabic'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='DejaVuSans' if self.language == 'fr' else 'NotoSansArabic'
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='DejaVuSans' if self.language == 'fr' else 'NotoSansArabic'
        ))
        
        # Table header style
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='DejaVuSans' if self.language == 'fr' else 'NotoSansArabic',
            alignment=TA_CENTER
        ))


class BulletinPDFGenerator(PDFGenerator):
    """
    Generate Bulletin Scolaire (Report Card) PDF
    """
    
    def generate_bulletin(self, bulletin_id, language='fr'):
        """
        Generate bulletin PDF
        """
        try:
            bulletin = Bulletin.objects.get(id=bulletin_id)
            student = bulletin.student
            institution = Institution.objects.first()  # Assuming single institution
            
            # Create PDF response
            response = HttpResponse(content_type='application/pdf')
            filename = f"bulletin_{student.student_id}_{bulletin.academic_year}_{bulletin.trimester}_{language}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            # Create PDF document
            doc = SimpleDocTemplate(response, pagesize=A4)
            story = []
            
            # Add institution header
            if institution:
                story.append(self._create_institution_header(institution, language))
                story.append(Spacer(1, 20))
            
            # Add student information
            story.append(self._create_student_info(student, bulletin, language))
            story.append(Spacer(1, 20))
            
            # Add academic information
            story.append(self._create_academic_info(bulletin, language))
            story.append(Spacer(1, 20))
            
            # Add grades table
            story.append(self._create_grades_table(bulletin, language))
            story.append(Spacer(1, 20))
            
            # Add attendance information
            story.append(self._create_attendance_info(bulletin, language))
            story.append(Spacer(1, 20))
            
            # Add notes
            story.append(self._create_notes_section(bulletin, language))
            
            # Build PDF
            doc.build(story)
            return response
            
        except Exception as e:
            return HttpResponse(f"Error generating bulletin: {str(e)}", status=500)
    
    def _create_institution_header(self, institution, language):
        """
        Create institution header
        """
        elements = []
        
        # Institution name
        institution_name = institution.name_ar if language == 'ar' and institution.name_ar else institution.name
        elements.append(Paragraph(institution_name, self.styles['CustomTitle']))
        
        # Institution details
        if language == 'fr':
            details = f"Adresse: {institution.address}<br/>Téléphone: {institution.phone}<br/>Email: {institution.email}"
        else:
            details = f"العنوان: {institution.address}<br/>الهاتف: {institution.phone}<br/>البريد الإلكتروني: {institution.email}"
        
        elements.append(Paragraph(details, self.styles['CustomNormal']))
        
        return elements
    
    def _create_student_info(self, student, bulletin, language):
        """
        Create student information section
        """
        elements = []
        
        if language == 'fr':
            title = "INFORMATIONS ÉLÈVE"
            info_data = [
                ["Nom complet:", student.user.get_full_name()],
                ["Identifiant élève:", student.student_id],
                ["Classe:", bulletin.class_name],
                ["Année scolaire:", bulletin.academic_year],
                ["Trimestre:", bulletin.trimester],
            ]
        else:
            title = "معلومات التلميذ"
            info_data = [
                ["الاسم الكامل:", student.user.get_full_name()],
                ["رقم التلميذ:", student.student_id],
                ["الفصل:", bulletin.class_name],
                ["السنة الدراسية:", bulletin.academic_year],
                ["الثلث:", bulletin.trimester],
            ]
        
        elements.append(Paragraph(title, self.styles['CustomSubtitle']))
        
        # Create student info table
        table_data = [["", ""]] + info_data
        table = Table(table_data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans' if language == 'fr' else 'NotoSansArabic'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_academic_info(self, bulletin, language):
        """
        Create academic performance section
        """
        elements = []
        
        if language == 'fr':
            title = "RÉSULTATS ACADÉMIQUES"
            info_data = [
                ["Moyenne générale:", f"{bulletin.total_average:.2f}/20" if bulletin.total_average else "N/A"],
                ["Rang dans la classe:", f"{bulletin.class_rank}" if bulletin.class_rank else "N/A"],
                ["Rang dans le niveau:", f"{bulletin.level_rank}" if bulletin.level_rank else "N/A"],
            ]
        else:
            title = "النتائج الأكاديمية"
            info_data = [
                ["المعدل العام:", f"{bulletin.total_average:.2f}/20" if bulletin.total_average else "غير متوفر"],
                ["الترتيب في الفصل:", f"{bulletin.class_rank}" if bulletin.class_rank else "غير متوفر"],
                ["الترتيب في المستوى:", f"{bulletin.level_rank}" if bulletin.level_rank else "غير متوفر"],
            ]
        
        elements.append(Paragraph(title, self.styles['CustomSubtitle']))
        
        # Create academic info table
        table_data = [["", ""]] + info_data
        table = Table(table_data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans' if language == 'fr' else 'NotoSansArabic'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_grades_table(self, bulletin, language):
        """
        Create grades table
        """
        elements = []
        
        if language == 'fr':
            title = "DÉTAIL DES NOTES"
            headers = ["Matière", "Coefficient", "Moyenne", "Enseignant", "Remarques"]
        else:
            title = "تفاصيل الدرجات"
            headers = ["المادة", "المعامل", "المعدل", "المعلم", "ملاحظات"]
        
        elements.append(Paragraph(title, self.styles['CustomSubtitle']))
        
        # Get bulletin subjects
        subjects = BulletinSubject.objects.filter(bulletin=bulletin)
        
        # Create table data
        table_data = [headers]
        for subject in subjects:
            subject_name = subject.subject_name_ar if language == 'ar' and subject.subject_name_ar else subject.subject_name
            table_data.append([
                subject_name,
                str(subject.coefficient),
                f"{subject.average:.2f}",
                subject.teacher_name,
                subject.teacher_notes[:50] + "..." if len(subject.teacher_notes) > 50 else subject.teacher_notes
            ])
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 1.2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans' if language == 'fr' else 'NotoSansArabic'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_attendance_info(self, bulletin, language):
        """
        Create attendance information section
        """
        elements = []
        
        if language == 'fr':
            title = "ASSIDUITÉ"
            info_data = [
                ["Total des jours:", str(bulletin.total_days)],
                ["Jours présents:", str(bulletin.present_days)],
                ["Jours absents:", str(bulletin.absent_days)],
                ["Taux d'assiduité:", f"{bulletin.attendance_rate:.1f}%" if bulletin.attendance_rate else "N/A"],
            ]
        else:
            title = "الحضور"
            info_data = [
                ["إجمالي الأيام:", str(bulletin.total_days)],
                ["أيام الحضور:", str(bulletin.present_days)],
                ["أيام الغياب:", str(bulletin.absent_days)],
                ["معدل الحضور:", f"{bulletin.attendance_rate:.1f}%" if bulletin.attendance_rate else "غير متوفر"],
            ]
        
        elements.append(Paragraph(title, self.styles['CustomSubtitle']))
        
        # Create attendance table
        table_data = [["", ""]] + info_data
        table = Table(table_data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans' if language == 'fr' else 'NotoSansArabic'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_notes_section(self, bulletin, language):
        """
        Create notes section
        """
        elements = []
        
        if language == 'fr':
            title = "OBSERVATIONS"
            teacher_title = "Remarques des enseignants:"
            principal_title = "Remarques du directeur:"
        else:
            title = "الملاحظات"
            teacher_title = "ملاحظات المعلمين:"
            principal_title = "ملاحظات المدير:"
        
        elements.append(Paragraph(title, self.styles['CustomSubtitle']))
        
        # Teacher notes
        elements.append(Paragraph(teacher_title, self.styles['CustomNormal']))
        elements.append(Paragraph(bulletin.teacher_notes or "Aucune remarque", self.styles['CustomNormal']))
        elements.append(Spacer(1, 10))
        
        # Principal notes
        elements.append(Paragraph(principal_title, self.styles['CustomNormal']))
        elements.append(Paragraph(bulletin.principal_notes or "Aucune remarque", self.styles['CustomNormal']))
        
        return elements


class AttestationPDFGenerator(PDFGenerator):
    """
    Generate Attestation PDFs
    """
    
    def generate_presence_attestation(self, attestation_id, language='fr'):
        """
        Generate Attestation de Présence PDF
        """
        try:
            attestation = Attestation.objects.get(id=attestation_id)
            student = attestation.student
            institution = Institution.objects.first()
            
            response = HttpResponse(content_type='application/pdf')
            filename = f"attestation_presence_{student.student_id}_{language}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            doc = SimpleDocTemplate(response, pagesize=A4)
            story = []
            
            # Institution header
            if institution:
                story.append(self._create_institution_header(institution, language))
                story.append(Spacer(1, 30))
            
            # Title
            if language == 'fr':
                title = "ATTESTATION DE PRÉSENCE"
            else:
                title = "شهادة حضور"
            
            story.append(Paragraph(title, self.styles['CustomTitle']))
            story.append(Spacer(1, 30))
            
            # Content
            story.append(self._create_attestation_content(attestation, language))
            
            # Signature section
            story.append(Spacer(1, 50))
            story.append(self._create_signature_section(language))
            
            doc.build(story)
            return response
            
        except Exception as e:
            return HttpResponse(f"Error generating attestation: {str(e)}", status=500)
    
    def generate_inscription_attestation(self, attestation_id, language='fr'):
        """
        Generate Attestation d'Inscription PDF
        """
        try:
            attestation = Attestation.objects.get(id=attestation_id)
            student = attestation.student
            institution = Institution.objects.first()
            
            response = HttpResponse(content_type='application/pdf')
            filename = f"attestation_inscription_{student.student_id}_{language}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            doc = SimpleDocTemplate(response, pagesize=A4)
            story = []
            
            # Institution header
            if institution:
                story.append(self._create_institution_header(institution, language))
                story.append(Spacer(1, 30))
            
            # Title
            if language == 'fr':
                title = "ATTESTATION D'INSCRIPTION"
            else:
                title = "شهادة التسجيل"
            
            story.append(Paragraph(title, self.styles['CustomTitle']))
            story.append(Spacer(1, 30))
            
            # Content
            story.append(self._create_inscription_content(attestation, language))
            
            # Signature section
            story.append(Spacer(1, 50))
            story.append(self._create_signature_section(language))
            
            doc.build(story)
            return response
            
        except Exception as e:
            return HttpResponse(f"Error generating attestation: {str(e)}", status=500)
    
    def _create_institution_header(self, institution, language):
        """
        Create institution header
        """
        elements = []
        
        institution_name = institution.name_ar if language == 'ar' and institution.name_ar else institution.name
        elements.append(Paragraph(institution_name, self.styles['CustomTitle']))
        
        if language == 'fr':
            details = f"Adresse: {institution.address}<br/>Téléphone: {institution.phone}"
        else:
            details = f"العنوان: {institution.address}<br/>الهاتف: {institution.phone}"
        
        elements.append(Paragraph(details, self.styles['CustomNormal']))
        
        return elements
    
    def _create_attestation_content(self, attestation, language):
        """
        Create attestation content
        """
        elements = []
        
        if language == 'fr':
            content = f"""
            Je soussigné(e), Directeur/Directrice de l'établissement, certifie que l'élève :
            
            <b>Nom complet :</b> {attestation.student.user.get_full_name()}<br/>
            <b>Identifiant :</b> {attestation.student.student_id}<br/>
            <b>Classe :</b> {attestation.class_name}<br/>
            <b>Niveau :</b> {attestation.level_name}<br/>
            <b>Année scolaire :</b> {attestation.academic_year}<br/>
            
            est régulièrement inscrit(e) dans notre établissement pour l'année scolaire {attestation.academic_year}.
            
            Cette attestation est délivrée pour servir et valoir ce que de droit.
            """
        else:
            content = f"""
            أنا الموقع أدناه، مدير/مديرة المؤسسة، أؤكد أن التلميذ:
            
            <b>الاسم الكامل:</b> {attestation.student.user.get_full_name()}<br/>
            <b>رقم التلميذ:</b> {attestation.student.student_id}<br/>
            <b>الفصل:</b> {attestation.class_name}<br/>
            <b>المستوى:</b> {attestation.level_name}<br/>
            <b>السنة الدراسية:</b> {attestation.academic_year}<br/>
            
            مسجل بانتظام في مؤسستنا للسنة الدراسية {attestation.academic_year}.
            
            هذه الشهادة صادرة للعمل بها حسب الأصول.
            """
        
        elements.append(Paragraph(content, self.styles['CustomNormal']))
        return elements
    
    def _create_inscription_content(self, attestation, language):
        """
        Create inscription attestation content
        """
        elements = []
        
        if language == 'fr':
            content = f"""
            Je soussigné(e), Directeur/Directrice de l'établissement, certifie que l'élève :
            
            <b>Nom complet :</b> {attestation.student.user.get_full_name()}<br/>
            <b>Identifiant :</b> {attestation.student.student_id}<br/>
            <b>Date de naissance :</b> {attestation.student.date_of_birth}<br/>
            <b>Classe :</b> {attestation.class_name}<br/>
            <b>Niveau :</b> {attestation.level_name}<br/>
            <b>Année scolaire :</b> {attestation.academic_year}<br/>
            
            a été officiellement inscrit(e) dans notre établissement le {attestation.created_at.strftime('%d/%m/%Y')}.
            
            Cette attestation d'inscription est délivrée une seule fois et confirme l'inscription officielle de l'élève.
            """
        else:
            content = f"""
            أنا الموقع أدناه، مدير/مديرة المؤسسة، أؤكد أن التلميذ:
            
            <b>الاسم الكامل:</b> {attestation.student.user.get_full_name()}<br/>
            <b>رقم التلميذ:</b> {attestation.student.student_id}<br/>
            <b>تاريخ الميلاد:</b> {attestation.student.date_of_birth}<br/>
            <b>الفصل:</b> {attestation.class_name}<br/>
            <b>المستوى:</b> {attestation.level_name}<br/>
            <b>السنة الدراسية:</b> {attestation.academic_year}<br/>
            
            تم تسجيله رسمياً في مؤسستنا في {attestation.created_at.strftime('%d/%m/%Y')}.
            
            هذه الشهادة صادرة مرة واحدة فقط وتؤكد التسجيل الرسمي للتلميذ.
            """
        
        elements.append(Paragraph(content, self.styles['CustomNormal']))
        return elements
    
    def _create_signature_section(self, language):
        """
        Create signature section
        """
        elements = []
        
        if language == 'fr':
            content = f"""
            Fait à Tunis, le {datetime.now().strftime('%d/%m/%Y')}<br/><br/>
            
            Le Directeur/La Directrice<br/><br/>
            
            Signature : ____________________
            """
        else:
            content = f"""
            حرر بتونس، في {datetime.now().strftime('%d/%m/%Y')}<br/><br/>
            
            المدير/المديرة<br/><br/>
            
            التوقيع: ____________________
            """
        
        elements.append(Paragraph(content, self.styles['CustomNormal']))
        return elements
