from fastapi import Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.seller import Seller
from source.schemas.seller_schema import SellerLoginSchema, SellerSchema
from source.modules.seller.seller_service import create_seller_service, login_seller_service
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
    if access_token:
        response = RedirectResponse(url="/seller/home", status_code=303)
        response.set_cookie(key="access_token", value=access_token)
        return response
    else:
        return templates.TemplateResponse(
            "seller/login.html",
            {"request": request, "message": "Incorrect email or password"},
        )