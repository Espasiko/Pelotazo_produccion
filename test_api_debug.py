#!/usr/bin/env python3
import requests
import json
import time
import subprocess
import sys
from threading import Thread

def test_api():
    """Prueba la API y muestra los logs"""
    print("=== PROBANDO API EN PUERTO 8001 ===")
    
    # Esperar un poco para que la API se inicie
    time.sleep(2)
    
    try:
        # 1. Obtener token
        print("\n1. Obteniendo token...")
        login_data = {
            "username": "admin",
            "password": "admin"
        }
        
        response = requests.post(
            "http://localhost:8001/api/v1/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            print(f"   ✅ Token obtenido: {token[:20]}...")
            
            # 2. Obtener productos
            print("\n2. Obteniendo productos...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            products_response = requests.get(
                "http://localhost:8001/api/v1/products/all",
                headers=headers,
                timeout=10
            )
            
            if products_response.status_code == 200:
                products = products_response.json()
                print(f"   ✅ Se obtuvieron {len(products)} productos")
                
                # Mostrar algunos productos
                for i, product in enumerate(products[:3], 1):
                    print(f"   {i}. {product['name']} - ${product['price']} - {product['category']}")
                    
            else:
                print(f"   ❌ Error obteniendo productos: {products_response.status_code}")
                print(f"   Response: {products_response.text}")
        else:
            print(f"   ❌ Error obteniendo token: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ No se pudo conectar a la API")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_api()