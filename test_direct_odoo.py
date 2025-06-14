#!/usr/bin/env python3
"""
Script para probar directamente el OdooService y ver los logs detallados
"""

import sys
import os

# Agregar el directorio raíz al path
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_path)

# Importar directamente desde api
from api.services.odoo_service import OdooService
from api.utils.config import config

def test_odoo_service():
    """Prueba directa del OdooService"""
    print("=== PRUEBA DIRECTA DE ODOO SERVICE ===")
    
    # Mostrar configuración
    print(f"\n📋 CONFIGURACIÓN:")
    print(f"   URL: {config.ODOO_URL}")
    print(f"   DB: {config.ODOO_DB}")
    print(f"   User: {config.ODOO_USERNAME}")
    print(f"   Password: {'*' * len(config.ODOO_PASSWORD)}")
    
    # Crear instancia del servicio
    print(f"\n🔧 Creando instancia de OdooService...")
    odoo_service = OdooService()
    
    # Probar get_products
    print(f"\n🔍 Ejecutando get_products()...")
    print("=" * 50)
    
    try:
        products = odoo_service.get_products()
        
        print("=" * 50)
        print(f"\n📊 RESULTADO:")
        print(f"   Productos obtenidos: {len(products)}")
        
        if products:
            print(f"\n📦 PRIMEROS 3 PRODUCTOS:")
            for i, product in enumerate(products[:3], 1):
                print(f"   {i}. ID: {product.id}")
                print(f"      Nombre: {product.name}")
                print(f"      Código: {product.code}")
                print(f"      Categoría: {product.category}")
                print(f"      Precio: ${product.price}")
                print(f"      Stock: {product.stock}")
                print()
                
            # Verificar si son datos reales o fallback
            first_product = products[0]
            if first_product.name == "Refrigerador Samsung RT38K5982BS":
                print("🔍 ANÁLISIS: Estos son DATOS DE FALLBACK")
                print("   La conexión con Odoo no está funcionando correctamente.")
            else:
                print("🔍 ANÁLISIS: Estos son DATOS REALES de Odoo")
                print("   La conexión con Odoo está funcionando correctamente.")
        else:
            print("   ❌ No se obtuvieron productos")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print(f"\n📋 TRACEBACK:")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_odoo_service()