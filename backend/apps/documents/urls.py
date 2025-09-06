from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)
router.register(r'bulletins', views.BulletinViewSet)
router.register(r'attestations', views.AttestationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('attestation-presence/', views.GeneratePresenceAttestationView.as_view(), name='attestation-presence'),
    path('attestation-inscription/', views.GenerateInscriptionAttestationView.as_view(), name='attestation-inscription'),
    path('bulletin/<int:bulletin_id>/download/', views.DownloadBulletinView.as_view(), name='download-bulletin'),
]
