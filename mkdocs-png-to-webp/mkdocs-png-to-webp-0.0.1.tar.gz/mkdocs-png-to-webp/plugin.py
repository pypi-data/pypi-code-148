from mkdocs.plugins import BasePlugin


class ConvertPngToWebp(BasePlugin):

    def on_files(self, files, config):

        return files

    def on_page_content(self, html, page, config, files):

        return html
    