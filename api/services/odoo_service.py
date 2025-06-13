import xmlrpc.client
import gc
from typing import List, Optional, Dict, Any
from ..utils.config import config
from ..models.schemas import Product, Provider, Customer, Sale, ProductCreate

class OdooService:
    """Servicio para interactuar con Odoo via XML-RPC"""
    
    def __init__(self):
        self.config = config.get_odoo_config()
        self._common = None
        self._models = None
        self._uid = None
    
    def _get_connection(self):
        """Establece conexión con Odoo"""
        try:
            if not self._common:
                self._common = xmlrpc.client.ServerProxy(f'{self.config["url"]}/xmlrpc/2/common')
            
            if not self._uid:
                self._uid = self._common.authenticate(
                    self.config["db"],
                    self.config["username"],
                    self.config["password"],
                    {}
                )
            
            if not self._models and self._uid:
                self._models = xmlrpc.client.ServerProxy(f'{self.config["url"]}/xmlrpc/2/object')
            
            return self._uid is not None
        except Exception as e:
            print(f"Error conectando con Odoo: {e}")
            return False
    
    def _cleanup_connection(self):
        """Limpia las conexiones y libera memoria"""
        if self._common:
            del self._common
            self._common = None
        if self._models:
            del self._models
            self._models = None
        gc.collect()
    
    def _execute_kw(self, model: str, method: str, args: list, kwargs: dict = None) -> Any:
        """Ejecuta una llamada a Odoo"""
        if not self._get_connection():
            return None
        
        try:
            if kwargs is None:
                kwargs = {}
            return self._models.execute_kw(
                self.config["db"],
                self._uid,
                self.config["password"],
                model,
                method,
                args,
                kwargs
            )
        except Exception as e:
            print(f"Error ejecutando {method} en {model}: {e}")
            return None
    
    def get_products(self) -> List[Product]:
        """Obtiene productos desde Odoo"""
        try:
            # Buscar productos
            product_ids = self._execute_kw('product.template', 'search', [[]])
            
            if not product_ids:
                return self._get_fallback_products()
            
            # Obtener datos de productos
            odoo_products = self._execute_kw(
                'product.template', 
                'read', 
                [product_ids],
                {'fields': ['id', 'name', 'default_code', 'categ_id', 'list_price', 'qty_available']}
            )
            
            if not odoo_products:
                return self._get_fallback_products()
            
            # Transformar a formato esperado
            transformed_products = []
            for p in odoo_products:
                category_name = self._get_category_name(p.get('categ_id'))
                
                transformed_products.append(Product(
                    id=p['id'],
                    name=p['name'],
                    code=p.get('default_code', '') or f"PROD-{p['id']}",
                    category=category_name,
                    price=p.get('list_price', 0.0),
                    stock=int(p.get('qty_available', 0)),
                    image_url=f"https://example.com/images/product_{p['id']}.jpg"
                ))
            
            return transformed_products
            
        except Exception as e:
            print(f"Error obteniendo productos: {e}")
            return self._get_fallback_products()
        finally:
            self._cleanup_connection()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto específico por ID"""
        try:
            odoo_product = self._execute_kw(
                'product.template',
                'read',
                [[product_id]],
                {'fields': ['id', 'name', 'default_code', 'categ_id', 'list_price', 'qty_available']}
            )
            
            if not odoo_product:
                return self._get_fallback_product_by_id(product_id)
            
            p = odoo_product[0]
            category_name = self._get_category_name(p.get('categ_id'))
            
            return Product(
                id=p['id'],
                name=p['name'],
                code=p.get('default_code', '') or f"PROD-{p['id']}",
                category=category_name,
                price=p.get('list_price', 0.0),
                stock=int(p.get('qty_available', 0)),
                image_url=f"https://example.com/images/product_{p['id']}.jpg"
            )
            
        except Exception as e:
            print(f"Error obteniendo producto {product_id}: {e}")
            return self._get_fallback_product_by_id(product_id)
        finally:
            self._cleanup_connection()
    
    def get_providers(self) -> List[Provider]:
        """Obtiene proveedores desde Odoo"""
        try:
            # Buscar proveedores (partners que son suppliers)
            provider_ids = self._execute_kw(
                'res.partner',
                'search',
                [['&', ('is_company', '=', True), ('supplier_rank', '>', 0)]]
            )
            
            if not provider_ids:
                return self._get_fallback_providers()
            
            # Obtener datos de proveedores
            odoo_providers = self._execute_kw(
                'res.partner',
                'read',
                [provider_ids],
                {'fields': ['id', 'name', 'email', 'phone', 'city', 'country_id']}
            )
            
            if not odoo_providers:
                return self._get_fallback_providers()
            
            # Transformar a formato esperado
            transformed_providers = []
            for p in odoo_providers:
                transformed_providers.append(Provider(
                    id=p['id'],
                    name=p['name'],
                    tax_calculation_method="excluded",
                    discount_type="percentage",
                    payment_term="30_days",
                    incentive_rules="Margen por defecto: 30.0%",
                    status="active"
                ))
            
            return transformed_providers
            
        except Exception as e:
            print(f"Error obteniendo proveedores: {e}")
            return self._get_fallback_providers()
        finally:
            self._cleanup_connection()

    def create_product(self, product_data: ProductCreate) -> Optional[Product]:
        """Crea un nuevo producto en Odoo."""
        try:
            print("ODOO_SERVICE: Iniciando create_product")
            if not self._get_connection():
                print("ODOO_SERVICE: Error de conexión inicial a Odoo")
                return None

            # Buscar o crear la categoría del producto
            category_name = product_data.category
            print(f"ODOO_SERVICE: Buscando categoría '{category_name}'")
            category_ids = self._execute_kw('product.category', 'search', [[('name', '=', category_name)]])
            print(f"ODOO_SERVICE: Resultado búsqueda categoría: {category_ids}")
            if not category_ids:
                # Crear la categoría si no existe
                print(f"ODOO_SERVICE: Categoría '{category_name}' no encontrada, creando...")
                new_category_id = self._execute_kw('product.category', 'create', [{'name': category_name}])
                print(f"ODOO_SERVICE: Resultado creación categoría: {new_category_id}")
                if not new_category_id:
                    print(f"Error creando categoría '{category_name}' en Odoo.")
                    return None
                category_id = new_category_id
            else:
                category_id = category_ids[0]

            # Preparar datos para Odoo
            odoo_product_values = {
                'name': product_data.name,
                'default_code': product_data.code,
                'list_price': product_data.price,
                'standard_price': product_data.price, # Coste, se puede ajustar
                'categ_id': category_id,
                'type': 'product',  # 'consu' para consumible, 'service' para servicio
                'qty_available': product_data.stock, # Esto normalmente se maneja con movimientos de stock
                'sale_ok': True,
                'purchase_ok': True,
                # 'image_1920': product_data.image_url, # Si tienes la imagen en base64
            }

            # Crear el producto en Odoo
            print(f"ODOO_SERVICE: Creando producto en Odoo con valores: {odoo_product_values}")
            product_id = self._execute_kw('product.template', 'create', [odoo_product_values])
            print(f"ODOO_SERVICE: Resultado creación producto (ID): {product_id}")
            if not product_id:
                print(f"Error creando producto '{product_data.name}' en Odoo.")
                return None

            # Leer el producto creado para devolverlo
            print(f"ODOO_SERVICE: Leyendo producto creado con ID: {product_id}")
            created_product_data = self._execute_kw(
                'product.template',
                'read',
                [[product_id]],
                {'fields': ['id', 'name', 'default_code', 'categ_id', 'list_price', 'qty_available']}
            )
            if not created_product_data:
                print(f"ODOO_SERVICE: Error leyendo producto creado con ID: {product_id}")
                return None
            print(f"ODOO_SERVICE: Datos producto leído: {created_product_data}")
            
            p = created_product_data[0]
            # Obtener el nombre de la categoría del producto creado
            created_category_name = self._get_category_name(p.get('categ_id'))

            return Product(
                id=p['id'],
                name=p['name'],
                code=p.get('default_code', '') or f"PROD-{p['id']}",
                category=created_category_name,
                price=p.get('list_price', 0.0),
                stock=int(p.get('qty_available', 0)), # qty_available en product.template puede no ser lo mismo que stock real
                image_url=f"/web/image/product.template/{p['id']}/image_1920/" if p.get('image_1920') else None,
                is_active=True # Asumimos que si se crea, está activo
            )

        except Exception as e:
            print(f"ODOO_SERVICE: Excepción en create_product: {e}")
            return None
        finally:
            print("ODOO_SERVICE: Finalizando create_product y limpiando conexión")
            self._cleanup_connection()
    
    def _get_category_name(self, categ_id) -> str:
        """Obtiene el nombre de una categoría"""
        if not categ_id:
            return "Sin categoría"
        
        try:
            category = self._execute_kw(
                'product.category',
                'read',
                [categ_id[0]],
                {'fields': ['name']}
            )
            return category[0]['name'] if category else "Sin categoría"
        except:
            return "Sin categoría"
    
    def _get_fallback_products(self) -> List[Product]:
        """Datos de productos de respaldo"""
        return [
            Product(
                id=1,
                name="Refrigerador Samsung RT38K5982BS",
                code="REF-SAM-001",
                category="Refrigeradores",
                price=899.99,
                stock=12,
                image_url="https://example.com/images/refrigerador.jpg"
            ),
            Product(
                id=2,
                name="Lavadora LG F4WV5012S0W",
                code="LAV-LG-002",
                category="Lavadoras",
                price=649.99,
                stock=8,
                image_url="https://example.com/images/lavadora.jpg"
            ),
            Product(
                id=3,
                name="Televisor Sony KD-55X80J",
                code="TV-SONY-003",
                category="Televisores",
                price=799.99,
                stock=5,
                image_url="https://example.com/images/televisor.jpg"
            )
        ]
    
    def _get_fallback_product_by_id(self, product_id: int) -> Optional[Product]:
        """Producto de respaldo por ID"""
        fallback_products = self._get_fallback_products()
        for product in fallback_products:
            if product.id == product_id:
                return product
        return None
    
    def _get_fallback_providers(self) -> List[Provider]:
        """Datos de proveedores de respaldo"""
        return [
            Provider(
                id=1,
                name="MIELECTRO",
                tax_calculation_method="excluded",
                discount_type="percentage",
                payment_term="30_days",
                incentive_rules="Margen por defecto: 30.0%",
                status="active"
            ),
            Provider(
                id=2,
                name="BECKEN",
                tax_calculation_method="excluded",
                discount_type="percentage",
                payment_term="30_days",
                incentive_rules="Margen por defecto: 30.0%",
                status="active"
            )
        ]

# Instancia del servicio
odoo_service = OdooService()
