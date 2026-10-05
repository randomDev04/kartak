
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.database import get_db
from app.models import Blog as BlogModel
from app.routes.auth import verify_access_token


router = APIRouter(prefix="/blogs", tags=["blogs"])

# Create blog endpoint (PROTECTED)
@router.post("/", response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate, db:Session=Depends(get_db), user:dict = Depends(verify_access_token)):
    new_blog = BlogModel(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get all blogs endpoint
@router.get("/", response_model=list[schemas.BlogResponse])
def get_blogs(db:Session=Depends(get_db)):
    return db.query(BlogModel).all()

# Get a single blog by ID endpoint
@router.get("/{blog_id}", response_model=schemas.BlogResponse)
def get_blog(blog_id:int, db:Session=Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# Update a blog by ID endpoint
@router.put("/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(blog_id:int, blog:schemas.BlogCreate, db:Session=Depends(get_db)):
    existing_blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()

    if not existing_blog:
        raise HTTPException(status_code=404, details="Blog not found")

    existing_blog.title = blog.title
    existing_blog.content = blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog

# Delete a blog by ID endpoint
@router.delete("/{blog_id}")
def delete_blog(blog_id:int, db:Session=Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return {
        "message": "Blog deleted successfully",
    }
