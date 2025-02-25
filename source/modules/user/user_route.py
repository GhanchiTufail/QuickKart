from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from source.schemas.user_schema import UserLoginSchema, UserSchema
from source.config.database import get_db
from source.utils.token import get_current_user
from source.modules.user.user_controller import login_user_controller, create_user_controller
from source.models.user import User

router = APIRouter(prefix="/user", tags=["User"])
templates = Jinja2Templates(directory="templates")

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("user/user_gateway/signup.html", {"request": request})


@router.post("/register")
async def create_seller(request: Request, user: UserSchema = Form(...), db: Session = Depends(get_db)):
    return create_user_controller(request, user, db)


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("user/user_gateway/login.html", {"request": request})


@router.post("/login")
async def login_seller(request: Request, user: UserLoginSchema = Form(...), db: Session = Depends(get_db)):
    return login_user_controller(request, user, db)


# user dashboard (protected)
@router.get("/home")
async def admin_dashboard(request: Request,user: User  = Depends(get_current_user)):
    return templates.TemplateResponse("user/home.html",{"request": request, "data": user})