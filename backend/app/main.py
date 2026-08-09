from fastapi import FastAPI

from app.database import engine, Base
from app.routes import items

Base.metadata.create_all(bind=engine)

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