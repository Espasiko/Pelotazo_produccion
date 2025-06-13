# Memoria técnica 13/06 - Fastmal

## Resumen de cambios
- Subida de cambios a la rama `fastmal` para preservar el estado del contenedor y la configuración actual.
- Incluye `Dockerfile.fastapi`, ajustes en `docker-compose.yml`, `start.sh` y `README.md`.
- Estado funcional parcial: el backend FastAPI y el frontend React están configurados, pero persisten problemas de conexión y CSP.

## Puertos expuestos
- **FastAPI:** 8000
- **Frontend React:** 3001
- **Odoo 18:** 8070 y 8069

## Contenedores activos
- `fastapi`
- `frontend`
- `odoo18`

## Configuración de red y docker
- `docker-compose.yml` expone los puertos correctamente para cada servicio.
- No existen referencias a 8001 en la configuración actual.
- El archivo `Dockerfile.fastapi` expone el puerto 8000 y utiliza `uvicorn` para levantar el backend.

## Estado actual y pendientes
- Persisten problemas de conexión entre frontend y backend (CSP y posibles CORS).
- Pendiente revisar la integración entre servicios y realizar pruebas de comunicación.
- Se ha hecho push de la rama `fastmal` al repositorio remoto para respaldo.

## Observaciones adicionales
- Revisar logs de errores y configuración de CSP en el frontend.
- Confirmar que Odoo 18 funciona correctamente en los puertos definidos.
- Documentar cualquier cambio adicional relevante en futuras actualizaciones.