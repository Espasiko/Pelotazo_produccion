import requests
import json

def verify_odoo_connection():
    try:
        # Verificar que FastAPI esté ejecutándose
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ FastAPI está ejecutándose")
        else:
            print("❌ FastAPI no responde correctamente")
            return False
        
        # Intentar autenticación
        auth_data = {
            "username": "yo@mail.com",
            "password": "admin"
        }
        auth_response = requests.post("http://localhost:8000/token", data=auth_data)
        
        if auth_response.status_code == 200:
            token = auth_response.json()["access_token"]
            print("✅ Autenticación exitosa")
            
            # Verificar productos
            headers = {"Authorization": f"Bearer {token}"}
            products_response = requests.get("http://localhost:8000/api/v1/products/all", headers=headers)
            
            if products_response.status_code == 200:
                products = products_response.json()
                print(f"✅ Productos obtenidos: {len(products)}")
                
                # Verificar si son productos reales o de respaldo
                fallback_names = ["Refrigerador Samsung RT38K5982BS", "Lavadora LG F4WV5012S0W", "Televisor Sony KD-55X80J"]
                real_products = [p for p in products if p["name"] not in fallback_names]
                
                if len(real_products) > 0:
                    print("✅ ÉXITO: Se están obteniendo productos reales de Odoo")
                    return True
                else:
                    print("❌ PROBLEMA: Solo se obtienen productos de respaldo")
                    return False
            else:
                print("❌ Error obteniendo productos")
                return False
        else:
            print("❌ Error en autenticación")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    verify_odoo_connection()


