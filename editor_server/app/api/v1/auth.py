from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, List

from app.models.users import Users
from app.schemas.users import CreateUser, LoginToken, UserInstance
from app.libs.auth_cli import AuthCls
from app.libs.encryption_cli import encryption_cls


auth_router = APIRouter(prefix='/api/v1')


@auth_router.post('/login')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> LoginToken:
    auth_cls = AuthCls()
    user = await auth_cls.authenticate_user(
        form_data.username,
        form_data.password
    )
    sub = {
        'sub': user.username
    }
    access_token = await auth_cls.create_access_token(sub)
    return LoginToken(access_token=access_token, token_type='bearer')


@auth_router.get('/users', response_model=List[UserInstance])
async def users():
    users = await Users.all()
    return users


@auth_router.post('/register', response_model=UserInstance)
async def register(payload: CreateUser):
    data = payload.model_dump()
    data['password'] = encryption_cls.encrypt(data['password'])
    user = await Users.create(**data)
    await user.save()
    return user
