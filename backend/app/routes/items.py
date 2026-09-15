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

# Create item endpoint
@router.post("")
def post_item(item:Item, db:Session=Depends(get_db)):
    db_item = ItemModel(name=item.name, price=item.price, in_stock=item.in_stock)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"item":db_item, "message":"Item created successfully."}

# Single item retrieval endpoint
@router.get("/{item_id}")
def get_item(item_id:int, db:Session=Depends(get_db)):
    # item = db.get(ItemModel, item_id)
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item, "message": "Item retrieved successfully."}

# Multiple items retrieval endpoint
@router.get("/")
def get_Items(db:Session=Depends(get_db)):
    todos = db.query(ItemModel).all()

    # paginate the results
    page = 1
    page_size = 10
    start = (page - 1) * page_size
    end = start + page_size
    todos = todos[start:end]

    return {
        "total":len(todos),
        "items":todos,
        "message":"Items retrieved successfully."
    }


# Update item endpoint
@router.put("/{item_id}")
def update_item(item_id:int, item:Item, db:Session=Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.price = item.price
    db_item.in_stock = item.in_stock
    db.commit()
    db.refresh(db_item)

    return {
        "item":db_item,
        "message":"Item updated successfully."
    }

# Delete item endpoint
@router.delete("/{item_id}")
def delete_item(item_id:int, db:Session=Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully."}