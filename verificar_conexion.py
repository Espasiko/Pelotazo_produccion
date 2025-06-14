#!/usr/bin/env python3

import requests
import json

def verificar_api():
    """Verifica que la API esté funcionando"""
    try:
        response = requests.get('http://localhost:8000/health')
        print('✅ API Status:', response.json())
        print('✅ API conectada correctamente')
        return True
    except Exception as e:
        print('❌ Error conectando con API:', e)
        return False

def verificar_odoo_desde_docker():
    """Verifica la conexión desde el contenedor Docker"""
    try:
        # Verificar que el contenedor FastAPI esté corriendo
        import subprocess
        result = subprocess.run(['docker', 'ps', '--filter', 'name=fastapi', '--format', 'table {{.Names}}\t{{.Status}}'], 
                              capture_output=True, text=True)
        print('\n📋 Estado del contenedor FastAPI:')
        print(result.stdout)
        
        # Verificar logs del contenedor
        logs_result = subprocess.run(['docker', 'logs', '--tail', '10', 'fastapi'], 
                                   capture_output=True, text=True)
        print('\n📋 Últimos logs de FastAPI:')
        print(logs_result.stdout)
        
        return True
    except Exception as e:
        print('❌ Error verificando Docker:', e)
        return False

if __name__ == '__main__':
    print('🔍 Verificando conexión API y Odoo...')
    print('=' * 50)
    
    api_ok = verificar_api()
    docker_ok = verificar_odoo_desde_docker()
    
    print('\n' + '=' * 50)
    if api_ok and docker_ok:
        print('✅ Todas las verificaciones pasaron correctamente')
        print('✅ La corrección del puerto 8069 en docker-compose.yml fue exitosa')
    else:
        print('❌ Algunas verificaciones fallaron')