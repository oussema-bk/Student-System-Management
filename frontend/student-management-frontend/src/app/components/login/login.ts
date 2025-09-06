import { Component, OnInit, OnDestroy, Inject, PLATFORM_ID } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../../services/api.service';
import { isPlatformBrowser } from '@angular/common';

// Interfaces for API responses
interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

interface User {
  id: number;
  email: string;
  role: 'student' | 'teacher' | 'parent' | 'manager' | 'administrator';
  first_name?: string;
  last_name?: string;
}

interface ApiError {
  detail?: string;
  non_field_errors?: string[];
  [key: string]: any;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  styleUrls: ['./login.scss'],
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatProgressSpinnerModule
  ]
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  isLoading = false;
  hidePassword = true;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private router: Router,
    private snackBar: MatSnackBar,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  ngOnInit(): void {
    // Check if already authenticated (only in browser)
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('access_token');
      if (token) {
        this.router.navigate(['/dashboard']);
      }
    }
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.isLoading = true;
      const credentials = this.loginForm.value;

      this.apiService.login(credentials).subscribe({
        next: (response: any) => {
          this.isLoading = false;
          
          // Store tokens and user data (only in browser)
          if (isPlatformBrowser(this.platformId)) {
            localStorage.setItem('access_token', response.access);
            localStorage.setItem('refresh_token', response.refresh);
            localStorage.setItem('current_user', JSON.stringify(response.user));
          }
          
          this.snackBar.open('Connexion réussie!', 'Fermer', {
            duration: 3000,
            horizontalPosition: 'center',
            verticalPosition: 'top'
          });
          
          // Redirect to appropriate dashboard based on role
          this.redirectBasedOnRole(response.user.role);
        },
        error: (error: any) => {
          this.isLoading = false;
          let errorMessage = 'Erreur de connexion';
          
          if (error.error?.detail) {
            errorMessage = error.error.detail;
          } else if (error.error?.non_field_errors) {
            errorMessage = error.error.non_field_errors[0];
          } else if (error.status === 0) {
            errorMessage = 'Impossible de se connecter au serveur. Vérifiez votre connexion.';
          }
          
          this.snackBar.open(errorMessage, 'Fermer', {
            duration: 5000,
            horizontalPosition: 'center',
            verticalPosition: 'top',
            panelClass: ['error-snackbar']
          });
        }
      });
    } else {
      this.markFormGroupTouched();
    }
  }

  private redirectBasedOnRole(role: string): void {
    switch (role) {
      case 'student':
        this.router.navigate(['/student-dashboard']);
        break;
      case 'teacher':
        this.router.navigate(['/teacher-dashboard']);
        break;
      case 'parent':
        this.router.navigate(['/parent-dashboard']);
        break;
      case 'manager':
        this.router.navigate(['/manager-dashboard']);
        break;
      case 'administrator':
        this.router.navigate(['/admin-dashboard']);
        break;
      default:
        this.router.navigate(['/dashboard']);
    }
  }

  private markFormGroupTouched(): void {
    Object.keys(this.loginForm.controls).forEach(key => {
      const control = this.loginForm.get(key);
      control?.markAsTouched();
    });
  }

  getErrorMessage(fieldName: string): string {
    const control = this.loginForm.get(fieldName);
    if (control?.hasError('required')) {
      return 'Ce champ est obligatoire';
    }
    if (control?.hasError('email')) {
      return 'Email invalide';
    }
    if (control?.hasError('minlength')) {
      return 'Le mot de passe doit contenir au moins 6 caractères';
    }
    return '';
  }
}
