#!/bin/bash

# Test authentication
echo "Testing authentication..."
TOKEN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin_password_secure" \
  http://localhost:8000/token)

echo "Token response: $TOKEN_RESPONSE"

# Extract token
TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "Extracted token: $TOKEN"

# Test products endpoint
echo "Testing products endpoint..."
PRODUCTS_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/products)
echo "Products response: $PRODUCTS_RESPONSE"