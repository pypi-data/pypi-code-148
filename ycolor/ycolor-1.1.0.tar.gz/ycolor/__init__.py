'''A convenient color text printing tool
You can print color text in three ways:
printcolor(mess,end='\n',fore=Fore.WHITE,back=Back.BLACK)
printcolor_text(mess,end='\n',color='WHITE+BLACK')
printcolor_int(mess,end='\n',color=0x0f)'''

import ctypes as _ctypes
import sys as _sys

_handle = _ctypes.windll.kernel32.GetStdHandle(-11)

class ColorError(Exception):
    pass

class Back():
    DARK_BLUE = 0x10 # dark blue
    DARK_GREEN = 0x20 # dark green
    DARK_SKYBLUE = 0x30 # dark skyblue
    DARK_RED = 0x40 # dark red
    DARK_PINK = 0x50 # dark pink
    DARK_YELLOW = 0x60 # dark yellow
    DARK_WHITE = 0x70 # dark white
    DARK_GRAY = 0x80 # dark gray
    BLACK = 0x00 #black
    BLUE = 0x90 # blue
    GREEN = 0xa0 # green
    SKYBLUE = 0xb0 # skyblue
    RED = 0xc0 # red
    PINK = 0xd0 # pink
    YELLOW = 0xe0 # yellow
    WHITE = 0xf0 # white

class Fore():
    BLACK = 0x00 # black
    DARK_BLUE = 0x01 # dark blue
    DARK_GREEN = 0x02 # dark green
    DARK_SKYBLUE = 0x03 # dark skyblue
    DARK_RED = 0x04 # dark red
    DARK_PINK = 0x05 # dark pink
    DARK_YELLOW = 0x06 # dark yellow
    DARK_WHITE = 0x07 # dark white
    DARK_GRAY = 0x08 # dark gray
    BLUE = 0x09 # blue
    GREEN = 0x0a # green
    SKYBLUE = 0x0b # skyblue
    RED = 0x0c # red
    PINK = 0x0d # pink
    YELLOW = 0x0e # yellow
    WHITE = 0x0f # white


def printcolor(mess,end='\n',fore=Fore.WHITE,back=Back.BLACK):
    '''Print colored text'''
    printcolor_int(mess,end=end,color=fore|back)

def printcolor_text(mess,end='\n',color='WHITE+BLACK'):
    '''Print colored text in the format of "Fore+Back"
You can also choose not to enter Fore or (and) Back'''
    place = color.find('+')
    if place == -1:
        raise ColorError("You should type'Fore+Back")
    fore = color[:place]
    back = color[place+1:]
    fore = _printcolor_text_help(fore,'Fore',Fore.WHITE)
    back = _printcolor_text_help(back,'Back',Back.BLACK)
    printcolor(mess,end=end,fore=fore,back=back)

def _printcolor_text_help(what,whattext,whatelse):
    error = ()
    if what == '':
        whatreturn = whatelse
    else:
        try:
            whatreturn = eval(f'{whattext}.{what}')
        except Exception:
            error = (whattext,what)
    if not error:
        return whatreturn

    else:
        raise ColorError(f"{error[0]} don't have color {error[1]}")

def printcolor_int(mess,end='\n',color=0x0f):
    '''Use digital to print colored text like 0x0f'''
    try:
        _ctypes.windll.kernel32.SetConsoleTextAttribute(_handle, color)
        _sys.stdout.write(mess)
        _ctypes.windll.kernel32.SetConsoleTextAttribute(_handle, 0x0f)
        _sys.stdout.write(end)
    except Exception:
        pass
    
if __name__ == '__main__':
    printcolor('hello')
    printcolor('hello',fore=Fore.RED,back=Back.DARK_GRAY)
    printcolor_text('hello',color='RED+DARK_GRAY')
    printcolor_int('hello',color=0xfc)
