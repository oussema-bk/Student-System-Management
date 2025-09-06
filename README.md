# Student Management System

A comprehensive Student Management System built with Django (backend) and Angular (frontend), designed for the Tunisian educational system with multilingual support (French & Arabic).

## 🎯 Features

### Multi-Role System
- **Parents**: View children's grades, attendance, payments, download bulletins
- **Students**: View own academic records, grades, attendance
- **Teachers**: Manage classes, grades, attendance for assigned classes
- **Administrators**: Full system management, user creation, academic configuration
- **Managers**: Financial management, document generation, reports

### Academic Management
- **Hierarchical Levels**: Primaire → 3ème section Maths 1 → 4ème section Maths 1
- **Classes & Subjects**: Configurable coefficients and exam types
- **Grading System**: Trimestrial/semestrial with weighted averages
- **Attendance Tracking**: Real-time attendance management
- **Academic Reports**: Success/failure rates, class rankings

### Financial Management
- **Invoice Management**: Tuition fees, teacher salaries, expenses
- **Payment Tracking**: Multiple payment methods (cash, bank transfer, cheque)
- **Financial Reports**: Monthly/yearly income and expense reports
- **Receipt Generation**: Automated receipt creation

### Document Generation
- **Bulletin Scolaire**: Report cards in French/Arabic
- **Attestation de Présence**: Current enrollment confirmation
- **Attestation d'Inscription**: Official registration document
- **Financial Receipts**: Payment confirmations

### Security & Multilingual Support
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Granular permissions per user role
- **Multilingual Interface**: French and Arabic support
- **Data Encryption**: Sensitive data protection

## 🛠️ Technology Stack

### Backend
- **Django 4.2+** with Django REST Framework
- **PostgreSQL** Database
- **JWT Authentication** with SimpleJWT
- **ReportLab/WeasyPrint** for PDF generation
- **Django Internationalization** for multilingual support
- **Celery** for background tasks
- **Redis** for caching and message broker

### Frontend
- **Angular 16+** with Angular Material
- **Angular i18n** for multilingual support
- **RxJS** for state management
- **Angular JWT Service** for authentication

### Deployment
- **Docker & Docker Compose** for containerization
- **Nginx** reverse proxy
- **PostgreSQL** container
- **Redis** container

## 📁 Project Structure

```
Arwa/
├── backend/                 # Django backend
│   ├── student_management/  # Main Django project
│   ├── apps/               # Django apps
│   │   ├── accounts/       # User management
│   │   ├── academics/      # Academic management
│   │   ├── finance/        # Financial management
│   │   └── documents/      # Document generation
│   ├── requirements.txt
│   ├── Dockerfile
│   └── env.example
├── frontend/               # Angular frontend
│   └── student-management-frontend/
│       ├── src/
│       ├── package.json
│       └── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── setup.sh
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL (for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Arwa
   ```

2. **Run the setup script**
   ```bash
   ./setup.sh
   ```

3. **Start with Docker (Recommended)**
   ```bash
   docker-compose up --build
   ```

4. **Or start manually**
   ```bash
   # Backend
   cd backend
   python manage.py runserver
   
   # Frontend (in another terminal)
   cd frontend/student-management-frontend
   npm start
   ```

### Access Points
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **With Nginx**: http://localhost (all services)

## 🔧 Configuration

### Environment Variables
Copy `backend/env.example` to `backend/.env` and configure:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=student_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Database Setup
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 📊 Database Schema

### Core Models
- **User**: Custom user model with roles (parent, student, teacher, administrator, manager)
- **Institution**: Educational institution information
- **Level**: Hierarchical academic levels
- **Class**: Classes belonging to levels and academic years
- **Subject**: Subjects with coefficients
- **Student**: Student profiles with academic information
- **Teacher**: Teacher profiles with specializations
- **Parent**: Parent profiles with contact information

### Academic Models
- **AcademicYear**: Academic year management
- **Trimester**: Trimesters/semesters with coefficients
- **ExamType**: Exam types with percentage weights
- **Grade**: Student grades per subject and exam type
- **Attendance**: Student attendance tracking
- **ClassSubject**: Many-to-many relationship between classes and subjects

### Financial Models
- **Invoice**: Invoices for various types of payments
- **Payment**: Payment tracking and management
- **Receipt**: Payment confirmations
- **Expense**: Institutional expenses
- **FinancialReport**: Monthly/yearly financial reports

### Document Models
- **Document**: Generated document metadata
- **Bulletin**: Detailed grade reports
- **Attestation**: Presence and enrollment confirmations

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token

### Accounts
- `GET /api/accounts/users/` - List users
- `POST /api/accounts/users/` - Create user
- `GET /api/accounts/profile/` - Get user profile
- `PATCH /api/accounts/profile/` - Update profile

### Academics
- `GET /api/academics/classes/` - List classes
- `GET /api/academics/grades/` - List grades
- `POST /api/academics/grades/calculate/` - Calculate averages
- `GET /api/academics/students/{id}/bulletin/` - Generate bulletin

### Finance
- `GET /api/finance/invoices/` - List invoices
- `POST /api/finance/invoices/` - Create invoice
- `GET /api/finance/payments/` - List payments
- `POST /api/finance/payments/` - Record payment

### Documents
- `GET /api/documents/bulletins/` - List bulletins
- `POST /api/documents/attestation-presence/` - Generate presence attestation
- `POST /api/documents/attestation-inscription/` - Generate inscription attestation

## 🌍 Multilingual Support

The system supports French and Arabic languages:

### Backend
- Django internationalization with `gettext_lazy`
- Language-specific model fields (`name_ar`)
- Configurable language preferences per user

### Frontend
- Angular i18n integration
- Language switching functionality
- RTL support for Arabic

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Granular permissions
- **Password Validation**: Django's built-in password validators
- **CORS Configuration**: Secure cross-origin requests
- **Data Encryption**: Sensitive data protection
- **Audit Logging**: User action tracking

## 📈 Academic Calculations

### Grade Calculation
```
Subject Average = Σ(Grade × Exam Type Percentage) / 100
Overall Average = Σ(Subject Average × Subject Coefficient) / Σ(Subject Coefficients)
```

### Ranking System
- Class rankings based on overall averages
- Level rankings across all classes
- Configurable coefficients for trimesters/semesters

## 🐳 Docker Deployment

### Production Deployment
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Service Management
```bash
# Restart specific service
docker-compose restart backend

# Scale services
docker-compose up --scale backend=2

# Backup database
docker-compose exec db pg_dump -U postgres student_management > backup.sql
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend/student-management-frontend
npm test
```

## 📝 Development Guidelines

### Backend
- Follow Django best practices
- Use type hints in Python code
- Write comprehensive docstrings
- Implement proper error handling
- Use Django's built-in security features

### Frontend
- Follow Angular style guide
- Use Angular Material components
- Implement proper error handling
- Use reactive programming with RxJS
- Follow accessibility guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints

## 🔮 Future Enhancements

- Mobile application (React Native/Flutter)
- Advanced reporting and analytics
- Integration with external systems
- Real-time notifications
- Advanced document templates
- Bulk operations
- Data import/export functionality
