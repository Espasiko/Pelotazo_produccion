#!/usr/bin/env python3
"""
Script para verificar la comunicación XML-RPC con Odoo
"""

import xmlrpc.client
import sys
import traceback

def test_odoo_xmlrpc():
    """Prueba la conexión XML-RPC con Odoo paso a paso"""
    
    # Configuración
    odoo_url = "http://localhost:8070"
    odoo_db = "manus_odoo-bd"
    odoo_username = "yo@mail.com"
    odoo_password = "admin"
    
    print("=== VERIFICACIÓN DE COMUNICACIÓN XML-RPC CON ODOO ===")
    print(f"URL: {odoo_url}")
    print(f"Base de datos: {odoo_db}")
    print(f"Usuario: {odoo_username}")
    print(f"Contraseña: {odoo_password}")
    print("\n" + "="*60)
    
    try:
        # Paso 1: Conectar al servicio common
        print("\n1. CONECTANDO AL SERVICIO COMMON...")
        common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
        print("✓ Conexión al servicio common establecida")
        
        # Paso 2: Obtener información de versión
        print("\n2. OBTENIENDO INFORMACIÓN DE VERSIÓN...")
        try:
            version_info = common.version()
            print(f"✓ Información de versión obtenida:")
            print(f"  - Versión del servidor: {version_info.get('server_version', 'N/A')}")
            print(f"  - Versión del protocolo: {version_info.get('protocol_version', 'N/A')}")
            print(f"  - Serie de versión: {version_info.get('server_serie', 'N/A')}")
        except Exception as e:
            print(f"✗ Error obteniendo versión: {e}")
            return False
        
        # Paso 3: Autenticación
        print("\n3. AUTENTICANDO USUARIO...")
        try:
            uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})
            if uid:
                print(f"✓ Autenticación exitosa. UID: {uid}")
            else:
                print("✗ Autenticación fallida. Credenciales incorrectas o base de datos no existe.")
                return False
        except Exception as e:
            print(f"✗ Error en autenticación: {e}")
            return False
        
        # Paso 4: Conectar al servicio object
        print("\n4. CONECTANDO AL SERVICIO OBJECT...")
        try:
            models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')
            print("✓ Conexión al servicio object establecida")
        except Exception as e:
            print(f"✗ Error conectando al servicio object: {e}")
            return False
        
        # Paso 5: Probar acceso a modelos
        print("\n5. PROBANDO ACCESO A MODELOS...")
        
        # Probar acceso a product.template
        try:
            print("\n5.1. Probando acceso a product.template...")
            product_count = models.execute_kw(
                odoo_db, uid, odoo_password,
                'product.template', 'search_count', [[]]
            )
            print(f"✓ Número de productos en product.template: {product_count}")
            
            if product_count > 0:
                # Obtener algunos productos
                product_ids = models.execute_kw(
                    odoo_db, uid, odoo_password,
                    'product.template', 'search', [[]],
                    {'limit': 5}
                )
                print(f"✓ IDs de primeros 5 productos: {product_ids}")
                
                # Leer datos de productos
                products = models.execute_kw(
                    odoo_db, uid, odoo_password,
                    'product.template', 'read', [product_ids],
                    {'fields': ['id', 'name', 'default_code', 'list_price']}
                )
                print(f"✓ Datos de productos obtenidos:")
                for product in products:
                    print(f"  - ID: {product['id']}, Nombre: {product['name']}, Código: {product.get('default_code', 'N/A')}, Precio: {product.get('list_price', 0)}")
            else:
                print("⚠ No hay productos en la base de datos")
                
        except Exception as e:
            print(f"✗ Error accediendo a product.template: {e}")
            print(f"Traceback: {traceback.format_exc()}")
        
        # Probar acceso a res.partner (proveedores)
        try:
            print("\n5.2. Probando acceso a res.partner (proveedores)...")
            partner_count = models.execute_kw(
                odoo_db, uid, odoo_password,
                'res.partner', 'search_count', 
                [['&', ('is_company', '=', True), ('supplier_rank', '>', 0)]]
            )
            print(f"✓ Número de proveedores: {partner_count}")
            
        except Exception as e:
            print(f"✗ Error accediendo a res.partner: {e}")
        
        # Probar acceso a product.category
        try:
            print("\n5.3. Probando acceso a product.category...")
            category_count = models.execute_kw(
                odoo_db, uid, odoo_password,
                'product.category', 'search_count', [[]]
            )
            print(f"✓ Número de categorías: {category_count}")
            
        except Exception as e:
            print(f"✗ Error accediendo a product.category: {e}")
        
        print("\n" + "="*60)
        print("✓ COMUNICACIÓN XML-RPC CON ODOO VERIFICADA EXITOSAMENTE")
        print("✓ La API FastAPI DEBERÍA poder conectarse a Odoo")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR GENERAL: {e}")
        print(f"Traceback completo: {traceback.format_exc()}")
        return False

def test_odoo_availability():
    """Prueba si Odoo está disponible en el puerto especificado"""
    import urllib.request
    import urllib.error
    
    print("\n=== VERIFICANDO DISPONIBILIDAD DE ODOO ===")
    
    try:
        response = urllib.request.urlopen("http://localhost:8070", timeout=10)
        print(f"✓ Odoo responde en http://localhost:8070")
        print(f"✓ Código de respuesta: {response.getcode()}")
        return True
    except urllib.error.URLError as e:
        print(f"✗ Odoo no está disponible en http://localhost:8070: {e}")
        return False
    except Exception as e:
        print(f"✗ Error verificando disponibilidad: {e}")
        return False

if __name__ == "__main__":
    print("Iniciando verificación de comunicación XML-RPC con Odoo...\n")
    
    # Primero verificar si Odoo está disponible
    if not test_odoo_availability():
        print("\n❌ Odoo no está disponible. Verifica que esté ejecutándose.")
        sys.exit(1)
    
    # Luego probar la comunicación XML-RPC
    if test_odoo_xmlrpc():
        print("\n🎉 RESULTADO: La comunicación XML-RPC funciona correctamente")
        print("🔍 Si la API FastAPI usa datos de fallback, el problema puede ser:")
        print("   - Configuración incorrecta en variables de entorno")
        print("   - Manejo de excepciones que oculta errores")
        print("   - Problemas de red dentro del contenedor Docker")
        sys.exit(0)
    else:
        print("\n❌ RESULTADO: La comunicación XML-RPC falló")
        print("🔍 Verifica:")
        print("   - Que Odoo esté ejecutándose")
        print("   - Las credenciales de acceso")
        print("   - La configuración de la base de datos")
        sys.exit(1)