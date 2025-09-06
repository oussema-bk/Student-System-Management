#!/bin/bash

# Student Management System Setup Script
echo "🚀 Setting up Student Management System..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/logs
mkdir -p backend/media
mkdir -p backend/staticfiles

# Copy environment file
echo "⚙️ Setting up environment..."
if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "✅ Environment file created from template"
else
    echo "ℹ️ Environment file already exists"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend/student-management-frontend
npm install
cd ../..

# Create Django migrations
echo "🗄️ Creating database migrations..."
cd backend
python manage.py makemigrations
python manage.py migrate
cd ..

# Create superuser (optional)
echo "👤 Creating superuser..."
echo "You can create a superuser by running:"
echo "cd backend && python manage.py createsuperuser"

# Build Docker images (optional)
echo "🐳 Building Docker images..."
docker-compose build

echo "✅ Setup complete!"
echo ""
echo "To start the development environment:"
echo "1. Start with Docker: docker-compose up"
echo "2. Or start manually:"
echo "   - Backend: cd backend && python manage.py runserver"
echo "   - Frontend: cd frontend/student-management-frontend && npm start"
echo ""
echo "Access the application at:"
echo "- Frontend: http://localhost:4200"
echo "- Backend API: http://localhost:8000/api/"
echo "- Django Admin: http://localhost:8000/admin/"
