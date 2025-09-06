from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'receipts', views.ReceiptViewSet)
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'financial-reports', views.FinancialReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
