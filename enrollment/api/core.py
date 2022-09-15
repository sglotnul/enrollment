from typing import Iterable, Callable

from aiohttp.web import RouteDef

from .middleware import errors_format_middleware
from .app import Application, create_app, format_pg_connection_string
from .routing import urlpatterns

MIDDLEWARES = (errors_format_middleware, )

def add_routes(app: Application, routes: Iterable[RouteDef]):
    app.router.add_routes(routes)

def add_middlewares(app: Application, middlewares: Iterable[Callable]):
    app.middlewares.extend(middlewares)

def start_application(
    host: str, 
    port: int, 
    pg_host: str, 
    pg_port: int, 
    pg_user: str,
    pg_password: str,
    pg_db_name: str
): 
    app = create_app(format_pg_connection_string(pg_host, pg_port, pg_user, pg_password, pg_db_name))

    add_routes(app, urlpatterns)

    add_middlewares(app, MIDDLEWARES)

    app.start(host=host, port=port)