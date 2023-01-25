"""
The `EDICTOR application <http://lingulist.de/edictor/>`_ is an online tool for creating,
maintaining, and publishing etymological data which is stored in simple TSV format.
This TSV format can be accessed in a somewhat configurable way via HTTP URLs.
"""
import typing
import pathlib
import urllib.parse
from urllib.request import urlretrieve


def get_url(
        base_url="https://lingulist.de/edictor",
        path=None,
        **params
):
    params = {
        k: '|'.join(v) if isinstance(v, (list, tuple)) else v
        for k, v in params.items() if v is not None}
    url_parts = list(urllib.parse.urlparse(base_url))
    if path:
        if not url_parts[2].endswith('/') and not path.startswith('/'):
            path = '/' + path
        url_parts[2] += path
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


def fetch(
        dataset: str,
        remote_dbase: typing.Optional[str] = None,
        concepts: typing.Optional[typing.List[str]] = None,
        languages: typing.Optional[typing.List[str]] = None,
        columns: typing.Optional[typing.List[str]] = None,
        base_url: str = "http://lingulist.de/edictor",
        out: typing.Optional[typing.Union[pathlib.Path, str]] = None,
):
    """
    Retrieve the TSV data file for a dataset curated with EDICTOR.

    :param dataset: Name of the dataset in EDICTOR
    :param remote_dbase: Name of the database file on EDICTOR (if different than dataset name)
    :param concepts: List of concepts to include in the download (defaults to all)
    :param languages: List of languages to include in the download (defaults to all)
    :param columns: List of columns to include in the download (defaults to all)
    :param base_url:
    :param out: Path to which to save the data (defaults to './<dataset>.tsv')
    :return:
    """
    remote_dbase = remote_dbase or (dataset + '.sqlite')
    url = get_url(
        base_url=base_url,
        path='/triples/get_data.py',
        file=dataset,
        concepts=concepts,
        doculects=languages,
        columns=columns,
        remote_dbase=remote_dbase,
    )
    if out:
        out = pathlib.Path(out)
        if out.is_dir():
            out = out / '{}.tsv'.format(dataset)
    else:
        out = pathlib.Path('{}.tsv'.format(dataset))
    return urlretrieve(url, str(out))
