from argparse import ArgumentParser, _SubParsersAction

SubparsersDictType = dict[str, list]
ParserType = ArgumentParser | _SubParsersAction


class HasSubparsers:
    _subparsers: SubparsersDictType = {}

    @classmethod
    def _init_subparsers(cls, parser: ArgumentParser):
        commands_groups = cls._subparsers.keys()

        for group in commands_groups:
            subparsers = parser.add_subparsers(title=group)
            for cmd in cls._subparsers[group]:
                cmd.init_parser(subparsers)

    def init_parser(self, subparsers: _SubParsersAction):
        command_parser = super().init_parser(subparsers)
        self._init_subparsers(command_parser)
        return command_parser


__all__ = [
    "HasSubparsers",
]
