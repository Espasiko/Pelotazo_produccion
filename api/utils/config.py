import os
from typing import Optional

class Config:
    """Configuración centralizada de la aplicación"""
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "odoo_middleware_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Configuración de la API
    API_TITLE: str = "Odoo Middleware API"
    API_DESCRIPTION: str = "API para simular Odoo y facilitar el desarrollo del dashboard"
    API_VERSION: str = "1.0.0"
    
    # Configuración de CORS
    CORS_ORIGINS: list = ["*"]  # En producción, especificar orígenes exactos
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Configuración de Odoo
    ODOO_URL: str = os.getenv("ODOO_URL", "http://localhost:8070")
    ODOO_DB: str = os.getenv("ODOO_DB", "manus_odoo-bd")
    ODOO_USERNAME: str = os.getenv("ODOO_USERNAME", "yo@mail.com")
    ODOO_PASSWORD: str = os.getenv("ODOO_PASSWORD", "admin")
    
    # Configuración de paginación
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    # Configuración de logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_odoo_config(cls) -> dict:
        """Retorna la configuración de Odoo como diccionario"""
        return {
            "url": cls.ODOO_URL,
            "db": cls.ODOO_DB,
            "username": cls.ODOO_USERNAME,
            "password": cls.ODOO_PASSWORD
        }

config = Config()
