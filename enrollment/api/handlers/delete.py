

from aiohttp.web import HTTPOk
from aiohttp.web_exceptions import HTTPNotFound

from sqlalchemy import exists, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseView, parametrized_handler

from enrollment.db.schema import Item

class DeleteView(BaseView):
    async def exists(self, id: str) -> bool:
        async with AsyncSession(bind=self.engine) as session:
            res = await session.execute(select(exists(Item).where(Item.id == id)))
            await session.close()
            return res.scalars().first()

    @parametrized_handler
    async def delete(self, id: str):
        if not await self.exists(id):
            raise HTTPNotFound(text="item with id {0} not found".format(id))
        async with AsyncSession(bind=self.engine) as session:
            await session.execute(delete(Item).where(Item.id == id))  
            await session.commit()
        return HTTPOk()