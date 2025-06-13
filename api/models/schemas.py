from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Generic, TypeVar
from datetime import datetime
from pydantic import BaseModel

T = TypeVar('T')

# Modelos de autenticación
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Modelos de negocio
class Product(BaseModel):
    id: int
    name: str  # Campo obligatorio en Odoo
    description: Optional[str] = None
    price: Optional[float] = None  # list_price es opcional en Odoo
    category: Optional[str] = None  # categ_id es opcional
    stock_quantity: Optional[int] = None
    sku: Optional[str] = None  # default_code es opcional
    image_url: Optional[str] = None
    is_active: bool = True

class ProductCreate(BaseModel):
    name: str  # Campo obligatorio
    code: Optional[str] = None  # default_code es opcional
    category: Optional[str] = None  # categ_id es opcional
    price: Optional[float] = None  # list_price es opcional
    stock: Optional[int] = None  # stock es opcional
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None

class InventoryItem(BaseModel):
    id: int
    product_id: int  # Campo obligatorio en stock.quant
    product_name: str
    quantity: float  # Campo obligatorio en stock.quant
    location: str  # location_id es obligatorio
    location_id: Optional[int] = None
    lot_id: Optional[int] = None  # Opcional
    package_id: Optional[int] = None  # Opcional
    owner_id: Optional[int] = None  # Opcional
    last_updated: datetime

class InventoryItemCreate(BaseModel):
    product_id: int  # Campo obligatorio
    quantity: float  # Campo obligatorio
    location: str  # Campo obligatorio
    location_id: Optional[int] = None
    lot_id: Optional[int] = None
    package_id: Optional[int] = None
    owner_id: Optional[int] = None

class Sale(BaseModel):
    id: int
    partner_id: int  # Campo obligatorio en sale.order (customer)
    customer_id: Optional[int] = None  # Mantenemos compatibilidad
    customer_name: Optional[str] = None
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None
    total_amount: float
    date: datetime
    status: str  # state field en Odoo
    reference: Optional[str] = None
    order_line: Optional[List[Dict[str, Any]]] = []  # Líneas de pedido
    state: Optional[str] = "draft"  # Estados: draft, sent, sale, done, cancel

class SaleCreate(BaseModel):
    partner_id: int  # Campo obligatorio
    customer_id: Optional[int] = None  # Compatibilidad
    customer_name: Optional[str] = None
    reference: Optional[str] = None
    customer: Optional[str] = None
    date: Optional[datetime] = None
    total: Optional[float] = None
    total_amount: Optional[float] = 0.0
    status: Optional[str] = "draft"
    order_line: Optional[List[Dict[str, Any]]] = []
    state: Optional[str] = "draft"

class Customer(BaseModel):
    id: int
    name: str  # Campo obligatorio en res.partner
    email: Optional[str] = None  # Opcional en Odoo
    phone: Optional[str] = None  # Opcional en Odoo
    address: Optional[str] = None  # street es opcional
    street: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    customer: bool = True  # Marca como cliente
    supplier: bool = False  # Marca como proveedor
    total_purchases: Optional[float] = 0.0

class CustomerCreate(BaseModel):
    name: str  # Campo obligatorio
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    customer: bool = True
    supplier: bool = False
    status: Optional[str] = "Activo"

class Provider(BaseModel):
    id: int
    name: str  # Campo obligatorio en res.partner
    email: Optional[str] = None  # Opcional en Odoo
    phone: Optional[str] = None  # Opcional en Odoo
    street: Optional[str] = None  # Opcional
    city: Optional[str] = None  # Opcional
    country_id: Optional[int] = None  # Opcional
    country: Optional[str] = None  # Mantenemos compatibilidad
    customer: bool = False  # Marca como cliente
    supplier: bool = True  # Marca como proveedor

class ProviderCreate(BaseModel):
    name: str  # Campo obligatorio
    email: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    country: Optional[str] = None
    customer: bool = False
    supplier: bool = True

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    tax_calculation_method: Optional[str] = None
    discount_type: Optional[str] = None
    payment_term: Optional[str] = None
    incentive_rules: Optional[str] = None
    status: Optional[str] = None

# Modelos de respuesta
class SessionResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

class DashboardStats(BaseModel):
    total_products: Optional[int] = 0
    total_sales: Optional[float] = 0.0
    total_customers: Optional[int] = 0
    total_inventory_value: Optional[float] = 0.0
    recent_sales: Optional[List[Sale]] = []
    low_stock_products: Optional[List[Product]] = []

# Modelos de paginación
class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10
    
class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    size: int
    pages: int
