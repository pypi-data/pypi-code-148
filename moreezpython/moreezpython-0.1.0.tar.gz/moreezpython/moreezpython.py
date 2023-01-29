import os
import time

class color:
    #Color
    GRAY = '\033[38;5;247m'
    WHITE = '\033[97m'
    # Blue
    CYAN = '\033[38;5;45m'
    BLUE = '\033[38;5;32m'
    B_BLUE = '\033[38;5;17m'
    L_BLUE = '\033[96m'
    # Green
    L_GREEN = '\033[38;5;83m'
    GREEN = '\033[38;5;46m'
    B_GREEN = '\033[38;5;28m'
    # Purple
    MAGENTA = '\033[35m'
    PURPLE = '\033[38;5;63m'
    L_PURPLE = '\033[38;5;105m'
    B_PURPLE = '\033[38;5;55m'
    # Red
    L_RED = '\033[38;5;1m'
    RED = '\033[38;5;160m'
    B_RED = '\033[38;5;52m'
    # Yellow
    L_YELLOW = '\033[38;5;222m'
    YELLOW = '\033[38;5;220m'
    B_YELLOW = '\033[38;5;214m'
    GOLD = '\033[38;5;136m'

    #Debug Color
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function Log
def log(args):
    print(f"{color.GREEN}{args}{color.END}")

# Function help
def help():
    textcolor = 'f"{color.<colorname>}"'
    textcolorexemple = 'f"{color.CYAN}"'
    print(f"\n{color.CYAN}{color.UNDERLINE}Here are the commands available{color.END}{color.CYAN}\n\n- Log (usage : log(args); example : log('Hello, World')\n- Count (usage : count(args, print); example : count(5, False)\n- Stop (usage : stop())\n- nostop (usage : nostop())\n- color (usage : {textcolor}; exemple : {textcolorexemple}){color.END}")

# Function stop
def stop():
    exit(f"\n{color.WARNING}Exit by Command{color.END}")

# Function nostop
def nostop():
    input()

# Function count
def count(number, write):
    if not isinstance(number, int):
        exit(f"{color.FAIL}Error, you need to put one int in args in the function count {color.END}")

    if write == "True":
        for i in range(number):
            i = i + 1
            print(i)
            time.sleep(0.1)
    elif write == "False":
        for i in range(number):
            i = i + 1
            time.sleep(0.1)
    elif write == "true":
        for i in range(number):
            i = i + 1
            write(i)
            time.sleep(0.1)
    elif write == "false":
        for i in range(number):
            i = i + 1
            time.sleep(0.1)
    else:
        exit(f"{color.FAIL}Error, You don't write True or False in the function count (usage: mep.count(<number>,<True or False>) {color.END}")