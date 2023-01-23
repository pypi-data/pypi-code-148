from ..v1 import MyArgumentParser

class Parser:
    def __init__(self, parser=None):
        if parser is not None:
            self.parser = parser
        else:
            self.parser = MyArgumentParser()

    def __str__(self):
        return f"Parser: {self.__dict__}"
    
    def create_parser(self, description=None):
        self.parser = MyArgumentParser(add_help=True, description=description)
        return self

    def add_argument(self, *args, **kwargs):
        #print(args)
        #print(*args)
        #print(kwargs)
        #print(*kwargs)
        self.parser.add_argument(*args, **kwargs)
        return self

    def parse_args(self, args=None):
        self.parser.parse_args(args)
        return self

    def get_parsed_args(self):
        return self.parser.get_parsed_args()

    @staticmethod
    def new_parser(parser=None):
        return Parser(parser)

    class Factory():
        @staticmethod
        def new_parser(parser=None):
            return Parser(parser)

    factory = Factory()