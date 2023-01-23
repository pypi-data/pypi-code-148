# -*- coding: utf-8 -*-
#
# PyAV documentation build configuration file, created by
# sphinx-quickstart on Fri Dec  7 22:13:16 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

from docutils import nodes
import logging
import math
import os
import re
import sys
import sys
import xml.etree.ElementTree as etree

import sphinx
from sphinx import addnodes
from sphinx.util.docutils import SphinxDirective


logging.basicConfig()


if sphinx.version_info < (1, 8):
    print("Sphinx {} is too old; we require >= 1.8.".format(sphinx.__version__), file=sys.stderr)
    exit(1)


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'sphinx.ext.doctest',

    # We used to use doxylink, but we found its caching behaviour annoying, and
    # so made a minimally viable version of our own.
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'PyAV'
copyright = u'2017, Mike Boers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
about = {}
with open('../av/about.py') as fp:
    exec(fp.read(), about)

# The full version, including alpha/beta/rc tags.
release = about['__version__']

# The short X.Y version.
version = release.split('-')[0]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'pyav'
html_theme_path = [os.path.abspath(os.path.join(__file__, '..', '_themes'))]
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/logo-250.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

doctest_global_setup = '''

import errno
import os

import av
from av.datasets import fate, fate as fate_suite, curated

from tests import common
from tests.common import sandboxed as _sandboxed

def sandboxed(*args, **kwargs):
    kwargs['timed'] = True
    return _sandboxed('docs', *args, **kwargs)

_cwd = os.getcwd()
here = sandboxed('__cwd__')
try:
    os.makedirs(here)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
os.chdir(here)

video_path = curated('pexels/time-lapse-video-of-night-sky-857195.mp4')

'''

doctest_global_cleanup = '''

os.chdir(_cwd)

'''


doctest_test_doctest_blocks = ''


extlinks = {
    'ffstruct': ('http://ffmpeg.org/doxygen/trunk/struct%s.html', 'struct '),
    'issue': ('https://github.com/PyAV-Org/PyAV/issues/%s', '#'),
    'pr': ('https://github.com/PyAV-Org/PyAV/pull/%s', '#'),
    'gh-user': ('https://github.com/%s', '@'),
}

intersphinx_mapping = {
    'https://docs.python.org/3': None,
}

autodoc_member_order = 'bysource'
autodoc_default_options = {
    'undoc-members': True,
    'show-inheritance': True,
}


todo_include_todos = True


class PyInclude(SphinxDirective):

    has_content = True

    def run(self):


        source = '\n'.join(self.content)
        output = []
        def write(*content, sep=' ', end='\n'):
            output.append(sep.join(map(str, content)) + end)

        namespace = dict(write=write)
        exec(compile(source, '<docs>', 'exec'), namespace, namespace)

        output = ''.join(output).splitlines()
        self.state_machine.insert_input(output, 'blah')

        return [] #[nodes.literal('hello', repr(content))]


def load_entrypoint(name):

    parts = name.split(':')
    if len(parts) == 1:
        parts = name.rsplit('.', 1)
    mod_name, attrs = parts

    attrs = attrs.split('.')
    try:
        obj = __import__(mod_name, fromlist=['.'])
    except ImportError as e:
        print('Error while importing.', (name, mod_name, attrs, e))
        raise
    for attr in attrs:
        obj = getattr(obj, attr)
    return obj

