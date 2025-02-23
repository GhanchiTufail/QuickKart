from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from source.models.seller import Seller
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token
from source.schemas.seller_schema import SellerLoginSchema, SellerSchema
from source.schemas.product_schema import ProductSchema

def create_seller_service(seller: SellerSchema, db: Session):
    try:
        query = db.query(Seller).filter(Seller.email == seller.email).first()
        if query:
            return {"error":"Email"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if seller exist or not")
    try:
        query = db.query(Seller).filter(Seller.store_name == seller.store).first()
        if query:
            return {"error":"store"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if seller exist or not")
    try:
        query = db.query(Seller).filter(Seller.phone == seller.phone).first()
        if query:
            return {"error":"phone"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if seller exist or not")
    try:
        new_seller = Seller(name=seller.name, email=seller.email, password=hash_password(seller.password), store_name = seller.store, phone = seller.phone, category = seller.category)
        db.add(new_seller)
        db.commit()
        db.refresh(new_seller)
        return True
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in creating seller str{e}")


def login_seller_service(seller: SellerLoginSchema, db: Session):
    try:
        seller_data = db.query(Seller).filter(Seller.email == seller.email).first()
        if seller_data and verify_password(seller.password, seller_data.password):
            access_token = create_access_token(seller.email, "seller")
            return access_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating seller token")