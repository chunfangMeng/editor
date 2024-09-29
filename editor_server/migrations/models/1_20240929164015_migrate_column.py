from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE INDEX "idx_permissions_code_a3bbd6" ON "permissions" ("code", "name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_permissions_code_a3bbd6";"""
