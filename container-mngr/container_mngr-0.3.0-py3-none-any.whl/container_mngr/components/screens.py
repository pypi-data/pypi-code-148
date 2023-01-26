from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Footer
from .runtime import RuntimePanel
from .containers import ContainersPanel
from .images import ImagesPanel


class BaseScreen(Screen):
    def compose(self) -> ComposeResult:
        for widget in self.compose_screen():
            yield widget

        yield Footer()

    def compose_screen(self) -> ComposeResult:
        return []


class RuntimeScreen(BaseScreen):
    def compose_screen(self) -> ComposeResult:
        yield RuntimePanel()


class ImagesScreen(BaseScreen):
    _panel: ImagesPanel
    BINDINGS = [("down", "move_down", "Move down"), ("up", "move_up", "Move up")]

    def compose_screen(self) -> ComposeResult:
        self._panel = ImagesPanel()
        yield self._panel

    def action_move_down(self) -> None:
        self._panel.action_move_down()

    def action_move_up(self) -> None:
        self._panel.action_move_up()


class ContainersScreen(BaseScreen):
    _panel: ContainersPanel
    BINDINGS = [("down", "move_down", "Move down"), ("up", "move_up", "Move up")]

    def compose_screen(self) -> ComposeResult:
        self._panel = ContainersPanel()
        yield self._panel

    def action_move_down(self) -> None:
        self._panel.action_move_down()

    def action_move_up(self) -> None:
        self._panel.action_move_up()
