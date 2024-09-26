from fastapi import APIRouter, Depends
from typing import List

from app.libs.auth_cli import authenticate_user
from app.models.users import Users
from app.schemas.users import UserInstance


user_router = APIRouter(
    prefix='/api/v1/users',
    tags=['users'],
    dependencies=[Depends(authenticate_user)]
)


@user_router.get('/users', response_model=List[UserInstance])
async def users():
    users = await Users.all()
    return users
