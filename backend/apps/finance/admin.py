from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Invoice, Payment, Receipt, Expense, FinancialReport


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_type', 'student', 'amount', 'due_date', 'status', 'manager')
    list_filter = ('invoice_type', 'status', 'due_date', 'created_at')
    search_fields = ('invoice_number', 'student__user__first_name', 'student__user__last_name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_method', 'payment_date', 'status')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('invoice__invoice_number', 'reference_number')
    ordering = ('-payment_date',)
    readonly_fields = ('created_at',)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'payment', 'generated_at')
    search_fields = ('receipt_number', 'payment__invoice__invoice_number')
    ordering = ('-generated_at',)
    readonly_fields = ('generated_at',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'expense_date', 'manager')
    list_filter = ('category', 'expense_date', 'manager')
    search_fields = ('title', 'description')
    ordering = ('-expense_date',)
    readonly_fields = ('created_at',)


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'start_date', 'end_date', 'total_income', 'total_expenses', 'net_profit')
    list_filter = ('report_type', 'generated_at')
    search_fields = ('title',)
    ordering = ('-generated_at',)
    readonly_fields = ('generated_at', 'net_profit')