from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.session import Base

class ChangeType(enum.Enum):
    ADD = "add"
    REMOVE = "remove"
    ADJUST = "adjust"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(500))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    sales = relationship("Sale", back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("Product", back_populates="inventory")
    history = relationship("InventoryHistory", back_populates="inventory")

class InventoryHistory(Base):
    __tablename__ = "inventory_history"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    previous_quantity = Column(Integer)
    new_quantity = Column(Integer)
    change_type = Column(Enum(ChangeType))
    timestamp = Column(DateTime, default=datetime.utcnow)

    inventory = relationship("Inventory", back_populates="history")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    sale_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="sales") 