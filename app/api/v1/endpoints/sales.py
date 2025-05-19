from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.models import Sale, Product
from app.schemas.schemas import SaleCreate, Sale as SaleSchema, RevenueAnalysis, RevenueComparison

router = APIRouter()

@router.post("/", response_model=SaleSchema)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.get("/", response_model=List[SaleSchema])
def get_sales(
    skip: int = 0,
    limit: int = 100,
    start_date: datetime = None,
    end_date: datetime = None,
    product_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Sale)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    
    sales = query.offset(skip).limit(limit).all()
    return sales

@router.get("/revenue", response_model=RevenueAnalysis)
def get_revenue_analysis(
    period: str = "daily",
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()

    query = db.query(
        func.sum(Sale.total_amount).label("total_revenue"),
        func.count(Sale.id).label("total_sales")
    ).filter(
        Sale.sale_date.between(start_date, end_date)
    )

    result = query.first()
    
    return RevenueAnalysis(
        period=period,
        total_revenue=result.total_revenue or 0,
        total_sales=result.total_sales or 0,
        average_order_value=(result.total_revenue or 0) / (result.total_sales or 1)
    )

@router.get("/compare", response_model=RevenueComparison)
def compare_revenue(
    period1_start: datetime,
    period1_end: datetime,
    period2_start: datetime,
    period2_end: datetime,
    db: Session = Depends(get_db)
):
    def get_period_analysis(start_date, end_date):
        result = db.query(
            func.sum(Sale.total_amount).label("total_revenue"),
            func.count(Sale.id).label("total_sales")
        ).filter(
            Sale.sale_date.between(start_date, end_date)
        ).first()
        
        return RevenueAnalysis(
            period=f"{start_date.date()} to {end_date.date()}",
            total_revenue=result.total_revenue or 0,
            total_sales=result.total_sales or 0,
            average_order_value=(result.total_revenue or 0) / (result.total_sales or 1)
        )

    period1 = get_period_analysis(period1_start, period1_end)
    period2 = get_period_analysis(period2_start, period2_end)

    percentage_change = (
        ((period2.total_revenue - period1.total_revenue) / period1.total_revenue * 100)
        if period1.total_revenue > 0 else 0
    )

    return RevenueComparison(
        period1=period1,
        period2=period2,
        percentage_change=percentage_change
    )

@router.get("/by-product/{product_id}", response_model=List[SaleSchema])
def get_sales_by_product(
    product_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(Sale).filter(Sale.product_id == product_id)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    
    return query.all() 