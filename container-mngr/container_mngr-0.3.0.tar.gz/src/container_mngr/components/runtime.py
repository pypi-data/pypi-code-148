from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ..data.docker import get_runtime_info
from ..data.models import ContainerRuntimeInfo
from ..data.errors import ContainerRuntimeAPIError


class RuntimePanel(Widget):
    _property_mapping = {
        "NCPU": "CPU Count",
        "Architecture": "CPU Architecture",
        "Name": "Name",
        "ServerVersion": "Server Version",
        "KernelVersion": "Kernel Version",
        "OSType": "OS Type",
        "OperatingSystem": "Operating System",
        "OSVersion": "OS Version",
    }

    def compose(self) -> ComposeResult:
        content = self._render_content()

        yield Static(Panel(content, title="Runtime"))

    def _render_content(self):
        try:
            info = get_runtime_info()
            return self._render_runtime_info(info)
        except ContainerRuntimeAPIError as ex:
            return self._render_error(ex)

    def _render_runtime_info(self, runtime_info: ContainerRuntimeInfo):
        table = Table(
            box=None, show_header=False, expand=False, pad_edge=False, show_edge=False
        )

        self._render_table_row(table, "CPU Count", str(runtime_info.cpu_count))
        self._render_table_row(table, "Architecture", runtime_info.cpu_architecture),
        self._render_table_row(table, "Name", runtime_info.name)
        self._render_table_row(table, "Runtime Version", runtime_info.server_version)
        self._render_table_row(table, "Kernel Version", runtime_info.kernel_version)
        self._render_table_row(table, "OS Type", runtime_info.os_type)
        self._render_table_row(table, "Operating System", runtime_info.os)
        self._render_table_row(table, "OS Version", runtime_info.os_version)

        return table

    def _render_error(self, ex: ContainerRuntimeAPIError):
        return Text(
            f"Error while pulling runtime information: {ex.inner_error}",
            style="Bold Red",
        )

    def _render_table_row(self, table: Table, header: str, value: str):
        table.add_row(Text(text=header, style="bold bright_blue"), Text(text=value))
