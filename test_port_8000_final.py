#!/usr/bin/env python3
import requests
import json

def test_products_all_endpoint_8000():
    """Prueba el endpoint /api/v1/products/all en puerto 8000"""
    try:
        print("🔍 Verificando rutas disponibles en puerto 8000...")
        
        # Verificar rutas disponibles
        openapi_response = requests.get("http://localhost:8000/openapi.json")
        if openapi_response.status_code == 200:
            openapi_data = openapi_response.json()
            paths = openapi_data.get('paths', {})
            
            print("\n📋 Rutas de productos encontradas:")
            product_routes = []
            for path in paths:
                if 'product' in path.lower():
                    product_routes.append(path)
                    print(f"  ✅ {path}")
            
            if '/api/v1/products/all' in product_routes:
                print("\n🎯 ¡Ruta /api/v1/products/all encontrada!")
            else:
                print("\n❌ Ruta /api/v1/products/all NO encontrada")
                return False
        
        # Autenticación
        auth_data = {
            "username": "admin",
            "password": "admin_password_secure"
        }
        
        print("\n🔐 Obteniendo token de acceso...")
        auth_response = requests.post(
            "http://localhost:8000/token", 
            data=auth_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if auth_response.status_code != 200:
            print(f"❌ Error en autenticación: {auth_response.status_code}")
            print(f"Respuesta: {auth_response.text}")
            return False
            
        token_data = auth_response.json()
        access_token = token_data["access_token"]
        print(f"✅ Token obtenido exitosamente")
        
        # Probar el endpoint /api/v1/products/all
        headers = {"Authorization": f"Bearer {access_token}"}
        
        print("\n📦 Probando endpoint /api/v1/products/all en puerto 8000...")
        response = requests.get("http://localhost:8000/api/v1/products/all", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\n🎉 ¡ÉXITO! El endpoint funciona correctamente en puerto 8000!")
            data = response.json()
            print(f"📊 Número de productos obtenidos: {len(data)}")
            
            if len(data) > 0:
                print("\n📋 Ejemplo de producto:")
                first_product = data[0]
                for key, value in first_product.items():
                    print(f"  {key}: {value}")
            
            print("\n✅ El frontend ahora debería poder mostrar los productos correctamente")
            return True
        else:
            print(f"❌ Error en el endpoint: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor en localhost:8000")
        print("💡 Asegúrate de que el contenedor FastAPI esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🧪 PRUEBA FINAL DEL ENDPOINT /products/all EN PUERTO 8000")
    print("="*60)
    
    success = test_products_all_endpoint_8000()
    
    print("\n" + "="*60)
    if success:
        print("🎊 ¡PRUEBA COMPLETADA EXITOSAMENTE!")
        print("✅ El endpoint /api/v1/products/all funciona en puerto 8000")
        print("✅ El frontend debería mostrar productos correctamente")
        print("✅ El problema de routing ha sido resuelto")
    else:
        print("❌ LA PRUEBA FALLÓ")
        print("❌ Revisar configuración del servidor")
    print("="*60)

if __name__ == "__main__":
    main()