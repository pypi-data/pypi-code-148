from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.columns import Columns

from textual.app import App
from textual import events
from textual.widgets import Placeholder, Header, Footer, ScrollView


class SimpleApp(App):

    async def on_load(self, event: events.Load) -> None:
        await self.bind("q", "quit", "Quit")

    async def on_mount(self, event: events.Mount) -> None:
        self.body = body = ScrollView()
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(body)

        async def add_content():
            layout = Layout()
            layout.split_row(
                    Layout(name="BACKLOG"),
                    Layout(name="TODO"),
                    Layout(name="IN_PROGRESS"),
                    Layout(name="REVIEW"),
                    Layout(name="DONE"),
            )
            layout["BACKLOG"].split_column(
            Layout(Panel("Task_1", subtitle="project_1", height=10)),
                    Layout(Panel("Task_2", height=10))
            )
            print(layout)
            await body.update(layout)

            # table = Table(title="Tasks", expand=True)

            # for i in ("BACKLOG", "TODO", "IN_PROGRESS", "REVIEW", "DONE"):
            #     table.add_column(i, style="magenta")
            # await body.update(table)

            # for i in range(10):
            #     table.add_row(*[f"task {i},{j}" for j in range(5)])

        await self.call_later(add_content)

        # async def get_markdown() -> None:
        #     await body.update("Hello, this is an update version of my new project")

        # await self.call_later(get_markdown)


SimpleApp.run(title="Terminal Kanban")
