#!/bin/bash
cat <<EOF > .env
DB_ENGINE = 'asyncpg'
DB_HOST = 'editor_db'
DB_PORT = '5433'
DB_USER = 'postgres'
DB_PASSWORD = '123456'
DB_NAME = 'editor'

AUTH_SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0
EOF

aerich init-db && aerich migrate --name migrate_column && aerich upgrade

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9000 --reload