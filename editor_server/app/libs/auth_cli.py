import jwt

from datetime import datetime, timedelta, timezone
from typing import  Optional

from app.core.settings import settings
from app.models.users import Users
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
