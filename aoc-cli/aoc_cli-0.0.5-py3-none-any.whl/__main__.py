import argparse
from pathlib import Path
from importlib.metadata import entry_points

from dotenv import load_dotenv

from .utils import get_default_year, guess_language


def parse_args(languages: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    init_parser = subparsers.add_parser('init', help='Initialise an advent of code project/folder.')
    
    init_parser.add_argument('location', type=str, help="where to scaffold project.", default=".")
    init_parser.add_argument('--year', type=int, default=get_default_year())
    init_parser.add_argument('--language', choices=languages, default='python')

    get_parser = subparsers.add_parser('get', help="Get input file, requires AOC_SESSION environment variable.")
    get_parser.add_argument('--location', type=str, help="Which input to download and where", default=".")
    
    run_parser = subparsers.add_parser('run', help="execute a part processor in the current directory.")
    run_parser.add_argument('part', type=int, choices=(1,2))

    submit_parser = subparsers.add_parser('submit', help="Submit an answer, requires AOC_SESSION environment variable.")
    submit_parser.add_argument('part', type=int, choices=(1,2))

    open_parser = subparsers.add_parser('open', help="Open a webbrowser to the day in question.")

    

    return parser.parse_args()


def is_init_valid(args) -> bool:
    max_year = get_default_year()
    if args.year < 2015 or args.year > max_year:
        raise ValueError(f"Year must be between 2015 and {max_year} (inclusive).")

    return True

def load_plugins():
    plugins = entry_points(group="aoc_cli.plugins")
    return [plugin.load() for plugin in plugins]


def select_plugin(plugins, language):
    try:
        return [p for p in plugins if hasattr(p, "__language__") and p.__language__ == language][0]
    except IndexError:
        raise ValueError(f"No plugin found for {language}.")


def handle_init(plugins, year: int, language: str, location: Path) -> None:
    """Given {year}, {language} and {location}, scaffolds out a project
    in accordance with the Initialiser class of the respective {language} plugin.

    Args:
        year (int): _description_
        language (str): _description_
        location (Path): _description_
    """
    plugin = select_plugin(plugins, language)
    i = plugin.Initialiser(year, location)
    i.initialise()

    
def handle_get(plugin, location: Path=None) -> None:
    """Derives year and day from {location}, downloads input to {location}/input.txt

    Args:
        location (Path): Directory
    """
    g = plugin.Getter(location)
    g.get_input()

def handle_run(plugin, part: int) -> None:
    r = plugin.Runner(part)
    r.run()


def handle_submit(plugin, part: int) -> None:
    s = plugin.Submitter(part)   
    s.submit()


def handle_open(plugin) -> None:
    o = plugin.Opener()
    o.open()


def main() -> None:
    load_dotenv()
    plugins = load_plugins()
    available_scaffolders = [p.__language__ for p in plugins if hasattr(p, "__language__")]
    args = parse_args(languages=available_scaffolders)
    
    if hasattr(args, "location"):
        location = Path(args.location)
    else:
        location = Path()
    

    if args.command == "init":
        print(plugins)
        handle_init(plugins=plugins, year=args.year, language=args.language, location=location)
    else:
        # The following commands are all location aware which means their handlers need to
        # know a) their path, and then b) their handler (language/interpreter)
        try:
            language = guess_language(plugins, location)
            plugin = select_plugin(plugins=plugins, language=language)
            if args.command == "get":
                handle_get(plugin=plugin, location=location)
            elif args.command == "run":
                handle_run(plugin=plugin, part=args.part, location=location)
            elif args.command == "submit":
                handle_submit(plugin=plugin, part=args.part, location=location)
            elif args.command == "open":
                handle_open(plugin=plugin, location=location)

            else:
                raise ValueError(f"Invalid command {args.command} supplied.")
        except ValueError:
            print(f"Unable to run {args.command}, ValueError raised.")
            raise
        

if __name__ == "__main__":
    main()