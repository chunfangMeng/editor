from tortoise import fields

from .base import BaseModel, TimestampMixin


# 用户
class Users(BaseModel, TimestampMixin):
    username = fields.CharField(max_length=255, unique=True, db_index=True,
                                help_text="用户名")
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    last_login = fields.DatetimeField(null=True)
    last_request = fields.DatetimeField(null=True)

    class Meta:
        table = "users"


# 权限
class Permissions(BaseModel, TimestampMixin):
    code = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "permissions"
        indexes = (('code', 'name'),)


# 权限组
class PermissionGroups(BaseModel, TimestampMixin):
    code = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "permission_groups"
        indexes = (('code', 'name'),)


# 权限组与权限关联
class PermissionGroupPermissions(BaseModel, TimestampMixin):
    permission_group = fields.ForeignKeyField(
        "models.PermissionGroups", related_name="permission_group_permissions"
    )
    permission = fields.ForeignKeyField(
        "models.Permissions", related_name="permission_group_permissions"
    )

    class Meta:
        table = "permission_group_permissions"
        indexes = (('permission_group', 'permission'),)


# 用户与权限组关联
class UserPermissionGroups(BaseModel, TimestampMixin):
    user = fields.ForeignKeyField("models.Users",
                                  related_name="user_permission_groups")
    permission_group = fields.ForeignKeyField(
        "models.PermissionGroups", related_name="user_permission_groups"
    )
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "user_permission_groups"
        indexes = (('user', 'permission_group'),)


# 用户与权限关联
class UserPermissions(BaseModel, TimestampMixin):
    user = fields.ForeignKeyField("models.Users",
                                  related_name="user_permissions")
    permission = fields.ForeignKeyField("models.Permissions",
                                        related_name="user_permissions")
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "user_permissions"
        indexes = (('user', 'permission'),)
