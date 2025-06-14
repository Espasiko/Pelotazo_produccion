#!/usr/bin/env python3
"""
Script para debuggear por qué FastAPI no se conecta correctamente a Odoo
"""

import sys
import os
sys.path.append('/home/espasiko/mainmanusodoo/manusodoo-roto')

from api.services.odoo_service import OdooService
from api.utils.config import config

def debug_fastapi_odoo_connection():
    """Debuggea la conexión de FastAPI con Odoo"""
    
    print("=== DEBUG: CONEXIÓN FASTAPI-ODOO ===")
    print("\n1. VERIFICANDO CONFIGURACIÓN...")
    
    # Verificar configuración
    odoo_config = config.get_odoo_config()
    print(f"Configuración de Odoo:")
    for key, value in odoo_config.items():
        print(f"  - {key}: {value}")
    
    print("\n2. CREANDO INSTANCIA DE ODOO SERVICE...")
    try:
        odoo_service = OdooService()
        print("✓ Instancia de OdooService creada")
    except Exception as e:
        print(f"✗ Error creando OdooService: {e}")
        return False
    
    print("\n3. PROBANDO CONEXIÓN DIRECTA...")
    try:
        # Probar conexión directa
        connection_result = odoo_service._get_connection()
        print(f"Resultado de conexión: {connection_result}")
        
        if connection_result:
            print("✓ Conexión establecida exitosamente")
            print(f"UID obtenido: {odoo_service._uid}")
        else:
            print("✗ Fallo en la conexión")
            return False
            
    except Exception as e:
        print(f"✗ Error en conexión: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    print("\n4. PROBANDO EJECUCIÓN DE CONSULTAS...")
    try:
        # Probar búsqueda de productos
        print("4.1. Probando búsqueda de productos...")
        product_ids = odoo_service._execute_kw('product.template', 'search', [[]])
        print(f"IDs de productos encontrados: {len(product_ids) if product_ids else 0}")
        
        if product_ids:
            print(f"Primeros 5 IDs: {product_ids[:5]}")
            
            # Probar lectura de productos
            print("4.2. Probando lectura de productos...")
            products_data = odoo_service._execute_kw(
                'product.template', 
                'read', 
                [product_ids[:3]],
                {'fields': ['id', 'name', 'default_code', 'list_price']}
            )
            
            if products_data:
                print(f"✓ Datos de productos obtenidos: {len(products_data)} productos")
                for product in products_data:
                    print(f"  - {product['name']} (ID: {product['id']})")
            else:
                print("✗ No se pudieron leer los datos de productos")
        else:
            print("⚠ No se encontraron productos")
            
    except Exception as e:
        print(f"✗ Error ejecutando consultas: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
    
    print("\n5. PROBANDO MÉTODO get_products() COMPLETO...")
    try:
        products = odoo_service.get_products()
        print(f"Productos obtenidos por get_products(): {len(products)}")
        
        if products:
            print("Primeros 3 productos:")
            for i, product in enumerate(products[:3]):
                print(f"  {i+1}. {product.name} - Precio: {product.price} - Stock: {product.stock}")
                
            # Verificar si son datos reales o de fallback
            fallback_names = ["Refrigerador Samsung", "Lavadora LG", "Televisor Sony"]
            is_fallback = any(product.name in fallback_names for product in products[:3])
            
            if is_fallback:
                print("\n⚠ DETECTADO: Los datos son de FALLBACK (simulados)")
                print("Esto significa que la conexión a Odoo falló en algún punto")
            else:
                print("\n✓ Los datos parecen ser REALES de Odoo")
        else:
            print("✗ No se obtuvieron productos")
            
    except Exception as e:
        print(f"✗ Error en get_products(): {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
    
    print("\n" + "="*60)
    return True

def test_category_resolution():
    """Prueba la resolución de categorías"""
    print("\n=== PROBANDO RESOLUCIÓN DE CATEGORÍAS ===")
    
    try:
        odoo_service = OdooService()
        
        # Probar método _get_category_name si existe
        if hasattr(odoo_service, '_get_category_name'):
            print("Probando _get_category_name...")
            # Simular una categoría
            test_category = [1, 'Categoría de Prueba']
            category_name = odoo_service._get_category_name(test_category)
            print(f"Resultado: {category_name}")
        else:
            print("Método _get_category_name no encontrado")
            
    except Exception as e:
        print(f"Error probando categorías: {e}")

if __name__ == "__main__":
    print("Iniciando debug de conexión FastAPI-Odoo...\n")
    
    success = debug_fastapi_odoo_connection()
    test_category_resolution()
    
    if success:
        print("\n🔍 ANÁLISIS COMPLETADO")
        print("Si los datos son de fallback, revisa:")
        print("1. Manejo de excepciones en odoo_service.py")
        print("2. Configuración de variables de entorno")
        print("3. Permisos de acceso a la base de datos")
    else:
        print("\n❌ DEBUG FALLÓ - Revisa los errores anteriores")