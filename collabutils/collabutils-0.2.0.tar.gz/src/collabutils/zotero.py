"""
Zotero provides a good platform to collaborate on bibliogrpahies.

We support collaborative curation of bibliographical data as follows:

- The data is curated in a shared Zotero library.
- Items in this library are tagged for membership in the bibliographies of certain datasets, \
  using tags of the form "dataset:<dataset-id>".
- Items are optionally tagged with tags of the form "id:<dataset-id>:<local-id>" for local \
  BibTeX keys in a specific dataset.

An instance of :class:`Zotero` allows

- seeding such libraries from a (possibly stub) BibTeX file via :meth:`Zotero.upload_bib`
- downloading such libraries via :meth:`Zotero.download_bib`
- deleting such libraries via :meth:`Zotero.delete_bib`
"""
import re
import copy
import pathlib
import collections

from pycldf.sources import Source

from collabutils.util import warn
try:
    from pybtex.database import parse_string
    from pyzotero.zotero import Zotero as API
except ImportError as e:  # pragma: no cover
    warn('zotero.Zotero', 'zotero', e)

__all__ = ['Zotero']

BIBTEX_TO_ZOTERO = {
    'article': 'journalArticle',
    'book': 'book',
    'booklet': 'book',
    'conference': 'conferencePaper',
    'inbook': 'bookSection',
    'incollection': 'bookSection',
    'inproceeding': 'conferencePaper',
    # manual
    'mastersthesis': 'thesis',
    'misc': 'document',
    'phdthesis': 'thesis',  # + thesisType! 'PhD thesis' or 'masters thesis'
    # proceeding
    'techreport': 'report',
    'unpublished': 'manuscript',
    # BibLaTeX
    # mvbook
    # bookinbook
    # suppbook
    # booklet
    # collection
    # mvcollection
    # incollection
    # suppcollection
    # online
    # patent
    # periodical
    # suppperiodical
    # mvproceedings
    # reference
    # mvreference
    # inreference
    # report
    # set
    'thesis': 'thesis',
    # custom
    # electronic
}

FIELDS_TO_ZOTERO = {
    'address': 'place',
    # 'author -> creators
    'booktitle': 'bookTitle',
    'doi': 'DOI',
    # 'editor -> creators
    'journal': 'publicationTitle',
    'school': 'institution',
    'year': 'date',
    'abstract': 'abstractNote',
}


