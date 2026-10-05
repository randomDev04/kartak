from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine
import app.models
from app.routes import blogs

app.models.Base.metadata.create_all(bind=engine)

appRouter = FastAPI(title="Blog API")
appRouter.include_router(blogs.router)

# Home route
@appRouter.get("/")
def read_root():
    return {"message": "Welcome to the Blog API!"}