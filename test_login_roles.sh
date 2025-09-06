#!/bin/bash

echo "🔐 Testing Login for All User Roles"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_login() {
    local role="$1"
    local email="$2"
    local password="$3"
    
    echo -n "Testing $role login ($email)... "
    
    response=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"password\": \"$password\"}")
    
    if echo "$response" | grep -q "access"; then
        echo -e "${GREEN}✓ SUCCESS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        echo "Response: $response"
        return 1
    fi
}

# Test all user roles
echo -e "\n${YELLOW}Testing Authentication:${NC}"
test_login "Student" "student1@excellence.tn" "student123"
test_login "Teacher" "teacher1@excellence.tn" "teacher123"
test_login "Parent" "parent1@excellence.tn" "parent123"
test_login "Manager" "manager@excellence.tn" "manager123"
test_login "Admin" "admin@excellence.tn" "admin123"

echo -e "\n${YELLOW}Testing Frontend Access:${NC}"
echo -n "Main app redirect... "
if curl -s -I http://localhost/ | grep -q "302"; then
    echo -e "${GREEN}✓ SUCCESS${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
fi

echo -n "Login page accessible... "
if curl -s -I http://localhost:4200/login | grep -q "200"; then
    echo -e "${GREEN}✓ SUCCESS${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
fi

echo -e "\n${GREEN}🎉 Login Testing Complete!${NC}"
echo -e "\n${YELLOW}Ready to Login:${NC}"
echo "• Go to: http://localhost/"
echo "• Use any of the test credentials above"
echo "• Each role will redirect to their specific dashboard"
