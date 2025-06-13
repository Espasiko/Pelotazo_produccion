#!/usr/bin/env python3
import requests
import json

def test_products_endpoint_8001():
    base_url = "http://localhost:8001"
    
    # 1. Obtener token de autenticación
    print("Obteniendo token de autenticación...")
    auth_data = {
        "username": "admin",
        "password": "admin_password_secure"
    }
    
    try:
        response = requests.post(f"{base_url}/token", data=auth_data)
        print(f"Status Code de autenticación: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"✅ Token obtenido exitosamente")
            
            # 2. Probar endpoint /api/v1/products/all
            print("\nProbando endpoint /api/v1/products/all...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{base_url}/api/v1/products/all", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ ¡Endpoint funcionando correctamente!")
                try:
                    products = response.json()
                    print(f"Número de productos obtenidos: {len(products)}")
                    if len(products) > 0:
                        print(f"Primer producto: {products[0]}")
                except Exception as e:
                    print(f"Error parseando JSON: {e}")
                    print(f"Respuesta raw: {response.text[:200]}...")
            else:
                print(f"❌ Error en el endpoint: {response.status_code}")
                print(f"Response: {response.text}")
                
        else:
            print(f"❌ Error en autenticación: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose en el puerto 8001?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_products_endpoint_8001()