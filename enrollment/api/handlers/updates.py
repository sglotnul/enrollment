from aiohttp.web import HTTPOk

from .base import BaseView

class UpdatesView(BaseView):
    async def get(self):
        return HTTPOk()