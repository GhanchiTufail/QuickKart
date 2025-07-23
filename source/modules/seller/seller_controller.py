from fastapi import Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.seller import Seller
from source.schemas.seller_schema import SellerLoginSchema, SellerSchema
from source.modules.seller.seller_service import create_seller_service, login_seller_service, product_delete_service, product_detail_service, seller_order_service, order_delivered_service
from source.utils.categories import CategoryEnum

templates = Jinja2Templates(directory="templates")

def create_seller_controller(request: Request, seller: SellerSchema, db: Session):
    query = create_seller_service(seller,db)
    if query:
        return templates.TemplateResponse(
            "seller/signup.html",
            {"request": request, "message": f"{query["error"]} already exists","categories":list(CategoryEnum)},
        )
    return RedirectResponse(url="/seller/login", status_code=303)


def login_seller_controller(request: Request, seller: SellerLoginSchema, db: Session):
    access_token = login_seller_service(seller, db)
    if access_token is None:
        return templates.TemplateResponse("seller/seller_ban.html",{"request":request})
    if access_token:
        response = RedirectResponse(url="/seller/home", status_code=303)
        response.set_cookie(key="access_token", value=access_token)
        return response
    else:
        return templates.TemplateResponse(
            "seller/login.html",
            {"request": request, "message": "Incorrect email or password"},
        )


def seller_order_controller(request: Request, seller: Seller, db: Session, status: str | None = None):
    try:
        return seller_order_service(seller, db, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in seller order controller {str(e)}")
    

def product_delivered_controller(request: Request, id: int, seller: Seller, db: Session):
    try:
        return order_delivered_service(id,seller,db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in Product delivered Controller {str(e)}")