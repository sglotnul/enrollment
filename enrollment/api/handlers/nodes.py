from json import dumps

from sqlalchemy import select, join, func
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPNotFound

from .base import BaseView, parametrized_handler
from .validation.schema import DATE_FORMAT

from enrollment.db.schema import Item
from enrollment.db.types import ItemType

class NodesView(BaseView):
    def query(self, id: str):
        t2 = aliased(Item, name='t2')
        return select(
            Item,
            func.array_remove(func.array_agg(t2.id), None)
        ).select_from(
            join(Item, t2, Item.id == t2.parentId, isouter=True)
        ).where(Item.id == id).group_by(Item.id)

    async def get_intem_data_recursive(self, id: str) -> dict:
        async with AsyncSession(bind=self.engine) as session:
            data = (await session.execute(self.query(id))).first()
            if data is None:
                raise HTTPNotFound(text="item with id {0} not found".format(id))
            item, children = data

            data = dict(item)
            data['size'] = data['size'] or 0
            data['date'] = data['date'].strftime(DATE_FORMAT)
            if item.type == ItemType.file:
                data['children'] = None
            else:
                data['children'] = []
                for child_id in children:
                    child_data = await self.get_intem_data_recursive(child_id)
                    data['children'].append(child_data)
                    data['size'] += child_data['size']
            data['type'] = data['type'].value
            return data

    @parametrized_handler
    async def get(self, id: str):
        node_data = await self.get_intem_data_recursive(id)
        return json_response(node_data)