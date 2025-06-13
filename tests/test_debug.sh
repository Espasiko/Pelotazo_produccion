#!/bin/bash

echo "Testing token endpoint..."
response=$(curl -s -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123")

echo "Response: $response"

if [ -z "$response" ]; then
    echo "Empty response from server"
    exit 1
fi

echo "Token endpoint test completed"
