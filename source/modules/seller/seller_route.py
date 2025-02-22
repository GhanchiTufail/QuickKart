from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.schemas.seller_schema import SellerLoginSchema, SellerSchema
from source.config.database import get_db
from source.models.seller import Seller
from source.utils.token import create_access_token, get_current_seller

router = APIRouter(prefix="/seller", tags=["Seller"])
templates = Jinja2Templates(directory="templates")

# Register Page
@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("seller/signup.html", {"request": request})

# Register Backend
@router.post("/register")
async def register_user(
    request: Request,
    seller: SellerSchema = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(Seller).filter(Seller.email == seller.email).first()
    if existing_user:
        return templates.TemplateResponse(
            "seller/signup.html",
            {"request": request, "message": "Email already exists"}
        )
    new_seller = Seller(name=seller.name, email=seller.email, phone=seller.phone,store_name=seller.store, password=seller.password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return RedirectResponse(url="/seller/login", status_code=302)

# Login Page
@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("seller/login.html", {"request": request})

# Login Backend
@router.post("/login")
async def login_user(
    request: Request,
    seller: SellerLoginSchema = Form(...),
    db: Session = Depends(get_db)
):
    seller_data = db.query(Seller).filter(Seller.email == seller.email).first()
    if seller_data and seller_data.password == seller.password:
        access_token = create_access_token(seller.email, "seller")
        response = RedirectResponse(url="/seller/home", status_code=302)
        response.set_cookie(key="access_token", value=access_token)
        return response
    else:
        return templates.TemplateResponse(
            "seller/login.html",
            {"request": request, "message": "Incorrect email or password"}
        )

# Seller Dashboard
@router.get("/home")
async def user_dashboard(request: Request):
    return templates.TemplateResponse("seller/home.html", {"request": request})