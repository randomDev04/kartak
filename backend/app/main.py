from fastapi import FastAPI
from app.routes import items

app = FastAPI(title="Kartak API")

app.include_router(items.router)

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/search")
def search_items(query:str | None = None):
    if(query):
        return {"query":query,"message":"Search results for the query."}
    else:
        return {"query":query,"message":"No query provided."}