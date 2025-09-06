from rest_framework import viewsets, permissions
from .models import Invoice, Payment, Receipt, Expense, FinancialReport
from .serializers import InvoiceSerializer, PaymentSerializer, ReceiptSerializer, ExpenseSerializer, FinancialReportSerializer
from apps.accounts.permissions import IsManagerOrAdministrator


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]


class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdministrator]