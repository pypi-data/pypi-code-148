

def add_verbose(subparser):
    subparser.add_argument(
        '--verbose', action='store_true',
        help='set the verbosity of the output')