class EnumTable(SphinxDirective):

    required_arguments = 1
    option_spec = {
        'class': lambda x: x,
    }

    def run(self):

        cls_ep = self.options.get('class')
        cls = load_entrypoint(cls_ep) if cls_ep else None

        enum = load_entrypoint(self.arguments[0])

        properties = {}

        if cls is not None:
            for name, value in vars(cls).items():
                if isinstance(value, property):
                    try:
                        item = value._enum_item
                    except AttributeError:
                        pass
                    else:
                        if isinstance(item, enum):
                            properties[item] = name

        colwidths = [15, 15, 5, 65] if cls else [15, 5, 75]
        ncols = len(colwidths)

        table = nodes.table()

        tgroup = nodes.tgroup(cols=ncols)
        table += tgroup

        for width in colwidths:
            tgroup += nodes.colspec(colwidth=width)

        thead = nodes.thead()
        tgroup += thead

        tbody = nodes.tbody()
        tgroup += tbody

        def makerow(*texts):
            row = nodes.row()
            for text in texts:
                if text is None:
                    continue
                row += nodes.entry('', nodes.paragraph('', str(text)))
            return row

        thead += makerow(
            '{} Attribute'.format(cls.__name__) if cls else None,
            '{} Name'.format(enum.__name__),
            'Flag Value',
            'Meaning in FFmpeg',
        )

        seen = set()

        for name, item in enum._by_name.items():

            if name.lower() in seen:
                continue
            seen.add(name.lower())

            try:
                attr = properties[item]
            except KeyError:
                if cls:
                    continue
                attr = None

            value = '0x{:X}'.format(item.value)

            doc = item.__doc__ or '-'

            tbody += makerow(
                attr,
                name,
                value,
                doc,
            )

        return [table]




doxylink = {}
ffmpeg_tagfile = os.path.abspath(os.path.join(__file__, '..', '_build', 'doxygen', 'tagfile.xml'))
if not os.path.exists(ffmpeg_tagfile):
    print("ERROR: Missing FFmpeg tagfile.")
    exit(1)
doxylink['ffmpeg'] = (ffmpeg_tagfile, 'https://ffmpeg.org/doxygen/trunk/')


def doxylink_create_handler(app, file_name, url_base):

    print("Finding all names in Doxygen tagfile", file_name)

    doc = etree.parse(file_name)
    root = doc.getroot()

    parent_map = {}  # ElementTree doesn't five us access to parents.
    urls = {}

    for node in root.findall('.//name/..'):

        for child in node:
            parent_map[child] = node

        kind = node.attrib['kind']
        if kind not in ('function', 'struct', 'variable'):
            continue

        name = node.find('name').text

        if kind not in ('function', ):
            parent = parent_map.get(node)
            parent_name = parent.find('name') if parent else None
            if parent_name is not None:
                name = '{}.{}'.format(parent_name.text, name)

        filenode = node.find('filename')
        if filenode is not None:
            url = filenode.text
        else:
            url = '{}#{}'.format(
                node.find('anchorfile').text,
                node.find('anchor').text,
            )

        urls.setdefault(kind, {})[name] = url

    def get_url(name):
        # These are all the kinds that seem to exist.
        for kind in (
            'function',
            'struct',
            'variable', # These are struct members.
            # 'class',
            # 'define',
            # 'enumeration',
            # 'enumvalue',
            # 'file',
            # 'group',
            # 'page',
            # 'typedef',
            # 'union',
        ):
            try:
                return urls[kind][name]
            except KeyError:
                pass


    def _doxylink_handler(name, rawtext, text, lineno, inliner, options={}, content=[]):

        m = re.match(r'^(.+?)(?:<(.+?)>)?$', text)
        title, name = m.groups()
        name = name or title

        url = get_url(name)
        if not url:
            print("ERROR: Could not find", name)
            exit(1)

        node = addnodes.literal_strong(title, title)
        if url:
            url = url_base + url
            node = nodes.reference(
                '', '', node, refuri=url
            )

        return [node], []

    return _doxylink_handler




def setup(app):

    app.add_css_file('custom.css')

    app.add_directive('flagtable', EnumTable)
    app.add_directive('enumtable', EnumTable)
    app.add_directive('pyinclude', PyInclude)

    skip = os.environ.get('PYAV_SKIP_DOXYLINK')
    for role, (filename, url_base) in doxylink.items():
        if skip:
            app.add_role(role, lambda *args: ([], []))
        else:
            app.add_role(role, doxylink_create_handler(app, filename, url_base))


