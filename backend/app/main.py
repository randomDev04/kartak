from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Kartak API")

class Item(BaseModel):
    name:str
    price:float
    in_stock:bool = True

@app.post("/items")
def post_item(item:Item):
    return {"item":item, "message":"Item created successfully."}

@app.get("/items/{item_id}")
def get_item(item_id:int):
    return {"item_id": item_id, "message": "Item retrieved successfully."}  

@app.get("/search")
def search_items(query:str | None = None):
    if(query):
        return {"query":query,"message":"Search results for the query."}
    else:
        return {"query":query,"message":"No query provided."}