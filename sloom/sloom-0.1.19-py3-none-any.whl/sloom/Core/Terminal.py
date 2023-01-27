

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Terminal:
    def __init__(self) -> None:
        pass

    @staticmethod
    def put(s):
        print(f"> {s}")
    
    @staticmethod
    def error(s):
        print(f"> {bcolors.FAIL}ERROR{bcolors.ENDC} - {s}")