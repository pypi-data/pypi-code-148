import re
from typing import Optional
from mkdocs import utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page


class BulmaClassesPlugin(BasePlugin):
    config_scheme = {
        ("param", config_options.Type(str, default="")),
    }

    markdown_regexes = {
        "(.*)\n(=+)(\n+)(.*)\n(-+)": '<h1 class="title is-1 has-text-light" id="\g<1>">\g<1></h1><h3 class="subtitle is-3 has-text-light" id="\g<4>">\g<4></h3>',
    }

    regex_dict = {
        '<table (id="\w*")? class="((?!table).*)">': '<table \g<1> class="table \g<2>">', # Look at https://regex101.com/r/3UZHgz/1 for unit tests
        '<h1 id=\"([\w-]*)\" class=\"(?![(title)|(is\-1)])([\w-]*)\">': '<h1 id="\g<1>" class="title is-1 has-text-light \g<2>">', # Look at https://regex101.com/r/bxQBvm/3 for unit tests
        '<h2 id="([\w-]*)">': '<h2 id="\g<1>" class="title is-2 has-text-light">',
        '<h3 id="([\w-]*)">': '<h3 id="\g<1>" class="title is-3 has-text-light">',
        '<h4 id="([\w-]*)">': '<h4 id="\g<1>" class="title is-4 has-text-light">',
        '<h5 id="([\w-]*)">': '<h5 id="\g<1>" class="title is-5 has-text-light">',
        '<h6 id="([\w-]*)">': '<h6 id="\g<1>" class="title is-6 has-text-light">',
        '<a href="(.*)">': '<a href="\g<1>" class="is-clickable has-text-link-light">',
        "\n<ul>.*</ul>\n": '<div class="content">\g<0></div>',  # Look at https://regex101.com/r/X0PSlS/2 for unit tests
        # '<code>.*</code>': '<div class="content">\n\g<0>\n</div>'
    }

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_page_markdown(
        self, markdown: str, page: Page, config, files
    ) -> Optional[str]:
        # Substitute any element that need Markdown to be mapped.
        for key, value in self.markdown_regexes.items():
            regex = re.compile(key, re.MULTILINE)
            # TODO: This substitution not leave any chance to process any
            # markdown inside a captured content of the regex (.*), like the
            # issue with Titles and Subtitles. There's a possibility to make it
            # with the least possible complexity?
            markdown = re.sub(regex, value, markdown)

        return markdown

    def on_post_page(self, output: str, *, page: Page, config) -> Optional[str]:
        # Substitute any element that need HTML to be mapped.
        # Here we take all other simple Markdown elements with easy mapping to Bulma classes
        for key, value in self.regex_dict.items():
            if m := re.findall(key, output):
                utils.log.debug(f"Found {key} in {page.title}: {m}")
            regex = re.compile(key, re.MULTILINE | re.DOTALL)
            output = re.sub(regex, value, output, 0)
        return output
