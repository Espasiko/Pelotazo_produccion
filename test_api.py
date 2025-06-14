#!/usr/bin/env python3
import requests
import json

# Obtener token de autenticación
print("=== ANÁLISIS DE LA API FASTAPI ===\n")
print("1. Obteniendo token de autenticación...")
token_data = {
    'username': 'admin',
    'password': 'admin_password_secure'
}

try:
    response = requests.post('http://localhost:8000/token', data=token_data)
    print(f"   Status code: {response.status_code}")
    
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get('access_token')
        
        if access_token:
            print(f"   ✅ Token obtenido exitosamente")
            
            # Probar endpoint products/all con el token
            print("\n2. Probando endpoint /api/v1/products/all...")
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            products_response = requests.get('http://localhost:8000/api/v1/products/all', headers=headers)
            print(f"   Status code: {products_response.status_code}")
            
            if products_response.status_code == 200:
                products = products_response.json()
                print(f"   ✅ Se obtuvieron {len(products)} productos")
                
                # Analizar si son datos reales o simulados
                print("\n3. ANÁLISIS DE DATOS:")
                print("   Los productos devueltos son:")
                for i, product in enumerate(products, 1):
                    print(f"   {i}. {product['name']} - ${product['price']} - {product['category']}")
                
                # Verificar si son datos de fallback
                fallback_names = [
                    "Refrigerador Samsung RT38K5982BS",
                    "Lavadora LG F4WV5012S0W", 
                    "Televisor Sony KD-55X80J"
                ]
                
                is_fallback = any(product['name'] in fallback_names for product in products)
                
                if is_fallback:
                    print("\n   🔍 RESULTADO: Estos son DATOS SIMULADOS (fallback)")
                    print("   La API no está conectando exitosamente con Odoo y está")
                    print("   devolviendo datos de prueba predefinidos.")
                else:
                    print("\n   🔍 RESULTADO: Estos parecen ser DATOS REALES de Odoo")
                    print("   La API está conectando exitosamente con la base de datos.")
                    
            else:
                print(f"   ❌ Error al obtener productos: {products_response.text}")
        else:
            print("   ❌ No se pudo obtener el token de acceso")
    else:
        print(f"   ❌ Error al obtener el token: {response.text}")
        
    # Verificar conexión con Odoo directamente
    print("\n4. Verificando conexión directa con Odoo...")
    try:
        odoo_response = requests.get('http://localhost:8070', timeout=5)
        if odoo_response.status_code == 200:
            print("   ✅ Odoo está funcionando en http://localhost:8070")
        else:
            print(f"   ⚠️ Odoo responde pero con código: {odoo_response.status_code}")
    except Exception as odoo_error:
        print(f"   ❌ No se puede conectar con Odoo: {odoo_error}")
        
except Exception as e:
    print(f"❌ Error general: {e}")

print("\n=== ANÁLISIS COMPLETADO ===")