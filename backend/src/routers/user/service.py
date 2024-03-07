from typing import Optional

from fastapi import Request, status, HTTPException
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
import jwt as _jwt

from settings_env import settings
from src.model.model import User
from src.schemas.schemas import SchemeUser


async def service_get_user_by_login(login: str, db: Session):
    user_result = await db.execute(select(User).filter(User.login == login))
    user = user_result.scalars().first()
    return user


async def service_create_token(user: User):
    user_object = SchemeUser.from_orm(user)
    token = _jwt.encode(user_object.dict(), settings.SECRET_KEY)
    return dict(access_token=token, token_type="bearer")


async def service_get_user_by_id(id: int, db: Session):
    user_result = await db.execute(select(User).filter(User.id == id))
    user = user_result.scalars().first()
    return user


def service_oauth2scheme():
    return OAuth2PasswordBearerCookie(tokenUrl="/api/user/token")


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param

