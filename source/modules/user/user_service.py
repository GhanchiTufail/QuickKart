from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from source.models.user import User
from source.models.cart import Cart
from source.models.order import Order
from source.models.product import Product
from source.models.order_items import OrderItem
from source.models.rental_items import Rental
from source.models.order import Order
from source.models.notification import Notification
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token
from source.schemas.user_schema import UserLoginSchema, UserSchema
from datetime import datetime,timedelta, date
from sqlalchemy import desc
import copy

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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"error in checking if user exist or not {str(e)}")
    try:
        user_data = db.query(User).filter(User.email == user.email).first()
        if user_data and verify_password(user.password,user_data.password):# verify_password(user.password, user_data.password):
            access_token = create_access_token(user.email, "user")
            return access_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating user token")
    

# Add to cart
def add_to_cart(id: int,quantity:int, product_price, user_id: int, db: Session):
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


def order_service(id: int, db: Session):
    try:
        cart_item = db.query(Cart).filter(Cart.user_id == id).all()
    except:
        raise HTTPException("Error while getting user id from cart")
    
    price = 0
    for i in cart_item:
        userId = i.user_id
        price += i.amount
        product = db.query(Product).filter(Product.id == i.product_id).first()
        product.stock -= 1
        
        user = db.query(User).filter(User.id == id).first()
        add_notification = Notification(
            user_id = id,
            seller_id = product.seller_id,
            product_id = product.id,
            user_message = f"Order for {product.name} is placed successfully",
            seller_message = f"Order from {user.name} for {product.name} is placed",
            notification_type = "order"
        )
        db.add(add_notification)
        db.commit()
        db.refresh(add_notification)

    add_order = Order(
    user_id = userId,
    total_price = price,
    )
    db.add(add_order)
    db.commit()
    db.refresh(add_order)

    
    for i in cart_item:
        add_order_item = OrderItem(
        order_id = add_order.id,
        product_id = i.product_id,
        quantity = i.quantity,
        price = i.amount
        )
        db.add(add_order_item)
        db.commit()
        db.refresh(add_order_item)

        

    db.query(Cart).filter(Cart.user_id == id).delete()
    db.commit()

def account_service(id: int ,db: Session):
    query = db.query(User).filter(User.id == id).first()
    return query
    return {
        "id":query.id,
        "name":query.name,
        "email":query.email,
        "phone":query.phone
    }


def cart_remove_service(id: int, db: Session):
    db.query(Cart).filter(Cart.id == id).delete()
    db.commit()


def single_product_service(id: int, db: Session):
    product = db.query(Product).filter(Product.id == id).first()
    return product


def rent_item_service(id: int,month: int,user: User, db: Session):
    product = db.query(Product).filter(Product.id == id).first()
    rentel = Rental(
        user_id = user.id,
        product_id = id,
        start_date = func.now(),
        end_date = func.now() + timedelta(days=(month * 30)),
        total_price = product.daily_rate * month,
        status = "active",
        is_history = False
    )
    db.add(rentel)
    db.commit()
    db.refresh(rentel)


def get_order_service(user: User, db: Session):
    products = db.query(Product, OrderItem.quantity, Order.status, Order.created_at)\
                 .join(OrderItem, Product.id == OrderItem.product_id)\
                 .join(Order, OrderItem.order_id == Order.id)\
                 .filter(Order.user_id == user.id).all()    

    order_list = []

    for product, quantity, status, created_at in products:
        order_list.append({
            "name": product.name,
            "image": product.image,
            "price": product.price,
            "status": status,  # Status from Order
            "quantity": quantity,
            "created_at": created_at.date()  # Order creation time
        }) 
    return order_list
    

def rental_list_service(user: User, db: Session):
    rentals = db.query(Product, Rental.start_date, Rental.end_date, Rental.total_price, Rental.status, Rental.created_at)\
                .join(Rental, Product.id == Rental.product_id)\
                .filter(Rental.user_id == user.id).all()    

    rental_list = []
    

    for product, start_date, end_date, total_price, status, created_at in rentals:
        rental_list.append({
            "name": product.name,
            "image": product.image,
            "rent_pm": int(product.daily_rate),
            "price": product.price,
            "start_date": start_date.date(),
            "end_date": end_date.date() if end_date else None,  # Handle case where end_date is None
            "total_price": total_price,
            "status": status,
            "created_at": created_at.date()
        }) 
    return rental_list


def notification_list_service(user: User, db: Session):
    notification = db.query(Notification).filter(Notification.user_id == user.id).order_by(desc(Notification.created_at)).all()

    NotificationResponse = []
    for i in notification:
        NotificationResponse.append({
                "type":i.notification_type,
                "Time": i.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "user":i.user_message,
                "read":i.is_read
            })

    for i in notification:
        i.is_read = True
        db.commit()
        db.refresh(i)

    return NotificationResponse


def search_for_product(search: str, db: Session):
    product = db.query(Product).filter(Product.name.ilike(f"%{search}%")).all()
    return product