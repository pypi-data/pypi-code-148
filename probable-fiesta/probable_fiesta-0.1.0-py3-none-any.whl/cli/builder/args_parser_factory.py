from .parser_builder import ParserBuilder

class ArgsParserFactory:
    """Factory for creating an args parser."""
    def __init__(self):
        pass

    def new(self, *args, **kwargs):
        pB = ParserBuilder()

        parser = pB.parser.create_new_args_parser()

        parser.add_argument(*args, **kwargs)

        parser.build()

        return parser.get_args_parser()
