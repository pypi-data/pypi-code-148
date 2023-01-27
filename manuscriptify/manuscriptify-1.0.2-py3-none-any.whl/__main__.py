# manuscriptify
# Compile google docs into a manuscript
# Copyright (c) 2022 Manuscriptify
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
main app logic

"""
from itertools import chain

from googleapiclient.errors import HttpError

from manuscriptify.filetree import FileTree
from manuscriptify.fragment import Fragment
from manuscriptify.chapter import Chapter
from manuscriptify.outfile import Outfile
from manuscriptify.functions import run_with_shell_args
from manuscriptify.functions import fragify_string
from manuscriptify.functions import progress_bar
from manuscriptify.functions import is_chapter
from manuscriptify.exceptions import InconvenientResults
from manuscriptify.exceptions import SortKeyError

FILE_MIME = 'application/vnd.google-apps.document'


@run_with_shell_args
def manuscriptify(**kwargs):
    args = [
        kwargs['project_folder'],
        kwargs['workshop']
    ]
    try:
        progress_bar(0)
        filetree = FileTree().tree(*args)
        progress_bar(10)
        fragments = []
        ch_depth = kwargs['chapter_depth']
        chapters = ch_depth > 0
        if not chapters:
            markup = f'Chapter 0:{kwargs["title"]}%%'
            title = fragify_string(markup)
            fragments.append(title)
        for f in filetree:
            try:
                if chapters and is_chapter(f, ch_depth):
                    chapter_logline = Chapter(f)
                    fragments.append(chapter_logline)
            except KeyError:

                # single file use case
                pass

            if f['mimeType'] == FILE_MIME:
                fragment = Fragment(f['id'])
                fragments.append(fragment)
        progress_bar(35)
        kwargs['content'] = list(chain(*fragments))
        Outfile(**kwargs)
        progress_bar(100)
        print(kwargs['title'], 'compiled successfully')
    except AttributeError as e:
        app_errors = [InconvenientResults]
        if type(e) in app_errors:
            pass
        else:
            raise
    except HttpError as e:
        print(e)
        raise


manuscriptify('dummy_arg')
