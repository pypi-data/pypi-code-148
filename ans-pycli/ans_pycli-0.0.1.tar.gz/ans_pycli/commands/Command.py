from .BaseCommand import BaseCommand
from .mixins import HasSubparsers


class Command(BaseCommand):
    pass


class NestedCommand(HasSubparsers, Command):
    pass
