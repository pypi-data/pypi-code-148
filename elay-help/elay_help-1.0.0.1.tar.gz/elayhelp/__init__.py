import shutil

def printc(text):
    print(*[x.center(shutil.get_terminal_size().columns) for x in text.split("\n")],sep="\n")