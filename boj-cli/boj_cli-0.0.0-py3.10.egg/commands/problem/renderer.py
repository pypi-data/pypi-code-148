from rich.console import Console

from connect.utils.terminal.markdown.renderer import GFMarkdown
from connect.utils.terminal.markdown.theme import ConnectTheme


def render(markup, theme=None, code_theme='ansi_light', width=None):
    markdown = GFMarkdown(markup, code_theme=code_theme)
    console = Console(theme=theme or CustomTheme(), width=width)
    with console.capture() as capturer:
        console.print(markdown)
    return capturer.get()


class CustomTheme(ConnectTheme):
    def __init__(self, styles=None, inherit=True):
        _styles = {
            'markdown.strong': 'bold bright_white',
            'markdown.emph': 'italic bright_white',
            'markdown.s': 'strike red',
            'markdown.code_inline': 'bright_white on black',
            'markdown.table.border': 'blue',
            'markdown.table.header': 'deep_sky_blue1',
            'markdown.h1': 'bold yellow',
            'markdown.h2': 'deep_sky_blue3',
            'markdown.h3': 'deep_sky_blue1',
            'markdown.h4': 'turquoise2',
            'markdown.h5': 'cornflower_blue',
            'markdown.h6': 'steel_blue1',
        }
        if styles is not None:
            _styles.update(styles)

        super().__init__(styles=_styles, inherit=inherit)
