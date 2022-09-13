from datetime import datetime

from marshmallow import Schema, ValidationError, validates, validates_schema
from marshmallow.fields import Str, Integer, DateTime, List, Url, Nested
from marshmallow.validate import OneOf, Length

from enrollment.db.types import ItemType

DATE_FORMAT = r"%Y-%m-%dT%H:%M:%SZ"

class ItemSchema(Schema):
    id = Str(required=True)
    url = Url(relative=True, allow_none=True, load_default=None, validate=Length(max=255))
    parentId = Str(allow_none=True, load_default=None)
    type = Str(required=True, validate=OneOf([t.value for t in ItemType]))
    size = Integer(allow_none=True, load_default=None)

    @validates_schema
    def validate_size(self, data, **_):
        size = data.get('size', None)
        data_type = data['type']
        if data_type == ItemType.folder.value and size is not None:
            raise ValidationError("Folder can't have not-null size field")
        elif data_type == ItemType.file.value and (size is None or size <= 0):
            raise ValidationError("File can't have negative or zero size")

    @validates_schema
    def validate_parentId(self, data, **_):
        parentId = data.get('parentId', None)
        if parentId and parentId == data['id']:
            raise ValidationError("Item can't be a parent of itself")

class ImportsSchema(Schema):
    items = List(Nested(ItemSchema), required=True)
    updateDate = DateTime(format=DATE_FORMAT, required=True)

    @validates('updateDate')
    def validate_birth_date(self, value: datetime):
        if value > datetime.today():
            raise ValidationError("Date can't be in future")
        
    @validates_schema
    def validate_unique_item_id(self, data, **_):
        items_ids = set()
        for item in data['items']:
            if item['id'] in items_ids:
                raise ValidationError(
                    'item with id %r is not unique' % item['id']
                )
            items_ids.add(item['id'])