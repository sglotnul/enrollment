

from json import JSONDecodeError
from marshmallow import ValidationError

from aiohttp.web import HTTPOk
from aiohttp.web_exceptions import HTTPNotFound

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseView, parametrized_handler
from .imports import update_parents_recursive
from .validation import DateSchema

from enrollment.db.schema import Item

class DeleteView(BaseView):
    async def get_item(self, id: str) -> Item:
        res = await self.session.execute(select(Item).where(Item.id == id))
        return res.scalar_one()

    @parametrized_handler
    async def delete(self, id: str):
        self.request.query.get('date', None)

        schema = DateSchema()
        date = None

        try:
            date = schema.load(self.request.query)['date']
        except JSONDecodeError as err:
            raise ValidationError(str(err))

        async with AsyncSession(bind=self.engine) as session:
            self.session = session
            item = await self.get_item(id)

            if item is None:
                raise HTTPNotFound(text="item with id {0} not found".format(id))

            await update_parents_recursive(self.session, item.parentId, date)
        
            await session.execute(delete(Item).where(Item.id == id))  
            await session.commit()
        return HTTPOk()