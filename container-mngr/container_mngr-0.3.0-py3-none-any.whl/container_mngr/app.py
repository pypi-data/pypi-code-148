from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer
from .components.screens import RuntimeScreen, ContainersScreen, ImagesScreen


class ContainerMngrApp(App):
    CSS_PATH = "container_mngr_app.css"
    TITLE = "Container Manager"
    BINDINGS = [
        ("f1", "app.switch_screen('containers')", "Containers"),
        ("f2", "app.switch_screen('images')", "Images"),
        ("f3", "app.switch_screen('runtime')", "Runtime Info"),
        ("ctrl+r", "run_container", "Run container"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
    ]
    SCREENS = {
        "runtime": RuntimeScreen,
        "images": ImagesScreen,
        "containers": ContainersScreen,
    }

    def compose(self) -> ComposeResult:
        yield Footer()

    async def on_mount(self) -> None:
        await self.push_screen("containers")
