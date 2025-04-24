from fastapi import Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import and_
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.user import User
from source.models.product import Product
from source.models.cart import Cart
from source.schemas.user_schema import UserLoginSchema, UserSchema
from source.modules.user.user_service import login_user_service, create_user_service, add_to_cart, show_cart, order_service, account_service, cart_remove_service, single_product_service, rent_item_service, get_order_service, rental_list_service, notification_list_service, search_for_product

templates = Jinja2Templates(directory="templates")

def create_user_controller(request: Request, user: UserSchema, db: Session):
    query,message = create_user_service(user,db)
    if query is False:
        return templates.TemplateResponse(
            "user/user_gateway/signup.html",
            {"request": request, "message": f"{message} already exists"},
        )
    if query is True:
        return RedirectResponse(url="/user/login", status_code=303)

def login_user_controller(request: Request, user: UserLoginSchema, db: Session):
    access_token = login_user_service(user, db)
    if access_token:
        response = RedirectResponse(url="/user/home", status_code=303)
        response.set_cookie(key="access_token", value=access_token)
        return response
    elif access_token is None:
        return templates.TemplateResponse(
            "user/user_gateway/login.html",
            {"request": request, "message": "Incorrect email or password"},
        )
    
# def product_list(request: Request, db: Session):
#     pass

def add_to_cart_controller(request: Request, product_id: int, user_id: int, db: Session, quantity: int = 1):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product.stock < 1:
        return 0
    query = db.query(Cart).filter(and_(Cart.product_id == product_id , Cart.user_id == Cart.user_id)).first()
    # print(query.id, query.quantity)
    if query:
        query.quantity+=quantity
    else:
        query = db.query(Product).filter(product_id == Product.id).first()
        product_price = query.price * quantity
        add_to_cart(product_id,quantity,product_price,user_id,db)

def show_cart_controller(request : Request, user: User, db: Session):
    query = show_cart(user, db)
    
def order_controller(request: Request, id: int, db: Session):
    order_service(id,db)

def account_controller(request: Request, id: int, db: Session):
    try:
        return account_service(id,db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in account controller {str(e)}")
    
def cart_remove_controller(request: Request, id: int, db: Session):
    try:
        cart_remove_service(id,db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while removing cart item {str(e)}")
    

def single_product_controller(request: Request, id: int, db: Session):
    try:
        return single_product_service(id,db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in single product controller : {str(e)}")
    
def order_list_controller(request: Request, id: int, db: Session):
    try:
        print(1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in order list controller {str(e)}")
    

def rent_product_controller(request: Request, id: int, month: int, user: User, db: Session):
    try:
        rent_item_service(id,month,user,db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in rent product controller {str(e)}")
    

def get_order_controller(request: Request, user: User, db: Session):
    try:
        products = get_order_service(user, db)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in order controller {str(e)}")
    

def rental_list_controller(request: Request, user: User , db: Session):
    try:
        return rental_list_service(user,db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in rental list controller {str(e)}")
    

def notification_list_controller(request: Request, user: User, db: Session):
    try:
        return notification_list_service(user, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in notification list controller {str(e)}")
    

def search_product_controller(request: Request, search: str, db: Session):
    try:
        return search_for_product(search, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in notification list controller {str(e)}")