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
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService, Grade, Student, Subject, ExamType } from '../../services/api.service';
import { NavigationComponent } from '../shared/navigation';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-teacher-dashboard',
  templateUrl: './teacher-dashboard.html',
  styleUrls: ['./teacher-dashboard.scss'],
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
    ReactiveFormsModule,
    NavigationComponent
  ]
})
export class TeacherDashboardComponent implements OnInit {
  currentUser: any = null;
  teacher: any = null;
  students: Student[] = [];
  subjects: Subject[] = [];
  examTypes: ExamType[] = [];
  grades: Grade[] = [];
  isLoading = false;

  displayedColumnsStudents = ['name', 'student_id', 'class', 'actions'];
  displayedColumnsGrades = ['student', 'subject', 'exam_type', 'grade', 'trimester', 'date'];

  gradeForm: FormGroup;
  newGrade: Partial<Grade> = {
    student: undefined,
    subject: undefined,
    exam_type: undefined,
    grade: 0,
    trimester: '1'
  };

  constructor(
    private apiService: ApiService,
    private router: Router,
    private fb: FormBuilder,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.gradeForm = this.fb.group({
      student: ['', Validators.required],
      subject: ['', Validators.required],
      exam_type: ['', Validators.required],
      grade: ['', [Validators.required, Validators.min(0), Validators.max(20)]],
      trimester: ['1', Validators.required]
    });
  }

  ngOnInit(): void {
    // Check authentication (only in browser)
    if (isPlatformBrowser(this.platformId)) {
      const userStr = localStorage.getItem('current_user');
      if (userStr) {
        this.currentUser = JSON.parse(userStr);
        this.loadTeacherData();
      } else {
        this.router.navigate(['/login']);
      }
    }
  }

  loadTeacherData(): void {
    this.isLoading = true;
    
    // Load teacher profile
    this.apiService.getTeachers().subscribe({
      next: (teachers) => {
        this.teacher = teachers.find(t => t.user.email === this.currentUser.email);
        if (this.teacher) {
          this.loadStudents();
          this.loadSubjects();
          this.loadExamTypes();
          this.loadGrades();
        }
        this.isLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading teacher data:', error);
        this.isLoading = false;
      }
    });
  }

  loadStudents(): void {
    this.apiService.getStudents().subscribe({
      next: (students) => {
        this.students = students;
      },
      error: (error: any) => {
        console.error('Error loading students:', error);
      }
    });
  }

  loadSubjects(): void {
    this.apiService.getSubjects().subscribe({
      next: (subjects) => {
        this.subjects = subjects;
      },
      error: (error: any) => {
        console.error('Error loading subjects:', error);
      }
    });
  }

  loadExamTypes(): void {
    this.apiService.getExamTypes().subscribe({
      next: (examTypes) => {
        this.examTypes = examTypes;
      },
      error: (error: any) => {
        console.error('Error loading exam types:', error);
      }
    });
  }

  loadGrades(): void {
    this.apiService.getGrades().subscribe({
      next: (grades) => {
        this.grades = grades;
      },
      error: (error: any) => {
        console.error('Error loading grades:', error);
      }
    });
  }

  onSubmitGrade(): void {
    if (this.gradeForm.valid) {
      const gradeData = this.gradeForm.value;
      this.newGrade = {
        student: gradeData.student,
        subject: gradeData.subject,
        exam_type: gradeData.exam_type,
        grade: gradeData.grade,
        trimester: gradeData.trimester
      };

      this.apiService.createGrade(this.newGrade).subscribe({
        next: (response) => {
          console.log('Grade created successfully:', response);
          this.gradeForm.reset();
          this.gradeForm.patchValue({ trimester: '1' });
          this.loadGrades();
        },
        error: (error: any) => {
          console.error('Error creating grade:', error);
        }
      });
    } else {
      this.markFormGroupTouched();
    }
  }

  private markFormGroupTouched(): void {
    Object.keys(this.gradeForm.controls).forEach(key => {
      const control = this.gradeForm.get(key);
      control?.markAsTouched();
    });
  }

  getGradeColor(grade: number): string {
    if (grade >= 16) return 'primary';
    if (grade >= 14) return 'accent';
    if (grade >= 12) return 'warn';
    return '';
  }

  getErrorMessage(fieldName: string): string {
    const control = this.gradeForm.get(fieldName);
    if (control?.hasError('required')) {
      return 'Ce champ est obligatoire';
    }
    if (control?.hasError('min')) {
      return 'La note doit être supérieure ou égale à 0';
    }
    if (control?.hasError('max')) {
      return 'La note doit être inférieure ou égale à 20';
    }
    return '';
  }
}
