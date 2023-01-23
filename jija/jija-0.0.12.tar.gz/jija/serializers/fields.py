from jija.serializers.validators import *
from jija.serializers.exceptions import ValidationError


class Field:
    DOC_TYPE = NotImplemented
    DOC_FORMAT = None

    validators = ()

    def __init__(self, *, required=True, default=None):
        self.required = required
        self.default = default

    async def validate(self, value):
        if value is None:
            if self.required and self.default is None:
                raise ValidationError('Required field', value)
            else:
                return value or self.default

        for validator in self.validators:
            value = await validator.validate(value, self)

        return value

    def doc_get_schema(self):
        return {
            **self.doc_get_type_data(),
            **self.doc_get_extra()
        }

    def doc_get_type_data(self):
        type_data = {
            'type': self.DOC_TYPE
        }

        if self.DOC_FORMAT:
            type_data['format'] = self.DOC_FORMAT

        return type_data

    def doc_get_extra(self):
        return {}


class CharField(Field):
    DOC_TYPE = 'string'

    validators = (LengthMinValidator, LengthMaxValidator)

    def __init__(self, *, min_length=None, max_length=None, regex=None, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex

    def doc_get_extra(self):
        extra = {}
        if self.max_length is not None:
            extra['maxLength'] = self.max_length

        if self.min_length is not None:
            extra['minLength'] = self.min_length

        return extra


class NumericField(Field):
    def __init__(self, *, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def doc_get_extra(self):
        extra = {}

        if self.max_value is not None:
            extra['maximum'] = self.max_value

        if self.min_value is not None:
            extra['minimum'] = self.min_value

        return extra


class IntegerField(NumericField):
    DOC_TYPE = 'integer'
    DOC_FORMAT = 'int32'

    validators = (IntegerValidator, RangeMinValidator, RangeMaxValidator)


class FloatField(NumericField):
    DOC_TYPE = 'number'
    DOC_FORMAT = 'float'

    validators = (FloatValidator, RangeMinValidator, RangeMaxValidator)


class DateField(Field):
    DOC_TYPE = 'string'
    DOC_FORMAT = 'date'

    validators = (DateValidator, RangeMinValidator, RangeMaxValidator)

    def __init__(self, *, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value


class SelectField(Field):
    validators = (OptionsValidator,)

    def __init__(self, *, options, **kwargs):
        super().__init__(**kwargs)
        self.options = options
