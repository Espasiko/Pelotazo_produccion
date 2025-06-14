# Solución Completa: Escáner de Códigos de Barras Móvil → Odoo 18

## 🎯 Visión General de la Solución

Esta documentación describe cómo crear un sistema completo donde el marido puede escanear códigos de barras desde su móvil y los datos se envían automáticamente a Odoo 18 en los campos correctos.

## 📱 Arquitectura de la Solución

### 1. **App Móvil** (Frontend)
- Escáner de códigos de barras
- Interfaz simple para confirmar productos
- Envío automático de datos

### 2. **Backend API** (Servidor)
- Recibe datos del móvil
- Enriquece información del producto
- Envía a Odoo via XML-RPC

### 3. **Odoo 18** (Destino)
- Recibe productos automáticamente
- Actualiza stock/ventas
- Gestiona inventario

## 🔧 Implementación Paso a Paso

### Paso 1: Extender la App Flask Existente

Modificaremos `app_mapeo.py` para añadir endpoints móviles:

```python
# Nuevos endpoints para móvil
@app.route('/api/mobile/scan', methods=['POST'])
def mobile_scan_product():
    """Recibe código de barras desde móvil"""
    data = request.json
    barcode = data.get('barcode')
    action = data.get('action')  # 'sale' o 'stock_in'
    quantity = data.get('quantity', 1)
    
    # Buscar producto en base de datos de códigos de barras
    product_info = get_product_info_from_barcode(barcode)
    
    # Enviar a Odoo
    result = send_to_odoo(product_info, action, quantity)
    
    return jsonify(result)

@app.route('/api/mobile/products/<barcode>', methods=['GET'])
def get_product_by_barcode(barcode):
    """Obtiene información del producto por código de barras"""
    # Integración con API de Barcode Lookup o base de datos local
    product_info = lookup_product(barcode)
    return jsonify(product_info)
```

### Paso 2: Integración con API de Códigos de Barras

```python
import requests

def get_product_info_from_barcode(barcode):
    """Obtiene información del producto desde API externa"""
    # Opción 1: API gratuita de Open Food Facts
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 1:
                product = data['product']
                return {
                    'name': product.get('product_name', 'Producto sin nombre'),
                    'barcode': barcode,
                    'brand': product.get('brands', ''),
                    'category': product.get('categories', ''),
                    'image_url': product.get('image_url', ''),
                    'found': True
                }
    except:
        pass
    
    # Si no se encuentra, crear producto básico
    return {
        'name': f'Producto {barcode}',
        'barcode': barcode,
        'found': False
    }
```

### Paso 3: Conexión con Odoo 18

```python
import xmlrpc.client

class OdooConnector:
    def __init__(self):
        self.url = 'http://localhost:8069'
        self.db = 'tu_base_datos'
        self.username = 'admin'
        self.password = 'tu_password'
        self.uid = None
        self.models = None
        
    def connect(self):
        """Conecta con Odoo"""
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        return self.uid is not False
    
    def create_or_update_product(self, product_info):
        """Crea o actualiza producto en Odoo"""
        if not self.connect():
            return {'error': 'No se pudo conectar a Odoo'}
        
        # Buscar si el producto ya existe
        existing = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.template', 'search',
            [['barcode', '=', product_info['barcode']]]
        )
        
        product_data = {
            'name': product_info['name'],
            'barcode': product_info['barcode'],
            'type': 'product',
            'invoice_policy': 'order',
            'purchase_ok': True,
            'sale_ok': True,
        }
        
        if existing:
            # Actualizar producto existente
            self.models.execute_kw(
                self.db, self.uid, self.password,
                'product.template', 'write',
                [existing, product_data]
            )
            return {'success': True, 'action': 'updated', 'id': existing[0]}
        else:
            # Crear nuevo producto
            product_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                'product.template', 'create',
                [product_data]
            )
            return {'success': True, 'action': 'created', 'id': product_id}
    
    def register_sale(self, product_barcode, quantity=1):
        """Registra una venta en Odoo"""
        # Crear pedido de venta automático
        # Implementar lógica de venta
        pass
    
    def update_stock(self, product_barcode, quantity, location='stock'):
        """Actualiza stock del producto"""
        # Crear movimiento de stock
        # Implementar lógica de inventario
        pass
```

### Paso 4: App Móvil (PWA o App Nativa)

#### Opción A: PWA (Progressive Web App)

```html
<!-- mobile_scanner.html -->
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Escáner Tienda</title>
    <script src="https://unpkg.com/@zxing/library@latest"></script>
</head>
<body>
    <div id="scanner-container">
        <video id="video" width="100%" height="400px"></video>
        <div id="result"></div>
        <button onclick="startScan()">Iniciar Escáner</button>
        <button onclick="registerSale()">Registrar Venta</button>
        <button onclick="registerStock()">Entrada Stock</button>
    </div>
    
    <script>
        let lastBarcode = null;
        
        async function startScan() {
            const video = document.getElementById('video');
            const codeReader = new ZXing.BrowserBarcodeReader();
            
            try {
                const result = await codeReader.decodeOnceFromVideoDevice();
                lastBarcode = result.text;
                document.getElementById('result').innerHTML = 
                    `Código escaneado: ${lastBarcode}`;
                
                // Obtener info del producto
                const productInfo = await fetch(`/api/mobile/products/${lastBarcode}`);
                const product = await productInfo.json();
                
                document.getElementById('result').innerHTML += 
                    `<br>Producto: ${product.name}`;
                    
            } catch (err) {
                console.error(err);
            }
        }
        
        async function registerSale() {
            if (!lastBarcode) {
                alert('Primero escanea un producto');
                return;
            }
            
            const response = await fetch('/api/mobile/scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    barcode: lastBarcode,
                    action: 'sale',
                    quantity: 1
                })
            });
            
            const result = await response.json();
            alert(result.success ? 'Venta registrada!' : 'Error: ' + result.error);
        }
        
        async function registerStock() {
            if (!lastBarcode) {
                alert('Primero escanea un producto');
                return;
            }
            
            const quantity = prompt('¿Cuántas unidades?', '1');
            
            const response = await fetch('/api/mobile/scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    barcode: lastBarcode,
                    action: 'stock_in',
                    quantity: parseInt(quantity)
                })
            });
            
            const result = await response.json();
            alert(result.success ? 'Stock actualizado!' : 'Error: ' + result.error);
        }
    </script>
</body>
</html>
```

