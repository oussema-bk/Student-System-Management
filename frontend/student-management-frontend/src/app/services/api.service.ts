import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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

export interface Teacher {
  id: number;
  user: {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
  };
  teacher_id: string;
  specialization: string;
  hire_date: string;
}

export interface Parent {
  id: number;
  user: {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
  };
  phone: string;
  address: string;
}

export interface Subject {
  id: number;
  name: string;
  coefficient: number;
}

export interface ExamType {
  id: number;
  name: string;
  percentage: number;
}

export interface Grade {
  id: number;
  student: Student;
  subject: Subject;
  exam_type: ExamType;
  grade: number;
  trimester: string;
  created_at: string;
}

export interface Invoice {
  id: number;
  invoice_number: string;
  student: Student;
  amount: number;
  due_date: string;
  status: string;
  created_at: string;
}

export interface Payment {
  id: number;
  invoice: Invoice;
  amount: number;
  payment_method: string;
  payment_date: string;
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://172.18.0.5:8000/api';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Host': 'localhost',
      'Authorization': token ? `Bearer ${token}` : ''
    });
  }

  // Authentication
  login(credentials: {email: string, password: string}): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Host': 'localhost'
    });
    return this.http.post(`${this.baseUrl}/auth/login/`, credentials, { headers });
  }

  // Students
  getStudents(): Observable<Student[]> {
    return this.http.get<Student[]>(`${this.baseUrl}/accounts/students/`, { headers: this.getHeaders() });
  }

  getStudent(id: number): Observable<Student> {
    return this.http.get<Student>(`${this.baseUrl}/accounts/students/${id}/`, { headers: this.getHeaders() });
  }

  // Teachers
  getTeachers(): Observable<Teacher[]> {
    return this.http.get<Teacher[]>(`${this.baseUrl}/accounts/teachers/`, { headers: this.getHeaders() });
  }

  getTeacher(id: number): Observable<Teacher> {
    return this.http.get<Teacher>(`${this.baseUrl}/accounts/teachers/${id}/`, { headers: this.getHeaders() });
  }

  // Parents
  getParents(): Observable<Parent[]> {
    return this.http.get<Parent[]>(`${this.baseUrl}/accounts/parents/`, { headers: this.getHeaders() });
  }

  getParent(id: number): Observable<Parent> {
    return this.http.get<Parent>(`${this.baseUrl}/accounts/parents/${id}/`, { headers: this.getHeaders() });
  }

  // Grades
  getGrades(): Observable<Grade[]> {
    return this.http.get<Grade[]>(`${this.baseUrl}/academics/grades/`, { headers: this.getHeaders() });
  }

  getStudentGrades(studentId: number): Observable<Grade[]> {
    return this.http.get<Grade[]>(`${this.baseUrl}/academics/grades/?student=${studentId}`, { headers: this.getHeaders() });
  }

  createGrade(grade: Partial<Grade>): Observable<Grade> {
    return this.http.post<Grade>(`${this.baseUrl}/academics/grades/`, grade, { headers: this.getHeaders() });
  }

  // Financial
  getInvoices(): Observable<Invoice[]> {
    return this.http.get<Invoice[]>(`${this.baseUrl}/finance/invoices/`, { headers: this.getHeaders() });
  }

  getStudentInvoices(studentId: number): Observable<Invoice[]> {
    return this.http.get<Invoice[]>(`${this.baseUrl}/finance/invoices/?student=${studentId}`, { headers: this.getHeaders() });
  }

  getPayments(): Observable<Payment[]> {
    return this.http.get<Payment[]>(`${this.baseUrl}/finance/payments/`, { headers: this.getHeaders() });
  }

  createPayment(payment: Partial<Payment>): Observable<Payment> {
    return this.http.post<Payment>(`${this.baseUrl}/finance/payments/`, payment, { headers: this.getHeaders() });
  }

  // Academic
  getLevels(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/academics/levels/`, { headers: this.getHeaders() });
  }

  getClasses(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/academics/classes/`, { headers: this.getHeaders() });
  }

  getSubjects(): Observable<Subject[]> {
    return this.http.get<Subject[]>(`${this.baseUrl}/academics/subjects/`, { headers: this.getHeaders() });
  }

  getExamTypes(): Observable<ExamType[]> {
    return this.http.get<ExamType[]>(`${this.baseUrl}/academics/exam-types/`, { headers: this.getHeaders() });
  }

  getAttendance(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/academics/attendance/`, { headers: this.getHeaders() });
  }
}