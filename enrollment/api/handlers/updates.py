from aiohttp.web import HTTPNotImplemented

from .base import BaseView

class UpdatesView(BaseView):
    async def get(self):
        raise HTTPNotImplemented()