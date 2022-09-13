from sqlalchemy.ext.asyncio import AsyncEngine

from aiohttp.web_urldispatcher import View

def parametrized_handler(func):
    def wrapper(self):
        params = self.request.match_info.values()
        return func(self, *params)
    return wrapper

class BaseView(View):
    @property
    def engine(self) -> AsyncEngine:
        return self.request.app.engine