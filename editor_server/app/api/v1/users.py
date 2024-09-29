from fastapi import APIRouter, Depends
from typing import List

from app.libs.auth_cli import authenticate_user
from app.models.users import (Users, Permissions, PermissionGroups,
                              UserPermissionGroups)
from app.schemas.users import (CreatePermission, UserInstance,
                               PermissionInstance, CreatePermissionGroup,
                               CreateUserPermissionGroups,
                               CreateUserPermissions)


user_router = APIRouter(
    prefix='/api/v1/users',
    tags=['users'],
    dependencies=[Depends(authenticate_user)]
)


@user_router.get('/users', summary='获取用户列表', response_model=List[UserInstance])
async def users():
    users = await Users.all()
    return users


@user_router.get('/permissions', summary='获取权限列表',
                 response_model=List[PermissionInstance])
async def permissions():
    permissions = await Permissions.all()
    return permissions


@user_router.post('/permissions', summary='创建权限')
async def create_permission(data: CreatePermission):
    permission = await Permissions.create(**data.model_dump())
    return permission


@user_router.get('/permission_groups', summary='获取权限组列表')
async def permission_groups():
    permission_groups = await PermissionGroups.all()
    return permission_groups


@user_router.post('/permission_groups', summary='创建权限组')
async def create_permission_group(data: CreatePermissionGroup):
    permission_group = await PermissionGroups.create(**data.model_dump())
    return permission_group


@user_router.get('/user-permission-groups', summary='用户与权限组关联列表')
async def get_user_permission_groups():
    user_permission_groups = await UserPermissionGroups.all()
    return user_permission_groups


@user_router.post('/user-permission-groups', summary='用户与权限组关联')
async def user_permission_groups(data: CreateUserPermissionGroups):
    user_permission_group = await UserPermissionGroups.create(
        **data.model_dump()
    )
    return user_permission_group


@user_router.get('/user-permissions', summary='用户与权限关联列表')
async def get_user_permissions():
    user_permissions = await UserPermissionGroups.all()
    return user_permissions


@user_router.post('/user-permission', summary='用户与权限关联')
async def user_permission(data: CreateUserPermissions):
    user_permission = await UserPermissionGroups.create(
        **data.model_dump()
    )
    return user_permission
