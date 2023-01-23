##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Interpreter for a pre-compiled TAL program.
"""
import html
import sys

from zope.i18nmessageid import Message

from zope.tal.taldefs import TAL_VERSION
from zope.tal.taldefs import METALError
from zope.tal.taldefs import getProgramMode
from zope.tal.taldefs import getProgramVersion
from zope.tal.taldefs import isCurrentVersion
from zope.tal.taldefs import quote
from zope.tal.talgenerator import TALGenerator
from zope.tal.translationcontext import TranslationContext


# Avoid constructing this tuple over and over
I18nMessageTypes = (Message,)
TypesToTranslate = I18nMessageTypes + (str, )

BOOLEAN_HTML_ATTRS = frozenset([
    # List of Boolean attributes in HTML that should be rendered in
    # minimized form (e.g. <img ismap> rather than <img ismap="">)
    # From http://www.w3.org/TR/xhtml1/#guidelines (C.10)
    # TODO: The problem with this is that this is not valid XML and
    # can't be parsed back!
    # XXX: This is an exact duplicate of htmltalparser.BOOLEAN_HTML_ATTRS. Why?
    "compact", "nowrap", "ismap", "declare", "noshade", "checked",
    "disabled", "readonly", "multiple", "selected", "noresize",
    "defer"
])

_nulljoin = ''.join
_spacejoin = ' '.join


def normalize(text):
    # Now we need to normalize the whitespace in implicit message ids and
    # implicit $name substitution values by stripping leading and trailing
    # whitespace, and folding all internal whitespace to a single space.
    return _spacejoin(text.split())


class AltTALGenerator(TALGenerator):

    def __init__(self, repldict, expressionCompiler=None, xml=0):
        self.repldict = repldict
        self.enabled = 1
        TALGenerator.__init__(self, expressionCompiler, xml)

    def enable(self, enabled):
        self.enabled = enabled

    def emit(self, *args):
        if self.enabled:
            TALGenerator.emit(self, *args)

    def emitStartElement(self, name, attrlist, taldict, metaldict, i18ndict,
                         position=(None, None), isend=0):
        metaldict = {}
        taldict = {}
        i18ndict = {}
        if self.enabled and self.repldict:
            taldict["attributes"] = "x x"
        TALGenerator.emitStartElement(self, name, attrlist,
                                      taldict, metaldict, i18ndict,
                                      position, isend)

    def replaceAttrs(self, attrlist, repldict):
        if self.enabled and self.repldict:
            repldict = self.repldict
            self.repldict = None
        return TALGenerator.replaceAttrs(self, attrlist, repldict)


class MacroStackItem(list):
    # This is a `list` subclass for backward compatibility.
    """Stack entry for the TALInterpreter.macroStack.

    This offers convenience attributes for more readable access.

    """
    __slots__ = ()

    @property
    def macroName(self):
        return self[0]

    @property
    def slots(self):
        return self[1]

    @property
    def definingName(self):
        return self[2]

    @property
    def extending(self):
        return self[3]

    @property
    def entering(self):
        return self[4]

    @entering.setter
    def entering(self, value):
        self[4] = value

    @property
    def i18nContext(self):
        return self[5]


class TALInterpreter:
    """TAL interpreter.

    Some notes on source annotations.  They are HTML/XML comments added to the
    output whenever ``sourceFile`` is changed by a ``setSourceFile`` bytecode.
    Source annotations are disabled by default, but you can turn them on by
    passing a ``sourceAnnotations`` argument to the constructor.  You can
    change the format of the annotations by overriding formatSourceAnnotation
    in a subclass.

    The output of the annotation is delayed until some actual text is output
    for two reasons:

        1. ``setPosition`` bytecode follows ``setSourceFile``, and we need
           position information to output the line number.
        2. Comments are not allowed in XML documents before the ``<?xml?>``
           declaration.

    For performance reasons (TODO: premature optimization?) instead of checking
    the value of ``_pending_source_annotation`` on every write to the output
    stream, the ``_stream_write`` attribute is changed to point to
    ``_annotated_stream_write`` method whenever ``_pending_source_annotation``
    is set to True, and to _stream.write when it is False.  The following
    invariant always holds::

        if self._pending_source_annotation:
            assert self._stream_write is self._annotated_stream_write
        else:
            assert self._stream_write is self.stream.write

    """

    def __init__(self, program, macros, engine, stream=None,
                 debug=0, wrap=1023, metal=1, tal=1, showtal=-1,
                 strictinsert=1, stackLimit=100, i18nInterpolate=1,
                 sourceAnnotations=0):
        """Create a TAL interpreter.

        :param program: A compiled program, as generated
            by :class:`zope.tal.talgenerator.TALGenerator`
        :param macros: Namespace of macros, usually also from
            :class:`~.TALGenerator`

        Optional arguments:

        :keyword stream: output stream (defaults to sys.stdout).
        :keyword bool debug: enable debugging output to sys.stderr (off by
            default).
        :keyword int wrap: try to wrap attributes on opening tags to this
            number of column (default: 1023).
        :keyword bool metal: enable METAL macro processing (on by default).
        :keyword bool tal: enable TAL processing (on by default).
        :keyword int showtal: do not strip away TAL directives.  A special
            value of -1 (which is the default setting) enables showtal when TAL
            processing is disabled, and disables showtal when TAL processing is
            enabled.  Note that you must use 0, 1, or -1; true boolean values
            are not supported (for historical reasons).
        :keyword bool strictinsert: enable TAL processing and stricter HTML/XML
            checking on text produced by structure inserts (on by default).
            Note that Zope turns this value off by default.
        :keyword int stackLimit: set macro nesting limit (default: 100).
        :keyword bool i18nInterpolate: enable i18n translations (default: on).
        :keyword bool sourceAnnotations: enable source annotations with HTML
            comments (default: off).
        """
        self.program = program
        self.macros = macros
        self.engine = engine  # Execution engine (aka context)
        self.Default = engine.getDefault()
        self._pending_source_annotation = False
        self._currentTag = ""
        self._stream_stack = [stream or sys.stdout]
        self.popStream()
        self.debug = debug
        self.wrap = wrap
        self.metal = metal
        self.tal = tal
        if tal:
            self.dispatch = self.bytecode_handlers_tal
        else:
            self.dispatch = self.bytecode_handlers
        assert showtal in (-1, 0, 1)
        if showtal == -1:
            showtal = (not tal)
        self.showtal = showtal
        self.strictinsert = strictinsert
        self.stackLimit = stackLimit
        self.html = 0
        self.endsep = "/>"
        self.endlen = len(self.endsep)
        # macroStack entries are MacroStackItem instances;
        # the entries are mutated while on the stack
        self.macroStack = []
        # `inUseDirective` is set iff we're handling either a
        # metal:use-macro or a metal:extend-macro
        self.inUseDirective = False
        self.position = None, None  # (lineno, offset)
        self.col = 0
        self.level = 0
        self.scopeLevel = 0
        self.sourceFile = None
        self.i18nStack = []
        self.i18nInterpolate = i18nInterpolate
        self.i18nContext = TranslationContext()
        self.sourceAnnotations = sourceAnnotations

    def StringIO(self):
        # Third-party products wishing to provide a full text-aware
        # StringIO can do so by monkey-patching this method.
        return FasterStringIO()

    def saveState(self):
        return (self.position, self.col, self.stream, self._stream_stack,
                self.scopeLevel, self.level, self.i18nContext)

    def restoreState(self, state):
        (self.position, self.col, self.stream,
         self._stream_stack, scopeLevel, level, i18n) = state
        if self._pending_source_annotation:
            self._stream_write = self._annotated_stream_write
        else:
            self._stream_write = self.stream.write
        assert self.level == level
        while self.scopeLevel > scopeLevel:
            self.engine.endScope()
            self.scopeLevel = self.scopeLevel - 1
        self.engine.setPosition(self.position)
        self.i18nContext = i18n

    def restoreOutputState(self, state):
        (dummy, self.col, self.stream,
         self._stream_stack, scopeLevel, level, i18n) = state
        if self._pending_source_annotation:
            self._stream_write = self._annotated_stream_write
        else:
            self._stream_write = self.stream.write
        assert self.level == level
        assert self.scopeLevel == scopeLevel

    def pushMacro(self, macroName, slots, definingName, extending):
        if len(self.macroStack) >= self.stackLimit:
            raise METALError("macro nesting limit (%d) exceeded "
                             "by %s" % (self.stackLimit, repr(macroName)))
        self.macroStack.append(
            MacroStackItem((macroName, slots, definingName, extending,
                            True, self.i18nContext)))

    def popMacro(self):
        return self.macroStack.pop()

    def __call__(self):
        """
        Interpret the current program.

        :return: Nothing.
        """
        assert self.level == 0
        assert self.scopeLevel == 0
        assert self.i18nContext.parent is None
        self.interpret(self.program)
        assert self.level == 0
        assert self.scopeLevel == 0
        assert self.i18nContext.parent is None

    def pushStream(self, newstream):
        self._stream_stack.append(self.stream)
        self.stream = newstream
        if self._pending_source_annotation:
            self._stream_write = self._annotated_stream_write
        else:
            self._stream_write = self.stream.write

    def popStream(self):
        self.stream = self._stream_stack.pop()
        if self._pending_source_annotation:
            self._stream_write = self._annotated_stream_write
        else:
            self._stream_write = self.stream.write

    def _annotated_stream_write(self, s):
        idx = s.find('<?xml')
        if idx >= 0 or s.isspace():
            # Do not preprend comments in front of the <?xml?> declaration.
            end_of_doctype = s.find('?>', idx)
            if end_of_doctype > idx:
                self.stream.write(s[:end_of_doctype + 2])
                s = s[end_of_doctype + 2:]
                # continue
            else:
                self.stream.write(s)
                return
        self._pending_source_annotation = False
        self._stream_write = self.stream.write
        self._stream_write(self.formatSourceAnnotation())
        self._stream_write(s)

    def formatSourceAnnotation(self):
        lineno = self.position[0]
        if lineno is None:
            location = self.sourceFile
        else:
            location = '{} (line {})'.format(self.sourceFile, lineno)
        sep = '=' * 78
        return '<!--\n{}\n{}\n{}\n-->'.format(sep, location, sep)

    def stream_write(self, s,
                     len=len):
        self._stream_write(s)
        i = s.rfind('\n')
        if i < 0:
            self.col = self.col + len(s)
        else:
            self.col = len(s) - (i + 1)

    bytecode_handlers = {}

    def interpret(self, program):
        oldlevel = self.level
        self.level = oldlevel + 1
        handlers = self.dispatch
        try:
            if self.debug:
                for (opcode, args) in program:
                    s = "{}do_{}({})\n".format("    " * self.level, opcode,
                                               repr(args))
                    if len(s) > 80:
                        s = s[:76] + "...\n"
                    sys.stderr.write(s)
                    handlers[opcode](self, args)
            else:
                for (opcode, args) in program:
                    handlers[opcode](self, args)
        finally:
            self.level = oldlevel

    def do_version(self, version):
        assert version == TAL_VERSION
    bytecode_handlers["version"] = do_version

    def do_mode(self, mode):
        assert mode in ("html", "xml")
        self.html = (mode == "html")
        if self.html:
            self.endsep = " />"
        else:
            self.endsep = "/>"
        self.endlen = len(self.endsep)
    bytecode_handlers["mode"] = do_mode

    def do_setSourceFile(self, source_file):
        self.sourceFile = source_file
        self.engine.setSourceFile(source_file)
        if self.sourceAnnotations:
            self._pending_source_annotation = True
            self._stream_write = self._annotated_stream_write

    bytecode_handlers["setSourceFile"] = do_setSourceFile

    def do_setPosition(self, position):
        self.position = position
        self.engine.setPosition(position)
    bytecode_handlers["setPosition"] = do_setPosition

    def do_startEndTag(self, stuff):
        self.do_startTag(stuff, self.endsep, self.endlen)
    bytecode_handlers["startEndTag"] = do_startEndTag

    def do_startTag(self, stuff, end=">", endlen=1, _len=len):
        # The bytecode generator does not cause calls to this method
        # for start tags with no attributes; those are optimized down
        # to rawtext events.  Hence, there is no special "fast path"
        # for that case.
        (name, attrList) = stuff
        self._currentTag = name
        L = ["<", name]
        append = L.append
        col = self.col + _len(name) + 1
        wrap = self.wrap
        align = col + 1
        if align >= wrap / 2:
            align = 4  # Avoid a narrow column far to the right
        attrAction = self.dispatch["<attrAction>"]
        try:
            for item in attrList:
                if _len(item) == 2:
                    rendered = item[1:]
                else:
                    # item[2] is the 'action' field:
                    if item[2] in ('metal', 'tal', 'xmlns', 'i18n'):
                        if not self.showtal:
                            continue
                        rendered = self.attrAction(item)
                    else:
                        rendered = attrAction(self, item)
                    if not rendered:
                        continue
                for s in rendered:
                    slen = _len(s)
                    if (wrap and
                        col >= align and
                            col + 1 + slen > wrap):
                        append("\n")
                        append(" " * align)
                        col = align + slen
                    else:
                        append(" ")
                        col = col + 1 + slen
                    append(s)
            append(end)
            col = col + endlen
        finally:
            self._stream_write(_nulljoin(L))
            self.col = col
    bytecode_handlers["startTag"] = do_startTag

    def attrAction(self, item):
        name, value, action = item[:3]
        if action == 'insert':
            return ()
        macs = self.macroStack
        if action == 'metal' and self.metal and macs:
            # Drop all METAL attributes at a use-depth beyond the first
            # use-macro and its extensions
            if len(macs) > 1:
                for macro in macs[1:]:
                    if not macro.extending:
                        return ()
            if not macs[-1].entering:
                return ()
            macs[-1].entering = False
            # Convert or drop depth-one METAL attributes.
            i = name.rfind(":") + 1
            prefix, suffix = name[:i], name[i:]
            if suffix == "define-macro":
                # Convert define-macro as we enter depth one.
                useName = macs[0].macroName
                defName = macs[0].definingName
                res = []
                if defName:
                    res.append(
                        '{}define-macro={}'.format(prefix, quote(defName)))
                if useName:
                    res.append('{}use-macro={}'.format(prefix, quote(useName)))
                return res
            elif suffix == "define-slot":
                name = prefix + "fill-slot"
            elif suffix == "fill-slot":
                pass
            else:
                return ()

        if value is None:
            value = name
        else:
            value = "{}={}".format(name, quote(value))
        return [value]

    def attrAction_tal(self, item):
        name, value, action = item[:3]
        ok = 1
        expr, xlat, msgid = item[3:]
        if self.html and name.lower() in BOOLEAN_HTML_ATTRS:
            evalue = self.engine.evaluateBoolean(item[3])
            if evalue is self.Default:
                if action == 'insert':  # Cancelled insert
                    ok = 0
            elif evalue:
                value = None
            else:
                ok = 0
        elif expr is not None:
            evalue = self.engine.evaluateText(item[3])
            if evalue is self.Default:
                if action == 'insert':  # Cancelled insert
                    ok = 0
            else:
                if evalue is None:
                    ok = 0
                value = evalue

        if ok:
            if xlat:
                translated = self.translate(msgid or value, value)
                if translated is not None:
                    value = translated
            elif isinstance(value, I18nMessageTypes):
                translated = self.translate(value)
                if translated is not None:
                    value = translated
            if value is None:
                value = name
            return ["{}={}".format(name, quote(value))]
        else:
            return ()
    bytecode_handlers["<attrAction>"] = attrAction

    def no_tag(self, start, program):
        state = self.saveState()
        self.stream = stream = self.StringIO()
        self._stream_write = stream.write
        self.interpret(start)
        self.restoreOutputState(state)
        self.interpret(program)

    def do_optTag(self, stuff, omit=0):
        (name, cexpr, tag_ns, isend, start, program) = stuff
        if tag_ns and not self.showtal:
            return self.no_tag(start, program)

        self.interpret(start)
        if not isend:
            self.interpret(program)
            s = '</%s>' % name
            self._stream_write(s)
            self.col = self.col + len(s)

    def do_optTag_tal(self, stuff):
        cexpr = stuff[1]
        if cexpr is not None and (cexpr == '' or
                                  self.engine.evaluateBoolean(cexpr)):
            self.no_tag(stuff[-2], stuff[-1])
        else:
            self.do_optTag(stuff)
    bytecode_handlers["optTag"] = do_optTag

    def do_rawtextBeginScope(self, stuff):
        (s, col, position, closeprev, dict) = stuff
        self._stream_write(s)
        self.col = col
        self.do_setPosition(position)
        if closeprev:
            engine = self.engine
            engine.endScope()
            engine.beginScope()
        else:
            self.engine.beginScope()
            self.scopeLevel = self.scopeLevel + 1

    def do_rawtextBeginScope_tal(self, stuff):
        (s, col, position, closeprev, dict) = stuff
        self._stream_write(s)
        self.col = col
        engine = self.engine
        self.position = position
        engine.setPosition(position)
        if closeprev:
            engine.endScope()
            engine.beginScope()
        else:
            engine.beginScope()
            self.scopeLevel = self.scopeLevel + 1
        engine.setLocal("attrs", dict)
    bytecode_handlers["rawtextBeginScope"] = do_rawtextBeginScope

    def do_beginScope(self, dict):
        self.engine.beginScope()
        self.scopeLevel = self.scopeLevel + 1

    def do_beginScope_tal(self, dict):
        engine = self.engine
        engine.beginScope()
        engine.setLocal("attrs", dict)
        self.scopeLevel = self.scopeLevel + 1
    bytecode_handlers["beginScope"] = do_beginScope

    def do_endScope(self, notused=None):
        self.engine.endScope()
        self.scopeLevel = self.scopeLevel - 1
    bytecode_handlers["endScope"] = do_endScope

    def do_setLocal(self, notused):
        pass

    def do_setLocal_tal(self, stuff):
        (name, expr) = stuff
        self.engine.setLocal(name, self.engine.evaluateValue(expr))
    bytecode_handlers["setLocal"] = do_setLocal

    def do_setGlobal_tal(self, stuff):
        (name, expr) = stuff
        self.engine.setGlobal(name, self.engine.evaluateValue(expr))
    bytecode_handlers["setGlobal"] = do_setLocal

    def do_beginI18nContext(self, settings):
        get = settings.get
        self.i18nContext = TranslationContext(self.i18nContext,
                                              domain=get("domain"),
                                              source=get("source"),
                                              target=get("target"))
    bytecode_handlers["beginI18nContext"] = do_beginI18nContext

    def do_endI18nContext(self, notused=None):
        self.i18nContext = self.i18nContext.parent
        assert self.i18nContext is not None
    bytecode_handlers["endI18nContext"] = do_endI18nContext

    def do_insertText(self, stuff):
        self.interpret(stuff[1])
    bytecode_handlers["insertText"] = do_insertText
    bytecode_handlers["insertI18nText"] = do_insertText

    def _writeText(self, text):
        # '&' must be done first!
        s = text.replace(
            "&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self._stream_write(s)
        i = s.rfind('\n')
        if i < 0:
            self.col += len(s)
        else:
            self.col = len(s) - (i + 1)

    def do_insertText_tal(self, stuff):
        text = self.engine.evaluateText(stuff[0])
        if text is None:
            return
        if text is self.Default:
            self.interpret(stuff[1])
            return
        if isinstance(text, I18nMessageTypes):
            # Translate this now.
            text = self.translate(text)
        self._writeText(text)

    def do_insertI18nText_tal(self, stuff):
        # TODO: Code duplication is BAD, we need to fix it later
        text = self.engine.evaluateText(stuff[0])
        if text is not None:
            if text is self.Default:
                self.interpret(stuff[1])
            else:
                if isinstance(text, TypesToTranslate):
                    text = self.translate(text)
                self._writeText(text)

    def do_i18nVariable(self, stuff):
        varname, program, expression, structure = stuff
        if expression is None:
            # The value is implicitly the contents of this tag, so we have to
            # evaluate the mini-program to get the value of the variable.
            state = self.saveState()
            try:
                tmpstream = self.StringIO()
                self.pushStream(tmpstream)
                try:
                    self.interpret(program)
                finally:
                    self.popStream()
                if self.html and self._currentTag == "pre":
                    value = tmpstream.getvalue()
                else:
                    value = normalize(tmpstream.getvalue())
            finally:
                self.restoreState(state)
        else:
            # TODO: Seems like this branch not used anymore, we
            # need to remove it

            # Evaluate the value to be associated with the variable in the
            # i18n interpolation dictionary.
            if structure:
                value = self.engine.evaluateStructure(expression)
            else:
                value = self.engine.evaluate(expression)

            # evaluate() does not do any I18n, so we do it here.
            if isinstance(value, I18nMessageTypes):
                # Translate this now.
                value = self.translate(value)

            if not structure:
                value = html.escape(str(value))

        # Either the i18n:name tag is nested inside an i18n:translate in which
        # case the last item on the stack has the i18n dictionary and string
        # representation, or the i18n:name and i18n:translate attributes are
        # in the same tag, in which case the i18nStack will be empty.  In that
        # case we can just output the ${name} to the stream
        i18ndict, srepr = self.i18nStack[-1]
        i18ndict[varname] = value
        placeholder = '${%s}' % varname
        srepr.append(placeholder)
        self._stream_write(placeholder)
    bytecode_handlers['i18nVariable'] = do_i18nVariable

    def do_insertTranslation(self, stuff):
        i18ndict = {}
        srepr = []
        obj = None
        self.i18nStack.append((i18ndict, srepr))
        msgid = stuff[0]
        # We need to evaluate the content of the tag because that will give us
        # several useful pieces of information.  First, the contents will
        # include an implicit message id, if no explicit one was given.
        # Second, it will evaluate any i18nVariable definitions in the body of
        # the translation (necessary for $varname substitutions).
        #
        # Use a temporary stream to capture the interpretation of the
        # subnodes, which should /not/ go to the output stream.
        currentTag = self._currentTag
        tmpstream = self.StringIO()
        self.pushStream(tmpstream)
        try:
            self.interpret(stuff[1])
        finally:
            self.popStream()
        # We only care about the evaluated contents if we need an implicit
        # message id.  All other useful information will be in the i18ndict on
        # the top of the i18nStack.
        default = tmpstream.getvalue()
        if not msgid:
            if self.html and currentTag == "pre":
                msgid = default
            else:
                msgid = normalize(default)
        self.i18nStack.pop()
        # See if there is was an i18n:data for msgid
        if len(stuff) > 2:
            obj = self.engine.evaluate(stuff[2])
        xlated_msgid = self.translate(msgid, default, i18ndict, obj)
        # TODO: I can't decide whether we want to html.escape the translated
        # string or not.  OTOH not doing this could introduce a cross-site
        # scripting vector by allowing translators to sneak JavaScript into
        # translations.  OTOH, for implicit interpolation values, we don't
        # want to escape stuff like ${name} <= "<b>Timmy</b>".
        assert xlated_msgid is not None
        self._stream_write(xlated_msgid)
    bytecode_handlers['insertTranslation'] = do_insertTranslation

    def do_insertStructure(self, stuff):
        self.interpret(stuff[2])
    bytecode_handlers["insertStructure"] = do_insertStructure
    bytecode_handlers["insertI18nStructure"] = do_insertStructure

    def do_insertStructure_tal(self, stuff):
        (expr, repldict, block) = stuff
        structure = self.engine.evaluateStructure(expr)
        if structure is None:
            return
        if structure is self.Default:
            self.interpret(block)
            return
        if isinstance(structure, I18nMessageTypes):
            text = self.translate(structure)
        else:
            text = str(structure)
        if not (repldict or self.strictinsert):
            # Take a shortcut, no error checking
            self.stream_write(text)
            return
        if self.html:
            self.insertHTMLStructure(text, repldict)
        else:
            self.insertXMLStructure(text, repldict)

    def do_insertI18nStructure_tal(self, stuff):
        # TODO: Code duplication is BAD, we need to fix it later
        (expr, repldict, block) = stuff
        structure = self.engine.evaluateStructure(expr)
        if structure is not None:
            if structure is self.Default:
                self.interpret(block)
            else:
                if not isinstance(structure, TypesToTranslate):
                    structure = str(structure)
                text = self.translate(structure)
                if not (repldict or self.strictinsert):
                    # Take a shortcut, no error checking
                    self.stream_write(text)
                elif self.html:
                    self.insertHTMLStructure(text, repldict)
                else:
                    self.insertXMLStructure(text, repldict)

    def insertHTMLStructure(self, text, repldict):
        from zope.tal.htmltalparser import HTMLTALParser
        gen = AltTALGenerator(repldict, self.engine, 0)
        p = HTMLTALParser(gen)  # Raises an exception if text is invalid
        p.parseString(text)
        program, macros = p.getCode()
        self.interpret(program)

    def insertXMLStructure(self, text, repldict):
        from zope.tal.talparser import TALParser
        gen = AltTALGenerator(repldict, self.engine, 0)
        p = TALParser(gen)
        gen.enable(0)
        p.parseFragment('<!DOCTYPE foo PUBLIC "foo" "bar"><foo>')
        gen.enable(1)
        p.parseFragment(text)  # Raises an exception if text is invalid
        gen.enable(0)
        p.parseFragment('</foo>', 1)
        program, macros = gen.getCode()
        self.interpret(program)

    def do_evaluateCode(self, stuff):
        lang, program = stuff
        # Use a temporary stream to capture the interpretation of the
        # subnodes, which should /not/ go to the output stream.
        tmpstream = self.StringIO()
        self.pushStream(tmpstream)
        try:
            self.interpret(program)
        finally:
            self.popStream()
        code = tmpstream.getvalue()
        output = self.engine.evaluateCode(lang, code)
        self._stream_write(output)
    bytecode_handlers["evaluateCode"] = do_evaluateCode

    def do_loop(self, stuff):
        (name, expr, block) = stuff
        self.interpret(block)

    def do_loop_tal(self, stuff):
        (name, expr, block) = stuff
        iterator = self.engine.setRepeat(name, expr)
        while next(iterator):
            self.interpret(block)
    bytecode_handlers["loop"] = do_loop

    def translate(self, msgid, default=None, i18ndict=None,
                  obj=None, domain=None):
        if default is None:
            default = getattr(msgid, 'default', str(msgid))
        if i18ndict is None:
            i18ndict = {}
        if domain is None:
            domain = getattr(msgid, 'domain', self.i18nContext.domain)
        if obj:
            i18ndict.update(obj)
        if not self.i18nInterpolate:
            return msgid
        # TODO: We need to pass in one of context or target_language
        return self.engine.translate(msgid, self.i18nContext.domain,
                                     i18ndict, default=default)

    def do_rawtextColumn(self, stuff):
        (s, col) = stuff
        self._stream_write(s)
        self.col = col
    bytecode_handlers["rawtextColumn"] = do_rawtextColumn

    def do_rawtextOffset(self, stuff):
        (s, offset) = stuff
        self._stream_write(s)
        self.col = self.col + offset
    bytecode_handlers["rawtextOffset"] = do_rawtextOffset

    def do_condition(self, stuff):
        (condition, block) = stuff
        if not self.tal or self.engine.evaluateBoolean(condition):
            self.interpret(block)
    bytecode_handlers["condition"] = do_condition

    def do_defineMacro(self, stuff):
        (macroName, macro) = stuff
        wasInUse = self.inUseDirective
        self.inUseDirective = False
        self.interpret(macro)
        self.inUseDirective = wasInUse
    bytecode_handlers["defineMacro"] = do_defineMacro

    def do_useMacro(self, stuff,
                    definingName=None, extending=False):
        (macroName, macroExpr, compiledSlots, block) = stuff
        if not self.metal:
            self.interpret(block)
            return
        macro = self.engine.evaluateMacro(macroExpr)
        if macro is self.Default:
            macro = block
        else:
            if not isCurrentVersion(macro):
                raise METALError(
                    "macro %s has incompatible version %s" %
                    (repr(macroName), repr(
                        getProgramVersion(macro))), self.position)
            mode = getProgramMode(macro)
            if mode != (self.html and "html" or "xml"):
                raise METALError("macro %s has incompatible mode %s" %
                                 (repr(macroName), repr(mode)), self.position)
        self.pushMacro(macroName, compiledSlots, definingName, extending)

        # We want 'macroname' name to be always available as a variable
        outer = self.engine.getValue('macroname')
        self.engine.setLocal('macroname', macroName.rsplit('/', 1)[-1])

        prev_source = self.sourceFile
        wasInUse = self.inUseDirective
        self.inUseDirective = True
        self.interpret(macro)
        self.inUseDirective = wasInUse

        if self.sourceFile != prev_source:
            self.engine.setSourceFile(prev_source)
            self.sourceFile = prev_source
        self.popMacro()
        # Push the outer macroname again.
        self.engine.setLocal('macroname', outer)
    bytecode_handlers["useMacro"] = do_useMacro

    def do_extendMacro(self, stuff):
        # extendMacro results from a combination of define-macro and
        # use-macro.  definingName has the value of the
        # metal:define-macro attribute.
        (macroName, macroExpr, compiledSlots, block, definingName) = stuff
        extending = self.metal and self.inUseDirective
        self.do_useMacro((macroName, macroExpr, compiledSlots, block),
                         definingName, extending)
    bytecode_handlers["extendMacro"] = do_extendMacro

    def do_fillSlot(self, stuff):
        # This is only executed if the enclosing 'use-macro' evaluates
        # to 'default'.
        (slotName, block) = stuff
        self.interpret(block)
    bytecode_handlers["fillSlot"] = do_fillSlot

    def do_defineSlot(self, stuff):
        (slotName, block) = stuff
        if not self.metal:
            self.interpret(block)
            return
        macs = self.macroStack
        if macs:
            len_macs = len(macs)
            # Measure the extension depth of this use-macro
            depth = 1
            while depth < len_macs:
                if macs[-depth].extending:
                    depth += 1
                else:
                    break
            # Search for a slot filler from the most specific to the
            # most general macro.  The most general is at the top of
            # the stack.
            slot = None
            i = len_macs - 1
            while i >= (len_macs - depth):
                slot = macs[i].slots.get(slotName)
                if slot is not None:
                    break
                i -= 1
            if slot is not None:
                # Found a slot filler.  Temporarily chop the macro
                # stack starting at the macro that filled the slot and
                # render the slot filler.
                chopped = macs[i:]
                del macs[i:]
                try:
                    self.interpret(slot)
                finally:
                    # Restore the stack entries.
                    for mac in chopped:
                        mac.entering = False  # Not entering
                    macs.extend(chopped)
                return
            # Falling out of the 'if' allows the macro to be interpreted.
        self.interpret(block)
    bytecode_handlers["defineSlot"] = do_defineSlot

    def do_onError(self, stuff):
        (block, handler) = stuff
        self.interpret(block)

    def do_onError_tal(self, stuff):
        (block, handler) = stuff
        state = self.saveState()
        self.stream = stream = self.StringIO()
        self._stream_write = stream.write
        try:
            self.interpret(block)
        # TODO: this should not catch ZODB.POSException.ConflictError.
        # The ITALExpressionEngine interface should provide a way of
        # getting the set of exception types that should not be
        # handled.
        except BaseException:
            exc = sys.exc_info()[1]
            try:
                self.restoreState(state)
                engine = self.engine
                engine.beginScope()
                error = engine.createErrorInfo(exc, self.position)
            finally:
                # Avoid traceback reference cycle due to the __traceback__
                # attribute.
                del exc
            engine.setLocal('error', error)
            try:
                self.interpret(handler)
            finally:
                engine.endScope()
        else:
            self.restoreOutputState(state)
            self.stream_write(stream.getvalue())
    bytecode_handlers["onError"] = do_onError

    bytecode_handlers_tal = bytecode_handlers.copy()
    bytecode_handlers_tal["rawtextBeginScope"] = do_rawtextBeginScope_tal
    bytecode_handlers_tal["beginScope"] = do_beginScope_tal
    bytecode_handlers_tal["setLocal"] = do_setLocal_tal
    bytecode_handlers_tal["setGlobal"] = do_setGlobal_tal
    bytecode_handlers_tal["insertStructure"] = do_insertStructure_tal
    bytecode_handlers_tal["insertI18nStructure"] = do_insertI18nStructure_tal
    bytecode_handlers_tal["insertText"] = do_insertText_tal
    bytecode_handlers_tal["insertI18nText"] = do_insertI18nText_tal
    bytecode_handlers_tal["loop"] = do_loop_tal
    bytecode_handlers_tal["onError"] = do_onError_tal
    bytecode_handlers_tal["<attrAction>"] = attrAction_tal
    bytecode_handlers_tal["optTag"] = do_optTag_tal


class FasterStringIO(list):
    # text-aware append-only version of StringIO.
    write = list.append

    def __init__(self, value=None):
        list.__init__(self)
        if value is not None:
            self.append(value)

    def getvalue(self):
        return ''.join(self)


def _write_ValueError(s):
    raise ValueError("I/O operation on closed file")
