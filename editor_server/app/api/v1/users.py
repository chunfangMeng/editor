from fastapi import APIRouter, Depends
from typing import List

from app.core.response import response, BaseResponse
from app.libs.auth_cli import authenticate_user
from app.models.users import (Users, Permissions, PermissionGroups,
                              UserPermissionGroups, UserPermissions)
from app.schemas.users import (CreatePermission, UserInstance,
                               PermissionInstance, CreatePermissionGroup,
                               CreateUserPermissionGroups,
                               PermissionGroupInstance,
                               CreateUserPermissions,
                               UserPermissionGroupInstance,
                               UserPermissionInstance)


user_router = APIRouter(
    prefix='/api/v1/users',
    tags=['用户与权限'],
    dependencies=[Depends(authenticate_user)]
)


@user_router.get('/users', summary='获取用户列表',
                 response_model=BaseResponse[List[UserInstance]])
async def users():
    users = await Users.all()
    return await response(200, '获取用户列表成功', users)


@user_router.get('/permissions', summary='获取权限列表',
                 response_model=BaseResponse[List[PermissionInstance]])
async def permissions():
    permissions = await Permissions.all()
    return await response(200, '获取权限列表成功', permissions)


@user_router.post('/permissions', summary='创建权限',
                  response_model=BaseResponse[PermissionInstance])
async def create_permission(data: CreatePermission):
    permission = await Permissions.create(**data.model_dump())
    return await response(200, '创建权限成功', permission)


@user_router.get('/permission_groups', summary='获取权限组列表',
                 response_model=BaseResponse[List[PermissionGroupInstance]])
async def permission_groups():
    permission_groups = await PermissionGroups.filter(is_active=True)
    return await response(200, '获取权限组列表成功', permission_groups)


@user_router.post('/permission_groups', summary='创建权限组',
                  response_model=BaseResponse[PermissionGroupInstance])
async def create_permission_group(data: CreatePermissionGroup):
    permission_group = await PermissionGroups.create(**data.model_dump())
    return await response(200, '创建权限组成功', permission_group)


@user_router.get('/user-permission-groups', summary='用户与权限组关联列表',
                 response_model=BaseResponse[
                     List[UserPermissionGroupInstance]])
async def get_user_permission_groups():
    user_permission_groups = await UserPermissionGroups.all()
    return await response(200, '获取用户与权限组关联列表成功', user_permission_groups)


@user_router.post('/user-permission-groups', summary='用户与权限组关联',
                  response_model=BaseResponse)
async def user_permission_groups(data: CreateUserPermissionGroups):
    existed_bind = await UserPermissionGroups.filter(
        **data.model_dump()
    ).first()
    if existed_bind:
        return await response(400, '用户与权限组已关联')
    user_permission_group = await UserPermissionGroups.create(
        **data.model_dump()
    )
    return user_permission_group


@user_router.get('/user-permissions', summary='用户与权限关联列表',
                 response_model=BaseResponse[List[UserPermissionInstance]])
async def get_user_permissions():
    user_permissions = await UserPermissions.all().select_related(
        'user', 'permission'
    )
    data = [{
        'id': item.id,
        'user': UserInstance.model_validate(item.user),
        'permission': PermissionInstance.model_validate(item.permission),
        'is_active': item.is_active
    } for item in user_permissions]
    return await response(200, '获取用户与权限关联列表成功', data)


@user_router.post('/user-permission', summary='用户与权限关联',
                  response_model=BaseResponse)
async def user_permission(data: CreateUserPermissions):
    existed_bind = await UserPermissions.filter(
        **data.model_dump()
    ).first()
    if existed_bind:
        return await response(400, '用户与权限已关联')
    await UserPermissions.create(
        **data.model_dump()
    )
    return await response(200, '用户与权限关联成功')


@user_router.delete('/user-permission/{id}', summary='删除用户与权限关联',
                    response_model=BaseResponse)
async def delete_user_permission(id: int):
    user_permission = await UserPermissions.get(id=id)
    await user_permission.delete()
    return await response(200, '删除用户与权限关联成功')


@user_router.delete('/user-permission-groups/{id}', summary='删除用户与权限组关联',
                    response_model=BaseResponse)
async def delete_user_permission_groups(id: int):
    user_permission_group = await UserPermissionGroups.get(id=id)
    await user_permission_group.delete()
    return await response(200, '删除用户与权限组关联成功')
