from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API Root endpoint providing navigation to all available endpoints
    """
    return Response({
        'message': 'Student Management System API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': {
                'login': '/api/auth/login/',
                'refresh': '/api/auth/refresh/',
            },
            'accounts': {
                'users': '/api/accounts/users/',
                'students': '/api/accounts/students/',
                'teachers': '/api/accounts/teachers/',
                'parents': '/api/accounts/parents/',
            },
            'academics': {
                'levels': '/api/academics/levels/',
                'classes': '/api/academics/classes/',
                'subjects': '/api/academics/subjects/',
                'grades': '/api/academics/grades/',
                'attendance': '/api/academics/attendance/',
            },
            'finance': {
                'invoices': '/api/finance/invoices/',
                'payments': '/api/finance/payments/',
                'receipts': '/api/finance/receipts/',
                'expenses': '/api/finance/expenses/',
            },
            'documents': {
                'documents': '/api/documents/documents/',
                'bulletins': '/api/documents/bulletins/',
                'attestations': '/api/documents/attestations/',
            },
            'admin': '/admin/',
        },
        'test_credentials': {
            'manager': {
                'email': 'manager@excellence.tn',
                'password': 'manager123'
            },
            'student': {
                'email': 'student1@excellence.tn',
                'password': 'student123'
            },
            'teacher': {
                'email': 'teacher1@excellence.tn',
                'password': 'teacher123'
            },
            'parent': {
                'email': 'parent1@excellence.tn',
                'password': 'parent123'
            }
        }
    }, status=status.HTTP_200_OK)
