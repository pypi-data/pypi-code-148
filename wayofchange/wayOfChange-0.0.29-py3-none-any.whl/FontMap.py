from Unicode import Unicode
from Utility import Utility
input = Utility.input
class FontMap:
    "🐶🐺🐱🐭🐹🐰🐸🐯🐨🐻🐷🐽🐮🐗🐵🐒🐴🐑🐘🐼🐧🐦🐤🐥🐣🐔🐍🐢🐛🐝🐜🐿🐞🐌🐙🐚🐠🐟🐬🐳🐋🐄🐏🐀🐃🐅🐇🐉🐎🐐🐓🐕🐖🐁🐂🐲🐡🐊🐫🐪🐆🐈🐩🐾🦀🦁🦂🕷🦃🦄🦐🦑🦋🦍🦊🦌🦏🦇🦅🦆🦉🦎🦈🦓🦒🦔🦕🦖🦝🦙🦛🦘🦡🦢🦚🦜🦟🐻‍❄️🦭🐃🪱🦬🪳🦣🦤🐈‍⬛🦗🦫🪲🪰"
    "No, abacus treble clef  or plus minus unicode disable"

    latexFontStyles = [
        "BoldFont",
        "ItalicFont",
        "BoldItalicFont",
        "SlantedFont",
        "BoldSlantedFont",
        "SmallCapsFont",
        "UprightFont",
    ]
    fontFamilies = {
        "chinese": {
            "latexName": "cj",
            "fontName": "SimSun",
            "chars": ["。", "道德经", "易經", "易经", "易經", "太玄經"],
        },
        "symbol 1 alt": {
            "latexName": "symbZ",
            "fontName": "Symbola",
            "chars": [
                         "🐜","🎪", "🦀",'🐛','☯','❄',

                "𝄻",
                "𝄼",
                "𝄽",
                "𝄾",
                "🠥",
                "🠧",
                "➿",
                "🔮",

                "👐",
                "🍀",
                "🍂",
                "💐",
                "🏯",
                "🍁",
                "🌿",
                "❂",
                "🌴",
                "⚊",
                "⚋",
                "𝅜",
                "𝅘𝅥𝅯",
                "𝅘𝅥𝅰",
                "𝅘𝅥𝅱",
                "𝅘𝅥𝅲",

                "🐭",
                "🐘",
                "🐡",
                "🐍",
                "🐞",
                "🦀",  # '\U0001F600'🦀,🦀 #Crab🦀🦀🦀🦀🦀🦀🦀🦀🦀'
                "🐙",
                "🐌",
                "🙉",
                "⨍",
                "🐒",
                "🐫",
                "🐳",
                "🐰",
                "🌈",
                "🌱",
                "🌵",
                     ]
                     
        },

        "symbol 1": {
            "latexName": "symbA",
            #"fontName": "Symbola_monospacified_for_DejaVuSansMono",
            "fontName": "Symbola_monospacified_for_DejaVuSansMono",
            "chars": [

            ]
            + Unicode.romanNumeralCapitals
            + Unicode.romanNumeralLowercase,
        },
        "symbol black": {
            "latexName": "symbB",
            "fontName": "seguisym",
            "chars": [
                "⚬",

                "│",
                "┃",
                "╽",
                "╿",
                "╏",
                "║",
                "┆",
                "╵",
                "〡",
                "〢",
                "╹",
                "╻",
                "╷",
                "〣",
            ],
        },
        "music symbol": {
            "latexName": "symbM",
            "fontName": "MuseJazzText_9",
            "chars": ["♮", "♭", "♯", "𝄫", "𝄪", "𝅝", "𝅗𝅥", "♩", "♪", ""],
        },
        "obscure unicode": {
            "latexName": "symbC",
            "fontName": "unifont-11.0.02",
            "chars": ["🧮"],
        },
        "alt font 1": {"latexName": "altFA", "fontName": "sylfaen", "chars": []},
        "jazzA": {"latexName": "jazzA", "fontName": "JAZZTEXT", "chars": []},#JAZZTEXT, THWACK  PetalumaScript
        "jazzB": {"latexName": "jazzB", "fontName": "ADD-JAZZ", "chars": []},
        "british": {"latexName": "britA", "fontName": "rm-albion", "chars": []},
        "british embossed": {
            "latexName": "britB",
            "fontName": "GrafikText",
            "chars": [],
        },
        "celtic embossed": {
            "latexName": "britC",
            "fontName": "FrakturShadowed",
            "chars": [],
        },
        "block letter A": {
            "latexName": "boldA",
            "fontName": "AbrilFatface-Regular",
            "chars": [],
        },
        "block letter B": {
            "latexName": "boldB",
            "fontName": "GramophoneNF",
            "chars": [],
        },
        "extra bold": {
            "latexName": "boldC",
            "fontName": "texgyrebonum-bold",
            "chars": [],
        },
    }

    fontByWay = {
        "Jazz": {"latexName": "jazz", "fontName": "JAZZTEXT", "italic": "ADD-JAZZ"},
        "Carnatic": {
            "latexName": "carn",
            "fontName": "DorovarflfCarolus-axyg",
            "ItalicFont": "DorovarflfItalic-EaX8",
        },
        "Hexagram": {"latexName": "hexa", "fontName": "GramophoneNF"},
        "Word": {"latexName": "wayofword", "fontName": "MonkeyFingersNF"},
        #'Word': {'latexName': 'wayofword', 'fontName': 'DorovarflfCarolus-axyg','ItalicFont':'DorovarflfItalic-EaX8'},
        "Change Number": {
            "latexName": "changenumber",
            "fontName": "AbrilFatface-Regular",
        },
        "Scale Name": {"latexName": "scalename", "fontName": "AbrilFatface-Regular"},
        #'Change Number': {'latexName': 'changenumber', 'fontName': 'PastiRegular-mLXnm','ItalicFont':'PastiOblique-7B0wK'},
    }
    omitSymbols = [
        "",
        " ",
        "+/-",
        "+",
        "-",
        ",",
        ".",
        ":",
        "±",
        "№",
        "🧮",
        "°",
        "Δ",
        "a",
        "A",
        "b",
        "B",
        "c",
        "C",
        "d",
        "D",
        "e",
        "E",
        "f",
        "F",
        "g",
        "G",
        "h",
        "H",
        "i",
        "I",
        "j",
        "J",
        "k",
        "K",
        "l",
        "L",
        "m",
        "M",
        "n",
        "N",
        "o",
        "O",
        "p",
        "P",
        "q",
        "Q",
        "r",
        "R",
        "s",
        "S",
        "t",
        "T",
        "u",
        "U",
        "v",
        "V",
        "w",
        "W",
        "x",
        "X",
        "y",
        "Y",
        "z",
        "Z",
    ]

    cjkRanges = [
        {"from": ord("\u3300"), "to": ord("\u33ff")},  # compatibility ideographs
        {"from": ord("\ufe30"), "to": ord("\ufe4f")},  # compatibility ideographs
        {"from": ord("\uf900"), "to": ord("\ufaff")},  # compatibility ideographs
        {
            "from": ord("\U0002F800"),
            "to": ord("\U0002fa1f"),
        },  # compatibility ideographs
        {"from": ord("\u3040"), "to": ord("\u309f")},  # Japanese Hiragana
        {"from": ord("\u30a0"), "to": ord("\u30ff")},  # Japanese Katakana
        {"from": ord("\u2e80"), "to": ord("\u2eff")},  # cjk radicals supplement
        {"from": ord("\u4e00"), "to": ord("\u9fff")},
        {"from": ord("\u3400"), "to": ord("\u4dbf")},
        {"from": ord("\U00020000"), "to": ord("\U0002a6df")},
        {"from": ord("\U0002a700"), "to": ord("\U0002b73f")},
        {"from": ord("\U0002b740"), "to": ord("\U0002b81f")},
        {
            "from": ord("\U0002b820"),
            "to": ord("\U0002ceaf"),
        },  # included as of Unicode 8.0
    ]

    def is_cjk(char):
        return any(
            [range["from"] <= ord(char) <= range["to"] for range in FontMap.ranges]
        )

    @classmethod
    def makeFontMapTex(cls, absolutePathToFonts=False, saveEveryCharToFile=True):
        # https://texdoc.org/serve/fontspec/0
        _fontPathCommand = "\\FontPath"
        #_fontPath = "F:/wayOfChange"
        _fontPath = os.getcwd()
        _tex = "\providecommand*{{{}}}{{{}}}\n".format(_fontPathCommand, _fontPath)
        _tex += """\RequirePackage{fontspec}
\RequirePackage{newunicodechar}
"""
        #input(_tex)
        _glyphs = []
        _glyphsChi = []
        _glyphsSym = []

        # for idx,i in enumerate({**Trigram.notesets, **Tetragram.notesets}):
        """for idx,i in enumerate({**Trigram.notesets, **Tetragram.notesets}):

            _nGram = [Trigram,Tetragram][idx]
            print(i, idx,_nGram,_nGram.notesets)
            for s in _nGram.notesets:
                for char in s:
                    _glyphs.append(_nGram.notesets[s]['chinese'])
       """
        for f in (FontMap.fontFamilies, FontMap.fontByWay):
            for i in f:
                _fam = f[i]
                _fontName = _fam["fontName"]
                _fontFiletype = None
                _fontCandidate = os.path.join(_fontPath, _fontName)
                for extension in ("otf", "ttf", "ttc"):
                    if _fontFiletype is None and os.path.exists(
                        _fontCandidate + "." + extension
                    ):
                        _fontFiletype = extension
                        _fontCandidate += "." + extension
                if _fontFiletype is None:
                    raise FileNotFoundError(
                        "The font does not exist at {}. You may not be able to render stuff right or other problems".format(_fontCandidate)
                    )
                if absolutePathToFonts:
                    _tex += (
                        "\\newfontfamily{\\"
                        + _fam["latexName"]
                        + "}{"
                        + _fontPath
                        + "/"
                        + _fam["fontName"]
                        + "."
                        + _fontFiletype
                        + "}%\n"
                    )
                else:
                    _tex += (
                        "\\newfontfamily{\\"
                        + _fam["latexName"]
                        + "}{"
                        + _fam["fontName"]
                        + "."
                        + _fontFiletype
                        + "}"
                    )
                    _fontVariants = {}
                    for k, variant in enumerate(FontMap.latexFontStyles):
                        if variant in _fam:
                            # input(FontMap.latexFontStyles[k])
                            # input(str(_fam[variant]))
                            _fontVariantFiletype = None
                            _fontCandidate = os.path.join(
                                _fontPath, _fontName
                            )
                            for extension in ("otf", "ttf", "ttc"):
                                if _fontVariantFiletype is None and os.path.exists(
                                    _fontCandidate + "." + extension
                                ):
                                    _fontVariantFiletype = extension
                                    _fontCandidate += "." + extension
                                    _fontVariants[variant] = {
                                        "fontName": _fontCandidate,
                                        "Extension": extension,
                                    }
                            if _fontVariantFiletype is None:
                                raise FileNotFoundError(
                                    "The font does not exist at {}".format(
                                        _fontCandidate
                                    )
                                )
                    # _tex += '[\n    Extension = .'+_fontFiletype+' ,'

                    if len(_fontVariants) >= 1:
                        _tex += "["
                        for k, variant in enumerate(_fontVariants):
                            _tex += (
                                "\n    "
                                + variant
                                + " = { "
                                + _fam[variant]
                                + "."
                                + _fontVariantFiletype
                                + " }"
                            )
                            if k < (len(_fontVariants) - 1):
                                _tex += ","
                        _tex += "\n]"
                    # _tex += '\n]'

                    _tex += "%\n"

        # \newfontfamily{\cj}{SimSun}

        # Get chinese in
        for i in Hexagram.chinese:
            for char in i:
                _glyphsChi.append(char)
        for s in Trigram.notesets:
            _chinese = Trigram.notesets[s]["chinese"]
            for char in _chinese:
                _glyphsChi.append(char)
        for s in Tetragram.semitones:
            _chinese = Tetragram.semitones[s]["chinese"]
            for char in _chinese:
                _glyphsChi.append(char)
        for s in Tetragram.ternaryList:
            _chinese = Tetragram.ternaryList[s]["chinese"]
            for char in _chinese:
                _glyphsChi.append(char)
        _glyphsChi.append(Book.unicodeChars["Hexagram Chinese"])
        _glyphsChi.append(Book.unicodeChars["Tetragram Chinese"])
        for char in Book.unicodeChars["IChing Chinese"]:
            _glyphsChi.append(char)
        for i in FontMap.fontFamilies["chinese"]["chars"]:
            for c in i:
                _glyphsChi.append(c)
        for i in _glyphsChi:
            if i not in FontMap.omitSymbols and i not in _glyphs:
                _tex += (
                    "\\newunicodechar {"
                    + i
                    + "}{{\\"
                    + FontMap.fontFamilies["chinese"]["latexName"]
                    + " "
                    + i
                    + "}}"
                )
                _tex += "%\n"
                _glyphs.append(i)

        for i in Book.unicodeChars:
            i = Book.unicodeChars[i].replace(" ", "").replace("\hfill", "")
            _fontFamily = FontMap.fontFamilies["symbol 1"]["latexName"]
            if i not in FontMap.omitSymbols and i not in _glyphs:
                _fontFamily = FontMap.fontFamilies["symbol 1"]["latexName"]
                for f in FontMap.fontFamilies:
                    if i in FontMap.fontFamilies[f]["chars"]:
                        _fontFamily = FontMap.fontFamilies[f]["latexName"]
                        break
                for c in i:
                    if c not in FontMap.omitSymbols and c not in _glyphs:
                        _hackStrEnd = ''
                        _hackStrBeginning = ''
                        if i == Book.unicodeChars['Sharp']:
                            #https://tex.stackexchange.com/questions/57788/understanding-ifnextchar
                            _hackStrEnd =  ' \\kern-.42ex'
                            _hackStrBeginning =''
                            #input('abddfbadbfbdf')
                        _tex += (
                            "\\newunicodechar {"
                            + c
                            + "}{"+_hackStrBeginning+"{\\"
                            + _fontFamily
                            + " "
                            + c
                            + "}}{}}}".format(_hackStrEnd)
                            + "%\n"
                        )
                        _glyphsSym.append(i)
                        _glyphs.append(i)
        for i in Zodiac.semitoneToZodiac:
            _fontFamily = FontMap.fontFamilies["symbol 1"]["latexName"]
            for c in i:
                if c not in FontMap.omitSymbols and c not in _glyphs:
                    _tex += (
                        "\\newunicodechar {"
                        + c
                        + "}{{\\"
                        + _fontFamily
                        + " "
                        + c
                        + "}}"
                        + "%\n"
                    )
                _glyphs.append(c)
        for i in Braille.semitonesFF:
            _fontFamily = FontMap.fontFamilies["symbol 1"]["latexName"]
            i = Braille.semitonesFF[i]
            # input(i)
            for c in i:
                if c not in FontMap.omitSymbols and c not in _glyphs:
                    _tex += (
                        "\\newunicodechar {"
                        + c
                        + "}{{\\"
                        + _fontFamily
                        + " "
                        + c
                        + "}}"
                        + "%\n"
                    )
                _glyphs.append(c)
        for i in (
            Hexagram.symbol[1:]
            + [Tetragram.semitones[t]["symbol"] for t in Tetragram.semitones.keys()]
            + [Trigram.notesets[t]["symbol"] for t in Trigram.notesets.keys()]
        ):
            _fontFamily = FontMap.fontFamilies["symbol black"]["latexName"]

            print(i,end=' ')
            for c in i:
                if c not in FontMap.omitSymbols and c not in _glyphs:
                    _tex += (
                        "\\newunicodechar {"
                        + c
                        + "}{{\\"
                        + _fontFamily
                        + " "
                        + c
                        + "}}"
                        + "%\n"
                    )
                _glyphs.append(c)

        for i in list(Change.infoWaySymbols):
            i = Change.infoWaySymbols[i].replace(" ", "").replace("\hfill", "")
            _fontFamily = FontMap.fontFamilies["symbol 1"]["latexName"]
            for f in FontMap.fontFamilies:
                if i in FontMap.fontFamilies[f]["chars"]:
                    _fontFamily = FontMap.fontFamilies[f]["latexName"]
                    break
            if i not in FontMap.omitSymbols and i not in _glyphs:
                for c in i:
                    if c not in FontMap.omitSymbols and c not in _glyphs:
                        _tex += (
                            "\\newunicodechar {"
                            + c
                            + "}{{\\"
                            + _fontFamily
                            + " "
                            + c
                            + "}}"
                            + "%\n"
                        )
                _glyphsSym.append(i)
                _glyphs.append(i)
        for family in FontMap.fontFamilies:
            for symbols in FontMap.fontFamilies[family]["chars"]:
                for char in symbols:
                    if char not in FontMap.omitSymbols and char not in _glyphs:
                        _tex += (
                            "\\newunicodechar {"
                            + char
                            + "}{{\\"
                            + FontMap.fontFamilies[family]["latexName"]
                            + " "
                            + char
                            + "}}"
                            + "%\n"
                        )
                        _glyphs.append(char)
        # check it out
        if len(set(_glyphs)) != len(_glyphs):
            _differenceInGlyphs = set([x for x in _glyphs if _glyphs.count(x) > 1])
            print("Shouldn't be duplicates in glyphs\n{}. Duplicates are: {}".format(
                    _glyphs, _differenceInGlyphs))
            raise TypeError(
                "Shouldn't be duplicates in glyphs\n{}. Duplicates are: {}".format(
                    _glyphs, _differenceInGlyphs
            )
            )
        '''
\directlua
{
 fonts.handlers.otf.addfeature
  {
    name = "ktest",
    type = "kern",
    data =
        {
            ["1"] = { 
                      ["1"] =  -200 ,
                      ["2"] =  -200 
                    },
        },
  }
 }'''
        _filename = Project.fontMapTexPath
        text_file = open(_filename, "w+", encoding="UTF-8")
        if _tex[-1] == "\n":
            _tex = _tex[0:-1]
        text_file.write(_tex)
        # text_file.write("%s" % _tex)
        text_file.close()
        print(_tex)

        print("glyphs " + " ".join(_glyphs))
        print("updated " + _filename)
        print("no of glyphs", len(_glyphs))
        print("updated the file: fontmap at " + _filename)
        if saveEveryCharToFile:
            _filename = _filename.replace('.tex','CharSample.tex')
            text_file = open(_filename, "w+", encoding="UTF-8")
            text_file.write(' '.join(_glyphs))
            text_file.close()
            print('wrote 1 of every glyph to {}'.format(_filename))

        return _tex

        # Hexagrams
        # Book symbols