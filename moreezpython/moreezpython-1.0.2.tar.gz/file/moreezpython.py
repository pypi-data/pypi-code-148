import os
import time

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

def log(args):
    print(f"{bcolors.OKGREEN}{args}{bcolors.ENDC}")

def help():
    print(f"\n{bcolors.OKCYAN}Here are the commands available\n\n- Log (usage : log(args); example : log('Hello, World')\n {bcolors.ENDC}")

def stop():
    exit(f"\n{bcolors.WARNING}Exit by Command{bcolors.ENDC}")

def nostop():
    input()

def count(args):
    for i in range(args):
        i = i + 1
        print(i)
        time.sleep(0.1)