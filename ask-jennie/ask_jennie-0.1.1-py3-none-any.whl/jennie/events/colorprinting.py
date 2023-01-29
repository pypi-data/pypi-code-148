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

class ColorPrinting():
    def error(self, message):
        print(bcolors.FAIL + str(message) + bcolors.ENDC)

    def warning(self, message):
        print(bcolors.WARNING + str(message) + bcolors.ENDC)

    def success(self, message):
        print(bcolors.OKGREEN + str(message) + bcolors.ENDC)

    def info(self, message):
        print(bcolors.OKBLUE + str(message) + bcolors.ENDC)