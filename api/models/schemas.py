from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Generic, TypeVar
from datetime import datetime

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
    name: str
    code: str
    category: str
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductCreate(BaseModel):
    name: str
    code: str
    category: str
    price: float
    stock: int
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
    product_id: int
    product_name: str
    quantity: int
    location: str
    last_updated: str
    code: Optional[str] = None
    reserved: Optional[int] = None

class Sale(BaseModel):
    id: int
    customer_id: int
    customer_name: str
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total: float
    date: str
    status: str
    reference: Optional[str] = None

class SaleCreate(BaseModel):
    reference: str
    customer: str
    date: str
    total: float
    status: str

class Customer(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    total_purchases: float
    city: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = "Activo"

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    city: str
    country: str
    status: str = "Activo"

class Provider(BaseModel):
    id: int
    name: str
    tax_calculation_method: str
    discount_type: str
    payment_term: str
    incentive_rules: Optional[str] = None
    status: str = "active"

class ProviderCreate(BaseModel):
    name: str
    tax_calculation_method: str
    discount_type: str
    payment_term: str
    incentive_rules: Optional[str] = None
    status: str = "active"

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    tax_calculation_method: Optional[str] = None
    discount_type: Optional[str] = None
    payment_term: Optional[str] = None
    incentive_rules: Optional[str] = None
    status: Optional[str] = None

# Modelos de respuesta
class SessionResponse(BaseModel):
    uid: int
    username: str
    name: str
    session_id: str
    db: str

class DashboardStats(BaseModel):
    total_products: int
    low_stock: int
    sales_this_month: int
    active_customers: int
    top_categories: List[Dict[str, Any]]

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
