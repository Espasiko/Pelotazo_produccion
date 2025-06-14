#!/usr/bin/env python3
import xmlrpc.client

def test_odoo_connection():
    try:
        # Configuración de conexión
        url = 'http://localhost:8070'
        db = 'manus_odoo-bd'
        username = 'yo@mail.com'
        password = 'admin'
        
        print(f"Probando conexión a Odoo en {url}...")
        
        # Conectar al servicio común
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        
        # Obtener información de versión
        version_info = common.version()
        print(f"Versión de Odoo: {version_info}")
        
        # Autenticar usuario
        uid = common.authenticate(db, username, password, {})
        print(f"UID de usuario: {uid}")
        
        if uid:
            # Conectar al servicio de modelos
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            
            # Buscar productos
            product_ids = models.execute_kw(db, uid, password,
                'product.template', 'search', [[]])
            print(f"IDs de productos encontrados: {product_ids[:5]}...")  # Mostrar solo los primeros 5
            
            if product_ids:
                # Leer datos de productos
                products = models.execute_kw(db, uid, password,
                    'product.template', 'read', [product_ids[:3]],
                    {'fields': ['id', 'name', 'default_code', 'list_price']})
                
                print("\nPrimeros 3 productos:")
                for product in products:
                    print(f"  ID: {product['id']}, Nombre: {product['name']}, Código: {product.get('default_code', 'N/A')}, Precio: {product.get('list_price', 0)}")
                
                return True
            else:
                print("No se encontraron productos en Odoo")
                return False
        else:
            print("Error: No se pudo autenticar el usuario")
            return False
            
    except Exception as e:
        print(f"Error conectando con Odoo: {e}")
        return False

if __name__ == "__main__":
    success = test_odoo_connection()
    if success:
        print("\n✅ Conexión con Odoo exitosa - hay productos reales disponibles")
    else:
        print("\n❌ Conexión con Odoo falló - se usarán productos simulados")