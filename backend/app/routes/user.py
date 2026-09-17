from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from jose import JWTError, jwt
from app.models import User as UserModel
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/users", tags=["users"])

SECRET_KEY = "myscretkey"

ALGORITHM = "HS256"

# to check the requested data validation
class User(BaseModel):
    username:str
    email:str
    password:str

# Create Token
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp":expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

# Login Api
@router.post("/login")
def login(user:User):
    if user.username != "admin" or user.password != "12345":
        raise HTTPException(status_code=401, detail = "Invalid username or password")

    token = create_access_token({"sub":user.username})

    return {
        "access_token":token,
        "token_type":"bearer"
    }

#Token verification
def verify_token(token:str = Header(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


#protected route
@router.get("/protected")
def protected_route(payload:dict = Depends(verify_token)):
    return {"message":"You have access to this protected route", "user":payload["sub"]}