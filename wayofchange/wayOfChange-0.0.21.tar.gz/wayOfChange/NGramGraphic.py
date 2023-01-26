from __future__ import annotations, print_function
from Key import Key
from Utility import Utility
input = Utility.input
class NGramGraphic:
    """@classmethod
    def nGramPath(cls, rootKey: Key, noteset: [int], lines=6, invertedColours=False,
                  greyScale=False, filetype='pdf', ):
        if not lines in (3, 4, 6): raise ValueError('Invalid lines.')
        if lines == 3:
            nGramType = 'Trigram'
            subpage = Trigram.notesets[noteset]
        elif lines == 4:
            nGramType = 'Tetragram'
            subpage = Tetragram.notesets[noteset]
        elif lines == 6:
            nGramType = 'Hexagram'
            subpage = Hexagram.notesets[noteset]
        filename = nGramType + '_' + subpage
        path = os.path.join(Graphics.directory, nGramType, filename)

        print('here she be')
        input(path)

    @classmethod
    def renderNGrams(cls,
                     rootKeys: [Key] = [Key(n) for n in Key.allFlats],
                     filetypes=['pdf']):
        rootKeys = [Key(n) for n in rootKeys]
        print('making Hexagrams.')
        for noteset in Hexagram.notesets:
            hexagram = Hexagram.notesets[noteset]
            print('Hexagram', Hexagram['subpage'], 'in ')
            for key in rootKeys:
                print(key, end=', ')

            print()"""

    validTypes = [
        "Monogram",
        "Digram",
        "Trigram",
        "Tetragram",
        "Pentagram",
        "Hexagram",
        "Septagram",
        "Octagram",
        "Nantogram",
        "Decagram",
        "Monodecagram",
        "Duadecagram",
    ]
    '''# This is confusing, what can you do!? ;)
    Graphics.validDiagrams += validTypes'''
    aspectRatio = 1
    lineSpacing = 0.61803399
    breakSpacing = 0.23606797893228276  # small phi cubed
    # breakSpacing = .333333333333333333333333333333333333333333333333
    penThickness = 1
    lineColour = (0, 0, 0, 255)
    lineColourInvert = (255, 255, 255, 255)
    lineCountToDimensions = {
        "6": {"width": 11 / 12, "height": 1},
        "3": {"width": 1, "height": 1},
        "default": {"width": 1, "height": 1},
    }

    def __init__(self, lineCount=6, nGramType=None):
        """using nGramType == 'Trigram' will override using lineCount"""
        if nGramType == None:
            self.lineCount = lineCount
            self.nGramType = NGramGraphic.validTypes[int(lineCount) - 1]
        else:
            self.nGramType = nGramType
            self.lineCount = NGramGraphic.validTypes.index(nGramType) + 1
        self.book = Book(notesToUse=JazzNote.numberOctaveFlats[:lineCount])
        if lineCount != 6:
            warnings.warn(
                "Certain stuff has not been implemented for non-Hexagram ngrams yet."
            )
        if str(self.lineCount) in NGramGraphic.lineCountToDimensions.keys():
            self.canvasWidth = NGramGraphic.lineCountToDimensions[str(self.lineCount)][
                "width"
            ]
            self.canvasHeight = NGramGraphic.lineCountToDimensions[str(self.lineCount)][
                "height"
            ]
        else:
            self.canvasWidth = NGramGraphic.lineCountToDimensions["default"]["width"]
            self.canvasHeight = NGramGraphic.lineCountToDimensions["default"]["height"]

    def renderFiles(self, externalGraphicsPath=None):
        if externalGraphicsPath == None:
            from .Graphics import Graphics
            externalGraphicsPath = Graphics.externalGraphicsPath

        path = pyx.path
        deco = pyx.deco
        color = pyx.color
        style = pyx.style

        for change in self.book:
            semitones = change.getSemitones()
            for root in Key.allFlats:
                for greyScale in (False, True):
                    for invertColour in (False, True):
                        if not invertColour:
                            lineColour = NGramGraphic.lineColour
                            lineColourInv = NGramGraphic.lineColourInv
                        elif invertColour:
                            lineColour = NGramGraphic.lineColourInv
                            lineColourInv = NGramGraphic.lineColour
                        '''colours = Colour.getTransposedColours(
                            Key(root).distanceFromC(),
                            greyScale=greyScale,
                            invertColour=invertColour,
                        )'''
                        colours = Colour.getTransposedColours(
                            Key(root).distanceFromC(),neutralColours=True

                        )
                        filepath = self.getPath(
                            change=change,
                            key=root,
                            invertColour=invertColour,
                            greyScale=greyScale,
                            includeExtension=True,
                            externalGraphicsPath=externalGraphicsPath,
                        )
                        filedir = self.getPath(
                            change=change,
                            key=root,
                            invertColour=invertColour,
                            greyScale=greyScale,
                            includeFile=False,
                            externalGraphicsPath=externalGraphicsPath,
                        )

                        canvas = pyx.canvas.canvas()

                        canvasHeight = self.canvasHeight
                        canvasWidth = self.canvasWidth
                        lineHeight = canvasHeight * self.lineSpacing / self.lineCount
                        lineSpaceHeight = (
                            canvasHeight * (1 - self.lineSpacing) / (self.lineCount - 1)
                        )
                        # nput('the dimensions are these: width: {} height: {}'.format(canvasWidth,canvasHeight))

                        "input( 6*(lineSpaceHeight + lineHeight))"
                        for l in range(self.lineCount):
                            y0 = (lineHeight + lineSpaceHeight) * l
                            y1 = y0 + lineHeight
                            x0, x1, x2, x3 = (
                                0,
                                (1 - self.breakSpacing) * canvasWidth / 2,
                                (1 + self.breakSpacing) * canvasWidth / 2,
                                canvasWidth,
                            )
                            if l in semitones:
                                rects = (
                                    path.path(
                                        path.moveto(x0, y0),
                                        path.lineto(x0, y1),
                                        path.lineto(x3, y1),
                                        path.lineto(x3, y0),
                                        path.lineto(x0, y0),
                                        path.closepath(),
                                    ),
                                )
                            else:
                                rects = (
                                    path.path(
                                        path.moveto(x0, y0),
                                        path.lineto(x0, y1),
                                        path.lineto(x1, y1),
                                        path.lineto(x1, y0),
                                        path.lineto(x0, y0),
                                        path.closepath(),
                                    ),
                                    path.path(
                                        path.moveto(x2, y0),
                                        path.lineto(x2, y1),
                                        path.lineto(x3, y1),
                                        path.lineto(x3, y0),
                                        path.lineto(x2, y0),
                                        path.closepath(),
                                    ),
                                )

                            canvas.linewidth = 1
                            colour = colours[l]
                            """canvas.stroke(rect2,[
                                color.rgb(lineColour[0] / 255,lineColour[1] / 255,lineColour[2] / 255)])
                            canvas.fill(rect2,[
                                color.rgb(colour[0] / 255,colour[1] / 255,colour[2] / 255)])"""

                            for rect in rects:
                                if l in semitones:
                                    fillColour = colour
                                else:
                                    fillColour = lineColourInv
                                canvas.draw(
                                    rect,
                                    [
                                        style.linejoin.round,
                                        color.rgb(
                                            lineColour[0] / 255,
                                            lineColour[1] / 255,
                                            lineColour[2] / 255,
                                        ),
                                        deco.stroked(),
                                        deco.filled(
                                            [
                                                color.rgb(
                                                    fillColour[0] / 255,
                                                    fillColour[1] / 255,
                                                    fillColour[2] / 255,
                                                )
                                            ]
                                        ),
                                    ],
                                )

                        Utility.makeDirectory(filedir)
                        canvas.writetofile(filepath)
                        print(
                            "saved {} {} to file///:{}.".format(
                                self.nGramType,
                                change.getChangeNumber(combinatoricSize=self.lineCount),
                                filepath,
                            )
                        )

    def getPath(
        self,
        change: Change,
        key=Key("C"),
        invertColour=False,
        greyScale=False,
        includeGraphicsPath=True,
        externalGraphicsPath=False,
        includeFile=True,
        includeExtension=False,
        pathSeperator="\\",
    ):

        key = Key(key)
        nGramType = NGramGraphic.validTypes[self.lineCount - 1]
        if invertColour == False:
            if greyScale == False:
                path = Graphics.hexagramsDirectory
            else:
                path = Graphics.hexagramsBWDirectory
        else:
            if greyScale == False:
                path = Graphics.hexagramsInvDirectory
            else:
                path = Graphics.hexagramsBWInvDirectory
        if not includeGraphicsPath:
            path = "Hexagram" + pathSeperator
        path = os.path.join(path,key.getASCII())
        if includeFile:
            path = os.path.join(path,"Hexagram_" + str(
                change.getChangeNumber(
                    combinatoricSize=self.lineCount,
                )
            ))
            if includeExtension:
                path += ".pdf"
        path = path.replace("\\", pathSeperator).replace("/", pathSeperator)
        path = path.replace("Hexagram", nGramType)
        # input('in NGramGraphic.getPath path: {} includeExtension: {}'.format(path,includeExtension))
        if externalGraphicsPath:
            path = path.replace(
                Graphics.directory.replace("\\", pathSeperator).replace(
                    "/", pathSeperator
                ),
                Graphics.directoryExternal.replace("\\", pathSeperator).replace(
                    "/", pathSeperator
                ),
            )
        return path