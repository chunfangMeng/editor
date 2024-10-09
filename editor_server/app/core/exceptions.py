from typing import Union

from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.responses import JSONResponse

from app.core.response import response, BaseResponse


async def http_exception_handler(
        request: Request, exc: HTTPException) -> BaseResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=(await response(exc.status_code, exc.detail)).model_dump(),
    )


async def params_validation_handler(
        request: Request,
        exc: Union[RequestValidationError, ]) -> BaseResponse:
    return JSONResponse(
        content=await response(
            code=HTTP_422_UNPROCESSABLE_ENTITY,
            message=f'数据校验错误 {exc.errors()}',
        )
    )
