from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from aiohttp.web import run_app
from aiohttp.web_app import Application as BaseApp

async def check_connection(app):
    async with app.engine.connect() as conn:
        await conn.execute(text('SELECT 1;'))

class Application(BaseApp):
    engine: AsyncEngine = None

    def start(self, *args, **kwargs):
        self.on_startup.append(check_connection)
        run_app(self, *args, **kwargs)

def format_pg_connection_string(
    pg_host: str, 
    pg_port: int, 
    pg_user: str,
    pg_password: str,
    db_name: str
) -> str:
    return "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(pg_user, pg_password, pg_host, pg_port, db_name)

def create_app(url: str) -> Application:
    app = Application()

    app.engine = create_async_engine(url)

    return app