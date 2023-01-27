from __future__ import annotations, print_function
import colorsys
from Utility import Utility
input = Utility.input
class Colour:
    A4 = 432
    # These colours will be the default, but then it will replace it after.
    makeGraphicsColoured = 0
    useBlackBackground = 0
    """rgbByDistanceColourDk = ['008700', '8eff29', 'ffff0d', 'ff9b00',
                        'ff6600', 'c02e29', 'ff0000', 'dc00b9',
                        '8507b9', '6007ff', '0000ff', '00ae62']

    rgbByDistanceColourLt = ['008700', '8eff29', 'ffff0d', 'ff9b00',
                        'ff6600', 'c02e29', 'ff0000', 'dc00b9',
                        '8507b9', '6007ff', '0000ff', '00ae62']"""

    if False:
        hues = [i / 12 for i in range(12)]
        # Transpose from start == red to start == green
        hues = hues[5:] + hues[:5]

    else:
        hues = [
            0,  # Red
            1.0 / 24,  # Red-Orange
            2.0 / 24,  # Orange
            3.1 / 24,  # Honey Eb
            4 / 24,  # Yellow
            5.2 / 24,  # Chartreuse
            7 / 24,  # Green
            10 / 24,
            13 / 24,  # Blue
            17.5 / 24,  # Blurple
            19.1 / 24,  # Purple
            21 / 24,
        ]
        """        hues = [0, 2 / 24, 2 / 24,
                3 / 24, 4 / 6, 2 / 9,
                7 / 24, 10 / 24, 13 / 24,
                18 / 24, 19.5 / 24, 21 / 24]"""
        hues = hues[7:] + hues[:7]
    hues = hues[::-1]
    hlsByDistanceColourDk = [(hue, 0.45, 1) for hue in hues]  # .2
    hlsByDistanceColourLt = [(hue, 0.67, 1) for hue in hues]
    hlsByDistanceColourNt = [(hue, 0.5, 1) for hue in hues]
    # input(hlsByDistanceColourDk)
    rgbByDistanceColourDk = [
        colorsys.hls_to_rgb(hls[0], hls[1], hls[2]) for hls in hlsByDistanceColourDk
    ]
    rgbByDistanceColourLt = [
        colorsys.hls_to_rgb(hls[0], hls[1], hls[2]) for hls in hlsByDistanceColourLt
    ]
    rgbByDistanceColourNt = [
        colorsys.hls_to_rgb(hls[0], hls[1], hls[2]) for hls in hlsByDistanceColourNt
    ]

    rgbByDistanceColourDk = [
        "".join("%02X" % round(i * 255) for i in rgb) for rgb in rgbByDistanceColourDk
    ]
    rgbByDistanceColourLt = [
        "".join("%02X" % round(i * 255) for i in rgb) for rgb in rgbByDistanceColourLt
    ]
    rgbByDistanceColourNt = [
        "".join("%02X" % round(i * 255) for i in rgb) for rgb in rgbByDistanceColourNt
    ]

    rgbInkColourDk = "FFFFFF"
    rgbInkColourLt = "000000"
    rgbInkColourNt = "FFFFFF"
    rgbPaperColourDk = "000000"
    rgbPaperColourLt = "FFFFFF"
    rgbPaperColourNt = "000000"
    # input('rgbByDistanceColourDk {}\nrgbByDistanceColourLt {}'.format(rgbByDistanceColourDk,rgbByDistanceColourLt))
    rgbByDistanceBWDk = ["CCCCCC"] * 12
    rgbByDistanceBWLt = ["444444"] * 12
    rgbByDistanceBWNt = ["888888"] * 12
    if makeGraphicsColoured == False:
        rgbByDistance = [i for i in rgbByDistanceBWDk]
    else:
        rgbByDistance = [i for i in rgbByDistanceColourDk]
    # nameByDistance = ['1','b2','2','b3','3','4','b5','5','b6','6','b7','7']
    nameByDistanceLt = [
        "C-Lt",
        "Db-Lt",
        "D-Lt",
        "Eb-Lt",
        "E-Lt",
        "F-Lt",
        "Gb-Lt",
        "G-Lt",
        "Ab-Lt",
        "A-Lt",
        "Bb-Lt",
        "B-Lt",
    ]
    nameByDistanceDk = [
        "C-Dk",
        "Db-Dk",
        "D-Dk",
        "Eb-Dk",
        "E-Dk",
        "F-Dk",
        "Gb-Dk",
        "G-Dk",
        "Ab-Dk",
        "A-Dk",
        "Bb-Dk",
        "B-Dk",
    ]
    nameByDistanceNt = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    validLatexTags = nameByDistanceLt + nameByDistanceDk + nameByDistanceNt
    # nameByDistance = ['green','green-yellow','yellow','yellow-orange','orange','orange-red','red','red-purple','purple','purple-blue','blue']

    def __init__(self, A4=432, makeGraphicsColoured=True):
        self.A4 = A4
        self.makeGraphicsColoured = makeGraphicsColoured
        # These colours will be the default, but then it will replace it after.
        self.rgbByDistanceColourDk = [
            "008700",
            "8eff29",
            "ffff0d",
            "ff9b00",
            "ff6600",
            "c02e29",
            "ff0000",
            "dc00b9",
            "8507b9",
            "6007ff",
            "0000ff",
            "00ae62",
        ]
        self.rgbByDistanceBWDk = [
            "000000",
            "000000",
            "000000",
            "000000",
            "000000",
            "000000",
            "000000",
            "000000",
            "000000",
        ]
        if makeGraphicsColoured == False:
            self.rgbByDistance = self.rgbByDistanceBWDk
        else:
            self.rgbByDistance = self.rgbByDistanceColourDk

    @classmethod
    def blendColourValue(cls, a, b, t):
        """
        :param a: first colour value
        :param b: second colour value
        :param t: transition between
        :return average value:
        """
        return math.sqrt((1 - t) * a**2 + t * b**2)

    @classmethod
    def blendAlphaValue(cls, a, b, t):
        return (1 - t) * a + t * b

    @classmethod
    def blendColours(cls, c1, c2, t):
        """
        :param c1: colour 1
        :param c2: colour 2
        :param t: transition
        :return:
        """
        usingAlpha = len(c1) in (2, 4) == True
        ret = []
        for b1, band1 in enumerate(c1):
            band2 = c2[b1]
            if b1 != len(c1) or not usingAlpha:
                raise TypeError("not done")

    @classmethod
    def writeColourSchemesToFile(cls, fileFormat="tex"):

        _jsStr = ""
        _schemes = ("Colour", "ColourInv", "BW", "BWInv")
        for s, scheme in enumerate(_schemes):
            print("generating", scheme)
            if fileFormat == "tex":
                _filename = os.path.join(Project.directoryTex , "colourMap-" + scheme + ".tex")
            elif fileFormat == "js":
                _filename = os.path.join(Project.directoryJS, "colourMap.js")
            else:
                raise ValueError("non valid format")
            if scheme == "Colour":
                _colours = Colour.rgbByDistanceColourDk
                _coloursInv = Colour.rgbByDistanceColourLt
            elif scheme == "ColourInv":
                _colours = Colour.rgbByDistanceColourLt
                _coloursInv = Colour.rgbByDistanceColourDk
            elif scheme == "BW":
                _colours = ["000000"] * 12
                _coloursNeut = ["000000"] * 12
                _coloursInv = ["FFFFFF"] * 12
            elif scheme == "BWInv":
                _colours = ["FFFFFF"] * 12
                _coloursInv = ["000000"] * 12
                _coloursNeut = ["FFFFFF"] * 12
            if scheme in ("Colour", "ColourInv"):
                _coloursNeut = Colour.rgbByDistanceColourNt

            _str = ""

            if fileFormat == "js" and s == 0:
                _str += (
                    "const keyColours = {\n"
                    + "".join(['  "' + i + '": {},\n' for i in _schemes])
                    + "};\n"
                )
            for p, palette in enumerate((_colours, _coloursNeut, _coloursInv)):

                if p == 0:
                    colourTags = Colour.nameByDistanceDk
                    inkColour = Colour.rgbInkColourDk
                    paperColour = Colour.rgbPaperColourDk
                elif p == 1:
                    colourTags = Colour.nameByDistanceNt
                    inkColour = Colour.rgbInkColourNt
                    paperColour = Colour.rgbPaperColourNt
                elif p == 2:
                    colourTags = Colour.nameByDistanceLt
                    inkColour = Colour.rgbInkColourLt
                    paperColour = Colour.rgbPaperColourLt
                for c, colour in enumerate(palette):
                    print(colourTags[c], colour)
                    if fileFormat == "tex":
                        _str += (
                            "\definecolor{"
                            + colourTags[c]
                            + "}{HTML}{"
                            + colour
                            + "}%\n"
                        )
                    elif fileFormat == "js":
                        _str += 'keyColours["{}"]["{}"] = "#{}";\n'.format(
                            scheme, colourTags[c], colour
                        )
                if fileFormat == "tex":
                    _str += "\definecolor{ink}{HTML}{" + inkColour + "}%\n"
                    _str += "\definecolor{paper}{HTML}{" + paperColour + "}%\n"
                elif fileFormat == "js":

                    if "Dk" in colourTags[0]:
                        darkness = "-Dk"
                    elif "Lt" in colourTags[0]:
                        darkness = "-Lt"
                    elif "Nt" in colourTags[0]:
                        darkness = "-Nt"
                    else:
                        darkness = ""
                    _str += 'keyColours["{}"]["{}"] = "#{}";\n'.format(
                        scheme, "ink" + darkness, inkColour
                    )
                    _str += 'keyColours["{}"]["{}"] = "#{}";\n'.format(
                        scheme, "paper" + darkness, paperColour
                    )

                # _str += '\n'

            if _str[-1] == "\n":
                _str = _str[0:-1]
            text_file = open(_filename, "w+")
            text_file.write(_str)
            text_file.close()
            _jsStr += _str

            # print(_str)

            print("updated colourMap at " + _filename)
            # input(_str + '\nwould thou like to continue?')
        if fileFormat == "js":
            text_file = open(_filename, "w+")
            text_file.write(_jsStr)
            text_file.close()

    @classmethod
    def getGlobalRGBsFromA4(cls, f: int) -> []:
        # not finished
        raise TypeError("not done")
        # using well tempered tuning
        if f in (None, 0):
            f = cls.A4
        RGBs = []
        freqs = []
        # grab the frequency of C, 9 notes below
        # because the book assumes that the 'first' place
        # is C, not A
        C4 = f * 2 ** (-9 / 12)
        for i in range(12):
            freqs.append(C4 * 2 ** (i / 12))
        # TODO: calculate hue
        # Then get rgb for that
        # Then

    @classmethod
    def getTransposedColourTags(
        cls,
        colourTranspose: int = 0,
        makeGreyscale=False,
        invertColour=False,
        pianoKeys=False,
        neutralColours=False,
    ):
        if makeGreyscale:
            if not pianoKeys:
                if invertColour:
                    _colours = Colour.nameByDistanceLt
                elif not invertColour:
                    _colours = Colour.nameByDistanceDk
                if neutralColours:
                    _colours = Colour.nameByDistanceNt
            elif pianoKeys:
                _colours = [0 for i in range(12)]
                for i in range(len(_colours)):
                    if i in (0, 2, 4, 5, 7, 9, 11):
                        if invertColour:
                            _colours[i] = "black"
                        elif not invertColour:
                            _colours[i] = "white"
                    else:
                        if invertColour:
                            _colours[i] = "white"
                        elif not invertColour:
                            _colours[i] = "black"
        elif not makeGreyscale:
            if invertColour:
                _colours = Colour.nameByDistanceLt
            elif not invertColour:
                _colours = Colour.nameByDistanceDk
            if neutralColours:
                _colours = Colour.nameByDistanceNt

        if len(_colours) != 12:
            raise (
                TypeError(
                    "There are supposed to be 12 colours but there are not. length {}\n{} ".format(
                        len(_colours), _colours
                    )
                )
            )
        return [_colours[(i + colourTranspose) % 12] for i in range(12)]

    @classmethod
    def getTransposedColours(
        cls,
        colourTranspose: int = 0,
        greyScale=False,
        invertColour=False,
        pianoKeys=False,
        neutralColours=False,
    ):
        if greyScale:
            if not pianoKeys:
                if neutralColours:
                    _colours = Colour.rgbaTupleByDistanceBWNt
                elif invertColour:
                    _colours = Colour.rgbaTupleByDistanceBWLt
                elif not invertColour:
                    _colours = Colour.rgbaTupleByDistanceBWDk
            elif pianoKeys:
                _colours = [0 for i in range(12)]
                for i in range(len(_colours)):
                    if i in (0, 2, 4, 5, 7, 9, 11):
                        if invertColour:
                            _colours[i] = (0, 0, 0, 255)
                        elif not invertColour:
                            _colours[i] = (255, 255, 255, 255)
                    else:
                        if invertColour:
                            _colours[i] = (255, 255, 255, 255)
                        elif not invertColour:
                            _colours[i] = (0, 0, 0, 255)
        elif not greyScale:
            if neutralColours:
                _colours = Colour.rgbaTupleByDistanceColourNt
            elif invertColour:
                _colours = Colour.rgbaTupleByDistanceColourLt
            elif not invertColour:
                _colours = Colour.rgbaTupleByDistanceColourDk
        if len(_colours) != 12:
            raise (
                TypeError(
                    "There are supposed to be 12 colours but there are not. length {}\n{} ".format(
                        len(_colours), _colours
                    )
                )
            )
        return [_colours[(i + colourTranspose) % 12] for i in range(12)]

    @classmethod
    def getColourOfChange(cls, change: Change):
        raise TypeError("not done")

    @classmethod
    def getRGBTuples(cls, includeAlpha=False, alpha=255) -> list[tuple]:
        _tuples = []
        for i in cls.rgbByDistance:
            _tuples.append(cls.convertRGBToTupleForm(i))
        return _tuples

    @classmethod
    def convertRGBToTupleForm(cls, rgb: str, includeAlpha=False, alpha=255) -> tuple:

        first = rgb[:2]
        second = rgb[2:4]
        third = rgb[4:]
        if includeAlpha == False:
            return tuple([int(first, 16), int(second, 16), int(third, 16)])
        else:
            return tuple([int(first, 16), int(second, 16), int(third, 16), alpha])

    @classmethod
    def modifyAlphaChannelOfRGBATuple(cls, rgba: tuple, alpha: int) -> tuple:
        if not len(rgba) == 4:
            raise TypeError("rgba tuple supposed to have 4 channels." + str(rgba))
        if alpha < 0 or alpha > 255 or type(alpha) != int:
            raise ValueError("alpha to be supplied as int between 0-255. " + str(alpha))
        return tuple([rgba[0], rgba[1], rgba[2], alpha])
        
