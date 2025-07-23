from fastapi import Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.admin import Admin
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token, get_current_admin
from source.schemas.admin_schema import AdminSchema, SellerPagination, UserPagination
from source.modules.admin.admin_service import create_admin_service, login_admin_service, seller_list_service, user_list_service, product_list_service, seller_ban_service
from math import ceil

templates = Jinja2Templates(directory="templates")

def create_admin_controller(request: Request, admin: AdminSchema, db: Session):
    try:
        query = create_admin_service(request,admin,db)
        if query is False:
            return templates.TemplateResponse(
                "admin/signup.html",
                {"request": request, "message": "Email already exists"},
            )
        if query is True:
            return RedirectResponse(url="/admin/login", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in create admin controller {str(e)}" )


def login_admin_controller(request: Request, admin: AdminSchema, db: Session):
    access_token = login_admin_service(admin, db)
    if access_token:
        response = RedirectResponse(url="/admin/admin_dashboard", status_code=303)
        response.set_cookie(key="access_token", value=access_token)
        return response
    else:
        return templates.TemplateResponse(
            "admin/login.html",
            {"request": request, "message": "Incorrect email or password"},
        )
    
# updated
def seller_list_controller(seller:SellerPagination,db: Session):
    query,users = seller_list_service(seller,db)
    pages = ceil(users/seller.limit)
    sellers = []
    for data in query:
        sellers.append({
            "id":str(data.id),
            "name":data.name,
            "email":data.email,
            "phone":data.phone,
            "store":data.store_name,
            "category":data.category,
            "status":str(data.is_banned)
        })
    return {
        "pages":pages,
        "users":users,
        "data":query}

def user_list_controller(user: UserPagination, db: Session):
    query = user_list_service(user, db)
    