class Zotero:
    """
    A high-level Zotero API client. Low level communication with Zotero is done using the
    `pyzotero` package.

    .. seealso:: `<https://pypi.org/project/Pyzotero/>`_
    """
    def __init__(self, libid, apikey, group=True):
        """
        :param libid: Numeric ID of the Zotero library
        :param apikey: API key with read/write permissions for the library
        :param group: Flag signaling whether we are dealing with a group or user library
        """
        self.api = API(libid, 'group' if group else 'user', apikey)
        self._item_templates = {}

    @staticmethod
    def id_tag(dataset_id, bibkey):
        return 'id:{}:{}'.format(dataset_id, bibkey)

    @staticmethod
    def id_from_tagstring(s, dataset_id):
        m = re.search(r'id:{}:(?P<id>[^\s,]+)'.format(re.escape(dataset_id)), s)
        if m:
            return m.group('id')

    @staticmethod
    def dataset_tag(dataset_id):
        return 'dataset:{}'.format(dataset_id)

    def upload_bib(self, dataset_id, bibpath, log=None):
        """
        Upload items from a BibTeX file as items of the Zotero library for a dataset.

        :param dataset_id: Dataset identifier (e.g. a `cldfbench.Dataset.id`).
        :param bibpath: Path to the BibTeX file to be uploaded.
        :param log:
        :return:
        """
        res = collections.OrderedDict()
        db = parse_string(pathlib.Path(bibpath).read_text(encoding='utf8'), 'bibtex')
        for key, entry in db.entries.items():
            src = Source.from_entry(key, entry)
            tag = self.id_tag(dataset_id, src.id)
            try:
                _ = self.api.items(tag=tag, limit=1)[0]
                if log:  # pragma: no cover
                    log.info('Skipping {}'.format(tag))
                res[src.id] = True
            except IndexError:
                res[src.id] = self.create_item(src, tag, self.dataset_tag(dataset_id))
        return res

    def download_bib(self, dataset_id, bibpath=None, remove=None):
        """
        Download all items tagged for a dataset into a BibTeX file.

        :param dataset_id:
        :param bibpath:
        :param remove: List of field names to remove (e.g. the "keywords" field, which is popuated \
        by Zotero's BibTeX export with all tags) or `None`.
        :return:
        """
        remove = remove or []
        bib = []
        for item in self.get_items(self.dataset_tag(dataset_id), content='bibtex'):
            src = self._bibtex2source(item)
            # determine the dataset-local bibkey:
            id_ = self.id_from_tagstring(src.get('keywords', ''), dataset_id)
            if id_:
                src.id = id_
            for k in remove:
                if k in src:
                    del src[k]
            bib.append(src.bibtex())
        bib = '\n\n'.join(bib)
        if bibpath:
            pass
        return bib

    def delete_bib(self, dataset_id, log=None):
        """
        Delete all items tagged for a dataset - unless they are tagged for other datasets as well.

        :param dataset_id:
        :param log:
        :return:
        """
        for item in self.get_items(self.dataset_tag(dataset_id)):
            if any(':' + dataset_id not in t['tag'] for t in item['data']['tags']):
                if log:
                    log.warning('Skipping item linked to other datasets')
                continue
            self.api.delete_item(item)

    def get_items(self, tag, **kw):
        return self.api.everything(self.api.items(tag=tag, **kw))

    @staticmethod
    def _bibtex2source(bibtex):
        src = Source.from_entry(*list(parse_string(bibtex, 'bibtex').entries.items())[0])

        def repl(m):
            if m.group('cat') == 'type':
                src.genre = m.group('value').strip()
            else:
                field, value = m.group('value').split(':', maxsplit=1)
                if field == 'note':
                    return value.strip()
                src[field] = value.strip()
            return ''

        if 'note' in src:
            note = re.sub(
                ':bibtex:(?P<cat>type|field):(?P<value>.+?):xetbib:', repl, src['note']).strip()
            if note:
                src['note'] = note
            else:
                del src['note']
        return src

    def _empty_item(self, src):
        zot_genre = BIBTEX_TO_ZOTERO.get(src.genre.lower(), 'document')
        if zot_genre not in self._item_templates:
            self._item_templates[zot_genre] = self.api.item_template(zot_genre)
        return copy.deepcopy(self._item_templates[zot_genre])

    def create_item(self, src, *tags):
        """
        """
        item = self._empty_item(src)

        extra = {'type': src.genre}
        for k, v in src.items():
            kl = k.lower()
            if kl in ['editor', 'author']:
                continue
            zotk = FIELDS_TO_ZOTERO.get(kl, kl)
            if zotk in item and isinstance(item[zotk], str):
                item[zotk] = src[k]
            else:
                extra['field:{}'.format(kl)] = src[k]

        if extra:
            item['extra'] = '\n'.join(
                [':bibtex:{}: {}:xetbib:'.format(k, v) for k, v in extra.items()])

        entry = src.entry
        item['creators'] = []
        for ct in ['author', 'editor']:
            for name in entry.persons[ct]:
                item['creators'].append(dict(
                    creatorType=ct,
                    firstName=str(name).split(',')[-1].strip(),
                    lastName=str(name).split(',')[0]))
        item['tags'].extend(tags)
        item['tags'] = [dict(tag=t) for t in item['tags']]
        return bool(self.api.create_items([item])['success'])
