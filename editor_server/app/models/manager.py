from tortoise import fields

from .base import BaseModel, TimestampMixin


class ManagerUser(BaseModel, TimestampMixin):
    """管理员用户"""
    user = fields.ForeignKeyField("models.Users", related_name="manager_user")
    nickname = fields.CharField(max_length=255, unique=True, db_index=True,
                                help_text="昵称")
    avatar = fields.CharField(max_length=255, null=True, help_text="头像")
    is_active = fields.BooleanField(default=True, help_text="是否激活")
    phone = fields.CharField(max_length=255, null=True, help_text="手机号")

    class Meta:
        table = "manager_user"
