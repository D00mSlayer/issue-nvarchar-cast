from copy import copy
from schematics.models import Model

def to_orm(db_entity_cls):
    def db_entity_factory(data, context):
        if isinstance(data, Model):
            data = data.to_primitive()
        return db_entity_cls(**data)
    return db_entity_factory


class CustomModel(Model):
    def __init__(self, *args, **kwargs):
        self.initial_params = args[0] if args else {}
        context = kwargs.pop('context', None)
        super(CustomModel, self).__init__(
            strict=False,
            app_data=context,
            *args,
            **kwargs
        )
        self._bind_context(context)

    def _bind_context(self, context):
        self.ctx = self.context = context
        self.session = context['session']

    @classmethod
    def map_in(cls, data, *mappers, **context):
        for mapper in mappers:
            data = mapper(data, context)
        return cls(data, **context)

    def map_out(self, *mappers, **context):
        export_app_data = copy(self.context).update(context)
        data = dict(copy(self._data))
        for mapper in mappers:
            data = mapper(data, export_app_data)
        return data

    def to_db_entity(self, entity_cls, *mappers):
        mappers = mappers + (to_orm(entity_cls),)
        return self.map_out(*mappers, context=self.context)

    @classmethod
    def from_db_entity(cls, db_entity, *mappers, **context):
        return cls.map_in(db_entity.asDict(), *mappers, **context)
