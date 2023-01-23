"""
HTML/XHTML/HTML 5 tag builder.

This is based on the `html` package of webhelpers2, maintained at
https://github.com/mikeorr/WebHelpers2
under the following license:

Copyright (c) 2005-2015 Ben Bangert, James Gardner, Philip Jenvey,
                        Mike Orr, Jon Rosenbaugh, Christoph Haas,
                        Marcin Lulek, Jeff Dairiki,
                        and other contributors.
History:

- 2005: Ben Bangert created WebHelpers.
- 2008: Mike Orr took over maintenance of WebHelpers.
- 2012: Mike Orr forked WebHelpers2 for backward-incompatible changes.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author or contributors may not be used to endorse or
   promote products derived from this software without specific prior
   written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
"""
import functools

import markupsafe
from markupsafe import escape_silent as escape

__all__ = ["HTML", "escape", "literal"]


class literal(markupsafe.Markup):
    """An HTML literal string, which will not be further escaped.

    I'm a subclass of ``markupsafe.Markup``, which itself is a subclass
    of ``unicode`` in Python 2 or ``str`` in Python 3. The main
    difference from ordinary strings is the ``.__html__`` method, which
    allows smart escapers to recognize it as a "safe" HTML string that
    doesn't need to be escaped.

    All my string methods preserve literal arguments and escape plain
    strings. However, in expressions you must pay attention to which
    value "controls" the expression. I seem to be able to control all
    combinations of the ``+`` operator, but with ``%`` and ``.join`` I
    must be on the left side. So these all work::

        "A" + literal("B")
        literal(", ".join(["A", literal("B")])
        literal("%s %s") % (16, literal("kg"))

    But these return plain strings which are vulnerable to
    double-escaping later::

        "\\n".join([literal("<span>A</span"), literal("Bar!")])
        "%s %s" % ([literal("16"), literal("&lt;&gt;")])
    """
    __slots__ = ()

    def __new__(cls, base="", encoding=None, errors="strict"):
        """Constructor.

        I convert my first argument to a string like ``str()`` does.
        However, I convert ``None`` to the empty string, which is
        usually what's desired in templates. (In contrast, raw
        ``Markup(None)`` returns ``"None"``.)

        Examples::

            >>> literal("A")   # => literal("A")
            >>> literal(">")   # => literal(">")
            >>> literal(None)  # => literal("")
            >>> literal(11)    # => literal("11")
            >>> literal(datetime.date.today())   # => literal("2014-08-31")

        The default encoding is "ascii".
        """
        if base is None:
            return EMPTY
        return super(literal, cls).__new__(cls, base, encoding, errors)

    @classmethod
    def escape(cls, s):
        """Escape the argument and return a literal.

        This is a *class* method. The result depends on the argument type:

        * literal: return unchanged.
        * an object with an ``.__html__`` method: call it and
          return the result. The method should take no arguments and
          return the object's preferred HTML representation as a string.
        * plain string: escape any HTML markup characters in it, and
          wrap the result in a literal to prevent double-escaping later.
        * non-string: call ``str()``, escape the result, and wrap it in
          a literal.
        * None: convert to the empty string and return a literal.

        If the argument has an ``.__html__`` method, I call it and
        return the result. This causes literals to pass through unchanged,
        and other objects with an ``.__html__`` method return their
        preferred HTML representation. If the argument is a plain
        string, I escape any HTML markup characters and wrap the result
        in a literal to prevent further escaping. If the argument is a
        non-string, I convert it to a string, escape it, and wrap it in
        a literal.  Examples::

            >>> literal.escape(">")            # => literal("&gt;")
            >>> literal.escape(literal(">"))   # => literal(">")
            >>> literal.escape(None)           # => literal("")

        I call ``markupsafe.escape_silent()``. It escapes double quotes
        as "&#34;", single quotes as "&#39;", "<" as "&lt;", ">" as
        "&gt;", and "&" as "&amp;".
        """
        if s is None:
            return EMPTY
        return super(literal, cls).escape(s)

    def lit_join(self, iterable):
        """Like the ``.join`` string method but don't escape elements in the iterable."""
        s = super(markupsafe.Markup, self).join(iterable)
        return self.__class__(s)


