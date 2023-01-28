from __future__ import annotations, print_function
from Utility import Utility
from Change import Change
from JazzNote import JazzNote
from Colour import Colour
import numpy as np
import math
input = Utility.input
class FCircle:
    # white = (255, 255, 255, 255)
    canvasBGColour = (0, 0, 0, 0)
    circleBGColourInv = (255, 255, 255, 255)
    circleBGColour = (0, 0, 0, 255)
    lineColour = (0, 0, 0, 255)
    lineColourInv = (255, 255, 255, 255)  # (0,0,0,255)
    minimumCirclePixels = 2
    proportion = 0.618033988749894848204586834
    artCircleProportion = 0.618033988749894848204586834 * 2 ** (1 / 2)
    lineProportion = 0.04258684210526316
    radiusOuterProportionRCircle = proportion * 1.3
    radiusOfEachRCircle = 0.15
    singleNoteCircleProportion = proportion
    fractality = 3
    vectorSmallResolution = 64
    vectorMediumResolution = 256
    vectorLargeResolution = 2048
    vectorSaveResolutions = [
        vectorSmallResolution,
        vectorMediumResolution,
        vectorLargeResolution,
    ]
    polygonResolution = 64
    saveOnlyOneKeyIfResolutionExceeds = 2048
    validTypes = ["FCircle", "SCircle", "PCircle"]

    def __init__(
        self,
        centre: list[float, float],
        r: [float],
        change: Change,
        colourTranspose: int,
        proportion=None,
        invertBG=False,
    ):
        self.centre = centre
        self.x = centre[0]
        self.y = centre[1]
        if proportion is None:
            proportion = FCircle.proportion
        self.r = r * proportion
        #input( change.__class__.__name__)
        if change.__class__.__name__ == "Change":
            self.change = change
        else:
            raise TypeError(
                "change needs to be type Change, not "
                + str(type(change))
                + " "
                + str(change)
                + '. '
                + change.__class__.__name__
            )
        self.colourTranspose = colourTranspose
        self.invertBG = invertBG

    def __repr__(self):
        return "FCircle(centre={},r={},change=Change({}),colourTranspose={},invertBG={})".format(
            self.centre,
            self.r,
            self.change.__repr__(),
            self.colourTranspose,
            self.invertBG,
        )

    def __str__(self):
        return "FCircle({},{},{},{})".format(
            self.centre, self.r, self.change, self.colourTranspose
        )

    @classmethod
    def setClassConstantsForSCircle(cls):
        FCircle.includeRCircle = False
        FCircle.useChordCircles = True
        FCircle.proportion = 1
        FCircle.lineProportion = 0.0001
        FCircle.alternateBG = False

    @classmethod
    def setClassConstantsForFCircle(cls):
        FCircle.includeRCircle = True
        FCircle.useChordCircles = False
        FCircle.alternateBG = True
        FCircle.proportion = 0.618033988749894848204586834
        FCircle.lineProportion = 0.04258684210526316
        FCircle.alternateBG = True

    def drawTrigrams(self, im, colours, lineColour, thickness, showDebug=False):

        draw = ImageDraw.Draw(im)
        r2 = self.r * 2.0
        r = self.r / FCircle.proportion
        centreX = self.r
        centreY = self.r
        pi = math.pi
        lineProportion = 1 / 12.0
        # https://math.stackexchange.com/questions/377234/circle-in-square-calculate-distance-from-squares-corner-to-circles-perimeter
        # diagonal = 0.5 * ( r2 * 2 ** -1 - r2)
        diagonal = 0.5 * r2 * (2**-1 - 1)
        trigramH = diagonal / (2**0.5)  # 2#(2*pi)

        _trigrams = self.change.divideScaleBy(denominator=4, normaliseToSlice=True)
        _qturn = math.radians(90)
        _width = trigramH * 3 / 2.0
        st = 0
        for t, trigram in enumerate(_trigrams):
            # _angle = math.radians(90 * t + 45 + 270)
            _angle = math.radians(90 * t + 45 + 270)
            # input('angle {}'.format(math.degrees(_angle)))
            _lines = trigram.getSemitones()
            # first number is the radius of circle where trigrams start

            x = 1 * math.cos(_angle) * r + r
            y = 1 * math.sin(_angle) * r + r
            x += int(math.cos(_angle) * diagonal / pi)
            y += int(math.sin(_angle) * diagonal / pi)
            for l in range(3):

                x -= int(math.cos(_angle) * diagonal / pi)
                y -= int(math.sin(_angle) * diagonal / pi)
                _colour = colours[st % len(colours)]
                if l in _lines:
                    # Unbroken line
                    x1 = x + (math.cos(_angle - _qturn) * _width / 2)
                    y1 = y + (math.sin(_angle - _qturn) * _width / 2)
                    x2 = x + (math.cos(_angle + _qturn) * _width / 2)
                    y2 = y + (math.sin(_angle + _qturn) * _width / 2)

                    Graphics.fatLine(
                        im=im,
                        line=[x1, y1, x2, y2],
                        outline=lineColour,
                        fill=_colour,
                        thickness=thickness,
                    )

                else:
                    # broken line
                    Graphics.fatLine(
                        im=im,
                        line=[
                            x + (math.cos(_angle - _qturn) * _width / 2),
                            y + (math.sin(_angle - _qturn) * _width / 2),
                            x - (math.cos(_angle + _qturn) * _width / 12),
                            y - (math.sin(_angle + _qturn) * _width / 12),
                        ],
                        fill=_colour,
                        outline=lineColour,
                        thickness=thickness,
                    )
                    Graphics.fatLine(
                        im,
                        [
                            x - (math.cos(_angle - _qturn) * _width / 2),
                            y - (math.sin(_angle - _qturn) * _width / 2),
                            x + (math.cos(_angle + _qturn) * _width / 12),
                            y + (math.sin(_angle + _qturn) * _width / 12),
                        ],
                        fill=_colour,
                        outline=lineColour,
                        thickness=thickness,
                    )

                    """Graphics.fatLine(im, [x - (math.cos(_angle - _qturn) * _width / 2),
                                          y - (math.sin(_angle - _qturn) * _width / 2),
                                          x + (math.cos(_angle + _qturn) * _width / 12),
                                          y + (math.sin(_angle + _qturn) * _width / 12),
                                          ], fill=_colour, outline=lineColour, thickness=thickness
                                     )"""
                    print(st)
                st += 1

        if showDebug:
            im.show()
        return im

    @classmethod
    def renderFCircleGrid(
        cls,
        columns: int,
        rows: int,
        colourKey: str = None,
        useHexagramGrid=True,
        sortHexIntoSubsequence=False,
        mirrorNegativeAxis=True,
        splitX=4,
        splitY=4,
        greyScale=False,
        invertColour=False,
        skipIfFileExists=False,
    ):

        raise TypeError("shit")
        # _sPx = Latex.SmallCircleResolution
        if colourKey is None:
            colourKey = Book.rootColourKey

        if useHexagramGrid:
            if sortHexIntoSubsequence:
                _subname = "_hexagram-subsequence"
            else:
                _subname = "_hexagram-iChing"
        elif not useHexagramGrid:
            _subname = "_sequence"

        Utility.makeDirectory(os.path.join(Graphics.fCircleChartsDirectory, _subname))
        if not invertColour:
            if not greyScale:
                _directory = os.path.join(Graphics.fCircleChartsDirectory, _subname)
            else:
                _directory = os.path.join(Graphics.fCircleChartsBWDirectory, _subname)
        else:
            if not greyScale:
                _directory = os.path.join(Graphics.fCircleChartsInvDirectory, _subname)
            else:
                _directory = (
                    os.path.join(Graphics.fCircleChartsBWInvDirectory, _subname)
                )

        _sPx = 64
        _sep = round(_sPx / 3.14159**3)
        _xpad = 0
        _ypad = round(0 + (_sPx / 0.772727272727272) - _sPx)
        _cellWidth = _sPx + _sep + _xpad
        _cellHeight = _sPx + _sep + _ypad
        # input('imsgeSize {} circleSize {}'.format((columns*(_sPx+_sep)),_sPx))
        _paddingRows = 0
        _paddingRows = 0
        til = Image.new("RGB", (columns * _cellWidth + _sep, rows * _cellHeight + _sep))
        draw = ImageDraw.Draw(til)
        font = ImageFont.truetype(Latex.fontStr, round(17))
        # _fontHeight = font.getSize('M')[1]

        if sortHexIntoSubsequence:
            _hexagramBook = Book(["1", "b2", "2", "b3", "3", "4"])
            # input(str(_hexagramBook.sequence))
            _positiveHexagrams = [_hexagramBook[i] for i in range(0, 32, +1)]
            _negativeHexagrams = [i.withoutNote("1") for i in _positiveHexagrams]
            _negativeHexagrams.reverse()

            _hexaST = [
                i.getSemitones() for i in _negativeHexagrams + _positiveHexagrams
            ]

            # for i in _positiveHexagrams:
            # _hexaST.append(i.getSemitones())

            print(
                "positive",
                _positiveHexagrams,
                "negative",
                _negativeHexagrams,
                "length",
                len(_hexaST),
                "hexaST",
                _hexaST,
                sep="\n",
            )
            """_hexagramNumbers = ['adsfg' for i in range(65)]
            for i in range(1,65):
                _hexagramNumbers[i] = Hexagram.subChange[i]
                print('asdfasdfasdf',_hexagramNumbers[i])
            #input(_hexagramNumbers)#[Change.makeFromSet(s).getHexagram(['subpage']) for s in _hexaST]
            _hexaST = [Hexagram.notesets[_hexagramNumbers[i]] for i in _hexagramNumbers[1:]]"""
        elif not sortHexIntoSubsequence:
            _hexaST = [s for s in Hexagram.notesets[1:]]
        _changeST = _hexaST
        print("started drawing. ", end="")
        _cell = 0
        for i1, h1 in tqdm(enumerate(_hexaST)):
            _cell += 1
            print("row", i1)
            for i2, h2 in enumerate(_hexaST):
                _cell += 1
                # _changeNumber=Change.makeFromSet(h1+[i+6 for i in h2]).getChangeNumber(decorateChapter=False,addOneToBookPage=True)
                if useHexagramGrid:

                    _change = Change.makeFromSet(h1 + [i + 6 for i in h2])
                elif not useHexagramGrid:
                    _pageNumber = i1 * 64 + i2 - 2048
                    # print(_pageNumber)
                    # TODO: If you change sequence indexing change rootIsChangeOne
                    _change = Change.makeFromChangeNumber(
                        _pageNumber,
                    )  # i1*64+i2-2048)

                # print(h1,h2,_change)
                #### Do it this way if you want to grab the src imgs from bitmaps
                # im = Image.open(Graphics.getFCirclePath(
                #    _change, colourKey, _sPx, includeFilename=True))  # 25x25
                #### Do it this way if you want to grab the src imgs from pdfs
                im = pdf2image.convert_from_path(
                    Graphics.getFCirclePath(
                        _change,
                        colourKey,
                        256,
                        includeFilename=True,
                        filetype="pdf",
                    ),
                    size=_sPx,
                )[0].convert("RGBA")

                _x = _cellWidth * i2 + _sep
                _y = _cellHeight * i1 + _sep
                _txt = (
                    "".join(_change.getHexagram())
                    + " " * (4 - len(_change))
                    + str(_change.getChangeNumber())
                )
                til.paste(im.convert("RGBA"), (_x, _y))
                draw.text(
                    (_x, _y + _sPx + _ypad / 3), _txt, font=font, fill=(255, 255, 255)
                )

        _filename = "FCircleChart"
        _extension = ".png"

        if splitX > 1 or splitY > 1:

            _cropDirectory = os.path.join(_directory, "crop{}by{}\\".format(splitX, splitY))

            Utility.makeDirectory(_cropDirectory)
            width, height = til.size  # Get dimensions
            _cropWidth = width / splitX
            _cropHeight = height / splitY
            print("width {} height {}".format(_cropWidth, _cropHeight))
            for x in range(splitX):
                for y in range(splitY):

                    _fullname = (
                        _cropDirectory
                        + _filename
                        + "_"
                        + colourKey
                        + "_x"
                        + str(x)
                        + "of"
                        + str(splitX)
                        + "y"
                        + str(y)
                        + "of"
                        + str(splitY)
                        + _extension
                    )
                    if skipIfFileExists and os.path.isfile(_fullname):
                        print(_fullname, "exists so not making it.")
                        return _fullname
                    left = x * _cropWidth
                    top = y * _cropHeight
                    right = left + _cropWidth
                    bottom = top + _cropHeight
                    _crop = til.crop((left, top, right, bottom))
                    _crop.save(_fullname)
                    print(
                        "finished crop. {} \nl{} t{} r{} b{}".format(
                            _fullname, left, top, right, bottom
                        )
                    )

        _fullname = os.path.join(_directory, _filename + _subname + "_" + colourKey + _extension)
        til.save(_fullname)
        print("finished making. " + _fullname)

    def getRingCircles(self, invertBG=False) -> [FCircle]:
        _proportion = FCircle.radiusOuterProportionRCircle
        if invertBG:
            _invertBG = not self.invertBG
        else:
            _invertBG = self.invertBG
        _mode = 0
        _rCircles = []
        _semitones = self.change.getSemitones()
        for st in range(12):
            _degree = st * 360 / 12 - 90
            _radian = _degree * 3.141596238 / 180

            if st in _semitones:
                if self.change.notes[0] == JazzNote("1"):
                    _colourTranspose = (st + self.colourTranspose - _semitones[0]) % 12
                else:
                    _colourTranspose = (
                        _semitones[0] + self.colourTranspose - _semitones[_mode]
                    ) % 12
                _rCircle = FCircle(
                    [
                        self.x
                        + math.cos(_radian) * self.r * _proportion / FCircle.proportion,
                        self.y
                        + math.sin(_radian) * self.r * _proportion / FCircle.proportion,
                    ],
                    self.r * FCircle.radiusOfEachRCircle / FCircle.proportion,
                    self.change.mode(_mode)
                    if self.change.notes[0] == JazzNote("1")
                    else self.change.getRotation(st - _semitones[0]),
                    _colourTranspose,
                    _proportion,
                    invertBG=_invertBG,
                )
                # print('stuuuuuuff',st +self.colourTranspose -_semitones[_mode])
                _rCircles.append(_rCircle)
                _mode += 1

        """for i in range(len(self.change):
            _rCircles.append(FCircle
                ([self.x,
                self.y],
                self.r,
                change.mode(i),
                self.colourTranspose+\
                self.change.notes[i].semitonesFromOne(),
                self.r*RCircle.proportion/FCircle.proportion)
                             )"""
        return _rCircles

    def getInnerCircles(
        self,
        defaultSize=0.618033988749894848204586834,
        useRingCircles=True,
        alternateBG=True,
        invertBG=False,
        useChordCircles=False,
        usePolyCircles=True,
        showDebug=False,
        circleType="FCircle",
    ) -> list[FCircle]:
        # .7071067811865475 1 over the square root of 2
        # .618033988749894848204586834 phi

        if invertBG:
            _invertBG = not self.invertBG
        else:
            _invertBG = self.invertBG

        if len(self.change.notes) == 0:
            return []

        # defaultSize contrrols the single note shape

        if False and len(self.change.notes) == 1:
            _newSize = self.r * defaultSize
            _angle = self.change.notes[0].getAngle(
                returnDegrees=False, goQuarterTurnAnticlockwise=True
            )

            """return [FCircle(centre=[self.x + math.cos(_angle) * (self.r - _newSize),
                                    self.y + math.sin(_angle) * (self.r - _newSize)],
                            r=_newSize, change=self.change,
                            colourTranspose=self.colourTranspose,
                            invertBG=_invertBG)]"""

            _artCircles = [
                FCircle(
                    centre=[
                        self.x + math.cos(_angle) * _newSize,
                        self.y + math.sin(_angle) * _newSize,
                    ],
                    r=_newSize,
                    change=Change([]),
                    colourTranspose=self.colourTranspose,
                    invertBG=_invertBG,
                )
            ]
        else:
            _artCircles = np.array([])
        _innerCircles = np.array([])
        _chordCrops = np.array([])
        _poly = np.array([])
        _ringCircles = np.array([])
        _circles = _artCircles
        if useChordCircles:
            # print('chord c')
            _chordCrops = self.getChordCrops(invertBG=True)
            # _circles += _chordCrops
            _circles = np.append(_circles, _chordCrops)
        if useRingCircles:
            # print('chord r')
            _ringCircles = self.getRingCircles(invertBG=False)
            _circles = np.append(_circles, _ringCircles)
            # _circles += _ringCircles
        if usePolyCircles and not len(self.change) in (1, 2):
            # print('chord p  {}'.format(_poly))
            _poly = self.getPolyCircle(invertBG=True)
            # input('poly {} FCircle {}'.format(_poly,self))
            # print('done chord p')
            if not _poly is None:
                _circles = np.append(_circles, _poly)
            else:
                raise TypeError("poly failed")
        # print('circles:',_circles)

        valid_circles = _circles[np.logical_and(np.not_equal(_circles, None),
                                                np.greater_equal([_circle.r * 2 for _circle in _circles],
                                                                 FCircle.minimumCirclePixels))]
        _innerCircles = np.append(_innerCircles, valid_circles)
        
        
        #Non Vectorised
        '''for circle in _circles:
            if circle is None:
                continue
            elif circle.r * 2 < FCircle.minimumCirclePixels:
                continue
            else:
                # _innerCircles.append(circle)
                _innerCircles = np.append(_innerCircles, circle)'''

        if showDebug:
            input(
                "helpful error.. \ncrops {}\npoly {}\nrings {}\ncircles {}\n innercircles {}".format(
                    len(_chordCrops),
                    _poly,
                    len(_ringCircles),
                    len(_circles),
                    len(_innerCircles),
                )
            )

        if len(_innerCircles) > 0 and type(_innerCircles[0]) != FCircle:
            input("error I think. the list should be flattened")
        # print('returning innercircles')
        return _innerCircles

    def getChordCrops(self, invertBG=False) -> list[FCircle]:
        if len(self.change.notes) <= 1:
            return []
        _bigR = self.r  # *FCircle.proportion
        _chordCrops = Graphics.getChordCentres(
            change=self.change,
            R=_bigR,
            returnFCircle=True,
            colourTranspose=self.colourTranspose,
            topLeftOrigin=False,
        )
        _chordCrops = [
            i.movePosition(self.x - 2 * self.r, self.y - 2 * self.r)
            for i in _chordCrops
        ]

        if not invertBG:
            for i in _chordCrops:
                i.invertBG = self.invertBG
            return _chordCrops
        else:
            for i in _chordCrops:
                i.invertBG = not self.invertBG
            return _chordCrops

    def getPolyCircle(
        self, invertBG=False, returnPoly=False, scale=1.0, shrinkIntoOrigin=True
    ) -> FCircle:
        # print('start getPolyCircle()')

        _poly = self.change.getPolygon(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            scale=scale,
            shrinkIntoOrigin=shrinkIntoOrigin,
            returnFCircle=not returnPoly,
            colourTranspose=self.colourTranspose,
        )

        # print('got _poly')
        if returnPoly:
            return _poly
        if _poly is None:
            return None

        # _poly = _poly.movePosition(self.x - 2 * self.r,
        #                             self.y - 2 * self.r)
        # _poly.movePosition(se)
        if invertBG:
            _poly.invertBG = not self.invertBG
        else:
            _poly.invertBG = self.invertBG
        return _poly

    def movePosition(self, xDist, yDist) -> FCircle:
        return FCircle(
            [self.x + xDist, self.y + yDist], self.r, self.change, self.colourTranspose
        )