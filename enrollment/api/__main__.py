import sys

from typing import Iterable, Callable

from aiohttp.web import RouteDef

from .middleware import errors_format_middleware
from .app import Application, create_app
from .routing import urlpatterns

MIDDLEWARES = (errors_format_middleware, )

def add_routes(app: Application, routes: Iterable[RouteDef]):
    app.router.add_routes(routes)

def add_middlewares(app: Application, middlewares: Iterable[Callable]):
    app.middlewares.extend(middlewares)

def main(): 
    app = create_app(sys.argv[1])

    add_routes(app, urlpatterns)

    #add_middlewares(app, MIDDLEWARES)

    app.start('0.0.0.0', 8080)

if __name__ == "__main__":
    main()