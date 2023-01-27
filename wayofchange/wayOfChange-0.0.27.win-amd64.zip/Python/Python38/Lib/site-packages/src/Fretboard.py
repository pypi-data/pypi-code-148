from __future__ import annotations, print_function

class Fretboard:
    height = 256
    lineWidth = round(height / 64)
    # marginSize measured in str space size
    marginSize = 0.5
    octaveWidthProportion = 2
    octaveWidth = height * 3.5

    
    lineColour = (0, 0, 0, 255)
    lineColourInvert = (255, 255, 255, 255)
    indicationColour = (255, 255, 255, 255)
    indicationColourInvert = (255, 255, 255, 255)
    indicationLineColour = (0, 0, 0, 255)  # (128,128,128,255)
    indicationLineColourInvert = (0, 0, 0, 255)  # (128,128,128,255)
    canvasBGColour = (255, 255, 255, 0)

    showFrets = 12
    # instruments default to Guitar values if not specified.
    instruments = {
        "Guitar": {
            "strNotes": ["E", "A", "D", "G", "B", "E"],
            "fretIndicators": (5, 7, 9, 15, 17, 19),
            "fretIndicatorsDouble": [12, 24],
            "showFrets": 24,
            "doubleDotsOffset": 9,
        },
        "DADGAD": {"strNotes": ["D", "A", "D", "G", "A", "D"]},
        "DADGBD": {"strNotes": ["D", "A", "D", "G", "B", "D"]},
        "Mando": {
            "strNotes": ["G", "D", "A", "E"],
            "fretIndicators": (5, 7, 10, 15, 17, 19),
            "fretIndicatorsDouble": [12],
        },
        "Uke": {
            "strNotes": ["G", "C", "E", "A"],
            "fretIndicators": (5, 7, 10, 12, 15),
            "fretIndicatorsDouble": [],
            "showFrets": 19,
        },
    }

    def __init__(self, instrument="Guitar", showFrets=None):
        # input('{} {}'.format(Fretboard.instruments.keys(),instrument))
        if instrument in Fretboard.instruments.keys():
            self.instrument = instrument
        else:
            raise KeyError(
                "you need to add this instrument: "
                + str(instrument)
                + ", to Fretboard.instruments"
            )
        if "strNotes" in Fretboard.instruments[instrument].keys():
            self.strNotes = Fretboard.instruments[instrument]["strNotes"]
        else:
            raise ValueError("you need to add strNotes to this instrument")
        for n in self.strNotes:
            if JazzNote.isAlphabetNoteStr(n):
                pass
            else:
                raise TypeError("strNotes expects notes in alphabet format Ab")

        if showFrets is None:
            if "showFrets" in Fretboard.instruments[instrument].keys():
                self.showFrets = Fretboard.instruments[instrument]["showFrets"]
            else:
                self.showFrets = Fretboard.instruments["Guitar"]["showFrets"]

        if "fretIndicators" in Fretboard.instruments[instrument].keys():
            self.fretIndicators = Fretboard.instruments[instrument]["fretIndicators"]
        else:
            self.fretIndicators = Fretboard.instruments["Guitar"]["fretIndicators"]

        if "fretIndicatorsDouble" in Fretboard.instruments[instrument].keys():
            self.fretIndicatorsDouble = Fretboard.instruments[instrument][
                "fretIndicatorsDouble"
            ]
        else:
            self.fretIndicators = Fretboard.instruments["Guitar"][
                "fretIndicatorsDouble"
            ]

        if "doubleDotsOffset" in Fretboard.instruments[instrument].keys():
            self.doubleDotsOffset = Fretboard.instruments[instrument][
                "doubleDotsOffset"
            ]
        else:
            self.doubleDotsOffset = Fretboard.instruments["Guitar"]["doubleDotsOffset"]

    def getFretboardPath(
        self,
        change: Change,
        key: str,
        greyScale=False,
        invertColour=False,
        returnName=True,
        returnDirectory=True,
        includeGraphicsPath=True,
        pathSeperator="/",
        resolution: int = None,
        fretBoardType: str = None,
        filetype: str = "png",
        externalGraphicsPath=False,
        includeExtension=True,
    ) -> str:
        key = JazzNote.noteNameFlats[JazzNote.distanceFromC(key)]
        if resolution is None:
            resolution = Fretboard.height
        _str = ""
        if returnDirectory:
            if includeGraphicsPath:
                # raise TypeError('includeGraphicsPath path should be false right now')
                if greyScale:
                    if not invertColour:
                        _str += Graphics.fretboardsBWDirectory
                    else:
                        _str += Graphics.fretboardsBWInvDirectory
                else:
                    if not invertColour:
                        _str += Graphics.fretboardsDirectory
                    else:
                        _str += Graphics.fretboardsInvDirectory
            else:
                _str += self.instrument + "/"

            if externalGraphicsPath:
                _str = _str.replace(Graphics.directory, Graphics.directoryExternal)

            _str += str(resolution) + "px_" + filetype + "/"
            _str += key + "/"

        if returnName:
            _str += "{}_{}".format(
                self.instrument,
                change.getChangeNumber(decorateChapter=False, addOneToBookPage=True),
            )
            if includeExtension:
                _str += "." + filetype
        _str = _str.replace("\\", pathSeperator)
        _str = _str.replace("/", pathSeperator)
        _str = _str.replace("Fretboard", self.instrument)

        return _str

    def renderFretboards(
        self,
        changes: [Change],
        keys: [str],
        greyScale,
        invertColour=False,
        indicateNotesWithFCircle=False,
        fretsAreEquidistant=False,
        connectFretboardLines=True,
        showImage=False,
        makeColourSchemes=True,
        makeNewIndicatorDiagrams=False,
        useRadiusLines = True,
        filetypes=["pdf"],
        resolution=64,
    ):
        color = pyx.color
        canvas = pyx.canvas
        trafo = pyx.trafo
        style = pyx.style
        path = pyx.path
        deco = pyx.deco
        _noteColours = Colour.getTransposedColours(neutralColours=True)
        # Each fret space is .94387 as wide as the previous fret space
        if type(keys) == list and all(
            [JazzNote.isAlphabetNoteStr(key) for key in keys]
        ):
            pass
        else:
            raise TypeError(
                "keys expects a list of alphabet keys. not {} with type == {}".format(
                    keys, type(keys)
                )
            )

        if fretsAreEquidistant:
            _fretWidths = [
                self.octaveWidth / self.showFrets for i in range(self.showFrets + 1)
            ]
            _firstFretWidth = _fretWidths[0]
        else:
            _firstFretWidth = (
                self.octaveWidth / self.showFrets
            ) * self.octaveWidthProportion ** (-6 / 12)
            _fretWidths = [
                _firstFretWidth * self.octaveWidthProportion ** ((12 - i) / 12)
                for i in range(self.showFrets + 1)
            ]
        _fretX = _fretWidths[0]
        _strVertSpace = self.height / (len(self.strNotes) + self.marginSize * 2 - 1)
        _marginSpace = _strVertSpace * self.marginSize
        _imWidth = sum(_fretWidths[:-1]) + _fretX + _marginSpace
        usingRaster = "png" in filetypes
        usingVector = any([i in Graphics.vectorFiletypes for i in filetypes])
        vectorFCircleResolution = FCircle.vectorSaveResolutions[0]
        _FCirclesMadePng = []
        print(
            "beginning renderFretboards() with these {} change(s) {}\n in the key(s): {}\nfretBoard.instrument: {}".format(
                len(changes),
                ", ".join([str(c.getChangeNumber()) for c in changes]),
                keys,
                self.instrument,
            )
        )
        for k in keys:
            assert JazzNote.isAlphabetNoteStr(k), "shit"
            _colourSchemes = []
            for g in (False, True):
                for i in (False, True):
                    if (i == invertColour and g == greyScale) or makeColourSchemes:
                        print("stats i: {} g: {}".format(i, g))
                        _colourSchemes.append(
                            {
                                "greyScale": g,
                                "invertedColours": i,
                                                            }
                        )
                        if indicateNotesWithFCircle:
                            #raise TypeError ('shit')
                            _colourSchemes[-1]["canvasFCircles"] = []
                            _colourSchemes[-1]["canvasFCirclesInverted"] = []
                            _fCircleFiletypes = [] if not usingRaster else ["png"]
                            _whichCache = ('canvasFCircles',
                            greyScale, invertColour, rootColourKey, resolutionresolution, _fCircleFiletypes)
                            try:
                                Fretboard.cache
                            except NameError:
                                Fretboard.cache = {}

                            try:
                                _colourSchemes[-1]["canvasFCircles"] = Fretboard.cache[_whichCache]
                            except NameError:
                                print("key is {}!!!".format(k))
                                for st in range(12):
                                    _colourSchemes[-1]["canvasFCircles"].append(
                                        Graphics.renderFCircle(
                                            change=Change.makeFromSet([st]),
                                            greyScale=g,
                                            invertColour=i,
                                            rootColourKey=k,
                                            resolution=vectorFCircleResolution,
                                            saveOnlyOneKey=True,
                                            returnAsPyXCanvas=True,
                                            filetypes= _fCircleFiletypes,
                                        )
                                    )
                                    _colourSchemes[-1]["canvasFCirclesInverted"].append(
                                        Graphics.renderFCircle(
                                            change=Change.makeFromSet([st]),
                                            greyScale=g,
                                            invertColour=not i,
                                            rootColourKey=k,
                                            resolution=vectorFCircleResolution,
                                            saveOnlyOneKey=True,
                                            returnAsPyXCanvas=True,
                                            filetypes=_fCircleFiletypes,
                                        )
                                    )
                                    # print('come here again',len(_colourSchemes[-1]['canvasFCirclesInverted'][-1]))
                                    # input(str(_colourSchemes[-1]['canvasFCirclesInverted'][-1].bbox()))
                                Fretboard.cache[_whichCache] = _colourSchemes[-1]["canvasFCircles"]
                        if i == False:
                            _colourSchemes[-1]["lineColour"] = pyx.color.rgb(
                                Fretboard.lineColour[0] / 255,
                                Fretboard.lineColour[1] / 255,
                                Fretboard.lineColour[2] / 255,
                            )
                            _colourSchemes[-1]["indicationLineColour"] = pyx.color.rgb(
                                Fretboard.indicationLineColour[0] / 255,
                                Fretboard.indicationLineColour[1] / 255,
                                Fretboard.indicationLineColour[2] / 255,
                            )
                            _colourSchemes[-1]["indicationColour"] = pyx.color.rgb(
                                Fretboard.indicationColour[0] / 255,
                                Fretboard.indicationColour[1] / 255,
                                Fretboard.indicationColour[2] / 255,
                            )
                        else:
                            _colourSchemes[-1]["lineColour"] = pyx.color.rgb(
                                Fretboard.lineColourInvert[0] / 255,
                                Fretboard.lineColourInvert[1] / 255,
                                Fretboard.lineColourInvert[2] / 255,
                            )
                            _colourSchemes[-1]["indicationLineColour"] = pyx.color.rgb(
                                Fretboard.indicationLineColourInvert[0] / 255,
                                Fretboard.indicationLineColourInvert[1] / 255,
                                Fretboard.indicationLineColourInvert[2] / 255,
                            )
                            _colourSchemes[-1]["indicationColour"] = pyx.color.rgb(
                                Fretboard.indicationColourInvert[0] / 255,
                                Fretboard.indicationColourInvert[1] / 255,
                                Fretboard.indicationColourInvert[2] / 255,
                            )

            for change in changes:
                _fretX = _fretWidths[0]
                for col in range(len(_colourSchemes)):
                    _colourSchemes[col]["canvas"] = canvas.canvas()

                _noteNames = [
                    JazzNote.noteNameFlats[(i + JazzNote.distanceFromC(k)) % 12]
                    for i in change.getSemitones()
                ]
                _outerFretboardBounds = {}
                if usingRaster:
                    _im = Image.new(
                        "RGBA",
                        (round(_imWidth), round(self.height)),
                        Fretboard.canvasBGColour,
                    )
                    _draw = ImageDraw.Draw(_im)
                if usingVector:
                    _canvas = canvas.canvas()
                    _trafo = trafo.scale(sx=4 / _imWidth, sy=4 / -_imWidth, x=0, y=0)
                    _lineWidthVec = style.linewidth(
                        Fretboard.lineWidth / Fretboard.height
                    )
                    # _trafo = trafo.scale(sx=1 , sy=-1 , x=0, y=0)
                    _outerFretboardPath = path.path()
                _stringY = self.height - _marginSpace
                _stringNotes = []
                _stringYs = []
                _fretXs = []
                for s, string in enumerate(self.strNotes):
                    if usingRaster:
                        _draw.line(
                            (_fretX, _stringY, _imWidth - _marginSpace, _stringY),
                            fill=Fretboard.lineColour,
                            width=Fretboard.lineWidth,
                        )
                    if usingVector:
                        # _canvas.insert()
                        if not connectFretboardLines or s not in (
                            0,
                            len(self.strNotes) - 1,
                        ):
                            print(
                                "string at {} {} {} {}".format(
                                    _fretX, _stringY, _imWidth - _marginSpace, _stringY
                                )
                            )

                            # _linePath = path.path(path.moveto(_fretX,_stringY),
                            #                      path.lineto(_imWidth-_marginSpace,_stringY),
                            #                      path.closepath())

                            # _canvas.stroke(_linePath,
                            #               [style.linewidth.THICK,_trafo,color.rgb(255/255,255/255,255/255)])
                            for c in _colourSchemes:
                                c["canvas"].stroke(
                                    path.line(
                                        _fretX,
                                        _stringY,
                                        _imWidth - _marginSpace,
                                        _stringY,
                                    ),
                                    [_lineWidthVec, c["lineColour"], _trafo],
                                )
                        elif s == 0:
                            _outerFretboardBounds["L"] = _fretX
                            _outerFretboardBounds["R"] = _imWidth - _marginSpace
                            _outerFretboardBounds["T"] = _stringY
                        elif s == len(self.strNotes) - 1:
                            _outerFretboardBounds["B"] = _stringY
                    _stringYs.append(_stringY)
                    _stringY -= _strVertSpace
                    _stringNotes.append([])
                    for fret in range(self.showFrets + 1):
                        _stringNotes[-1].append(
                            JazzNote.noteNameFlats[
                                (JazzNote.distanceFromC(string) + fret) % 12
                            ]
                        )

                # Populate fretXs
                for fret in range(self.showFrets + 1):
                    _fretXs.append(_fretX)
                    # Draw fret

                    if usingRaster:
                        _draw.line(
                            (_fretX, _stringYs[0], _fretX, _stringYs[-1]),
                            fill=Fretboard.lineColour,
                            width=Fretboard.lineWidth,
                        )
                    if usingVector:
                        if not connectFretboardLines or s not in (
                            0,
                            self.showFrets - 1,
                        ):
                            for c in _colourSchemes:
                                c["canvas"].stroke(
                                    path.line(
                                        _fretX, _stringYs[0], _fretX, _stringYs[-1]
                                    ),
                                    [_trafo, _lineWidthVec, c["lineColour"]],
                                )
                        else:
                            pass
                    # Draw fret marker
                    _mW = _marginSpace / 5
                    _mX = _fretX - _fretWidths[fret] / 2
                    _mY = (_stringYs[0] + _stringYs[-1]) / 2
                    _mYoffset = _mW * self.doubleDotsOffset
                    # input('hasdf {}'.format(self.fretIndicatorsDouble))
                    # Draw fret indicators
                    if (fret) in self.fretIndicators:
                        if usingRaster:
                            _draw.ellipse(
                                [_mX - _mW, _mY - _mW, _mX + _mW, _mY + _mW],
                                fill=(0, 0, 0, 255),
                            )
                        if usingVector:
                            for c in _colourSchemes:
                                c["canvas"].draw(
                                    path.circle(_mX, _mY, _mW),
                                    [
                                        _lineWidthVec,
                                        _trafo,
                                        deco.stroked([c["indicationLineColour"]]),
                                        deco.filled([c["indicationLineColour"]]),
                                    ],
                                )

                    elif (fret) in self.fretIndicatorsDouble:
                        if usingRaster:
                            _draw.ellipse(
                                [
                                    _mX - _mW,
                                    _mY - _mW - _mYoffset,
                                    _mX + _mW,
                                    _mY + _mW - _mYoffset,
                                ],
                                fill=(0, 0, 0, 255),
                            )
                            _draw.ellipse(
                                [
                                    _mX - _mW,
                                    _mY - _mW + _mYoffset,
                                    _mX + _mW,
                                    _mY + _mW + _mYoffset,
                                ],
                                fill=(0, 0, 0, 255),
                            )

                        if usingVector:
                            for c in _colourSchemes:
                                c["canvas"].draw(
                                    path.circle(_mX, _mY + _mYoffset, _mW),
                                    [
                                        _lineWidthVec,
                                        _trafo,
                                        deco.stroked([c["indicationLineColour"]]),
                                        deco.filled([c["indicationColour"]]),
                                    ],
                                )
                                c["canvas"].draw(
                                    path.circle(_mX, _mY - _mYoffset, _mW),
                                    [
                                        _lineWidthVec,
                                        _trafo,
                                        deco.stroked([c["indicationLineColour"]]),
                                        deco.filled([c["indicationColour"]]),
                                    ],
                                )
                    _fretX += _fretWidths[fret]
                if connectFretboardLines and usingVector:
                    _outerFretboardPath = path.path()
                    _outerFretboardPath.append(
                        path.moveto(
                            _outerFretboardBounds["L"], _outerFretboardBounds["T"]
                        )
                    )
                    _outerFretboardPath.append(
                        path.lineto(
                            _outerFretboardBounds["R"], _outerFretboardBounds["T"]
                        )
                    )
                    _outerFretboardPath.append(
                        path.lineto(
                            _outerFretboardBounds["R"], _outerFretboardBounds["B"]
                        )
                    )
                    _outerFretboardPath.append(
                        path.lineto(
                            _outerFretboardBounds["L"], _outerFretboardBounds["B"]
                        )
                    )
                    _outerFretboardPath.append(path.closepath())
                    for c in _colourSchemes:
                        c["canvas"].stroke(
                            _outerFretboardPath,
                            [_lineWidthVec, c["lineColour"], _trafo],
                        )

                vectorFCirclesMade = []

                for s, string in enumerate(self.strNotes):
                    for fret in range(self.showFrets + 1):
                        if _stringNotes[s][fret] in _noteNames:
                            if len(_fretXs) > fret + 1:
                                if _fretXs[fret + 1] - _fretXs[fret] > _marginSpace * 2:
                                    _L = _fretXs[fret] - _marginSpace * 2
                                    _T = _stringYs[s] - _marginSpace
                                    _R = _fretXs[fret]
                                    _B = _stringYs[s] + _marginSpace
                                    # print('a width', _R - _L)
                                else:
                                    _R = _fretXs[fret]
                                    # _L = _fretXs[max(0, fret - 1)]
                                    _L = _fretXs[max(0, fret - 1)]
                                    _L = max(_L, _R - _marginSpace * 2)
                                    _T = _stringYs[s] - (_R - _L) / 2
                                    _B = _stringYs[s] + (_R - _L) / 2
                                    # print('b width', _R - _L)
                            else:
                                _R = _fretXs[fret]
                                _L = _fretXs[max(0, fret - 1)]
                                _L = max(_L, _R - _marginSpace * 2)
                                _T = _stringYs[s] - (_R - _L) / 2
                                _B = _stringYs[s] + (_R - _L) / 2
                                # print('width', _R - _L)
                            if fret == 0:
                                pass
                                # _L += _marginSpace * 2
                                # _R += _marginSpace * 2
                            if not indicateNotesWithFCircle:
                                if usingRaster:
                                    _draw.ellipse(
                                        (_L, _T, _R, _B),
                                        fill=(0, 0, 0, 255),
                                        outline=Fretboard.lineColour,
                                    )
                                if usingVector:
                                    
                                    for c in _colourSchemes:
                                        # Draw invisible indicator to keep the frame consistent
                                        if s == 0 and fret == 0 \
                                                and all([Key(k, scaleFunction=note) not in self.strNotes for note in change]):
                                            _L = _fretXs[fret] - _marginSpace * 2

                                        _noteKey = Key(_stringNotes[s][fret])
                                        _noteColour = _noteColours[_noteKey.distanceFromC()]
                                        #print(_noteKey.distanceFromC(),Key(k).distanceFromC())
                                        #input(_noteKey.distanceFromC()-Key(k).distanceFromC())
                                        _noteChange = Change(noteset=[(_noteKey.distanceFromC() - Key(k).distanceFromC())%12])
                                        #input(_noteChange)
                                        c['indicationColour']  = color.rgb(_noteColour[0]/255,_noteColour[1]/255,_noteColour[2]/255)
                                            
                                            
                                        c["canvas"].draw(
                                            path.circle(
                                                (_R + _L) / 2,
                                                (_T + _B) / 2,
                                                (_R - _L) / 2,
                                            ),
                                            [
                                                _lineWidthVec,
                                                _trafo,
                                                deco.stroked(
                                                    [c["indicationLineColour"]]
                                                ),
                                                deco.filled([c["indicationColour"]]),
                                            ],
                                        )
                                        _rad = abs(_R - ((_R + _L) / 2))
                                        if useRadiusLines:
                                            c['canvas'].draw(path.line(
                                                (_R + _L) / 2,
                                                (_T + _B) / 2,
                                                (_R + _L) / 2 + _rad * math.cos(_noteChange.getAngles(returnDegrees=False,goQuarterTurnAnticlockwise=True)[0]),
                                                (_T + _B) / 2 + _rad * math.sin(_noteChange.getAngles(returnDegrees=False,goQuarterTurnAnticlockwise=True)[0]),
                                            ),
                                            [_lineWidthVec,deco.stroked([c["indicationLineColour"]]),
                                            _trafo,c["indicationLineColour"]])
                            elif indicateNotesWithFCircle:

                                _iWidth = _R - _L
                                if True or s == 0 and fret == 0:
                                    _maxWidth = min(
                                        abs(_stringYs[1] - _stringYs[0]),
                                        abs(_fretXs[1] - _fretXs[0]),
                                    )
                                # input( 'an important message:\nself.showFrets: {} _R: {} _L {} iWidth {} fretXs {}'.format(
                                #    self.showFrets,_R,_L,_iWidth,_fretXs))

                                _FCircleColourKey = k  # JazzNote.noteNameFlats[(JazzNote.noteNameFlats.index(_note) )%12]# + _startingDistFromC

                                _changeToIndicate = Change.makeFromSet(
                                    [
                                        (
                                            JazzNote.distanceFromC(
                                                _stringNotes[s][fret]
                                            )
                                            - JazzNote.distanceFromC(k)
                                        )
                                        % 12
                                    ]
                                )
                                _FCirclePathRaster = Graphics.getFCirclePath(
                                    _changeToIndicate,
                                    _FCircleColourKey,
                                    int(_iWidth),
                                    includeFilename=True,
                                    greyScale=greyScale,
                                    invertColour=(fret == 0),
                                )
                                # input('_FCirclePathRaster = {} \nisfile? {}'.format(os.path.normpath(_FCirclePathRaster),os.path.isfile(_FCirclePathRaster)))
                                if (
                                    not os.path.isfile(_FCirclePathRaster)
                                    and "png" in filetypes
                                ):  # FCircle does not exist
                                    if _iWidth == 0:
                                        print(
                                            "Unfortunately _iWidth is 0 for some reason so skipping renderFCircle"
                                        )
                                    else:
                                        if usingRaster:

                                            # input('happened')
                                            if (
                                                _changeToIndicate,
                                                int(_iWidth),
                                            ) not in _FCirclesMadePng:
                                                Graphics.renderFCircle(
                                                    change=_changeToIndicate,
                                                    resolution=int(_iWidth),
                                                    rootColourKey="C",
                                                    saveOnlyOneKey=False,
                                                    filetypes=["png"],
                                                )
                                                print(
                                                    "did make it because we had not made {} yet.".format(
                                                        (
                                                            _changeToIndicate,
                                                            int(_iWidth),
                                                        )
                                                    )
                                                )
                                                _FCirclesMadePng.append(
                                                    (_changeToIndicate, int(_iWidth))
                                                )
                                elif _iWidth != 0 and (not makeNewIndicatorDiagrams):
                                    pass
                                if _iWidth != 0:  # Stupid bug
                                    if usingRaster:
                                        _FCircleFileRaster = Image.open(
                                            _FCirclePathRaster.replace("/", "\\")
                                        ).convert("RGBA")
                                        _im.paste(
                                            _FCircleFileRaster,
                                            (int(_L), int(_T)),
                                            _FCircleFileRaster,
                                        )
                                    if usingVector:
                                        for colourScheme in _colourSchemes:
                                            """_FCirclePathVec = Graphics.getFCirclePath(
                                                _changeToIndicate,
                                                _FCircleColourKey,
                                                resolution=FCircle.vectorSaveResolutions[0], includeFilename=True,
                                                greyScale=colourScheme['greyScale'],
                                                invertColour=(fret == 0) if colourScheme['invertedColours'] == False else fret!=0,
                                                filetype='svg'
                                            )"""
                                            _canvasFCircle = colourScheme[
                                                "canvasFCircles"
                                                + ("Inverted" if fret == 0 else "")
                                            ][_changeToIndicate[0].semitonesFromOne()]
                                            # input('{}'.format(_iWidth,'fhgjfghjfghj'))
                                            _FCircleYScale = -2 * (_iWidth / _maxWidth)
                                            _FCircleXScale = 2 * (_iWidth / _maxWidth)
                                            _FCircleYScale = -2 * (
                                                min(_maxWidth, _iWidth)
                                                / vectorFCircleResolution
                                            )
                                            _FCircleXScale = 2 * (
                                                min(_maxWidth, _iWidth)
                                                / vectorFCircleResolution
                                            )

                                            # input('xscale {} yscale {} iWidth {} maxWidth.... {} vectorFCircleResolution {}'.format(
                                            #    _FCircleXScale,_FCircleYScale,_iWidth,_maxWidth,vectorFCircleResolution))

                                            _FCircleScaleTrafo = trafo.scale(
                                                _FCircleXScale, _FCircleYScale, 0, 0
                                            )

                                            _canvasFCircleScaled = canvas.canvas()
                                            _canvasFCircleScaled.insert(
                                                _canvasFCircle, [_FCircleScaleTrafo]
                                            )

                                            _FCircleTranslateTrafo = trafo.translate(
                                                _L, _T
                                            )

                                            colourScheme["canvas"].insert(
                                                _canvasFCircleScaled,
                                                [_FCircleTranslateTrafo, _trafo],
                                            )

                                            # input(_FCirclePathVec)
                                            # c['canvas'].insert(epsfile.epsfile(0, 0, _FCirclePathVec))
                                            # c['canvas'].insert(svgfile.svgfile(0, 0, _FCirclePathVec,parsed=True,width=self.height/8))

                if usingRaster:
                    _fullnameRaster = self.getFretboardPath(
                        change,
                        k,
                        greyScale,
                        invertColour=invertColour,
                        filetype="png",
                        resolution=resolution,
                    )
                    _pathnameRaster = self.getFretboardPath(
                        change,
                        k,
                        greyScale,
                        invertColour=invertColour,
                        filetype="png",
                        returnName=False,
                        resolution=resolution,
                    )
                    print(
                        "saving raster file:///{} to file:///{}".format(
                            _fullnameRaster.replace("\\", "/"),
                            _pathnameRaster.replace("\\", "/"),
                        )
                    )

                if usingVector:
                    bounds = path.path()
                    boundsL = _fretXs[0] - _marginSpace
                    boundsR = _fretXs[-1]
                    boundsT = _stringYs[0] + _marginSpace
                    boundsB = _stringYs[-1] - _marginSpace
                    bounds.append(path.moveto(boundsL, boundsT))
                    bounds.append(path.lineto(boundsR, boundsT))
                    bounds.append(path.lineto(boundsR, boundsB))
                    bounds.append(path.lineto(boundsL, boundsB))
                    # bounds.append(path.lineto(boundsL, boundsT))
                    bounds.append(path.closepath())
                    # color.transparency(.5)
                    # input(bounds)
                    for c in _colourSchemes:
                        boundsCanvas = canvas.canvas()
                        boundsCanvas.stroke(
                            bounds, [color.rgb(0, 1, 0), color.transparency(1), _trafo]
                        )
                        c["canvas"].insert(boundsCanvas)
                    for filetype in [
                        f for f in filetypes if f in Graphics.vectorFiletypes
                    ]:
                        # input('scheeeeemz ({}) \n{} \nfiletypes {}'.format(len(_colourSchemes),_colourSchemes,filetypes))

                        assert filetype != "eps"
                        assert len(_colourSchemes) == 4
                        for c in _colourSchemes:
                            _fullname = self.getFretboardPath(
                                change,
                                k,
                                greyScale=c["greyScale"],
                                invertColour=c["invertedColours"],
                                filetype=filetype,
                                resolution=resolution,
                            )

                            _pathname = self.getFretboardPath(
                                change,
                                k,
                                greyScale=c["greyScale"],
                                invertColour=c["invertedColours"],
                                returnName=False,
                                filetype=filetype,
                                resolution=resolution,
                            )
                            assert "eps" not in _fullname
                            print(
                                "saving vector file:///{} to file:///{}".format(
                                    _fullname, _pathname.replace("/", "/")
                                )
                            )
                            if not os.path.isdir(_pathname):
                                Utility.makeDirectory(_pathname)

                            c["canvas"].writetofile(_fullname)
                            # boundsCanvas.writetofile(_fullname)
                    # input('asdas {}'.format(len(_colourSchemes)))
                if showImage and usingRaster:
                    _im.show()
                    input("showing imagge")
                if makeColourSchemes:
                    if usingRaster:
                        Graphics.transposeColourSchemes(
                            _im,
                            _fullnameRaster,
                            k,
                        )
                    if Project.findLinesWhereBookGetItemOccurred:
                        input(
                            "lines where getItem heppened {}".format(
                                Book.linesWhereGetItemHappened
                            )
                        )
                if "png" in filetypes:
                    if not os.path.isdir(_pathnameRaster):
                        Utility.makeDirectory(_pathnameRaster)
                    _im.save(_fullnameRaster)

                makeNewIndicatorDiagrams = False
                # print('finished with fretboard {} {} {}'.format(change, key,change.getChangeNumber(addOneToBookPage=True)))
            # del _colourSchemes