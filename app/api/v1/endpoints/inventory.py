from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.models import Inventory, InventoryHistory, Product, ChangeType
from app.schemas.schemas import (
    InventoryCreate,
    Inventory as InventorySchema,
    InventoryHistory as InventoryHistorySchema,
    InventoryAlert
)

router = APIRouter()

@router.post("/", response_model=InventorySchema)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == inventory.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_inventory = db.query(Inventory).filter(Inventory.product_id == inventory.product_id).first()
    if existing_inventory:
        raise HTTPException(status_code=400, detail="Inventory already exists for this product")
    
    db_inventory = Inventory(**inventory.model_dump())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.get("/", response_model=List[InventorySchema])
def get_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).offset(skip).limit(limit).all()
    return inventory

@router.get("/alerts", response_model=List[InventoryAlert])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    alerts = db.query(
        Inventory, Product
    ).join(
        Product, Inventory.product_id == Product.id
    ).filter(
        Inventory.quantity <= Inventory.low_stock_threshold
    ).all()
    
    return [
        InventoryAlert(
            product_id=alert[0].product_id,
            product_name=alert[1].name,
            current_quantity=alert[0].quantity,
            low_stock_threshold=alert[0].low_stock_threshold,
            status="LOW_STOCK"
        )
        for alert in alerts
    ]

@router.put("/{inventory_id}", response_model=InventorySchema)
def update_inventory(
    inventory_id: int,
    new_quantity: int,
    change_type: ChangeType,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    history = InventoryHistory(
        inventory_id=inventory_id,
        previous_quantity=inventory.quantity,
        new_quantity=new_quantity,
        change_type=change_type
    )
    db.add(history)
    
    inventory.quantity = new_quantity
    inventory.last_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(inventory)
    return inventory

@router.get("/history/{inventory_id}", response_model=List[InventoryHistorySchema])
def get_inventory_history(
    inventory_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    history = db.query(InventoryHistory).filter(
        InventoryHistory.inventory_id == inventory_id
    ).order_by(
        InventoryHistory.timestamp.desc()
    ).offset(skip).limit(limit).all()
    
    return history 