#!/bin/bash
cat <<EOF > .env
DB_ENGINE = 'asyncpg'
DB_HOST = 'db'
DB_PORT = '5432'
DB_USER = 'postgres'
DB_PASSWORD = '123456'
DB_NAME = 'editor'

AUTH_SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
EOF

aerich init-db & aerich migrate --name migrate_column & aerich upgrade

uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 4