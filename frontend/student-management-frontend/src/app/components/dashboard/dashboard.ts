import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';
import { MatMenuModule } from '@angular/material/menu';
import { Router } from '@angular/router';

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

  constructor(private router: Router) {}

  ngOnInit(): void {
    const userStr = localStorage.getItem('current_user');
    if (userStr) {
      this.currentUser = JSON.parse(userStr);
    }
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
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
