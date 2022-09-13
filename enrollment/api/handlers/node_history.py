from aiohttp.web import HTTPOk

from .base import BaseView

class NodeHistoryView(BaseView):
    async def get(self):
        id = self.get_parameter('id', int)
        
        return HTTPOk()