from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.utils.token import get_current_admin
from source.schemas.admin_schema import AdminSchema
from source.modules.admin.admin_controller import create_admin_controller, login_admin_controller

router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("admin_gateway/signup.html", {"request": request})


@router.post("/register")
async def create_admin(request: Request, admin: AdminSchema = Form(...), db: Session = Depends(get_db)):
    return create_admin_controller(request, admin, db)


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("admin_gateway/login.html", {"request": request})


@router.post("/login")
async def login_admin(request: Request, admin: AdminSchema = Form(...), db: Session = Depends(get_db)):
    return login_admin_controller(request, admin, db)


# Admin dashboard (protected)
@router.get("/admin_dashboard")
async def admin_dashboard(request: Request,email: dict = Depends(get_current_admin)):
    return templates.TemplateResponse("admin_dashboard.html",{"request": request, "email": email["email"]})