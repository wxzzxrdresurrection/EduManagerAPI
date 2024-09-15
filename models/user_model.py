from pydantic import BaseModel
import datetime
import jwt
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from config.db import MongoConnection

SECRET_KEY = "2fd807cc35eb108c162b99c2f31ad096892ce5f444a6df26f8a4819d6e483771"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    id: str | None = None
    first_name: str
    middle_name: str
    last_name: str
    email: str
    password: str
    telephone: str
    disabled: bool = False
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    email: str

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, email: str):
    user = db.get_item_from_collection_by_key("users", "email", email)
    if user:
        return user
    return None

# Función para autenticar al usuario
def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    message = "Login successful"
    if not user:
        message = "User not found"
        return {}, message
    if not verify_password(password, user["password"]):
        message = "User not found"
        return {}, message
    return user, message

def create_access_token(data, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    to_encode["created_at"] = str(to_encode["created_at"])
    if to_encode["updated_at"]:
        to_encode["updated_at"] = str(to_encode["updated_at"])
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = MongoConnection()
    user = get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user
    

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user or current_user.disabled: 
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


