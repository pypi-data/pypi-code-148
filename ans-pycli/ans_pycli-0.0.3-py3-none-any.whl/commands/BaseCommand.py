from ans_pycli.helpers import no_action, set_val
from argparse import ArgumentParser, _SubParsersAction


class BaseCommand:
    _name: str = None
    _description: str = None
    _help = None
    _func: callable = None

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 help: str = None,
                 func: callable = None):
        set_val(self, "_name", name, _type=str)
        set_val(self, "_description", description, self._help, help, _type=str)
        set_val(self, "_help", help, self._description, description, _type=str)
        set_val(self, "_func", func, no_action, _type=callable)

    def init(self):
        pass

    def init_parser(self, subparsers: _SubParsersAction) -> ArgumentParser:
        command_parser = subparsers.add_parser(**self.parser_schema)
        command_parser.set_defaults(func=self.func)
        return command_parser

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def help(self):
        return self._help

    @property
    def func(self):
        return self._func

    @property
    def parser_schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "help": self.help,
        }
