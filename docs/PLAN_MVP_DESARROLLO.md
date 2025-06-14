# 📋 PLAN DE DESARROLLO MVP - ManusOdoo

**Fecha:** 14 de Junio de 2025  
**Objetivo:** Crear un Producto Mínimo Viable (MVP) funcional para presentar a la dueña del negocio

---

## 🎯 ANÁLISIS DEL ESTADO ACTUAL

### ✅ **Componentes Ya Implementados:**

#### **Backend (FastAPI + Odoo 18):**
- ✅ Docker Compose configurado (PostgreSQL, Odoo 18, Adminer, FastAPI)
- ✅ Scripts de migración de datos desde Excel
- ✅ Sistema de mapeo de categorías y productos
- ✅ API FastAPI básica configurada
- ✅ Conexión con Odoo 18 establecida

#### **Frontend (React + Refine + Ant Design):**
- ✅ Dashboard principal implementado
- ✅ Módulos básicos: Products, Inventory, Sales, Customers, Reports, Providers
- ✅ Tema oscuro configurado
- ✅ Integración con Refine framework
- ✅ Componentes de navegación (Header, Sider)

#### **Scripts de Utilidad:**
- ✅ Script de instalación completo (`install.sh`)
- ✅ Scripts de análisis de Excel
- ✅ Herramientas de migración de datos
- ✅ Sistema de verificación de instalación

---

## 🚀 PLAN DE DESARROLLO MVP (2-3 SEMANAS)

### **FASE 1: FUNCIONALIDADES CORE (Semana 1)**

#### **1.1 Sistema de Migración de Datos Excel → Odoo 18**
**Prioridad:** 🔴 CRÍTICA

**Tareas:**
- [ ] Mejorar interfaz web para `script_migracion_excel_odoo.py`
- [ ] Crear endpoint FastAPI para subida de archivos Excel
- [ ] Implementar validación de datos antes de migración
- [ ] Dashboard de progreso de migración en tiempo real
- [ ] Sistema de rollback en caso de errores

**Módulos Odoo 18 Requeridos:**
- ✅ `base_import` (incluido por defecto)
- ✅ `product` (incluido por defecto)
- ✅ `stock` (incluido por defecto)

**Tiempo estimado:** 3-4 días

#### **1.2 Sistema de Alertas Básicas**
**Prioridad:** 🟡 ALTA

**Tareas:**
- [ ] Implementar alertas de stock bajo usando módulo nativo de Odoo 18
- [ ] Sistema de notificaciones por email
- [ ] Dashboard de alertas en React
- [ ] Configuración de umbrales de stock

**Módulos Odoo 18 Requeridos:**
- ✅ `stock` (reordering rules incluidas)
- 🆓 `mail` (notificaciones por email)
- 🆓 Módulo adicional: `product_low_stock_notification` (gratuito)

**Tiempo estimado:** 2-3 días

### **FASE 2: FUNCIONALIDADES AVANZADAS (Semana 2)**

#### **2.1 Sistema de Códigos de Barras con Móvil**
**Prioridad:** 🟡 ALTA

**Tareas:**
- [ ] Configurar módulo Barcode de Odoo 18
- [ ] Implementar escáner web usando cámara del móvil
- [ ] Integración con inventario para entrada/salida de productos
- [ ] PWA (Progressive Web App) para uso móvil

**Módulos Odoo 18 Requeridos:**
- ✅ `barcodes` (incluido en Odoo 18)
- ✅ `stock_barcode` (incluido en Odoo 18)
- 🆓 Módulo adicional: `sh_invoice_barcode_mobile` (gratuito)

**Tecnologías Frontend:**
- `@zxing/library` para lectura de códigos de barras
- PWA con service workers

**Tiempo estimado:** 4-5 días

#### **2.2 Dashboard de Estadísticas y Reportes**
**Prioridad:** 🟡 ALTA

**Tareas:**
- [ ] Gráficos de ventas en tiempo real
- [ ] Estadísticas de inventario
- [ ] Reportes de ingresos y gastos
- [ ] Indicadores KPI principales

