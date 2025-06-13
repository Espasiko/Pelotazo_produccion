#!/bin/bash

# Test authentication
echo "Testing authentication..."
response=$(curl -s -X POST 'http://localhost:8000/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=admin_password_secure')

echo "Auth response: $response"

# Extract token if successful
if [[ $response == *"access_token"* ]]; then
  token=$(echo $response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
  echo "Token: $token"
  
  # Test products endpoint with token
  echo "Testing products endpoint..."
  products_response=$(curl -s -H "Authorization: Bearer $token" 'http://localhost:8000/api/v1/products')
  echo "Products response: $products_response"
else
  echo "Authentication failed"
fi