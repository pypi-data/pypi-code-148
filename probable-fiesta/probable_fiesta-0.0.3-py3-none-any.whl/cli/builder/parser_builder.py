from .args_parse import Parser

class ParserBuilder:

    def __init__(self, args_parser=None):
        if args_parser is not None:
            self.args_parser = args_parser
        else:
            self.args_parser = Parser.Factory.new_parser()

    @property
    def parser(self):
        return ParserBuilderParser(self.args_parser)
    
    def build(self):
        return self

class ParserBuilderParser(ParserBuilder):

    def __init__(self, args_parser):
        super().__init__(args_parser)

    def set_args_parser(self, args_parser):
        self.args_parser = args_parser
        return self

    def create_new_args_parser(self):
        self.args_parser = Parser.Factory.new_parser()
        return self

    def get_args_parser(self):
        return self.args_parser.parser

    def add_argument(self, *args, **kwargs):
        print(f"Adding {args} to parser: {self.args_parser}")
        self.args_parser.add_argument(*args, **kwargs)
        return self

    def parse_args(self, args=None):
        if not self.args_parser.parser:
            print("No parser found. Creating one for you")
            self.args_parser.parser = Parser.Factory.new_parser()
        return self.args_parser.parser.parse_args(args)

    def get_parsed_args(self):
        return self.args_parser.parser.get_parsed_args()