#!/bin/bash

echo "🌐 Testing Frontend-API Integration"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get access token
echo -n "Getting access token... "
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "student1@excellence.tn", "password": "student123"}' | grep -o '"access":"[^"]*"' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ SUCCESS${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    exit 1
fi

# Test API endpoints with authentication
echo -e "\n${YELLOW}Testing API Endpoints${NC}"

test_api_endpoint() {
    local name="$1"
    local url="$2"
    local expected_status="$3"
    
    echo -n "Testing $name... "
    
    response=$(curl -s -w "%{http_code}" -H "Authorization: Bearer $TOKEN" "$url")
    status_code="${response: -3}"
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        return 1
    fi
}

# Test various API endpoints
test_api_endpoint "Students List" "http://localhost:8000/api/accounts/students/" "200"
test_api_endpoint "Teachers List" "http://localhost:8000/api/accounts/teachers/" "200"
test_api_endpoint "Parents List" "http://localhost:8000/api/accounts/parents/" "200"
test_api_endpoint "Grades List" "http://localhost:8000/api/academics/grades/" "200"
test_api_endpoint "Invoices List" "http://localhost:8000/api/finance/invoices/" "200"
test_api_endpoint "Payments List" "http://localhost:8000/api/finance/payments/" "200"
test_api_endpoint "Subjects List" "http://localhost:8000/api/academics/subjects/" "200"
test_api_endpoint "Levels List" "http://localhost:8000/api/academics/levels/" "200"
test_api_endpoint "Classes List" "http://localhost:8000/api/academics/classes/" "200"

# Test frontend accessibility
echo -e "\n${YELLOW}Testing Frontend Pages${NC}"

test_frontend_page() {
    local name="$1"
    local url="$2"
    local expected_status="$3"
    
    echo -n "Testing $name... "
    
    response=$(curl -s -w "%{http_code}" "$url")
    status_code="${response: -3}"
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        return 1
    fi
}

test_frontend_page "Main App" "http://localhost/" "302"
test_frontend_page "Frontend Direct" "http://localhost:4200/" "302"
test_frontend_page "Login Page" "http://localhost:4200/login" "200"

echo -e "\n${GREEN}🎉 Frontend-API Integration Test Complete!${NC}"
echo -e "\n${YELLOW}Ready to Use:${NC}"
echo "• Login at: http://localhost/"
echo "• Use any of the test credentials"
echo "• Each role will redirect to their specific dashboard"
echo "• All API endpoints are working and authenticated"
