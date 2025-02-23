from fastapi import Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.user import User
from source.schemas.user_schema import UserLoginSchema, UserSchema
from source.modules.user.user_service import login_user_service, create_user_service

templates = Jinja2Templates(directory="templates")

def create_user_controller(request: Request, user: UserSchema, db: Session):
    query = create_user_service(user,db)
    if query is False:
        return templates.TemplateResponse(
            "user/user_gateway/signup.html",
            {"request": request, "message": "Email already exists"},
        )
    if query is True:
        return RedirectResponse(url="/user/login", status_code=303)


def login_user_controller(request: Request, user: UserLoginSchema, db: Session):
    access_token = login_user_service(user, db)
    if access_token:
        response = RedirectResponse(url="/user/home", status_code=303)
        response.set_cookie(key="access_token", value=access_token)
        return response
    else:
        return templates.TemplateResponse(
            "user/user_gateway/login.html",
            {"request": request, "message": "Incorrect email or password"},
        )