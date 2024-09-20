from tortoise.models import Model
from tortoise import fields


class BaseModel(Model):
    """Base model for all models"""
    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.id}>"


class TimestampMixin(Model):
    """Mixin for models with created_at and updated_at fields"""
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
