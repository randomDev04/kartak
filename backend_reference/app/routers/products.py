from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Product
from app.schemas import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
