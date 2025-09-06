import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatBadgeModule } from '@angular/material/badge';
import { isPlatformBrowser } from '@angular/common';

export interface MenuItem {
  label: string;
  icon: string;
  route: string;
  roles: string[];
  badge?: number;
}

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.html',
  styleUrls: ['./navigation.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatMenuModule,
    MatSidenavModule,
    MatListModule,
    MatDividerModule,
    MatBadgeModule
  ]
})
export class NavigationComponent implements OnInit {
  currentUser: any = null;
  isSidebarOpen = false;
  
  menuItems: MenuItem[] = [
    // Student Menu
    { label: 'Tableau de bord', icon: 'dashboard', route: '/student-dashboard', roles: ['student'] },
    { label: 'Mes Notes', icon: 'school', route: '/student-dashboard', roles: ['student'] },
    { label: 'Mes Factures', icon: 'receipt', route: '/student-dashboard', roles: ['student'] },
    { label: 'Mes Paiements', icon: 'payment', route: '/student-dashboard', roles: ['student'] },
    
    // Teacher Menu
    { label: 'Tableau de bord', icon: 'dashboard', route: '/teacher-dashboard', roles: ['teacher'] },
    { label: 'Mes Étudiants', icon: 'school', route: '/teacher-dashboard', roles: ['teacher'] },
    { label: 'Saisir Notes', icon: 'edit', route: '/teacher-dashboard', roles: ['teacher'] },
    { label: 'Présences', icon: 'event_available', route: '/teacher-dashboard', roles: ['teacher'] },
    
    // Parent Menu
    { label: 'Tableau de bord', icon: 'dashboard', route: '/parent-dashboard', roles: ['parent'] },
    { label: 'Mes Enfants', icon: 'child_care', route: '/parent-dashboard', roles: ['parent'] },
    { label: 'Notes des Enfants', icon: 'school', route: '/parent-dashboard', roles: ['parent'] },
    { label: 'Paiements', icon: 'payment', route: '/parent-dashboard', roles: ['parent'] },
    
    // Manager Menu
    { label: 'Tableau de bord', icon: 'dashboard', route: '/manager-dashboard', roles: ['manager'] },
    { label: 'Gestion Financière', icon: 'account_balance', route: '/manager-dashboard', roles: ['manager'] },
    { label: 'Factures', icon: 'receipt', route: '/manager-dashboard', roles: ['manager'] },
    { label: 'Paiements', icon: 'payment', route: '/manager-dashboard', roles: ['manager'] },
    { label: 'Rapports', icon: 'assessment', route: '/manager-dashboard', roles: ['manager'] },
    { label: 'Documents', icon: 'description', route: '/manager-dashboard', roles: ['manager'] },
    
    // Admin Menu
    { label: 'Tableau de bord', icon: 'dashboard', route: '/admin-dashboard', roles: ['administrator'] },
    { label: 'Utilisateurs', icon: 'people', route: '/admin-dashboard', roles: ['administrator'] },
    { label: 'Étudiants', icon: 'school', route: '/admin-dashboard', roles: ['administrator'] },
    { label: 'Enseignants', icon: 'person', route: '/admin-dashboard', roles: ['administrator'] },
    { label: 'Classes', icon: 'class', route: '/admin-dashboard', roles: ['administrator'] },
    { label: 'Matières', icon: 'book', route: '/admin-dashboard', roles: ['administrator'] },
    { label: 'Configuration', icon: 'settings', route: '/admin-dashboard', roles: ['administrator'] }
  ];

  constructor(
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      const userStr = localStorage.getItem('current_user');
      if (userStr) {
        this.currentUser = JSON.parse(userStr);
      }
    }
  }

  getFilteredMenuItems(): MenuItem[] {
    return this.menuItems.filter(item => 
      item.roles.includes(this.currentUser.role)
    );
  }

  navigateTo(route: string): void {
    this.router.navigate([route]);
    this.isSidebarOpen = false;
  }

  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('current_user');
    }
    this.router.navigate(['/login']);
  }

  toggleSidebar(): void {
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
