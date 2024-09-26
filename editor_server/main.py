from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise import Tortoise

from app.api.v1.auth import auth_router
from app.api.v1.users import user_router
from app.core.settings import settings, TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if getattr(app.state, "db_connection", None):
        async with Tortoise.close_connections():
            yield
    else:
        await Tortoise.init(config=TORTOISE_ORM)
        app.state.db_connection = True
        yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.APP_OPENAPI_URL,
    version=settings.APP_VERSION,
)


app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return "Index"
