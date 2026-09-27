from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.models import User as UserModel
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/users", tags=["users"])

# JST CONFIGURATION
SECRET_KEY = "myscretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# PAssword hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dummy user data for testing purposes
fake_user = {
    "username": "admin",
    "email": "admin@example.com",
    "hashed_password": pwd_context.hash("12345")
}

# Hash password
def hash_password(password:str):
    return pwd_context.hash(password)

# verify password
def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

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
def login(form_data:OAuth2PasswordRequestForm=Depends()):

    print(form_data.username)

    if form_data.username != fake_user["username"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(
        form_data.password,
        fake_user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    access_token = create_access_token({"sub":form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

#Token verification
def verify_token(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#protected route
@router.get("/protected")
def protected_route(payload:dict = Depends(verify_token)):
    return {"message":"You have access to this protected route", "user":payload["sub"]}