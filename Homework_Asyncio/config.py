PG_USER = 'user1'
PG_PASSWORD = 'user1'
PG_HOST = '127.0.0.1'
PG_DB = 'asyncio_homework'
PG_DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5433/{PG_DB}'
PG_DSN_ALC = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5433/{PG_DB}'
