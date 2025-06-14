#!/bin/bash
# install.sh - Script de instalación completa ManusOdoo
# Incluye todas las dependencias para Odoo 18, FastAPI, React/Refine, y herramientas de migración

echo "=== Instalación ManusOdoo Completa ==="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[SYSTEM]${NC} $1"
}

# Verificar si el script se ejecuta como root
if [[ $EUID -eq 0 ]]; then
   print_error "Este script no debe ejecutarse como root"
   exit 1
fi

# Actualizar sistema
print_status "Actualizando sistema..."
sudo apt-get update
sudo apt-get upgrade -y

# Verificar e instalar Docker
if ! command -v docker &> /dev/null; then
    print_status "Docker no está instalado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    print_status "Docker instalado correctamente"
else
    print_status "Docker ya está instalado"
fi

# Verificar e instalar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_status "Docker Compose no está instalado. Instalando..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_status "Docker Compose instalado correctamente"
else
    print_status "Docker Compose ya está instalado"
fi

# Verificar e instalar Node.js
if ! command -v node &> /dev/null; then
    print_status "Node.js no está instalado. Instalando..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    print_status "Node.js instalado correctamente"
else
    NODE_VERSION=$(node --version)
    print_status "Node.js ya está instalado (versión: $NODE_VERSION)"
fi

# Verificar e instalar Python
if ! command -v python3 &> /dev/null; then
    print_status "Python3 no está instalado. Instalando..."
    sudo apt-get install -y python3 python3-pip python3-venv
    print_status "Python3 instalado correctamente"
else
    PYTHON_VERSION=$(python3 --version)
    print_status "Python3 ya está instalado (versión: $PYTHON_VERSION)"
fi

# Instalar dependencias adicionales del sistema
print_status "Instalando dependencias adicionales del sistema..."
sudo apt-get install -y curl wget git build-essential software-properties-common
sudo apt-get install -y libpq-dev python3-dev python3-venv python3-pip
sudo apt-get install -y postgresql-client libxml2-dev libxslt1-dev zlib1g-dev
sudo apt-get install -y libjpeg-dev libfreetype6-dev liblcms2-dev libopenjp2-7-dev
sudo apt-get install -y libtiff5-dev tk-dev tcl-dev libharfbuzz-dev libfribidi-dev
sudo apt-get install -y libxcb1-dev

# Crear directorios necesarios
print_status "Creando directorios necesarios..."
mkdir -p addons config logs informes tmp odoo_import plantillasodoo
mkdir -p api/models api/routes api/services api/utils
mkdir -p src public static templates tests

# Configurar entorno virtual Python
print_status "Configurando entorno virtual Python..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Entorno virtual Python creado"
else
    print_status "Entorno virtual Python ya existe"
fi

# Activar entorno virtual e instalar dependencias Python
print_status "Instalando dependencias Python..."
source venv/bin/activate
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    print_status "Dependencias Python instaladas desde requirements.txt"
else
    print_warning "requirements.txt no encontrado, instalando dependencias básicas"
    pip install --upgrade pip
    pip install fastapi uvicorn pydantic python-multipart python-jose PyJWT
    pip install pandas openpyxl xlrd requests xmlrpc-client
    pip install python-dotenv aiofiles jinja2
fi
deactivate

# Instalar dependencias Node.js y construir frontend
print_status "Instalando dependencias Node.js..."
if [ -f "package.json" ]; then
    npm install
    print_status "Dependencias Node.js instaladas"
    
    # Construir aplicación frontend
    print_status "Construyendo aplicación frontend..."
    npm run build 2>/dev/null || print_warning "No se pudo ejecutar npm run build (normal en desarrollo)"
else
    print_warning "package.json no encontrado, saltando instalación de Node.js"
fi

# Hacer ejecutables los scripts
print_status "Configurando permisos de scripts..."
chmod +x start.sh 2>/dev/null || true
chmod +x stop.sh 2>/dev/null || true
chmod +x dev-dashboard.sh 2>/dev/null || true
chmod +x backup.sh 2>/dev/null || true
chmod +x analizar_excel.py 2>/dev/null || true
chmod +x analizar_proveedor.py 2>/dev/null || true
chmod +x script_migracion_categorias.py 2>/dev/null || true
chmod +x script_migracion_excel_odoo.py 2>/dev/null || true
chmod +x menu_principal.py 2>/dev/null || true
chmod +x verificar_instalacion.py 2>/dev/null || true