**Módulos Odoo 18 Requeridos:**
- ✅ `sale_management` (incluido)
- ✅ `account` (incluido)
- ✅ `stock` (incluido)
- 🆓 `dashboard` (nativo de Odoo 18)

**Librerías Frontend:**
- `@ant-design/charts` para gráficos
- `recharts` como alternativa

**Tiempo estimado:** 3-4 días

### **FASE 3: SISTEMA OCR Y REFINAMIENTOS (Semana 3)**

#### **3.1 Sistema OCR para Facturas con Mistral AI**
**Prioridad:** 🟠 MEDIA (para MVP)

**Tareas:**
- [ ] Integración con API de Mistral AI
- [ ] Endpoint FastAPI para procesamiento de facturas
- [ ] Extracción de datos: proveedor, productos, precios, fechas
- [ ] Validación y corrección manual de datos extraídos
- [ ] Creación automática de facturas en Odoo 18

**Módulos Odoo 18 Requeridos:**
- ✅ `account` (facturación)
- 🆓 Módulo adicional: `ocr_invoice` (€249.99 - ALTERNATIVA: desarrollar propio)

**Tecnologías:**
- API Mistral AI para OCR
- `python-multipart` para subida de archivos
- `Pillow` para procesamiento de imágenes

**Tiempo estimado:** 5-6 días

#### **3.2 Sistema de Alertas Avanzadas**
**Prioridad:** 🟠 MEDIA

**Tareas:**
- [ ] Alertas de fechas de pago próximas
- [ ] Recordatorios de backup diario
- [ ] Alertas de vencimiento de productos
- [ ] Notificaciones push en PWA

**Tiempo estimado:** 2-3 días

---

## 🛠️ IMPLEMENTACIÓN TÉCNICA

### **Arquitectura Propuesta:**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React PWA     │    │   FastAPI        │    │   Odoo 18       │
│   (Frontend)    │◄──►│   (API Gateway)  │◄──►│   (ERP Core)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PWA Cache     │    │   Mistral AI     │    │   PostgreSQL    │
│   Service Worker│    │   OCR Service    │    │   Database      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### **Tecnologías Clave:**

#### **Backend:**
- **FastAPI**: API REST principal
- **Odoo 18**: ERP core con módulos nativos
- **PostgreSQL**: Base de datos
- **Mistral AI**: Procesamiento OCR

#### **Frontend:**
- **React 18**: Framework principal
- **Refine**: Framework de admin dashboard
- **Ant Design**: Componentes UI
- **PWA**: Aplicación web progresiva
- **@zxing/library**: Lectura de códigos de barras

#### **DevOps:**
- **Docker Compose**: Orquestación de servicios
- **Nginx**: Proxy reverso (a añadir)

---

## 📦 MÓDULOS ODOO 18 REQUERIDOS

### **Módulos Nativos (Gratuitos):**
- ✅ `base_import` - Importación de datos
- ✅ `product` - Gestión de productos
- ✅ `stock` - Gestión de inventario
- ✅ `barcodes` - Códigos de barras
- ✅ `stock_barcode` - Inventario con códigos de barras
- ✅ `sale_management` - Gestión de ventas
- ✅ `account` - Contabilidad y facturación
- ✅ `mail` - Sistema de notificaciones
- ✅ `dashboard` - Tableros de control

### **Módulos de Terceros (Gratuitos):**
- 🆓 `product_low_stock_notification` - Alertas de stock bajo
- 🆓 `sh_invoice_barcode_mobile` - Escáner móvil para facturas

### **Funcionalidades a Desarrollar:**
- 🔧 **OCR con Mistral AI** - Sistema personalizado
- 🔧 **Dashboard React** - Interfaz personalizada
- 🔧 **PWA Mobile** - Aplicación móvil web

---

## ⚡ CRONOGRAMA DETALLADO

