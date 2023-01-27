from __future__ import annotations, print_function
from Latex import Latex
from Project import Project
from Utility import Utility
input = Utility.input()
class Trigram:
    """Supply it a semitone position list"""

    allowedWays = [
        "symbol",
        "name",
        "chinese",
        "pinyin",
        "subChange",
        "subpage",
        "syllable",
        "other syllable",
        "both syllable",
    ]
    printWays = [
        "symbol",
        "name",
        "chinese",
        "pinyin",
        "subChange",
        "subpage",
    ]
    lineProportion = 0.5
    '''book = Book(
        notesToUse=["b2", "2"],
        notesToInclude=["1"],
    )'''
    notesets = {}
    notesets[(0,)] = {
        "symbol": "☳",
        "name": "Lightning",
        "adjective": "Enlightening",
        "pinyin": "zhèn",
        "chinese": "震",
        "subpage": 1,
        "vowel": "a",
        "consonant": "b",
    }
    notesets[(0, 1,)] = {
        "symbol": "☱",
        "name": "Valley",
        "pinyin": "duì",
        "chinese": "兌",
        "subpage": 2,
        "vowel": "e",
        "consonant": "d",
    }
    notesets[(0, 2,)] = {
        "symbol": "☲",
        "name": "Fire",
        "pinyin": "lí",
        "chinese": "離",
        "subpage": 3,
        "vowel": "i",
        "consonant": "g",
    }
    notesets[(0, 1, 2,)] = {
        "symbol": "☰",
        "name": "Heaven",
        "pinyin": "qián",
        "chinese": "乾",
        "subpage": 4,
        "vowel": "o",
        "consonant": "v",
    }
    notesets[()] = {
        "symbol": "☷",
        "name": "Earth",
        "pinyin": "kūn",
        "chinese": "坤",
        "subpage": -1,
        "vowel": "A",
        "consonant": "p",
    }
    notesets[(1,)] = {
        "symbol": "☵",
        "name": "Water",
        "pinyin": "kǎn",
        "chinese": "坎",
        "subpage": -2,
        "vowel": "E",
        "consonant": "t",
    }
    notesets[(2,)] = {
        "symbol": "☶",
        "name": "Mountain",
        "pinyin": "gèn",
        "chinese": "艮",
        "subpage": -3,
        "vowel": "I",
        "consonant": "k",
    }
    notesets[(1, 2,)] = {
        "symbol": "☴",
        "name": "Wind",
        "pinyin": "xùn",
        "chinese": "巽",
        "subpage": -4,
        "vowel": "O",
        "consonant": "f",
    }

    """first version of consonants brackets == alphabetical
    1 : b       b    (b)   v
    2 : d       c    (d)   g
    3 : f       d    (g)   b
    4 : g       f    (v)   d
    -1: j   p   p/v   p   (f)
    -2: k   t   s     t   (k)
    -3: l   v         k   (p)
    -4: m   j         f   (t)     """

    """first version of vowels
    https://www.quora.com/What-is-the-difference-between-e-%C3%A8-%C3%A9-%C3%AA-%C3%AB-%C4%93-%C4%97-and-%C4%99
    1 : a
    2 : e     è
    3 : i
    4 : o
    -1: é     ý     ā     ē   ī    ō
    -2: ou    ea
    -3: ai
    -4: u"""
    if Latex.on and Latex.replaceBuggyPinyinChars and not Project.makeWebAssets:
        
        print(
            "If you want LaTex to make nice pinyin chars you should disable Project.makeWebAssets!!\n"
            * 3
        )
        for i in notesets:
            for replacement in Latex.pinyinReplacements:
                notesets[i]["pinyin"] = notesets[i]["pinyin"].replace(
                    replacement, Latex.pinyinReplacements[replacement]
                )

    @classmethod
    def makeTrigramTable(
        cls, rewriteProjectFile=True, flipAxes=True, rewriteFile=True
    ) -> str:
        printWays = Trigram.allowedWays + ["Jazz", "Change Number"]
        printWays.remove("both syllable")
        _ways = Trigram.allowedWays
        _str = ""
        rows = []
        for t, trigram in enumerate(Trigram.notesets):
            rows.append([])
            for way in printWays:
                if way in Trigram.allowedWays:
                    # rows[-1].append(Tetragram.notesets[tetragram][way])
                    rows[-1].append(
                        Change.makeFromSet(trigram).getTrigram(
                            [way], decorateWithSmallCircle=True, useTabbingImg=True
                        )[0]
                    )
                else:
                    # print(Change.isValidWay('Change Number'))
                    # input('else' + way)

                    if way == "subChange":
                        way = "Change Number"
                    if Change.isValidWay(way):
                        # input('is valid change way')
                        for t, transposition in enumerate((0, 3, 6, 9)):
                            _change = Change.makeFromSet(
                                [s + transposition for s in trigram]
                            )
                            _byWay = _change.byWays(way)
                            if type(_byWay) in (list, Change):
                                rows[-1].append(" ".join(_byWay))
                            else:
                                rows[-1].append(_byWay)
                    else:
                        raise TypeError("{} is not a validWay of Change".format(way))

        if flipAxes:
            rows = Utility.flipAxesOfList(rows)
        _str += Latex.makeTabular(rows)
        if rewriteFile:
            _filename = Project.trigramTableFilename
            text_file = open(_filename, "w", encoding="utf-8")
            try:
                text_file.write("%s" % _str)
            except Exception as e:
                input(_str + " wtf!!!!" + str(e))
            text_file.close()
            print("rewrote", _filename)
        print(_str)
        input("thar be rows")

    @classmethod
    def OLDmakeTrigramTable(cls, rewriteProjectFile=True) -> str:
        _str = ""
        _ways = Trigram.allowedWays + ["Jazz"]
        _trigramBook = Book(["1", "b2", "2"])
        _positivetrigrams = [_trigramBook[i] for i in range(0, 4, +1)]
        _negativetrigrams = [i.withoutNote("1") for i in _positivetrigrams]
        _allTrigrams = _negativetrigrams + _positivetrigrams
        # _tabs = len(_ways)
        _tabs = 0
        for way in _ways:
            if way in Trigram.allowedWays:
                _tabs += 1
            elif Change.isValidWay(way):
                _tabs += 4

        _str += "\\begin{tabular}{" + "| l" * _tabs + "|}\n"
        _str += "\\hline\n"
        for trigram in _allTrigrams:
            print("trrigram", trigram.__repr__())
            for w, way in enumerate(_ways):
                if way in Trigram.allowedWays:
                    print(trigram.getTrigram([way])[0])
                    _str += trigram.getTrigram([way])[0]
                    if w < len(_ways) - 1:
                        _str += " & "
                elif Change.isValidWay(way):
                    print("trigram", trigram)
                    for transposition in range(4):
                        print([i + transposition * 3 for i in trigram.getSemitones()])
                        _transposedTrigram = Change.makeFromSet(
                            [i + transposition * 3 for i in trigram.getSemitones()]
                        )
                        print(
                            "_transposedTrigram.byWays(way)",
                            _transposedTrigram.byWays(way),
                        )
                        _str += " ".join(_transposedTrigram.byWays(way))
                        _str += " & "
                        # _str += ' & '.join([str(i.byWays(way)) for i in _transposedTrigrams])
                        print("_transposedTrigrams {}".format(_transposedTrigram))
            _str += "\\\\\\hline\n"
        _str += "\\end{tabular}"
        while "& \\\\" in _str:
            _str = _str.replace("& \\\\", "\\\\")
        if rewriteProjectFile:
            _filename = Project.trigramTableFilename
            text_file = open(_filename, "w")
            text_file.write("%s" % _str)
            text_file.close()
            print("rewrote", _filename)
        return _str

    @classmethod
    def makeBlankMapping(cls, mappingName: str):
        for i in range(65):
            print(mappingName + ".insert(" + str(i) + ",0) #" + names[i])
        input("now?")

    @classmethod
    def allPinyin(cls):
        for i in cls.notesets.keys():
            print(cls.notesets[i]["pinyin"])