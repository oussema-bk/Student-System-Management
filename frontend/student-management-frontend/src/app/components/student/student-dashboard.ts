import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTabsModule } from '@angular/material/tabs';
import { MatChipsModule } from '@angular/material/chips';
import { Router } from '@angular/router';
import { ApiService, Grade, Invoice, Payment } from '../../services/api.service';
import { NavigationComponent } from '../shared/navigation';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-student-dashboard',
  templateUrl: './student-dashboard.html',
  styleUrls: ['./student-dashboard.scss'],
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
    NavigationComponent
  ]
})
export class StudentDashboardComponent implements OnInit {
  currentUser: any = null;
  student: any = null;
  grades: Grade[] = [];
  invoices: Invoice[] = [];
  payments: Payment[] = [];
  isLoading = false;

  displayedColumnsGrades = ['subject', 'exam_type', 'grade', 'trimester', 'date'];
  displayedColumnsInvoices = ['invoice_number', 'amount', 'due_date', 'status'];
  displayedColumnsPayments = ['invoice', 'amount', 'method', 'date', 'status'];

  constructor(
    private apiService: ApiService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit(): void {
    // Check authentication (only in browser)
    if (isPlatformBrowser(this.platformId)) {
      const userStr = localStorage.getItem('current_user');
      if (userStr) {
        this.currentUser = JSON.parse(userStr);
        this.loadStudentData();
      } else {
        this.router.navigate(['/login']);
      }
    }
  }

  loadStudentData(): void {
    this.isLoading = true;
    
    // Load student profile
    this.apiService.getStudents().subscribe({
      next: (students) => {
        this.student = students.find(s => s.user.email === this.currentUser.email);
        if (this.student) {
          this.loadGrades();
          this.loadInvoices();
          this.loadPayments();
        }
        this.isLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading student data:', error);
        this.isLoading = false;
      }
    });
  }

  loadGrades(): void {
    if (this.student) {
      this.apiService.getStudentGrades(this.student.id).subscribe({
        next: (grades) => {
          this.grades = grades;
        },
        error: (error: any) => {
          console.error('Error loading grades:', error);
        }
      });
    }
  }

  loadInvoices(): void {
    if (this.student) {
      this.apiService.getStudentInvoices(this.student.id).subscribe({
        next: (invoices) => {
          this.invoices = invoices;
        },
        error: (error: any) => {
          console.error('Error loading invoices:', error);
        }
      });
    }
  }

  loadPayments(): void {
    this.apiService.getPayments().subscribe({
      next: (payments) => {
        this.payments = payments.filter(p => 
          this.invoices.some(inv => inv.id === p.invoice.id)
        );
      },
      error: (error: any) => {
        console.error('Error loading payments:', error);
      }
    });
  }

  getGradeColor(grade: number): string {
    if (grade >= 16) return 'primary';
    if (grade >= 14) return 'accent';
    if (grade >= 12) return 'warn';
    return '';
  }

  getStatusColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'paid': return 'primary';
      case 'pending': return 'warn';
      case 'overdue': return 'warn';
      default: return '';
    }
  }

  getAverageGrade(): string {
    if (this.grades.length === 0) return 'N/A';
    const sum = this.grades.reduce((acc, grade) => acc + grade.grade, 0);
    const average = sum / this.grades.length;
    return average.toFixed(2);
  }
}
