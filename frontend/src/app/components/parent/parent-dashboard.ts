import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTabsModule } from '@angular/material/tabs';
import { MatChipsModule } from '@angular/material/chips';
import { Router } from '@angular/router';
import { ApiService, Grade, Invoice, Payment, Student } from '../../services/api.service';

@Component({
  selector: 'app-parent-dashboard',
  templateUrl: './parent-dashboard.html',
  styleUrls: ['./parent-dashboard.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatTabsModule,
    MatChipsModule
  ]
})
export class ParentDashboardComponent implements OnInit {
  currentUser: any = null;
  parent: any = null;
  children: Student[] = [];
  allGrades: Grade[] = [];
  allInvoices: Invoice[] = [];
  allPayments: Payment[] = [];
  isLoading = false;
  selectedChild: Student | null = null;

  displayedColumnsGrades = ['subject', 'exam_type', 'grade', 'trimester', 'date'];
  displayedColumnsInvoices = ['invoice_number', 'amount', 'due_date', 'status'];
  displayedColumnsPayments = ['invoice', 'amount', 'method', 'date', 'status'];

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const userStr = localStorage.getItem('current_user');
    if (userStr) {
      this.currentUser = JSON.parse(userStr);
      this.loadParentData();
    }
  }

  loadParentData(): void {
    this.isLoading = true;
    
    // Load parent profile
    this.apiService.getParents().subscribe({
      next: (parents) => {
        this.parent = parents.find(p => p.user.email === this.currentUser.email);
        if (this.parent) {
          this.loadChildren();
        }
        this.isLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading parent data:', error);
        this.isLoading = false;
      }
    });
  }

  loadChildren(): void {
    this.apiService.getStudents().subscribe({
      next: (students) => {
        // In a real app, you would filter by parent relationship
        this.children = students.slice(0, 2); // Simulate having 2 children
        if (this.children.length > 0) {
          this.selectedChild = this.children[0];
          this.loadChildData();
        }
      },
      error: (error: any) => {
        console.error('Error loading children:', error);
      }
    });
  }

  loadChildData(): void {
    if (this.selectedChild) {
      this.loadGrades();
      this.loadInvoices();
      this.loadPayments();
    }
  }

  loadGrades(): void {
    if (this.selectedChild) {
      this.apiService.getStudentGrades(this.selectedChild.id).subscribe({
        next: (grades) => {
          this.allGrades = grades;
        },
        error: (error: any) => {
          console.error('Error loading grades:', error);
        }
      });
    }
  }

  loadInvoices(): void {
    if (this.selectedChild) {
      this.apiService.getStudentInvoices(this.selectedChild.id).subscribe({
        next: (invoices) => {
          this.allInvoices = invoices;
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
        this.allPayments = payments.filter(p => 
          this.allInvoices.some(inv => inv.id === p.invoice.id)
        );
      },
      error: (error: any) => {
        console.error('Error loading payments:', error);
      }
    });
  }

  selectChild(child: Student): void {
    this.selectedChild = child;
    this.loadChildData();
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
    this.router.navigate(['/login']);
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
    if (this.allGrades.length === 0) return 'N/A';
    const sum = this.allGrades.reduce((acc, grade) => acc + grade.grade, 0);
    const average = sum / this.allGrades.length;
    return average.toFixed(2);
  }
}
