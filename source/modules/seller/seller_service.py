from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from source.models.seller import Seller
from source.models.product import Product
from source.models.order import Order
from source.models.order_items import OrderItem
from source.models.user import User
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
        new_seller = Seller(name=seller.name, email=seller.email, password=hash_password(seller.password), store_name = seller.store, phone = seller.phone, category = seller.category, rating = 0)
        db.add(new_seller)
        db.commit()
        db.refresh(new_seller)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in creating seller str{e}")


def login_seller_service(seller: SellerLoginSchema, db: Session):
    try:
        seller_data = db.query(Seller).filter(Seller.email == seller.email).first()
        if seller_data.is_banned == True:
            return None
        if seller_data and verify_password(seller.password, seller_data.password):
            access_token = create_access_token(seller.email, "seller")
            return access_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating seller token")
    

def product_delete_service(id: int, db: Session):
    query = db.query(Product).filter(Product.id == id).delete()
    db.commit()


def product_detail_service(id: int, db: Session):
    product = db.query(Product).filter(Product.id == id).first()
    return product


def seller_order_service(seller: Seller, db: Session ,status:str | None = None):
    products = db.query(
                    Product.id,
                    Product.name, 
                    Product.image, 
                    User.name.label("customer_name"), 
                    Order.id.label("order_id"), 
                    Order.created_at, 
                    Order.status,
                    OrderItem.quantity, 
                    OrderItem.price
                )\
                .join(OrderItem, OrderItem.product_id == Product.id)\
                .join(Order, Order.id == OrderItem.order_id)\
                .join(User, User.id == Order.user_id)\
                .filter(Product.seller_id == seller.id)

    # if status and status.lower() != 'all':
    #     products = products.filter(Order.status == status.capitalize())
    
    products = products.all()
    

    order_list = []
    
    for id,name, image, customer_name, order_id, created_at, status, quantity, price in products:
        order_list.append({
            "product_id": id,
            "product_name": name,
            "product_image": image,
            "customer_name": customer_name,
            "order_id": order_id,
            "order_status": status,
            "quantity": quantity,
            "price": price,
            "created_at": created_at.date()  # Extract date only
        })
    return order_list


def order_delivered_service(id: int, seller: Seller, db: Session):
    delivered = db.query(Order).filter(Order.id == id).first()

    delivered.status = "Delivered"
    
    db.commit()
    db.refresh(delivered)
    return {
        "info":delivered
    }