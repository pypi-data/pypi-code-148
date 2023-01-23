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
"""
Parse XML and compile to :class:`~.TALInterpreter` intermediate code,
using a :class:`~.TALGenerator`.
"""
from zope.tal.taldefs import XML_NS
from zope.tal.taldefs import ZOPE_I18N_NS
from zope.tal.taldefs import ZOPE_METAL_NS
from zope.tal.taldefs import ZOPE_TAL_NS
from zope.tal.talgenerator import TALGenerator
from zope.tal.xmlparser import XMLParser


class TALParser(XMLParser):
    """
    Parser for XML.

    After parsing with :meth:`~.XMLParser.parseFile`,
    :meth:`~.XMLParser.parseString`, :meth:`~.XMLParser.parseURL` or
    :meth:`~.XMLParser.parseStream`, you can call :meth:`getCode` to
    retrieve the parsed program and macros.
    """

    ordered_attributes = 1

    def __init__(self, gen=None, encoding=None):  # Override
        """
        :keyword TALGenerator gen: The configured (with an expression compiler)
            code generator to use. If one is not given, a default will be used.
        """
        XMLParser.__init__(self, encoding)
        if gen is None:
            gen = TALGenerator()
        self.gen = gen
        self.nsStack = []
        self.nsDict = {XML_NS: 'xml'}
        self.nsNew = []

    def getCode(self):
        """Return the compiled program and macros after parsing."""
        return self.gen.getCode()

    def StartNamespaceDeclHandler(self, prefix, uri):
        self.nsStack.append(self.nsDict.copy())
        self.nsDict[uri] = prefix
        self.nsNew.append((prefix, uri))

    def EndNamespaceDeclHandler(self, prefix):
        self.nsDict = self.nsStack.pop()

    def StartElementHandler(self, name, attrs):
        if self.ordered_attributes:
            # attrs is a list of alternating names and values
            attrlist = []
            for i in range(0, len(attrs), 2):
                key = attrs[i]
                value = attrs[i + 1]
                attrlist.append((key, value))
        else:
            # attrs is a dict of {name: value}
            attrlist = sorted(attrs.items())  # sort for definiteness
        name, attrlist, taldict, metaldict, i18ndict \
            = self.process_ns(name, attrlist)
        attrlist = self.xmlnsattrs() + attrlist
        self.gen.emitStartElement(name, attrlist, taldict, metaldict, i18ndict,
                                  self.getpos())

    def process_ns(self, name, attrlist):
        taldict = {}
        metaldict = {}
        i18ndict = {}
        fixedattrlist = []
        name, namebase, namens = self.fixname(name)
        for key, value in attrlist:
            key, keybase, keyns = self.fixname(key)
            ns = keyns or namens  # default to tag namespace
            item = key, value
            if ns == 'metal':
                metaldict[keybase] = value
                item = item + ("metal",)
            elif ns == 'tal':
                taldict[keybase] = value
                item = item + ("tal",)
            elif ns == 'i18n':
                i18ndict[keybase] = value
                item = item + ('i18n',)
            fixedattrlist.append(item)
        if namens in ('metal', 'tal', 'i18n'):
            taldict['tal tag'] = namens
        return name, fixedattrlist, taldict, metaldict, i18ndict

    _namespaces = {
        ZOPE_TAL_NS: "tal",
        ZOPE_METAL_NS: "metal",
        ZOPE_I18N_NS: "i18n",
    }

    def xmlnsattrs(self):
        newlist = []
        for prefix, uri in self.nsNew:
            if prefix:
                key = "xmlns:" + prefix
            else:
                key = "xmlns"
            if uri in self._namespaces:
                item = (key, uri, "xmlns")
            else:
                item = (key, uri)
            newlist.append(item)
        self.nsNew = []
        return newlist

    def fixname(self, name):
        if ' ' in name:
            uri, name = name.split(' ', 1)
            prefix = self.nsDict[uri]
            prefixed = name
            if prefix:
                prefixed = "{}:{}".format(prefix, name)
            ns = self._namespaces.get(uri, "x")
            return (prefixed, name, ns)
        return (name, name, None)

    def EndElementHandler(self, name):
        name = self.fixname(name)[0]
        self.gen.emitEndElement(name, position=self.getpos())

    def DefaultHandler(self, text):
        self.gen.emitRawText(text)


def test():
    import sys
    p = TALParser()
    file = "tests/input/test01.xml"
    if sys.argv[1:]:
        file = sys.argv[1]
    p.parseFile(file)
    program, macros = p.getCode()
    from zope.tal.dummyengine import DummyEngine
    from zope.tal.talinterpreter import TALInterpreter
    engine = DummyEngine(macros)
    TALInterpreter(program, macros, engine, sys.stdout, wrap=0)()


if __name__ == "__main__":
    test()
