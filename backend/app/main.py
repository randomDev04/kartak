
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.database import engine, Base
from app.routes import items, user, uploadFile as upload

# Allowed origins for CORS
origins = [
    "http://localhost:5173",
    "https://localhost:5173"
]


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kartak API")
app.include_router(items.router)
app.include_router(user.router)
app.include_router(upload.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allow requests from these origins FE
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)


@app.get("/health")
async def health_check():
    await asyncio.sleep(3)
    return {"status": "healthy", "message": "CORS API is running smoothly."}