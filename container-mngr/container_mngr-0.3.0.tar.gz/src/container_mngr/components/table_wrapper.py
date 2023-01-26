from abc import ABC, abstractmethod
from textual.widgets import Static
from rich import box
from rich.console import RenderableType
from rich.table import Table
from rich.text import Text


class TableDataProvider(ABC):
    @abstractmethod
    def get_headers(self) -> list[str]:
        return []

    @abstractmethod
    def get_rows(self) -> list:
        pass


class TableWrapper(Static):
    _data_provider: TableDataProvider
    _inner_table: Table
    _cur_idx: int = -1

    def __init__(
        self,
        data_provider: TableDataProvider,
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(
            renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
        )
        self._data_provider = data_provider

    def on_mount(self) -> None:
        try:
            self._inner_table = Table(
                box=box.SIMPLE_HEAVY, show_header=True, header_style="bold bright_blue"
            )

            for header in self._data_provider.get_headers():
                self._inner_table.add_column(header)

            for row in self._data_provider.get_rows():
                self._inner_table.add_row(*row)

            self.styles.border = ("heavy", "white")
            self.styles.outline = ("round", "white")
            self.update(self._inner_table)
        except Exception as ex:
            self.update(
                Text(
                    text=f"{ex}",
                    justify="center",
                    style="bold red",
                )
            )

    def action_move_down(self) -> None:
        if self._inner_table.row_count == 0:
            return

        if self._cur_idx >= 0:
            self._remove_row_highlight(self._cur_idx)

        if self._cur_idx == (self._inner_table.row_count - 1):
            self._cur_idx = 0
        else:
            self._cur_idx += 1

        self._highlight_row(self._cur_idx)
        self.update(self._inner_table)

    def action_move_up(self) -> None:
        if self._inner_table.row_count == 0:
            return

        if self._cur_idx >= 0:
            self._remove_row_highlight(self._cur_idx)

        if self._cur_idx <= 0:
            self._cur_idx = self._inner_table.row_count - 1
        else:
            self._cur_idx -= 1

        self._highlight_row(self._cur_idx)
        self.update(self._inner_table)

    def _highlight_row(self, row_idx: int) -> None:
        self._inner_table.rows[row_idx].style = "black on white"

    def _remove_row_highlight(self, row_idx: int) -> None:
        self._inner_table.rows[row_idx].style = None
