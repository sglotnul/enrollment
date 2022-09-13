from datetime import datetime
from json import JSONDecodeError
from select import select
from typing import List, Union
from collections import defaultdict

from aiohttp.web import HTTPOk

from marshmallow import ValidationError

from .base import BaseView
from .validation import ImportsSchema

from sqlalchemy import and_
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from enrollment.db.schema import Item
from enrollment.db.types import ItemType

def create_item(data: dict, date: datetime) -> Item:
    return Item(
        id=data['id'], 
        url=data['url'], 
        date=date,
        parentId=data['parentId'],
        type=ItemType(data['type']),
        size=data['size']
    )

def prepare_items(items, folders_in_db: List[str], date: datetime) -> List[Item]:
    awaitable = defaultdict(lambda: [list(), False])
    ans = []

    def append(item: Item):
        ans.append(create_item(item, date))
        record = awaitable[item['id']]
        record[1] = True
        for item in record[0]:
            append(item)

    for i in items:
        p_id = i['parentId']

        record = awaitable[p_id]
        if p_id is not None and p_id not in folders_in_db and not record[1]:
            record[0].append(i)
        else:
           append(i)
        
    if len(ans) != len(items):
        raise ValidationError("invalid files schema")

    return ans

class ImportsView(BaseView):
    async def update_parents_recursive(self, id: Union[str, None], date: datetime):
        if id is None:
            return
        await self.session.execute(update(Item).where(Item.id == id).values(date=date))
        next_item = await self.session.execute(select(Item.parentId).where(Item.id == id))
        next_item = next_item.scalars().first()

        await self.update_parents_recursive(next_item, date)

    async def validate_item(self, item: Item):
        db_item_type = await self.session.execute(select(Item.type).where(Item.id == item.id))
        db_item_type = db_item_type.scalars().first()
        if db_item_type is not None and db_item_type != item.type:
            raise ValidationError("unable to change item's type")

    async def post(self):
        schema = ImportsSchema()
        data = None

        try:
            data = schema.load(await self.request.json())
        except JSONDecodeError as err:
            raise ValidationError(str(err))

        async with AsyncSession(bind=self.engine) as session:
            self.session = session

            parents_to_validate = set()

            for item in data['items']:
                id = item.get('parentId', None)
                if id:
                    parents_to_validate.add(id)

            rows = await session.execute(select(Item.id).where(and_(Item.id.in_(parents_to_validate), Item.type==ItemType.folder.value.lower())))
            await session.close()

            items = prepare_items(data['items'], rows.scalars(), date=data['updateDate'])

            async with session.begin():
                for i in items:
                    await self.validate_item(i)

                    await session.merge(i)
                    await self.update_parents_recursive(i.parentId, i.date)
                await session.commit()

        await self.engine.dispose()

        return HTTPOk()