from __future__ import annotations, print_function
import os
from Utility import Utility
input = Utility.input
class Project:
    # masta
    # directory = 'C:\\Users\\Edrihan\\PycharmProjects\\wayOfChange\\' #Old path
    # directory = 'C:\\Users\\Ed\\wayOfChange\\'
    directory = os.path.realpath(os.path.join(os.path.realpath(__file__), '../','../'))

    #directory = os.path.realpath(os.path.join(os.path.realpath(__file__), '../', '../'))

    directoryExternal = r'G:\grailofscalegraphicsHD'
    directoryTex = os.path.join(directory, "tex")
    directoryJS = os.path.join(directory, "scripts")
    directoryGraphics = os.path.join(directory, "Graphics")
    directoryReactNative = "C:\\Users\\Edrihan\\Desktop\\WayOfChangeRN\\" #shit this got deleted
    directoryReactNativeAssets = (
        directoryReactNative + "\\android\\app\src\main\\res\\raw\\"
    )
    testWillSmith = 0
    testMulticolouredChords = 0
    makingFinalCopies = 0
    rootGrailOfScaleTexFilename = "document"
    testGetChordQuality = 0
    makeGrailOfScale = 0
    makePDFTimes = 0
    makeCondensedBookTex = 0
    makeCondensedBookPDFTimes = 0  # 3
    renderEachPageSeperately = 1
    makeLittleBook = 0
    condensedWOCFilename = "condensedWOC"
    singlePageGrailOfScaleFilename = "SingleChangeGOSDocument"
    singlePageGrailOfScalePath = os.path.join(
        directoryTex, singlePageGrailOfScaleFilename
    )
    removeAuxFiles = 1  # If none, will remove if makePDFTimes > 1
    makeWebAssets = 0
    externaliseDataForPython = 0
    makeColourSchemesTex = 0
    fontMapTexPath = os.path.join(directoryTex + "fontMap.tex")
    makeFontMapTex = 0
    makeGraphicalPage = 0
    makeBigBook = False
    makeKeysDiagrams = 0
    findMissingFCircles = 0
    makeCircles = 1
    makeCirclesTypes = ["SCircle", "FCircle"] # ['PCircle']
    makeTShirts = 0
    makeFretboards = 0
    makeAccordions = 0
    makeTradingCards = 0
    makeNGrams = 0
    makeMidiChanges = 0
    makeSeptatonicSongMidi = 0
    makeRandomPoems = 0
    makeFCircleCharts = 0
    makeMultiFCircleImage = 0
    makeInstrumentalChart = 0
    makeHexagramsToChangeChart = 0
    makeLegend = 0
    legendFilename = "miniLegend.tex"
    makeAllFCircleCharts = 1
    makeWayOfBitmap = 0
    wayOfBitmapFilename = "wayOfSquares.tex"
    makeHexagramList = 0
    makeHexagramTable = 0
    makeTetragramTable = 0
    makeTrigramTable = 0
    trigramTableFilename = "trigramTable1.tex"
    tetragramTableFilename = "tetragramTable1.tex"
    hexagramTableFilename = "hexagramTable1.tex"
    testMakeFromPageNumber = 0
    checkBrailleChars = False
    listFonts = 0
    displayWords = 0
    makeRingToChange = 0
    findLinesWhereBookGetItemOccurred = 0
    validateScaleNames = 0
    findLongestHexagramNames = 0
    testKeyChanges = 0
    testMelas = 0
    makeBeatlesBook = 0
    launchAudioApp = 0
    # plot function is created for
    # plotting the graph in
    # tkinter window
    
    
    @classmethod
    def createWidgets(cls):
        global fig
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)
        fig=plt.figure(figsize=(8,8))

        #ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=False)
        canvas=FigureCanvasTkAgg(fig,master=root)
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.show()

        self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.plot(canvas,ax))
        self.plotbutton.grid(row=1,column=1)

    def plot():


        filepath = select_file()


        # list of squares
        y = [i ** 2 for i in range(101)]
        #input(y)
        y, sr = librosa.load(filepath)
        #input(y)
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        print('started making waveshow')

        fig.clear()

        # list of squares
        #y = [i ** 2 for i in range(101)]
        #input('lkist of 2s')

        # adding the subplot

        #ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        #plot1.plot(y,ax)
        #plot1 = librosa.display.waveplot(y,xaxis='s',ax=ax)

        #print('done making waveshow')
        plt.show()
        print(onset_frames, onset_times)  # frame numbers of estimated onsets

        #plt.show()
        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        #plot1.plot(y)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=Project.root)
        canvas.draw()

        # placing the canvas on the Tkinter window
        #canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       Project.root)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

    @classmethod
    def renderFretboards(cls,core=0,cores=6,instruments=['Guitar'],indicateNotesWithFCircle=False):
        print("making fretboards. Check whether you are using multicore.")
        fretboards = []
        for instrument in instruments:
            if instrument in Fretboard.instruments:
                fretboards.append(Fretboard(instrument=instrument))
            else:
                raise TypeError('asdfasdfasdfasdfasd')
        for fretboard in fretboards:
            for greyScale in (False,):
                # for key in ('E',):

                # for change in range(-2047,2048):

                # input('just doing one')

                _changeRange = range(-2047, 2048)
                #_changeRange = range(1361, 1362)
                # _changeRange = range(9)
                _fretboardFiletypes = ["pdf"]
                fretboard.renderFretboards(
                    changes=[Change.makeFromChangeNumber(c) for c in _changeRange[core::cores]] + [Change([])],
                    #keys=JazzNote.noteNameFlats[0:],
                    keys=JazzNote.noteNameFlats[core::cores],
                    greyScale=False,
                    makeNewIndicatorDiagrams=True,
                    filetypes=_fretboardFiletypes,indicateNotesWithFCircle=indicateNotesWithFCircle,
                )

                _isFirstFretboard = False
                """fretboard.renderFretboards(
                    changes=[Change([])], keys=['C'],#JazzNote.noteNameFlats[1],
                    greyScale=False,filetypes=_fretboardFiletypes)"""

        input("finished with making {} fretboards...".format(instruments))
    
    @classmethod
    def renderPianos(cls, changes=None, core=0, cores=1, indicateNotesWithDiagramType='FCircle', invertColour=False, greyScale:(bool)=False, voicingType="Scale"):
        thePiano = Piano()

        _makeNewIndicatorDiagrams = True
        # for greyScale in (False, True):
        for greyScale in (greyScale,):
            # for key in ('Db',):
            # for invertColour in (False, True):
            for invertColour in (invertColour,):
                # Piano.renderPianoToFile(theBook[1361],
                #                   key=key,
                #                   )
                # for change in range(-2048,2049):

                # changeRange = range(1361, 1362)
                # changeRange = (1233,1361)
                # input("hey changeRannge {}".format(Change.makeFromChangeNumber(-1361)))
                thePiano.makePianoFiles(
                    changes=changes,  # [Change.makeFromChangeNumber(c) for c in changeRange],
                    keys=JazzNote.noteNameFlats[core::cores],
                    greyScale=greyScale,
                    invertColour=invertColour,
                    makeNewIndicatorDiagrams=_makeNewIndicatorDiagrams,
                    filetypes=["pdf"],
                    voicingType= voicingType,
                )

                _makeNewIndicatorDiagrams = False

            # print(thePiano)
            # input('testing the piano')

        print("finished maaking pianos\n" * 10)


    @classmethod
    def makeCondensedChangeTex(
        self,
        change,
        strBetweenWays=None,
        linesInTitle=2,
        cols=4,
        tabuliseChordWays = True,
        tabuliseBySemitonePosition=True,
        showDebug=True,
        rootKey="C",
        externalGraphicsPath=True,
        useCircleBehindJazzNotes=False,
        useCircleBehindWayOfWord=False,
        useCircleBeforeScaleChords=False,
        useCircleBehindHexagram=False,
        includeBackgroundGraphic=False,
        putGraphicsBannerInSubtitle = False,
        invertColour=False,
        useColour=True,
        includeLatexColorboxSettings=True,
        makePdfBookmark=False,
        debugOutput=True,
        growToLeftBy='.731cm',#'.731cm', #.94 cm
        growToRightBy='.731cm',#'6cm', #.94 cm here should be a - b  \standaloneconfig{border=0cm 0cm here 0cm}
        ways=None,
        chordsOfChangeType=None,
    ):

        #input('\nthe friggin thing is "' + str(change)+'"')
        if ways == None:
            if chordsOfChangeType == "Mode Family":
                ways = Book.condensedWaysModeFamily
                cols = 1
            elif chordsOfChangeType in (None,'Chords Of Change'):
                ways = Book.condensedWays
                cols == 4
            else:
                raise ValueError('chordsOfChangeType: {} must be one of these: {}'.format(chordsOfChangeType,"'Mode Family', 'Chords Of Change', or None"))
        assert cols in (1,4), 'ya right, right?'
        #assert not useCircleBeforeScaleChords
        #raise TypeError('this is obsolete, use Project.renderChordsOfChangePdfs')
        # input('{}'.format(',\n'.join([l + '=' + l for l in locals()])))
        print("calling Book.makeCondensedChangeTex({})".format(locals()))
        if useCircleBehindWayOfWord:
            raise ValueError("this will probably fuck up at change -1361")

        _lineBreak = "\\\\\n"
        if strBetweenWays == None:
            strBetweenWays = ""
            # strBetweenWays = '\\hfill '
            # strBetweenWays = '\\hfill '+Book.unicodeChars['Chinese Seperator']+'\\hfill '
        _str = ""
        """_str += '\\tcbset{enhanced,colback="""+rootKey+"""!5!white,boxrule=0.1pt,'
        _str += 'colframe="""+rootKey+"""!50!black,'
        _str += 'fonttitle=\\bfseries,  }"""

        if showDebug:
            print("ways ==", ways)
        if type(change) not in (Change, int):
            raise TypeError("expects a change")
        #[size=normal,title,small,fbox,tight,minimal]
        _boxSize = 'fbox'
        #_colorboxSettings = "\\tcbset{boxsep=0mm,size="+_boxSize+",boxrule=0.2pt,toptitle=.41cm,bottomtitle=-.59cm,top=0cm,bottom=-0.1cm,left=0mm,right=0mm,leftupper=0mm,coltitle=pink,rightupper=0mm,colframe=black,colback="+rootKey+"!5,subtitle style={boxrule=0.2pt,colback="+rootKey+"!10!white,top=0cm,bottom=-0.1cm,left=0mm,right=0mm,size="+_boxSize+"}}"
        _colorboxSettings = "\\tcbset{boxsep=0mm,size="+_boxSize+",boxrule=0.2pt,toptitle="+('0em' if ('Graphics Banner' not in ways or putGraphicsBannerInSubtitle) else '0em')+",bottomtitle="+("-\\baselineskip" if ('Graphics Banner' in ways or putGraphicsBannerInSubtitle) else '0em')+",top=0cm,bottom=-0.1cm,left=0mm,right=0mm,leftupper=0mm,coltitle=pink,rightupper=0mm,colframe=black,subtitle style={boxrule=0.2pt,colback="+rootKey+"!10!white,top=0cm,bottom=-0.1cm,left=0mm,right=0mm,size="+_boxSize+"}}"
        _smallColorBoxSettings = (
            #"\\definecolor{blankNameColour}{rgb}{0.122, 0.435, 0.698}"
            "\\definecolor{blankNameColour}{rgb}{0.6, 0.1, 0.698}"
        )
        #_smallColorBoxSettings += "\\newtcbox{\\nameBox}{on line,  colframe="+rootKey+"!0!black,colback="+rootKey+"!5!white,boxrule=0.1pt,arc=3pt,boxsep=0pt,left=12pt,right=150pt,top=12pt,bottom=1pt}"
        _smallColorBoxSettings += ""

        _multiColouredLatex = "\\newlength{\\lengthofmulticolourtext}\n"
        _multiColouredLatex += "\\newlength{\\heightofmulticolourtext}\n"

        _str += _multiColouredLatex + _colorboxSettings + _smallColorBoxSettings

        _colours = Colour.getTransposedColours(
            colourTranspose=JazzNote.distanceFromC(rootKey)
        )
        _colourTags = Colour.getTransposedColourTags(
            colourTranspose=JazzNote.distanceFromC(rootKey), neutralColours=True
        )
        _outlinedTextLineWidth = 0.4
        if invertColour:
            _inkColourTag = "white"
            _paperColourTag = "black"
        else:
            _inkColourTag = "black"
            _paperColourTag = "white"

        if includeLatexColorboxSettings:
            changeStr = _colorboxSettings + _smallColorBoxSettings
        _changeLengthData = ""
        _pageStr = ""
        _titleStr = ""
        _subtitleStr = ''
        if type(change) == Change:
            c = change.getChangeNumber()
        else:
            c = change
            change = self[change]
        # Now type(c) == int and type(change) == Change
        _pdfBookmark = ""
        if makePdfBookmark:
            raise TypeError('depracated. use this option in the makebook function')
            _pdfBookmark = change.makePdfLink()

        # print('random shit',str(c), end=', ')
        for w, way in enumerate(ways):
            if showDebug:
                print("making Condensed Chang by way of", way, end=":  ")
            _changeByWay = ""
            if way == "Line Break":
                _changeByWay = _lineBreak
            elif way == 'Prime Inverse':
                _primeInverse = Book.theBook.getTitle(change.getInverse().getNormalForm().getPrimeForm(),['Unique Change Number'])
                if False and _primeInverse == Book.theBook.getTitle(change,['Unique Change Number']):
                    _changeByWay = 'hey'
                else:
                    _changeByWay = Book.unicodeChars['yin-yang'] + _primeInverse


            elif way == 'Prime Enantiomorph':
                if change.getReverse() in [change.mode(m) for m in range(len(change))]:
                    _changeByWay = Change.infoWaySymbols["Is Palindrome"]
                else:
                    _changeByWay = Change.infoWaySymbols['Is Achiral'] + Book.theBook.getTitle(change.getReverse().getPrimeForm(),['Unique Change Number'])
                #_changeByWay = change.getEnantiomorph() if change.getEnantiomorph() not in (change,) else Change.infoWaySymbols['Is Palindrome']+str(change.getEnantiomorph().getReverse())

            elif way == "Graphics Banner":
                #_changeByWay = ['\\tcbsubtitle{',Latex.insertSmallDiagram(change, rootKey, diagramType='SCircle', filetype='pdf',
                _changeByWay = '\\hfill '.join([Latex.insertSmallDiagram(change, rootKey, diagramType='SCircle', filetype='pdf',
                                                        includeGraphicsPath=True, imgtag='bigpianoimg',invertColour=True),
                    Latex.insertSmallDiagram(change, rootKey, diagramType='Piano', filetype='pdf',
                                                        includeGraphicsPath=True, imgtag='bigpianoimg',invertColour=False),

                                         Latex.insertSmallDiagram(change, rootKey, diagramType='FCircle', filetype='pdf',
                                                                  includeGraphicsPath=True, imgtag='bigpianoimg',invertColour=True,resolution=256),
                                         Latex.insertSmallDiagram(change, rootKey, diagramType='PianoThirds', filetype='pdf',
                                                                  includeGraphicsPath=True, imgtag='bigpianoimg',invertColour=False),
                                         Latex.insertSmallDiagram(change, rootKey, diagramType='PCircle',
                                                                  filetype='pdf',
                                                                  includeGraphicsPath=True, imgtag='bigpianoimg',invertColour=False)
                ]) + '\\\\\n'

                _subtitleStr = _changeByWay
                #input(_subtitleStr)
                continue

            elif way == "Piano":
                _changeByWay = Latex.insertSmallDiagram(change, rootKey, diagramType='Piano', filetype='pdf',
                                                        includeGraphicsPath=True, imgtag='pianoimg')
            elif way == 'Guitar':
                _changeByWay = Latex.insertSmallDiagram(change, rootKey, diagramType='Guitar', filetype='pdf',
                                                        includeGraphicsPath=True, imgtag='guitarimg')
            elif way == "Hexagram Symbol Name":
                _changeByWay = change.getHexagram(
                    hexagramWays=["symbol", "name"],
                    concatenatePerHexagram=True,
                    insertStrBetweenSections="",
                    insertStrBetweenAnswers="",
                    decorateSymbolWith="PCircle" if useCircleBehindHexagram else False,
                    useGraphicSymbol=True,
                    filetype="pdf",
                    externalGraphicsPath=externalGraphicsPath,
                    invertColour=not invertColour,
                )

                _changeByWay = [
                    "{"
                    + ("\\hspace{0.3cm}" if useCircleBehindHexagram else "")
                    + "\\"
                    + FontMap.fontByWay["Hexagram"]["latexName"]
                    + " " + h
                    + "}"
                    for h in _changeByWay
                ]
                '''_changeByWay = [Latex.outlineText(
                        text=h,
                        colourTag=_paperColourTag,
                        outlineColourTag=_inkColourTag,
                        lineWidth=_outlinedTextLineWidth,
                    ) for h in _changeByWay]'''

                # input('geaorg "\n{}\n"'.format(_changeByWay))
                # input('"{}"'.format(_changeByWay[0]))
            elif way == "Word":
                # _changeByWay = ''.join(change.getHexagram(['syllable']))
                if useCircleBehindWayOfWord:
                    _changeByWay = "".join(
                        change.getTrigram(
                            ["syllable"],
                            decorateSyllableWith="PCircle",
                            externalGraphicsPath=externalGraphicsPath,
                            paperColour='black',inkColour='white'
                        )
                    )
                else:
                    _changeByWay = "".join(
                        change.getTrigram(["syllable"], colourResult=True)
                    )
                    """_changeByWay = Latex.outlineText(text=_changeByWay,
                                                 colourTag=_paperColourTag,
                                                 outlineColourTag=_inkColourTag,
                                                 lineWidth=_outlinedTextLineWidth)"""
            elif way == "Jazz":
                _changeByWay = []
                _notesByWay = change.straightenDegrees(
                    Change.allowedNoteNamesSuperset + Change.allowedNoteNamesWeird
                )
                """input('yazz {}\nbazz {}\ndazz{}'.format(
                    _notesByWay.__iter__(),
                    [i for i in _notesByWay],
                    _notesByWay.notes))"""

                # Add notes graphic behind answer
                _diagramPaths = []
                # print('poopoo')
                # input('{} {}'.format(_notesByWay,type(_notesByWay)))
                for n in range(len(change)):
                    # print(n,_notesByWay,change)
                    # input(Change(_notesByWay[n]).getColouredSelf())

                    if useCircleBehindJazzNotes:
                        _diagramPaths.append(
                            Graphics.getDiagramPath(
                                change=Change([_notesByWay[n]]),
                                key=rootKey,
                                diagramType="PCircle",
                                filetype="pdf",
                                resolution=FCircle.vectorSmallResolution,
                                externalGraphicsPath=externalGraphicsPath,
                            )
                        )
                        _changeByWay.append(
                            Latex.textGraphic(
                                text=_notesByWay[n],
                                graphPath=_diagramPaths[n],
                                diagramType="PCircle",
                                outlineText=True,
                                colourTag=_colourTags[change[n].semitonesFromOne()],
                                lineColourTag=_inkColourTag,
                                lineWidth=_outlinedTextLineWidth,
                            )
                        )

                    else:
                        '''_changeByWay.append(Latex.outlineText(
                                text=_notesByWay[n],
                                colourTag=_colourTags[change[n].semitonesFromOne()],
                                outlineColourTag=False,
                                lineWidth=_outlinedTextLineWidth,
                            ))'''


                        _changeByWay.append(
                            '{\\textcolor{' + _colourTags[change[n].semitonesFromOne()]+'}{' + str(_notesByWay[n]) + '}}'

                        )
                        #input(_changeByWay[-1])
                # _changeByWay = change.straightenDegrees(Change.allowedNoteNamesSuperset + Change.allowedNoteNamesWeird)
                # _changeByWay = ['\\raisebox{-\\height/4}{%\n\\begin{tikzpicture}\\draw (0, 0)[use as bounding box] node[inner sep=0] {\\includegraphics[width=1.1em,clip,trim=left bottom right top]{'
                # +_diagramPaths[n]+'}};\n\\draw (0, 0)[use as bounding box] node {'+ str(_changeByWay[n]) +'};\end{tikzpicture}}'
                # for n in range(len(change)) ]
                # input(_changeByWay[0])
            elif way == "Change Number":
                _changeByWay = change.getChangeNumber(
                    decorateWithSmallCircle='Graphics Banner' not in ways,
                    externalGraphicsPath=externalGraphicsPath,
                    imgTag="bigimg", diagramType = 'SCircle'
                )
                '''_changeByWay = Latex.outlineText(
                    text=_changeByWay,
                    colourTag=_paperColourTag,
                    outlineColourTag=_inkColourTag,
                    lineWidth=_outlinedTextLineWidth,
                )'''

            elif way == "Scale Name":
                _changeByWay = change.getScaleNames(
                    defaultWay="Word",
                    replaceCarnaticNamesWithSymbols=False,
                    replaceDirectionStrWithUnicode=False,
                )
                if type(_changeByWay) == list:
                    _changeByWay = _changeByWay[0]
                
                #print(_changeByWay)
                _changeByWay = "\\bfseries{" + _changeByWay + '}'
                '''_changeByWay = Latex.outlineText(
                    text= + _changeByWay,
                    colourTag=_paperColourTag,
                    outlineColourTag=_inkColourTag,
                    lineWidth=_outlinedTextLineWidth,
                )'''
            elif way == "Chord Quality":
                _changeByWay = '\\mbox{'+change.getChordQuality(
                    useHalfDiminishedUnicodeSymbols=False,
                    useHalfDiminishedChords=False,
                    rootKey=rootKey,
                    makeTextMulticoloured=useColour,
                    outlineColourTag=_paperColourTag
                ) +'}'
                """_changeByWay = Latex.outlineText(text=_changeByWay,
                                                 colourTag=_paperColourTag,
                                                 outlineColourTag=_inkColourTag,
                                                 lineWidth=_outlinedTextLineWidth)"""
                """if useColour:
                    _changeByWay = Latex.makeTextMulticoloured(text=_changeByWay,
                                                     colourTags=[i for i in _colourTags if i in change.byWays(rootKey)],
                                                     outlineColourTag=_inkColourTag,
                                                     lineWidth=_outlinedTextLineWidth)"""
                # input('BEGIN\n{}\nEND'.format(_changeByWay))
            elif way == "Mode Family":
                assert Book.makePrimes, "has to be on"
                
                modes = []
                # SEecond part removes dupes
                __modesWeDid = []
                #input('asdfasdfasdfasdf\n{}'.format(_titleStr))
                for n in range(0,max(len(change),1)):
                    if len(change) == 0:
                        mode = change #Receptive Receptivity
                    else:
                        mode = change.mode(n).straightenDegrees()
                    if mode in __modesWeDid:
                        continue
                    __modesWeDid.append(mode)
                    modes.append([])
                    mode = mode.straightenDegrees(allowedNotes=Change.allowedNoteNamesSuperset)
                    for noteIdx,note in enumerate(mode):
                        #assert len(str(note)) <= 2, 'this note will not work because it has more than 2 length: {}'.format(note)
                        #modes[-1] += (note.makeResultColoured(str(note)[0]) if len(str(note)) > 1 else ' \\hspace{.05ex} ') + ' & ' + (('\\hfil '+note.makeResultColoured(str(note)[1])) if len(str(note)) > 1 else note.makeResultColoured(str(note)[0]))

                        modes[-1].append(note.makeResultColoured('{\\jazz '+str(note)+'}'))


                    modes[-1] = ' & '.join(modes[-1])

                    _noteSpacing = '1em'
                    if len(modes[-1]) > 0:
                        

                        modes[-1] = '\\renewcommand{\\arraystretch}{.7}\\setlength\\tabcolsep{0.0em}\\noindent\\begin{tabular}{'+('>{\\centering}'+'p{'+_noteSpacing+'}')*len(mode)+'}'+modes[-1]+'\\end{tabular}'

                        if len(change) == 12:
                            _noteSpacing = '1.1em'
                            modes[-1] = '{\\large'+modes[-1]+'}'
                            #_noteSpacing = '.75em'
                        elif len(modes[-1]) == 11:
                            _noteSpacing = '1.1em'
                            modes[-1] = '{\\large'+modes[-1]+'}'
                            #_noteSpacing = '.87em'

                        else:
                            pass
                            #_noteSpacing = '1em'
                        mode:Change
                        _melaData = ((' \\hspace{1ex}{\\large'+Book.unicodeChars["Mela"]+mode.getMelaNumber()+'}') if mode.getMelaNumber() else '')
                        modes[-1] = '{\\changenumber '+str(mode.getChangeNumber()) + '} \\tabto{1.4cm}' + modes[-1] + _melaData
                        #modes[-1] = Change.infoWaySymbols['Primeness'] + mode.byWays('Primeness') + ' ' + modes[-1]
                    _instrumentDiagram = '\\raisebox{-1.15\\baselineskip}{\\includegraphics[height=1.9\\baselineskip,keepaspectratio,]{'+Graphics.getDiagramPath(mode,rootKey,'Piano',greyScale=not useColour) +'}}'
                    #input('\n{} {}[{}] == {}'.format(
                    #    Key(rootKey,change.notes[n]),change.notes,n,change.notes[n],))
                    if len(change) == 0:
                        _instrumentDiagram2 = _instrumentDiagram
                    else:
                        _instrumentDiagram2 = '\\raisebox{-1.15\\baselineskip}{\\includegraphics[height=1.9\\baselineskip,keepaspectratio,]{'+Graphics.getDiagramPath(mode,(Key(rootKey,change.notes[n])).inAllFlats().note,'Piano',greyScale=not useColour) +'}}'
                    _circleDiagram = '\\raisebox{-1.15\\baselineskip}{\\includegraphics[width = 1.9\\baselineskip,keepaspectratio,]{'+Graphics.getDiagramPath(mode,rootKey,'PCircle',greyScale=not useColour,resolution=64) +'}}'

                    _scaleNameDefaultWay = 'Hexagram Name'
                    _scaleNameFont = FontMap.fontByWay["Scale Name"]["latexName"]
                    if False and mode.getScaleNames(defaultWay='Hexagram Name',)[0] == mode.getHexagramName():
                        _scaleNameFont = FontMap.fontByWay["Hexagram"]["latexName"]
                    
                    _scaleName =mode.getScaleNames(replaceCarnaticNamesWithSymbols=False,replaceDirectionStrWithUnicode=False)[0]
                    _font = ImageFont.truetype("Symbola.ttf", 14)
                    _scaleNameWidth = _font.getsize(_scaleName)[0]
                    #input('{} {}'.format(_scaleName,))
                    _scaleName = '{\\' + _scaleNameFont + ' ' + _scaleName + '}'

                    if _scaleNameWidth >= _font.getsize('Thundering Nourishment')[0]:
                        _scaleName = '{\\fontsize{12.5pt}{15pt}\selectfont ' + _scaleName + '}'

                    elif _scaleNameWidth >= _font.getsize('Raga Suddha Simant')[0]:
                        #second param should be 20% more than first https://latex-tutorial.com/changing-font-size/
                        #input((_scaleName + '\n')*20)
                        #input('ghgfghgfhgfhfghgfh')
                        _scaleName = '{\\fontsize{13pt}{15.6pt}\selectfont '+_scaleName+'}'
                    else:
                        pass#input(_scaleName+' < Revolving Nourishment.',)
                    _scaleName = Change.infoWaySymbols['Primeness'] + str(mode.byWays('Primeness')) + ' \\tabto{4.35ex}' + _scaleName
                    
                    modes[-1] = '\\renewcommand{\\arraystretch}{.7}\\setlength\\tabcolsep{0.0em}\\begin{tabular}{p{2.5cm} p{1.2cm} p{6.5cm} p{2.4cm}}'+_instrumentDiagram+' & '+_circleDiagram+' & '+ _scaleName +'\\newline '+modes[-1]+ ' & '+_instrumentDiagram2+'\\end{tabular}%\n'
                    #modes.append(' & '.join([note.makeResultColoured(str(char)) + ' & ' for note in mode for char in str((note)) ]))
                    #modes.append(str(['{\\jazz '+note.makeResultColoured(str(note))+ '} & ' for note in change.mode(n).straightenDegrees()])  + ' & ' + 'thing' )
                    #modes.append(str(['{\\jazz '+note.makeResultColoured(str(note))+ '} & ' for note in change.mode(n).straightenDegrees()])  + ' & ' + 'thing' )
                #_pageStr += '\\setlength\\tabcolsep{0.0em}\\noindent\\begin{tabular}{'+'>{\\centering}p{1em} ' * len(mode) +'}'
                #_pageStr += '\\setlength\\tabcolsep{0.0em}\\noindent\\begin{tabularx}{\\textwidth}{'+'c ' * len(mode) +'}'

                _pageStr += '\\\\\n'.join(modes)
                #_pageStr += '\\end{tabularx}'
                #_pageStr += '\\\\\n'.join(modes)

            elif "Distinct Chord Piano" in way:
                # add mbox{} around results if not later tabulising
                # _changeByWay = change.byWays(way)
                _numPartOfDistinctChord = int(way[-1])
                _numPartOfDistinctChord -= 1
                _changeByWay = [
                    change.getDistinctScaleChord(
                        n,
                        _numPartOfDistinctChord,
                        removeChordsWithOneLessLength=False,
                        includeModesForDiads=True,
                        returnChordQuality=False,
                        rootKey=rootKey,
                    )
                    for n in range(len(change))
                ]
                _changeByWay = [Latex.insertSmallDiagram(
                    c,change.byWays(rootKey)[cIdx],'Piano',filetype='pdf',imgtag='bigpianoimg',includeGraphicsPath=True) for cIdx,c in enumerate(_changeByWay)]

                #_changeByWay = [r'\tcblower ']+_changeByWay

                #input('here we is {}'.format(_changeByWay))

            elif "Distinct Chord" in way:

                # add mbox{} around results if not later tabulising
                # _changeByWay = change.byWays(way)
                _numPartOfDistinctChord = int(way[-1])
                _numPartOfDistinctChord -= 1
                _changeByWay = [
                    change.getDistinctScaleChord(
                        n,
                        _numPartOfDistinctChord,
                        removeChordsWithOneLessLength=False,
                        includeModesForDiads=True,
                        useHalfDiminishedChords=False,
                        makeTextMulticoloured=useColour,
                        rootKey=rootKey,
                    )
                    for n in range(len(change))
                ]

                # change.romanNumerals(True,)[n]
                if useCircleBeforeScaleChords:
                    #input('asdfasdfasdf')
                    _changeByWay = [
                        "\\mbox{"
                        + Latex.insertSmallDiagram(
                            change=change.getDistinctScaleChord(
                                n,
                                _numPartOfDistinctChord,
                                removeChordsWithOneLessLength=False,
                                includeModesForDiads=True,
                                useHalfDiminishedChords=False,
                                returnChordQuality=False,
                                normaliseResult=False,
                            ),
                            key=rootKey,
                            diagramType="Piano",
                            filetype="pdf",
                            externalGraphicsPath=externalGraphicsPath,
                            imgtag="pianoimg",
                        )
                        + "{\\bfseries\\jazzA "
                        + Latex.outlineText(
                            text=change.byWays("Jazz")[n],
                            colourTag=_colourTags[change[n].semitonesFromOne()],
                            lineWidth=_outlinedTextLineWidth,
                        )
                        + "}"
                        + "\\hspace{0.25ex}"
                        + "{\\jazzA "
                        + note.replace("°", "dim")
                        + "}"
                        + "}"
                        + Latex.insertSmallDiagram(
                            change=change.getDistinctScaleChord(
                                n,
                                _numPartOfDistinctChord,
                                removeChordsWithOneLessLength=False,
                                includeModesForDiads=True,
                                useHalfDiminishedChords=False,
                                returnChordQuality=False,
                                normaliseResult=True,
                            ),
                            key=Key(rootKey).onJazz(change[n]),
                            externalGraphicsPath=externalGraphicsPath,
                            diagramType="PCircle",
                            filetype="pdf",
                            imgtag="bigimg",
                        )
                        + "\\hfill "
                        for n, note in enumerate(_changeByWay)
                    ]
                else:  # useScaleChordsForGraphics==False

                    '''_changeByWay = [
                        "\\mbox{{\\jazzA "
                        + Latex.outlineText(
                            text=change.byWays("Jazz")[n],
                            colourTag=_colourTags[change[n].semitonesFromOne()],
                            lineWidth=_outlinedTextLineWidth,
                        )
                        + "}"
                        + "\\hspace{0.25ex}"
                        + "{\\jazzA "
                        + note.replace("°", "dim")
                        + "}}"
                        for n, note in enumerate(_changeByWay)
                    ]'''
                    '''_changeByWay = ['{\\jazz\\setlength\\tabcolsep{0pt}\\noindent '+Latex.makeTabular([[
                        '\\noindent ' + Latex.outlineText(
                            text=change.byWays("Jazz")[n],
                            colourTag=_colourTags[change[n].semitonesFromOne()],
                            lineWidth=_outlinedTextLineWidth,
                        ), note.replace("°", "dim"),

                    ]],
                        enclosingVerticalLines=False, enclosingHorizontalLines=False,
                    ) +'}' for n, note in enumerate(_changeByWay)]'''
                    _changeByWay = ['{\\jazz\\setlength\\tabcolsep{0pt}\\noindent\\begin{tabular}{p{0.9em} l}' +
                        #'\\hfil ' + Latex.outlineText( #CENTERED
                        '\\noindent ' + Latex.outlineText( #LEFT ALIGNED
                            text=change.byWays("Jazz")[n],
                            colourTag=_colourTags[change[n].semitonesFromOne()],
                            lineWidth=_outlinedTextLineWidth,
                        ) + ' & ' + note.replace("°", "dim")


                    + '\\end{tabular}}' for n, note in enumerate(_changeByWay)]
                    #input(_changeByWay)
                    # input(_changeByWay[0])
                    # input(_changeByWay)
                # _changeByWay = [change.byWays('Classical')[n] + ' ' + note for n, note in enumerate(_changeByWay)]

            elif way in (Book.titleWays + Book.moreTitleWays):
                #assert way != 'C'
                if showDebug and True or changeIdx == 0:
                    print("titleway is valid for", way)
                global theBook
                _changeByWay += Book.theBook.getTitle(change, [way],)
                # if way == 'Line Break': _changeByWay += '\\noindent '
            elif Change.isValidWay(way) or JazzNote.isValidWay(way):
                #assert way != 'C'
                
                    #print("change is valid for", way)
                # input(change.byWays('Word'))

                _changeByWay:Change = change.straightenDegrees()
                _changeByWay = _changeByWay.byWays([way])
                if type(_changeByWay) == Change and len(_changeByWay) > 0:
                    _changeByWay = Latex.makeDataColoured(_changeByWay,colours=[(i + Key(rootKey).distanceFromC()) % 12 for i in change.getSemitones()])
                else:
                    print('skipping the colouration of {} in way {}'.format(_changeByWay,way))
            elif "Tab To" in way:
                _changeByWay = Latex.tabTo(way)
            elif way in ("\\hfill", "\\hfill "):
                _changeByWay = "\\hfill "
            else:
                raise ValueError("Didn't find way: '{}'".format(way))
                _changeByWay += self.printToText([c], ways=[way])
                if showDebug:
                    print(_changeByWay)
            ##################### Tabulising #########################

            if 'Distinct Chord' in way:
                pass
                if tabuliseChordWays:
                    _resultMatrix = []
                    if tabuliseBySemitonePosition:
                        _st = change.getSemitones()
                        _scaleDegree = 0
                        for n in range(12):
                            if n % cols == 0:
                                _resultMatrix.append([])
                            if n in _st:
                                _resultMatrix[-1].append(_changeByWay[_scaleDegree])
                                _scaleDegree += 1
                            else:
                                # _resultMatrix[-1].append('╏ \hspace{0.7em}') # ╎╎
                                _resultMatrix[-1].append(
                                    "\\mbox{"
                                    + Latex.outlineText(
                                        text="╏ \\hspace{0.7em}",
                                        lineWidth=_outlinedTextLineWidth,
                                        colourTag=_paperColourTag,
                                        strokeColourTag=_inkColourTag,
                                    )
                                    + "}"
                                )  # ╎╎ ╏
    
                    else:
    
                        for n, note in enumerate(_changeByWay):
                            if n % cols == 0:
                                _resultMatrix.append([])
                            _resultMatrix[-1].append(note)
                            # http://www.fontineed.com/font/JazzText_Regular
                    # input(_changeByWay)
                    #input('before: {} way {}'.format(_changeByWay,way))
                    _changeByWay = Latex.makeTabular(
                        _resultMatrix,
                        tableCaption=None,
                        enclosingHorizontalLines=False,
                        enclosingVerticalLines=False,
                        fillHorSpaceWithTabularX=True,#True if ("Distinct Chord Piano" in way) else False,
                        useHorizontalLines=False,
                        useVerticalLines=False,
                        centreResults=False,
                    )
                    #input('after: {}'.format(_changeByWay))
                else:  # not using tabulisation
                    #input('before: {} {}'.format(_changeByWay,way))
                    _changeByWay = [i + '\\hfill ' for i in _changeByWay]
                    #input('after: {}'.format(_changeByWay))
                # input(_changeByWay)



            #################Adding FONTS###############

            if type(_changeByWay) == list:
                _changeByWay = " ".join(_changeByWay)

            if way in ("Chord Quality"):
                _changeByWay = (
                    "{\\"
                    + FontMap.fontFamilies["jazzA"]["latexName"]
                    + " "
                    + str(_changeByWay).replace("°", "dim")
                    + "}"
                )
            if way in ("Jazz",):
                _changeByWay = (
                    "{\\"
                    + FontMap.fontFamilies["jazzA"]["latexName"]
                    + " "
                    + str(_changeByWay).replace("°", "dim")
                    + "}"
                )

            if way in ("Word",):
                _changeByWay = (
                    "{\\"
                    + FontMap.fontByWay["Word"]["latexName"]
                    + " "
                    + _changeByWay
                    + "}"
                )
            if way == "Scale Name":
                _changeByWay = (
                    "{\\"
                    + FontMap.fontByWay["Scale Name"]["latexName"]
                    + " "
                    + _changeByWay
                    + "}"
                )
                # Substitute blank box if scale is unnamed
                if not change.hasScaleName():
                    """input('scale name {} == defualt way {}'.format(
                        _changeByWay,change.getWord()
                    ))"""
                    #_changeByWay = "\\nameBox{\\hspace{3cm}}"
                    _changeByWay = Latex.insertSmallDiagram(change,rootKey,diagramType='Piano',filetype='pdf',includeGraphicsPath=True,imgtag='pianoimg')
                # _changeByWay = '{\\bfseries ' + _changeByWay + '}'
            if way == "Change Number":
                _changeByWay = (
                    "{\\"
                    + FontMap.fontByWay["Change Number"]["latexName"]
                    + " "
                    + str(_changeByWay)
                    + "}"
                )
                """if '-' in _changeByWay:
                    # _changeByWay = '{\\testA ' + _changeByWay.replace(str(c),str(c)) + '}'
                    # Set the font only after the '-'
                    _changeByWay = _changeByWay[:-len(str(c))] + '{\\' + FontMap.fontByWay['Change Number'][
                        'latexName'] + ' -}' + '{\\' + FontMap.fontByWay['Change Number'][
                                       'latexName'] + ' ' + str(c).replace('-', '') + '}"""

                # _changeByWay = '{\\testA ' +_changeByWay.replace('}{\\testF -}{\\testA ','') + '}'

                pass
                """else:
                    _changeByWay = '{\\'  +FontMap.fontByWay['Change Number'][
                                       'latexName']+' ' + _changeByWay + '}"""




            #elif w == 0 or Book.condensedWays[w - 1] == "Line Break":
            #    pass  # _pageStr += '\\noindent'
            if (
                _pageStr.count(_lineBreak) + _titleStr.count(_lineBreak)
            ) < linesInTitle:
                # input('line breaks: {}'.format(_pageStr.count(_lineBreak)))

                # print(_changeByWay)
                _titleStr += str(_changeByWay)
            else:

                _pageStr += _changeByWay
                # input('happengin {} happening'.format(_pageStr))

            if (
                w != len(ways) - 1
                and ways[w + 1] != "Line Break"
                and way != "Line Break"
                and 'Distinct Chord' not in way
            ):
                # ways[min(0,w - 1)] != 'Line Break':

                _pageStr += strBetweenWays

            # input('BEWGIN BLA\n\n\n {} \n way = {} '.format(_titleStr,way))
        
        #Smoosh everything together in the title for Mode Family
        if chordsOfChangeType == 'Mode Family':
            #input('Here she goes\n"{}"\n\n"{}"\nThere she went'.format(_subtitleStr,_titleStr))
            _titleStr = _titleStr.replace('\\hfill','')
            #Make all seps hfill
            _titleStr = _titleStr.replace(' ','\\hfill ')
            #_titleStr = _titleStr.replace(' ','')
            _titleStr = '{\\large ' + _titleStr + '}'
        
        
        
        # input('subChange string\n{}\nendpagestring'.format(_pageStr))
        _fCirclePath = Graphics.getFCirclePath(
            change=change,
            colourKey="C",
            resolution=256,
            includeFilename=True,
            filetype="pdf",
            externalGraphicsPath=externalGraphicsPath,
        )
        # Put Transparent image behind
        _fCircleSize = 3
        if tabuliseBySemitonePosition:
            if includeBackgroundGraphic:
                if cols == 3:
                    _fCircleSize = 4.8
                elif cols == 4:
                    _fCircleSize = 4.2

                _fCircleStr = (
                    "\\tikz[remember picture,overlay] \\node[opacity=0.05,inner sep=0pt] at (15,1){\\includegraphics[width="
                    + str(_fCircleSize)
                    + "cm,height="
                    + str(_fCircleSize)
                    + "cm]{"
                    + _fCirclePath
                    + "}};"
                )
        #.338
        #_titleStr, _subtitleStr = _subtitleStr, _titleStr
        _pageStr = (
            "\\noindent\\begin{minipage}[s][\\linewidth]{\\linewidth}\\begin{tcolorbox}[title="
            + (_subtitleStr if not putGraphicsBannerInSubtitle else '') + _titleStr
            + ",grow to left by="+growToLeftBy+",grow to right by="+growToRightBy+"]%\n"
            + (_fCircleStr if includeBackgroundGraphic else "")
            + _pageStr#+'\\vspace{-\\baselineskip}%\n'  #Use <- if you're using the subtitel
            + ('\\tcbsubtitle[before skip=-0cm,after skip=0cm]{'+_subtitleStr+'}%\n' if putGraphicsBannerInSubtitle else '')
            + "\\end{tcolorbox}\\end{minipage}"
        )

        # input(_pageStr)
        # _pageStr = '\\noindent\\begin{minipage}{0.85\\linewidth}\\begin{tcolorbox}[title=My title,watermark graphics=Basilica_5.png,watermark opacity=0.25,watermark text app=Basilica,watermark color=Navy]sdfgsdfgsdfgsdfg}\\end{minipage}'
        # Put image beside table
        # _fCircleStr = '\\includegraphics[height=1.6cm,trim=0cm +3.8cm 0 -3.8cm]{' + _fCirclePath + '}'

        if includeBackgroundGraphic:
            pass  # _pageStr += _fCircleStr

        # Where the fuck did that ] come from!
        # _pageStr = _pageStr.replace(']\\tikz','\\tikz')
        # _pageStr = _pageStr.replace('\n]\\tikz','\n\\tikz')
        # raise ValueError('fuck it.')
        # _str += _pageStr + '\n'
        if makePdfBookmark:
            _str += _pdfBookmark
        
        #input('pageStr:\n"\n{}\n" \n_str\n"\n{}\n"'.format(_pageStr,_str))
        if includeBackgroundGraphic:
            _str += (
                "\\noindent\\begin{tabular}{c r}"
                + _pageStr
                + " & "
                + _fCircleStr
                + "\\end{tabular}"

            )
        else:
            _str += _pageStr
        #input(_pageStr)
        _str+='\\let\\heightofmulticolourtext\\relax % so there is no conflict with newlength\n'
        _str+='\\let\\lengthofmulticolourtext\\relax %\n'
        if False and debugOutput:
            input('and the result is\n{}\nwhich has been the result'.format('\n'.join([str(l + 1) + ': ' + line for l,line in enumerate(_str.split('\n'))])))
        #input(_str)
        return _str

    @classmethod
    def renderCondensedChange(
        cls,
        change: Change,
        strBetweenWays=None,
        linesInTitle=2,
        cols=4,
        tabuliseBySemitonePosition=False,
        showDebug=True,
        rootKey="C",
        externalGraphicsPath=True,
        useCircleBehindJazzNotes=False,
        useCircleBehindWayOfWord=False,
        useCircleBeforeScaleChords=False,
        useCircleBehindHexagram=False,
        invertColour=False,
        useColour=True,
        includeLatexColorboxSettings=True,
        makePdfBookmark=False,
        openFileWhenDone=True,
        core=0,
        cores=1,
        skipIfFileExists=False,
        chordsOfChangeType=None
    ):

        print(('inside Project.renderCondensedChange(). doing change ' + str(change) + '\n') * 20)
        _outputDirectory = Graphics.getChordsOfChangePath(
            change=change,
            tabuliseBySemitonePosition=tabuliseBySemitonePosition,
            rootKey=rootKey,
            externalGraphicsPath=externalGraphicsPath,
            invertColour=invertColour,
            useColour=useColour,
            includeDirectory=True,
            includeFilename=False,
            chordsOfChangeType=chordsOfChangeType
        )
        _outputFilename = Graphics.getChordsOfChangePath(
            change=change,
            tabuliseBySemitonePosition=tabuliseBySemitonePosition,
            rootKey=rootKey,
            externalGraphicsPath=externalGraphicsPath,
            invertColour=invertColour,
            useColour=useColour,
            includeDirectory=False,
            includeFilename=True,
            chordsOfChangeType=chordsOfChangeType
        )
        if skipIfFileExists and os.path.isfile(
            os.path.join(_outputDirectory, _outputFilename)
        ):
            print(
                "skipping ",
                os.path.join(_outputDirectory, _outputFilename, "as it exists."),
            )
            return os.path.join(_outputDirectory, _outputFilename)
        else:
            print(
                "renderCondensedChange() making ",
                os.path.join(_outputDirectory, _outputFilename),
            )
        lcl = locals()
        # lcl.pop('cl')
        print("lcl.keys()", lcl.keys())
        params = {}
        for i in lcl.keys():
            if (
                i
                not in tuple(
                    Utility.getParameters(cls.makeCondensedChangeTex)[1].keys()
                )
                + Utility.getParameters(cls.makeCondensedChangeTex)[0]
            ):
                pass
            else:
                params[i] = lcl[i]
        
        _str = cls.makeCondensedChangeTex(**params)
        #input("_str == \n''{}\n''\nend of code for that change".format(_str))
        _texFilename = "ChordsOfChangeSingle.tex"
        _containerPath = "ChordsOfChangeContainer.tex"

        if cores > 1:

            _texCloneFilename = "ChordsOfChangeSingleCPUCore" + str(core) + ".tex"
            shutil.copy(
                _containerPath, "ChordsOfChangeContainerCPUCore" + str(core) + ".tex"
            )
            _containerPath = "ChordsOfChangeContainerCPUCore" + str(core) + ".tex"
            Utility.saveToFile(_str, os.path.join("tex", _texCloneFilename))
            #I don't get why you replace the text
            #Utility.replaceTextInFile(_containerPath, _texFilename, _texCloneFilename)
        else:
            Utility.saveToFile(_str, os.path.join("tex", _texFilename))

        # _str = Latex.wrapChangeDataWithPreambleEtc(_str,'ChordsOfChange')

        _texDirectory = ""
        _texPath = os.path.join(_texDirectory, _texFilename)

        Project.makeDirectory(_texDirectory)

        Utility.saveToFile(_str, os.path.join('tex',_texDirectory, _texFilename))

        # input('endddddd path {}'.format(_texPath))
        # print('{}\nWrote Chords Of Change file {}'.format(_texFilename,_str))
        print(
            "rendering chords of change pdf from single change #{}\n into the file {}".format(
                change.getChangeNumber(),
                os.path.join('tex',_texDirectory, _texFilename)
            )
        )
        #input('stop container path: {}'.format(_containerPath))
        Latex.buildFile(
            filepath=_containerPath,
            openFileWhenDone=openFileWhenDone,
            # options=['--shell-escape -output-directory={}'.format(_outputDirectory.replace('\\','/'))],
            options=["--shell-escape"],
            args=[],
            iterations=1,
        )
        
        print("built file {}".format(_containerPath))
        print('cropping file')                                        #left,   bottom, right,   top offset values,
        _cropSuccess = False
        while not _cropSuccess:
            try:
                #crop([_containerPath.replace('.tex','.pdf'),'-mo','-p 0','-a4','+.05','-.4','-.2','-0.015'])
                #crop([_containerPath.replace('.tex','.pdf'),'-mo','-p 0','-a4','+.00','+0.015','-4.1','-0.015'])
                crop([_containerPath.replace('.tex','.pdf'),'-mo','-p 0','-a4','+.00','-0.2','-4.1','-0.015'])
                # L B R T
                _cropSuccess = True
            except PermissionError as e:
                input('Was trying to crop but file is use. Try again?\n{}'.format(e))

        Utility.makeDirectory(_outputDirectory)
        print(
            "Copied file to {} then renamed it to {}".format(
                _outputDirectory, _outputFilename
            )
        )

        shutil.copy(
            _containerPath.replace(".tex", "") + ".pdf",
            _outputDirectory,
        )
        print(
            os.path.join(_outputDirectory, _containerPath.replace(".tex", "") + ".pdf"),
            _outputFilename,
        )

        # input(os.path.join(_outputDirectory,_outputFilename))
        if os.path.exists(os.path.join(_outputDirectory, _outputFilename)):
            os.remove(os.path.join(_outputDirectory, _outputFilename))
        print("removed file:///"+os.path.join(_outputDirectory, _outputFilename).replace('\\','/'))
        os.rename(
            os.path.join(_outputDirectory, _containerPath.replace(".tex", "") + ".pdf"),
            os.path.join(_outputDirectory, _outputFilename),
        )
        print(
            "renamed",
            os.path.join(_outputDirectory, _containerPath.replace(".tex", "") + ".pdf"),
        )

    @classmethod
    def makeChordsOfChangeBook(
        self,
        changes: list,
       
        strBetweenWays=None,
        linesInTitle=2,
        cols=3,
        diagramWidth = .75,
        useChaptersForChangeLength=True,
        tabuliseBySemitonePosition=True,
        showDebug=True,
        padVertSpaceBetweenChanges=True,
        rootKey="C",
        externalGraphicsPath=True,
        useCircleBehindJazzNotes=False,
        useCircleBehindWayOfWord=False,
        useCircleBeforeScaleChords=False,
        useCircleBehindHexagram=False,
        invertColour=False,
        useColour=True,
        usePDFBookmarks=True,
        filepath="condensedWOC.tex",
        includeGraphicsPath=False,
        iterations=2,
        fastMode=True
    ):
        if changes == None: changes = range(2049)
        #Switch this to make it slow. slow mening = good
        if fastMode:
            _allDistinctScaleChords = []
        else:
            _allDistinctScaleChords = book.getAllDistinctScaleChords()

        _filename = "condensedChanges"
        # _volStr = 'pt2of2'
        _volStr = "all"
        _filepath = os.path.join(Project.directoryTex, _filename , _volStr + ".tex")
        print("calling Project.makeChordsOfChangeBook({})".format(locals()))
        if useCircleBehindWayOfWord:
            raise ValueError("this will probably fuck up at change -1361")

        _lineBreak = "\\\\\n"
        _str = ""
        # print('going through changes....', changes)
        if useChaptersForChangeLength == None:
            useChaptersForChangeLength = sorted(list(changes)) == list(changes)
        if padVertSpaceBetweenChanges:
            _fillBetweenChanges = "\\vfill"
        else:
            _fillBetweenChanges = ""
        _pastChangeLength = -1
        _colours = Colour.getTransposedColours(
            colourTranspose=JazzNote.distanceFromC(rootKey)
        )
        _colourTags = Colour.getTransposedColourTags(
            colourTranspose=JazzNote.distanceFromC(rootKey), neutralColours=True
        )
        _outlinedTextLineWidth = 0.5
        if invertColour:
            _inkColourTag = "white"
            _paperColourTag = "black"
        else:
            _inkColourTag = "black"
            _paperColourTag = "white"

        for changeIdx, change in enumerate(changes):

            if change == 0:
                continue
            _changeLengthData = ""
            _pageStr = ""
            _titleStr = ""
            if type(change) == Change:
                c = change.getChangeNumber()
            else:
                c = change
                change = Change.makeFromChangeNumber(c)
            # Now type(c) == int and type(change) == Change
            if (len(change) != _pastChangeLength) and useChaptersForChangeLength:
                if c < 0:
                    _numOfNotesStr = "-" + str(len(change))
                else:
                    _numOfNotesStr = str(len(change))
                _sectionNameStr = (
                    Book.chapterHeadings[len(change)]
                )
                #_changeLengthData += "\\clearpage\\section*{" + _sectionNameStr + "}"
                _changeLengthData += "\\clearpage\\section{" + _sectionNameStr + "}"
                #https://tex.stackexchange.com/questions/101538/addcontentsline-lines-added-to-toc-not-numbered-and-lines-added-to-tot-not-sh
                '''_changeLengthData += (
                    "\\addtocounter{section}{1}"
                    "\\addcontentsline{toc}{section}{\\protect\\numberline{\\thesection} "+_sectionNameStr+"}"
                    #"\addcontentsline{toc}{subsubsection}{\protect\numberline{\thesubsubsection} line added to TOC: subsubsection one}"
                )'''
                if usePDFBookmarks:
                    _changeLengthData += '\\clearpage\\subsection{Mode Families}'
                _changeLengthData += Book.theBook.displayChapterInfo(change)

                # _changeLengthDescriptor = str(len(change)) + ' notes'
                # _str += '\\pdfbookmark[section]{' + _changeLengthDescriptor + '}{toc}'
                # _changeLengthData = '\\section*{Introduction}\\label{sec:intro}\\addcontentsline{toc}{section}{\\nameref{sec:intro}}' + _str + '}'
                # _changeLengthData = '\\section*{'+Book.chapterHeadings[len(change)]+'} \n'
            _pastChangeLength = len(change)
            #if c in Book.changesForBeginners:
            if c in _allDistinctScaleChords:
                # _featuredChangeStr = '\\addcontentsline{toc}{subsection}{' + self.getTitle(change,['Book Page','Scale Name','Chord Quality'])+'}'#
                _featuredChangeStr = Book.theBook.addPageToTableOfContents(
                    change=change,
                    captionType="subsection",
                    ways=Book.condensedTableOfContentsWays,
                    replaceSheetNumber=False,
                    externalGraphicsPath=externalGraphicsPath,
                    renderIfNotFound=True,
                )
                _pdfBookmark = ""
                print("featuredChange:", _featuredChangeStr)
            else:
                _featuredChangeStr = ""
                _pdfBookmark = change.makePdfLink()
                #input(_pdfBookmark)
            _str += _changeLengthData
            if _changeLengthData not in ('',None,False):
                _str += '\\clearpage\\subsection{Scale-Chords}'
            if usePDFBookmarks:
                _str += _pdfBookmark
            # _str += '\\noindent\\begin{tabular}{c r}' + _pageStr + ' & ' '\\end{tabular}' + _fillBetweenChanges + '\n'
            _str += '\\phantomsection\\protect\\label{cbw_'+str(change.getChangeNumber())+'}'

            _str += "\\noindent\\includegraphics[width="+str(diagramWidth)+"\\textwidth]{{{}}}".format(
                Graphics.getChordsOfChangePath(
                    change=change,
                    rootKey=rootKey,
                    tabuliseBySemitonePosition=tabuliseBySemitonePosition,
                    invertColour=invertColour,
                    useColour=useColour,
                    includeGraphicsPath=includeGraphicsPath,
                ).replace("\\", "/")
            )
            _str += _featuredChangeStr
            _str += _fillBetweenChanges + "\n"
            #input('this one:\n'+_str)
        _tex = open("condensedChanges.tex", "w+", encoding="UTF-8")
        _tex.write(_str)
        _tex.close()
        Latex.buildFile(filepath=filepath, iterations=iterations,convertToRaster=True)
        input("built the book. iterations == {}".format(iterations))
        return _str

    @classmethod
    def makeBigNamesList(cls):
        _str = ""
        _bigNamesList: dict = {}
        _relatedChanges: dict = {}
        print("started going through big names list")
        for c in tqdm(range(1, 2049)):
            change: Change = Change.makeFromChangeNumber(c)
            changeNames = []
            changeNames.append(change.getChordQuality())
            changeNames.append(" ".join(change.getHexagram(["name"])))
            for name in change.getScaleNames(
                replaceDirectionStrWithUnicode=False,
                replaceCarnaticNamesWithSymbols=False,
            ):
                changeNames.append(name)
            willSmithNames = change.getRelatedScaleNames()
            if willSmithNames: changeNames.extend(willSmithNames)

            for name in changeNames:
                
                _bigNamesList[name] = {
                    "definition": "\\hyperref[cbw_"+str(change.getChangeNumber())+"]{"+change.getChangeNumber(
                        decorateWithSmallCircle=True, externalGraphicsPath=True,
                    ) + '}',
                    "changeNumber": change.getChangeNumber(),
                }

            _relatedChanges[str(change.getChangeNumber())] = ", ".join(changeNames)
            _relatedChanges[str(change.getChangeNumber())]
        _bigNamesKeys = list(_bigNamesList.keys())
        _bigNamesKeys.sort(key=lambda v: v.upper())
        _lastLetterUsed = False
        for name in tqdm(_bigNamesKeys):
            nameData = _bigNamesList[name]["definition"]
            if name.isdigit():
                nameData = Utility.makeNumberCipheredIfPreceededBy(nameData, name, "_")
            nameData = nameData.replace(name, "")
            if name.isdigit():
                nameData = Utility.makeNumberUnciphered(nameData, name)
            # Include related changes
            # _str += nameData + ' '+ name + ': ' +_relatedChanges[str(_bigNamesList[name]['changeNumber'])] +'\n\n'
            if name and name[0].upper() != _lastLetterUsed:
                _str += (
                    "\\framebox[4em]{\\centering{\\Huge{"
                    + name[0].upper()
                    + "}}}{ }\n\n"
                )
                _lastLetterUsed = name[0].upper()
            _str += "\\noindent " + name + "\\hfill " + nameData + "\\hfill \n\n"

        Utility.saveToFile(_str, "tex\\bigNamesDictionary.tex")

        input("done making big names thingie")
        return _str

    @classmethod
    def renderChordsOfChangePrimeFamilyPdfs(
            cls,core,cores):
        theBook = Book.theBook
        if Book.makePrimes == False:
            pass#raise TypeError("Must be enabled to work")

        _primes = []
        for changeLen in range (0,13):
            for primeIdx, prime in enumerate(theBook.sequencePrimesByLength[changeLen]):
                _primes.append(prime)

        cls.renderChordsOfChangePdfs(changeRange=[p.getChangeNumber() for p in _primes], core=core,cores=cores,chordsOfChangeType='Mode Family')


    @classmethod
    def renderChordsOfChangePdfs(
        cls,
        changeRange: [int] = None,
        core: int = 0,
        cores: int = 1,
        skipIfFileExists=False,
        chordsOfChangeType=None,
    ):
        print("rendering chordsofchange")
        if changeRange == None:
            changeRange = list(range(1, 2049))
        print('change rnageee i\s',changeRange)
        print(
            "Project.renderChordsOfChangePdfs(changeRange:[int]={},core:int={},cores:int={}".format(
                changeRange, core, cores
            )
        )
        for c,changeNumber in enumerate(tqdm(changeRange[core::cores])):

            #input('here')
            print('beginning renderCondensedChange(changeNumber={})\n'.format(changeNumber) * 3)
            Project.renderCondensedChange(
                Change.makeFromChangeNumber(changeNumber),
                useColour=True,
                openFileWhenDone=False,
                core=core,
                cores=cores,
                skipIfFileExists=skipIfFileExists,
                chordsOfChangeType=chordsOfChangeType
            )
            print(("Finished change " + str(changeNumber) + "\n") * 20 + 'We are {}% done. {}/{}'.format(round(c/len(changeRange)),c,len(changeRange)))

    @classmethod
    def makeDirectory(cls, path):

        try:
            os.mkdir(path)
        except OSError:
            if os.path.isdir(path):
                print("Skipped making {} because it has already been created.")
            else:
                print(
                    "Creation of the directory {} failed for some reason.".format(path)
                )
        else:
            print("Successfully created the directory %s " % path)

    @classmethod
    def testScaleNames(cls, includeNegatives=False, includeHexagrams=False):
        _longestName = ""
        print(
            "testScaleNames(includeNegatives={}, includeHexagrams={})\n -> looking through changes to find longest name...".format(
                includeNegatives, includeHexagrams
            )
        )
        for change in theBook:
            if includeNegatives or change.getChangeNumber() > 0:
                if change.hasScaleName():
                    name = change.getScaleNames(
                        defaultWay="Hexagram Way" if includeHexagrams else False,
                        replaceDirectionStrWithUnicode=False,
                    )[0]
                if len(name) > len(_longestName):
                    _longestName = name
                    _longestChange = change
        input(
            "The longest name is #{}: {}: {} with a length of {}.".format(
                _longestChange.getChangeNumber(),
                _longestChange,
                _longestName,
                len(_longestName),
            )
        )