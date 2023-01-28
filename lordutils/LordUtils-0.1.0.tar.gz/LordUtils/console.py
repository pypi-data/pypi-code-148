
from rich.console import Console
from rich.traceback import install
from rich.terminal_theme import TerminalTheme
from .decorators import callCounter
import sys

console = Console(record=True, highlight=False, force_terminal=True, soft_wrap=True)

debug_active = True

theme = TerminalTheme(
    background=(30, 30, 30),
    foreground=(255, 255, 255),
    normal=[
        (0, 0, 0),
        (128, 0, 0),
        (0, 128, 0),
        (128, 128, 0),
        (0, 0, 128),
        (128, 0, 128),
        (0, 128, 128),
        (192, 192, 192),
    ],
    bright=[
        (128, 128, 128),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 0),
        (0, 0, 255),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
    ]
)

console_input = console.input


def install_traceback():
    install(console=console, show_locals=True)  # rich traceback


@callCounter
def print_exception():
    console.print_exception(show_locals=True)


def print(*mess, style="", highlight=True):
    console.print(' '.join(mess), style=style, end="", highlight=highlight)


def println(*mess, style="", highlight=True):
    console.print(' '.join(mess), style=style, highlight=highlight)


def debug(*mess, style="", highlight=True):
    if debug_active:
        console.print(' '.join(mess), style=style, highlight=highlight)


def message(prefix, *mess, style=""):
    console.print(f"[{prefix}] " + ' '.join(mess), style=style)


@callCounter
def error(*mess, wait=False):
    console.print('[Error]', ' '.join(mess), style="red")
    if wait:
        console.input("[ENTER]")
        clear_lines(1)


@callCounter
def warning(*mess, wait=False):
    end = '\t[enter]' if wait else '\n'
    console.print("[Warning]", ' '.join(mess), style="yellow", end=end)
    if wait:
        console.input("[ENTER]")
        clear_lines(1)


def write_ending_log():
    console.print(f"[yellow]{warning.getFullCount()} - Warnings\n"
                  f"[red]{error.getFullCount()} - Error\n"
                  f"[red bold]{print_exception.getFullCount()} - ! Critical-Error !")


def clear_lines(n: int):
    for i in range(0, n):
        sys.stdout.write('\x1b[1A' + '\x1b[2K')


def save_html(path="log.html"):
    console.save_html(path, theme=theme)
