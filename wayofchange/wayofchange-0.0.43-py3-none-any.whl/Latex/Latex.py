from __future__ import annotations, print_function
import os
from PIL import ImageFont
from Utility import Utility
input = Utility.input
class Latex:
    # \begin{table}[ht]

    fontPath = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
    #fontPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    lualatexInterpreter = "lualatex"
    mostCellsOfAResult = 0.5
    biggestCell = "Arr!"
    mostPointsOfCell = 0
    # 3.8588235294117648   164 pts wide
    # commandStrings['Line Break Scale Names] = .02
    commandStrings = {
        "Small Circle Command Start": "\\protect\\authorimg{",
        "Small Circle Command End": "}",
        "Small Circle Small Command Start": "\\protect\\tabbingimg{",
        "Small Circle Small Command End": "}",
        "Small Piano Command Start": "\includegraphics[height=0.75em]{{",
        "Small Piano Command End": "}}",
        "Small Piano Command Start Svg": "\includesvg[height=0.75em]{{",
        "Small Piano Command End Svg": "}}",
        "Line Break With Space": "\\\\[-.1\\baselineskip]\n",
        "Line Break": "\\\\[-.1\\baselineskip]\n",  # 'Line Break': '\\\\\n',
        "Line Break Default": "\\\\\n",  # 'Line Break': '\\\\\n',
        "Line Break Scale Names": "\\\\[-.1\\baselineskip]\n",
        "Line Break Small": "\\\\[-.2\\baselineskip]\n",
        "Table Line Break": "\\\\",
        "Page Break": "\\newpage\\noindent\n",
        "Start Table": " \\begin{table}[th]\n\\centering",
        "End Table": "\\end{table}\n",
        "End Tabular": "\\end{tabular}\n",
        "Highlight Start": "\\sethlcolor{",
        "Highlight End": "\\hl",
        "Colour Cell": "\cellcolor{",
        "Colour Box": "\\colorbox{",
        "End Colour Box": "\hrulefill",
        "Colour Text": "\\textcolor{",
        "Start Figure": "\\begin{figure}[H]{}",
        "End Figure": "\\end{figure}\n",
        "Clear Page": "\\clearpage\n",
        "No Indent": "\\noindent",
    }
    # 'Start Figure': '\\begin{figure}[htpb]{}'

    # Colour Box: \colorbox{
    makeTextColoured = True
    makeGraphicsColoured = False
    useSmallCircles = True
    insertBackgroundDiagram = True
    backgroundDiagramType = "FCircle"
    backgroundDiagramFiletype = "pdf"
    # These commands are defined in preamble.tex
    imageTags = ("guitarimg","tabbingimg", "bigtabbingimg", "authorimg", "bigimg", "hexagramimg",'pianoimg',"bigpianoimg",)
    backgroundDiagramResolution = 2048
    useRelativeGraphicsPath = True
    SmallCircleResolution = 64
    SmallCircleTabbingResolution = 64
    useSmallCirclesMultiColourSchemes = True
    makeTexFilesSubfiles = True
    tables = True
    on = True
    colourTypes = ["Colour Box", "Colour Text", "Colour Cell"]
    inkSaver = True
    # always keep blackPaper == False, because the colouring is controlled through LaTeX
    blackPaper = False
    wayOfSpace = True
    forceColourCells = False
    removeTextColourFromColouredCells = True
    replaceBuggyPinyinChars = True
    lineBreakClosesTabular = False
    lineBreakWithLine = False
    # fontStr = 'Symbola_hint.ttf'
    fontStr = os.path.join(fontPath,"symbol.ttf")
    # fontStr = 'PalatinoLinotype-RomanSymbolize_3.otf'
    fontSize = 12
    fontSizeSmall = 10
    fontSizeScriptsize = 8
    # fontSize = 12
    widthOfColSepInt = 1.4
    # widthOfColSepInt = 2
    # widthOfPage = 566
    # inch to pts is multiply by 72
    # mm to pts is multiply by 2.83465
    # pts
    widthOfPage = 585
    # widthOfPage = 612
    longWay = "Mneum ---"
    # mm
    widthOfLeftMargin = 10
    widthOfRightMargin = 10
    # -> to pts
    widthOfLeftMargin *= 2.83465
    widthOfRightMargin *= 2.83465
    widthOfPage -= widthOfLeftMargin + widthOfRightMargin
    # letterSpace = 0
    # I don't think letterSpace is doing anything
    letterSpace = -10

    try:
        font = ImageFont.truetype(fontStr, fontSize)
    except:
        raise ValueError("{} missing from fonts.".format(fontStr))
    fontFixed = ImageFont.truetype(fontStr, fontSize)
    pointSize = 0.03514597529378521  # This is measured in millimetres
    # linesPerPage = 56
    linesPerPage = 60  # 58 55
    if wayOfSpace:
        # make em 15 when rendering long

        numberOfCells = 14

    # The 2 stands for cm
    # widthOfFirstCellInt = math.floor(2 / pointSize)

    # measured in pts
    # widthOfColSepInt = font.getsize('.')[0]

    widthOfFirstCellInt = fontFixed.getsize(longWay)[0]
    widthOfFirstCellInt *= pointSize
    widthOfFirstCellStr = str(round(widthOfFirstCellInt, 2)) + "cm"

    # widthOfFirstCellStr = str(math.floor(widthOfFirstCellInt)) + 'pts'
    widthOfCellInt = ((widthOfPage - (widthOfFirstCellInt / pointSize))) / (
        numberOfCells - 1
    )
    # widthOfCellInt -= widthOfColSepInt
    widthOfCellInt *= pointSize
    # widthOfCellStr = str(math.floor(widthOfCellInt)) + 'pts'
    widthOfCellStr = str(round(widthOfCellInt, 2)) + "cm"

    # input(widthOfFirstCellStr + str(widthOfFirstCellInt))
    # input(widthOfCellStr + str(widthOfCellInt))
    pinyinReplacements = {
        "ǐ": "\\u{i}",
        "ǚ": "\\u{u}",
        "ǎ": "\\u{a}",
        "ǒ": "\\u{o}",
        "ǔ": "\\u{u}",
        "ū": "\\={u}",
        "ě": "\\u{e}",
    }

    # ě is not needed, just to provide consistency is it there

    @classmethod
    def makeTextStyledByWay(cls,text:str,way):
        
        textType=type(text)

        text = str(text)
        if textType is list:
            raise TypeError('wrong type')
        assert type(text) is not list, str(type(text)) +' ' +  str(text)
        for w in ('Jazz','Change Number'):
            if w in way:
                way = w
        if way in ('Tritone Sub',):
            way = 'Jazz'
        if any([w in way for w in ('Consonant','Syllable','Word')]):
            way = 'Word'
        try:
            FontMap
        except NameError:
            from FontMap import FontMap
        if way in FontMap.fontByWay.keys():
            text = '{\\'+FontMap.fontByWay[way]['latexName'] + ' ' + text + '}'
        elif way != 'Codon':
            #input(text)
            warnings.warn('Skipping styling text because '+way + ' not in FontMap.fontByWay:\n' + str(FontMap.fontByWay.keys()))
        return text

    @classmethod
    def tabTo(cls, amount):
        return (
            "\protect\\tabto{"
            + str(round(float(amount.replace("Tab To ", "")), 3))
            + "\\textwidth}"
        )

    @classmethod
    def expressRBGinLatex(cls, rgb):
        print('we are in a strange place here')
        input(Colour.getTransposedColours())

    @classmethod
    def wrapChangeDataWithPreambleEtc(cls, data: str, outputType="GrailOfScale") -> str:
        if outputType not in ("GrailOfScale", "ChordsOfChange"):
            raise ValueError("bla bla bla :)")
        _str = ""
        # https: // tex.stackexchange.com / questions / 21904 / input - and -absolute - paths
        # _str += "\makeatletter\def\input@path{{{}}}\makeatother\n".format(Project.directoryTex.replace('\\','/'))
        # %or: \def\input@path{{/path/to/folder/}{/path/to/other/folder/}}
        _str += (
            "\\providecommand*{\\ProjectPath}{"
            + Project.directory.replace("\\", "/")
            + "}\n"
        )
        if outputType == "GrailOfScale":
            _str += "\\documentclass[a4paper]{article}\n"
            _str += "\\input{\\ProjectPath/tex/preamble}"
        elif outputType == "ChordsOfChange":
            pass
            _str += "\\documentclass{standalone}\n"
            _str += "\\input{\\ProjectPath/tex/preamble}"

            _str += "\\usepackage{tcolorbox}\n"
            _str += "\\usepackage{tikz}\n"
            _str += "\\usepackage{tabto}\n"
            _str += "\\begin{document}\n"
            # _str += '\\input{\\ProjectPath/tex/chordsOfChangeSinglePreamble}'
        # _str += '\\begin{document}\n'
        _str += data
        if outputType == "ChordsOfChange":
            _str += "\\end{document}"
        # _str += '\\end{document}'
        return _str

    @classmethod
    def getTexPath(
        cls,
        change: Change,
        key: Key,
        outputType="GrailOfScale",
        includeProjectPath=True,
        includeFilename=True,
        externalGraphicsPath=False,
    ):
        """returns the path for the .tex file required to compile a .pdf for that change"""

        if outputType not in ("GrailOfScale", "ChordsOfChange"):
            raise ValueError("bla bla bla :)")
        if includeProjectPath:
            _path = Project.directoryTex
        else:
            _path = Project.directoryTex.replace(Project.directory, "")
        _path = os.path.join(_path, outputType, str(Key(key).inAllFlats()))
        if includeFilename:
            _path = os.path.join(
                _path,
                Latex.getTexFilename(change=change, key=key, outputType=outputType),
            )
        return _path

    @classmethod
    def getTexFilename(
        cls,
        change: Change,
        key: Key,
        outputType="GrailOfScale",
    ):
        return outputType + str(change.getChangeNumber()) + ".tex"

    @classmethod
    def makeTextMulticoloured(
        cls,
        text: str,
        colourTags: [str],
        lineWidth=0.2,
        outlineColourTag: str = "black",
        scale=1,
        letterByLetter=False,
        debugFrame=True,
    ):

        # _control = input('holy text {} colourTags {}'.format(text,colourTags))
        # if _control != '': raise TypeError('fuck')
        if len(colourTags) > 1 and type(colourTags) in (list, tuple):
            _str = "\pgfplotsset{colormap={ShadingColor}{"
            _fixedColourTags = []
            colourTags = colourTags[::-1]
            for c, colourTag in enumerate(colourTags):

                assert colourTag.count("#") < 2 and colourTag.count("b") < 2
                if len(colourTag) > 1 and colourTag[1] == "#" or colourTag[1:3] == "bb":
                    # input(colourTag)
                    _fixedColourTags.append(
                        colourTag.replace(
                            colourTag[0:2], Key(colourTag[0:2]).inAllFlats().getASCII()
                        )
                    )
                else:
                    _fixedColourTags.append(colourTag)

                assert _fixedColourTags[c] in Colour.validLatexTags, (
                    _fixedColourTags[c] + " " + colourTags[c]
                )
                # assert _fixedColourTags[c] in Latex.validColourTags
                _str += "color=(" + str(_fixedColourTags[c]) + ")"
                if c != (len(colourTags) - 1):
                    _str += ","
            _str += "}}"
            if outlineColourTag:
                _str += "\\TextShadeContour"
            else:
                _str += "\\TextShade"
            _str += "{" + str(len(colourTags)) + "}"
            if outlineColourTag:
                _str += "{" + outlineColourTag + "}"
            _str += "{" + text + "}"

        elif (type(colourTags) == list and len(colourTags) == 1) or type(
            colourTags
        ) == str:
            if len(colourTags) == 1 and type(colourTags) in (tuple, list):
                colourTag = colourTags[0]
            else:
                colourTag = colourTags
            if len(colourTag) > 1 and colourTag[1] == "#" or colourTag[1:3] == "bb":
                colourTag = colourTag.replace(
                    colourTag[0:2], Key(colourTag[0:2]).inAllFlats().getASCII()
                )
            assert (
                colourTag in Colour.validLatexTags
            ), "the one that does not work:" + str(colourTag) + '\nUse one of the following: ' + str(Colour.validLatexTags)
            _str = Latex.outlineText(
                text=text,
                colourTag=colourTag,
                lineWidth=0.5,#0.5
                strokeColourTag=outlineColourTag,
            )  # why is lineWidth==0.5? because contour draws the lines that phat
        else:
            raise ValueError(
                "colourTags needs two or more. colourTags == "
                + str(colourTags)
                + "text == "
                + text
            )
        return _str

    @classmethod
    def makeTextMulticolouredNEW(
        cls,
        text: str,
        colourTags: [str],
        lineWidth=0.2,
        strokeColourTag: str = False,
        scale=1,
        letterByLetter=False,
        debugFrame=True,
    ):
        """
        _txt = ''
        _txt += "\\providecommand{\\megacolour}{%\n"
        _txt += "\\begin{tikzpicture}[baseline]\n"
        _txt += "\\node["+colourTags[0]+", anchor=base, inner sep=0pt, outer sep=0pt] (n) {" + text + "};\n"

        for c,colourTag in enumerate(colourTags):
            if c == 0: continue
            _txt += "\\clip let \\p1 =(n.north east), in (n.south west) rectangle (\\x1,0.2*\\y1)\n;
            _txt += "\\node[green, anchor=base, inner sep=0pt, outer sep=0pt] {" + text + "};\n"
        """

        _txt += (
            "\\node[orange, anchor=base, inner sep=0pt, outer sep=0pt] (n) {"
            + text
            + "};\n"
        )
        _txt += "\\clip let \\p1 =(n.north east), in (n.south west) rectangle (\\x1,0.5*\\y1)\n;          "
        _txt += (
            "\\node[green, anchor=base, inner sep=0pt, outer sep=0pt] {" + text + "};\n"
        )
        _txt += "\\clip let \\p1 =(n.north east), in (n.south west) rectangle (\\x1,0.2*\\y1)\n;          "
        _txt += (
            "\\node[red, anchor=base, inner sep=0pt, outer sep=0pt] {" + text + "};\n"
        )
        _txt += "\\end{tikzpicture}}\n"
        # _txt += "~\\\\\n"
        _txt += "\\megacolour{} "
        # input('\n' + _txt)

        return _txt

    @classmethod
    def makeTextMulticolouredOLD(
        cls,
        text: str,
        colourTags: [str],
        lineWidth=0.2,
        strokeColourTag: str = False,
        scale=1,
        letterByLetter=False,
        adjustBaseline=True,
        adjustHSpace="-1.6in",
        debugFrame=True,
    ):
        """Needs to have the lengths created in latex (lengthofmulticolourtext, heightofmulticolourtext)
        Like this: \\newlength{\\lengthofmulticolourtext}\ before running this in a file."""
        try:
            Latex.multiColouredTextCounter += 1
        except AttributeError:
            Latex.multiColouredTextCounter = 0
        if letterByLetter:
            return "".join(
                [
                    Latex.makeTextMulticoloured(
                        text=char,
                        colourTags=colourTags,
                        scale=scale,
                        letterByLetter=False,
                        adjustHSpace="-2.4in",
                        debugFrame=debugFrame,
                    )
                    for char in text
                ]
            )
        _innerInkOutlineTag = "gray"
        _baselineAdjust = "-0.41em"

        _names = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
        ]
        _names = [i.capitalize() for i in _names]
        _formattedText = Latex.outlineText(
            text="{\\bfseries " + text + "}",
            colourTag=False,
            strokeColourTag="black",
            lineWidth=2 * lineWidth,
        )
        _txt = ""
        _txt += "\\setlength{{\\lengthofmulticolourtext}}{{\\widthof{{{}}}}}\n".format(
            _formattedText
        )
        _txt += "\\setlength{{\\heightofmulticolourtext}}{{\\heightof{{{}}}}}\n".format(
            _formattedText
        )
        _txt += "\\setlength{{\\depthofmulticolourtext}}{{\\depthof{{{{}}}}\n".format(
            _formattedText
        )
        _txt += "\\setlength{{\\totalheightofmulticolourtext}}{{\\totalheightof{{{{}}}}\n".format(
            _formattedText
        )
        _txt += "\\setlength{{\\bandheightofmulticolourtext}}{{{}\\totalheightof{{{{}}}}\n".format(
            len(colourTags), _formattedText
        )
        _txt += "\\setlength{\\bandtofmulticolourtext}{\\heightofmulticolourtext}\n"
        _txt += "\\setlength{\\bandbofmulticolourtext}{\\bandtofmulticolourtext}\n"
        _txt += (
            "\\addtolength{\\bandbofmulticolourtext}{\\bandheightofmulticolourtext}\n"
        )
        _txt += "\n"
        _X = 0
        _Y = 0
        _L = "-0.5\\lengthofmulticolourtext"
        _L = -0.5
        _R = "0.5\\lengthofmulticolourtext"
        _R = 0.5

        _T = "\\bandtofmulticolourtext"
        _B = "\\bandbofmulticolourtext"
        _height = "\\totalheightofmulticolourtext"

        _txt += "\\noindent "
        _dependancies = [
            "epsf",
            "svg",
            "tcolorbox",
            "makecell",
            "pdfrender",
            "colortbl",
        ]
        for dependancy in _dependancies:
            pass  # _txt += '\\RequirePackage{{{}}}\n'.format(dependancy)

        for cIdx, colourTag in enumerate(colourTags):
            _txt += "\\begin{{tikzfadingfrompicture}}[name={}".format(
                _names[cIdx] + str(Latex.multiColouredTextCounter),
            )

            _txt += "]\n"

            Latex.multiColouredTextCounter += 1
            _txt += "    \\node[scale={}, transparent!0] at ({},0) {{\\bfseries {}}};\n".format(
                scale, _L, text
            )
            # _txt += '\\node[scale={}, transparent!0] at (0,1) {{{}}};\n'.format(scale,
            #    Latex.outlineText(text='\\bfseries '+text,colourTag=False))
            _txt += "\\end{tikzfadingfrompicture}\n"
        _txt += "\\begin{tikzpicture}"
        if adjustBaseline:
            _txt += "[baseline=" + _baselineAdjust + "]"
            # _txt += '[baseline=(current bounding box.south]'
        _txt += "\n"
        # _txt += '\\path[scale={},thick,use as bounding box] at (0,0) {{ {} }}'.format(scale, text)
        # _txt += '\\node[scale={},thick] at ({},{}) {{\\bfseries {}}};\n'.format(scale,_X,_Y,text)
        # This is the "main" black character
        _txt += "\\path[clip] ({},{}) rectangle ({},{});".format(_L, _T, _R, _B)
        _txt += "\\node[scale={},thick,] at (0,0) {{\\bfseries {}}};\n".format(
            scale, _formattedText
        )

        # input(_txt + 'stupid bullshit omg' )

        # _txt += '\\node[scale={},thick] at ({},0) {{\\bfseries {}}};\n'.format(scale, _L,  _formattedText)
        for c, colourTag in enumerate(colourTags[::-1]):

            # _thisT = _T - (_height / len(colourTags)) * c

            # _thisB = _T - (_height / len(colourTags)) * (c + 1)
            _txt += "\path[path fading={},fill={},fit fading=false] ({},{}) rectangle ({},{});\n".format(
                _names[c] + str(Latex.multiColouredTextCounter - len(colourTags) + c),
                colourTag,
                _L,
                "\\bandbofmulticolourtext",
                _R,
                "\\bandtofmulticolourtext",
            )
            _txt += "\\addtolength{\\bandtofmulticolourtext}{\\bandheightofmulticolourtext}\n"
            _txt += "\\addtolength{\\bandbofmulticolourtext}{\\bandheightofmulticolourtext}\n"

        """\path[path fading=A,fill=red,draw=blue,fit fading=false] (-10,-1) rectangle (10,0);
        \path[path fading=B,fill=green,draw=blue,fit fading=false] (-10,0) rectangle (10,1);
        \path[path fading=C,fill=yellow,draw=blue,fit fading=false] (-10,-2) rectangle (10,-1);"""
        _txt += "\\end{tikzpicture}"

        # input('\n{}\nyep that is what happened'.format(_txt))
        if debugFrame:
            _txt = "\\framebox{" + _txt + "}"
        if adjustHSpace:
            # _txt = '\\hspace{\\lengthoftext}{' + _txt + '}'
            pass  # _txt = '{\\setlength{\\lengthofmulticolourtext}{\\widthof{' + text + '}}\\addtolength{\\lengthofmulticolourtext}{' + adjustHSpace + '}' + '\\hspace{0.5\\lengthofmulticolourtext}{' + _txt + '}}'

        # return '\\mbox{' + _txt + '}'
        # input(_txt)
        return _txt + " t"

    r"""
\begin{tikzfadingfrompicture}[name=A]
\node[scale=20, transparent!0] at (0,0) {\bfseries mi7};
\end{tikzfadingfrompicture}

\begin{tikzfadingfrompicture}[name=B]
\node[scale=20,transparent!0] at (0,0) {\bfseries mi7};
\end{tikzfadingfrompicture}
\begin{tikzfadingfrompicture}[name=C]
\node[scale=20,transparent!0] at (0,0) {\bfseries mi7};
\end{tikzfadingfrompicture}

\begin{tikzpicture}
\node[scale=20,thick] at (0,0) {\bfseries mi7};
\path[path fading=A,fill=red,draw=blue,fit fading=false] (-10,-1) rectangle (10,0);
\path[path fading=B,fill=green,draw=blue,fit fading=false] (-10,0) rectangle (10,1);
\path[path fading=C,fill=yellow,draw=blue,fit fading=false] (-10,-2) rectangle (10,-1);
%\path[draw=blue] (-10,-1) rectangle (10,0);
%\path[draw=red] (-10,0) rectangle (10,1);
\end{tikzpicture}"""

    @classmethod
    def makeTextMulticolouredWORKINGISH(
        cls,
        text: str,
        colourTags: [str],
        lineWidth=0.2,
        strokeColourTag: str = False,
        scale=1,
        letterByLetter=False,
        adjustBaseline=True,
        adjustHSpace="-1.6in",
        debugFrame=True,
    ):

        try:
            Latex.multiColouredTextCounter += 1
        except AttributeError:
            Latex.multiColouredTextCounter = 0
        if letterByLetter:
            return "".join(
                [
                    Latex.makeTextMulticoloured(
                        text=char,
                        colourTags=colourTags,
                        scale=scale,
                        letterByLetter=False,
                        adjustHSpace="-2.4in",
                        debugFrame=debugFrame,
                    )
                    for char in text
                ]
            )
        _innerInkOutlineTag = "gray"
        _baselineAdjust = "-0.41em"
        _X = 0
        _Y = 0
        _L = -1
        _R = 1
        _T = 0.25
        _B = -0.25
        _height = _T - _B

        _names = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
        ]
        _names = [i.capitalize() for i in _names]
        _formattedText = Latex.outlineText(
            text="{\\bfseries " + text + "}",
            colourTag=False,
            strokeColourTag="black",
            lineWidth=2 * lineWidth,
        )
        _txt = ""
        _txt += "\\noindent "
        _dependancies = [
            "epsf",
            "svg",
            "tcolorbox",
            "makecell",
            "pdfrender",
            "colortbl",
        ]
        for dependancy in _dependancies:
            pass  # _txt += '\\RequirePackage{{{}}}\n'.format(dependancy)

        for cIdx, colourTag in enumerate(colourTags):
            _txt += "\\begin{{tikzfadingfrompicture}}[name={}".format(
                _names[cIdx] + str(Latex.multiColouredTextCounter),
            )

            _txt += "]\n"

            Latex.multiColouredTextCounter += 1
            _txt += (
                "\\node[scale={}, transparent!0] at (0,0) {{\\bfseries {}}};\n".format(
                    scale, text
                )
            )
            # _txt += '\\node[scale={}, transparent!0] at (0,1) {{{}}};\n'.format(scale,
            #    Latex.outlineText(text='\\bfseries '+text,colourTag=False))
            _txt += "\\end{tikzfadingfrompicture}\n"
        _txt += "\\begin{tikzpicture}"
        if adjustBaseline:

            _txt += "[baseline=" + _baselineAdjust + "]"
            # _txt += '[baseline=(current bounding box.south]'
        _txt += "\n"
        # _txt += '\\path[scale={},thick,use as bounding box] at (0,0) {{ {} }}'.format(scale, text)
        # _txt += '\\node[scale={},thick] at ({},{}) {{\\bfseries {}}};\n'.format(scale,_X,_Y,text)
        # This is the "main" black character
        _txt += "\\node[scale={},thick] at (0,0) {{\\bfseries {}}};\n".format(
            scale, _formattedText
        )
        for c, colourTag in enumerate(colourTags[::-1]):
            _thisT = _T - (_height / len(colourTags)) * c
            _thisB = _T - (_height / len(colourTags)) * (c + 1)
            _txt += "\path[path fading={},fill={},fit fading=false] ({},{}) rectangle ({},{});".format(
                _names[c] + str(Latex.multiColouredTextCounter - len(colourTags) + c),
                colourTag,
                _L,
                _thisB,
                _R,
                _thisT,
            )

        """\path[path fading=A,fill=red,draw=blue,fit fading=false] (-10,-1) rectangle (10,0);
        \path[path fading=B,fill=green,draw=blue,fit fading=false] (-10,0) rectangle (10,1);
        \path[path fading=C,fill=yellow,draw=blue,fit fading=false] (-10,-2) rectangle (10,-1);"""
        _txt += "\\end{tikzpicture}"

        # input('\n{}\nyep that is what happened'.format(_txt))
        if debugFrame:
            _txt = "\\framebox{" + _txt + "}"
        if adjustHSpace:

            # _txt = '\\hspace{\\lengthoftext}{' + _txt + '}'
            _txt = (
                "{\\setlength{\\lengthofmulticolourtext}{\\widthof{"
                + text
                + "}}\\addtolength{\\lengthofmulticolourtext}{"
                + adjustHSpace
                + "}"
                + "\\hspace{0.5\\lengthofmulticolourtext}{"
                + _txt
                + "}}"
            )

        # return '\\mbox{' + _txt + '}'
        return _txt + " t"

    r"""
\begin{tikzfadingfrompicture}[name=A]
\node[scale=20, transparent!0] at (0,0) {\bfseries mi7};
\end{tikzfadingfrompicture}

\begin{tikzfadingfrompicture}[name=B]
\node[scale=20,transparent!0] at (0,0) {\bfseries mi7};
\end{tikzfadingfrompicture}
\begin{tikzfadingfrompicture}[name=C]
\node[scale=20,transparent!0] at (0,0) {\bfseries mi7};
\end{tikzfadingfrompicture}

\begin{tikzpicture}
\node[scale=20,thick] at (0,0) {\bfseries mi7};
\path[path fading=A,fill=red,draw=blue,fit fading=false] (-10,-1) rectangle (10,0);
\path[path fading=B,fill=green,draw=blue,fit fading=false] (-10,0) rectangle (10,1);
\path[path fading=C,fill=yellow,draw=blue,fit fading=false] (-10,-2) rectangle (10,-1);
%\path[draw=blue] (-10,-1) rectangle (10,0);
%\path[draw=red] (-10,0) rectangle (10,1);
\end{tikzpicture}"""

    @classmethod
    def outlineText(
        cls, text: str, colourTag: str, lineWidth=0.2, strokeColourTag=False
    ):

        """if outlineColourTag == False, outlines will be in the default colour"""
        # https://ctan.math.washington.edu/tex-archive/macros/latex/contrib/oberdiek/pdfrender.pdf
        # Go to -> 1.1 Usage for options
        """if not all([isinstance(i, (str, JazzNote)) for i in (text,)]):
            raise TypeError('{} {} {} {}'.format(text, colourTag, type(text), type(colourTag)))"""
        _txt = (
            r"""\textpdfrender{
    TextRenderingMode=FillStroke,
    LineWidth="""
            + str(lineWidth)
            + r"""pt,
    LineJoinStyle=1, 
    """
        )

        if strokeColourTag:
            _txt += "StrokeColor=" + strokeColourTag + ",\n"
        if colourTag:
            if len(colourTag) > 1 and colourTag[1] == "#" or colourTag[1:3] == "bb":
                colourTag = colourTag.replace(
                    colourTag[0:2], Key(colourTag[0:2]).inAllFlats().getASCII()
                )
            _txt += "    FillColor=" + colourTag + ",\n"
        _txt += "  }{" + str(text) + "}"

        return _txt

    @classmethod
    def textGraphic(
        cls,
        text: str,
        graphPath: str,
        diagramType=None,
        endStr="\\hspace{1ex}",
        beginningStr=None,
        textBoundingBox=True,
        imgBoundingBox=False,
        outlineText=False,
        colourTag="C-Dk",
        lineColourTag=False,
        sizeMultiplier=1.0,
        trimLeft=3.5,
        trimRight=0,
        moveUp=0,
        imgTransparency=1,
        lineWidth=0.2,
    ):
        if imgTransparency < 1:
            _transparencyOpenTag = (
                "{\\transparent{" + str(round(imgTransparency, 1)) + "}"
            )
            _transparencyCloseTag = "}"
        elif imgTransparency in (1, 0):
            _transparencyOpenTag = ""
            _transparencyCloseTag = ""
        elif imgTransparency > 1 or imgTransparency < 0:
            raise ValueError("imgTransparency out of bounds between 0 and 1.")
        if beginningStr == None:
            beginningStr = endStr
        if diagramType == None:
            diagramType = "PCircle"
        if diagramType == "FCircle":
            _graphicWidth = str(round(1.8 * sizeMultiplier, 2)) + "em"
            # _graphicYShift = '-0.50em'
            _graphicYShift = (
                str(round(-0.5 + 2 * (1 - sizeMultiplier) + moveUp, 2)) + "em"
            )
        elif diagramType == "PCircle":
            _graphicWidth = str(round(1.38 * sizeMultiplier, 2)) + "em"
            # _graphicYShift = '-0.6ex'
            _graphicYShift = _graphicYShift = (
                str(round(-0.258 + 0.61 * (1 - sizeMultiplier) + moveUp, 2)) + "em"
            )
        _textBoundingBox = "use as bounding box" if textBoundingBox else ""
        _imgBoundingBox = ",use as bounding box" if imgBoundingBox else ""
        if outlineText:
            text = Latex.outlineText(
                text, colourTag, lineWidth=lineWidth, strokeColourTag=lineColourTag
            )
        return (
            beginningStr
            + r"""\begin{tikzpicture}[anchor=base,baseline,trim left="""
            + str(trimLeft)
            + r""",trim right=-"""
            + str(trimRight)
            + r"""]
        \node[inner sep=1"""
            + _imgBoundingBox
            + """] (img) at ("""
            + str(0)
            + ","
            + _graphicYShift
            + ") {"
            + _transparencyOpenTag
            + "\includegraphics[width="
            + _graphicWidth
            + "]{"
            + str(graphPath)
            + "}"
            + _transparencyCloseTag
            + r"""};
        \node["""
            + _textBoundingBox
            + """] at (0,0) {"""
            + str(text)
            + r"""};
        \end{tikzpicture}"""
            + endStr
        )

    @classmethod
    def insertKeysDiagram(
        cls,
        change: Change,
        diagramTypes: list,
        greyScale=None,
        invertColour=None,
    ):
        if not all([i in Graphics.validDiagrams for i in diagramTypes]):
            raise ValueError(
                "instrumentTypes[i]: {} not in Graphics.validDiagrams:\n{}".format(
                    i, Graphics.validDiagrams
                )
            )
        if greyScale == None:
            greyScale = not Colour.makeGraphicsColoured
        if invertColour == None:
            invertColour = Colour.useBlackBackground
        _str = ""
        # _str += '\\clearpage '
        # _str += '\\begin{figure}[h!] '
        _str += "\\centering "
        _str += "\\begin{adjustbox}{max width=1\\textwidth,keepaspectratio}"
        _str += "\\includegraphics[width=\\textwidth]{"
        _str += (
            Graphics.getKeyDiagramPath(
                change=change,
                diagramTypes=diagramTypes,
                includeGraphicsPath=not Latex.useRelativeGraphicsPath,
            )
            + "}\n"
        )
        # _str += '\\caption{}'
        # _str += '\\label{fig:}'
        _str += "\\end{adjustbox}"
        # _str += '\\end{figure}'

        return _str

    @classmethod
    def writeIncludedChangeInfoToTex(cls, changeRange) -> str:
        _changesName = ""
        if Utility.listIsSequential(changeRange):
            _changesName += "Including Changes {} through {}".format(
                changeRange[0], changeRange[-1]
            )
        elif Book.makePrimes and changeRange == Book.sequencePrimes:
            _changesName += "Including the {} Prime Changes".format(
                len(Book.sequencePrimes)
            )
        elif changeRange == Raga.makeFestivalSounds():
            _changesName += "Including the 72 Melakarta Ragas and {} component chords"
        elif len(changeRange) <= 50:
            _changesName += "Including Changes: {}".format(",".join(changeRange))
        else:
            _changesNames += "Including Various Changes."
        return _changesName

    @classmethod
    def makeTexASubfile(cls, tex: str) -> str:
        _str = "\documentclass[../document.tex]{subfiles}\n"
        _str += "\\begin{document}\n"
        _str += tex
        _str += "\end{document}"
        return _str

    @classmethod
    def makeTabular(
        self,
        rows: [list],
        surroundByTable=False,
        tableCaption="A table of stuff",
        flipAxes=False,
        useHorizontalLines=False,
        useVerticalLines=False,
        enclosingHorizontalLines=True,
        enclosingVerticalLines=True,
        fillHorSpaceWithTabularX=False,
        centreResults=False,
    ):
        _skipMakingColumnTypes = False
        # rows should be a list of lists. list of rows which contain lists of values

        if not type(rows) == list or len(rows) == 0 or not type(rows[0]) == list:
            raise TypeError(
                "makeTabular accepts a list of lists. rows = {}".format(rows)
            )

        if flipAxes:
            rows = Utility.flipAxesOfList(rows)
        _str = ""
        if surroundByTable:
            _str += "\\begin{table}[!ht] "
            if len(tableCaption) > 0:
                _str += "\\caption{{}} ".format(tableCaption)
        if fillHorSpaceWithTabularX:
            # How it should look from https://tex.stackexchange.com/questions/89166/centering-in-tabularx-and-x-columns

            # input(_str)
            if centreResults:
                _colType = "@{}l"
                if useVerticalLines:
                    if enclosingVerticalLines:
                        _colType = "| " + _colType
                    else:
                        if useVerticalLines:
                            _colType = _colType + " |"
                        else:
                            pass
                _str = (
                    "\\begin{tabularx}{\\textwidth}{"
                    + _colType
                    + " *"
                    + str(len(rows[0]) - 1)
                    + "{>{\centering\\arraybackslash}X}@{}}"
                )  #
                _skipMakingColumnTypes = True
            else:
                _str += "\\begin{tabularx}{\\textwidth}{"
                _colType = "X"
        else:
            _str += "\\begin{tabular}{"
            if centreResults:
                _colType = "c"
            else:
                _colType = "l"

        if not _skipMakingColumnTypes:
            if enclosingVerticalLines:
                _str += "|"
            for col in range(len(rows[0])):
                _str += _colType
                if (len(rows[0]) - 1) != col:
                    _str += " "
                    if useVerticalLines:
                        _str += "| "
            if enclosingVerticalLines:
                _str += "|"
            _str += "}\n"
        if enclosingHorizontalLines:
            _str += "\\hline "
        for r, row in enumerate(rows):
            for d, data in enumerate(row):
                if data == None:
                    data = ""
                _str += data
                if d != (len(row) - 1):
                    _str += " & "
            if True or r != (len(rows) - 1):
                _str += "\\\\"
            if useHorizontalLines:
                if r != (len(rows) - 1):
                    _str += "\\hline"
            _str += "\n"
        if enclosingHorizontalLines:
            _str += "\\hline"
        if fillHorSpaceWithTabularX:
            _str += "\\end{tabularx}"
        else:
            _str += "\\end{tabular}"
        if surroundByTable:
            _str += "\\end{table}"
        # input(_str)
        return _str

    @classmethod
    def buildFile(
        self,
        filepath: str,
        clearAuxFiles=True,
        openFileWhenDone=True,
        args=[str],
        options: [str] = [],
        iterations=1,
        convertToRaster=False,
    ):
        if filepath[-4:] != ".tex":
            raise ValueError(
                "this expects a path to a .tex file filepath = " + filepath
            )
        _thisDoc = os.path.basename(os.path.normpath(filepath))
        _newPath = filepath.replace(".tex", ".pdf")
        if clearAuxFiles is None:
            if Project.removeAuxFiles:
                clearAuxFiles = True
            elif makePDFTimes > 1:
                clearAuxFiles = True
            else:
                clearAuxFiles = False
        _interpreter = Latex.lualatexInterpreter
        _args = []
        # _args = ['--max_strings=8000000', '--hash_extra=1000000''']
        _auxFiles = [
            _thisDoc + ".aux",
            _thisDoc + ".lof",
            _thisDoc + ".log",
            _thisDoc + ".out",
            _thisDoc + ".toc",
            _thisDoc + ".auxlock",
        ]
        _auxFiles = [a.replace(".tex", "") for a in _auxFiles]
        if clearAuxFiles:
            for auxFile in _auxFiles:
                if os.path.isfile(auxFile):
                    print("removing aux files: ", end="")
                    print(auxFile)
                    f = open(auxFile)
                    f.close()
                    fileNotFound = 1
                    while fileNotFound:
                        try:
                            os.remove("./" + auxFile)
                            fileNotFound = False
                        except:
                            input("probably could not remove file {}, try again?".format(auxFile))
                else:
                    print("skipped removing", auxFile, "as it is not a file")

        else:
            print("did not clear aux files for " + filepath)

        for i in range(iterations):
            print(
                "Making file time {}/{}. Ran this on command line: ".format(
                    1+i, iterations
                )
                + _interpreter
                + " "
                + " ".join(options)
                + " "
                + filepath
                + " "
                + " ".join(_args)
                + " "
            )
            os.system(
                _interpreter
                + " "
                + " ".join(options)
                + " "
                + filepath
                + " "
                + " ".join(_args)
                + " "
            )

        print("done turning {} into {}".format(_thisDoc, _newPath))
        if openFileWhenDone:
            try:

                Utility.openFile(_newPath)
                return _newPath
            except OSError:
                raise OSError(
                    "Check that Project.makePdfTimes > 0. Probably the pdf was never made. It is highly probable that the TeX engine crashed. (failed to complete)"
                )
        if convertToRaster:
            Utility.rasterisePDF(_newPath)


    @classmethod
    def buildProject(
        cls,
        includedChangesFilename: str,
        rootDoc: str = None,
        clearAuxFiles=None,
        volumeNumber=None,
        writeVolumeSelector=True,
        openFileWhenDone=True,
        makePDFTimes=None,
    ):
        if makePDFTimes == None:
            makePDFTimes = Project.makePDFTimes
        if clearAuxFiles is None:
            if Project.removeAuxFiles:
                clearAuxFiles = True
            elif makePDFTimes > 1:
                clearAuxFiles = True
            else:
                clearAuxFiles = False
        if volumeNumber == None:
            volumeNumber = "clone"

        if rootDoc == None:
            _rootDoc = Project.rootGrailOfScaleTexFilename
        else:
            _rootDoc = rootDoc
        _rootFilename = _rootDoc
        _thisDoc = _rootDoc + str(volumeNumber)
        _filename = _thisDoc + ".tex"
        now = str(datetime.datetime.now())[:19]
        now = now.replace(":", "_")
        # make copy of root doc
        src_dir = os.path.join(Project.directory, _rootFilename + ".tex")
        dst_dir = os.path.join(Project.directory, "{}{}.tex".format(_rootFilename, volumeNumber))
        backup_dir = os.path.join(Project.directoryTex, "backup\\")
        backup_filename = "{}{}_{}.tex".format(
            _rootFilename, volumeNumber, now.replace(" ", "_")
        )
        # Utility.printPrettyVars(src_dir,backup_dir,dst_dir,_filename,_rootFilename,_thisDoc)

        if src_dir != dst_dir:
            Utility.makeDirectory(backup_dir)
            shutil.copy(src_dir, backup_dir + backup_filename)
            print("copying backup to {}{}".format(backup_dir, backup_filename))

        shutil.copy(src_dir, dst_dir)
        print('and shutil.copy("{}", "{}")'.format(src_dir, dst_dir))
        _interpreter = Latex.lualatexInterpreter
        _args = ["--max_strings=8000000", "--hash_extra=1000000" ""]
        _auxFiles = [
            _thisDoc + ".aux",
            _thisDoc + ".lof",
            _thisDoc + ".log",
            _thisDoc + ".out",
            _thisDoc + ".toc",
        ]
        if clearAuxFiles:
            for auxFile in _auxFiles:
                if os.path.isfile(auxFile):
                    print("removing aux files: ", end="")
                    print(auxFile)
                    f = open(auxFile)
                    f.close()
                    fileNotFound = 1
                    while fileNotFound:
                        try:
                            os.remove("./" + auxFile)
                            fileNotFound = False
                        except:
                            input("probably could not remove file, try again?")

        if writeVolumeSelector and volumeNumber != "clone":
            print("")
            path = os.path.join(Project.directoryTex, includedChangesFilename.replace(".tex", ""))
            path = path.replace(Project.directory, "")
            path = path.replace("\\", "/")
            replacement = "\\subfile{" + path + "}"

            Utility.replaceStrInFile(_filename, "%%%changesVolume%%%", replacement)

        _thisDoc += ".pdf"
        if makePDFTimes == 0:
            print("BTW, makePDFTimes == 0 so LaTex will not render a new file.")
        for i in range(makePDFTimes):
            print(
                "\n\n\nBeginning pass " + str(i + 1),
                "of",
                makePDFTimes,
                end="!!!\n\n\n",
            )

            # https://stackoverflow.com/questions/33207950/compile-latex-file-using-a-python-script
            # subprocess.check_call([_interpreter, _filename],shell=True)
            # subprocess.call(shlex.split(_interpreter +' '.join(_args)))
            commandStr = "building " + _thisDoc + " in " + _interpreter
            print(commandStr)
            os.system(_interpreter + " " + _filename + " " + " ".join(_args) + " ")
            print(
                ".\n\n\nThis concludes pass "
                + str(i + 1)
                + " of "
                + str(makePDFTimes)
                + "\nFile at "
                + _thisDoc
                + "!!!\n"
            )

        if openFileWhenDone:
            try:
                Utility.openFile(_thisDoc)
                return _thisDoc
            except OSError:
                raise OSError(
                    "Check that Project.makePdfTimes > 0. Probably the pdf was never made. It is highly probable that the TeX engine crashed. (failed to complete)"
                )

    @classmethod
    def getTransposedColourKey(cls, semitonesTransposed: int, colourKey=None):
        from JazzNote import JazzNote
        if colourKey is None:
            from Book import Book
            colourKey = Book.rootColourKey
        elif "#" in colourKey:
            raise ValueError("colourKey should be expressed in all flats. " + colourKey)
        elif not JazzNote.isAlphabetNoteStr(colourKey):
            raise TypeError("colourKey should be an alphabet note")

        if colourKey is None:
            colourKey = Book.rootColourKey
        _noteNames = JazzNote.noteNameFlats
        _keyIndex = _noteNames.index(colourKey)
        return _noteNames[(_keyIndex + semitonesTransposed) % len(_noteNames)]

    @classmethod
    def insertSmallDiagram(
        cls,
        change: Change,
        key: Key,
        diagramType: str = "FCircle",
        resolution=None,
        imgtag="tabbingimg",
        includeGraphicsPath=False,
        invertColour=False,
        greyScale=False,
        externalGraphicsPath=False,
        filetype="png",
        renderIfNotFound=True,
    ):
        """externalGraphicsPath == True overrides includeGraphicsPath == True,
        If you want to change the settings for different imgtag values,
        you will find them in tex/preamble.tex"""
        try: Change
        except NameError: from Change import Change

        assert type(change) is Change
        # Replace this with requirement for Key type on key
        try: Key
        except NameError:
            from Key import Key

        if isinstance(key, Key):
            key = key.note
        from JazzNote import JazzNote
        if "#" in key:
            raise ValueError("key should be expressed in all flats. " + key)
        elif not (JazzNote.isAlphabetNoteStr(key)):
            raise TypeError(
                "key should be an alphabet note. No long accepting BW for black and white, not "
                + key
            )
        elif key is None:
            key = Book.rootColourKey
        if imgtag not in Latex.imageTags:
            raise ValueError(
                "imgtag {} must be in Latex.imageTags {}".format(
                    imgtag, Latex.imageTags
                )
            )
        # if not Colour.makeGraphicsColoured:
        #    key = 'BW'

        if resolution is None:
            if imgtag == "tabbingimg":
                resolution = Latex.SmallCircleTabbingResolution
            else:
                resolution = Latex.SmallCircleResolution


        try: Graphics
        except NameError: from Graphics import Graphics
        _path = Graphics.getDiagramPath(
            change=change,
            key=key,
            resolution=resolution,
            filetype=filetype,
            diagramType=diagramType,
            includeFilename=True,
            includeGraphicsPath=includeGraphicsPath,
            externalGraphicsPath=externalGraphicsPath,
            invertColour=invertColour,
            greyScale=greyScale,
        )
        _fullpath = Graphics.getDiagramPath(
            change=change,
            key=key,
            resolution=resolution,
            greyScale=greyScale,
            filetype=filetype,
            diagramType=diagramType,
            includeFilename=True,
            includeGraphicsPath=True,
            externalGraphicsPath=externalGraphicsPath,
            invertColour=invertColour,
        )
        #input('{} {}'.format(_path,_fullpath))

        try:
            Colour
        except NameError:
            from Colour import Colour


        if Graphics.seeIfDiagramExists(
            change,
            key,
            resolution,
            greyScale=greyScale,
            invertColour=Colour.useBlackBackground,
            diagramType=diagramType,
            filetype=filetype,
            externalGraphicsPath=externalGraphicsPath,
            renderIfNotFound=renderIfNotFound,
        ):

            _str = (
                Latex.commandStrings["Small Circle Command Start"]
                + _path
                + Latex.commandStrings["Small Circle Command End"]
            )
            # print('inside insertSmallDiagram, change = {} _str = {}'.format(change,_str))

            for tag in Latex.imageTags:
                if tag in (_str):
                    _str = _str.replace(tag, imgtag)
                    break
            # input(_str)
            return _str
        else:

            raise ValueError(
                "Apparently that one does not exist at {}.\nexternalGraphicsPath is {}".format(
                    _fullpath, externalGraphicsPath
                )
            )

    @classmethod
    def insertSmallCircleFromPageNumber(
        cls,
        pageNumber: int,
        colourKey=None,
        resolution=None,
        removePageNumber=False,
        tabbingimg=False,
        renderIfNotFound=True,
    ):
        """Change the height default in insertSmallDiagram."""
        pageNumber = int(pageNumber)
        if not -2049 < pageNumber < 2049:
            raise ValueError(
                "changeNumber {} should be between the range".format(pageNumber)
            )
        if colourKey is None:
            colourKey = Book.rootColourKey
        elif "#" in colourKey:
            raise ValueError("colourKey should be expressed in all flats. " + colourKey)
        elif not (JazzNote.isAlphabetNoteStr(colourKey) or colourKey == "BW"):
            raise TypeError(
                "colourKey should be an alphabet note or BW for black and white, not "
                + colourKey
            )

        if resolution is None:
            resolution = Latex.SmallCircleResolution
        if removePageNumber == True:
            _pageNumberStr = ""
        else:
            _pageNumberStr = str(pageNumber)

        return (
            Latex.insertSmallDiagram(
                change=Change.makeFromChangeNumber(pageNumber, rootIsChangeOne=True),
                colourKey=colourKey,
                tabbingimg=tabbingimg,
                includeGraphicsPath=includeGraphicsPath,
                renderIfNotFound=True,
            )
            + _pageNumberStr
        )

    @classmethod
    def replacePageStrsBySmallCircles(
        cls,
        pageStr: str,
        colourKey=None,
        removePageNumber=False,
        showDebug=False,
    ):
        if colourKey is None:
            colourKey = Book.rootColourKey
        elif "#" in colourKey:
            raise ValueError("colourKey should be expressed in all flats. " + colourKey)
        elif not JazzNote.isAlphabetNoteStr(colourKey):
            raise TypeError("colourKey should be an alphabet note")

        _pageChars = []
        _pageNumbers = []
        for c, char in enumerate(pageStr):
            if char == Book.unicodeChars["Change Number"]:
                _pageChars.append(c)
                _pageNumbers.append("")
                _charsAhead = 1
                # print('asdf',pageStr)
                while c + _charsAhead < len(pageStr) and pageStr[c + _charsAhead] in (
                    "-",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "0",
                ):
                    # while(pageStr[c+_charsAhead] in ('-','1','2','3','4','5','6','7','8','9','0',' ')):
                    _pageNumbers[-1] += pageStr[c + _charsAhead]
                    _charsAhead += 1
                if _pageNumbers[-1] == "":
                    # This is when a subChange was not found after symboll
                    del _pageNumbers[-1]
                    del _pageChars[-1]

        if len(_pageNumbers) > 1:
            if showDebug:
                input("The Text: {}\nThe Pages: {}".format(pageStr, _pageNumbers))
        _pageNumbers = [int(i) for i in _pageNumbers]
        for i in range(len(_pageNumbers)):
            if _pageNumbers[i] < 0:
                _pageNumbers[i] += 1
            elif _pageNumbers[i] > 0:
                _pageNumbers[i] -= 1
            else:
                raise ValueError(
                    "Page number should have been human format. That means it would not be 0."
                )
        _pageNumbers = [str(i) for i in _pageNumbers]
        for pageNumber in _pageNumbers:
            pageStr = pageStr.replace(
                Book.unicodeChars["Change Number"] + pageNumber,
                Latex.insertSmallCircleFromPageNumber(
                    pageNumber=pageNumber,
                    colourKey=colourKey,
                    removePageNumber=removePageNumber,
                ),
            )

        return pageStr

    @classmethod
    def replacePianoBySymbol(cls, cellData: str, symbol: str = None) -> str:

        if Latex.commandStrings["Small Piano Command Start"] in cellData:
            if symbol is None:
                symbol = Book.unicodeChars["Piano"]
            _SPianoPart = cellData[
                cellData.index(
                    Latex.commandStrings["Small Piano Command Start"]
                ) : cellData.index(Latex.commandStrings["Small Piano Command End"])
                + len(Latex.commandStrings["Small Piano Command End"])
                - 1
            ]
            return cellData.replace(_SPianoPart, symbol)
        else:
            return cellData

    @classmethod
    def replaceSmallCircleBySymbol(cls, cellData: str, symbol: str = None) -> str:
        if any(
            [
                command in cellData
                for command in (
                    Latex.commandStrings["Small Circle Command Start"],
                    Latex.commandStrings["Small Circle Small Command Start"],
                )
            ]
        ):
            # switches between graphic tags
            start = (
                Latex.commandStrings["Small Circle Command Start"]
                if Latex.commandStrings["Small Circle Command Start"] in cellData
                else Latex.commandStrings["Small Circle Small Command Start"]
            )
            if Latex.commandStrings["Small Circle Command End"] in cellData:
                if symbol is None:
                    symbol = Book.unicodeChars["Change Number"]
                # end dont matter cause its same either way
                _smallCirclePart = cellData[
                    cellData.index(start) : cellData.index(
                        Latex.commandStrings["Small Circle Command End"]
                    )
                    + len(Latex.commandStrings["Small Circle Command End"])
                    - 1
                ]
                return cellData.replace(_smallCirclePart, symbol)
            else:
                raise ValueError("wtf cellData " + cellData)
        else:
            return cellData

    @classmethod
    def changeHStretch(
        cls, pageStr: str, lines: int, showDebug=True, showDebugInOutput=True
    ) -> float:
        hStretch = Latex.linesPerPage / lines
        if lines < 40:
            hStretch = 1
        elif lines < 50:
            hStretch *= 0.85
        elif lines < 55:
            hStretch *= 0.8
        elif lines < 59:
            hStretch *= 0.68  # .92
        elif lines == 59:
            hStretch *= 0.60
        elif lines == 60:
            hStretch = 0.42
        elif lines < 64:
            hStretch *= 0.39
        elif lines == 64:
            hStretch *= 0.31
        elif lines == 65:
            hStretch *= 0.26
        elif lines == 66:
            hStretch *= 0.20
        elif lines == 67:
            hStretch *= 0.18
        elif lines < 68:
            hStretch *= 0.17
        elif lines < 70:
            hStretch *= 0.16
        elif lines < 75:
            hStretch *= 0.03  # 0.078
        elif lines < 80:
            hStretch *= 0.025
            hStretch -= 0.7
        elif lines >= 80:
            hStretch *= 0.02
            hStretch -= 0.1
        if showDebug == True:
            # pageStr += 'ln'+str(lines)
            print("lines = ", lines, "hStretch=", hStretch, end="")
        # print(pageStr,)
        # input()
        _searchStr = "\\renewcommand{\\arraystretch}{"
        _numPartToReplace = pageStr[
            pageStr.index(_searchStr) + len(_searchStr) : pageStr.index("}\\noindent")
        ]
        _partToReplace = _searchStr + _numPartToReplace + "}"
        _replacement = _searchStr + str(hStretch) + "}"
        # input('the partToReplace == {}'.format(_partToReplace))
        # print('were doing it',_partToReplace,'pageStr',pageStr,)
        # input('partToReplace\n{}\nhStretch\n{}'.format(_partToReplace,hStretch))
        pageStr = pageStr.replace(_partToReplace, _replacement)
        # print('pageStr after',pageStr)
        if showDebugInOutput:
            if Book.unicodeChars["Binary True"] in pageStr:
                if Book.unicodeChars["Binary False"] in pageStr:
                    _insertionIndex = min(
                        pageStr.index(Book.unicodeChars["Binary True"]),
                        pageStr.index(Book.unicodeChars["Binary False"]),
                    )
                else:
                    _insertionIndex = pageStr.index(Book.unicodeChars["Binary True"])
            else:
                _insertionIndex = pageStr.index(Book.unicodeChars["Binary False"])
            pageStr = Utility.insertSubstringInStr(
                _insertionIndex,
                pageStr,
                "st" + str(round(hStretch, 2)) + "ln" + str(int(lines)),
            )
            return pageStr
        else:
            return pageStr

    @classmethod
    def setHStretch(cls, changeLength: int, squishItMore=True) -> float:
        _str = "\\renewcommand{\\arraystretch}{"
        if squishItMore == True:
            _adjustment = -0.2
        else:
            _adjustment = 0
        if changeLength in (0, 1, 2):
            _str += str(1.0 + _adjustment)
        elif changeLength in (
            3,
            4,
        ):
            _str += str(0.5 + _adjustment)
        elif changeLength in (5, 6):
            _str += str(0.5 + _adjustment)
        elif changeLength == 7:
            _str += str(0.5 + _adjustment)
        elif changeLength == 8:
            _str += str(0.45 + _adjustment)
        elif changeLength == 9:
            _str += str(0.4 + _adjustment)
        elif changeLength in (10, 11):
            _str += str(0.35 + _adjustment)
        elif changeLength == 12:
            _str += str(0.2 + _adjustment)
        else:
            raise ValueError("wtf m8", changeLength)
        _str += "}"
        return _str

    @classmethod
    def getLineBreaks(cls, pageStr: str, showDebug=False):
        # First the half-linebreaks
        _partialLineBreaks = pageStr.count(
            Latex.commandStrings["Line Break With Space"]
        )
        _partialLineBreaks += pageStr.count(Latex.commandStrings["Line Break Small"])
        _partialLineBreaks += pageStr.count(
            Latex.commandStrings["Line Break Scale Names"]
        )
        # print(Utility.numPartOfStr(Latex.commandStrings['Line Break With Space']),Latex.commandStrings['Line Break With Space'],'gnugnugnu',sep='\n')
        # _partialLineBreaks *= Utility.numPartOfStr(Latex.commandStrings['Line Break With Space'])
        # Then the full ones
        _fullLineBreaks = pageStr.count("\\\\\n")
        _lineBreaks = _partialLineBreaks * 0.5 + _fullLineBreaks
        if showDebug == True:
            input("lineBreaks " + str(_lineBreaks) + " pageStr" + pageStr)
        return _lineBreaks

    @classmethod
    def makeDataSmaller(
        cls,
        results,
        fontSize: str,
    ):
        # returnAsList should be called makeNotAList
        if not Latex.on:
            return results
        _returnAsList = False
        if not type(results) == list:
            results = [results]
            _returnAsList = True
        if fontSize in ("small", "scriptsize", "footnotesize"):
            pass
        else:
            raise TypeError("thats not a good font size yet")
        for i, result in enumerate(results):
            results[i] = "{\\" + fontSize + " " + result + "}"
            # {\HUGE A huge text}
        # input('in makeDataSmaller: results: {}'.format(results))
        if _returnAsList:
            return results[0]
        else:
            return results

    @classmethod
    def makeDataColoured(cls, results, colours, colourType=None, adjustBySemitones=0):
        from Colour import Colour
        if not Latex.on or not Latex.makeTextColoured:
            # print('makedata coloured does not want to make it coloured',results)

            return results

        # make vars lists which can turn into single values at the end
        if not type(results) == list:
            results = [results]
            _returnAsList = False
        if not type(colours) == list:
            colours = [colours]
            _returnAsList = False
        else:
            _returnAsList = True
        if not len(colours) == len(results):
            raise ValueError(
                "You provided a number of results different from the number of makeTextColoured.\n"
                + str(results)
                + str(colours)
            )

        if len(colours) > 0 and (not type(colours[0]) == int) and (colours[0] != False):
            raise TypeError(
                "Colour codes are to be specified in an int between 0-11, not"
                + str(colours[0])
                + str(type(colours[0]))
                + "\n"
                + str(colours)
            )

        # Set the colour type (box or text) and the shade of colour (light or dark)
        if colourType in Latex.colourTypes or colourType is None:
            pass
        else:
            raise ValueError("invalid colourType", Latex.colourTypes, colourType)

        if colourType is None:
            if Latex.inkSaver:
                colourType = "Colour Text"
                if Latex.blackPaper:
                    darkColours = False
                elif not Latex.blackPaper:
                    darkColours = True
            else:
                colourType = "Highlight Start"
                if Latex.blackPaper:
                    darkColours = True
                elif not Latex.blackPaper:
                    darkColours = False
        elif colourType == "Colour Cell":
            if Latex.blackPaper:
                darkColours = True
            else:
                darkColours = False

        if darkColours == True:
            _nameByDistanceLightness = Colour.nameByDistanceDk
        elif darkColours == False:
            _nameByDistanceLightness = Colour.nameByDistanceLt
        # print('results are ',results,results[0],type(results[0]))
        # print('longname',_nameByDistanceLightness)
        # print('makeTextColoured',makeTextColoured)
        _colouredResults = []
        for n in range(len(results)):
            if not colours[n] is False and Latex.makeTextColoured == True:
                _colouredResults.append(Latex.commandStrings[colourType])

                _colouredResults[-1] += _nameByDistanceLightness[
                    (colours[n] + adjustBySemitones) % len(_nameByDistanceLightness)
                ]
                _colouredResults[-1] += "}"
                if colourType == "Highlight Start":
                    _colouredResults[-1] += Latex.commandStrings["Highlight End"]
                _colouredResults[-1] += "{" + str(results[n]) + "}"
                if not Latex.commandStrings[colourType] in _colouredResults[-1]:
                    raise ValueError(
                        "Colour tag did not happen for " + str(_colouredResults[-1])
                    )
            else:  # this colour is false
                _colouredResults.append(results[n])
        if not _returnAsList:
            return _colouredResults[0]
        else:
            # return _colouredResults
            return _colouredResults

    @classmethod
    def makeEmphasised(cls, result):
        return "\\emph{" + result + "}"

    @classmethod
    def makeTabularThirteenCells(
        cls, lineBeforeTwelveTabs=False, lineAfterTwelveTabs=False, extraCells=0
    ):
        """creates a tabular which can hold the answers
        centreResults will affect answers after the first."""
        _str = """\\begin{tabular}{"""
        # _str += '@{} p{'+ Latex.widthOfFirstCellStr + '}'
        _str += "@{} p{" + Latex.widthOfFirstCellStr + "}"
        if lineBeforeTwelveTabs:
            _str += "|"
        _str += ("@{} p{" + Latex.widthOfCellStr + "} @{}") * 12
        if lineAfterTwelveTabs:
            _str += "|"
        _str += ("@{} p{" + Latex.widthOfCellStr + "} @{}") * (
            Latex.numberOfCells + extraCells - 12
        )
        _str += "}\n"
        return _str

    @classmethod
    def arrangeRowInColumns(
        cls,
        data: list,
        positions: list,
        dataColoured=None,
        cellSize=None,
        firstCellSize=None,
        cellColours=None,
        totalCells=None,
        showDebug=False,
        alternatingRows=False,
        removeTextColourFromColouredCells=None,
        centreResults=False,
        extraCells=0,
        convertPageSymbolToSmallCircle=False,
    ):
        """if data[0]== '+/- 卦':
        input('arrangeRowInColumns()\ndata == {}\npositions == {}'.format(
            data,positions))"""
        if totalCells == None:
            totalCells = Latex.numberOfCells + extraCells
        if removeTextColourFromColouredCells == None:
            removeTextColourFromColouredCells = Latex.removeTextColourFromColouredCells
        if dataColoured == None:
            raise ValueError("provide the change coloured")
        if Latex.wayOfSpace:
            pass
        elif not Latex.wayOfSpace:
            positions = [i for i in range(len(positions))]
        if not len(data) == len(positions):
            if len(data) == len(positions):
                pass
            elif len(data) == len(positions) + 1:
                # Move cells over by one and put the way in the 0th cell
                positions = [0] + [i + 1 for i in positions]
            else:
                raise ValueError(
                    "these guys is not equal length\ndata:{}positions:{}\n".format(
                        data, positions
                    )
                )
        _unmodifiedPositions = positions

        def rotate(l, n):
            return l[-n:] + l[:-n]

        if cellSize is None:
            cellSize = Latex.widthOfCellInt
        if firstCellSize is None:
            firstCellSize = Latex.widthOfFirstCellInt
        """Make """
        # Check if result already has colour tags
        for i in data:
            if "}{" in str(i):
                raise ValueError(
                    "It appears that your data might have already had tags. "
                    "This will offset the calculation of their width " + data
                )
        # Get size of font and calculate how wide the results are, (how many cells wide)
        _font = ImageFont.truetype(Latex.fontStr, Latex.fontSize)
        _fontSmall = ImageFont.truetype(Latex.fontStr, Latex.fontSizeSmall)
        _fontScriptsize = ImageFont.truetype(Latex.fontStr, Latex.fontSizeScriptsize)

        # Sizes of the results in pts
        _sizes = []
        _sizesSmall = []
        _sizesScriptsize = []
        _fontChangeSmall = []
        _fontChangeScriptsize = []
        # _fontSizes = [12,11.5,11,10.5,10,9.5,9.0,8.5,8]
        # _fontSizes = [12,11,10,9,8]
        _fontSizes = [12]
        _sizeByFontSize = []
        _str = ""
        _rows = []
        _rowsUsed = 1
        _resultCellWidths = []
        _resultCellWidthsAdjusted = []
        _resultCellWidthsSmall = []
        _resultCellWidthsScriptsize = []
        _blankLine = "e" * totalCells
        _cellStrings = []
        _returnStr = ""
        _invalidAlternatingRows = False
        if Latex.useSmallCircles:
            _pageNumberReplaceStr = ""
        else:
            _pageNumberReplaceStr = ""

        for cellData in data:
            # getsize returns (x, y)
            # replacing character only because getsize is returning too wide on the subChange symbol
            _modifiedCellData = Latex.replaceSmallCircleBySymbol(cellData)
            _modifiedCellData = Latex.replacePianoBySymbol(_modifiedCellData)

            if "pdf" in _modifiedCellData:
                input(
                    "juss in case: _modifiedCellData = "
                    + _modifiedCellData
                    + "    "
                    + Latex.commandStrings["Small Circle Command Start"]
                )

            _modifiedCellData = _modifiedCellData.replace(
                Book.unicodeChars["Change Number"], _pageNumberReplaceStr
            )
            _modifiedCellData = _modifiedCellData.replace(
                Book.unicodeChars["Chapter Number"], _pageNumberReplaceStr
            )
            # acount for extra space
            # _sizes[-1] += Latex.widthOfColSepInt

            # adjust for LetterSpace
            # _sizes[-1] = _sizes[-1] + Latex.letterSpace * len(str(_sizes[-1]))
            _sizes.append(
                _font.getsize(str(_modifiedCellData))[0] + Latex.widthOfColSepInt * 2
            )
            _sizesSmall.append(
                _fontSmall.getsize(str(_modifiedCellData))[0]
                + Latex.widthOfColSepInt * 2
            )
            _sizesScriptsize.append(
                _fontScriptsize.getsize(str(_modifiedCellData))[0]
                + Latex.widthOfColSepInt * 2
            )
            # convert to cm
            _sizes[-1] *= Latex.pointSize
            _sizesSmall[-1] *= Latex.pointSize
            _sizesScriptsize[-1] *= Latex.pointSize
            _sizeByFontSize.append([])

            for s, size in enumerate(_fontSizes):
                _sizedFont = ImageFont.truetype(Latex.fontStr, size)
                _sizeByFontSize[-1].append(
                    _sizedFont.getsize(str(_modifiedCellData))[0]
                    + Latex.widthOfColSepInt * 2
                )
                _sizeByFontSize[-1][-1] *= Latex.pointSize

        # These are called rows, but they are actually sub-rows

        # Start a blank canvas
        for row in range(12):
            _rows.append(_blankLine)
        _resultWidthsBySize = []
        for i, result in enumerate(data):
            # Find out how many cells it takes to fit the result
            if i == 0:
                _thisCellSize = Latex.widthOfFirstCellInt
            else:
                _thisCellSize = cellSize
                # How does it switch cell types?
            _resultCellWidths.append(_sizes[i] / _thisCellSize)
            _resultCellWidthsSmall.append(_sizesSmall[i] / _thisCellSize)
            _resultCellWidthsScriptsize.append(_sizesScriptsize[i] / _thisCellSize)
            _resultCellWidthsAdjusted.append(_resultCellWidths[-1])
            _resultWidthsBySize.append([])
            for s, size in enumerate(_fontSizes):
                _sizedFont = ImageFont.truetype(Latex.fontStr, size)
                # print('result {} s {} size {} cells {} is what she wrote'.format(result, s, size,
                #                                               _sizeByFontSize[i][s] / _thisCellSize))
                _resultWidthsBySize[-1].append(_sizeByFontSize[i][s] / _thisCellSize)

        for i in range(len(_resultCellWidths)):
            if i + 1 < len(positions):
                _roomyWidth = positions[i + 1] - positions[i]
            else:
                _roomyWidth = totalCells - positions[i]
            _resultCellWidth = _resultCellWidths[i]
            _resultCellWidthSmall = _resultCellWidthsSmall[i]
            _resultCellWidthScriptsize = _resultCellWidthsScriptsize[i]
            for w, width in enumerate(_resultWidthsBySize):
                pass  # print(w,width,_fontSizes[w])
            # input('roomyWidth {} one {}'.format(_roomyWidth,1))
            if _resultCellWidth >= 1:  # _roomyWidth:
                if _resultCellWidthSmall < 1 and not any(
                    [i > 1 for i in _resultCellWidthsSmall]
                ):
                    _fontChangeSmall.append(i)
                    _resultCellWidthsAdjusted[i] = _resultCellWidthSmall
                    print(
                        "\narrangeRowInColumns making this one small saves a row,\n{} \n{},\n{}\n".format(
                            _resultCellWidths, _resultCellWidthsSmall, data
                        )
                    )
                elif _resultCellWidthScriptsize < 1 and not any(
                    [i > 1 for i in _resultCellWidthsScriptsize]
                ):
                    if _resultCellWidthSmall < 1:
                        _fontChangeSmall.append(i)
                        _resultCellWidthsAdjusted[i] = _resultCellWidthSmall
                        if showDebug:
                            print(
                                "\narrangeRowInColumns making this one script saves a row,\n{} \n{},\n{}\n{}\n".format(
                                    _resultCellWidths,
                                    _resultCellWidthsSmall,
                                    _resultCellWidthsScriptsize,
                                    data,
                                )
                            )
                    else:
                        _fontChangeScriptsize.append(i)
                        _resultCellWidthsAdjusted[i] = _resultCellWidthScriptsize
                        if showDebug:
                            print(
                                "\narrangeRowInColumns making this one script saves a row,\n{} \n{},\n{}\n{}\n".format(
                                    _resultCellWidths,
                                    _resultCellWidthsSmall,
                                    _resultCellWidthsScriptsize,
                                    data,
                                )
                            )

        # First stick the first result in the first cell
        # _rows[0][0] = 'b'
        """if _resultCellWidths[0] > 1:
            for extraCol in range(math.floor(_resultCellWidths[0])):
                #try:
                _rows[0][extraCol+1] = 'c'
                #except:
                    #print('exceptionally',extraCol+1,len(_rows))
                    #raise ValueError(extraCol,_rows)"""
        _foundCell = None
        _lastRow = 0

        for idx, s in enumerate(data):
            _width = math.floor(_resultCellWidthsAdjusted[idx]) + 1
            _widthSmall = math.floor(_resultCellWidthsSmall[idx]) + 1
            _position = positions[idx]
            # Find a cell
            _foundCell = False
            # print(rotate(list(range(_rowsUsed+1)),_lastRow),'burp')
            for i in range(12):
                # print(idx,i,'idx and i')
                if _foundCell:
                    break
                # Pick the next row
                _row = _rows[i]
                # print(_position,_width,_row)
                # if all([cell == 'e' for cell in _row[_position:_position + _width]]):
                if _row[_position : _position + _width] == "e" * _width:
                    _cellStrings.append(("b" + "c" * (_width - 1)))
                    _rows[i] = (
                        _rows[i][:_position]
                        + _cellStrings[idx]
                        + _rows[i][_position + _width :]
                    )
                    _rowsUsed = max(_rowsUsed, i + 1)
                    # print(_rows[i], 'when adding one')
                    # input('throw it down')
                    _foundCell = True
                    _lastRow = i
                elif (
                    False
                ):  # _row[_position:_position + _widthSmall] == 'e' * _widthSmall:
                    # disabled checking for small ones here
                    print("converting to smaller font should be happening {}".format(s))
                    _cellStrings.append(("b" + "c" * (_widthSmall - 1)))
                    _rows[i] = (
                        _rows[i][:_position]
                        + _cellStrings[idx]
                        + _rows[i][_position + _widthSmall :]
                    )
                    _rowsUsed = max(_rowsUsed, i + 1)
                    # print(_rows[i], 'when adding one')
                    # input('throw it down')
                    _foundCell = True
                    _lastRow = i
                    # small font makes it squish
                    _fontChangeSmall.append(idx)
                else:
                    # print(_rows)
                    pass
                    # continue
                    # input('it doesnt fit')
            if not _foundCell:
                # print('\n'.join(_rows), '\n', data, _resultCellWidths, positions, 'result output\n')
                # raise ResultsTooWideError 'there were not enough cells to contain the result.' + str(data)+ str(_rows)
                raise ResultsTooWideError

        # Trim the blank lines
        _rows = _rows[: _rows.index(_blankLine)]

        if len(_rows) > 1 and alternatingRows == True:
            # Attempt a directly alternating format
            _alternatingRows = [_blankLine for i in range(len(_rows))]
            _r = 0
            _alternatingRows[0] = (
                _cellStrings[0] + _alternatingRows[0][len(_cellStrings[0]) :]
            )
            _idx = 1
            _firstRow = 0
            for r, row in enumerate(_rows):
                if row[1] == "b":
                    _firstRow = r
                    break

            for row in range(len(_cellStrings) - 1):
                _width = len(_cellStrings[_idx])
                _rowMod = (row + _firstRow) % len(_rows)
                _pos = positions[_idx]
                _alternatingRows[_rowMod] = (
                    _alternatingRows[_rowMod][:_pos]
                    + _cellStrings[_idx]
                    + _alternatingRows[_rowMod][_pos + _width :]
                )
                _idx += 1

            # Check whether its values are equal to non-alternating rows
            if showDebug:
                print(
                    "rows vs alternatingrows..",
                    "\n".join(_rows),
                    "\n".join(_alternatingRows),
                    sep="\n\n",
                )
            for letter in ("e", "c", "b"):

                if not "".join(_rows).count(letter) == "".join(_alternatingRows).count(
                    letter
                ):
                    # if not _rows.join('').count(letter) == _alternatingRows.join('').count(letter):
                    _invalidAlternatingRows = True

                    if showDebug:
                        print(
                            "alternating rows did not work out. rows have "
                            + str("".join(_rows).count(letter))
                            + letter
                            + "\n"
                            + str("".join(_alternatingRows).count(letter))
                            + letter
                            + "\n"
                            + "\n".join(_rows)
                            + "\n\n"
                            + "\n".join(_alternatingRows)
                        )

                    # raise ValueError(str(''.join(_rows).count(letter)) + ' != ' +str(''.join(_alternatingRows).count(letter) )+ letter + str(_alternatingRows) + str( _rows))

        else:
            _alternatingRows = None

        # Find the biggest cell
        if _resultCellWidths[-1] > Latex.mostCellsOfAResult:
            Latex.mostCellsOfAResult = _resultCellWidths[-1]
            Latex.biggestCell = data[-1]
            Latex.mostPointsOfACell = _sizes[-1]

            # print(Latex.mostCellsOfAResult,Latex.biggestCell,"cell size exceeded")
        if not _alternatingRows is None and not _invalidAlternatingRows:
            _rows = _alternatingRows
            if showDebug:
                print("\n", "\n".join(_alternatingRows), "\n", sep="")
        else:  # print('\n'.join(_rows),sep='')
            pass
        if showDebug:
            print(
                data,
                _cellStrings,
                _resultCellWidths,
                positions,
                _resultCellWidthsSmall,
                "result output\n",
            )
        _numberOfCells = 0
        for row in _rows:
            _numberOfCells += row.count("b")
        if not _numberOfCells == len(data):
            raise ValueError("The table is fucked up")

        # Insert font size tags
        for fontChange in _fontChangeSmall:
            data[fontChange] = Latex.makeDataSmaller(data[fontChange], "small")
            dataColoured[fontChange] = Latex.makeDataSmaller(
                dataColoured[fontChange], "small"
            )
        for fontChange in _fontChangeScriptsize:
            data[fontChange] = Latex.makeDataSmaller(data[fontChange], "scriptsize")
            dataColoured[fontChange] = Latex.makeDataSmaller(
                dataColoured[fontChange], "scriptsize"
            )

        for row in _rows:
            # print('positions of row', row, len(row))
            for pos, char in enumerate(row):
                if pos + 1 < len(row) and char == "b":
                    # Put the font size before colouring and placing the rest
                    if row[pos + 1] in ("e", "b"):
                        if centreResults and pos > 0:
                            # _returnStr += '\\hfil '
                            # _returnStr += '{\\kern 2pt}'
                            _returnStr += "\\hspace{10pt}"
                        if not cellColours is None:
                            if not removeTextColourFromColouredCells:
                                _thisCell = Latex.makeDataColoured(
                                    str(dataColoured[positions.index(pos)]),
                                    cellColours[positions.index(pos)],
                                    colourType="Colour Cell",
                                )
                            else:
                                _thisCell = Latex.makeDataColoured(
                                    str(data[positions.index(pos)]),
                                    cellColours[positions.index(pos)],
                                    colourType="Colour Cell",
                                )
                        else:
                            _thisCell = str(dataColoured[positions.index(pos)])

                        # if len(_fontChangeSmall)>0 or positions.index(pos) in _fontChangeSmall:
                        #    input('blahg b data \n{}\npos{}\nfontChageSmll {} \npositions {} \n positions.index(pos){}'.format(
                        #        data, pos, _fontChangeSmall,positions,positions.index(pos)))
                        _returnStr += _thisCell
                        _returnStr += " & "
                    elif row[pos + 1] == "c":
                        _widthOfCell = 1
                        for extraCell in row[pos + 1 :]:
                            if extraCell == "c":
                                _widthOfCell += 1
                            else:
                                break

                        _multicolumnSize = Latex.widthOfCellInt * _widthOfCell
                        if pos == 0:
                            _multicolumnSize -= Latex.widthOfCellInt
                            _multicolumnSize += Latex.widthOfFirstCellInt
                        _multicolumnSize = round(_multicolumnSize, 2)
                        _returnStr += "\\multicolumn{"

                        _returnStr += str(_widthOfCell) + "}"
                        # _returnStr +=       '{' + '@{} p{' + str(_multicolumnSize) + 'cm}}{'
                        _returnStr += "{" + "@{} l}{"
                        if centreResults and pos != 0:
                            _returnStr += "\\hspace{10pt}"
                        if dataColoured == None:
                            raise ValueError(
                                "Specify makeTextColoured with dataColoured."
                            )
                            _colour = [i - 1 for i in _unmodifiedPositions[1:]][pos - 1]
                            # print([i-1 for i in _unmodifiedPositions[1:]],data,pos-1)
                            # input()
                            # _returnStr += str(Latex.makeDataColoured(str(data[positions[:].index(pos)]),pos-1)) + '} & '
                            # hardwired
                            # First column is not coloured by default
                            if pos == 0:
                                _returnStr += str(data[positions.index(pos)]) + "} & "
                            else:
                                _returnStr += (
                                    Latex.makeDataColoured(
                                        data[positions.index(pos)], _colour
                                    )
                                    + "} & "
                                )
                        else:

                            _returnStr += (
                                str(dataColoured[positions.index(pos)]) + "} & "
                            )

                elif char == "e":
                    if pos != len(row) - 1:
                        _returnStr += " & "
                elif char == "c":
                    pass
            _returnStr += Latex.commandStrings["Table Line Break"] + "\n"
        if convertPageSymbolToSmallCircle == True:
            _returnStr = Latex.replacePageStrsBySmallCircles(_returnStr)

        return _returnStr

    @classmethod
    def makeChangeGraphicTable(
        cls, change: Change, greyScale=True, renderIfNotFound=True
    ):
        _str = "%Data made with Latex.makeChangeGraphicTable(change={},greyScale={})\n".format(
            change, greyScale
        )
        _imageTypes = [
            "Accordion",
            "Key",
            "Piano",
            "Guitar",
        ]
        # Don't use subChange break at beginning or end of tabs
        # _tabs = ['Accordion','Key']
        _tabs = ["Key", "Piano", "Guitar", "Accordion"]  # 'Page Break'
        # _tabAlignments = ['p{.2\\textwidth} '] * 3
        _tabAlignments = ["l "] * 3
        _guitarBoard = Fretboard()
        _theseTabs = _tabs
        _thoseTabs = []
        if "Page Break" in _tabs:
            _theseTabs = _tabs[0 : _tabs.index("Page Break") + 1]
            _thoseTabs = _tabs[_tabs.index("Page Break") + 1 :]
        _str += "\\centering "
        # _str += '\\begin{adjustbox}{max height=.7\\textheight,max width=.8\\textwidth,keepaspectratio}'
        _str += "\\begin{adjustbox}{max width=.7\\textwidth,keepaspectratio}"
        _str += "\\begin{tabular}{" + "l"
        _str += "l " * (len(_theseTabs) - 1)
        # _str += ''.join([_tabAlignments[i] for i in range(len(_theseTabs)-1)])
        _str += "}\n"
        # _str += '\\hline\n'

        for key in JazzNote.noteNameFlats:
            for t, tab in enumerate(_theseTabs + _thoseTabs):
                if tab in _theseTabs:
                    _size = len(_theseTabs)
                else:
                    _size = len(_thoseTabs)
                if tab == "Key":
                    _str += JazzNote.convertNoteToRealUnicodeStr(key)
                elif tab in ("Piano", "Guitar", "Accordion"):
                    # _str += '\\includegraphics[width=\\textwidth/'+str(_size)+']{'
                    if tab != "Accordion":
                        filetype = "pdf"
                    else:
                        filetype = "png"
                    _str += "\\includegraphics[height=\\textheight/" + "12" + "]{"
                    _str += Graphics.getDiagramPath(
                        diagramType=tab,
                        change=change,
                        key=key,
                        greyScale=False,
                        includeGraphicsPath=False,
                        filetype=filetype,
                        renderIfNotFound=renderIfNotFound,
                        includeFileExtension=True,
                    )
                    _str += "}"

                if t != len(_theseTabs) - 1 and tab != "Page Break":
                    _str += " & "
                if tab == "Page Break":
                    _str += "\\end{tabular} "
                    _str += "\\clearpage\n"
                    _str += "\\begin{tabular}{" + "|l" * (len(_thoseTabs) + 1) + "|}"
                _str += "\n"
            _str += "\\\\"
            # _str += '\\hline\n'
        _str += "\\end{tabular}"
        _str += "\\end{adjustbox}"
        # aka instrumental chart
        return _str

    @classmethod
    def makeTable(cls):
        return "\\begin{table}[ht]{}\n"

    @classmethod
    def insertDiagramToPageBackground(
        cls,
        change: Change,
        key=None,
        resolution=None,
        diagramType=None,
        filetype=None,
        transparency=0.05,
    ):
        _returnStr = ""
        if diagramType == None:
            diagramType = Latex.backgroundDiagramType
        if filetype == None:
            filetype = Latex.backgroundDiagramFiletype
        if resolution is None:
            resolution = Latex.backgroundDiagramResolution
        if key is None:
            key = Book.rootColourKey
        if Graphics.seeIfDiagramExists(
            change,
            key,
            resolution,
            diagramType="FCircle",
            filetype=filetype,
            greyScale=False,
            invertColour=False,
        ):
            _diagram = Graphics.getDiagramPath(
                change=change,
                key=key,
                resolution=resolution,
                includeFilename=True,
                diagramType="FCircle",
                filetype=filetype,
                includeGraphicsPath=not Latex.useRelativeGraphicsPath,
            )
            # return '\\tikz[remember picture,overlay] \\node[opacity=0.07,inner sep=15pt] at (current subChange.center){\\includegraphics[width=\\linewidth,height=\\linewidth]' +\
            # '{'+Graphics.getFCirclePath(change,colourKey,resolution,includeFilename=True,includeGraphicsPath=not Latex.useRelativeGraphicsPath)+\
            # '}};'
            return (
                """\\AddToShipoutPicture*{\\put(0,0){\\parbox[b][\\paperheight]{\\paperwidth}{%\n"""
                + """\\vfill \\centering {\\transparent{"""
                + str(round(transparency, 2))
                + """}\includegraphics[width=1\\textwidth]{"""
                + _diagram
                + """}}%\n\\vfill}}}"""
            )
            # input(_str)
            return _str
        else:
            raise ValueError(
                "FCircle {} does not exist".format(
                    Graphics.getFCirclePath(
                        change, colourKey, resolution, includeFilename=True
                    )
                )
            )