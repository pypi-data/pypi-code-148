# manuscriptify
# Compile google docs into a manuscript
# Copyright (c) 2022 Manuscriptify
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
file generator

"""
from manuscriptify.parser import Parser
from manuscriptify.formatter import Formatter
from manuscriptify.filetree import FOLDER_MIME, FileTree
from manuscriptify.functions import progress_bar
from manuscriptify.google_api.clients import Clients

TEMPLATE = '1CRtUdlrV7PZ2OwTDIBZtOKhMHT-nRHCjkaD6Q4lUFkU'


class Outfile:
    """the outfile generator"""

    def __init__(self, creds=None, **kwargs):
        """compose a google doc out of the assembled content"""
        self.creds = creds
        docs, drive = Clients(creds).values()
        self.drive = drive
        self.kwargs = kwargs
        doc_id = self._create_from_template()
        kwargs_ = {
            'documentId': doc_id
        }
        doc = docs.documents().get(**kwargs_).execute()
        style = doc['documentStyle']
        kwargs['header_id'] = style['defaultHeaderId']
        requests = Parser(**kwargs)
        progress_bar(45)
        kwargs_['body'] = {
            'requests': requests
        }
        try:
            docs.documents().batchUpdate(**kwargs_).execute()
        except:
            kwargs_ = {
                'fileId': doc_id
            }
            drive.files().delete(**kwargs_).execute()
            raise
        kwargs = {
            'header_id': style['firstPageHeaderId'],
            'wc': requests.wc
        }
        kwargs_['body'] = {
            'requests': self._wc(**kwargs)
        }
        docs.documents().batchUpdate(**kwargs_).execute()
        target = (
            'workshop drafts' if
            self.kwargs.get('workshop')
            else 'manuscripts'
        )
        o_id = self._get_outfolder(target)
        kwargs = {
            'fileId': doc_id,
            'addParents': o_id,
            'body': {'name': self.kwargs['title']}
        }
        drive.files().update(**kwargs).execute()

    def _create_from_template(self):
        """copy the empty template document"""
        kwargs = {
            'fileId': TEMPLATE
        }
        file = self.drive.files().copy(**kwargs).execute()
        return file['id']

    @staticmethod
    def _wc(**kwargs):
        """add the word count header"""
        end_index = len(f'{kwargs["wc"]:,}') + 12
        header = [{
            'insertText': {
                'location': {
                    'segmentId': kwargs['header_id'],
                    'index': 0
                },
                'text': (f'Word count: {kwargs["wc"]:,}')
            }
        }]
        range_ = {
            'startIndex': 0,
            'endIndex': end_index,
            'segmentId': kwargs['header_id']
        }
        ts = Formatter.matter()
        header.append({
            'updateTextStyle': {
                'range': range_,
                'textStyle': ts,
                'fields': ','.join(ts.keys())
            }
        })
        st = Formatter.right()
        header.append({
            'updateParagraphStyle': {
                'range': range_,
                'paragraphStyle': st,
                'fields': ','.join(st.keys())
            }
        })
        return header

    def _get_outfolder(self, target):
        """get the folder we want to put stuff in"""
        pid = self._get_project_folder_id()
        queries = [
            f"mimeType = '{FOLDER_MIME}'",
            f"name = '{target}'",
            f"'{pid}' in parents",
            'trashed = false'
        ]
        kwargs = {
            'q': ' and '.join(queries),
            'pageSize': 1,
            'fields': 'files(id)'
        }
        results = self.drive.files().list(**kwargs).execute()
        if results['files']:
            f = results['files'][0]
        else:
            kwargs = {
                'body': {
                    'name': target,
                    'mimeType': FOLDER_MIME
                },
                'fields': 'id'
            }
            f = self.drive.files().create(**kwargs).execute()
            kwargs = {
                'fileId': f['id'],
                'addParents': pid
            }
            self.drive.files().update(**kwargs).execute()
        return f['id']

    def _get_project_folder_id(self):
        """get the project folder id"""
        project_folder = self.kwargs['project_folder']
        writing_id = FileTree(self.creds).writing(project_folder)
        kwargs_ = {
            'fileId': writing_id,
            'fields': 'parents'
        }
        writing = self.drive.files().get(**kwargs_).execute()
        return writing['parents'][0]
