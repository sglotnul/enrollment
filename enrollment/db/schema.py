from json import dumps

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import registry as create_registry

from .types import ItemTypeEnum
from .mixins import MappingSerializable

registry = create_registry()
Model = registry.generate_base()

class Item(Model, MappingSerializable):
    __tablename__ = 'items'

    id = Column(String, primary_key=True)
    url = Column(String(255))
    date = Column(DateTime, nullable=False)
    parentId = Column(String, ForeignKey('items.id', ondelete='CASCADE'))
    type = Column(ItemTypeEnum, nullable=False)
    size = Column(Integer)