# Finish initialising
Colour.rgbaTupleByDistance = [
    Colour.convertRGBToTupleForm(i, includeAlpha=True) for i in Colour.rgbByDistance
]
Colour.rgbTupleByDistance = [
    Colour.convertRGBToTupleForm(i, includeAlpha=False) for i in Colour.rgbByDistance
]
Colour.rgbaTupleByDistanceColourDk = [
    Colour.convertRGBToTupleForm(i, includeAlpha=True)
    for i in Colour.rgbByDistanceColourDk
]
Colour.rgbTupleByDistanceColourDk = [
    Colour.convertRGBToTupleForm(i, includeAlpha=False)
    for i in Colour.rgbByDistanceColourDk
]
Colour.rgbaTupleByDistanceColourNt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=True)
    for i in Colour.rgbByDistanceColourNt
]
Colour.rgbTupleByDistanceColourNt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=False)
    for i in Colour.rgbByDistanceColourNt
]
Colour.rgbaTupleByDistanceColourLt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=True)
    for i in Colour.rgbByDistanceColourLt
]
Colour.rgbTupleByDistanceColourLt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=False)
    for i in Colour.rgbByDistanceColourLt
]
Colour.rgbaTupleByDistanceBWLt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=True) for i in Colour.rgbByDistanceBWLt
]
Colour.rgbTupleByDistanceBWLt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=False)
    for i in Colour.rgbByDistanceBWLt
]
Colour.rgbaTupleByDistanceBWDk = [
    Colour.convertRGBToTupleForm(i, includeAlpha=True) for i in Colour.rgbByDistanceBWDk
]
Colour.rgbTupleByDistanceBWDk = [
    Colour.convertRGBToTupleForm(i, includeAlpha=False)
    for i in Colour.rgbByDistanceBWDk
]
Colour.rgbaTupleByDistanceBWNt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=True) for i in Colour.rgbByDistanceBWNt
]
Colour.rgbTupleByDistanceBWNt = [
    Colour.convertRGBToTupleForm(i, includeAlpha=False)
    for i in Colour.rgbByDistanceBWNt
]