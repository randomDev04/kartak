from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Item as ItemModel


router = APIRouter(prefix="/items", tags=["items"])

class Item(BaseModel):
    name:str
    price:float
    in_stock:bool = True

@router.post("")
def post_item(item:Item, db:Session=Depends(get_db)):
    db_item = ItemModel(name=item.name, price=item.price, in_stock=item.in_stock)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"item":db_item, "message":"Item created successfully."}

@router.get("/{item_id}")
def get_item(item_id:int, db:Session=Depends(get_db)):
    item = db.get(ItemModel, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item, "message": "Item retrieved successfully."}  

