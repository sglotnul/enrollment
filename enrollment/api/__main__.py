from sqlalchemy.ext.asyncio import create_async_engine

from .middleware import errors_format_middleware
from .routing import urlpatterns
from .app import Application

middlewares = (errors_format_middleware, )

def create_app() -> Application:
    app = Application(create_async_engine("postgresql+asyncpg://admin:admin@localhost:5432/maindb"))
    app.check_connection()

    app.router.add_routes(urlpatterns)

    app.middlewares.extend(middlewares)

    return app

def main():
    app = create_app()

    app.start('0.0.0.0', 8080)

if __name__ == "__main__":
    main()