COLORS = {
    "normal": '\033[0m',
    "black": '\033[0;30m',
    "red": '\033[0;31m',
    "green": '\033[0;32m',
    "yellow": '\033[0;33m',
    "blue": '\033[0;34m',
    "purple": '\033[0;35m',
    "cyan": '\033[0;36m',
    "white": '\033[0;37m' 
}

def prettyPrint(string, color = "normal", custom = False):
    if custom:
        print(f"{COLORS[custom]}{string}{COLORS['normal']}")
    else:
        print(f"{COLORS[color]}{string}{COLORS['normal']}")

