from fastapi import HTTPException, status, Depends, Request
import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.seller import Seller
from source.models.admin import Admin
from source.models.user import User
from datetime import datetime, timedelta

SECRET_KEY = "5446690435543456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(email: str, role: str):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    payload = {
        "email": email,
        "role": role,
        # "exp": expire  # Adding expiration time
    }
    try:
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token creation error: {str(e)}")
    

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email = payload.get("email")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Missing required fields",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

#admin role
async def get_current_admin(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    email = payload.get("email")
    role = payload.get("role")
    
    if role != "admin":
        raise credentials_exception
    
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin is None:
        raise credentials_exception
    
    return {
        "id":admin.id,
        "email":admin.email
    }


#seller role
async def get_current_seller(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    email = payload.get("email")
    role = payload.get("role")
    
    if role != "seller":
        raise credentials_exception
    
    seller = db.query(Seller).filter(Seller.email == email).first()
    if seller is None:
        raise credentials_exception
        
    return seller
    return {
        "id":seller.id,
        "name":seller.name,
        "email":seller.email
    }


#user role
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
)->dict:
    token = request.cookies.get("access_token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    email = payload.get("email")
    role = payload.get("role")
 
    if role != "user":
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
    return {
        "id":user.id,
        "name":user.name,
        "email":user.email
    }   