from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Student, Teacher, User


class Invoice(models.Model):
    """
    Invoice model for various types of payments
    """
    INVOICE_TYPE_CHOICES = [
        ('tuition', _('Tuition Fee')),
        ('salary', _('Teacher Salary')),
        ('expense', _('Expense')),
        ('other', _('Other')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('overdue', _('Overdue')),
        ('cancelled', _('Cancelled')),
    ]
    
    invoice_number = models.CharField(_('Invoice Number'), max_length=50, unique=True)
    invoice_type = models.CharField(_('Invoice Type'), max_length=20, choices=INVOICE_TYPE_CHOICES)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='invoices')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='salary_invoices')
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    description = models.TextField(_('Description'))
    due_date = models.DateField(_('Due Date'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_invoices')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.get_invoice_type_display()}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number
            import uuid
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    Payment model for tracking payments
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', _('Cash')),
        ('bank_transfer', _('Bank Transfer')),
        ('cheque', _('Cheque')),
        ('card', _('Card')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    ]
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_('Payment Method'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(_('Payment Date'))
    reference_number = models.CharField(_('Reference Number'), max_length=100, blank=True)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment {self.amount} - {self.get_payment_method_display()}"


class Receipt(models.Model):
    """
    Receipt model for payment confirmations
    """
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(_('Receipt Number'), max_length=50, unique=True)
    generated_at = models.DateTimeField(_('Generated at'), auto_now_add=True)
    file_path = models.CharField(_('File Path'), max_length=500, blank=True)
    
    class Meta:
        verbose_name = _('Receipt')
        verbose_name_plural = _('Receipts')
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"Receipt {self.receipt_number}"
    
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generate receipt number
            import uuid
            self.receipt_number = f"RCP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Expense(models.Model):
    """
    Expense model for institutional expenses
    """
    CATEGORY_CHOICES = [
        ('utilities', _('Utilities')),
        ('maintenance', _('Maintenance')),
        ('supplies', _('Supplies')),
        ('equipment', _('Equipment')),
        ('transportation', _('Transportation')),
        ('other', _('Other')),
    ]
    
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    category = models.CharField(_('Category'), max_length=20, choices=CATEGORY_CHOICES)
    expense_date = models.DateField(_('Expense Date'))
    receipt_file = models.FileField(_('Receipt File'), upload_to='expenses/receipts/', blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"{self.title} - {self.amount}"


class FinancialReport(models.Model):
    """
    Financial report model for monthly/yearly reports
    """
    REPORT_TYPE_CHOICES = [
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
        ('custom', _('Custom Period')),
    ]
    
    title = models.CharField(_('Title'), max_length=200)
    report_type = models.CharField(_('Report Type'), max_length=20, choices=REPORT_TYPE_CHOICES)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    total_income = models.DecimalField(_('Total Income'), max_digits=12, decimal_places=2, default=0)
    total_expenses = models.DecimalField(_('Total Expenses'), max_digits=12, decimal_places=2, default=0)
    net_profit = models.DecimalField(_('Net Profit'), max_digits=12, decimal_places=2, default=0)
    file_path = models.CharField(_('File Path'), max_length=500, blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    generated_at = models.DateTimeField(_('Generated at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Financial Report')
        verbose_name_plural = _('Financial Reports')
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"
    
    def save(self, *args, **kwargs):
        self.net_profit = self.total_income - self.total_expenses
        super().save(*args, **kwargs)