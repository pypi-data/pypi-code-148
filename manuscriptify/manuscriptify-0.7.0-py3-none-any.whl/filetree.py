# manuscriptify
# Compile google docs into a manuscript
# Copyright (c) 2022 Manuscriptify
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
fragment assembler

"""
from bisect import bisect, bisect_left

from manuscriptify.exceptions import InconvenientResults
from manuscriptify.exceptions import SortKeyError
from manuscriptify.google_api.clients import Clients

FIELDS = 'id, name, description, parents, mimeType'
FOLDER_MIME = 'application/vnd.google-apps.folder'

drive = Clients()['drive']


class FileTree(tuple):
    """all the relevant files, in their proper order"""

    def __new__(cls, project_folder, filter_=''):
        writing_folder = cls.writing(project_folder)
        folder_tree = cls._expand(writing_folder)
        files = cls._files(folder_tree)
        if filter_:
            files = cls._filter(files, filter_)
        return tuple(files)

    @classmethod
    def writing(cls, project_folder):
        """get source folder"""
        all_folders = cls._all_folders()
        project_folders = [
            f['id'] for f in all_folders if
            f['name'] == project_folder
        ]
        writing_folders = [
            f['id'] for f in all_folders if
            f['name'] == 'writing' and
            any(p in f['parents'] for
                p in project_folders)
        ]
        if len(writing_folders) == 1:
            return writing_folders[0]
        else:
            raise InconvenientResults(writing_folders)

    @classmethod
    def _all_folders(cls):
        """get all folders in drive"""
        mime_type = FOLDER_MIME
        queries = [
            f"mimeType = '{mime_type}'",
            "'me' in owners",
            'trashed = false'
        ]
        kwargs = {
            'api_method': drive.files().list,
            'q': ' and '.join(queries),
            'pageSize': 100,
            'fields': f'nextPageToken, files({FIELDS})'
        }
        return cls.get_all_results(**kwargs)

    @classmethod
    def _expand(cls, writing_folder):
        """get folders in source tree"""
        parents = [writing_folder]
        all_folders = cls._all_folders()
        descendants = []
        while True:
            next_gen = [
                f['id'] for f in all_folders if
                any(a in f['parents'] for
                    a in parents)
            ]
            if not next_gen:
                break
            descendants.extend(next_gen)
            parents = next_gen
        return [writing_folder] + descendants

    @classmethod
    def _files(cls, folder_tree):
        """get files in folder tree"""
        query = [f"'{folder_id}' in parents"
                 for folder_id in folder_tree]
        queries = [
            f"({' or '.join(query)})",
            'trashed = false'
        ]
        kwargs = {
            'api_method': drive.files().list,
            'q': ' and '.join(queries),
            'pageSize': 100,
            'fields': f'nextPageToken, files({FIELDS})'
        }
        results = cls.get_all_results(**kwargs)
        prioritized = cls._prioritize(results)
        try:
            files = sorted(prioritized, key=cls.sort_key)
        except (ValueError, KeyError):
            raise SortKeyError(prioritized)
        return files

    @staticmethod
    def get_all_results(api_method, list_key='files', **kwargs):
        """chain paginated results"""
        all_results = []
        page_token = None
        while True:
            if page_token:
                kwargs['pageToken'] = page_token
            results = api_method(**kwargs).execute()
            all_results.extend(results[list_key])
            if 'nextPageToken' not in all_results:
                break
            page_token = results['nextPageToken']
        return all_results

    @staticmethod
    def _prioritize(results):
        """add ancestor priorities"""
        for i, result in enumerate(results):
            while True:
                parents = [r for r in results if
                           r['id'] in result['parents']]
                if not parents:
                    break
                priorities = [
                    parents[0]['description'],
                    results[i]['description']
                ]
                results[i]['description'] = '.'.join(priorities)
                result = parents[0]
        return results

    @staticmethod
    def sort_key(x):
        """deweyify the description field"""
        version_key = [
            int(u) for u in
            x['description'].split('.')
        ]
        return version_key

    @classmethod
    def _filter(cls, files, filter_):
        """get subset of files for workshopping"""
        results = []
        for range_ in filter_.split(','):
            bounds = range_.split('-')
            if len(bounds) == 1:
                bounds += bounds
            lower, upper = [
                list(map(int, x)) for x in
                [b.split('.') for b in bounds]
            ]
            i = bisect_left(files, lower, key=cls.sort_key)
            j = bisect(files, upper + [99], key=cls.sort_key)
            if len(lower) > 1:
                chapter_frag = next(
                    f for f in files if
                    f['description'] == str(lower[0])
                )
                chapter_frag['name'] += '~~'
                results.append(chapter_frag)
            results += files[i:j]
        return results
