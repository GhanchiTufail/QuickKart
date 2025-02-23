from fastapi import Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.admin import Admin
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token, get_current_admin
from source.schemas.admin_schema import AdminSchema
from source.modules.admin.admin_service import create_admin_service, login_admin_service

templates = Jinja2Templates(directory="templates")

def create_admin_controller(request: Request, admin: AdminSchema, db: Session):
    query = create_admin_service(request,admin,db)
    if query is False:
        return templates.TemplateResponse(
            "admin_gateway/signup.html",
            {"request": request, "message": "Email already exists"},
        )
    if query is True:
        return RedirectResponse(url="/admin/login", status_code=303)


def login_admin_controller(request: Request, admin: AdminSchema, db: Session):
    access_token = login_admin_service(admin, db)
    if access_token:
        response = RedirectResponse(url="/admin/admin_dashboard", status_code=303)
        response.set_cookie(key="access_token", value=access_token)
        return response
    else:
        return templates.TemplateResponse(
            "admin_gateway/login.html",
            {"request": request, "message": "Incorrect email or password"},
        )