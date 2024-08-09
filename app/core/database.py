import aiomysql
import logging
import app.core.const as const
from app.core.error_handler import handle_database_error

class AsyncDBHandler:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host = const.DB_HOST,
                port = const.DB_PORT,
                user = const.DB_USER,
                password = const.DB_PASSWORD,
                db = const.DB_NAME,
                maxsize=100
            )
            print("Connection pool created")

    async def execute(self, query: str, *args):
        if not self.pool:
            await self.connect()
        try:
            connection = await self.pool.acquire()
            cursor = await connection.cursor()
            try:
                logging.debug(f"Executing query: {query} with args: {args}")
                await cursor.execute(query, args)
                await connection.commit()
                result = await cursor.fetchall()
                return result
            finally:
                await cursor.close()
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise handle_database_error(f"Database error: {e}")