escape = literal.escape  # noqa: F811
NL = literal("\n")
BR = literal("<br />\n")
EMPTY = literal("")


class HTMLBuilder(object):
    """An HTML tag generator."""

    literal = literal

    EMPTY = EMPTY
    SPACE = literal(" ")
    TAB2 = literal("  ")
    TAB4 = literal("    ")
    NL = NL
    BR = BR
    NL2 = NL * 2
    BR2 = BR * 2

    void_tags = {
        # HTML 5.1
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "keygen",
        "link",
        "menuitem",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
        # The following elements are HTML 4.1 (not in the HTML 5.1 spec):
        "basefont",
        "frame",
        "isindex",
    }
    boolean_attrs = {
        "allowfullscreen",
        "async",
        "autofocus",
        "autoplay",
        "checked",
        "controls",
        "default",
        "defer",
        "disabled",
        "formnovalidate",
        "hidden",
        "ismap",
        "loop",
        "multiple",
        "muted",
        "novalidate",
        "open",
        "readonly",
        "required",
        "reversed",
        "selected",
        "typemustmatch",
    }
    compose_attrs = {
        "accept": literal(", "),
        "accept-charset": literal(" "),
        "accesskey": literal(" "),
        "class": literal(" "),
        "coords": literal(","),
        "dropzone": literal(" "),
        "for": literal(" "),
        "headers": literal(" "),
        "media": literal(", "),
        "rel": literal(" "),
        "rev": literal(" "),
        "sandbox": literal(" "),
        "sizes": literal(" "),
        "srcset": literal(", "),
        "style": literal("; "),
    }

    # Opening and closing syntax for special HTML constructs.
    _cdata_tag = literal("<![CDATA["), literal("]]>")
    _comment_tag = literal("<!-- "), literal(" -->")

    def __call__(self, *args, **kw):

        """Escape the string args, concatenate them, and return a literal.

        This is the same as ``literal.escape(s)`` but accepts multiple
        strings.  Multiple arguments are useful when mixing child tags
        with text, such as::

            html = HTML("The king is a >>", HTML.strong("fink"), "<<!")

        Keyword args:

        ``nl``
            If true, append a newline to the value. (Default False.)

        ``lit``
            If true, don't escape the arguments. (Default False.)
        """

        nl = kw.pop("nl", False)
        lit = kw.pop("lit", False)
        if kw:
            raise TypeError("unknown keyword args: {0}".format(sorted(kw)))
        if not lit:
            args = map(escape, args)
        if nl:
            ret = NL.lit_join(args) + NL
        else:
            ret = EMPTY.lit_join(args)
        return ret

    def tag(self, tag, *args, **kw):

        """Create an HTML tag.

        ``tag`` is the tag name. The other positional arguments become the
        content for the tag, and are escaped and concatenated.

        Keyword arguments are converted to HTML attributes, except for
        the following special arguments:

        ``c``
            Specifies the content.  This cannot be combined with content
            in positional args.  The purpose of this argument is to
            position the content at the end of the argument list to
            match the native HTML syntax more closely.  Its use is
            entirely optional.  The value can be a string, a tuple, or a
            tag.

        ``_closed``
            If present and false, do not close the tag.  Otherwise the
            tag will be closed with a closing tag or an XHTML-style
            trailing slash.

        ``_nl``
            If present and true, insert a newline before the first content
            element, between each content element, and at the end of the tag.

            Note that this argument has a leading underscore while the
            same argument to ``__call__`` doesn't. That's because
            this method has so many other complex arguments, and for
            backward compatibility.

        ``_bool``
            Additional HTML attributes to consider boolean beyond those
            listed in ``.boolean_attrs``. See "Class Attributes" below.


        Other keyword arguments are converted to HTML attributes after
        undergoing several transformations:

        * Ignore attributes whose value is None.

        * Delete trailing underscores in attribute names.
          ('class_' -> 'class').

        * Replace non-trailing underscores with hyphens. ('data_foo' ->
          'data-foo').

        * If the attribute is a *boolean attribute* — e.g. "defer",
          "disable", "readonly" — render it as an HTML 5 boolean
          attribute. If the value is true, copy the attribute name to
          the value. If the value is false, don't render the attribute
          at all.  See ``self.boolean_attrs`` and ``_bool`` to
          customize which attributes are considered boolean.

        * If the attribute is known to be list- or set- valued — e.g.
          "class" (or "class_"), "style", "rel" — and the value is a
          list or tuple, convert the value to a string by conjoining
          the values.  A separator appropriate to the attribute will
          be used to separate the values within the string.
          (E.g. "class" is space-separated, "style" is
          semicolon-separated.)  If the value is an empty list or
          tuple, don't render the attribute at all. If the value
          contains elements that are 2-tuples, the first subelement is
          the string item, and the second subelement is a boolean
          flag; render only subelements whose flag is true.  This
          allows users to programatically set the parts of a
          composable attribute in a template without extra loops or
          logic code.  See ``self.compose_attrs`` to customize which
          attributes have list/tuple conversion and what their
          delimiter is.

        Examples:

        >>> HTML.tag("div", "Foo", class_="important")
        literal(u'<div class="important">Foo</div>')
        >>> HTML.tag("div", "Foo", class_=None)
        literal(u'<div>Foo</div>')
        >>> HTML.tag("div", "Foo", class_=["a", "b"])
        literal(u'<div class="a b">Foo</div>')
        >>> HTML.tag("div", "Foo", class_=[("a", False), ("b", True)])
        literal(u'<div class="b">Foo</div>')
        >>> HTML.tag("div", "Foo", style=["color:black", "border:solid"])
        literal(u'<div style="color:black; border:solid">Foo</div>')
        >>> HTML.tag("br")
        literal(u'<br />')
        >>> HTML.tag("input", disabled=True)
        literal(u'<input disabled="disabled"></input>')
        >>> HTML.tag("input", disabled=False)
        literal(u'<input></input>')

        To generate opening and closing tags in isolation:

        >>> HTML.tag("div", _closed=False)
        literal(u'<div>')
        >>> HTML.tag("/div", _closed=False)
        literal(u'</div>')
        """

        if "c" in kw:
            assert not args, "The special 'c' keyword argument cannot be used " \
                             "in conjunction with non-keyword arguments"
            args = kw.pop("c")
            if isinstance(args, str):
                args = (args,)
        closed = kw.pop("_closed", True)
        nl = kw.pop("_nl", False)
        boolean_attrs = kw.pop("_bool", None)
        attrs = kw
        self.optimize_attrs(attrs, boolean_attrs)
        attrs_str = self.render_attrs(attrs)
        chunks = []
        if not args and tag in self.void_tags and closed:
            substr = literal("<{0}{1} />")
            html = substr.format(tag, attrs_str)
            chunks.append(html)
        else:
            substr = literal("<{0}{1}>")
            html = substr.format(tag, attrs_str)
            chunks.append(html)
            chunks.extend(args)
            if closed:
                substr = literal("</{0}>")
                chunks.append(substr.format(tag))
        return self(*chunks, nl=nl)

    def __getattr__(self, attr):

        """Same as the ``tag`` method but using attribute access.

        ``HTML.a(...)`` is equivalent to ``HTML.tag("a", ...)``.
        """

        if attr.startswith('_'):
            raise AttributeError(attr)
        tag = functools.partial(self.tag, attr.lower())
        self.__dict__[attr] = tag
        return tag

    def comment(self, *args):

        """Wrap the content in an HTML comment.

        Escape and concatenate the string arguments.

        Example:

        >>> HTML.comment("foo", "bar")
        literal(u'<!-- foobar -->')
        """

        parts = [self._comment_tag[0]]
        parts.extend(args)
        parts.append(self._comment_tag[1])
        return self(*parts)

    def cdata(self, *args):

        """Wrap the content in a "<![CDATA[ ... ]]>" section.

        Plain strings will not be escaped because CDATA itself is an
        escaping syntax. Concatenate the arguments:

        >>> HTML.cdata(u"Foo")
        literal(u'<![CDATA[Foo]]>')

        >>> HTML.cdata(u"<p>")
        literal(u'<![CDATA[<p>]]>')
        """

        parts = [self._cdata_tag[0]]
        parts.extend(args)
        parts.append(self._cdata_tag[1])
        return self(*parts, lit=True)

    def render_attrs(self, attrs):

        """Format HTML attributes into a string of ' key="value"' pairs.

        You don't normally need to call this because the ``tag`` method
        calls it for you. However, it can be useful for lower-level
        formatting in string templates like this:

        .. code-block:: mako

           Click <a href="http://example.com/"{attrs1}>here</a>
           or maybe <a{attrs2}>here</a>.


        ``attrs`` is a list of attributes. The values will be escaped if
        they're not literals, but no other transformation will be
        performed on them.

        The return value will have a leading space if any attributes are
        present. If no attributes are specified, the return value is the
        empty string literal. This allows it to render prettily in
        the interpolations above regardless of whether ``attrs``
        contains anything.
        """

        keys = sorted(attrs)
        fmt = literal(' {0}="{1}"')
        strings = [fmt.format(x, attrs[x]) for x in keys]
        return EMPTY.join(strings)

    # Private methods
    def optimize_attrs(self, attrs, boolean_attrs=None):

        """Perform various transformations on an HTML attributes dict.

        Arguments:

        * **attrs**: the attribute dict. Modified in place!
        * **boolean_attrs**: set of attribute names to consider
          boolean in addition to ``self.boolean_attrs``.

        Modifies 'attrs' in place. Actions:

        1. Delete keys whose value is None.
        2. Delete trailing underscores in keys.
        3. Replace non-trailing underscores in keys with hyphens.
        4. If a key is listed in 'self.compose_attrs' and the value is
           a list or tuple, join the elements into a string using the separator
           specified. If the value is an empty list/tuple, delete the key
           entirely. If any element is itself a 2-tuple, the first subelement is
           the string item, and the second is treated as a boolean flag.  If
           the flag is true, keep the item, otherwise delete it from the list.
           This allows users to programmatically set the parts of a composable
           attribute in a template without extra loops and logic code.
        5. If a key is listed in 'self.boolean_attrs' or the 'boolean_attrs'
           argument, convert the value to an HTML boolean. If the value is
           true, set the value to match the key. If the value is false,
           delete the key.
        """
        if boolean_attrs:
            boolean_keys = self.boolean_attrs.union(boolean_attrs)
        else:
            boolean_keys = self.boolean_attrs
        # Make a copy of the keys because we'll be adding/deleting in the
        # original dict.
        keys = list(attrs.keys())
        for key in keys:
            value = attrs[key]
            # Delete key if None value.
            if value is None:
                del attrs[key]
                continue
            # Rename key if it contains internal or trailing underscores.
            key_orig = key
            while key.endswith("_"):
                key = key[:-1]
            key = key.replace("_", "-")
            if key != key_orig:
                attrs[key] = attrs.pop(key_orig)
            # Convert "composeable attributes" from list to delimited string.
            if key in self.compose_attrs and isinstance(value, (list, tuple)):
                # Convert 2-tuples to regular elements.
                value_orig = value
                value = []
                for elm in value_orig:
                    if isinstance(elm, (list, tuple)) and len(elm) == 2:
                        if elm[1]:
                            value.append(elm[0])
                        # Else ignore the element.
                    else:
                        value.append(elm)
                # If value is non-empty, join the elements. If empty, delete
                # the key.
                if value:
                    sep = self.compose_attrs[key]
                    attrs[key] = sep.join(value)
                else:
                    del attrs[key]
            # Convert boolean attributes.
            if key in boolean_keys:
                if value:
                    attrs[key] = key  # Set the value to match the key.
                else:
                    del attrs[key]
            key_orig = value_orig = None  # To guard against bugs.


HTML = HTMLBuilder()
