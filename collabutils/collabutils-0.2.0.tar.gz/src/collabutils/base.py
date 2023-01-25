import typing
import pathlib


class SharedSpreadsheetMixin:
    def fetch_sheets(
            self,
            sheets: typing.Optional[typing.Dict[str, str]] = None,
            outdir: typing.Optional[typing.Union[pathlib.Path, str]] = '.',
            **kw,
    ):
        raise NotImplementedError()  # pragma: no cover
