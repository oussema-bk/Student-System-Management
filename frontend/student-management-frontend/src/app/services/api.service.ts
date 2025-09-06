import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Student {
  id: number;
  user: {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
  };
  student_id: string;
  date_of_birth: string;
  gender: 'M' | 'F';
  is_archived: boolean;
}

export interface Grade {
  id: number;
  student: number;
  subject: {
    id: number;
    name: string;
    coefficient: number;
  };
  exam_type: {
    id: number;
    name: string;
    percentage: number;
  };
  trimester: {
    id: number;
    name: string;
  };
  grade: number;
  max_grade: number;
  teacher_notes: string;
  created_at: string;
}

export interface Attendance {
  id: number;
  student: number;
  class_obj: {
    id: number;
    name: string;
  };
  date: string;
  status: 'present' | 'absent' | 'late' | 'excused';
  teacher: {
    id: number;
    user: {
      first_name: string;
      last_name: string;
    };
  };
  notes: string;
}

export interface Bulletin {
  id: number;
  student: {
    id: number;
    user: {
      first_name: string;
      last_name: string;
    };
    student_id: string;
  };
  academic_year: string;
  trimester: string;
  class_name: string;
  total_average: number;
  class_rank: number;
  level_rank: number;
  attendance_rate: number;
  teacher_notes: string;
  principal_notes: string;
}

export interface Invoice {
  id: number;
  invoice_number: string;
  invoice_type: 'tuition' | 'salary' | 'expense' | 'other';
  student?: number;
  amount: number;
  description: string;
  due_date: string;
  status: 'pending' | 'paid' | 'overdue' | 'cancelled';
  created_at: string;
}

export interface Payment {
  id: number;
  invoice: number;
  amount: number;
  payment_method: 'cash' | 'bank_transfer' | 'cheque' | 'card';
  payment_date: string;
  reference_number: string;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly API_URL = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  // Students
  getStudents(params?: any): Observable<{ results: Student[]; count: number }> {
    return this.http.get<{ results: Student[]; count: number }>(`${this.API_URL}/accounts/students/`, { params });
  }

  getStudent(id: number): Observable<Student> {
    return this.http.get<Student>(`${this.API_URL}/accounts/students/${id}/`);
  }

  // Grades
  getGrades(params?: any): Observable<{ results: Grade[]; count: number }> {
    return this.http.get<{ results: Grade[]; count: number }>(`${this.API_URL}/academics/grades/`, { params });
  }

  createGrade(grade: Partial<Grade>): Observable<Grade> {
    return this.http.post<Grade>(`${this.API_URL}/academics/grades/`, grade);
  }

  updateGrade(id: number, grade: Partial<Grade>): Observable<Grade> {
    return this.http.patch<Grade>(`${this.API_URL}/academics/grades/${id}/`, grade);
  }

  deleteGrade(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/academics/grades/${id}/`);
  }

  calculateGrades(data: { student_id: number; trimester_id: number }): Observable<any> {
    return this.http.post(`${this.API_URL}/academics/grades/calculate/`, data);
  }

  // Attendance
  getAttendance(params?: any): Observable<{ results: Attendance[]; count: number }> {
    return this.http.get<{ results: Attendance[]; count: number }>(`${this.API_URL}/academics/attendance/`, { params });
  }

  createAttendance(attendance: Partial<Attendance>): Observable<Attendance> {
    return this.http.post<Attendance>(`${this.API_URL}/academics/attendance/`, attendance);
  }

  updateAttendance(id: number, attendance: Partial<Attendance>): Observable<Attendance> {
    return this.http.patch<Attendance>(`${this.API_URL}/academics/attendance/${id}/`, attendance);
  }

  // Bulletins
  getBulletins(params?: any): Observable<{ results: Bulletin[]; count: number }> {
    return this.http.get<{ results: Bulletin[]; count: number }>(`${this.API_URL}/documents/bulletins/`, { params });
  }

  downloadBulletin(bulletinId: number, language: string = 'fr'): Observable<Blob> {
    return this.http.get(`${this.API_URL}/documents/bulletin/${bulletinId}/download/?language=${language}`, {
      responseType: 'blob'
    });
  }

  // Invoices
  getInvoices(params?: any): Observable<{ results: Invoice[]; count: number }> {
    return this.http.get<{ results: Invoice[]; count: number }>(`${this.API_URL}/finance/invoices/`, { params });
  }

  createInvoice(invoice: Partial<Invoice>): Observable<Invoice> {
    return this.http.post<Invoice>(`${this.API_URL}/finance/invoices/`, invoice);
  }

  updateInvoice(id: number, invoice: Partial<Invoice>): Observable<Invoice> {
    return this.http.patch<Invoice>(`${this.API_URL}/finance/invoices/${id}/`, invoice);
  }

  // Payments
  getPayments(params?: any): Observable<{ results: Payment[]; count: number }> {
    return this.http.get<{ results: Payment[]; count: number }>(`${this.API_URL}/finance/payments/`, { params });
  }

  createPayment(payment: Partial<Payment>): Observable<Payment> {
    return this.http.post<Payment>(`${this.API_URL}/finance/payments/`, payment);
  }

  // Documents
  generatePresenceAttestation(data: { student_id: number; language: string }): Observable<Blob> {
    return this.http.post(`${this.API_URL}/documents/attestation-presence/`, data, {
      responseType: 'blob'
    });
  }

  generateInscriptionAttestation(data: { student_id: number; language: string }): Observable<Blob> {
    return this.http.post(`${this.API_URL}/documents/attestation-inscription/`, data, {
      responseType: 'blob'
    });
  }

  // Profile
  getProfile(): Observable<any> {
    return this.http.get(`${this.API_URL}/accounts/profile/`);
  }

  updateProfile(profile: any): Observable<any> {
    return this.http.patch(`${this.API_URL}/accounts/profile/`, profile);
  }
}
