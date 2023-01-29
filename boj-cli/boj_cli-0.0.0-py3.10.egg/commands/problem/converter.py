from markdownify import MarkdownConverter
from boj.core import util

# Heading styles
ATX = 'atx'
ATX_CLOSED = 'atx_closed'
UNDERLINED = 'underlined'
SETEXT = UNDERLINED

# Newline style
SPACES = 'spaces'
BACKSLASH = 'backslash'

# Strong and emphasis style
ASTERISK = '*'
UNDERSCORE = '_'


def chomp(text):
    """
    If the text in an inline tag like b, a, or em contains a leading or trailing
    space, strip the string and return a space as suffix of prefix, if needed.
    This function is used to prevent conversions like
        <b> foo</b> => ** foo**
    """
    prefix = ' ' if text and text[0] == ' ' else ''
    suffix = ' ' if text and text[-1] == ' ' else ''
    text = text.strip()
    return (prefix, suffix, text)


class MarkdownConverter(MarkdownConverter):
    def convert_hn(self, n, el, text, convert_as_inline):
        if convert_as_inline:
            return text

        style = self.options['heading_style'].lower()
        text = text.strip()
        if style == UNDERLINED and n <= 2:
            line = '=' if n == 1 else '-'
            return self.underline(text, line)
        hashes = '#' * n
        if style == ATX_CLOSED:
            return '%s %s %s\n\n' % (hashes, text, hashes)
        return '%s %s\n\n' % (hashes, text)

    def convert_img(self, el, text, convert_as_inline):
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        if (convert_as_inline
                and el.parent.name not in self.options['keep_inline_images_in']):
            return alt

        if util.home_url() not in src:
            return '![%s](%s/%s%s)' % (alt, util.home_url(), src, title_part)

        return '![%s](%s%s)' % (alt, src, title_part)

    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        href = el.get('href')
        title = el.get('title')
        # For the replacement see #29: text nodes underscores are escaped
        if (self.options['autolinks']
                and text.replace(r'\_', '_') == href
                and not title
                and not self.options['default_title']):
            # Shortcut syntax
            return '<%s>' % href
        if self.options['default_title'] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''

        if util.home_url() not in href:
            return '%s[%s](%s/%s%s)%s' % (prefix, text, util.home_url(), href, title_part, suffix) if href else text

        return '%s[%s](%s%s)%s' % (prefix, text, href, title_part, suffix) if href else text

    def convert_table(self, el, text, convert_as_inline):
        return "| " + text.strip() + "\n"

    def convert_td(self, el, text, convert_as_inline):
        return " " + text.strip() + " |"

    def convert_th(self, el, text, convert_as_inline):
        ret = " " + text.strip() + " |"
        if not el.next_sibling:
            col = len(el.parent.find_all(["th"]))
            ret += "\n|" + " | ".join(["---"] * col) + " |\n"

        return ret

    def convert_tr(self, el, text, convert_as_inline):
        cells = el.find_all(["td", "th"])
        is_headrow = all([(cell.name == "th") for cell in cells])
        overline = ""
        underline = ""
        if is_headrow:
            # first row and is headline: print headline underline
            underline += "| " + " | ".join(["---"] * len(cells)) + " |" + "\n"
        elif not el.previous_sibling and (
                el.parent.name == "table"
                or (el.parent.name == "tbody" and not el.parent.previous_sibling)
        ):
            # first row, not headline, and:
            # - the parent is table or
            # - the parent is tbody at the beginning of a table.
            # print empty headline above this row
            overline += "| " + " | ".join([""] * len(cells)) + " |" + "\n"
            overline += "| " + " | ".join(["---"] * len(cells)) + " |" + "\n"
        return overline + "| " + text.strip() + "\n" + underline
