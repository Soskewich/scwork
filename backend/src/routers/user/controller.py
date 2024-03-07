from fastapi import security, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
import jwt as _jwt

from settings_env import settings
from src.model.database import get_db
from src.routers.user.service import service_get_user_by_login, service_create_token, \
    service_oauth2scheme, service_get_user_by_id
from src.schemas.schemas import SchemeUser


async def controller_generate_token(form_data: security.OAuth2PasswordRequestForm, db: Session):
    user = await controller_auth_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Данные неверны")
    token = await service_create_token(user)
    return token


async def controller_auth_user(login: str, password: str, db: Session):
    user = await service_get_user_by_login(login, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    if not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Логин или пароль введены некорректно")
    return user


async def controller_get_current_user(token: str = Depends(service_oauth2scheme()), db: Session = Depends(get_db)):
    try:
        payload = _jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = await service_get_user_by_id(payload["id"], db)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка в логине или пароле")
    return SchemeUser.from_orm(user)

