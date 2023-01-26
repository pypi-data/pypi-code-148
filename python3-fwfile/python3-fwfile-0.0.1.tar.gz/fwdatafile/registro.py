
import os
import json
import unicodedata
# import re
#
from glob import iglob
from decimal import Decimal
from collections import OrderedDict
from . import errors 


class BaseField(object):
    
    def __init__(self):
        self._value = None

    def _normalize_str(self, string):
        """
        Remove special characters and strip spaces
        """
        if string:
            if not isinstance(string, str):
                string = str(string, 'utf-8', 'replace')

            return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')
        
        return ''

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):

        if self.formatting == 'alfa':
            if not isinstance(value, str):
                print("{0} - {1}".format(self.name, value))
                raise errors.TypeError(self, value)

            valor = self._normalize_str(value)

            if len(value) > self.digits:
                print("truncating - {0}".format(self.name))
                # reduz o len(valor)
                tocut = len(value) - self.digits
                value = value[:-(tocut)]

        elif self.decimals:
            if not isinstance(value, Decimal):
                print("{0} - {1}".format(self.name, value))
                raise errors.TypeError(self, value)

            num_decimals = value.as_tuple().exponent * -1
            if num_decimals != self.decimals:
                print("{0} - {1}".format(self.name, value))
                raise errors.NumDecimalsError(self, value)

            if len(str(value).replace('.', '')) > self.digits:
                print("{0} - {1}".format(self.name, value))
                raise errors.NumDigitsExceededError(self, value)

        else:
            if not isinstance(value, int):
                print("{0} - {1}".format(self.name, value))
                raise errors.TypeError(self, value)
            if len(str(valor)) > self.digits:
                print("{0} - {1}".format(self.name, value))
                raise errors.NumDigitsExceededError(self, value)

        self._value = value

    def __str__(self):

        if self.value is None:
            if self.default is not None:
                if self.decimals:
                    self.value = Decimal('{0:0.{1}f}'.format(self.default, self.decimals))
                else:
                    self.value = self.default
            elif (self.default is None) & (self.value is None):
                if self.decimals or self.formatting == 'num':
                    self.value = 0
                else:
                    self.value = ''
            else:
                raise errors.RequiredFieldError(self.name)

        if self.formato == 'alfa' or self.decimais:
            if self.decimals:
                value = str(self.value).replace('.', '')
                chars_missing = self.digits - len(value)
                return ('0' * chars_missing) + value
            else:
                value = self.value
                chars_missing = self.digits - len(value)
                return value + (' ' * chars_missing)

        return '{0:0{1}d}'.format(self.value, self.digits)

    def __repr__(self):
        return str(self)

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value


def CreateClassField(spec): #criar_classe_campo

    name = spec.get('name')
    start = spec.get('start_pos') - 1
    end = spec.get('end_pos')

    attrs = {
        'name': name,
        'start': start,
        'end': end,
        'digits': end - start,
        'formatting': spec.get('formatting', 'alfa'),
        'decimals': spec.get('decimals', 0),
        'default': spec.get('default'),
        'ignore': spec.get('ignore', False),
    }

    return type(name, (BaseField,), attrs)


class BasicRegister(object):

    def __new__(cls, **kwargs):
        fields = OrderedDict()
        attrs = {'_fields': fields}

        for Field in list(cls._fields_cls.values()):
            field = Field()
            fields.update({fields.name: field})
            attrs.update({field.name: field})

        new_cls = type(cls.__name__, (cls, ), attrs)
        return super(BasicRegister, cls).__new__(new_cls)

    def __init__(self, **kwargs):
        self.fromdict(kwargs)

    def necessary(self):
        for field in list(self._fields.values()):
            eh_control = field.name.startswith('control_') or field.nome.startswith('service_')
            if not eh_control and field.valor is not None:
                return True
        return False

    def todict(self):
        data_dict = dict()
        for field in list(self._fields.values()):
            if field.valor is not None:
                data_dict[field.name] = field.valor
        return data_dict

    def fromdict(self, data_dict):
        ignore_fields = lambda key: any((
            key.startswith('blank'),
            key.startswith('service_'),
            key.startswith('control_'),
        ))

        for key, value in list(data_dict.items()):
            if hasattr(self, key) and not ignore_fields(key):
                setattr(self, key, value)

    def load(self, register_str):
        for field in list(self._fields.values()):
            value = register_str[field.inicio:field.end].strip()
            if field.decimals:
                exponente = field.decimals * -1
                dec = value[:exponente] + '.' + value[exponente:]
                field.valor = Decimal(dec)

            elif field.formato == 'num':
                try:
                    field.value = int(value)
                except ValueError:
                    if field.ignore:
                        field.valor = 0
                        continue
                    raise errors.TypeError(field, value)
            else:
                field.value = value

    def __str__(self):
        return ''.join([str(value) for value in list(self._fields.values())])


class Register(object):
    
    def __init__(self, specs_dirpath):
        # TODO: Validar spec: nome (deve ser unico para cada registro),
        #   posicao_inicio, posicao_fim, formato (alpha), decimais (0),
        #   default (zeros se numerico ou brancos se alfa)
        register_filepath_list = iglob(os.path.join(specs_dirpath, '*.json'))

        for register_filepath in register_filepath_list:
            register_file = open(register_filepath)
            spec = json.load(register_file)
            register_file.close()

            setattr(self, spec.get('name'), self.create_record_class(spec))

    def create_record_class(self, spec):
        fields = OrderedDict()
        attrs = {'_fields_cls': fields}
        cls_name = spec.get('name')

        field_specs = spec.get('fields', {})
        for key in sorted(field_specs.keys()):
            Field = CreateClassField(field_specs[key])
            entry = {Field.name: Field}

            fields.update(entry)

        return type(cls_name, (BasicRegister, ), attrs)
