from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/items", tags=["items"])

class Item(BaseModel):
    name:str
    price:float
    in_stock:bool = True

@router.post("")
def post_item(item:Item):
    return {"item":item, "message":"Item created successfully."}

@router.get("/{item_id}")
def get_item(item_id:int):
    return {"item_id": item_id, "message": "Item retrieved successfully."}  

