import zlib
from aioredis import create_redis_pool


class ARedisClient:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.pool = None

    async def __aenter__(self):
        self.pool = await create_redis_pool(
            f'redis://{self.host}:{self.port}',
            db=self.db,
            password=self.password
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.close()

    async def set(self, key, value, compress=False, atomic=False):
        if compress:
            value = zlib.compress(value.encode('utf-8'))

        if atomic:
            async with self.pool.transaction() as transaction:
                await transaction.set(key, value)
        else:
            await self.pool.set(key, value)

    async def get(self, key):
        value = await self.pool.get(key)
        if value and value.startswith(b'\x78\x9c'):  # zlib 压缩数据的前缀
            return zlib.decompress(value).decode('utf-8')
        return value

    async def delete(self, key):
        await self.pool.delete(key)
