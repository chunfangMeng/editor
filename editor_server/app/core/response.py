from pydantic import BaseModel
from typing import Generic, TypeVar, Any


T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = 'success'
    data: T = []

    class Config:
        from_attributes = True


async def response(code: int, message: str, data: Any = []) -> BaseResponse:
    return BaseResponse(code=code, message=message, data=data)
