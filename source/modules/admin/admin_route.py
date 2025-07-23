from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.product import Product
from source.models.seller import Seller
from source.models.user import User
from source.models.order_items import OrderItem
from source.utils.token import get_current_admin
from source.schemas.admin_schema import AdminSchema, SellerPagination, UserPagination, ProductPagination
from source.modules.admin.admin_controller import create_admin_controller, login_admin_controller, seller_list_controller, user_list_service, seller_list_service, product_list_service, seller_ban_service


router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("admin/signup.html", {"request": request})


@router.post("/register")
async def create_admin(request: Request, admin: AdminSchema = Form(...), db: Session = Depends(get_db)):
    return create_admin_controller(request, admin, db)


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@router.post("/login")
async def login_admin(request: Request, admin: AdminSchema = Form(...), db: Session = Depends(get_db)):
    return login_admin_controller(request, admin, db)


@router.get("/admin_dashboard")
async def admin_dashboard(request: Request,email: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    product = db.query(Product).count()
    seller = db.query(Seller).count()
    user = db.query(User).count()
    order = db.query(OrderItem).count()
    return templates.TemplateResponse("admin/admin_dashboard.html",{"request": request, "email": email["email"], "product":product, "seller":seller, "user":user, "order":order})


@router.get("/sellers")
def seller_list(request: Request,seller: SellerPagination = Depends() ,db: Session = Depends(get_db)):
    sellers,page,total_seller,total_pages = seller_list_service(seller,db)
    return templates.TemplateResponse("admin/seller_list.html", {"request": request, "sellers": sellers, "page":page, "total_seller":total_seller, "total_pages":total_pages})


@router.get("/users")
async def get_users(request: Request,param: UserPagination = Depends(), db: Session = Depends(get_db)):
    users, page, total_pages, total_users = user_list_service(param,db)
    return templates.TemplateResponse("admin/user_list.html", {"request": request, "users": users, "page":page, "total_pages":total_pages, "total_users":total_users})


@router.get("/products")
async def get_products(request: Request,param: ProductPagination = Depends(), db: Session = Depends(get_db)):
    products = product_list_service(param,db)
    return templates.TemplateResponse("admin/product_list.html", {"request": request, "products": products["query"], "seller_id":products["Seller id"], "page":products["page"], "total_pages":products["total pages"], "total_products":products["total product"], "status":products["status"]})


@router.post("/seller/ban/{seller_id}")
async def ban_seller(request: Request, seller_id: int, db: Session = Depends(get_db)):
    seller_ban_service(seller_id, db)
    return RedirectResponse(url="/admin/sellers", status_code=303)


