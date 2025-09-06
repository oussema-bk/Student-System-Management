from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'academic-years', views.AcademicYearViewSet)
router.register(r'levels', views.LevelViewSet)
router.register(r'classes', views.ClassViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'exam-types', views.ExamTypeViewSet)
router.register(r'trimesters', views.TrimesterViewSet)
router.register(r'class-subjects', views.ClassSubjectViewSet)
router.register(r'student-classes', views.StudentClassViewSet)
router.register(r'grades', views.GradeViewSet)
router.register(r'attendance', views.AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('grades/calculate/', views.CalculateGradesView.as_view(), name='calculate-grades'),
    path('students/<int:student_id>/bulletin/', views.GenerateBulletinView.as_view(), name='generate-bulletin'),
    path('students/promote/', views.PromoteStudentsView.as_view(), name='promote-students'),
    path('reports/academic/', views.AcademicReportView.as_view(), name='academic-report'),
]
