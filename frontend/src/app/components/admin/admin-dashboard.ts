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
import { ApiService, Student, Teacher, Parent } from '../../services/api.service';
import { NavigationComponent } from '../shared/navigation';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.html',
  styleUrls: ['./admin-dashboard.scss'],
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
export class AdminDashboardComponent implements OnInit {
  currentUser: any = null;
  admin: any = null;
  students: Student[] = [];
  teachers: Teacher[] = [];
  parents: Parent[] = [];
  levels: any[] = [];
  classes: any[] = [];
  subjects: any[] = [];
  isLoading = false;
  showAddUserForm = false;
  showAddClassForm = false;
  showAddSubjectForm = false;

  newUser = {
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    role: 'student',
    phone: '',
    address: ''
  };

  newClass = {
    name: '',
    level: null,
    academic_year: new Date().getFullYear()
  };

  newSubject = {
    name: '',
    coefficient: 1,
    class: null
  };

  displayedColumnsStudents = ['name', 'student_id', 'email', 'status', 'actions'];
  displayedColumnsTeachers = ['name', 'teacher_id', 'specialization', 'email', 'actions'];
  displayedColumnsParents = ['name', 'email', 'phone', 'actions'];
  displayedColumnsClasses = ['name', 'level', 'academic_year', 'students_count', 'actions'];
  displayedColumnsSubjects = ['name', 'coefficient', 'class', 'actions'];

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
        this.loadAdminData();
      } else {
        this.router.navigate(['/login']);
      }
    }
  }

  loadAdminData(): void {
    this.isLoading = true;
    
    // Load all data
    Promise.all([
      this.apiService.getStudents().toPromise(),
      this.apiService.getTeachers().toPromise(),
      this.apiService.getParents().toPromise(),
      this.apiService.getLevels().toPromise(),
      this.apiService.getClasses().toPromise(),
      this.apiService.getSubjects().toPromise()
    ]).then(([students, teachers, parents, levels, classes, subjects]) => {
      this.students = students || [];
      this.teachers = teachers || [];
      this.parents = parents || [];
      this.levels = levels || [];
      this.classes = classes || [];
      this.subjects = subjects || [];
      this.isLoading = false;
    }).catch(error => {
      console.error('Error loading admin data:', error);
      this.isLoading = false;
    });
  }

  addUser(): void {
    if (this.newUser.first_name && this.newUser.last_name && this.newUser.email && this.newUser.password) {
      // Simulate API call
      this.snackBar.open('Utilisateur ajouté avec succès!', 'Fermer', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'top'
      });
      
      this.loadAdminData();
      this.resetUserForm();
    }
  }

  addClass(): void {
    if (this.newClass.name && this.newClass.level) {
      // Simulate API call
      this.snackBar.open('Classe ajoutée avec succès!', 'Fermer', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'top'
      });
      
      this.loadAdminData();
      this.resetClassForm();
    }
  }

  addSubject(): void {
    if (this.newSubject.name && this.newSubject.class) {
      // Simulate API call
      this.snackBar.open('Matière ajoutée avec succès!', 'Fermer', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'top'
      });
      
      this.loadAdminData();
      this.resetSubjectForm();
    }
  }

  resetUserForm(): void {
    this.newUser = {
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      role: 'student',
      phone: '',
      address: ''
    };
    this.showAddUserForm = false;
  }

  resetClassForm(): void {
    this.newClass = {
      name: '',
      level: null,
      academic_year: new Date().getFullYear()
    };
    this.showAddClassForm = false;
  }

  resetSubjectForm(): void {
    this.newSubject = {
      name: '',
      coefficient: 1,
      class: null
    };
    this.showAddSubjectForm = false;
  }

  getStatusColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'active': return 'primary';
      case 'inactive': return 'warn';
      case 'archived': return 'warn';
      default: return '';
    }
  }

  getTotalUsers(): number {
    return this.students.length + this.teachers.length + this.parents.length;
  }

  getActiveStudents(): number {
  }

  getTotalClasses(): number {
    return this.classes.length;
  }

  getTotalSubjects(): number {
    return this.subjects.length;
  }
}
