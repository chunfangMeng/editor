from tortoise import fields

from .base import BaseModel, TimestampMixin


class Users(BaseModel, TimestampMixin):
    username = fields.CharField(max_length=255, unique=True, help_text="用户名")
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    last_login = fields.DatetimeField(null=True)
    last_request = fields.DatetimeField(null=True)


class Permissions(BaseModel, TimestampMixin):
    code = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)


# 权限组
class PermissionGroups(BaseModel, TimestampMixin):
    code = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)


class PermissionGroupPermissions(BaseModel, TimestampMixin):
    permission_group = fields.ForeignKeyField(
        "models.PermissionGroups", related_name="permission_group_permissions"
    )
    permission = fields.ForeignKeyField(
        "models.Permissions", related_name="permission_group_permissions"
    )
