import jwt

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, List

from app.core.settings import settings
from app.models.users import Users, UserPermissions, UserPermissionGroups
from app.libs.encryption_cli import encryption_cls


class AuthCls:
    def __init__(self):
        self.secret_key = settings.AUTH_SECRET_KEY
        self.algorithm = settings.AUTH_ALGORITHM
        self.auth_access_token_expire_minutes = settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES  # noqa: E501

    async def create_access_token(self, data: dict,
                                  expires_delta: Optional[timedelta] = None):
        access_token_expires = timedelta(
            minutes=self.auth_access_token_expire_minutes
        )
        if expires_delta is None:
            expires_delta = access_token_expires
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key,
                                 algorithm=self.algorithm)
        return encoded_jwt

    async def authenticate_user(self, username: str, password: str):
        user_instance = await Users.filter(username=username).first()
        if not user_instance:
            raise Exception("User not found")
        is_valid = encryption_cls.verify(password, user_instance.password)
        if not is_valid:
            raise Exception("Invalid password")
        return user_instance


oauth2 = OAuth2PasswordBearer(tokenUrl='/api/v1/login/', scheme_name="User",)


async def authenticate_user(request: Request, token=Depends(oauth2)):
    try:
        payload = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )
        user_instance = await Users.filter(username=payload.get('sub')).first()
        if user_instance is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )
        request.state.user = user_instance
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )


def permission_wrapper(permission_codes: List[str],
                       group_codes: List[str] = None):

    async def permission_required(request: Request):
        if permission_codes is None and group_codes is None:
            return True
        user = request.state.user
        has_permission = await UserPermissions.filter(
            user=user,
            permission__code__in=permission_codes,
            is_active=True
        ).exists()
        if not has_permission:
            if group_codes is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限访问",
                )
            has_permission_group = await UserPermissionGroups.filter(
                user=user,
                permission_group__code__in=group_codes,
                is_active=True
            ).exists()
            if not has_permission_group:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限访问",
                )
        return True
    return permission_required
