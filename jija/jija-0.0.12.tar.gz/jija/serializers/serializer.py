import inspect

from typing import Dict

from jija.serializers import fields
from jija.serializers.exceptions import ValidationError


class Serializer:
    def __init__(self, data=None):
        self.data = data or {}
        self.errors = {}

        self.__valid = None
        self.__fields = self.get_fields()

    @classmethod
    def get_fields(cls) -> Dict[str, fields.Field]:
        serializer_fields = {}

        for name, obj in cls.__dict__.items():
            if issubclass(type(obj), fields.Field):
                serializer_fields[name] = obj

        return serializer_fields

    async def in_serialize(self):
        for name, field in self.__fields.items():
            try:
                self.data[name] = await field.validate(self.data.get(name))

            except ValidationError as exception:
                self.errors[name] = exception.error
                self.data[name] = exception.value

        if inspect.iscoroutinefunction(self.clean):
            await self.clean()
        else:
            self.clean()

        self.__valid = len(self.errors) == 0
        if not self.__valid:
            print(self.errors)

        return self.__valid

    async def out_validate(self):
        pass

    @property
    def valid(self):
        return self.__valid

    def clean(self):
        pass
