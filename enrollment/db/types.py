from enum import Enum as Enumerable

from sqlalchemy import Enum

class ItemType(Enumerable):
    file = 'FILE'
    folder = 'FOLDER'

ItemTypeEnum = Enum(ItemType, name="type")

__custom_types__ = (ItemTypeEnum, )