from datetime import datetime
from json import JSONDecodeError
from select import select
from typing import Union, List

from aiohttp.web import HTTPOk

from marshmallow import ValidationError

from .base import BaseView
from .validation import ImportsSchema

from sqlalchemy import and_
from sqlalchemy import select, update, exists, and_, insert
from sqlalchemy.ext.asyncio import AsyncSession

from enrollment.db.schema import Item, Relation
from enrollment.db.types import ItemType
from enrollment.utils.alghoritms import create_schema

def create_item(data: dict, date: datetime) -> Item:
    return Item(
        id=data['id'], 
        url=data['url'], 
        date=date,
        parentId=data['parentId'],
        type=ItemType(data['type']),
        size=data['size']
    )

async def update_parents_recursive(session: AsyncSession, id: Union[str, None], date: datetime) -> List[str]:
    updated = []
    
    if id is not None:
        updated.append(id)

        await session.execute(update(Item).where(Item.id == id).values(date=date))
        next_item = await session.execute(select(Item.parentId).where(Item.id == id))
        next_item = next_item.scalars().first()

        updated.extend(await update_parents_recursive(session, next_item, date))

    return updated


class ImportsView(BaseView):
    async def insert_item_recursive(self, item: dict, date: datetime, update_parents: bool=False) -> List[str]:
        id = item['id']

        row = await self.session.execute(select(Item.type, Item.parentId).where(Item.id == id))
        entry = row.first()

        if entry is not None:
            await self.session.execute(update(Item).where(Item.id == id).values(**dict(create_item(item, date))))
        else:
            await self.session.execute(insert(Item).values(**dict(create_item(item, date))))

        new_children = []
        for child in item['children']:
            new_children.extend(await self.insert_item_recursive(child, date))

        self.session.add_all(map(lambda child: Relation(parentId=id, childId=child), new_children))

        db_item_type, db_item_parent = None, None

        if entry is not None:
            db_item_type, db_item_parent = entry

            if db_item_type != ItemType(item['type']):
                raise ValidationError("unable to change item's type")
            if (await self.session.execute(select(exists(Relation).where(and_(Relation.parentId == id, Relation.childId == item['parentId']))))).scalar_one():
                raise ValidationError("invalid schema")
            updated_parents = await update_parents_recursive(self.session, db_item_parent, date)
            if db_item_parent != item['parentId']:
                new_children.append(id)
                rows = await self.session.execute(select(Relation.childId).where(Relation.parentId==id))
                new_children.extend(rows.scalars())

                for parent in updated_parents:
                    for c in new_children:
                        to_del = await self.session.get(Relation, (parent, c))
                        await self.session.delete(to_del)
        else:
            new_children.append(id)
            
        if update_parents and db_item_parent != item['parentId']:
            updated_parents = await update_parents_recursive(self.session, item['parentId'], date)
            for parent in updated_parents:
                self.session.add_all(map(lambda child: Relation(parentId=parent, childId=child), new_children))

        return new_children

    async def post(self):
        schema = ImportsSchema()
        data = None

        try:
            data = schema.load(await self.request.json())
        except JSONDecodeError as err:
            raise ValidationError(str(err))

        async with AsyncSession(bind=self.engine, autoflush=False) as session:
            self.session = session

            parents_to_validate = set()

            for item in data['items']:
                id = item.get('parentId', None)
                if id:
                    parents_to_validate.add(id)

            rows = await session.execute(select(Item.id).where(and_(Item.id.in_(parents_to_validate), Item.type==ItemType.folder.value.lower())).order_by(Item.id))
            await session.close()

            try:
                items = create_schema(data['items'], list(rows.scalars()))
            except ValueError as err:
                raise ValidationError(str(err))

            async with session.begin():
                for item in items:
                    await self.insert_item_recursive(item, data['updateDate'], True)
                await session.commit()

        await self.engine.dispose()

        return HTTPOk()