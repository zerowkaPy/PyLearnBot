from asyncpg import connect, Connection


async def set_connect(db_url:str):
        conn = await connect(db_url)
        return conn

async def close_connect(conn:Connection):
        await conn.close()