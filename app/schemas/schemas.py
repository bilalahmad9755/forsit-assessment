from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ChangeType(str, Enum):
    ADD = "add"
    REMOVE = "remove"
    ADJUST = "adjust"

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InventoryBase(BaseModel):
    quantity: int
    low_stock_threshold: int = 10

class InventoryCreate(InventoryBase):
    product_id: int

class Inventory(InventoryBase):
    id: int
    product_id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class InventoryHistoryBase(BaseModel):
    previous_quantity: int
    new_quantity: int
    change_type: ChangeType

class InventoryHistoryCreate(InventoryHistoryBase):
    inventory_id: int

class InventoryHistory(InventoryHistoryBase):
    id: int
    inventory_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    total_amount: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    sale_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class RevenueAnalysis(BaseModel):
    period: str
    total_revenue: float
    total_sales: int
    average_order_value: float

class RevenueComparison(BaseModel):
    period1: RevenueAnalysis
    period2: RevenueAnalysis
    percentage_change: float

class InventoryAlert(BaseModel):
    product_id: int
    product_name: str
    current_quantity: int
    low_stock_threshold: int
    status: str 