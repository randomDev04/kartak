
from fastapi import FastAPI
import asyncio

from app.database import engine, Base
from app.routes import items, user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kartak API")
app.include_router(items.router)
app.include_router(user.router)

@app.get("/health")
async def health_check():
    await asyncio.sleep(3)
    return {"status": "healthy"}