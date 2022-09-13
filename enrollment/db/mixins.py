from sqlalchemy.ext.declarative import DeclarativeMeta

class MappingSerializable:
    def __iter__(self) -> tuple:
        private_fields = ('metadata', 'registry')
        if isinstance(self.__class__, DeclarativeMeta):
            for field in [x for x in dir(self) if not x.startswith('_') and x not in private_fields]:
                data = self.__getattribute__(field)
                yield (field, data)