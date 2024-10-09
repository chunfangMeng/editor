from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "permissiongrouppermissions" RENAME TO "permission_group_permissions";
        ALTER TABLE "permissiongroups" RENAME TO "permission_groups";
        ALTER TABLE "userpermissiongroups" RENAME TO "user_permission_groups";
        ALTER TABLE "userpermissions" RENAME TO "user_permissions";
        CREATE TABLE IF NOT EXISTS "manager_user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "nickname" VARCHAR(255) NOT NULL UNIQUE,
    "avatar" VARCHAR(255),
    "is_active" BOOL NOT NULL  DEFAULT True,
    "phone" VARCHAR(255),
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_manager_use_nicknam_baf218" ON "manager_user" ("nickname");
COMMENT ON TABLE "manager_user" IS '管理员用户';
        CREATE INDEX "idx_permission__permiss_4e952f" ON "permission_group_permissions" ("permission_group_id", "permission_id");
        CREATE INDEX "idx_permission__code_775442" ON "permission_groups" ("code", "name");
        CREATE INDEX "idx_user_permis_user_id_d04dc8" ON "user_permission_groups" ("user_id", "permission_group_id");
        CREATE INDEX "idx_user_permis_user_id_c1e30d" ON "user_permissions" ("user_id", "permission_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_permission__permiss_4e952f";
        DROP INDEX "idx_user_permis_user_id_d04dc8";
        DROP INDEX "idx_permission__code_775442";
        DROP INDEX "idx_user_permis_user_id_c1e30d";
        ALTER TABLE "user_permissions" RENAME TO "userpermissions";
        ALTER TABLE "permission_groups" RENAME TO "permissiongroups";
        ALTER TABLE "user_permission_groups" RENAME TO "userpermissiongroups";
        ALTER TABLE "permission_group_permissions" RENAME TO "permissiongrouppermissions";
        DROP TABLE IF EXISTS "manager_user";"""
