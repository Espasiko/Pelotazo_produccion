#!/usr/bin/env python3
import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"

def test_auth():
    """Prueba la autenticación y obtiene un token"""
    print("Probando autenticación...")
    
    # Datos de login
    login_data = {
        "username": "admin",
        "password": "admin_password_secure"
    }
    
    # Hacer petición de login
    response = requests.post(
        f"{BASE_URL}/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"Token obtenido: {token[:50]}...")
        
        # Probar endpoint de productos con el token
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\nProbando endpoint /api/v1/products/all...")
        products_response = requests.get(
            f"{BASE_URL}/api/v1/products/all",
            headers=headers
        )
        
        print(f"Status Code: {products_response.status_code}")
        print(f"Response: {products_response.text[:500]}...")
        
        return token
    else:
        print("Error en autenticación")
        return None

if __name__ == "__main__":
    test_auth()