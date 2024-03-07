from fastapi import APIRouter, Depends, security
from sqlalchemy.ext.asyncio import AsyncSession as Session
from starlette.responses import JSONResponse

from settings_env import settings
from src.model.database import get_db
from src.routers.user.controller import controller_generate_token, controller_get_current_user


router = APIRouter(
    prefix="/api/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@router.post("/token")
async def login(form_data: security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login user
    :param form_data: login data
    :param db: Current db Session
    :return: JWT-token
    """
    token = await controller_generate_token(form_data, db)
    response = JSONResponse(dict(Bearer=token['access_token']))
    response.set_cookie("Authorization",
                        value=f"Bearer {token['access_token']}",
                        httponly=True,
                        domain=settings.DOMAIN,
                        secure=settings.SECURE_COOKIE,
                        max_age=1800,
                        expires=1800,)
    return response