# Crear archivos de configuración si no existen
print_status "Configurando archivos de entorno..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Configuración ManusOdoo
ODOO_URL=http://localhost:8069
ODOO_DB=manusodoo
ODOO_USER=admin
ODOO_PASSWORD=admin
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ODOO_URL=http://localhost:8069
EOF
    print_status "Archivo .env creado con configuración por defecto"
else
    print_status "Archivo .env ya existe"
fi

# Verificar Docker Compose
print_status "Verificando configuración Docker..."
if [ -f "docker-compose.yml" ]; then
    docker-compose config > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_status "Configuración Docker Compose válida"
    else
        print_error "Error en configuración Docker Compose"
    fi
else
    print_warning "docker-compose.yml no encontrado"
fi

# Verificar instalación completa
print_status "Verificando instalación completa..."

# Verificar Docker
if command -v docker &> /dev/null; then
    print_status "✓ Docker instalado correctamente"
    # Verificar si Docker está ejecutándose
    if docker info &> /dev/null; then
        print_status "✓ Docker está ejecutándose"
    else
        print_warning "⚠ Docker instalado pero no está ejecutándose"
    fi
else
    print_error "✗ Docker no está instalado"
    exit 1
fi

# Verificar Docker Compose
if command -v docker-compose &> /dev/null; then
    print_status "✓ Docker Compose instalado correctamente"
else
    print_error "✗ Docker Compose no está instalado"
    exit 1
fi

# Verificar Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "✓ Node.js instalado correctamente ($NODE_VERSION)"
else
    print_error "✗ Node.js no está instalado"
    exit 1
fi

# Verificar npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_status "✓ npm instalado correctamente ($NPM_VERSION)"
else
    print_error "✗ npm no está instalado"
    exit 1
fi

# Verificar Python3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "✓ Python3 instalado correctamente ($PYTHON_VERSION)"
else
    print_error "✗ Python3 no está instalado"
    exit 1
fi

# Verificar pip
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    print_status "✓ pip instalado correctamente"
else
    print_error "✗ pip no está instalado"
    exit 1
fi

# Verificar entorno virtual Python
if [ -d "venv" ]; then
    print_status "✓ Entorno virtual Python configurado"
else
    print_warning "⚠ Entorno virtual Python no encontrado"
fi

# Verificar archivos de configuración
if [ -f "docker-compose.yml" ]; then
    print_status "✓ docker-compose.yml presente"
else
    print_warning "⚠ docker-compose.yml no encontrado"
fi

if [ -f "requirements.txt" ]; then
    print_status "✓ requirements.txt presente"
else
    print_warning "⚠ requirements.txt no encontrado"
fi

if [ -f "package.json" ]; then
    print_status "✓ package.json presente"
else
    print_warning "⚠ package.json no encontrado"
fi

# Verificar scripts de migración
MIGRATION_SCRIPTS=("script_migracion_categorias.py" "script_migracion_excel_odoo.py" "menu_principal.py")
for script in "${MIGRATION_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        print_status "✓ $script presente"
    else
        print_warning "⚠ $script no encontrado"
    fi
done

echo ""
print_status "🎉 ¡Instalación de ManusOdoo completada con éxito!"
echo ""
print_info "📋 INSTRUCCIONES DE USO:"
print_info "1. Para iniciar el sistema completo: ./start.sh"
print_info "2. Accede a Odoo 18 en: http://localhost:8069"
print_info "3. API FastAPI disponible en: http://localhost:8000"
print_info "4. Dashboard de desarrollo: ./dev-dashboard.sh"
print_info "5. Scripts de migración: python3 menu_principal.py"
echo ""
print_info "📁 DIRECTORIOS CREADOS:"
print_info "- addons/ (módulos personalizados Odoo)"
print_info "- config/ (configuraciones)"
print_info "- logs/ (registros del sistema)"
print_info "- odoo_import/ (archivos de importación)"
print_info "- plantillasodoo/ (plantillas de migración)"
print_info "- api/ (código FastAPI)"
echo ""
print_warning "⚠️  IMPORTANTE - PERMISOS DOCKER:"
print_warning "Si tienes problemas con Docker, ejecuta:"
print_warning "sudo usermod -aG docker $USER"
print_warning "Luego cierra sesión y vuelve a iniciar sesión"
echo ""
print_info "🔧 HERRAMIENTAS DE MIGRACIÓN DISPONIBLES:"
print_info "- Análisis de Excel: python3 analizar_excel.py"
print_info "- Migración de categorías: python3 script_migracion_categorias.py"
print_info "- Migración completa: python3 script_migracion_excel_odoo.py"
print_info "- Menú principal: python3 menu_principal.py"
echo ""

if [ $? -ne 0 ]; then
    print_error "❌ La instalación no se completó correctamente"
    exit 1
fi