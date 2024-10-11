import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv(verbose=True)


class Settings(BaseSettings):
    APP_NAME: str = 'FastAPI'
    APP_VERSION: str = '0.0.1'
    APP_OPENAPI_URL: str = '/api/openapi.json'
    DOCS_URL: str = '/api/docs'
    REDOC_URL: str = '/api/redoc'
    DB_ENGINE: str = os.getenv('DB_ENGINE')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('DB_PORT')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')

    AUTH_SECRET_KEY: str = os.getenv('AUTH_SECRET_KEY')
    AUTH_ALGORITHM: str = 'HS256'
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: str = os.getenv('REDIS_PORT')
    REDIS_DB: int = os.getenv('REDIS_DB')


settings = Settings()

DB_URL = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
    settings.DB_ENGINE,
    settings.DB_USER,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_NAME,
)

TORTOISE_ORM = {
    "connections": {
        "default": DB_URL
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "app.models.users",
                       "app.models.manager"],
            "default_connection": "default",
        },
    },
}


INIT_PERMISSIONS = [{
    'code': 'VIEW_USERS',
    'name': '查看用户',
}, {
    'code': 'CREATE_PERMISSIONS',
    'name': '创建权限',
}, {
    'code': 'VIEW_PERMISSIONS',
    'name': '查看权限',
}, {
    'code': 'CREATE_PERMISSION_GROUPS',
    'name': '创建权限组',
}, {
    'code': 'VIEW_PERMISSION_GROUPS',
    'name': '查看权限组',
}]
