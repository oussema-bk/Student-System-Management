import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login';
import { DashboardComponent } from './components/dashboard/dashboard';
import { StudentDashboardComponent } from './components/student/student-dashboard';
import { TeacherDashboardComponent } from './components/teacher/teacher-dashboard';
import { ParentDashboardComponent } from './components/parent/parent-dashboard';
import { ManagerDashboardComponent } from './components/manager/manager-dashboard';
import { AdminDashboardComponent } from './components/admin/admin-dashboard';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'student-dashboard', component: StudentDashboardComponent },
  { path: 'teacher-dashboard', component: TeacherDashboardComponent },
  { path: 'parent-dashboard', component: ParentDashboardComponent },
  { path: 'manager-dashboard', component: ManagerDashboardComponent },
  { path: 'admin-dashboard', component: AdminDashboardComponent },
  { path: '**', redirectTo: '/login' }
];
