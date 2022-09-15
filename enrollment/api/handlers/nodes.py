from typing import List

from sqlalchemy import select, join, union
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPNotFound

from .base import BaseView, parametrized_handler
from .validation.schema import DATE_FORMAT

from enrollment.db.schema import Item, Relation
from enrollment.db.types import ItemType
from enrollment.utils.alghoritms import create_schema

class NodesView(BaseView):
    def query1(self, id: str) -> object:
        return union(
            select(
                Item
            ).select_from(
                join(Relation, Item, Relation.childId == Item.id)
            ).where(Relation.parentId == id),
            select(Item).where(Item.id == id)
        )
            
    def query2(self, id: str) -> object:
        return select(Relation.parentId).where(Relation.childId == id)

    async def get_items(self, id: str) -> List[dict]:
        rows = await self.session.execute(self.query1(id))
        return [dict(item) for item in rows]

    async def get_parents(self, id: str) -> List[str]:
        rows = await self.session.execute(self.query2(id))
        return list(rows.scalars())

    def format_schema(self, item: dict) -> dict:
        item['date'] = item['date'].strftime(DATE_FORMAT)
        item['size'] = item['size'] or 0
        t = item['type']
        item['type'] = item['type'].value

        if t == ItemType.file:
            item['children'] = None
        else:
            for child in item['children']:
                item['size'] += self.format_schema(child)

        return item['size']

    async def get_intem_data(self, id: str) -> dict:
        async with AsyncSession(bind=self.engine) as session:
            self.session = session

            items = await self.get_items(id)
            parents = await self.get_parents(id)
            
            schema = create_schema(items, parents)
            if len(schema) < 1:
                exc = HTTPNotFound()
                exc.text = "item with id {0} not found".format(id)
                raise exc
            
            item_data = schema[0]
            self.format_schema(item_data)
            
            return item_data

    @parametrized_handler
    async def get(self, id: str):
        node_data = await self.get_intem_data(id)
        return json_response(node_data)