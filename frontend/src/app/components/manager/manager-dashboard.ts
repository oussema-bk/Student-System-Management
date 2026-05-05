import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTabsModule } from '@angular/material/tabs';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ApiService, Invoice, Payment, Student } from '../../services/api.service';
import { NavigationComponent } from '../shared/navigation';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-manager-dashboard',
  templateUrl: './manager-dashboard.html',
  styleUrls: ['./manager-dashboard.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatTabsModule,
    MatChipsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDialogModule,
    NavigationComponent
  ]
})
export class ManagerDashboardComponent implements OnInit {
  currentUser: any = null;
  manager: any = null;
  students: Student[] = [];
  invoices: Invoice[] = [];
  payments: Payment[] = [];
  isLoading = false;
  showAddInvoiceForm = false;
  showAddPaymentForm = false;

  newInvoice = {
    student: null,
    amount: null,
    due_date: '',
    status: 'pending'
  };

  newPayment = {
    invoice: null,
    amount: null,
    payment_method: 'cash',
    payment_date: new Date().toISOString().split('T')[0],
    status: 'completed'
  };

  displayedColumnsInvoices = ['invoice_number', 'student', 'amount', 'due_date', 'status', 'actions'];
  displayedColumnsPayments = ['invoice', 'student', 'amount', 'method', 'date', 'status'];

  constructor(
    private apiService: ApiService,
    private router: Router,
    private snackBar: MatSnackBar,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      const userStr = localStorage.getItem('current_user');
      if (userStr) {
        this.currentUser = JSON.parse(userStr);
        this.loadManagerData();
      } else {
        this.router.navigate(['/login']);
      }
    }
  }

  loadManagerData(): void {
    this.isLoading = true;
    
    // Load all data
    Promise.all([
      this.apiService.getStudents().toPromise(),
      this.apiService.getInvoices().toPromise(),
      this.apiService.getPayments().toPromise()
    ]).then(([students, invoices, payments]) => {
      this.students = students || [];
      this.invoices = invoices || [];
      this.payments = payments || [];
      this.isLoading = false;
    }).catch(error => {
      console.error('Error loading manager data:', error);
      this.isLoading = false;
    });
  }

  addInvoice(): void {
    if (this.newInvoice.student && this.newInvoice.amount && this.newInvoice.due_date) {
      // Generate invoice number
      const invoiceNumber = 'INV-' + Date.now();
      
      const invoiceData = {
        ...this.newInvoice,
        invoice_number: invoiceNumber,
        created_at: new Date().toISOString()
      };

      // Simulate API call
      this.snackBar.open('Facture ajoutée avec succès!', 'Fermer', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'top'
      });
      
      this.loadManagerData();
      this.resetInvoiceForm();
    }
  }

  addPayment(): void {
    if (this.newPayment.invoice && this.newPayment.amount && this.newPayment.payment_date) {
      // Simulate API call
      this.snackBar.open('Paiement ajouté avec succès!', 'Fermer', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'top'
      });
      
      this.loadManagerData();
      this.resetPaymentForm();
    }
  }

  resetInvoiceForm(): void {
    this.newInvoice = {
      student: null,
      amount: null,
      due_date: '',
      status: 'pending'
    };
    this.showAddInvoiceForm = false;
  }

  resetPaymentForm(): void {
    this.newPayment = {
      invoice: null,
      amount: null,
      payment_method: 'cash',
      payment_date: new Date().toISOString().split('T')[0],
      status: 'completed'
    };
    this.showAddPaymentForm = false;
  }

  getStatusColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'paid': return 'primary';
      case 'completed': return 'primary';
      case 'pending': return 'warn';
      case 'overdue': return 'warn';
      default: return '';
    }
  }

  getTotalRevenue(): number {
    return this.payments.reduce((sum, payment) => sum + payment.amount, 0);
  }

  getPendingAmount(): number {
    return this.invoices
      .filter(invoice => invoice.status === 'pending')
      .reduce((sum, invoice) => sum + invoice.amount, 0);
  }

  getOverdueAmount(): number {
    const today = new Date();
    return this.invoices
      .filter(invoice => {
        const dueDate = new Date(invoice.due_date);
        return invoice.status === 'pending' && dueDate < today;
      })
      .reduce((sum, invoice) => sum + invoice.amount, 0);
  }
}
