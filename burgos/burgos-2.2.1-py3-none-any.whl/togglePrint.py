import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def togglePrint(mode:bool):
    if mode:
        enablePrint()
    else:
        blockPrint()

def nastyPrint(string:str):
    togglePrint(True)
    print(string)
    togglePrint(False)