#### Opción B: App Android/iOS con React Native

```javascript
// ScannerApp.js
import React, { useState } from 'react';
import { BarCodeScanner } from 'expo-barcode-scanner';
import { View, Text, Button, Alert } from 'react-native';

export default function ScannerApp() {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const [lastBarcode, setLastBarcode] = useState(null);

  const handleBarCodeScanned = ({ type, data }) => {
    setScanned(true);
    setLastBarcode(data);
    Alert.alert('Código escaneado', data);
  };

  const registerSale = async () => {
    try {
      const response = await fetch('http://tu-servidor.com/api/mobile/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          barcode: lastBarcode,
          action: 'sale',
          quantity: 1
        })
      });
      
      const result = await response.json();
      Alert.alert(result.success ? 'Venta registrada!' : 'Error');
    } catch (error) {
      Alert.alert('Error de conexión');
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={{ flex: 1 }}
      />
      {lastBarcode && (
        <View>
          <Text>Último código: {lastBarcode}</Text>
          <Button title="Registrar Venta" onPress={registerSale} />
          <Button title="Escanear Otro" onPress={() => setScanned(false)} />
        </View>
      )}
    </View>
  );
}
```

## 🚀 Plan de Implementación

### Fase 1: Backend (1-2 días)
1. Extender `app_mapeo.py` con endpoints móviles
2. Implementar conexión con Odoo 18
3. Integrar API de códigos de barras
4. Probar conexiones

### Fase 2: Interfaz Móvil (2-3 días)
1. Crear PWA con escáner
2. Implementar interfaz simple
3. Conectar con backend
4. Pruebas en móvil

### Fase 3: Integración Odoo (1-2 días)
1. Configurar productos en Odoo
2. Probar creación automática
3. Configurar flujos de venta/stock
4. Validar datos

## 💡 Ventajas de Esta Solución

✅ **Simplicidad**: Una sola app para todo
✅ **Tiempo Real**: Datos inmediatos en Odoo
✅ **Sin Errores**: No hay transcripción manual
✅ **Económico**: Usa APIs gratuitas
✅ **Escalable**: Fácil añadir funciones
✅ **Compatible**: 100% integrado con Odoo 18

## 📋 Flujo de Trabajo

1. **Venta**: Marido escanea → Confirma venta → Se registra en Odoo
2. **Stock**: Marido escanea → Indica cantidad → Stock se actualiza
3. **Nuevo Producto**: Si no existe → Se crea automáticamente en Odoo

## 🔧 APIs Recomendadas para Códigos de Barras

### 1. Open Food Facts (Gratuita)
- **URL**: `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`
- **Ventajas**: Completamente gratuita, gran base de datos de alimentos
- **Limitaciones**: Principalmente productos alimentarios

### 2. UPC Database (Freemium)
- **URL**: `https://api.upcitemdb.com/prod/trial/lookup`
- **Ventajas**: Amplia gama de productos
- **Limitaciones**: 100 consultas/día gratis

### 3. Barcode Lookup (De pago)
- **URL**: API comercial
- **Ventajas**: Base de datos muy completa
- **Limitaciones**: Requiere suscripción ($99/mes)

## 📱 Configuración del Escáner

### Dependencias JavaScript
```html
<!-- Para PWA -->
<script src="https://unpkg.com/@zxing/library@latest"></script>
```

### Dependencias React Native
```bash
# Para app nativa
npm install expo-barcode-scanner
```

## 🔐 Configuración de Seguridad

### Variables de Entorno
```bash
# .env
ODOO_URL=http://localhost:8069
ODOO_DB=tu_base_datos
ODOO_USER=admin
ODOO_PASSWORD=tu_password_seguro
BARCODE_API_KEY=tu_api_key_opcional
```

### Autenticación
- Implementar tokens JWT para la app móvil
- Usar HTTPS en producción
- Validar permisos de usuario en cada endpoint

## 📊 Monitorización y Logs

### Logs Recomendados
- Escaneos realizados
- Productos creados/actualizados
- Errores de conexión con Odoo
- Tiempo de respuesta de APIs

### Métricas
- Número de escaneos por día
- Productos nuevos detectados
- Tasa de éxito de importación a Odoo
- Tiempo promedio de procesamiento

## 🚀 Próximos Pasos

1. **Implementar backend**: Extender `app_mapeo.py`
2. **Crear PWA**: Interfaz móvil simple
3. **Configurar Odoo**: Preparar campos y permisos
4. **Pruebas**: Validar flujo completo
5. **Despliegue**: Poner en producción

## 📞 Soporte y Mantenimiento

- **Actualizaciones**: Revisar APIs de códigos de barras mensualmente
- **Backup**: Respaldar configuraciones de Odoo
- **Monitoreo**: Alertas por fallos de conexión
- **Documentación**: Mantener este documento actualizado

---

**Fecha de creación**: Diciembre 2024
**Versión**: 1.0
**Compatibilidad**: Odoo 18, Python 3.8+, Flask 2.0+