
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.database import get_db
from app.models import Blog as BlogModel


router = APIRouter(prefix="/blogs", tags=["blogs"])

# Create blog endpoint
@router.post("/", response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate, db:Session=Depends(get_db)):
    new_blog = BlogModel(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
