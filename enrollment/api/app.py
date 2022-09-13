from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncEngine

from aiohttp.web import run_app
from aiohttp.web_app import Application as BaseApp

class Application(BaseApp):
    engine: AsyncEngine = None

    def __init__(self, e: AsyncEngine, *args, **kwargs):
        self.engine = e
        super().__init__(*args, **kwargs)

    def start(self, host: str, port: int):
        run_app(self, host=host, port=port)

    async def check_connection(self):
        try:
            async with self.engine.connect() as conn:
                conn.execute('SELECT 1;')
        except:
            raise DatabaseError('attempt to connect to db failed')