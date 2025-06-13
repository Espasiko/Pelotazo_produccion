#!/usr/bin/env python3
import xmlrpc.client
import os

def test_odoo_connection():
    """Prueba la conexión real con Odoo y verifica los datos"""
    
    # Configuración de Odoo
    odoo_config = {
        "url": os.getenv("ODOO_URL", "http://localhost:8070"),
        "db": os.getenv("ODOO_DB", "manus_odoo-bd"),
        "username": os.getenv("ODOO_USERNAME", "yo@mail.com"),
        "password": os.getenv("ODOO_PASSWORD", "admin")
    }
    
    print("🔍 DIAGNÓSTICO DE CONEXIÓN CON ODOO")
    print("="*50)
    print(f"URL: {odoo_config['url']}")
    print(f"Base de datos: {odoo_config['db']}")
    print(f"Usuario: {odoo_config['username']}")
    print(f"Contraseña: {'*' * len(odoo_config['password'])}")
    print()
    
    try:
        # Paso 1: Conectar al servicio común
        print("📡 Paso 1: Conectando al servicio común...")
        common = xmlrpc.client.ServerProxy(f'{odoo_config["url"]}/xmlrpc/2/common')
        
        # Verificar versión de Odoo
        print("🔍 Verificando versión de Odoo...")
        version_info = common.version()
        print(f"✅ Versión de Odoo: {version_info}")
        print()
        
        # Paso 2: Autenticación
        print("🔐 Paso 2: Autenticando usuario...")
        uid = common.authenticate(
            odoo_config["db"],
            odoo_config["username"],
            odoo_config["password"],
            {}
        )
        
        if not uid:
            print("❌ ERROR: Autenticación fallida")
            print("💡 Posibles causas:")
            print("   - Usuario o contraseña incorrectos")
            print("   - Base de datos no existe")
            print("   - Usuario no tiene permisos")
            return False
        
        print(f"✅ Autenticación exitosa. UID: {uid}")
        print()
        
        # Paso 3: Conectar al servicio de objetos
        print("📊 Paso 3: Conectando al servicio de objetos...")
        models = xmlrpc.client.ServerProxy(f'{odoo_config["url"]}/xmlrpc/2/object')
        
        # Paso 4: Verificar acceso a productos
        print("📦 Paso 4: Verificando productos en Odoo...")
        
        # Contar productos totales
        product_count = models.execute_kw(
            odoo_config["db"],
            uid,
            odoo_config["password"],
            'product.template',
            'search_count',
            [[]]
        )
        
        print(f"📊 Total de productos en Odoo: {product_count}")
        
        if product_count == 0:
            print("⚠️  WARNING: No hay productos en la base de datos de Odoo")
            print("💡 Esto explica por qué se muestran datos simulados")
            print()
            
            # Verificar si hay categorías
            category_count = models.execute_kw(
                odoo_config["db"],
                uid,
                odoo_config["password"],
                'product.category',
                'search_count',
                [[]]
            )
            print(f"📂 Total de categorías: {category_count}")
            
            # Verificar si hay partners/proveedores
            partner_count = models.execute_kw(
                odoo_config["db"],
                uid,
                odoo_config["password"],
                'res.partner',
                'search_count',
                [[]]
            )
            print(f"👥 Total de partners: {partner_count}")
            
            return False
        
        # Obtener algunos productos de muestra
        print("📋 Obteniendo productos de muestra...")
        product_ids = models.execute_kw(
            odoo_config["db"],
            uid,
            odoo_config["password"],
            'product.template',
            'search',
            [[]],
            {'limit': 5}
        )
        
        if product_ids:
            products = models.execute_kw(
                odoo_config["db"],
                uid,
                odoo_config["password"],
                'product.template',
                'read',
                [product_ids],
                {'fields': ['id', 'name', 'default_code', 'list_price', 'categ_id']}
            )
            
            print("\n🎯 PRODUCTOS REALES ENCONTRADOS:")
            print("-" * 40)
            for product in products:
                print(f"ID: {product['id']}")
                print(f"Nombre: {product['name']}")
                print(f"Código: {product.get('default_code', 'Sin código')}")
                print(f"Precio: {product.get('list_price', 0)}")
                print(f"Categoría ID: {product.get('categ_id', 'Sin categoría')}")
                print("-" * 40)
        
        print("\n✅ CONEXIÓN CON ODOO EXITOSA")
        print("✅ HAY PRODUCTOS REALES EN LA BASE DE DATOS")
        return True
        
    except xmlrpc.client.Fault as e:
        print(f"❌ Error XML-RPC: {e}")
        return False
    except ConnectionError as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Verifica que Odoo esté ejecutándose en el puerto correcto")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🧪 DIAGNÓSTICO DE DATOS REALES VS SIMULADOS")
    print("="*60)
    
    success = test_odoo_connection()
    
    print("\n" + "="*60)
    if success:
        print("🎉 ¡HAY DATOS REALES EN ODOO!")
        print("🔍 El problema debe estar en el código del servicio")
        print("💡 Revisar por qué se están usando datos fallback")
    else:
        print("❌ NO HAY DATOS REALES EN ODOO")
        print("💡 Por eso se muestran los datos simulados")
        print("🔧 Necesitas importar productos reales a Odoo")
    print("="*60)

if __name__ == "__main__":
    main()