### **Semana 1: Core MVP**
| Día | Tarea | Responsable | Estado |
|-----|-------|-------------|--------|
| 1-2 | Migración Excel mejorada | Dev | 🔄 |
| 3-4 | Sistema de alertas básicas | Dev | ⏳ |
| 5 | Testing y correcciones | Dev | ⏳ |

### **Semana 2: Funcionalidades Avanzadas**
| Día | Tarea | Responsable | Estado |
|-----|-------|-------------|--------|
| 1-3 | Sistema códigos de barras | Dev | ⏳ |
| 4-5 | Dashboard estadísticas | Dev | ⏳ |

### **Semana 3: OCR y Refinamientos**
| Día | Tarea | Responsable | Estado |
|-----|-------|-------------|--------|
| 1-4 | Sistema OCR Mistral AI | Dev | ⏳ |
| 5 | Alertas avanzadas | Dev | ⏳ |

---

## 🎯 CRITERIOS DE ÉXITO MVP

### **Funcionalidades Mínimas Requeridas:**
1. ✅ **Migración de datos Excel** - Funcional al 100%
2. ✅ **Alertas de stock bajo** - Configuradas y funcionando
3. ✅ **Dashboard básico** - Métricas principales visibles
4. ✅ **Códigos de barras móvil** - Lectura básica funcionando
5. 🔄 **OCR básico** - Al menos facturas simples

### **Métricas de Rendimiento:**
- **Tiempo de migración**: < 5 minutos para 1000 productos
- **Tiempo de respuesta API**: < 2 segundos
- **Precisión OCR**: > 80% en facturas estándar
- **Compatibilidad móvil**: iOS Safari + Android Chrome

---

## 🚨 RIESGOS Y MITIGACIONES

### **Riesgos Técnicos:**
1. **API Mistral AI**: Límites de uso → Implementar cache y fallbacks
2. **Rendimiento móvil**: Cámara lenta → Optimizar librerías
3. **Migración de datos**: Errores de mapeo → Validaciones exhaustivas

### **Riesgos de Tiempo:**
1. **OCR complejo**: Facturas no estándar → Empezar con formatos simples
2. **Testing insuficiente**: Bugs en producción → Testing continuo

---

## 💰 ESTIMACIÓN DE COSTOS

### **Servicios Externos:**
- **Mistral AI API**: ~€50-100/mes (estimado)
- **Hosting**: €20-50/mes (VPS)
- **Dominio**: €10/año

### **Módulos de Pago (Opcionales):**
- **OCR Invoice Premium**: €249.99 (una vez)
- **Módulos adicionales**: €0-500 (según necesidades)

**Total estimado MVP**: €100-200/mes operativo

---

## 📋 PRÓXIMOS PASOS INMEDIATOS

### **Hoy (14/06/2025):**
1. [ ] Revisar y aprobar este plan con la dueña del negocio
2. [ ] Configurar entorno de desarrollo actualizado
3. [ ] Instalar módulos Odoo 18 requeridos

### **Mañana (15/06/2025):**
1. [ ] Comenzar mejoras en migración Excel
2. [ ] Configurar módulo de alertas de stock
3. [ ] Preparar entorno de testing

### **Esta Semana:**
1. [ ] Completar Fase 1 del MVP
2. [ ] Preparar demo funcional básico
3. [ ] Documentar APIs y endpoints

---

## 🎉 ENTREGABLES MVP

### **Demo Funcional Incluirá:**
1. **Dashboard principal** con métricas en tiempo real
2. **Sistema de migración** con interfaz web
3. **Alertas de stock** configuradas y funcionando
4. **Escáner de códigos de barras** desde móvil
5. **OCR básico** para facturas simples
6. **Reportes básicos** de ventas e inventario

### **Documentación:**
1. Manual de usuario básico
2. Guía de instalación actualizada
3. API documentation
4. Plan de escalabilidad post-MVP

---

**¡El MVP estará listo para presentación en 2-3 semanas!** 🚀

---

*Documento creado el 14 de Junio de 2025*  
*Proyecto: ManusOdoo - Sistema ERP Integrado*