from rich import print
from rich.console import group
from rich.panel import Panel

@group()
def get_panels():
    yield Panel("Hello")
    yield Panel("World")

print(Panel(get_panels()))
