import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';
import { MatMenuModule } from '@angular/material/menu';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatDividerModule,
    MatMenuModule
  ]
})
export class DashboardComponent implements OnInit {
  currentUser: any = null;
  isLoading = false;
  dashboardData: any = {
    cards: [
      { title: 'Students', value: '150', icon: 'school' },
      { title: 'Teachers', value: '25', icon: 'person' },
      { title: 'Classes', value: '12', icon: 'class' },
      { title: 'Subjects', value: '8', icon: 'book' }
    ]
  };

  constructor(
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit(): void {
    // Check authentication (only in browser)
    if (isPlatformBrowser(this.platformId)) {
      const userStr = localStorage.getItem('current_user');
      if (userStr) {
        this.currentUser = JSON.parse(userStr);
        this.redirectToRoleDashboard();
      } else {
        this.router.navigate(['/login']);
      }
    }
  }

  redirectToRoleDashboard(): void {
    switch (this.currentUser.role) {
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
        // Stay on general dashboard
        break;
    }
  }

  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('current_user');
    }
    this.router.navigate(['/login']);
  }

  getRoleDisplayName(role: string): string {
    const roleNames: { [key: string]: string } = {
      'administrator': 'Administrateur',
      'manager': 'Gestionnaire',
      'teacher': 'Enseignant',
      'parent': 'Parent',
      'student': 'Étudiant'
    };
    return roleNames[role] || role;
  }
}
