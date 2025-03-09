from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from source.models.user import User
from source.models.cart import Cart
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token
from source.schemas.user_schema import UserLoginSchema, UserSchema

def create_user_service(user: UserSchema, db: Session):
    try:
        query = db.query(User).filter(User.email == user.email).first()
        if query:
            return False,"email"
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if user exist or not")
    
    try:
        query = db.query(User).filter(User.phone == user.phone).first()
        if query:
            return False,"phone number"
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if user exist or not")
    
    try:
        new_user = User(name=user.name, email=user.email, password=hash_password(user.password), phone = user.phone)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True, "good"
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating user")


def login_user_service(user: UserLoginSchema, db: Session):
    try:
        user_data = db.query(User).filter(User.email == user.email).first()
        if user_data is None:
            return None
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if user exist or not")
    try:
        user_data = db.query(User).filter(User.email == user.email).first()
        if user_data and verify_password(user.password,user_data.password):# verify_password(user.password, user_data.password):
            access_token = create_access_token(user.email, "user")
            return access_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating user token")
    

# Add to cart
def add_to_cart(id: int,quantity:int, product_price, user_id: int, db: Session):
    print("3")
    try:
        cart = Cart(
            user_id = user_id,
            product_id = id,
            quantity = quantity,
            amount = product_price 
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error while adding cart {str(e)}")
    
def show_cart(user: User, db: Session):
    query = db.query(Cart).filter(user.id == Cart.user_id).all()
    return query
