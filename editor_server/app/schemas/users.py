import datetime
import re

from pydantic import BaseModel, field_validator
from typing import Optional, Union


class CreateUser(BaseModel):
    username: str = 'username'
    email: str = 'user@example.com'
    password: str = 'Example123'

    @field_validator('username')
    def username_validator(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('长度必须大于6')
        if not re.match(r'^[a-zA-Z0-9]*$', v):
            raise ValueError('Username must contain only letters and numbers')
        if v[0].isdigit():
            raise ValueError('Username cannot start with a number')
        return v

    @field_validator('email')
    def email_validator(cls, v: str) -> str:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email address format')
        return v

    @field_validator('password')
    def password_validator(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('密码长度必须大于6')
        return v


class UserInstance(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    last_login: Union[Optional[str], datetime.datetime]
    created_at: Union[Optional[str], datetime.datetime]

    @field_validator('last_login')
    def validate_last_login(cls, v):
        if v is None:
            return None
        try:
            return v.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    @field_validator('created_at')
    def validate_created_at(cls, v):
        if v is None:
            return None
        try:
            return v.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None


class LoginToken(BaseModel):
    access_token: str
    token_type: str


class PermissionInstance(BaseModel):
    id: int
    name: str
    code: str
    description: str = ''


class CreatePermission(BaseModel):
    name: str
    code: str
    description: str = ''

    @field_validator('name')
    def name_validator(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError('长度必须大于2')
        return v

    @field_validator('code')
    def code_validator(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError('长度必须大于2')
        return v


class CreatePermissionGroup(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

    @field_validator('name')
    def name_validator(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError('长度必须大于2')
        return v


class CreateUserPermissionGroups(BaseModel):
    user_id: int
    permission_group_id: int


class CreateUserPermissions(BaseModel):
    user_id: int
    permission_id: int
