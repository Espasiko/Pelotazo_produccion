#!/usr/bin/env python3
import requests
import json

def check_routes():
    try:
        # Obtener el esquema OpenAPI
        response = requests.get("http://localhost:8000/openapi.json")
        if response.status_code == 200:
            openapi_schema = response.json()
            
            print("=== RUTAS DISPONIBLES ===")
            paths = openapi_schema.get("paths", {})
            
            for path, methods in paths.items():
                print(f"\nRuta: {path}")
                for method, details in methods.items():
                    summary = details.get("summary", "Sin descripción")
                    print(f"  {method.upper()}: {summary}")
                    
            # Buscar específicamente rutas de productos
            print("\n=== RUTAS DE PRODUCTOS ===")
            product_paths = [path for path in paths.keys() if "product" in path.lower()]
            for path in product_paths:
                print(f"  {path}")
                
        else:
            print(f"Error obteniendo esquema: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_routes()