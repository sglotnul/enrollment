from aiohttp.web import RouteDef as RouteDefBase

from .handlers import *

class RouteDef(RouteDefBase):
    def __init__(self, method: str, path: str, handler):
        super().__init__(method, path, handler, {})

urlpatterns = (
    RouteDef('POST', r'/imports', ImportsView),
    RouteDef('DELETE', r'/delete/{id:\S+}', DeleteView),
    RouteDef('GET', r'/nodes/{id:\S+}', NodesView),
    RouteDef('GET', r'/updates', UpdatesView),
    RouteDef('GET', r'/node/{id:\S+}/history', NodeHistoryView),
)