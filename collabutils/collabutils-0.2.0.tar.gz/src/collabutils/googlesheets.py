"""
Google Sheets provides a good platform to curate tabular data collaboratively. Thus, we
can use it to work on input for CLDF datasets, such as language metadata. This module provides
functionality to pull such data from Google Sheets, suitable for inclusion in `cldfbench download`
command implementations.

We use the `gspread <https://pypi.org/project/gspread/>`_ library to interact with data in
Google Sheets. Thus, code needs access to a JSON OAuth2 key file to authenticate it.
Retrieving such a key file (and giving permissions to the corresponding service account
for particular sheets) is described at `<https://docs.gspread.org/en/latest/oauth2.html>`_.

Thus, everyone running `cldfbench download` for a dataset using Google Sheets, would need
(access to) a JSON OAuth2 key file with appropriate authorizations.
"""
import typing
import pathlib
import collections

from csvw.dsv import UnicodeWriter
from collabutils.util import warn
try:
    import gspread
except ImportError as e:  # pragma: no cover
    warn('googlesheets.Spreadsheet', 'googlesheets', e)
from collabutils.base import SharedSpreadsheetMixin

__all__ = ['Spreadsheet']


def get_service_account(keyfile=None):
    """
    https://docs.gspread.org/en/latest/oauth2.html#authentication

    :param keyfile:
    :return:
    """
    keyfile = keyfile or input('Path to Google API key file: ')
    keyfile = pathlib.Path(keyfile)
    assert keyfile.exists()
    return gspread.service_account(
        filename=str(keyfile), scopes=['https://spreadsheets.google.com/feeds'])


class Spreadsheet(SharedSpreadsheetMixin):
    """
    Typical usage in a `cldfbench.Dataset`'s `cmd_download` method:

    .. code-block:: python

        >>> document = Spreadsheet('doc-key', auth='credentials.json')
        >>> document.fetch_sheets(
        ...     sheets={'Varieties': 'languages.tsv'})
        ...     outdir=dataset.etc_dir,
        ...     delimiter='\t')
    """

    def __init__(
            self,
            key_or_url: str,
            auth: typing.Optional[typing.Union[pathlib.Path, str]] = None):
        service = get_service_account(keyfile=auth)
        if key_or_url.startswith('https://') or key_or_url.startswith('http://'):
            self.workbook = service.open_by_url(key_or_url)
        else:
            self.workbook = service.open_by_key(key_or_url)

    @property
    def sheets(self) -> typing.Dict[str, gspread.models.Spreadsheet]:
        return collections.OrderedDict([(s.title, s) for s in self.workbook.worksheets()])

    def fetch_sheets(
            self,
            sheets: typing.Optional[typing.Dict[str, str]] = None,
            outdir: typing.Optional[typing.Union[pathlib.Path, str]] = '.',
            **kw,
    ):
        """
        :param sheets: A mapping of sheet titles to filenames, specifying which sheets to save \
        in which files. If None, all sheets will be saved to files "sheet_<no>.csv".
        :param outdir:
        :param kw: Passed as kwargs into UnicodeWriter.
        """
        for i, (title, sheet) in enumerate(self.sheets.items(), start=1):
            if (title in sheets) or sheets is None:
                fname = 'sheet_{}.csv'.format(i) if sheets is None else sheets[title]
                with UnicodeWriter(pathlib.Path(outdir) / fname, **kw) as writer:
                    writer.writerows(sheet.get_all_values())
