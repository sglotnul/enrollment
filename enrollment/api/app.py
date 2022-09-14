from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.exc import DatabaseError

from aiohttp.web import run_app
from aiohttp.web_app import Application as BaseApp

async def check_connection(app):
    async with app.engine.connect() as conn:
        await conn.execute(text('SELECT 1;'))

class Application(BaseApp):
    engine: AsyncEngine = None

    def start(self, host: str, port: int):
        self.on_startup.append(check_connection)
        run_app(self, host=host, port=port)

def create_app(url: str) -> Application:
    app = Application()

    app.engine = create_async_engine(url)

    return app