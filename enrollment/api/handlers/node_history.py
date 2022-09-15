from aiohttp.web import HTTPNotImplemented

from .base import BaseView

class NodeHistoryView(BaseView):
    async def get(self, id: str):
        raise HTTPNotImplemented()