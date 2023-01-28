from __future__ import annotations, print_function
import os, math
import pyx
import PIL
import numpy as np
import datetime
from Project import Project
from Fretboard import Fretboard
from Change import Change
from JazzNote import JazzNote
from FCircle import FCircle
from Key import Key
from NGramGraphic import NGramGraphic
from Utility import Utility
from Colour import Colour

import polylabel # pip install python-polylabel

input = Utility.input
print = Utility.print
class Graphics:
    directoryExternal = (
        os.path.join(Project.directoryExternal, "Graphics")
    )  # Render to external HD
    directory = os.path.join(Project.directory, "Graphics")  # Render to internal HD
    useExternalDirectory = True
    # directory = directoryExternal  # Render to external HD <- dont do this
    colourDirectory = os.path.join(directory, "Col")
    greyscaleDirectory = os.path.join(directory, "BW")
    colourInvertedDirectory = os.path.join(directory, "ColInv")
    greyscaleInvertedDirectory = os.path.join(directory, "BWInv")
    chordsOfChangeDir = os.path.join(colourDirectory, "ChordsOfChange")
    chordsOfChangeInvDir = os.path.join(colourInvertedDirectory, "ChordsOfChange")
    chordsOfChangeBWDir = os.path.join(greyscaleDirectory, "ChordsOfChange")
    chordsOfChangeBWInvDir = os.path.join(greyscaleInvertedDirectory, "ChordsOfChange")
    fCirclesDirectory = os.path.join(colourDirectory, "FCircle")
    fCirclesBWDirectory = os.path.join(greyscaleDirectory, "FCircle")
    fCirclesInvDirectory = os.path.join(colourInvertedDirectory, "FCircle")
    fCirclesBWInvDirectory = os.path.join(greyscaleInvertedDirectory, "FCircle")
    sCirclesDirectory = os.path.join(colourDirectory, "SCircle")
    sCirclesBWDirectory = os.path.join(greyscaleDirectory, "SCircle")
    sCirclesInvDirectory = os.path.join(colourInvertedDirectory, "SCircle")
    sCirclesBWInvDirectory = os.path.join(greyscaleInvertedDirectory, "SCircle")
    pCirclesDirectory = os.path.join(colourDirectory, "PCircle")
    pCirclesBWDirectory = os.path.join(greyscaleDirectory, "PCircle")
    pCirclesInvDirectory = os.path.join(colourInvertedDirectory, "PCircle")
    pCirclesBWInvDirectory = os.path.join(greyscaleInvertedDirectory, "PCircle")
    fCircleChartsDirectory = os.path.join(colourDirectory, "FCircle_Charts")
    fCircleChartsBWDirectory = os.path.join(greyscaleDirectory, "FCircle_Charts")
    fCircleChartsInvDirectory = os.path.join(colourInvertedDirectory, "FCircle_Charts")
    fCircleChartsBWInvDirectory = os.path.join(
        greyscaleInvertedDirectory, "FCircle_Charts"
    )
    hexagramsDirectory = os.path.join(colourDirectory, "Hexagram")
    hexagramsBWDirectory = os.path.join(greyscaleDirectory, "Hexagram")
    hexagramsInvDirectory = os.path.join(colourInvertedDirectory, "Hexagram")
    hexagramsBWInvDirectory = os.path.join(greyscaleInvertedDirectory, "Hexagram")
    pianosDirectory = os.path.join(colourDirectory, "Piano")
    pianosBWDirectory = os.path.join(greyscaleDirectory, "Piano")
    pianosInvDirectory = os.path.join(colourInvertedDirectory, "Piano")
    pianosBWInvDirectory = os.path.join(greyscaleInvertedDirectory, "Piano")
    accordionsDirectory = os.path.join(colourDirectory, "Accordion")
    accordionsBWDirectory = os.path.join(greyscaleDirectory, "Accordion")
    accordionsInvDirectory = os.path.join(colourInvertedDirectory, "Accordion")
    accordionsBWInvDirectory = os.path.join(greyscaleInvertedDirectory, "Accordion")
    fretboardsDirectory = os.path.join(colourDirectory, "Fretboard")
    fretboardsBWDirectory = os.path.join(greyscaleDirectory, "Fretboard")
    fretboardsInvDirectory = os.path.join(colourInvertedDirectory, "Fretboard")
    fretboardsBWInvDirectory = os.path.join(greyscaleInvertedDirectory, "Fretboard")
    validDiagrams = list(Fretboard.instruments.keys())
    validDiagrams += [
        "Piano",
        "Accordion",
        "ChordsOfChange"
    ]
    validDiagrams += NGramGraphic.validTypes
    validDiagrams += ['Piano'+t for t in Change.validVoicingTypes]
    validDiagrams += FCircle.validTypes
    validLayouts = ["Key Row", "Piano"]
    validFiletypes = ["png", "pdf", "eps", "ps", "svg"]
    vectorFiletypes = validFiletypes[:]
    vectorFiletypes.remove("png")

    # Utility.printPrettyVars(validFiletypes,vectorFiletypes)
    # input()
    @classmethod
    def findMissingDiagrams(
            cls,
            colourKey: str,
            resolution: int,
            filetype="pdf",
            diagramType="FCircle",
            ignoreChangeNumbers=[],
            lookForRootedChanges=True,
            lookForRootlessChanges=True,
            returnChanges=True,
            renderIfNotFound=False
    ) -> [int]:
        "lookForRootedChanges == {}\nlookForRootlessChanges == {}\n".format(
            lookForRootedChanges, lookForRootlessChanges
        )
        print(str(cls)+'.findMissingDiagrams()')
        _missingDiagrams = []
        for i in tqdm(range(1, 2049)):
            _change = Change.makeFromChangeNumber(i)
            _changeNegative = _change.withoutNote("1")
            # makes lookForRo...() work
            _changeAxes = (
                (_change, _changeNegative)
                if all([j for j in (lookForRootedChanges, lookForRootlessChanges)])
                else (_change,)
                if lookForRootedChanges
                else (_changeNegative,)
            )
            for rootness in _changeAxes:
                for invertColour in (True, False):
                    for greyScale in (True, False):
                        if Graphics.seeIfDiagramExists(
                                filetype=filetype,
                                change=rootness,
                                key=colourKey,
                                resolution=resolution,
                                greyScale=greyScale,
                                invertColour=invertColour,
                                diagramType=diagramType,
                                impatientSkip=False,
                                renderIfNotFound=renderIfNotFound
                        ):
                            pass  # print('checking i and it exists'+str(i))
                        else:  # There is no FCircle here
                            if rootness.getChangeNumber() not in ignoreChangeNumbers:
                                if returnChanges:
                                    _missingDiagrams.append(rootness)
                                elif not returnChanges:
                                    _missingDiagrams.append(rootness.getChangeNumber())
        return _missingDiagrams
    
    
    @classmethod
    def deleteDiagrams(
        cls,
        changes: [Change],
        diagramTypes=[str],
        resolutions=[],
        filetypes=["pdf"],
        keys: [Key] = None,
        deleteCol=True,
        deleteBW=1,
        deleteColInv=1,
        deleteBWInv=1,
        externalGraphicsPath=False,
    ):
        # print('looking for files with these params: {}'.format(locals()))
        deletedFilesCount = 0
        if keys == None:
            keys = [Key.allFlats[i] for i in range(12)]

        for change in tqdm(changes[5::6]):
            for diagramType in diagramTypes:
                for resolution in resolutions:
                    for key in keys:
                        for filetype in filetypes:
                            params = {
                                "change": change,
                                "key": key,
                                "resolution": resolution,
                                "diagramType": diagramType,
                                "filetype": filetype,
                                "externalGraphicsPath": externalGraphicsPath,
                            }
                            paths = []
                            if deleteCol:
                                paths.append(
                                    Graphics.getDiagramPath(
                                        **params, greyScale=False, invertColour=False
                                    )
                                )
                            if deleteColInv:
                                paths.append(
                                    Graphics.getDiagramPath(
                                        **params, greyScale=False, invertColour=True
                                    )
                                )
                            if deleteBW:
                                paths.append(
                                    Graphics.getDiagramPath(
                                        **params, greyScale=True, invertColour=False
                                    )
                                )
                            if deleteBWInv:
                                paths.append(
                                    Graphics.getDiagramPath(
                                        **params, greyScale=True, invertColour=True
                                    )
                                )
                            for i in paths:
                                try:
                                    os.remove(i)
                                    print("deleted " + i)
                                    deletedFilesCount += 1
                                except FileNotFoundError:
                                    pass  # print('was not able to remove '+ i)

        input("done deleting files")

    @classmethod
    def deleteDiagramsOLD(
        cls,
        changes: [Change],
        diagramTypes=[str],
        resolutions=[],
        filetypes=["pdf"],
        keys: [Key] = None,
        deleteCol=True,
        deleteBW=1,
        deleteColInv=1,
        deleteBWInv=1,
        externalGraphicsPath=False,
    ):
        print("looking for files with these params".format(locals()))
        if keys == None:
            keys = [Key.allFlats[i] for i in range(12)]
        paths = []
        for diagramType in diagramTypes:
            for resolution in resolutions:
                for change in tqdm(changes):
                    for key in keys:
                        for filetype in filetypes:
                            params = {
                                "change": change,
                                "key": key,
                                "resolution": resolution,
                                "diagramType": diagramType,
                                "filetype": filetype,
                                "renderIfNotFound": False,
                                "externalGraphicsPath": externalGraphicsPath,
                            }
                            if deleteCol:
                                paths.append(
                                    Graphics.seeIfDiagramExists(
                                        **params, greyScale=False, invertColour=False
                                    )
                                )
                            if deleteColInv:
                                paths.append(
                                    Graphics.seeIfDiagramExists(
                                        **params, greyScale=False, invertColour=True
                                    )
                                )
                            if deleteBW:
                                paths.append(
                                    Graphics.seeIfDiagramExists(
                                        **params, greyScale=True, invertColour=False
                                    )
                                )
                            if deleteBWInv:
                                paths.append(
                                    Graphics.seeIfDiagramExists(
                                        **params, greyScale=True, invertColour=True
                                    )
                                )

        confirmation = input(
            "paths to delete\n{}\n\nThere are {} paths to delete. Delete? (enter a string)".format(
                paths, len(paths)
            )
        )
        if confirmation.strip():
            for path in tqdm(paths):
                if path:
                    success = False

                    try:
                        os.remove(path)
                        print("deleted", path)
                        success = True
                    except FileNotFoundError as e:
                        print("File Not Found!. {}".format(e))
        input("{}\n Finished deleting {} files.".format(paths, len(paths)))

    @classmethod
    def testShit(self):
        c1 = pyx.canvas.canvas()
        c2 = pyx.canvas.canvas()
        c1.stroke(path=pyx.path.line(0, 1, 1, 0))
        c2.insert(c1)
        c2.writePDFfile("C:\\Users\\Dre\\Desktop\\supergay")

    @classmethod
    def convertDiagramsToRaster(
        cls,
        changeRange=None,
        outputHeights=[int],
        core=0,
        cores=1,
        skipIfFileExists=False,
    ):
        if changeRange is None:
            # changeRange = range(-2048,2049)
            changeRange = (1362,)
            changeRange = list(range(1179, 2049)) + list(range(-2048, 0))
        for changeNumber in tqdm(changeRange[core::cores]):
            for key in ("C",):
                for diagramType in ("FCircle", "SCircle"):
                    change = Change.makeFromChangeNumber(changeNumber)
                    _diagramPath = Graphics.getDiagramPath(
                        change,
                        key,
                        diagramType,
                        resolution=4096,
                        filetype="pdf",
                        includeFileExtension=True,
                        includeGraphicsPath=True,
                    )
                    _diagramFilename = Graphics.getDiagramPath(
                        change,
                        key,
                        diagramType,
                        resolution=4096,
                        filetype="pdf",
                        includeFileExtension=True,
                        includeGraphicsPath=False,
                    )
                    _diagramFilename = _diagramFilename.split("/")[-1]
                    for outputHeight in outputHeights:

                        _outputFolder = _diagramPath.replace(
                            "pdf_4096px", "png_" + str(outputHeight) + "px"
                        ).replace(_diagramFilename, "")
                        if os.path.exists(
                            os.path.join(
                                _outputFolder, _diagramFilename.replace(".pdf", ".png")
                            )
                        ):
                            if skipIfFileExists:
                                print(
                                    "skipped {} because it exists, and skipIfFileExists == True".format(
                                        "file:///"
                                        + os.path.join(
                                            _outputFolder,
                                            _diagramFilename.replace(".pdf", ".png"),
                                        )
                                    )
                                )
                                continue
                            else:
                                os.remove(
                                    os.path.join(
                                        _outputFolder,
                                        _diagramFilename.replace(".pdf", ".png"),
                                    )
                                )
                        Utility.makeDirectory(_outputFolder)
                        print(
                            "doing one. {} {} on core {}/{} (starts counting at 0).".format(
                                "file:///" + _diagramFilename,
                                "file:///" + _outputFolder,
                                core,
                                cores,
                            )
                        )

                        # input(_diagramPath + ' ' + _outputFolder)

                        pdf2image.convert_from_path(
                            _diagramPath,
                            thread_count=1,
                            use_pdftocairo=True,
                            transparent=True,
                            size=outputHeight,
                            output_folder=_outputFolder,
                            single_file=True,
                            output_file=_diagramFilename.replace(".pdf", ""),
                        )

                        # os.rename(os.path.join(_outputFolder,_diagramFilename.replace('.pdf','.png')),_diagramFilename.replace('.pdf','.png'))
                        print(
                            "converted {} to {} outputfile: {}".format(
                                "file:///" + _diagramPath,
                                "file:///" + _outputFolder,
                                "file:///" + _diagramFilename.replace(".pdf", ""),
                            )
                        )

    @classmethod
    def getChordsOfChangePath(
        cls,
        change: Change,
        rootKey: Key,
        tabuliseBySemitonePosition: bool = True,
        invertColour: bool = False,
        useColour: bool = True,
        includeGraphicsPath: bool = True,
        includeDirectory: bool = True,
        includeFilename: bool = True,
        includeExtension=True,
        externalGraphicsPath=False,
        chordsOfChangeType=None
    ):
        if chordsOfChangeType == None or chordsOfChangeType == 'Chords Of Change':
            chordsOfChangeType = 'Chords Of Change'
        elif chordsOfChangeType == 'Mode Family':
            pass
        else:
            raise ValueError('chordsOfChangeType: {} must be one of these: {}'.format(chordsOfChangeType,
                                                                                      "'Mode Family', 'Chords Of Change', or None"))
        rootKey = Key(rootKey)
        if not isinstance(change, Change):
            raise TypeError(
                "{} should be of type Change, not {}".format(change, type(change))
            )
        _str = ""
        if includeDirectory:
            _str = os.path.join(_str, "ChordsOfChange")
            if includeGraphicsPath:
                if useColour:
                    if not invertColour:
                        _str = Graphics.chordsOfChangeDir
                    else:
                        _str = Graphics.chordsOfChangeInvDir
                else:
                    if not invertColour:
                        _str = Graphics.chordsOfChangeBWDir
                    else:
                        _str = Graphics.chordsOfChangeBWInvDir
            _str = os.path.join(_str, rootKey.note)

        if includeFilename:
            _str = os.path.join(
                _str, "{}{}".format(chordsOfChangeType.replace(' ',''),change.getChangeNumber())
            )
            if includeExtension:
                _str += ".pdf"
        if not includeGraphicsPath:
            _str = _str.replace(Graphics.directory, "")
        if externalGraphicsPath:
            _str = _str.replace(Graphics.directory, Graphics.directoryExternal)
        # input('Path is {}\nFunction called with parameters{}'.format(_str,locals()))
        return _str

    @classmethod
    def getDirectoryOfColourScheme(cls, greyScale, invertColour):
        if not invertColour:
            if not greyScale:
                _directory = Graphics.colourDirectory
            else:
                _directory = Graphics.greyscaleDirectory
        else:
            if not greyScale:
                _directory = Graphics.colourInvertedDirectory
            else:
                _directory = Graphics.greyscaleInvertedDirectory
        return _directory

    @classmethod
    def getKeyDiagramPath(
        cls,
        change: Change,
        diagramTypes: list,
        resolution: int = 256,
        includeFilename=True,
        pathSeperator="/",
        greyScale=False,
        invertColour=False,
        includeGraphicsPath=True,
        includeSubdirectory=True,
        key: str = None,
    ):
        _str = ""
        if key == None:
            _key = ""
        else:
            _key = JazzNote.makeAlphabetNoteUseSingleFlats(key)

        _keyDiagramName = "_" + "_".join(
            [i for i in sorted(Utility.flattenList(diagramTypes))]
        )
        _filename = _keyDiagramName + "_"
        _filename += str(
            change.getChangeNumber(decorateChapter=False, addOneToBookPage=True)
        )
        if _key != "":
            _filename += "_" + _key
        _filename += ".png"
        _directory = ""
        if includeGraphicsPath:
            _directory = Graphics.getDirectoryOfColourScheme(greyScale, invertColour)
        if includeSubdirectory:
            _directory += _keyDiagramName + pathSeperator
            _directory += str(resolution) + "px" + pathSeperator
        _directory = _directory.replace("/", pathSeperator).replace("\\", pathSeperator)
        if includeFilename:
            _directory += _filename
        return _directory

    @classmethod
    def getFiletypeResolutionFolderName(cls, filetype, resolution):
        return filetype + "_" + str(resolution) + "px"

    @classmethod
    def getDiagramPath(
        cls,
        change: Change,
        key: str,
        diagramType: str,
        resolution: int = 256,
        includeFilename=True,
        pathSeperator="/",
        greyScale=False,
        invertColour=False,
        includeGraphicsPath=True,
        externalGraphicsPath=False,
        filetype="pdf",
        includeFileExtension=False,
        warnOnFileNotFound=True,
        renderIfNotFound=False,
        tryToReplaceMissingWithRootKey=True,
        showDebug=False,
    ):

        if not externalGraphicsPath:
            pass
            # raise TypeError('Change this line to externalGraphicsPath=externalGraphicsPath.\nIf you do not know why I am complaining, then delete this Error.')
        if externalGraphicsPath and not includeGraphicsPath:
            includeGraphicsPath = True
        if not isinstance(change, Change):
            raise TypeError(
                "{} should be of type Change, not {}".format(change, type(change))
            )

        if not filetype in Graphics.validFiletypes:
            raise TypeError(
                "{} not in Graphics.validFileTypes. {}".format(
                    filetype, Graphics.validFiletypes
                )
            )
        if resolution == 0:
            raise ValueError("resolution of 0 probably is pointless")
        # Replace With code from Key class
        if isinstance(key, Key):
            key = key.note
        key = JazzNote.makeAlphabetNoteUseSingleFlats(key)
        if not diagramType in Graphics.validDiagrams:
            raise ValueError(
                "{} not in Graphics.validDiagrams \n{}".format(
                    diagramType, Graphics.validDiagrams
                )
            )
        if diagramType in FCircle.validTypes:

            dPath = Graphics.getFCirclePath(
                change=change,
                colourKey=key,
                resolution=resolution,
                includeFilename=includeFilename,
                pathSeperator=pathSeperator,
                greyScale=greyScale,
                invertColour=invertColour,
                includeGraphicsPath=includeGraphicsPath,
                externalGraphicsPath=externalGraphicsPath,
                circleType=diagramType,
                filetype=filetype,
                includeFileExtension=False,
            )

            assert not includeGraphicsPath or 'wayOfChange' in dPath, dPath
        elif diagramType[:5] == "Piano":
            _pianoType = 'Scale'
            if len(diagramType) > 5:
                if diagramType[5:] in Change.validVoicingTypes:
                    _pianoType = diagramType[5:]
            dPath = Piano.getPianoPath(
                change=change,
                key=key,
                includeFilename=includeFilename,
                pathSeperator=pathSeperator,
                greyScale=greyScale,
                invertColour=invertColour,
                includeGraphicsPath=includeGraphicsPath,
                externalGraphicsPath=externalGraphicsPath,
                filetype=filetype,
                includeFileExtension=False,
                voicingType=_pianoType
            )

        elif diagramType == "Accordion":
            if filetype == "pdf":
                raise ValueError("Accordion can not be rendered in pdf")
            dPath = Accordion.getAccordionPath(
                change=change,
                key=key,
                resolution=resolution,
                returnName=includeFilename,
                pathSeperator=pathSeperator,
                greyScale=greyScale,
                invertColour=invertColour,
                filetype=filetype,
                includeGraphicsDirectory=includeGraphicsPath,
                externalGraphicsPath=externalGraphicsPath,
                includeFileExtension=False,
            )
        elif diagramType in list(Fretboard.instruments.keys()):

            dPath = Fretboard.instruments[diagramType]["Fretboard"].getFretboardPath(
                change=change,
                key=key,
                greyScale=greyScale,
                invertColour=invertColour,
                returnName=includeFilename,
                includeGraphicsPath=includeGraphicsPath,
                pathSeperator=pathSeperator,
                resolution=resolution,
                fretBoardType=diagramType,
                filetype=filetype,
                externalGraphicsPath=externalGraphicsPath,
                includeExtension=False,
            )
            # input(dPath)

            if len(dPath) > 100:
                raise ValueError("why? {}".format(dPath))
        elif diagramType in NGramGraphic.validTypes:
            dPath = NGramGraphic(nGramType=diagramType).getPath(
                change=change,
                key=key,
                greyScale=greyScale,
                invertColour=invertColour,
                includeGraphicsPath=includeGraphicsPath,
                includeExtension=False,
                pathSeperator=pathSeperator,
                externalGraphicsPath=externalGraphicsPath,
            )
        elif diagramType == 'ChordsOfChange':
            dPath = Graphics.getChordsOfChangePath(
                change=change,
                rootKey=key,
                externalGraphicsPath=externalGraphicsPath,
                invertColour=invertColour,
                useColour=not greyScale,
                includeDirectory=True,
                includeFilename=True,
            )
        else:
            raise ValueError(
                "not done implementing {} in getDiagramPath().".format(diagramType)
            )

        if externalGraphicsPath:
            # Replacing to move to external HD
            input("NONONO")
            dPath = dPath.replace(Graphics.directory, Graphics.directoryExternal)

        osPath = dPath + "." + filetype.lower()
        # osPath = osPath.replace('/','\\')

        if os.path.isfile(osPath) and os.path.isdir(os.path.dirname(osPath)):
            if showDebug:
                print(osPath, "exists....")

        else:
            replacementPath = osPath
            # input(osPath)
            if renderIfNotFound:
                Graphics.seeIfDiagramExists(
                    change=change,
                    key=key,
                    resolution=resolution,
                    greyScale=greyScale,
                    invertColour=invertColour,
                    diagramType=diagramType,
                    filetype=filetype,
                    externalGraphicsPath=externalGraphicsPath,
                    showDebug=showDebug,
                    renderIfNotFound=True,
                )

            elif tryToReplaceMissingWithRootKey and replacementPath:

                if showDebug:
                    print("replacing\n", dPath, end=" ")
                    dPath = replacementPath
                    print("with\n", dPath, "because it did not exist in that key.")

            elif warnOnFileNotFound:
                warnings.warn(
                    "{} not found. Are you sure you want to render this? It probably will not compile.".format(
                        osPath
                    )
                )
        if includeFileExtension == True:
            dPath += "." + filetype.lower()
        assert not includeGraphicsPath or 'wayOfChange' in dPath, \
            'diagramType=={} dPath=={}'.format(diagramType,dPath)
        return dPath

    @classmethod
    def renderKeysDiagrams(
        cls,
        book: Book,
        diagramTypes: list = [["Piano"]],  #
        # diagramTypes:list=[['Piano','Guitar'],['FCircle','Accordion']],
        keys: list = None,
        layoutType: str = "Piano",
        resolution: int = 256,
        keyPadding: float = 0.03,
        keyTableColAndRows: tuple = (2, 6),
        keyTableIterateChangeByCol=True,
        pageProportion=8.5 / 11,
        greyScale=False,
        invertColour=False,
        changes=None,
        onlyMakeIfFileIsMissing=True,
        showIm=False,
    ):

        if keys == None:
            keys = JazzNote.noteNameFlats
        if not all([(d in Graphics.validDiagrams) for r in diagramTypes for d in r]):
            raise ValueError(
                "{} not in Graphics.validDiagrams ({})".format(
                    i, Graphics.validDiagrams
                )
            )
        if type(diagramTypes[0]) != list:
            raise ValueError("expecting list of lists, not {}".format(diagramTypes))

        """for r in diagramTypes:
            print(r,'r')
            for i in r:
                print(i,'i')
                if i not in Graphics.validDiagrams:
                    raise TypeError('{} not in Graphics.validDiagrams {}'.format(
                        i,Graphics.validDiagrams
                    ))"""

        if not all([JazzNote.isAlphabetNoteStr(i) for i in keys]):
            raise ValueError("{} not a validAlphabetNoteStr".format(i, validDiagrams))
        if not layoutType in Graphics.validLayouts:
            raise ValueError(
                "{} not in Graphics.validDiagrams ({})".format(i, validDiagrams)
            )
        if keyTableColAndRows[0] * keyTableColAndRows[1] < len(keys):
            raise ValueError(
                "these numbers {} of rows and columns will not allow you to display all keys {}.".format(
                    keyTableColAndRows, keys
                )
            )
        if changes == None:
            changes = book
        if len(changes) > 1:
            print(
                "renderKeysDiagrams(diagramTypes={},keys={},layoutType={})".format(
                    diagramTypes, keys, layoutType
                )
            )
        if len(changes) > 1000:
            print("WARNING! This uses like 60GB of RAM to do all of them.")

        _rootIsChangeOneForIndexingTemp = Book.rootIsChangeOneForIndexing
        Book.rootIsChangeOneForIndexing = True

        diagramIms = []
        maxWidths = {}
        for diagramRow in diagramTypes:
            for diagramType in diagramRow:
                maxWidths[diagramType] = 0
        if len(changes) > 1000:
            print("making internal list of images.\nMaking change ", end="")
        for change in changes:
            print(change, end=", ")
            _change = book[change]
            diagramIms.append([])
            for key in keys:
                # print(key)
                diagramIms[-1].append([])
                for diagramRow in diagramTypes:
                    for diagramType in diagramRow:
                        diagramIms[-1][-1].append(
                            {
                                "path": Graphics.getDiagramPath(
                                    change=_change,
                                    key=key,
                                    diagramType=diagramType,
                                    resolution=resolution,
                                    includeFilename=True,
                                    pathSeperator="/",
                                    greyScale=greyScale,
                                    invertColour=invertColour,
                                ),
                            }
                        )
                        # print(diagramIms[-1][-1])
                        # input('path: '+ diagramIms[-1][-1][-1]['path']+'\n')
                        diagramIms[-1][-1][-1]["im"] = Image.open(
                            diagramIms[-1][-1][-1]["path"]
                        ).convert("RGBA")
                        diagramIms[-1][-1][-1]["change"] = change
                        diagramIms[-1][-1][-1]["diagramType"] = diagramType
                        _im = diagramIms[-1][-1][-1]["im"]
                        if _im.width > maxWidths[diagramType]:
                            maxWidths[diagramType] = _im.width
        print("finished making internal list.")
        _maxWidth = max([maxWidths[i] for i in maxWidths])
        # print(maxWidths,[str(i)+' : '+str(idx) for idx,i in enumerate(maxWidths)])
        if layoutType == "Piano":
            _pageHeight = 7 * resolution + 6 * resolution * (keyPadding)
            # Add room for rows of diagrams
            _pageHeight *= len(diagramTypes)
            _pageHeight -= resolution * keyPadding
            _pageHeight = math.floor(_pageHeight)

        elif layoutType == "Key Row":
            pass
        _pageWidth = math.floor(_pageHeight * pageProportion)
        _pageWidthMinimum = 0
        for row in diagramTypes:
            _rowWidth = 0
            # print(diagramTypes,maxWidths)
            # input(row)
            for d, diagram in enumerate(row):
                _rowWidth += maxWidths[diagram]
                _rowWidth += keyPadding * resolution

            _pageWidthMinimum = max(
                _pageWidthMinimum, (_rowWidth * 2) - keyPadding * 1 * resolution
            )  # len(diagramTypes))

        # print('_pageWidth,_pageWidthMinimum',_pageWidth,_pageWidthMinimum)

        if _pageWidth < _pageWidthMinimum:
            _pageWidth = int(_pageWidthMinimum)
            _pageHeight = int(_pageWidth / pageProportion)
        if layoutType == "Piano":
            _pagePiano = Piano(
                keyboardHeightPx=_pageWidth,
                octaveWidthProportion=_pageHeight / _pageWidth,  # 1/pageProportion,
                blackKeyProportion=0.5,
                evenlySpacedWhites=True,
            )
            _poly = _pagePiano.getPianoKeyPolygons(startingKey="C", totalKeys=12)
        if len(changes) > 1000:
            print("Now actually drawing pictures for change ", end="")
        for change in diagramIms:

            _change = book[change[0][0]["change"]]
            _savePath = Graphics.getKeyDiagramPath(
                _change,
                diagramTypes=diagramTypes,
                resolution=resolution,
            )
            if onlyMakeIfFileIsMissing and os.path.isfile(_savePath):
                print("skipped making {} ".format(_savePath))
                continue

            _bIm = Image.new(
                "RGBA", (_pageWidth, _pageHeight), (255, 255, 255, 0)
            )  # base image
            draw = ImageDraw.Draw(_bIm)
            _changeNumber = change[0][0]["change"]
            for k, key in enumerate(change):

                _kP = _poly[k]
                # exchange the x and y
                _b = max([i for i in _kP[0::2]])
                _t = min([i for i in _kP[0::2]])
                _l = min([i for i in _kP[1::2]])
                _r = max([i for i in _kP[1::2]])
                # flip the x
                _l = _pageWidth - _l
                _r = _pageWidth - _r
                # make sure the coordinates are right
                _l, _r = min(_l, _r), max(_l, _r)
                _t, _b = min(_t, _b), max(_t, _b)
                # print(_l,_t,_r,_b)
                # input()
                # _bIm = Graphics.ellipse(im=_bIm, xy=[_l,_t,_r,_b],
                #                 fill=(233,122,0,255), outline=(55,55,55,255), width=10)

                # Graphics.drawFatPolygonToIm(_bIm,(_l,_t,_r,_b),outline=(44,44,44,255),width=10)
                # draw.rectangle(((_l, _t), (_r, _b)), outline="red")

                _y = _t
                for row in diagramTypes:
                    _x = _l
                    for diagramType in row:
                        for findDiagramType in key:
                            if findDiagramType["diagramType"] == diagramType:
                                _dIm = findDiagramType["im"]
                                break
                        # print('key=',key, 'diagramType',diagramType,'row', row,sep='\n')
                        # print('\nkey\n:',key,'\ntype\n',diagramType,'yeaheyeah')
                        # _dIm = key[diagramType]['im'] #diagram image
                        # _dIm.convert('RGBA')
                        _dW, _dH = _dIm.size
                        # print(diagramType)
                        # print('CHANGE',change,'KEY',key,'bla',type(key))
                        _bIm.paste(_dIm, (_x, _y, _x + _dW, _y + _dH), mask=_dIm)
                        if layoutType == "Piano":
                            pass
                            # print(_poly, len(_poly))
                            # input(' was _poly')
                        elif layoutType == "Key Row":
                            pass
                        _x += _dIm.size[0] + int(resolution * keyPadding)
                    _y += _dIm.size[1] + int(resolution * keyPadding)
            # print('change:\n',change,)
            # print('\nor\n',change[0][0]['change'])
            if showIm:
                _bIm.show()
                input("showing image")
            _path = Graphics.getKeyDiagramPath(
                change=book[_changeNumber],
                diagramTypes=diagramTypes,
                resolution=resolution,
                includeFilename=False,
                greyScale=greyScale,
                invertColour=invertColour,
            )
            _filename = Graphics.getKeyDiagramPath(
                change=book[_changeNumber],
                diagramTypes=diagramTypes,
                resolution=resolution,
                greyScale=greyScale,
                invertColour=invertColour,
                includeFilename=True,
                includeGraphicsPath=False,
                includeSubdirectory=False,
            )
            Utility.makeDirectory(_path)
            # _bIm = _bIm.convert('P')
            _bIm.save(_path + _filename, format="png")
            print("saved {} to {}".format(_filename, _path.replace("/", "\\")))

            # _bIm.show()
        # print('diagramIms:\n{}\nmaxWidths: {}\npageHeight: {}'.format(
        # diagramIms,maxWidths,_pageHeight))
        # print('key:', key,
        #  '\npoly:', _poly, '\nt', _t, 'l', _l, 'b', _b, 'r', _r)

        Book.rootIsChangeOneForIndexing = _rootIsChangeOneForIndexingTemp

    @classmethod
    def multiFCircleImage(
        cls,
        changes: [[Change]],
        resolution,
        filename="multiFCircles",
        circleType="SCircle",
    ):
        if circleType == "SCircle":
            FCircle.setClassConstantsForSCircle()
        if type(changes) == Change:
            raise TypeError("supposed to be a list of lists of Change")
        if type(changes[0]) == Change:
            raise TypeError("supposed to be a list of lists of Change")
        _Lpad = int(resolution / math.pi**4)
        _Rpad = _Lpad
        _Tpad = int(resolution / math.pi**4)
        _Bpad = _Tpad

        _imW = (resolution + _Lpad + _Rpad) * max([len(i) for i in changes])
        _imH = (resolution + _Tpad + _Bpad) * len(changes)
        _imW = int(_imW)
        _imH = int(_imH)
        print(
            "changes", changes, _imW, _imH, "<- dimension", "len changes", len(changes)
        )
        # im = Image.new("RGBA", ((resolution + _Lpad + _Rpad) * len(changes[0]),
        #               (resolution + _Tpad + _Bpad) * len(changes)))
        im = Image.new("RGBA", (_imW, _imH), (0, 0, 0, 255))

        draw = ImageDraw.Draw(im)
        _y = _Tpad

        for row in tqdm(changes):
            _x = _Lpad
            for change in row:
                if change != None:
                    Graphics.pasteFCircleOnIm(
                        im,
                        (_x, _y, _x + resolution, _y + resolution),
                        change,
                        "C",
                        False,
                        True,
                        circleType=circleType,
                        filetype="pdf",
                    )
                _x += _Lpad + resolution + _Rpad
            _y += _Tpad + resolution + _Bpad
        _path = os.path.join(Graphics.directory, filename)
        print("saving multiFCircleImage to", _path + ".png")
        im.save(_path + ".png")
        if circleType == "SCircle":
            FCircle.setClassConstantsForFCircle()

    @classmethod
    def pasteFCircleOnIm(
        cls,
        im,
        xy,
        change: Change,
        key,
        greyScale,
        invertColour,
        circleType="FCircle",
        filetype="png",
    ):
        # input(xy)

        _T = xy[1]
        _L = xy[0]
        _B = xy[3]
        _R = xy[2]
        _width = int(_R - _L)

        if Graphics.seeIfDiagramExists(
            change,
            key,
            _width,
            greyScale=greyScale,
            invertColour=invertColour,
            impatientSkip=False,
            filetype=filetype,
            diagramType=circleType,
            showDebug=True,
        ):

            pass  # input('it is using png')
        else:  # FCircle does not exist
            print(
                "{} not found!. Making it.".format(
                    Graphics.getDiagramPath(
                        change,
                        key,
                        circleType,
                        _width,
                        greyScale=greyScale,
                        invertColour=invertColour,
                        filetype=filetype,
                    ).replace("/", "\\")
                )
            )
            Graphics.renderFCircle(
                change=change,
                resolution=_width,
                rootColourKey=key,
                saveOnlyOneKey=False,
                filetypes=[filetype],
                circleType=circleType,
            )
        if filetype == "png":
            _FCircle = Image.open(
                Graphics.getFCirclePath(
                    change,
                    key,
                    _width,
                    greyScale=greyScale,
                    invertColour=invertColour,
                    includeFilename=True,
                    filetype="png",
                    circleType=circleType,
                )
            ).convert("RGBA")
            # input(_FCircle)
        else:
            _FCircle = pdf2image.convert_from_path(
                Graphics.getFCirclePath(
                    change,
                    key,
                    _width,
                    greyScale=greyScale,
                    invertColour=invertColour,
                    includeFilename=True,
                    filetype=filetype,
                    circleType=circleType,
                ),
                size=_width,
            )[0].convert("RGBA")
            # input('{} {} '.format(_FCircle,_width))
        # input(im)
        # print(im.mode, _FCircle.mode, _L,_R,_T,_B)
        # input('hair we are')
        # im.show()
        im = im.paste(_FCircle, (int(_L), int(_T)), _FCircle)

    @classmethod
    def transposeColourSchemes(
        cls,
        im,
        path,
        keyOrig,
        keys: [] = Key.allFlats,
        transposeColourKey=False,
        showImage=False,
        returnAsPillowIm=False,
    ):
        path = path.replace("/", "\\")
        if "png" not in path:
            raise TypeError("asdf")
        _seperator = "\\"

        if not Graphics.directory in path:
            raise ValueError(
                "Check path again. Please supply absolute path. path = {}".format(path)
            )
        if not Graphics.colourDirectory in path:
            raise TypeError(
                "To get the colours right, function needs you to supply the coloured directory, not path = {}".format(
                    path
                )
            )
        if transposeColourKey == True:
            _keys = keys
        else:
            _keys = [keyOrig]
        _colours = Colour.getTransposedColours(
            colourTranspose=0, greyScale=False, invertColour=False
        )
        _coloursInv = Colour.getTransposedColours(
            colourTranspose=0, greyScale=False, invertColour=True
        )

        for k, key in enumerate(_keys):
            print("trasposing bitmap colours, key is", key)
            _colourTranspose = JazzNote.distanceFromC(key) - JazzNote.distanceFromC(
                keyOrig
            )
            for invertColour in (True, False):
                for greyScale in (True, False):
                    if not invertColour and not greyScale:
                        continue
                    _coloursNew = Colour.getTransposedColours(
                        colourTranspose=_colourTranspose,
                        greyScale=greyScale,
                        invertColour=invertColour,
                    )
                    _coloursNewInv = Colour.getTransposedColours(
                        colourTranspose=_colourTranspose,
                        greyScale=greyScale,
                        invertColour=not invertColour,
                    )
                    if not greyScale:
                        if not invertColour:
                            _graphicsDir = Graphics.colourDirectory
                        else:
                            _graphicsDir = Graphics.colourInvertedDirectory
                    else:
                        if not invertColour:
                            _graphicsDir = Graphics.greyscaleDirectory
                        else:
                            _graphicsDir = Graphics.greyscaleInvertedDirectory
                    _imNew = Graphics.changeColourSchemeOfImg(
                        im, _colours + _coloursInv, _coloursNew + _coloursNewInv
                    )
                    if invertColour:
                        _imNew = Graphics.changeColourSchemeOfImg(
                            _imNew,
                            [(0, 0, 0, 255), (255, 255, 255, 255)],
                            [(255, 255, 255, 255), (0, 0, 0, 255)],
                        )

                    _pathNew = path.replace(Graphics.colourDirectory, _graphicsDir)
                    _dirNew = _pathNew[: _pathNew.rfind(_seperator)]
                    if showImage:
                        print(_pathNew)
                        _imNew.show()
                    if os.path.isdir(_dirNew):
                        pass
                    else:
                        Utility.makeDirectory(_dirNew)
                        print("creating ", _dirNew)

                    _imNew = _imNew.convert("P", palette=Image.ADAPTIVE, colors=26)

                    _imNew.save(_pathNew)
                    print(
                        "saved transposition to file:///{}".format(
                            _pathNew.replace("\\", "/")
                        )
                    )
        print("..from original        file:///{}".format(path.replace("\\", "/")))

    @classmethod
    def fatLine(
        cls, im, line, outline, fill, thickness, outlineThickness=None, showDebug=False
    ):
        if showDebug:
            print("beginning", thickness, outlineThickness)

        if not outlineThickness is None:
            raise TypeError("asdlfkjas")
        if type(line) == list:
            if len(line) == 2:
                if len(line[0]) != 2:
                    raise ValueError("line is not set up right {}".format(line))
                x1 = line[0][0]
                y1 = line[0][1]
                x2 = line[1][0]
                y2 = line[1][1]
            if len(line) == 4:
                x1 = line[0]
                y1 = line[1]
                x2 = line[2]
                y2 = line[3]
        """x1 = int (x1)
        y1 = int (y1)
        x2 = int (x2)
        y2 = int (y2)"""
        draw = ImageDraw.Draw(im)

        o = x2 - x1
        a = y2 - y1
        h = abs(Graphics.distanceBetween(x1, y1, x2, y2))
        # if thickness is None:
        #    thickness = Trigram.lineProportion * h /3

        # compute angle
        a = math.atan((y2 - y1) / (x2 - x1))

        sin = math.sin(a)
        cos = math.cos(a)

        draw.line(
            [int(i) for i in [x1, y1, x2, y2]], fill=outline, width=int(thickness)
        )
        # makeShorter
        d = thickness / 4
        if x2 > x1:
            x1 += abs(cos * d)
            x2 -= abs(cos * d)
        else:
            x1 -= abs(cos * d)
            x2 += abs(cos * d)
        if y2 > y1:
            y1 += abs(sin * d)
            y2 -= abs(sin * d)
        else:
            y1 -= abs(sin * d)
            y2 += abs(sin * d)

        # y1 += sin * d
        # x2 -= cos *d
        # y2 -= sin * d
        draw.line(
            [int(i) for i in [x1, y1, x2, y2]], fill=fill, width=int(thickness / 3)
        )
        return 1
        angle3 = math.tan(o / a)
        angle2 = math.sin(o / h)
        # angle = math.cos(a/h)
        angle = math.radians(45)
        # input('angle {} angle2{} angle 3{} o {} a {} o/a P {}'.format(
        #   math.degrees(angle),math.degrees(angle2),math.degrees(angle3), o, a, o/a))

        # thickness = Trigram.lineProportion * h / 3

        outlineThickness = thickness / 4
        xdelta = sin * thickness / 2.0
        ydelta = cos * thickness / 2.0
        print("a is", math.degrees(a), "x delta", xdelta)

        xx1 = x1 - xdelta
        yy1 = y1 + ydelta
        xx2 = x1 + xdelta
        yy2 = y1 - ydelta
        xx3 = x2 + xdelta
        yy3 = y2 - ydelta
        xx4 = x2 - xdelta
        yy4 = y2 + ydelta
        if showDebug:
            print(
                "xx1 {} \nxx2 {} \nxx3 {} \nxx4 {} \nyy1 {} \nyy2 {} \nyy3 {} \nyy4 {}".format(
                    xx1, xx2, xx3, xx4, yy1, yy2, yy3, yy4
                )
            )

        draw.polygon((xx1, yy1, xx2, yy2, xx3, yy3, xx4, yy4), fill=outline)
        draw.line([xx1, yy1, xx2, yy2], fill=(0, 255, 0, 255))
        draw.line([xx1, yy1, xx4, yy4], fill=(0, 0, 255, 255))
        # draw.polygon((xx1, yy1, xx2, yy2, xx3, yy3, xx4, yy4),fill=(0,255,0,255))
        # print('thick {} linethick {}'.format(thickness,outlineThickness))
        print("sp.angle", math.degrees(angle))
        if x2 > x1:
            x1 += abs(outlineThickness * 2 * sin)
            x2 -= abs(outlineThickness * 2 * cos)
        else:
            x1 -= abs(outlineThickness * 2 * cos)
            x2 += abs(outlineThickness * 2 * sin)
        if y2 > y1:
            y1 += abs(outlineThickness * 2 * cos)
            y2 -= abs(outlineThickness * 2 * sin)
        else:
            y1 -= abs(outlineThickness * 2 * sin)
            y2 += abs(outlineThickness * 2 * cos)

        xdelta = sin * (outlineThickness) / 2
        ydelta = cos * (outlineThickness) / 2
        xx1 = x1 - xdelta
        yy1 = y1 + ydelta
        xx2 = x1 + xdelta
        yy2 = y1 - ydelta
        xx3 = x2 + xdelta
        yy3 = y2 - ydelta
        xx4 = x2 - xdelta
        yy4 = y2 + ydelta
        draw.polygon((xx1, yy1, xx2, yy2, xx3, yy3, xx4, yy4), fill=fill)
        # draw.polygon((xx1, yy1, xx2, yy2, xx3, yy3, xx4, yy4),fill=(0,0,255,255))

    def quantizetopalette(silf, palette, dither=False):
        """Convert an RGB or L mode image to use a given P image's palette."""

        silf.load()

        # use palette from reference image made below
        palette.load()
        im = silf.im.convert("P", 0, palette.im)
        # the 0 above means turn OFF dithering making solid colors
        return silf._new(im)

    """for imgfn in sys.argv[1:]:
        palettedata = [0, 0, 0, 255, 0, 0, 255, 255, 0, 0, 255, 0, 255, 255, 255, 85, 255, 85, 255, 85, 85, 255, 255,
                       85]

        #   palettedata = [ 0, 0, 0, 0,170,0, 170,0,0, 170,85,0,] # pallet 0 dark
        #   palettedata = [ 0, 0, 0, 85,255,85, 255,85,85, 255,255,85]  # pallet 0 light

        #   palettedata = [ 0, 0, 0, 85,255,255, 255,85,255, 255,255,255,]  #pallete 1 light
        #   palettedata = [ 0, 0, 0, 0,170,170, 170,0,170, 170,170,170,] #pallete 1 dark
        #   palettedata = [ 0,0,170, 0,170,170, 170,0,170, 170,170,170,] #pallete 1 dark sp

        #   palettedata = [ 0, 0, 0, 0,170,170, 170,0,0, 170,170,170,] # pallet 3 dark
        #   palettedata = [ 0, 0, 0, 85,255,255, 255,85,85, 255,255,255,] # pallet 3 light

        #  grey  85,85,85) blue (85,85,255) green (85,255,85) cyan (85,255,255) lightred 255,85,85 magenta (255,85,255)  yellow (255,255,85)
        # black 0, 0, 0,  blue (0,0,170) darkred 170,0,0 green (0,170,0)  cyan (0,170,170)magenta (170,0,170) brown(170,85,0) light grey (170,170,170)
        #
        # below is the meat we make an image and assign it a palette
        # after which it's used to quantize the input image, then that is saved
        palimage = Image.new('P', (16, 16))
        palimage.putpalette(palettedata * 32)
        oldimage = Image.open(sys.argv[1])
        oldimage = oldimage.convert("RGB")
        newimage = quantizetopalette(oldimage, palimage, dither=False)
        dirname, filename = os.path.split(imgfn)
        name, ext = os.path.splitext(filename)
        newpathname = os.path.join(dirname, "cga-%s.png" % name)
        newimage.save(newpathname)

    #   palimage.putpalette(palettedata *64)  64 times 4 colors on the 256 index 4 times, == 256 colors, we made a 256 color pallet."""

    @classmethod
    def quantizeColourScheme(cls, colours, quantize=1):
        """Returns an array of colourSchemes of various luminosities
        If quantize == 1 nothing happens so increase it."""
        quantizedSchemes = []
        usingAlpha = len(colours[0]) == 4
        for colour in colours:

            r = colour[0]
            g = colour[1]
            b = colour[2]
            if usingAlpha:
                a = colours[3]
            for q in range(quantize):
                shift = round(256 / max(q, 1))
                if usingAlpha == 4:

                    quantizedSchemes.append(
                        (
                            (r + shift) % 256,
                            (g + shift) % 256,
                            (b + shift) % 256,
                            (a + shift) % 256,
                        )
                    )
                else:
                    quantizedSchemes.append(
                        ((r + shift) % 256, (g + shift) % 256, (b + shift) % 256)
                    )
        return quantizedSchemes

    @classmethod
    def getColoursInImg(
        cls,
        im,
    ) -> [(int, int, int)]:
        """Returns each RGB value used in Pil.im"""
        colours = []
        RGBAs = np.unique(img.reshape(-1, img.shape[2]), axis=0)
        RGBAsUnique = RGBAs[:, :3:]
        return RGBAsUnique

    @classmethod
    def shiftKeyOfImg(cls, im, transpositionSteps=[7]):
        margin = 0.02
        img = np.array(im)  # "data" is a height x width x 4 numpy array
        # https://stackoverflow.com/questions/24780697/numpy-unique-list-of-colors-in-the-image
        time = datetime.datetime.now()
        print("{} finding unique colours in im. takes a bit.".format(time))
        imRGBAs = np.unique(img.reshape(-1, img.shape[2]), axis=0)
        imRGBDupes = imRGBAs.tolist()
        imRGBDupes = [i[:3] for i in imRGBDupes]
        imRGBs = []
        for i in imRGBDupes:
            if i not in imRGBs:
                imRGBs.append(i)

        print(
            "{} done that... creating palette transpositions.".format(
                datetime.datetime.now()
            )
        )

        colourPalette = Colour.getTransposedColours(
            colourTranspose=0,
        )
        hsvPalette = [
            colorsys.rgb_to_hsv(i[0] / 255.0, i[1] / 255.0, i[2] / 255.0)
            for i in colourPalette
        ]

        for transposition in transpositionSteps:
            paletteDestinations = Colour.getTransposedColours(
                colourTranspose=transposition,
            )
            hsvDestinations = [
                colorsys.rgb_to_hsv(i[0] / 255.0, i[1] / 255.0, i[2] / 255.0)
                for i in colourPalette
            ]
            srcColours = []
            dstColours = []
            colourCoordinates = []
            output = img.copy()
            for colourIdx, colour in enumerate(imRGBs):
                r, g, b = colour[0], colour[1], colour[2]
                h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
                for paletteIdx, preset in enumerate(hsvPalette):
                    print(".", end="")
                    if preset[0] - margin < h < preset[0] + margin:
                        hueDifference = (
                            hsvPalette[(paletteIdx + transposition) % 12][0]
                            - hsvPalette[paletteIdx][0]
                        )
                        sR, sG, sB, = (
                            colour[0],
                            colour[1],
                            colour[2],
                        )

                        sH, sS, sV = colorsys.rgb_to_hsv(
                            sR / 255.0, sG / 255.0, sB / 255.0
                        )
                        dR, dG, dB = colorsys.hsv_to_rgb(
                            (h + hueDifference) % 1, sS, sV
                        )
                        dR *= 255
                        dG *= 255
                        dB *= 255
                        if (sR, sG, sB) not in srcColours:
                            # np.append(srcColours,(sR,sG,sB),axis=-1)
                            # np.append(dstColours,(dR,dG,dB),axis=-1)
                            srcColours.append((sR, sG, sB))
                            dstColours.append((dR, dG, dB))
                            print(
                                "srcColours.append({})\ndstColours.append({})".format(
                                    srcColours[-1], dstColours[-1]
                                )
                            )

                            # indices = np.nonzero(img[:,:,:3] == srcColours[-1])
                            # valid = np.all(img[:,:,:3] == [sR, sG, sB], axis=-1)
                            # indices = np.nonzero(valid)

                            # indices = np.where(np.all(img == srcColours[-1],axis=-1)[0][0])
                            # if len(indices) >= 1:

                            # coordinates = list(zip(indices[0], indices[1]))

                            # colourCoordinates.append(list(set(list(coordinates))))

                            # rs, cs = valid.nonzero()
                            print(
                                "paletteIdx {}/{} {} [{}]/{} {}".format(
                                    paletteIdx,
                                    len(hsvPalette),
                                    colour,
                                    colourIdx,
                                    len(imRGBs),
                                    transposition,
                                )
                            )
                            # red, green, blue, alpha = output.T  # Temporarily unpack the bands for readability

                            # Replace white with red... (leaves alpha values alone...)
                            # white_areas = (red == r) & (blue == g) & (green == b)
                            # output[..., :-1][white_areas.T] = (dR,dG,dB,)  # Transpose back needed
                            # output[..., :-1][valid] = (dR,dG,dB,)
            """for coordIdx,coordinates in enumerate(colourCoordinates):
                coordinatesLength = len(coordinates)
                dstColour = dstColours[coordIdx]
                for cellIdx, cell in enumerate(coordinates):
                    row, col = cell[0], cell[1]
                    output[row][col] = dstColour + (img[row][col][3],)"""
            # print('{}  {}/{}: x:{} y:{}'.format(cellIdx, coordinatesLength,coordIdx, len(colourCoordinates), col, row))
        # print('converting numpy array to pil image. And..',end='')
        #  output = Image.fromarray(output)
        #  print('done.')
        #  output.show()

        srcColoursCopy = [i for i in srcColours]
        dstColoursCopy = [i for i in dstColours]
        srcColours, dstColours = [], []
        for i in range(len(srcColoursCopy)):
            if srcColoursCopy[i] not in srcColours:
                srcColours.append(srcColoursCopy[i])
                dstColours.append(dstColoursCopy[i])

        # print('{} changing colours in img... {} srcColours to change.{}\nThey wil change to {}'.format(datetime.datetime.now(),len(srcColours),srcColours,dstColours),end=' ')
        im = Graphics.changeColourSchemeOfImg(
            im, colours=srcColours, newColours=dstColours
        )
        # print('{} done'.format(datetime.datetime.now()))
        # im.show()
        # input('hmmmm')

        # https://stackoverflow.com/questions/24874765/python-pil-shift-the-hue-and-saturation
        # ld = im.load()
        # width, height = im.size
        """for y in range(height):
            for x in range(width):
                r, g, b = ld[x, y]
                h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
                h = (h + -90.0 / 360.0) % 1.0
                s = s ** 0.65
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                #ld[x, y] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999))"""

        # https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color/3753428#3753428

        # red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        # white_areas = (red == 255) & (blue == 255) & (green == 255)
        # data[..., :-1][white_areas.T] = (255, 0, 0)  # Transpose back needed
        # output[..., :-1][valid] = (dR, dG, dB,)
        # im2 = Image.fromarray(output)
        # im2.show()
        # input('end of shiftKeyOfImg')

    @classmethod
    def changeColourSchemeOfImg(cls, im, colours, newColours):
        # https://stackoverflow.com/questions/6483489/change-the-color-of-all-pixels-with-another-color

        # print('changing ',len(colours),'colours to ',len(newColours))
        # print('colours\n',colours)
        # print('newColours\n',newColours)
        data = np.array(im)
        newData = np.array(im)
        # r1, g1, b1 = 0, 0, 0  # Original value
        # r2, g2, b2 = 255, 255, 255  # Value that we want to replace it with
        """if colours == newColours:
            raise TypeError ('the colours are equal, \n{} \n{}'.format(
                colours, newColours
            ))"""
        if len(colours) != len(newColours):
            raise TypeError("the colours have unequal length")
        for i, c in enumerate(colours):
            print(".", end="")
            newC = newColours[i]
            r1, g1, b1 = c[0], c[1], c[2]  # Original value
            r2, g2, b2 = newC[0], newC[1], newC[2]
            red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
            mask = (red == r1) & (green == g1) & (blue == b1)
            newData[:, :, :3][mask] = [r2, g2, b2]
        im = Image.fromarray(newData)
        return im

    @classmethod
    def ellipse(cls, im, xy, fill, outline, width: int, constrainSize=False):
        """provide xy as list in form [x1,y1,x2,y2]"""
        try:
            draw = ImageDraw.Draw(im)
        except:
            raise TypeError("Holy fuck shit")

        x1 = min(xy[0], xy[2])
        x2 = max(xy[0], xy[2])
        y1 = min(xy[1], xy[3])
        y2 = max(xy[1], xy[3])

        if constrainSize:
            draw.ellipse((x1, y1, x2, y2), fill=outline)

            draw.ellipse((x1 + width, y1 + width, x2 - width, y2 - width), fill=fill)
        else:
            draw.ellipse((x1 - width, y1 - width, x2 + width, y2 + width), fill=outline)
            draw.ellipse((x1, y1, x2, y2), fill=fill)

        # return im

    @classmethod
    def drawFatPolygonToIm(cls, im, poly, outline, width):

        _draw = ImageDraw.Draw(im)
        _polyTuples = []
        _ellipseSize = width / 2.0
        if type(poly[0]) == int:
            # Its a list of coordinates like [0,3,2,3..]
            for i in range(0, len(poly), 2):
                _polyTuples.append((poly[i], poly[i + 1]))
        elif type(poly[0]) == tuple:
            _polyTuples = poly
        elif type(poly[0]) == list:
            if len(poly[0]) == 2:
                for i in poly:
                    _polyTuples.append((i[0], i[1]))

        if len(_polyTuples) != (len(poly) / 2):
            pass  # raise TypeError('asdfsadafsd {} {}\n{} {}'.format(len(poly),poly,len(_polyTuples),_polyTuples))
        # input('poly {} {}'.format(poly,_polyTuples))

        # input('outline {} poly {}'.format(outline, _polyTuples))
        if len(_polyTuples) != 0 and _polyTuples[-1] != _polyTuples[0]:
            _polyTuples.append(_polyTuples[0])
        _draw.line(_polyTuples, fill=(outline), width=width)

        for point in _polyTuples:
            _draw.ellipse(
                (
                    point[0] - _ellipseSize,
                    point[1] - _ellipseSize,
                    point[0] + _ellipseSize,
                    point[1] + _ellipseSize,
                ),
                fill=outline,
            )

        return im

    @classmethod
    def getCircleFilename(
        cls,
        change: Change,
        colourKey: str,
        resolution: int,
        invertColour: bool,
        greyScale: bool,
        circleType="FCircle",
        filetype="png",
        includeFileExtension=True,
    ):

        key = JazzNote.makeAlphabetNoteUseSingleFlats((colourKey))
        if circleType not in FCircle.validTypes:
            raise TypeError(
                "{} not in FCircle.validTypes {}".format(circleType, FCircle.validTypes)
            )

        if includeFileExtension:
            extension = "." + filetype.lower()
        else:
            extension = ""
        return (
            circleType
            + "_"
            + str(change.getChangeNumber(decorateChapter=False, addOneToBookPage=True))
            + extension
        )

    @classmethod
    def getOldCirclePath(cls, change: Change):
        if change.getChangeNumber() <= 1:
            return "F:\\Backups\\wayOfChange backups\\Circles\\8192 px\\G\\Circle {} in G.png".format(
                str(change.getChangeNumber())
            )
        else:
            return "F:\\Backups\\wayOfChange backups\\Circles\\8192 px\\G\\Circle no {}.png".format(
                str(change.getChangeNumber())
            )

    @classmethod
    def getFCirclePath(
        cls,
        change: Change,
        colourKey: str,
        resolution: int,
        invertColour=False,
        greyScale=False,
        includeFilename=False,
        pathSeperator="/",
        includeGraphicsPath=True,
        externalGraphicsPath=False,
        circleType="FCircle",
        filetype="png",
        censorPng=False,
        includeFileExtension=True,
    ):

        if censorPng and filetype == "png":
            raise TypeError("changing these to pdf")
        if circleType not in FCircle.validTypes:
            raise TypeError(
                "{} not in FCircle.validTypes {}".format(circleType, FCircle.validTypes)
            )
        if change.__class__.__name__ != 'Change':
            raise TypeError(
                "{} should be of type Change, not {}".format(change, type(change))
            )
        if not JazzNote.isAlphabetNoteStr(colourKey):
            raise ValueError("{} should be an alphabet-note. ".format(colourKey))
        change = change.removeDuplicateNotes(octaveLimit=1)
        change = change.sortBySemitonePosition()
        if not invertColour:
            if not greyScale:
                if circleType == "FCircle":
                    _dir = Graphics.fCirclesDirectory
                elif circleType == "SCircle":
                    _dir = Graphics.sCirclesDirectory
                elif circleType == "PCircle":
                    _dir = Graphics.pCirclesDirectory
            else:
                if circleType == "FCircle":
                    _dir = Graphics.fCirclesBWDirectory
                elif circleType == "SCircle":
                    _dir = Graphics.sCirclesBWDirectory
                elif circleType == "PCircle":
                    _dir = Graphics.pCirclesBWDirectory
        elif invertColour:
            if not greyScale:
                if circleType == "FCircle":
                    _dir = Graphics.fCirclesInvDirectory
                elif circleType == "SCircle":
                    _dir = Graphics.sCirclesInvDirectory
                elif circleType == "PCircle":
                    _dir = Graphics.pCirclesInvDirectory
            else:
                if circleType == "FCircle":
                    _dir = Graphics.fCirclesBWInvDirectory
                elif circleType == "SCircle":
                    _dir = Graphics.sCirclesBWInvDirectory
                elif circleType == "PCircle":
                    _dir = Graphics.pCirclesBWInvDirectory




        if includeGraphicsPath:
            _path = _dir
            if externalGraphicsPath:
                _path = _path.replace(Graphics.directory, Graphics.directoryExternal)
        else:
            _path = _dir.replace(Project.directoryGraphics,'')


        if circleType == "PCircle" and filetype in Graphics.vectorFiletypes:
            resolution = 64
        _path = os.path.join(_path,Graphics.getFiletypeResolutionFolderName(
            filetype=filetype, resolution=resolution
        ))
        _path = _path.replace("FCircle", circleType)

        _path = os.path.join(_path,os.path.join(_path,colourKey))

        if includeFilename == True:
            _path = os.path.join(_path,Graphics.getCircleFilename(
                change,
                colourKey,
                resolution,
                invertColour=invertColour,
                greyScale=greyScale,
                circleType=circleType,
                filetype=filetype,
                includeFileExtension=includeFileExtension,
            ))
        _path = _path.replace("\\", pathSeperator)
        _path = _path.replace("/", pathSeperator)

        # input(Utility.printPrettyVars(_path,circleType))


        return _path

    @classmethod
    def renderDiagram(
        cls,
        change: Change,
        key: str,
        resolution: int,
        greyScale: bool,
        invertColour: bool,
        diagramType="FCircle",
        filetypes=["pdf"],
        externalGraphicsPath=False,
        showDebug=False,
    ):
        params = dict(locals())

        if diagramType in ("FCircle","SCircle"):
            renderFunc = Graphics.renderFCircle
        elif diagramType in ("Piano", "PianoThirds"):
            renderFunc = Piano().makePianoFiles
        elif diagramType == "PCircle":
            renderFunc = Graphics.renderPCircle
        elif diagramType in NGramGraphic.validTypes:
            renderFunc = NGramGraphic(nGramType=diagramType).renderFiles
        elif diagramType in Fretboard.instruments:
            renderFunc = Fretboard(instrument=diagramType).renderFretboards
        elif diagramType == "Accordion":
            renderFunc = Accordion.renderAccordion
        elif diagramType == 'ChordsOfChange':
            renderFunc = Project.renderCondensedChange
        else:
            raise ValueError(
                "Unsupported diagramType in Graphics.renderDiagram()\nadd the diagram type here. diagramType == '{}'".format(diagramType)
            )




        import inspect
        renderParams = [str(p) for p in inspect.signature(renderFunc).parameters]

        rootKeyVarName = False
        pluralsToSingulars = []
        singularsToPlurals = []
        for p in renderParams:
            if "key" in p.lower() and p not in ("key", "makeAllKeys", "saveOnlyOneKey"):
                rootKeyVarName = p

            if p[-1] == "s" and p[:-1] in params:
                params[p] = [params[p[:-1]]]
                pluralsToSingulars.append(p)
            if (p + "s") in params:
                print(params[p + "s"])
                input('here params[p] == params[p])')
                params[p + "s"] = params[p]

        if len(pluralsToSingulars):
            pass

        if rootKeyVarName:
            if "keys" in rootKeyVarName:
                params[rootKeyVarName] = [key]
            else:
                params[rootKeyVarName] = key

        if "key" not in renderParams:
            params.__delitem__("key")

        # input()
        unusedParams = {p: params[p] for p in params if p not in renderParams}
        renderParams = {p: params[p] for p in params if p in renderParams}
        if diagramType == 'SCircle':
            renderParams['circleType'] = 'SCircle'
        elif diagramType == 'PianoThirds':
            renderParams['voicingType'] = 'Thirds'


        # renderParams.__delitem__('cls')
        print(
            "Did not use these paramters: {}\nrunning the thing\n{}.{}".format(
                unusedParams, renderFunc.__name__, renderParams
            )
        )

        print("renderFunc", str(renderFunc))
        print("renderParams", str(renderParams))
        print("unusedParams", str(unusedParams))
        print("params", str(params))
        renderFunc(**renderParams)
        try:
            renderFunc(**renderParams)
        except TypeError as e:
            print("attemp unsuccessful")

            raise TypeError(e)

    @classmethod
    def seeIfDiagramExists(
        cls,
        change: Change,
        key: str,
        resolution: int,
        greyScale,
        invertColour,
        diagramType="FCircle",
        filetype="png",
        externalGraphicsPath=False,
        impatientSkip=False,
        renderIfNotFound=True,
        showDebug=False,
    ) -> str:
        if showDebug:
            if impatientSkip:
                print(
                    "not seeing if Diagram exists",
                    change,
                    key,
                    resolution,
                    "in path. (impatient) "
                    + Graphics.getDiagram(
                        change,
                        key,
                        resolution,
                        diagramType="FCircle",
                        filetype=filetype,
                        includeFilename=True,
                    ),
                )
            else:
                print(
                    "seeing if Diagram exists",
                    change,
                    key,
                    resolution,
                    diagramType,
                    filetype,
                    "in path. "
                    + Graphics.getDiagramPath(
                        change,
                        key,
                        resolution=resolution,
                        diagramType=diagramType,
                        filetype=filetype,
                        includeFilename=True,
                    ),
                )

        path = Graphics.getDiagramPath(
            change=change,
            key=key,
            resolution=resolution,
            includeFilename=True,
            greyScale=greyScale,
            invertColour=invertColour,
            diagramType=diagramType,
            filetype=filetype,
            includeGraphicsPath=True,
            externalGraphicsPath=externalGraphicsPath,
            includeFileExtension=True,
        )
        path = os.path.abspath(path)
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            return path
        elif renderIfNotFound:
            input("graphic not found so rendering {} {}, because {} isfile =={} or its size is zero.\n{}".format(
                change,change.getChangeNumber(), path, os.path.isfile(path),
                r"C:\Users\Ed\wayOfChange\Graphics\Col\PCircle\pdf_64px\C")
            )
            assert externalGraphicsPath == False
            Graphics.renderDiagram(
                change=change,
                key=key,
                resolution=resolution,
                greyScale=greyScale,
                invertColour=invertColour,
                diagramType=diagramType,
                filetypes=[filetype],
                externalGraphicsPath=externalGraphicsPath,
                showDebug=showDebug,
            )
            if os.path.isfile(path) and os.path.getsize(path) > 0:
                return path
            else:
                raise TypeError(
                    "Something went wrong because {} does not exist.".format(path)
                )

        else:
            return False

    @classmethod
    def makeColourTransposedImage(cls, im, colourShift=1):

        im = im.convert("RGBA")

        data = np.array(im)  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = (255, 0, 0)  # Transpose back needed

        im2 = Image.fromarray(data)
        im2.show()

    @classmethod
    def getTShirtPath(
        cls,
        change: Change,
        rootKey="C",
        filetype="png",
        frontSide=True,
        canvasWidth=1,
        canvasHeight=1,
        invertColour=False,
        designType="default",
    ):
        shirtTypes = {
            (3600, 4500): {"filename": "GildanT"},
            (4204, 4795): {
                "filename": "JerseyTank",
                "Printify Item": "Women's Relaxed Jersey Tank Top",
            },
            (4500, 5090): {"filename"},
        }

        if designType == "default":
            productType = "TShirt"
        if (canvasWidth, canvasHeight) in shirtTypes.keys():
            filename = shirtTypes[(canvasWidth, canvasHeight)]["filename"]

        return os.path.join(Graphics.directoryExternal,'TShirt',productType + "_" + str(change.getChangeNumber()) + "_" + str(rootKey) + "_" + "_" + str(canvasWidth) + "x" + str(canvasHeight) + "_" + ("front" if frontSide else "back") + "." + filetype)
        #return (  + "TShirt\\" + productType + "_" + str(change.getChangeNumber()) + "_" + str(rootKey) + "_" + "_" + str(canvasWidth) + "x" + str(canvasHeight) + "_" + ("front" if frontSide else "back") + "." + filetype        )'

    @classmethod
    def renderTShirts(
        cls,
        changeRange: [int],
        rootKeys=["C"],
        designType="default",
        changeNumberFont="iomanoid.ttf",
        scaleNameFont="BadMofo.ttf",
        chordQualityFont="JAZZTEXT.ttf",
        signatureFont="BohemianTypewriter.ttf",
        hexagramStoryFont="MelancholySerif-zoGL.otf",
        fastMode=False,
        HDassets=False,
        tShirtWays=None,
        canvasWidth=3600,
        canvasHeight=4500,
        bgColour=[255, 255, 255, 0],
        makeFront=True,
        makeBack=False,
        makeCornerSmallCircles=True,
        drawHexagramSymbols=True,
    ):

        canvasWidth = 3600
        canvasHeight = 4800  # 4800 3600x4659 = 8.5 / 11
        # canvasWidth = 4204
        # canvasHeight = 4795
        smallCircles = 12
        smallCircleWidth = canvasWidth / smallCircles
        changeNumberFontSize = canvasWidth / 10
        changeNumberFont = ImageFont.truetype(
            os.path.join(Project.directory, changeNumberFont), round(changeNumberFontSize)
        )
        chordQualityFontSize = canvasWidth / 10
        chordQualityFont = ImageFont.truetype(
            os.path.join(Project.directory,chordQualityFont), round(chordQualityFontSize)
        )
        scaleNameFontSize = canvasWidth / 10
        scaleNameFont = ImageFont.truetype(
            os.path.join(Project.directory, scaleNameFont), round(scaleNameFontSize)
        )
        signatureFontSize = canvasWidth / 56
        signatureFont = ImageFont.truetype(
            os.path.join(Project.directory, signatureFont), round(signatureFontSize)
        )
        signatureText = "©Édrihan Lévesque"
        hexagramStoryFontSize = signatureFontSize = canvasWidth / 68
        hexagramStoryFont = ImageFont.truetype(
            os.path.join(Project.directory, hexagramStoryFont), round(hexagramStoryFontSize)
        )

        def insertSmallCircle(
            change, rootKey, colourInversion, resolution, circleType="FCircle"
        ):
            functionParams = locals().copy()
            try:
                insertSmallCircle.smallCircleRenders
            except AttributeError:
                insertSmallCircle.smallCircleRenders = {}

            multiFCirclePrimes = Graphics.getDiagramPath(
                change=change,
                key="C",
                diagramType="FCircle",
                resolution=4096,
                invertColour=invertColour,
                pathSeperator="\\",
                includeFileExtension=True,
            )
            smallCircleKey = Graphics.getDiagramPath(
                change=change,
                key=rootKey,
                diagramType="FCircle",
                resolution=4096,
                invertColour=invertColour,
                pathSeperator="\\",
                includeFileExtension=True,
            )
            if smallCircleKey in insertSmallCircle.smallCircleRenders.keys():
                return insertSmallCircle.smallCircleRenders[smallCircleKey]
            elif circlePath in insertSmallCircle.smallCircleRenders:
                # Colour transpose here
                return insertSmallCircle.smallCircleRenders[smallCircleKey]
            else:  # hasn't been rendered yet

                print(
                    "converting vector to bitmap for {} just because hasnt been rendered yet;0".format(
                        fCirclePath.replace("\\", "/")
                    )
                )
                insertSmallCircle.smallCircleRenders[
                    circlePath + "@" + str(resolution)
                ] = pdf2image.convert_from_path(
                    fCirclePath,
                    dpi=300,
                    size=(canvasWidth, canvasWidth),
                    single_file=True,
                    transparent=True,
                    use_pdftocairo=True,
                )[
                    0
                ]
                # input('hey hey hey hye ' + str(insertSmallCircle.smallCircleRenders))
                if rootKey == "C":
                    return insertSmallCircle.smallCircleRenders[
                        circlePath + "@" + str(resolution)
                    ]
                else:
                    insertSmallCircle(**functionParams)

        for changeNumber in changeRange:
            change = Change.makeFromChangeNumber(changeNumber)
            for invertColour in (False, True):
                if not invertColour:
                    inkColour = (255, 255, 255)
                    inkColourInv = (0, 0, 0)
                else:
                    inkColour = (0, 0, 0)
                    inkColourInv = (255, 255, 255)

                if tShirtWays == None:
                    tShirtWays = Book.tShirtWays

                scalename = str(
                    Utility.removeAccentsFromText(
                        change.getScaleNames(
                            replaceCarnaticNamesWithSymbols=False,
                            replaceDirectionStrWithUnicode=False,
                            rebindRootToNextNoteIfNoOne=False,
                        )[0]
                    )
                )
                hexagramname = Utility.removeAccentsFromText(
                    " ".join(change.getHexagram(["name"]))
                )
                hexagramStory1Text = change.getHexagram(["story"])[0]
                hexagramStory2Text = change.getHexagram(["story"])[1]

                # "C:\\Users\\Ed\\wayOfChange\\Graphics\\Col\\FCircle\\pdf_2048px\\C\\FCircle_2048.pdf"
                for rootKey in rootKeys:
                    coloursOrig = (
                        Colour.getTransposedColours(
                            colourTranspose=0,
                            greyScale=False,
                            invertColour=False,
                        )
                        + Colour.getTransposedColours(
                            colourTranspose=0,
                            greyScale=False,
                            invertColour=True,
                        )
                        + Colour.getTransposedColours(
                            colourTranspose=Key.distanceFromC(Key(rootKey)),
                            greyScale=False,
                            neutralColours=True,
                        )
                    )
                    coloursTrans = (
                        Colour.getTransposedColours(
                            colourTranspose=Key.distanceFromC(Key(rootKey)),
                            greyScale=False,
                            invertColour=False,
                        )
                        + Colour.getTransposedColours(
                            colourTranspose=Key.distanceFromC(Key(rootKey)),
                            greyScale=False,
                            invertColour=True,
                        )
                        + Colour.getTransposedColours(
                            colourTranspose=Key.distanceFromC(Key(rootKey)),
                            greyScale=False,
                            neutralColours=True,
                        )
                    )
                    print(
                        "making TShirt {}{} for {}".format(
                            rootKey, str(change.getChangeNumber()), str(change)
                        )
                    )
                    if makeFront:
                        tShirtPathFront = Graphics.getTShirtPath(
                            change=change,
                            rootKey="C",
                            frontSide=True,
                            canvasWidth=canvasWidth,
                            canvasHeight=canvasHeight,
                            designType=designType,
                        )
                        imFront = Image.new(
                            "RGBA", (canvasWidth, canvasHeight), (0, 255, 0, 0)
                        )
                        imFrontDraw = ImageDraw.Draw(imFront)
                    if makeBack:
                        tShirtPathBack = Graphics.getTShirtPath(
                            change=change,
                            rootKey="C",
                            frontSide=False,
                            canvasWidth=canvasWidth,
                            canvasHeight=canvasHeight,
                            designType=designType,
                        )
                        imBack = Image.new(
                            "RGBA", (canvasWidth, canvasHeight), (0, 255, 0, 0)
                        )
                        imBackDraw = ImageDraw.Draw(imBack)

                    """pdf2image.convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, 
                    last_page=None, fmt='ppm', jpegopt=None, thread_count=1, userpw=None, 
                    use_cropbox=False, strict=False, transparent=False, single_file=False, 
                    output_file=str(uuid.uuid4()), poppler_path=None, grayscale=False, 
                    size=None, paths_only=False, use_pdftocairo=False, timeout=600)"""

                    """    Syntax: obj.text( (x,y), Text, font, fill)
            
                Parameters: 
            
                    (x, y): This X and Y denotes the starting position(in pixels)/coordinate of adding the text on an image.
                    Text: A Text or message that we want to add to the Image.
                    Font: specific font type and font size that you want to give to the text.
                    Fill: Fill is for to give the Font color to your text."""

                    """images = convert_from_bytes(open(fCirclePath, 'rb').read(),
                                dpi = 300, transparent=True, size = (canvasWidth, canvasWidth)
                    )"""

                    if not change == Change([]):
                        pass
                        # oldCircle = Image.open(Graphics.getOldCirclePath(change))
                        # oldCircle = oldCircle.resize(size=(canvasWidth, canvasWidth), resample=Image.LANCZOS)

                    # imFrontDraw.text((0, canvasWidth), str(change.getChangeNumber()), font=changeNumberFont, fill=(0, 0, 0))

                    if scalename == hexagramname:
                        scalename = change.getWord()
                    if makeFront:
                        frontTextLine1 = hexagramname
                        frontTextLine1Font = scaleNameFont
                        frontTextLine1Width = frontTextLine1Font.getsize(
                            frontTextLine1
                        )[0]
                        frontTextLine1Height = frontTextLine1Font.getsize(
                            frontTextLine1
                        )[1]
                        # imFrontDraw.text((canvasWidth / 2, canvasWidth + (changeNumberFontSize - scaleNameFontSize)), hexagramname,
                        imFrontDraw.text(
                            (canvasWidth / 2, 0),
                            frontTextLine1,
                            font=frontTextLine1Font,
                            color=inkColour,
                            fill=inkColourInv,
                            anchor="ma",
                        )
                    if makeBack:
                        backTextLine1 = scalename
                        backTextLine1Font = scaleNameFont
                        imBackDraw.text(
                            (
                                canvasWidth / 2,
                                canvasWidth
                                + (changeNumberFontSize - scaleNameFontSize),
                            ),
                            backTextLine1,
                            font=backTextLine1Font,
                            color=inkColour,
                            fill=inkColourInv,
                            anchor="ma",
                        )
                        imBackDraw.text(
                            (0, canvasWidth),
                            str(change.getChangeNumber()),
                            font=changeNumberFont,
                            color=inkColour,
                            fill=inkColourInv,
                        )

                        backTextLine1Height = backTextLine1Font.getsize(backTextLine1)[
                            1
                        ]

                    if not fastMode:
                        if makeFront:
                            y1 = canvasWidth + frontTextLine1Height
                        if makeBack:
                            y1 = canvasWidth + backTextLine1Height
                        y2 = y1 + smallCircleWidth
                        y3 = y1 + 2 * smallCircleWidth
                        y1 = round(y1)
                        y2 = round(y2)
                        y3 = round(y3)

                        if makeBack:
                            fCirclePath = Graphics.getDiagramPath(
                                change=change,
                                key=rootKey,
                                diagramType="FCircle",
                                resolution=4096,
                                invertColour=invertColour,
                                pathSeperator="\\",
                                includeFileExtension=True,
                            )
                            print(
                                "converting vector to bitmap for {}".format(fCirclePath)
                            )
                            if os.path.isfile(fCirclePath):
                                imagesFCircle = pdf2image.convert_from_path(
                                    fCirclePath,
                                    dpi=300,
                                    size=(canvasWidth, canvasWidth),
                                    single_file=True,
                                    transparent=True,
                                    use_pdftocairo=True,
                                )
                                imBack.paste(imagesFCircle[0], (0, 0))
                                # hexagram story

                            # signature
                            imBackDraw.text(
                                (canvasWidth, y1),
                                signatureText,
                                font=signatureFont,
                                color=inkColour,
                                fill=inkColourInv,
                                anchor="rm",
                            )
                        if makeFront:
                            sCirclePath = Graphics.getDiagramPath(
                                change=change,
                                key="C",
                                diagramType="SCircle",
                                resolution=2**12,
                                pathSeperator="\\",
                                includeFileExtension=True,
                            )
                            print(
                                "big graphic.. converting vector to bitmap for file:///{}".format(
                                    sCirclePath.replace("\\", "/")
                                )
                            )
                            """imagesSCircle = pdf2image.convert_from_path(sCirclePath,
                                                              dpi=300, size=(canvasWidth, canvasWidth), single_file=True,
                                                              transparent=True, use_pdftocairo=True
                                                              )"""

                            imageSCircle = insertSmallCircle(
                                change,
                                rootKey,
                                colourInversion=invertColour,
                                resolution=(canvasWidth, canvasWidth),
                                circleType="SCircle",
                            )
                            imageSCircleData = imageSCircle.getdata()

                            # Graphics.changeColourSchemeOfImg(imFront, )

                            imFront.paste(imageSCircle, (0, frontTextLine1Height))
                            # imFront = Graphics.shiftKeyOfImg(imFront, [7])[0]
                            # imFront.show()

                            imFrontDraw.text(
                                (0, frontTextLine1Height),
                                hexagramStory1Text,
                                font=hexagramStoryFont,
                                color=inkColour,
                                fill=inkColourInv,
                                anchor="lt",
                            )
                            imFrontDraw.text(
                                (canvasWidth, frontTextLine1Height),
                                hexagramStory2Text,
                                font=hexagramStoryFont,
                                color=inkColour,
                                fill=inkColourInv,
                                anchor="rt",
                            )
                            imFrontDraw.text(
                                (canvasWidth, canvasWidth),
                                signatureText,
                                font=signatureFont,
                                color=inkColour,
                                fill=inkColourInv,
                                anchor="rm",
                            )
                            if makeCornerSmallCircles:
                                # First Hexagram
                                sCirclePathFirstHexagram = Graphics.getDiagramPath(
                                    change=change.getHexagram(["Change"])[0],
                                    key=rootKey,
                                    diagramType="SCircle",
                                    resolution=4096,
                                    pathSeperator="\\",
                                    includeFileExtension=True,
                                    invertColour=invertColour,
                                )
                                # Second Hexagram
                                sCirclePathSecondHexagram = Graphics.getDiagramPath(
                                    change=change.getHexagram(["Change"])[1],
                                    key=rootKey,
                                    diagramType="SCircle",
                                    resolution=4096,
                                    pathSeperator="\\",
                                    includeFileExtension=True,
                                    invertColour=invertColour,
                                )

                                try:
                                    # Inverse
                                    sCirclePathInverse = Graphics.getDiagramPath(
                                        change=change.getInverse(),
                                        key=rootKey,
                                        diagramType="SCircle",
                                        resolution=4096,
                                        pathSeperator="\\",
                                        includeFileExtension=True,
                                        invertColour=invertColour,
                                    )
                                    # Reverse
                                    imageSCircleInverse = insertSmallCircle(
                                        change=change.getInverse(),
                                        rootKey=rootKey,
                                        colourInversion=invertColour,
                                        resolution=(smallCircleWidth, smallCircleWidth),
                                        circleType="SCircle",
                                    )
                                    imageSCircleReverse = insertSmallCircle(
                                        change=change.getReverse(),
                                        rootKey=rootKey,
                                        colourInversion=invertColour,
                                        resolution=(smallCircleWidth, smallCircleWidth),
                                        circleType="SCircle",
                                    )

                                except:
                                    raise ValueError("file does not exist.")
                                    imagesSCircleInverse = pdf2image.convert_from_path(
                                        Graphics.getDiagramPath(
                                            change=Change([]),
                                            key=rootKey,
                                            diagramType="SCircle",
                                            resolution=4096,
                                            pathSeperator="\\",
                                            includeFileExtension=True,
                                        ),
                                        dpi=300,
                                        size=(smallCircleWidth, smallCircleWidth),
                                        single_file=True,
                                        transparent=True,
                                        use_pdftocairo=True,
                                    )
                                imagesSCircleFirstHexagram = pdf2image.convert_from_path(
                                    sCirclePathFirstHexagram,
                                    dpi=300,
                                    size=(smallCircleWidth, smallCircleWidth),
                                    single_file=True,
                                    transparent=True,
                                    use_pdftocairo=True,
                                )
                                imagesSCircleSecondHexagram = pdf2image.convert_from_path(
                                    sCirclePathSecondHexagram,
                                    dpi=300,
                                    size=(smallCircleWidth, smallCircleWidth),
                                    single_file=True,
                                    transparent=True,
                                    use_pdftocairo=True,
                                )
                                imageSCircleFirstHexagram = insertSmallCircle(
                                    change=change.getHexagram(["Change"])[0],
                                    rootKey=rootKey,
                                    colourInversion=invertColour,
                                    resolution=(smallCircleWidth, smallCircleWidth),
                                    circleType="SCircle",
                                )
                                imageSCircleSecondHexagram = insertSmallCircle(
                                    change=change.getHexagram(["Change"])[1],
                                    rootKey=rootKey,
                                    colourInversion=invertColour,
                                    resolution=(smallCircleWidth, smallCircleWidth),
                                    circleType="SCircle",
                                )

                                imFront.paste(
                                    imageSCircleInverse,
                                    (0, round(y1 - smallCircleWidth)),
                                )
                                imFront.paste(
                                    imageSCircleReverse,
                                    (
                                        round(canvasWidth - smallCircleWidth),
                                        round(y1 - smallCircleWidth),
                                    ),
                                )
                                imFront.paste(imageSCircleFirstHexagram, (0, 0))
                                imFront.paste(
                                    imageSCircleSecondHexagram,
                                    (round(canvasWidth - smallCircleWidth), 0),
                                )

                            if drawHexagramSymbols:

                                symbolPathFirstHexagram = Graphics.getDiagramPath(
                                    change=change.divideScaleBy(
                                        denominator=2, normaliseToSlice=True
                                    )[0],
                                    key=rootKey,
                                    diagramType="Hexagram",
                                    pathSeperator="\\",
                                    includeFileExtension=True,
                                    invertColour=invertColour,
                                )
                                symbolPathSecondHexagram = Graphics.getDiagramPath(
                                    change=change.divideScaleBy(
                                        denominator=2, normaliseToSlice=True
                                    )[1],
                                    key=Key.allFlats[Key.allFlats.index(rootKey) + 6],
                                    diagramType="Hexagram",
                                    pathSeperator="\\",
                                    includeFileExtension=True,
                                    invertColour=invertColour,
                                )

                                """input('hey buddy what is up {} {} \n{} {}'.format(
                                    change.getHexagram(['Change']), change,
                                    symbolPathFirstHexagram, symbolPathSecondHexagram
                                ))"""
                                imagesSymbolFirstHexagram = pdf2image.convert_from_path(
                                    symbolPathFirstHexagram,
                                    dpi=300,
                                    size=(smallCircleWidth, smallCircleWidth),
                                    single_file=True,
                                    transparent=True,
                                    use_pdftocairo=True,
                                )
                                imagesSymbolSecondHexagram = pdf2image.convert_from_path(
                                    symbolPathSecondHexagram,
                                    dpi=300,
                                    size=(smallCircleWidth, smallCircleWidth),
                                    single_file=True,
                                    transparent=True,
                                    use_pdftocairo=True,
                                )
                                imFront.paste(imagesSymbolFirstHexagram[0], (0, 0))
                                imFront.paste(
                                    imagesSymbolSecondHexagram[0],
                                    (round(canvasWidth - smallCircleWidth), 0),
                                )

                            for i in range(smallCircles):
                                x = round(i * smallCircleWidth)

                                """sCirclePathSequential = Graphics.getDiagramPath(
                                    change=Change.makeFromChangeNumber(i + changeNumber + (1 if (changeNumber <= -1 and changeNumber + 1 + i > 0) else 0) - (4096 if changeNumber + 1 + i > 2048 else 0)) ,
                                    key='C', diagramType='SCircle', resolution=4096, pathSeperator='\\',
                                    includeFileExtension=True,invertColour=invertColour)
                                sCirclePathChangedNote = Graphics.getDiagramPath(
                                    change=change.getChangedNote(i), key='C', diagramType='SCircle',
                                    resolution=4096, pathSeperator='\\',
                                    includeFileExtension=True,invertColour=invertColour)
                                sCirclePathRotated = Graphics.getDiagramPath(
                                    change=change.getRotation(i), key='C', diagramType='SCircle',
                                    resolution=4096, pathSeperator='\\',
                                    includeFileExtension=True,invertColour=invertColour)"""
                                print(
                                    "doing file:///{}. It is smallCircle {} of {}".format(
                                        sCirclePath, i, smallCircles
                                    )
                                )

                                """imagesSCircleChangedNote = pdf2image.convert_from_path(sCirclePathChangedNote,
                                                                            dpi=300, size=(smallCircleWidth, smallCircleWidth), single_file=True,
                                                                            transparent=True, use_pdftocairo=True)
                                imagesSCircleSequential = pdf2image.convert_from_path(sCirclePathSequential,
                                                                             dpi=300, size=(smallCircleWidth, smallCircleWidth),
                                                                             single_file=True,
                                                                             transparent=True, use_pdftocairo=True)
                                imagesSCircleRotated = pdf2image.convert_from_path(sCirclePathRotated,
                                                                            dpi=300, size=(smallCircleWidth, smallCircleWidth),
                                                                            single_file=True,
                                                                            transparent=True, use_pdftocairo=True)"""
                                imageSCircleChangedNote = insertSmallCircle(
                                    change=change.getChangedNote(i),
                                    rootKey=rootKey,
                                    colourInversion=invertColour,
                                    resolution=(smallCircleWidth, smallCircleWidth),
                                    circleType="SCircle",
                                )
                                imageSCircleSequential = insertSmallCircle(
                                    change=Change.makeFromChangeNumber(
                                        i
                                        + changeNumber
                                        + (
                                            1
                                            if (
                                                changeNumber <= -1
                                                and changeNumber + 1 + i > 0
                                            )
                                            else 0
                                        )
                                        - (4096 if changeNumber + 1 + i > 2048 else 0)
                                    ),
                                    rootKey=rootKey,
                                    colourInversion=invertColour,
                                    resolution=(smallCircleWidth, smallCircleWidth),
                                    circleType="SCircle",
                                )
                                imageSCircleRotated = insertSmallCircle(
                                    change=change.getRotation(i),
                                    rootKey=rootKey,
                                    colourInversion=invertColour,
                                    resolution=(smallCircleWidth, smallCircleWidth),
                                    circleType="SCircle",
                                )

                                # Add condition for height allowing these rows
                                imFront.paste(imageSCircleChangedNote, (x, y1))
                                imFront.paste(imageSCircleSequential, (x, y2))
                                imFront.paste(imageSCircleRotated, (x, y3))
                                print("pasting", imageSCircleChangedNote, (x, y1))

                    if rootKey != "C":
                        print("commencing colour transposition... ", end="")
                        imFront = Graphics.shiftKeyOfImg(imFront, [rootKey])
                    else:
                        print(
                            "not commencing colour transposition because we are in C currently... ",
                            end="",
                        )

                    # imFront = Graphics.changeColourSchemeOfImg(imFront,coloursOrig,coloursTrans)
                    print("and we have liftoff (from a colourful rocket).")
                    success = False
                    while not success:
                        try:
                            if makeFront:
                                imFront.save(tShirtPathFront)
                                print(
                                    "saved TShirt Front to file:///"
                                    + tShirtPathFront.replace("\\", "/")
                                )
                            if makeBack:
                                imBack.save(tShirtPathBack)
                                print(
                                    "saved TShirt Back to file:///",
                                    tShirtPathBack.replace("\\", "/"),
                                )
                            success = True
                        except:
                            input(
                                "did not save. One of these fucked up,\n {}\n{}.\n try again?".format(
                                    tShirtPathFront, tShirtPathFront
                                )
                            )

    @classmethod
    def renderPCircle(
        cls,
        change: Change,
        key,
        makeAllKeys=True,
        savePdf=True,
        saveEps=False,
        externalGraphicsPath=False,
        textWay="Position",
        fixGlitchWithYBump=False, #seems like pyx finally fixed this
        invertColour=False,
        greyScale=False,
        skipIfFileExists=False,
    ):
        if skipIfFileExists and os.path.isfile(
            Graphics.getDiagramPath(
                change=change,
                key=key,
                diagramType="PCircle",
                invertColour=invertColour,
                greyScale=greyScale,
                externalGraphicsPath=externalGraphicsPath,
                filetype="pdf",
                includeFileExtension=True,
                tryToReplaceMissingWithRootKey=False,
            )
        ):
            print(
                "skipping this instead because it already exists, so: ",
                end="  .. and this is because skipIfFileExists == True",
            )
            return True
        if all([i for i in (invertColour, greyScale)]):
            raise TypeError("No")
        import pyx
        text = pyx.text
        style = pyx.style
        path = pyx.path
        color = pyx.color

        pyx.text.set(
            pyx.text.LatexEngine,
            texenc="utf-8",
        )
        texRunnerPreamble = r"\usepackage[utf8]{inputenc}"
        try:
            pyx.text.preamble(texRunnerPreamble)
        except FileNotFoundError as e:
            raise FileNotFoundError('Have you installed LaTeX? Have you also added it to PATH? If not do both. ' + str(e))
        # pyx.text.
        if makeAllKeys == True:
            key = "C"
            canvases = [pyx.canvas.canvas() for i in range(12)]
            from Colour import Colour
            coloursByCanvas = [
                Colour.getTransposedColours(
                    colourTranspose=(JazzNote.distanceFromC(key) + i) % 12,
                    invertColour=False,
                    neutralColours=False,
                )
                for i in range(12)
            ]
            coloursInvByCanvas = [
                Colour.getTransposedColours(
                    colourTranspose=JazzNote.distanceFromC(key),
                    invertColour=False,
                )
                for i in range(12)
            ]
        else:
            canvases = [pyx.canvas.canvas(textengine=text)]
            # c = canvas.canvas()
            colours = Colour.getTransposedColours(
                colourTranspose=JazzNote.distanceFromC(key),
                invertColour=False,
                neutralColours=False,
            )
            coloursInv = Colour.getTransposedColours(
                colourTranspose=JazzNote.distanceFromC(key),
                invertColour=False,
            )
            coloursByCanvas = [
                Colour.getTransposedColours(
                    colourTranspose=(JazzNote.distanceFromC(key) + i) % 12,
                    invertColour=False,
                    neutralColours=False,
                )
                for i in (JazzNote.distanceFromC(key),)
            ]
            coloursInvByCanvas = [
                Colour.getTransposedColours(
                    colourTranspose=JazzNote.distanceFromC(key),
                    invertColour=False,
                )
                for i in (JazzNote.distanceFromC(key),)
            ]
        # input(colours)
        poly = change.getPolygon(
            useTopOrigin=True,
            boundL=-1,
            boundR=1,
            boundT=1,
            boundB=-1,
            closePolygon=True,
        )
        degrees = change.getAngles(goQuarterTurnAnticlockwise=True)
        allDegrees = Change(
            ["1", "b2", "2", "b3", "3", "4", "b5", "5", "b6", "6", "b7", "7"]
        ).getAngles(goQuarterTurnAnticlockwise=True)
        semitones = change.getSemitones()
        # Utility.printPrettyVars(poly)

        ####Main circle

        circle = pyx.path.circle(0, 0, 1)
        line = pyx.path.line(-3, 1, 3, 2)
        for c in canvases:
            c.stroke(circle, [pyx.style.linewidth.THick,
                              pyx.color.rgb(1,1,1)],
                     )

        isects_circle, isects_line = circle.intersect(line)
        """for isect in isects_circle:
            isectx, isecty = circle.at(isect)
            c.stroke(path.line(0, 0, isectx, isecty))"""

        # transparent triangles
        import itertools
        for sides in range(3, 4):  # len(change) - 1):
            for shape in itertools.combinations(range(len(semitones)), sides):
                tripath = path.path()

                x, y, z = int(shape[0]), int(shape[1]), int(shape[2])

                assert all([i < len(change) for i in (x, y, z)])

                """r = Colour.blendColourValue(coloursInv[x][0]/255,coloursInv[y][0]/255,0.3333)
                b = Colour.blendColourValue(coloursInv[x][1]/255,coloursInv[y][1]/255,0.3333)
                g = Colour.blendColourValue(coloursInv[x][2]/255,coloursInv[y][2]/255,0.3333)
                r = Colour.blendColourValue(r, coloursInv[z][0]/255, 0.33333)
                b = Colour.blendColourValue(g, coloursInv[z][1]/255, 0.3333)
                g = Colour.blendColourValue(b, coloursInv[z][2]/255, 0.33333)"""
                # Utility.printPrettyVars(r,g,b,x,y,z,change,len(change))
                # input('{} {} {}'.format(poly[int(x)],x,type(x)))
                tripath.append(path.moveto(poly[x][0], -poly[x][1]))
                tripath.append(path.lineto(poly[y][0], -poly[y][1]))
                tripath.append(path.lineto(poly[z][0], -poly[z][1]))
                tripath.append(path.lineto(poly[x][0], -poly[x][1]))
                tripath.append(path.closepath())
                for cidx, c in enumerate(canvases):
                    r = (
                        (
                            coloursInvByCanvas[cidx][x][0]
                            + coloursInvByCanvas[cidx][y][0]
                            + coloursInvByCanvas[cidx][z][0]
                        )
                        / 255
                        / 3
                    )
                    g = (
                        (
                            coloursInvByCanvas[cidx][x][1]
                            + coloursInvByCanvas[cidx][y][1]
                            + coloursInvByCanvas[cidx][z][1]
                        )
                        / 255
                        / 3
                    )
                    b = (
                        (
                            coloursInvByCanvas[cidx][x][2]
                            + coloursInvByCanvas[cidx][y][2]
                            + coloursInvByCanvas[cidx][z][2]
                        )
                        / 255
                        / 3
                    )
                    c.fill(tripath, [color.rgb(r, g, b), color.transparency(0.8)])
                #print("shape", shape)

        polypath = path.path()

        linesByInterval = {}
        thislines = []
        ####Draw interval vector
        for start in range(len(change)):

            pos = start
            # if any([i in  for i in range(12)])
            # polypath.append(path.moveto(poly[pos][0],poly[pos][1]))
            # c.stroke(path.moveto(poly[pos][0],poly[pos][1]))
            for interval in range(1, 12 - start):
                startpath = path.path()
                startpath.append(path.moveto(poly[start][0], -poly[start][1]))
                if str(interval) not in linesByInterval.keys():
                    linesByInterval[str(interval)] = []
                    print("making it", linesByInterval)

                while (pos + interval) % len(change) != start:
                    oldpos = pos
                    pos += interval
                    pos %= len(change)
                    ln = sorted([oldpos, pos])

                    # if ln not in linesByInterval[str(interval)]:
                    if all(
                        [
                            ln not in linesByInterval[length]
                            for length in linesByInterval.keys()
                        ]
                    ):
                        #print("adding line", linesByInterval[str(interval)])
                        startpath.append(path.lineto(poly[pos][0], -poly[pos][1]))
                        """c.stroke(path.lineto(poly[oldpos][0], -poly[oldpos][1],
                                           poly[pos][0], -poly[pos][1]), 
                                 [style.linewidth.thin,
                                  color.rgb((colours[pos][0] + colours[oldpos][0]) /255/2,
                                            (colours[pos][1] + colours[oldpos][1]) / 255 / 2,
                                            (colours[pos][2] + colours[oldpos][2]) / 255 / 2)])"""
                        linesByInterval[str(interval)].append(ln)
                    else:
                        break
                        # input('{} in {}'.format(line,linesByInterval[str(interval)]))
                else:
                    startpath.append(path.lineto(poly[0][0], -poly[0][1]))
                    # c.stroke((path.closepath()))

                pos = start
                startpath.append(path.closepath())
                for c in canvases:
                    c.stroke(startpath, [style.linewidth.normal, color.rgb.black])
        ###### Ring circles

        _ringCircleSize = 0.33
        _circleSize = 1 + _ringCircleSize
        _imRadius = _circleSize + _ringCircleSize

        ####### Boundary invisible
        bounds = path.path()
        bounds.append(path.moveto(0, 0))
        bounds.append(path.lineto(0, 1 * _imRadius))
        bounds.append(path.lineto(1 * _imRadius, 1 * _imRadius))
        bounds.append(path.lineto(1 * _imRadius, 0))
        bounds.append(path.lineto(0, 0))
        bounds.append(path.closepath())

        for i, canv in enumerate(canvases):
            canvases[i].stroke(bounds, [color.rgb(0, 0, 0), color.transparency(1)])

        if textWay == "Jazz":
            _notesText = change.straightenDegrees()  # WRITE JAZZ
        elif textWay == "Position":
            _notesText = change.getSemitones()  # WRITE semitones
        elif textWay == "Consonant":
            _notesText = [n.getConsonant() for n in change]  # WRITE consonant
        else:
            raise ValueError(
                "textWay: Must be Jazz, Position, or Consonant. ;) You provided {}".format(
                    textWay
                )
            )
        _ringCircleNoteIdx = -1
        for s in range(12):
            angle = allDegrees[s]
            x, y = math.cos(angle) * _circleSize, math.sin(angle) * _circleSize
            if s in semitones:
                _ringCircleNoteIdx += 1
                _noteText = _notesText[_ringCircleNoteIdx]
                _noteText = str(_noteText)
                if len(_noteText) > 1:
                    #Do this because otherwise the characters are too close together
                    _noteText = '\\hspace{-.5ex}'.join(_noteText)
                circle = path.circle(x, -y, _ringCircleSize)
                for cidx, c in enumerate(canvases):
                    c.fill(
                        circle,
                        [
                            color.rgb(
                                coloursByCanvas[cidx][s][0] / 255,
                                coloursByCanvas[cidx][s][1] / 255,
                                coloursByCanvas[cidx][s][2] / 255,
                            )
                        ],
                    )
                    c.stroke(circle, [style.linewidth.THIck])
                    _ringCircleText = str(_noteText)

                    # Squish ccharacters closer together with \hspace
                    if len(_ringCircleText) > 1:
                        _ringCircleTextSquished = ""
                        for charIdx, char in enumerate(_ringCircleText):
                            _ringCircleTextSquished += char
                            if charIdx != (len(_ringCircleText) - 1):
                                _ringCircleTextSquished += (
                                    "\\hspace{-" + str(round(0.5 * 1, 2)) + "ex}frig"
                                )
                        _ringCircleText = _ringCircleTextSquished[:]
                        # input(_ringCircleText)
                    # This replace() does not work :(
                    _ringCircleText = _ringCircleText.replace("♭", "$\\flat$\\")
                    _ringCircleText = _ringCircleText.replace("♯", "$\\sharp$\\")

                    _ringCircleText = "\\bf{\\LARGE{\\noindent " + str(_noteText) + "}}"

                    """if (any([i in _ringCircleText for i in ('♭','$\\flat$\\')])):
                        input('asdfasdf {} {} '.format(_ringCircleText, 
                                                       _ringCircleText.replace('♭', '$\\flat$\\').replace('♯', '$\\sharp$\\')))
                    """
                    glitchBump = 0
                    if fixGlitchWithYBump and s == semitones[0]:
                        glitchBump = 0.61802 * _ringCircleSize

                    c.text(
                        x,
                        -y + glitchBump,
                        _ringCircleText.replace("♭", "$\\flat$\\").replace(
                            "♯", "$\\sharp$\\"
                        ),
                        [text.halign.center, text.valign.middle, text.size(5)],
                    )
            else:
                dashSize = _circleSize
                lx1 = (
                    math.cos(angle) * dashSize * (1 + _ringCircleSize / 2)
                )  # *dashSize
                ly1 = (
                    math.sin(angle) * dashSize * (1 + _ringCircleSize / 2)
                )  # *dashSize
                lx2 = math.cos(angle)  # / dashSize
                ly2 = math.sin(angle)  # / dashSize

                xshift = math.cos(angle + math.pi / 2) * (1 - dashSize) * NGramGraphic.breakSpacing
                yshift = math.sin(angle + math.pi / 2) * (1 - dashSize) * NGramGraphic.breakSpacing

                line = path.path()
                line.append(path.moveto(lx1 + xshift, -ly1 - yshift))
                line.append(path.lineto(lx2 + xshift, -ly2 - yshift))
                line.append(path.lineto(lx2 - xshift, -ly2 + yshift))
                line.append(path.lineto(lx1 - xshift, -ly1 + yshift))
                line.append(path.lineto(lx1 + xshift, -ly1 - yshift))
                line.append(path.closepath())

                segmentSize = NGramGraphic.lineSpacing

                x1 = lx2
                x2 = lx2 + math.cos(angle) * _ringCircleSize * segmentSize
                y1 = ly2
                y2 = ly2 + math.sin(angle) * _ringCircleSize * segmentSize
                square1 = path.path()
                square1.append(path.moveto(x1 + xshift, -y1 - yshift))
                square1.append(path.lineto(x2 + xshift, -y2 - yshift))
                square1.append(path.lineto(x2 - xshift, -y2 + yshift))
                square1.append(path.lineto(x1 - xshift, -y1 + yshift))
                square1.append(path.lineto(x1 + xshift, -y1 - yshift))
                square1.append(path.closepath())

                x1 = lx1
                x2 = lx1 - math.cos(angle) * _ringCircleSize * segmentSize
                y1 = ly1
                y2 = ly1 - math.sin(angle) * _ringCircleSize * segmentSize
                square2 = path.path()
                square2.append(path.moveto(x1 + xshift, -y1 - yshift))
                square2.append(path.lineto(x2 + xshift, -y2 - yshift))
                square2.append(path.lineto(x2 - xshift, -y2 + yshift))
                square2.append(path.lineto(x1 - xshift, -y1 + yshift))
                square2.append(path.lineto(x1 + xshift, -y1 - yshift))
                square2.append(path.closepath())

                for cidx, c in enumerate(canvases):
                    # c.stroke(path.line(lx1, -ly1, lx2, -ly2, ),
                    #         [style.linewidth.thin, color.rgb.green])
                    for square in (square1, square2):
                        #Turn this on to enable filling lines with colour
                        c.fill(
                            square,
                            [
                                color.rgb(

                                    1,
                                    1,
                                    1,
                                )
                            ],
                        )

                        '''c.fill(
                            square,
                            [
                                color.rgb(

                                    inkByCanvas[cidx][0] / 255,
                                    inkByCanvas[cidx][1] / 255,
                                    inkByCanvas[cidx][2] / 255,
                                )
                            ],
                        )'''
                        c.stroke(square, [style.linewidth.Thick])

        for cidx, c in enumerate(canvases):
            # print(donePairs)
            # Utility.printPrettyVars(polypath.path())
            # print(lines)
            key = JazzNote.noteNameFlats[cidx]
            pdfpath = Graphics.getDiagramPath(
                change=change,
                key=key,
                diagramType="PCircle",
                filetype="pdf",
                invertColour=invertColour,
                greyScale=greyScale,
                externalGraphicsPath=externalGraphicsPath
            )
            pdfdir = Graphics.getDiagramPath(
                change=change,
                key=key,
                diagramType="PCircle",
                filetype="pdf",
                includeFilename=False,
                invertColour=invertColour,
                greyScale=greyScale,
                externalGraphicsPath=externalGraphicsPath
            )
            assert not ('F:' in pdfdir), 'asdfasdfasdfasdf'
            epspath = Graphics.getDiagramPath(
                change=change,
                key=key,
                diagramType="PCircle",
                filetype="eps",
                invertColour=invertColour,
                greyScale=greyScale,
                externalGraphicsPath=externalGraphicsPath
            )
            epsdir = Graphics.getDiagramPath(
                change=change,
                key=key,
                diagramType="PCircle",
                filetype="eps",
                includeFilename=False,
                invertColour=invertColour,
                greyScale=greyScale,
                externalGraphicsPath=externalGraphicsPath
            )
            if savePdf:
                Utility.makeDirectory(pdfdir)
            if saveEps:
                Utility.makeDirectory(epsdir)

            # input(epsdir)
            # input(Utility.printPrettyVars(filepath))

            '''print(
                "This is stuff here: len(polypath):{} polypath:{}".format(
                    len(polypath), polypath
                )
            )'''
            saveSuccess = False
            while not saveSuccess:
                try:
                    if saveEps:
                        if externalGraphicsPath:
                            raise ValueError("have not added saving to external")
                        c.writeEPSfile(epspath)
                        print("saving to", epspath.replace("/", "\\") + ".eps")
                    # input(str([i for i in c]))
                    if savePdf:
                        if externalGraphicsPath:
                            # input(pdfpath)

                            pass#pdfpath = pdfpath.replace("\\", "/")
                        if os.path.isfile(pdfpath):
                            os.remove(pdfpath)
                        Utility.makeDirectory(
                            os.path.dirname(pdfpath),
                        )
                        saveSuccess = False
                        while not saveSuccess:

                            try:
                                c.writePDFfile(pdfpath)
                                # input('trying writing TO {}'.format(pdfpath))

                            except Exception as e:
                                input("could not save {} (fail polypath or RAM problem) {}. Try again?\nError: {}".format(
                                        pdfpath, polypath, e)
                                )
                                print(polypath)
                                """except PermissionError as e:
                                    input('{} File is probably open somewhere. Press Enter'.format(pdfpath))
                                except:
                                    input('you are fucked, bud.') 
                                if not os.path.isfile(pdfpath):
                                    raise FileNotFoundError('Shit.. it did make the file at {}'.format(pdfpath))"""

                            # input(pdfpath)

                            print(
                                "saving to",
                                pdfpath.replace("/", "\\")
                                + ".pdf because externalGraphicsPath ==",
                                externalGraphicsPath,
                            )
                            saveSuccess = True
                except Exception:
                    raise Exception
                saveSuccess = True
        # print('fucker',epsdir)
        # input(epspath)

        print(
            "{} lines are\n".format(
                sum([len(linesByInterval[i]) for i in linesByInterval])
            )
        )
        for length in linesByInterval.keys():
            print(length, linesByInterval[length])

    @classmethod
    def renderChangePolyOLD(cls, change: Change, key):
        c = canvas.canvas()
        colours = Colour.getTransposedColours(
            colourTranspose=JazzNote.distanceFromC(key),
        )
        poly = change.getPolygon(
            useTopOrigin=True,
            boundL=-1,
            boundR=1,
            boundT=1,
            boundB=-1,
            closePolygon=True,
        )
        degrees = change.getAngles(goQuarterTurnAnticlockwise=True)
        semitones = change.getSemitones()
        # Utility.printPrettyVars(poly)
        circle = path.circle(0, 0, 1)
        line = path.line(-3, 1, 3, 2)

        c.stroke(circle, [style.linewidth.normal])
        # c.stroke(line, [style.linewidth.Thick])
        isects_circle, isects_line = circle.intersect(line)
        """for isect in isects_circle:
            isectx, isecty = circle.at(isect)
            c.stroke(path.line(0, 0, isectx, isecty))"""
        polypath = path.path()
        thispath = path.path()
        lines = []
        thislines = []
        for start in range(len(change)):
            thislines, thispoly = [], path.path()
            if (
                len(thispath) > 0
                and thispath[-1] != path.moveto(poly[start][0], -poly[start][1])
                or len(thispath) == 0
            ):
                thispath.append(path.moveto(poly[start][0], -poly[start][1]))
            for interval in range(1, len(change) // 2):
                pos = start
                while (pos + interval) % len(change) != start:

                    if [
                        pos,
                        (pos + interval) % len(change),
                    ].sort() not in thislines and True:
                        print(
                            "[{},{}] nota in {}".format(
                                pos, (pos - interval) % len(change), thislines
                            )
                        )
                        if [
                            (pos + interval) % len(change),
                            pos,
                        ].sort() not in lines and [
                            pos,
                            (pos + interval) % len(change),
                        ].sort() not in lines:
                            thislines.append([pos])
                            pos = (pos + interval) % len(change)
                            thislines[-1].append(pos)
                            thislines[-1].sort()
                        else:
                            pos = (pos + interval) % len(change)
                            continue
                        point = poly[pos % len(change)]
                        if path.lineto(point[0], -point[1]) not in thispath:
                            thispath.append(apathitem=path.lineto(point[0], -point[1]))
                        # input('[{},{}] notb in {}'.format(pos, (pos - interval) % len(change), lines))

                    else:
                        pos = (pos + interval) % len(change)
                    point = poly[pos % len(change)]

                    """if pos == len(change) - 1:

                        continue"""

                else:
                    print(
                        "moving on from interval {} because {} + {} == start {} ({})".format(
                            interval,
                            pos,
                            interval,
                            (pos + interval) % len(change),
                            (pos + interval) % len(change) == start,
                        )
                    )
                    # polypath.append(apathitem=path.lineto(poly[0][0], -poly[0][1]))
            # polypath.append(path.moveto(poly[start][0],poly[start][1]))
            if len(thispath) > 0 and poly[-1] != path.closepath():

                if type(thispath[-1]) == path.lineto:
                    thispath.append(path.closepath())
            polypath.extend(thispath)
            lines.extend(thislines)
            c.stroke(thispath, [style.linewidth.THIn, color.rgb.red])
            # polypath = path.path()
        for s in range(len(semitones)):
            angle = degrees[s]
            x, y = math.cos(angle), math.sin(angle)
            circle = path.circle(x, -y, 0.25)
            c.stroke(circle, [style.linewidth.thick])

        # print(donePairs)
        # Utility.printPrettyVars(polypath.path())
        # print(lines)
        pdfpath = Graphics.getDiagramPath(
            change=change,
            key=key,
            diagramType="PCircle",
            filetype="pdf",
        )
        pdfdir = Graphics.getDiagramPath(
            change=change,
            key=key,
            diagramType="PCircle",
            filetype="pdf",
            includeFilename=False,
        )
        epspath = Graphics.getDiagramPath(
            change=change,
            key=key,
            diagramType="PCircle",
            filetype="eps",
        )
        epsdir = Graphics.getDiagramPath(
            change=change,
            key=key,
            diagramType="PCircle",
            filetype="eps",
            includeFilename=False,
        )

        Utility.makeDirectory(pdfdir)

        Utility.makeDirectory(epsdir)

        # input(epsdir)
        # input(Utility.printPrettyVars(filepath))
        print("{} {}".format(len(polypath), polypath))
        try:
            c.writePDFfile(pdfpath)
        except:
            raise ValueError("fail polypath {}".format(polypath))
            print(polypath)
        # print('fucker',epsdir)
        # input(epspath)
        c.writeEPSfile(epspath)
        print("{} lines are\n{}".format(len(lines), lines))

    @classmethod
    def convertDirectoryOfPNGtoAVI(cls, directory, video_name="video.avi"):
        # got this solution from
        ## https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python

        images = [img for img in os.listdir(directory) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(directory, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, 1, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()

    @classmethod
    def drawRCircleToIm(
        cls,
        circle: FCircle,
        im,
        lineProportion,
        lineAdjust,
        drawConnectiveLines=True,
        circleBGColour=None,
        lineColour=None,
        colours: list = None,
        colourTranspose=0,
        invertedColours: list = None,
        invertColour=False,
        greyScale=False,
    ):
        if type(im) is PIL.Image.Image:
            useVector = False
        elif type(im) is pyx.canvas.canvas:
            useVector = True
        else:
            raise TypeError(
                "im needs to be image type from PIL or canvas.canvas from pyx, not {}".format(
                    type(im)
                )
            )

        if not colours is None or not invertedColours is None:
            raise ValueError("use None for colours and inverted colours for defualting")
        # Default colours
        # Default colours

        _proportion = FCircle.radiusOuterProportionRCircle

        _degrees = circle.change.getAngles(
            returnDegrees=True, repeatFirstResult=True, goQuarterTurnAnticlockwise=True
        )
        _mode = 0
        _rCircles = circle.getRingCircles(invertBG=not invertColour)
        for st in range(12):
            _degree = st * 360 / 12 - 90
            _radian = _degree * 3.141596238 / 180
            if st in circle.change.getSemitones():
                """_rCircle = FCircle([circle.x + math.cos(_radian) * circle.r * _proportion/FCircle.proportion,
                 circle.y+ math.sin(_radian) * circle.r * _proportion/FCircle.proportion],
                circle.r*RCircle.radiusOfEachCircle/FCircle.proportion,
                circle.change.mode(_mode),
                st,_proportion)"""
                _rCircle = _rCircles[_mode]

                # im = Graphics.drawFCircleToIm(circle=_rCircle,
                Graphics.drawFCircleToIm(
                    circle=_rCircle,
                    im=im,
                    invertColour=invertColour,
                    colourTranspose=colourTranspose,
                    lineProportion=lineProportion,
                    lineAdjust=lineAdjust,
                    greyScale=greyScale,
                )
                _mode += 1
        return im

    @classmethod
    def drawFCircleToIm(
        cls,
        circle: FCircle,
        im,
        lineProportion,
        lineAdjust,
        drawClockDashes=False,
        dashProportion=0.1,
        majorRuler=True,
        colourCircleOutline=False,
        circleBGColour=None,
        lineColour=None,
        colours: list = None,
        colourTranspose=0,
        invertColour=False,
        alternateBG=False,
        drawBlankCircle=False,
        greyScale=None,
        showTrigrams=True,
        displayCircle=False,
        artCircleProportion=None,
        scale=1.00,
        splitCircleChords=True,
        circleType=None,
        success = False
    ):

        _args = locals() # Make copy before assigning any variables
        
        while not _args['success']:
            _args['success'] = False
            try:
                #input(_args)
                _args.pop('cls')
                _args['success'] = True
                return Graphics.drawFCircleToIm(**_args)

            except MemoryError:
                input("You need more RAM to continue. Try again?")

        if circleType == None:
            circleType = "FCircle"
            # input('shit')
        if type(im) is PIL.Image.Image:
            useVector = False
        elif type(im) is pyx.canvas.canvas:
            useVector = True
        else:
            raise TypeError(
                "im needs to be image type from PIL or canvas.canvas from pyx, not {} {}".format(
                    im, type(im)
                )
            )
        # input('heh'+str(type(im)))
        # Default colours

        useInvertedColours = (
            circle.invertBG if not invertColour else not circle.invertBG
        )
        # input(useInvertedColours)
        # useInvertedColours = circle.invertBG
        if lineColour is None:
            if not useInvertedColours:
                lineColour = FCircle.lineColour
                _lineColourInv = FCircle.lineColourInv
            elif useInvertedColours:
                lineColour = FCircle.lineColourInv
                _lineColourInv = FCircle.lineColour
        else:
            if lineColour == FCircle.lineColour:
                _lineColourInv = FCircle.lineColourInv
            else:
                _lineColourInv = FCircle.lineColour
        # Make all lines black for SCircle
        if circleType == "SCircle":
            _lineColourInv = FCircle.lineColour
            lineColour = FCircle.lineColour
        if colours is None:

            colours = Colour.getTransposedColours(
                colourTranspose, greyScale=greyScale, invertColour=useInvertedColours
            )
            coloursInv = Colour.getTransposedColours(
                colourTranspose,
                greyScale=greyScale,
                invertColour=not useInvertedColours,
            )
        else:
            raise TypeError(
                "colours should be none. do you really want to override default vaules with specific colours?"
            )

        if circleBGColour is None:
            if len(circle.change.notes) != 1:
                if circleType == "SCircle":
                    circleBGColour = FCircle.circleBGColour
                    circleBGColourInv = FCircle.circleBGColour
                elif circleType == "FCircle":
                    if not useInvertedColours:
                        if alternateBG:
                            circleBGColour = FCircle.circleBGColourInv
                            circleBGColourInv = FCircle.circleBGColour
                        elif not alternateBG:
                            circleBGColour = FCircle.circleBGColour
                            circleBGColourInv = FCircle.circleBGColourInv
                    # elif useInvertedColours and alternateBG:
                    elif useInvertedColours:
                        if alternateBG:
                            circleBGColour = FCircle.circleBGColour
                            circleBGColourInv = FCircle.circleBGColourInv
                        elif not alternateBG:
                            circleBGColour = FCircle.circleBGColourInv
                            circleBGColourInv = FCircle.circleBGColour
                if not circle.change.__class__.__name__ == "Change":
                    raise TypeError("bla bla bla")
                # input('multi. note bg: {} circle.change: {} len(circle.change): {} type(circle.change):{}'.format(
                #   circleBGColour, circle.change,len(circle.change),type(circle.change)))
            elif len(circle.change.notes) == 1:

                circleBGColour = colours[
                    (circle.change.notes[0].semitonesFromOne() + circle.colourTranspose)
                    % len(colours)
                ]
                circleBGColourInv = coloursInv[
                    (circle.change.notes[0].semitonesFromOne() + circle.colourTranspose)
                    % len(colours)
                ]
                # input('single note bg: {} circle.change: {} len(circle.change): {} type(circle.change):{}'.format(
                #    circleBGColour, circle.change, len(circle.change), type(circle.change)))

        # if alternateBG:
        #    print('alternateBG = {}'.format(circleBGColour))
        else:
            pass
            # raise TypeError('use circleBG = None to default right')
        if colourCircleOutline == True:
            _lineColour = colours[circle.colourTranspose]
        else:
            _lineColour = lineColour

        if circleBGColour == (255, 255, 255):
            circleBGColour = (254, 255, 255)
        if circleBGColourInv == (255, 255, 255):
            circleBGColourInv = (254, 255, 255)
        if lineColour == (255, 255, 255):
            lineColour = (254, 255, 255)
        if _lineColour == (255, 255, 255):
            _lineColour = (254, 255, 255)
        fCircleR = circle.r
        if artCircleProportion == None:
            artCircleProportion = FCircle.artCircleProportion

        if type(circle) != FCircle:
            raise TypeError(
                "Circle: {} is supposed to be type FCircle. ({})".format(
                    circle, type(circle)
                )
            )

        _lineWidth = fCircleR * lineProportion
        # _lineWidth += (_lineWidth - lineTarget) * lineAdjust
        # _lineWidthVector = fCircleR * lineProportion
        _lineWidthVector = _lineWidth / 2
        _lineWidthEllipseVector = _lineWidth * 2
        _lineWidth = int(max(_lineWidth, 1))

        _degrees = circle.change.getAngles(
            returnDegrees=True, repeatFirstResult=True, goQuarterTurnAnticlockwise=True
        )
        if not useVector:
            draw = ImageDraw.Draw(im)

        if circle.change == Change([]):
            pass  # drawBlankCircle = True

        outerNudge = 1 - scale

        if useVector:

            # input('hey there {}'.format(circleBGColour))
            path = pyx.path
            style = pyx.style
            deco = pyx.deco
            color = pyx.color

            def rAndLineWidth(r, lineWidth):
                return r  # + lineWidth / 2

            """im.fill(path.circle(circle.x, -circle.y, rAndLineWidth(circle.r,_lineWidthEllipseVector) * scale),
                [

                    #color.rgb(1, 0.99999, 1) if lineColour != FCircle.circleBGColour else \
                    #    color.rgb(lineColour[0] / 255, lineColour[1] / 255, lineColour[2] / 255)
                 color.rgb(_lineColour[0] / 255, _lineColour[1] / 255, _lineColour[2] / 255)

                 ])"""
            # The above code works but draws it twice.. docs @ https://pyx-project.org/examples/drawing/strokefill.html
            # input('Yep... FCircle {}\ncircleBGColour {}'.format(circle.__repr__(), circleBGColour))
            if len(circle.change) == 0:
                circleBGColour = (255, 255, 255) if invertColour else (0, 0, 0)
            if circleBGColour[:3] == (255, 255, 255):
                circleBGColour = (255, 254, 254)
            im.draw(
                path.circle(circle.x, -circle.y, circle.r * scale),
                [
                    style.linewidth(_lineWidthEllipseVector),
                    color.rgb(
                        _lineColour[0] / 255, _lineColour[1] / 255, _lineColour[2] / 255
                    ),
                    deco.filled(
                        [
                            color.rgb(
                                circleBGColour[0] / 255,
                                circleBGColour[1] / 255,
                                circleBGColour[2] / 255,
                            )
                        ]
                    ),
                ],
            )

            im.stroke(
                path.circle(circle.x, -circle.y, circle.r * scale),
                [
                    style.linewidth(_lineWidthEllipseVector),
                    color.rgb(
                        _lineColour[0] / 255,
                        _lineColour[1] / 255,
                        _lineColour[2] / 255,
                    ),
                ],
            )
        else:
            Graphics.ellipse(
                im=im,
                xy=[
                    circle.x - fCircleR - outerNudge,
                    circle.y - fCircleR - outerNudge,
                    circle.x + fCircleR + outerNudge,
                    circle.y + fCircleR + outerNudge,
                ],
                fill=circleBGColour,
                outline=_lineColour,
                width=_lineWidth,
            )

        if drawBlankCircle == True:
            raise TypeError("he jose")
            # return 1
            return im
        else:
            pass

        if drawClockDashes == True:
            for i in range(12):
                _radian = i * 2 * math.pi / 12
                _outerX = circle.x + fCircleR * math.cos(_radian)
                _outerY = circle.y + fCircleR * math.sin(_radian)
                draw.line(
                    (
                        _outerX,
                        _outerY,
                        _outerX - fCircleR * math.cos(_radian) * dashProportion,
                        _outerY - fCircleR * math.sin(_radian) * dashProportion,
                    ),
                    fill=_lineColour,
                    width=_lineWidth,
                )
        # gusto

        """if False and len(circle.change.notes) == 1:
            if useVector:
                im.stroke(path.circle(circle.x, -circle.y, circle.r),
                          [style.linewidth(_lineWidthVector),
                           color.rgb(_lineColour[0] / 255, _lineColour[1] / 255, _lineColour[2] / 255)])
                im.fill(path.circle(circle.x, -circle.y, circle.r),
                        [style.linewidth(_lineWidthVector),
                         color.rgb(colours[_chordColour % 12][0] / 255, colours[_chordColour % 12][1] / 255,
                                   colours[_chordColour % 12][2] / 255)])
            else:
                im = Graphics.ellipse(im=im, xy=[circle.x - fCircleR,
                                                 circle.y - fCircleR,
                                                 circle.x + fCircleR,
                                                 circle.y + fCircleR],
                                      fill=colours[_chordColour % 12], outline=_lineColour, width=_lineWidth * 2)"""

        for d in range(len(_degrees) - 1):
            _chordColour1 = (
                circle.change.notes[d].semitonesFromOne() + circle.colourTranspose
            )
            _chordColour2 = (
                circle.change.notes[
                    (d + 1) % len(circle.change.notes)
                ].semitonesFromOne()
                + circle.colourTranspose
            )
            _degree = _degrees[d] % 360
            _degreeNext = _degrees[d + 1] % 360
            if useVector:
                if len(circle.change) > 1:
                    r = (
                        circle.r
                    )  # rAndLineWidth(circle.r,1) if circleType == 'FCircle' else circle.r
                    if splitCircleChords:

                        _arcpath1 = path.path()
                        _arcpath2 = path.path()
                        endpoint = (
                            ((_degree) + (_degreeNext)) / 2 % 360
                            if _degreeNext > _degree
                            else ((_degree) + (_degreeNext) + 360) / 2 % 360
                        )
                        # input('degree ' + str(_degree + dumb) + ' degreeNext '+str(_degreeNext + dumb)+' inBetween '+str(endpoint + dumb) + ' colour '+str(_chordColour1))
                        _arcpath1.append(
                            path.arc(circle.x, -circle.y, r, -endpoint, -(_degree))
                        )
                        _arcpath2.append(
                            path.arc(circle.x, -circle.y, r, -(_degreeNext), -endpoint)
                        )
                        _arcpath1.append(
                            path.lineto(  # circle.x + math.sin(-90) * (circle.r + outerNudge) * scale * 1.1,
                                circle.x
                                + r
                                * (
                                    math.cos(math.radians(_degreeNext))
                                    + math.cos(math.radians(_degree))
                                )
                                / 2,
                                -circle.y
                                - r
                                * (
                                    math.sin(math.radians(_degreeNext))
                                    + math.sin(math.radians(_degree))
                                )
                                / 2,
                            )
                        )
                        _arcpath2.append(
                            path.lineto(
                                circle.x
                                + r
                                * (
                                    math.cos(math.radians(_degreeNext))
                                    + math.cos(math.radians(_degree))
                                )
                                / 2,
                                -circle.y
                                - r
                                * (
                                    math.sin(math.radians(_degreeNext))
                                    + math.sin(math.radians(_degree))
                                )
                                / 2,
                            )
                        )
                        _arcpath1.append(path.closepath())
                        _arcpath2.append(path.closepath())
                        success = False
                        while not success:
                            try:
                                im.fill(
                                    _arcpath2,
                                    [
                                        style.linewidth(
                                            _lineWidthEllipseVector
                                            if circleType == "FCircle"
                                            else 0
                                        ),
                                        color.rgb(
                                            colours[_chordColour2 % 12][0] / 255,
                                            colours[_chordColour2 % 12][1] / 255,
                                            colours[_chordColour2 % 12][2] / 255,
                                        ),
                                    ],
                                )
                                im.fill(
                                    _arcpath1,
                                    [
                                        style.linewidth(
                                            _lineWidthEllipseVector
                                            if circleType == "FCircle"
                                            else 0
                                        ),
                                        color.rgb(
                                            colours[_chordColour1 % 12][0] / 255,
                                            colours[_chordColour1 % 12][1] / 255,
                                            colours[_chordColour1 % 12][2] / 255,
                                        ),
                                    ],
                                )
                                success = True
                            except MemoryError:
                                input('ran out of memory during drawing. Try again?')
                    elif not splitCircleChords:
                        _arcpath = path.path()
                        _arcpath.append(
                            path.arc(
                                circle.x,
                                -circle.y,
                                r,
                                -_degrees[d + 1] + 0,
                                -_degrees[d] + 0,
                            )
                        )
                        _arcpath.append(path.closepath())
                        im.fill(
                            _arcpath,
                            [
                                style.linewidth(
                                    _lineWidthEllipseVector
                                    if circleType == "FCircle"
                                    else 0
                                ),
                                color.rgb(
                                    colours[_chordColour1 % 12][0] / 255,
                                    colours[_chordColour1 % 12][1] / 255,
                                    colours[_chordColour1 % 12][2] / 255,
                                ),
                            ],
                        )

            else:
                draw.chord(
                    [
                        circle.x - fCircleR,
                        circle.y - fCircleR,
                        circle.x + fCircleR,
                        circle.y + fCircleR,
                    ],
                    _degree,
                    _degreeNext,
                    fill=colours[_chordColour1 % 12],
                    outline=_lineColour,
                    width=_lineWidth,
                )

        # Draw Polygon
        _poly = circle.getPolyCircle(returnPoly=True, scale=1)

        if not _poly is None:
            if not useVector:
                Graphics.drawFatPolygonToIm(
                    im, _poly, outline=_lineColourInv, width=_lineWidth
                )
            else:

                _polypath = path.path()
                _polypath.append(path.moveto(_poly[0][0], -_poly[0][1]))

                for point in _poly[1:]:
                    _polypath.append(path.lineto(point[0], -point[1]))
                if type(_polypath[-1]) is path.lineto:
                    _polypath.append(path.closepath())
                """im.stroke(_polypath, [
                    color.rgb(_lineColourInv[0] / 255, _lineColourInv[1] / 255, _lineColourInv[2] / 255),
                    style.linewidth(_lineWidthVector),
                    ])])"""

                # im.fill(_polypath,[color.rgb(lineColour[0] / 255, lineColour[1] / 255, lineColour[2] / 255)])
                # im.fill(_polypath, [color.rgb(0, 0, 1),style.linejoin.round])

                if (
                    _lineColour[0] / 255,
                    _lineColour[1] / 255,
                    _lineColour[2] / 255,
                ) not in ((0, 0, 0), (1, 1, 1)):
                    print(
                        _lineColour[0] / 255, _lineColour[1] / 255, _lineColour[2] / 255
                    )
                    input("Silly things")
                im.draw(
                    _polypath,
                    [
                        (
                            color.rgb(
                                _lineColourInv[0] / 255,
                                _lineColourInv[1] / 255,
                                _lineColourInv[2] / 255,
                            )
                            if _lineColourInv != FCircle.lineColourInv
                            else color.rgb(1, 0.99999, 1)
                        ),
                        style.linewidth(_lineWidthVector),
                        style.linejoin.round,
                        deco.stroked(),
                        deco.filled(
                            [
                                (
                                    color.rgb(
                                        _lineColour[0] / 255.0,
                                        _lineColour[1] / 255.0,
                                        _lineColour[2] / 255.0,
                                    )
                                    if _lineColour != FCircle.lineColourInv
                                    else color.rgb(1, 0.99999, 1)
                                )
                            ]
                        ),
                    ],
                )

        if len(circle.change) in (0, 1):

            # input('{} {} {}'.format(circle.x, math.cos(_degrees[0]),artCircleProportion))
            _artCircleR = artCircleProportion * circle.r
            if len(circle.change) == 0:
                _artCircleX = circle.x
            else:
                _artCircleX = circle.x + math.cos(math.radians(_degrees[0])) * (
                    circle.r - _artCircleR
                )

            if useVector:
                _artCircleLineWidth = _lineWidthEllipseVector * artCircleProportion
                if len(circle.change) == 0:
                    _artCircleY = -circle.y
                else:
                    _artCircleY = -circle.y - math.sin(math.radians(_degrees[0])) * (
                        circle.r - _artCircleR
                    )
            else:
                _artCircleLineWidth = _lineWidth * artCircleProportion
                if len(circle.change) == 0:
                    _artCircleY = circle.y
                else:
                    _artCircleY = circle.y + math.sin(math.radians(_degrees[0])) * (
                        circle.r - _artCircleR
                    )

            if (len(circle.change)) == 1:
                if invertColour:
                    _artCircleRGB = coloursInv[
                        circle.change.notes[0].semitonesFromOne()
                    ]
                else:
                    _artCircleRGB = colours[circle.change.notes[0].semitonesFromOne()]
            else:
                if invertColour:
                    _artCircleRGB = circleBGColourInv
                else:
                    _artCircleRGB = circleBGColour
            # input('coloursInv:\n{}\ncolours:\n{}'.format(coloursInv,colours))

            _artCircleRed = _artCircleRGB[0] / 255
            _artCircleGreen = _artCircleRGB[1] / 255
            _artCircleBlue = _artCircleRGB[2] / 255
            _artCircleLineRGB = _lineColour
            _artCircleLineRed = _artCircleLineRGB[0] / 255
            _artCircleLineGreen = _artCircleLineRGB[1] / 255
            _artCircleLineBlue = _artCircleLineRGB[2] / 255
            c = 0
            while _artCircleR >= FCircle.minimumCirclePixels:
                c += 1
                if len(circle.change) == 1:
                    if c % 2 == 0:
                        if c % 4 == 0:
                            _artCircleRGB = circleBGColour
                            _artCircleLineRGB = _lineColour
                        else:
                            _artCircleRGB = circleBGColourInv
                            _artCircleLineRGB = _lineColourInv
                    else:
                        if c % 4 == 1:
                            _artCircleRGB = _lineColourInv
                            _artCircleLineRGB = _lineColour
                        else:
                            _artCircleRGB = _lineColour
                            _artCircleLineRGB = _lineColourInv
                else:  # Receptive Receptivity
                    if c % 2 == 0:
                        if invertColour:
                            l, d = 0, 255
                        else:
                            l, d = 255, 0
                        if c % 4 == 0:
                            _artCircleRGB = (d, d, d)
                            _artCircleLineRGB = (l, l, l)
                        else:
                            _artCircleRGB = (l, l, l)
                            _artCircleLineRGB = (d, d, d)
                    else:
                        if c % 4 == 1:
                            _artCircleRGB = Colour.getTransposedColours(
                                greyScale=True, invertColour=not invertColour
                            )[0]
                            _artCircleLineRGB = _lineColour

                        else:
                            _artCircleRGB = Colour.getTransposedColours(
                                greyScale=True, invertColour=invertColour
                            )[0]
                            _artCircleLineRGB = _lineColourInv

                if _artCircleRGB[:3] == (255, 255, 255):
                    _artCircleRGB = (255, 254, 254)
                if _artCircleLineRGB[:3] == (255, 255, 255):
                    _artCircleLineRGB = (255, 254, 254)
                _artCircleRed = _artCircleRGB[0] / 255
                _artCircleGreen = _artCircleRGB[1] / 255
                _artCircleBlue = _artCircleRGB[2] / 255
                _artCircleLineRed = _artCircleLineRGB[0] / 255
                _artCircleLineGreen = _artCircleLineRGB[1] / 255
                _artCircleLineBlue = _artCircleLineRGB[2] / 255

                # print('Using {} Drew circle at {},{} with \nr={}\nfillclr:{}'.format(
                #    'vector' if useVector else 'bitmap',_artCircleX, _artCircleY, _artCircleR,_artCircleRGB))

                if useVector:
                    """im.stroke(path.circle(_artCircleX, _artCircleY, _artCircleR),
                    [style.linewidth(_artCircleLineWidth),
                     color.rgb(_artCircleLineRed, _artCircleLineGreen, _artCircleLineBlue),

                     ])"""
                    im.fill(
                        path.circle(_artCircleX, _artCircleY, _artCircleR),
                        [
                            style.linewidth(_artCircleLineWidth),
                            color.rgb(_artCircleRed, _artCircleGreen, _artCircleBlue),
                        ],
                    )
                    """im.draw(path.circle(_artCircleX, _artCircleY, _artCircleR),
                            [
                                color.rgb(_artCircleRed, _artCircleRed,
                                           _artCircleRed) ,
                                deco.stroked(),
                                deco.filled(
                                    [color.rgb(_artCircleRed, _artCircleGreen,
                                                _artCircleBlue)
                                          ]
                                )])"""
                else:
                    try:
                        Graphics.ellipse(
                            im=im,
                            xy=[
                                _artCircleX - _artCircleR,
                                _artCircleY - _artCircleR,
                                _artCircleX + _artCircleR,
                                _artCircleY + _artCircleR,
                            ],
                            fill=_artCircleRGB,
                            outline=_artCircleLineRGB,
                            width=_artCircleLineWidth,
                        )
                    except:
                        raise TypeError("fuckers. here is the im: {}".format(im))
                _artCircleR *= artCircleProportion
                _artCircleLineWidth *= artCircleProportion
                if len(circle.change) == 1:
                    _artCircleX = circle.x + math.cos(math.radians(_degrees[0])) * (
                        circle.r - _artCircleR
                    )
                    if useVector:
                        _artCircleY = -circle.y - math.sin(
                            math.radians(_degrees[0])
                        ) * (circle.r - _artCircleR)
                    else:
                        _artCircleY = circle.y + math.sin(math.radians(_degrees[0])) * (
                            circle.r - _artCircleR
                        )

        if displayCircle and not useVector:
            im.show()
        if type(im) is PIL.Image.Image:
            pass
        elif type(im) is pyx.canvas.canvas:
            pass
        else:
            raise TypeError(
                "im got currupted PIL.Image or canvas.canvas from pyx, not {}".format(
                    type(im)
                )
            )

        return im


    @classmethod
    def renderSCircle(cls,*args,**kwargs):
        kwargs['circleType'] = 'SCircle'
        #assert 'change' in kwargs
        return cls.renderFCircle(*args,**kwargs)

    
    @classmethod
    def renderFCircle(
        cls,
        change: Change,
        resolution: int = 128,
        circleType="FCircle",
        includeBGCircle=True,
        canvasBGColour=None,
        circleBGColour=None,
        lineColour=None,
        chordAlpha=255,  # .0125
        lineAdjust=0.5,
        minimumRadiusToGetOulined=30,
        fractality=None,
        minimumPixelsOfCircle=3,
        rootColourKey: str = None,
        invertColour=False,
        greyScale=False,
        alternateBG=None,
        includeTrigram=None,
        saveOnlyOneKey=None,
        filetypes=["pdf"],
        returnAsPyXCanvas=False,
        skipIfFileExists=False,
        externalGraphicsPath=False,
    ):

        assert not returnAsPyXCanvas
        if skipIfFileExists and not returnAsPyXCanvas:
            filesStatus = []
            colourKeys = [rootColourKey]
            if not saveOnlyOneKey:
                colourKeys = Key.allFlats
            for filetype in filetypes:
                for key in colourKeys:
                    __path = Graphics.getDiagramPath(
                        change=change,
                        key=key,
                        diagramType=circleType,
                        resolution=resolution,
                        greyScale=greyScale,
                        invertColour=invertColour,
                        externalGraphicsPath=externalGraphicsPath,
                        filetype=filetype,
                        includeFileExtension=True,
                        warnOnFileNotFound=False,
                        tryToReplaceMissingWithRootKey=False,
                        
                    )

                    if os.path.isfile(__path) and os.path.getsize(__path) > 0:
                        filesStatus.append(1)
                    else:
                        filesStatus.append(0)
            if all([f for f in filesStatus]):
                return True
        if circleType == "SCircle":
            includeRCircle = False
            useChordCircles = True
            _FCircleClassSettings = {}
            property_names = [
                p
                for p in dir(FCircle)
                if any(
                    [
                        isinstance(getattr(FCircle, p), t) and "__" not in p
                        for t in (list, int, float, tuple, str)
                    ]
                )
            ]
            for k in property_names:
                _FCircleClassSettings[k] = getattr(FCircle, k)
            _GraphicsClassSettings = {}
            property_names = [
                p
                for p in dir(Graphics)
                if any(
                    [
                        isinstance(getattr(Graphics, p), t) and "__" not in p
                        for t in (list, int, float, tuple, str)
                    ]
                )
            ]
            for k in property_names:
                _GraphicsClassSettings[k] = getattr(Graphics, k)
            FCircle.proportion = 1
            FCircle.lineProportion = 0.0001
            # print('\n'.join([k + ' ' + str(_GraphicsClassSettings[k]) for k in _GraphicsClassSettings]))
            # input('\n'.join([k + ' ' + str(_FCircleClassSettings[k]) for k in _FCircleClassSettings]))
            if alternateBG is None:
                alternateBG = False
        elif circleType == "FCircle":
            includeRCircle = True
            useChordCircles = False
            if alternateBG is None:
                alternateBG = True
        if includeTrigram is None:
            includeTrigram = False
        if saveOnlyOneKey is None:
            saveOnlyOneKey = False
            if returnAsPyXCanvas:
                saveOnlyOneKey = True
            # saveOnlyOneKey = resolution >= saveOnlyOneKeyIfResolutionExceeds
        # input('in renderFCircle. alternateBG = {}'.format(alternateBG))
        if not saveOnlyOneKey:
            if rootColourKey != "C":
                # raise ValueError('I am pretty sure that saving in all keys requires that we start in C.')
                print(
                    "changing rootColourKey to C because saveOnlyOneKey ==",
                    saveOnlyOneKey,
                )
                rootColourKey = "C"

        for i in filetypes:
            if not i in Graphics.vectorFiletypes and i != "png":
                raise ValueError(
                    "All of {} should be in {}".format(
                        filetypes, Graphics.vectorFiletypes + ["png"]
                    )
                )

        _usingVector = (
            any([i in Graphics.vectorFiletypes for i in filetypes]) or returnAsPyXCanvas
        )
        _usingRaster = "png" in filetypes
        lineProportion = FCircle.lineProportion
        _lineWidth = resolution / 2 * lineProportion

        _lineWidth = int(max(_lineWidth, 1))

        # Default colours
        if canvasBGColour is None:
            canvasBGColour = FCircle.canvasBGColour
        if circleBGColour is None:
            circleBGColour = FCircle.circleBGColour
            circleBGColourInverted = FCircle.circleBGColourInv
        if lineColour is None:
            if not invertColour:
                lineColour = FCircle.lineColour
                lineColourInverted = FCircle.lineColourInv
            elif invertColour:
                lineColour = FCircle.lineColourInv
                lineColourInverted = FCircle.lineColour
        if resolution == 0:
            raise ValueError("resolution must be greater than 0.")
        # Colours are 12
        if JazzNote.isAlphabetNoteStr(rootColourKey) or rootColourKey == "BW":
            pass
        else:
            raise TypeError(
                "rootColourKey is to be provided in alphaBetNote. BW for black and white, is depracated. "
                + str(rootColourKey)
            )

        _rootColourTranspose = JazzNote.distanceFromC(rootColourKey)

        _colours = Colour.getTransposedColours(
            colourTranspose=_rootColourTranspose,
            greyScale=greyScale,
            invertColour=False,
        )

        _coloursInverted = Colour.getTransposedColours(
            colourTranspose=_rootColourTranspose, greyScale=greyScale, invertColour=True
        )

        _rootR = resolution / 2
        _rootFCircle = FCircle(
            centre=[_rootR, _rootR],
            r=_rootR,
            change=change,
            colourTranspose=_rootColourTranspose,
            invertBG=False,
        )
        if _usingVector:

            _colourSchemes = []
            path = pyx.path
            color = pyx.color
            canvas = pyx.canvas
            for k in JazzNote.noteNameFlats:
                if k == rootColourKey or not saveOnlyOneKey:
                    for g in (True, False):
                        for invertColour in (False, True):
                            if not (g == True and k != "C"):
                                _colourSchemes.append(
                                    {
                                        "key": k,
                                        "greyScale": g,
                                        "invertColour": invertColour,
                                        "canvas": pyx.canvas.canvas(),
                                        "rootFCircle": FCircle(
                                            centre=[_rootR, _rootR],
                                            r=_rootR,
                                            change=change,
                                            colourTranspose=0,  # JazzNote.distanceFromC(k),
                                            invertBG=False,
                                        ),
                                    }
                                )
                                for filetype in filetypes:
                                    _colourSchemes[-1][
                                        "pathname" + filetype
                                    ] = Graphics.getFCirclePath(
                                        circleType=circleType,
                                        change=change,
                                        colourKey=k,
                                        resolution=resolution,
                                        includeFilename=False,
                                        greyScale=g,
                                        invertColour=invertColour,
                                        filetype=filetype,
                                        externalGraphicsPath=externalGraphicsPath
                                    )

                                    _colourSchemes[-1][
                                        "fullname" + filetype
                                    ] = Graphics.getFCirclePath(
                                        circleType=circleType,
                                        change=change,
                                        colourKey=k,
                                        resolution=resolution,
                                        includeFilename=True,
                                        greyScale=g,
                                        invertColour=invertColour,
                                        filetype=filetype,
                                        externalGraphicsPath=externalGraphicsPath
                                    )
                                    _colourSchemes[-1][
                                        "filename" + filetype
                                    ] = Graphics.getCircleFilename(
                                        circleType=circleType,
                                        change=change,
                                        colourKey=k,
                                        resolution=resolution,
                                        invertColour=invertColour,
                                        greyScale=g,
                                        filetype=filetype,
                                        
                                    )

        # for i in _colourSchemes: print(i)
        # input('press blayh to continue')
        # input('_colourSchemes is {}'.format(_colourSchemes))
        # _colours = [Colour.modifyAlphaChannelOfRGBATuple(i, chordAlpha) for i in _colours]

        # _filename = 'Circle ' + str(
        #    change.getChangeNumber(addOneToBookPage=True, decorateChapter=False)) + ' in '+rootColourKey+ ".png"
        if True or _usingRaster:
            _filename = Graphics.getCircleFilename(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                invertColour=invertColour,
                greyScale=greyScale,
                filetype="png",
            )
            _pathname = Graphics.getFCirclePath(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                includeFilename=False,
                invertColour=invertColour,
                greyScale=greyScale,
                externalGraphicsPath=externalGraphicsPath
            )
            _fullname = Graphics.getFCirclePath(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                includeFilename=True,
                invertColour=invertColour,
                greyScale=greyScale,
                externalGraphicsPath=externalGraphicsPath
            )

        if True or "pdf" in filetypes:
            _filenamepdf = Graphics.getCircleFilename(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                invertColour=invertColour,
                greyScale=greyScale,
                filetype="pdf",
            )

            _pathnamepdf = Graphics.getFCirclePath(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                includeFilename=False,
                invertColour=invertColour,
                greyScale=greyScale,
                filetype="pdf",
                externalGraphicsPath=externalGraphicsPath
            )
            _fullnamepdf = Graphics.getFCirclePath(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                includeFilename=True,
                invertColour=invertColour,
                greyScale=greyScale,
                filetype="pdf",
                externalGraphicsPath=externalGraphicsPath
            )

        if True or "eps" in filetypes:
            _pathnameeps = Graphics.getFCirclePath(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                includeFilename=False,
                invertColour=invertColour,
                greyScale=greyScale,
                filetype="eps",
                externalGraphicsPath=externalGraphicsPath
            )

            _fullnameeps = Graphics.getFCirclePath(
                circleType=circleType,
                change=change,
                colourKey=rootColourKey,
                resolution=resolution,
                includeFilename=True,
                invertColour=invertColour,
                greyScale=greyScale,
                filetype="eps",
                externalGraphicsPath=externalGraphicsPath
            )

        # _rootChords = _rootFCircle.getChordCrops()
        # print('_rootChords',_rootChords)

        _rootInners = _rootFCircle.getInnerCircles(
            invertBG=alternateBG,
            useRingCircles=includeRCircle,
            useChordCircles=useChordCircles,
            circleType=circleType,
        )
        # input('bblargg\nrootFCircle {}\nrootInners {}'.format(
        #    _rootFCircle,_rootInners))

        """print('_rootInners',_rootInners,
              'rootFCircle',_rootFCircle,
              'change',change)"""

        if fractality is None:
            if len(_rootInners) > 0:
                fractality = Graphics.iterationsToConvergence(
                    _rootR * FCircle.proportion,
                    max([i.r for i in _rootInners]),
                    minimumPixelsOfCircle,
                )

        if len(_rootInners) == 0:
            fractality = 1
        if _usingRaster:
            _rootIm = Image.new("RGBA", (resolution, resolution), canvasBGColour)
        if _usingVector or returnAsPyXCanvas:
            _rootCanvas = pyx.canvas.canvas()
            # trafoScale = trafo.scale(sx=1, sy=1, x=0, y=0)
            trafoScale = pyx.trafo.scale(
                sx=32 / resolution, sy=32 / resolution, x=0, y=0
            )
        ####### Boundary invisible
        # boundsSize = _rootFCircle.r / FCircle.proportion / 2
        boundsSize = _rootFCircle.r / FCircle.proportion

        # _rootIm = Image.new('P', (resolution, resolution), canvasBGColour)
        # _rootDraw = ImageDraw.Draw(_rootIm)

        if includeBGCircle == True:
            if _usingRaster:
                if _rootIm is None:
                    raise ValueError("shittty poop")
                Graphics.drawFCircleToIm(
                    _rootFCircle,
                    _rootIm,
                    lineProportion=lineProportion,
                    lineAdjust=lineAdjust,
                    greyScale=greyScale,
                    invertColour=not invertColour,
                )
            if _usingVector:
                """Graphics.drawFCircleToIm(
                    _rootFCircle, im=_rootCanvas,
                    lineProportion=lineProportion,
                    lineAdjust=lineAdjust,
                    greyScale=greyScale,
                )"""
                for c, colourScheme in enumerate(_colourSchemes):

                    Graphics.drawFCircleToIm(
                        circle=colourScheme["rootFCircle"],
                        im=colourScheme["canvas"],
                        lineProportion=lineProportion,
                        lineAdjust=lineAdjust,
                        greyScale=colourScheme["greyScale"],
                        invertColour=colourScheme["invertColour"],
                        colourTranspose=JazzNote.distanceFromC(colourScheme["key"]),
                        alternateBG=alternateBG,
                        circleType=circleType,
                    )

                    if includeRCircle:
                        colourScheme["canvas"] = Graphics.drawRCircleToIm(
                            circle=_rootFCircle,
                            im=colourScheme["canvas"],
                            lineProportion=lineProportion,
                            lineAdjust=lineAdjust,
                            greyScale=colourScheme["greyScale"],
                            invertColour=colourScheme["invertColour"],
                            colourTranspose=JazzNote.distanceFromC(
                                colourScheme["key"]
                            ),  # HERE
                        )
            # input('eh buddy ' + str(type(_rootCanvas)))
        if includeRCircle:
            if _usingRaster:
                _rootIm = Graphics.drawRCircleToIm(
                    _rootFCircle,
                    _rootIm,
                    lineProportion=lineProportion,
                    lineAdjust=lineAdjust,
                    greyScale=greyScale,
                )

        if _usingRaster:
            _bIm = _rootIm
        _bInners = np.array(_rootInners)
        # _bInners = _rootInners
        _lessThanTwoNotes = False
        # TODO: doesnt work with vector and vector colour schemes
        if includeTrigram:
            _rootFCircle.drawTrigrams(
                _rootIm,
                colours=_colours,
                lineColour=lineColour,
                thickness=resolution / 31,
            )

        _startTime = datetime.datetime.now()
        _startTimeFractalLevel = datetime.datetime.now()
        _lastNumberOfCircles = 0
        _totalNumberOfCircles = 0
        # print('starting:', _fullname.replace('/', '\\'), 'at', _startTime, " it's saving as:", _filename, '\nat',
        #   _pathname)

        for f in range(fractality):

            _fInners = np.array([])
            if _usingRaster:
                _fIm = Image.new(
                    "RGBA", (resolution, resolution), FCircle.canvasBGColour
                )
            print(
                "{} {} for {} ({}), fractality: {}/{}. {}% done. {}px key of {}. {} circles this round. {} minutes spent last level at {} circles/s. Made {} circles total.".format(
                    datetime.datetime.now(),
                    circleType,
                    change.getScaleNames()[0],
                    change.getChangeNumber(addOneToBookPage=True),
                    f,
                    fractality,
                    round(100 * f / fractality, 2),
                    resolution,
                    rootColourKey,
                    len(_bInners),
                    round(
                        (datetime.datetime.now() - _startTimeFractalLevel).seconds / 60,
                        2,
                    ),
                    round(
                        _lastNumberOfCircles
                        / max(
                            (datetime.datetime.now() - _startTimeFractalLevel).seconds,
                            1,
                        ),
                        2,
                    ),
                    _totalNumberOfCircles,
                )
            )
            _startTimeFractalLevel = datetime.datetime.now()
            _lastNumberOfCircles = len(_bInners)
            _totalNumberOfCircles += _lastNumberOfCircles
            # print(_bInners)

            if len(_bInners) > 0:
                for bCircleIdx, bCircle in enumerate(_bInners):
                    # print('drawing circle #',bCircleIdx)
                    if _usingRaster:
                        Graphics.drawFCircleToIm(
                            circle=bCircle,
                            im=_fIm,
                            lineProportion=lineProportion,
                            lineAdjust=lineAdjust,
                            greyScale=greyScale,
                        )

                    if _usingVector:
                        """Graphics.drawFCircleToIm(circle=bCircle, im=_rootCanvas,
                        lineProportion=lineProportion,
                        lineAdjust=lineAdjust,
                        greyScale=greyScale)"""
                        # input(bCircle.__repr__())
                        for c, colourScheme in enumerate(_colourSchemes):
                            Graphics.drawFCircleToIm(
                                circle=bCircle,
                                im=_colourSchemes[c]["canvas"],
                                lineProportion=lineProportion,
                                lineAdjust=lineAdjust,
                                greyScale=_colourSchemes[c]["greyScale"],
                                invertColour=colourScheme["invertColour"],
                                colourTranspose=JazzNote.distanceFromC(
                                    colourScheme["key"]
                                ),
                                circleType=circleType,
                            )

                    # print('getting inner circles')

                    _fInners = np.concatenate(
                        [
                            _fInners,
                            bCircle.getInnerCircles(
                                invertBG=alternateBG,
                                useRingCircles=includeRCircle,
                                useChordCircles=useChordCircles,
                                circleType=circleType,
                            ),
                        ]
                    )
                    # print('done getting inner circles {}'.format(_fInners))

                    """if len(_fInners) > 1:
                        for innerbCircle in _fInners:
                            #print('innerbCircle',innerbCircle)
                            _bInners.append(innerbCircle)"""
                del _bInners
                #gc.collect()
            _bInners = _fInners
            del _fInners  # UNTESTED
            #gc.collect()
            # _bIm.paste(_fIm,(0,0),_fIm)
            if _usingRaster:
                _bIm.paste(_fIm, (0, 0), mask=_fIm)

            # _finalIm = Image.new("RGBA", _bIm.size)
            # _finalIm = Image.alpha_composite(_finalIm, _bIm)
            # _finalIm = Image.alpha_composite(_finalIm, _fIm)
            # _bIm = _finalIm
        # _bIm.alpha_composite(_fIm, dest=(0, 0), source=(0, 0))
        # _bIm.alpha_composite(_fIm, dest=(0, 0), source=(0, 0))
        # _bIm = Image.blend(_bIm,_fIm,0.5)
        # _bIm = Image.blend(_bIm,_fIm,0.5)
        # _bIm.show()
        # input('check the image')
        for pathname in [_pathname, _pathnamepdf, _pathnameeps]:
            if os.path.isdir(pathname):
                pass
            else:
                if (
                    pathname == _pathnamepdf
                    and resolution not in FCircle.vectorSaveResolutions
                    and not "pdf" in filetypes
                ):
                    pass
                elif (
                    pathname == _pathnameeps
                    and resolution not in FCircle.vectorSaveResolutions
                    and not "eps" in filetypes
                ):
                    pass
                else:

                    if (
                        ("pdf" in pathname and "pdf" in filetypes)
                        or ("png" in pathname and "png" in filetypes)
                        or ("svg" in pathname and "svg" in filetypes)
                    ):
                        Utility.makeDirectory(pathname)

        if not saveOnlyOneKey:
            if rootColourKey != "C":
                raise TypeError(
                    "This colour shift thing starts in C. Not {}. saveOnlyOneKey={}\nFCircle{}".format(
                        rootColourKey, saveOnlyOneKey, _fullname
                    )
                )

            if invertColour == True:

                print("set invertColour to False because saveOnlyOneKey is True.")
                invertColour == False
        if "png" in filetypes:
            for greyScale in (False, True):

                if saveOnlyOneKey:
                    _keysToRender = [rootColourKey]
                else:
                    _keysToRender = JazzNote.noteNameFlats
                for i, key in enumerate(_keysToRender):
                    for colourInversion in (False, True):
                        if greyScale:
                            _coloursNew = Colour.getTransposedColours(
                                colourTranspose=0,
                                greyScale=greyScale,
                                invertColour=colourInversion,
                            )
                            _coloursNewInv = Colour.getTransposedColours(
                                colourTranspose=0,
                                greyScale=greyScale,
                                invertColour=not colourInversion,
                            )
                        else:
                            if colourInversion:
                                _coloursNew = _coloursInverted[:]
                                _coloursNewInv = _colours[:]
                            else:
                                _coloursNew = _colours[:]
                                _coloursNewInv = _coloursInverted[:]
                        for t in range(i):
                            _coloursNew.append(_coloursNew.pop(0))
                        _transposedImage = Graphics.changeColourSchemeOfImg(
                            _rootIm,
                            _colours + _coloursInverted,
                            _coloursNew + _coloursNewInv,
                        )
                        if colourInversion:
                            _transposedImage = Graphics.changeColourSchemeOfImg(
                                _transposedImage,
                                [lineColour, lineColourInverted],
                                [lineColourInverted, lineColour],
                            )

                        _transposedPath = Graphics.getFCirclePath(
                            circleType=circleType,
                            change=change,
                            colourKey=key,
                            resolution=resolution,
                            invertColour=colourInversion,
                            greyScale=greyScale,
                            filetype="png",
                            includeFilename=False,
                            externalGraphicsPath=externalGraphicsPath
                        )
                        _transposedName = Graphics.getFCirclePath(
                            circleType=circleType,
                            change=change,
                            colourKey=key,
                            resolution=resolution,
                            invertColour=colourInversion,
                            greyScale=greyScale,
                            includeFilename=True,
                            filetype="png",
                            externalGraphicsPath=externalGraphicsPath
                        )

                        if os.path.isdir(_transposedPath):
                            pass
                        else:
                            print("transposed path file:///{}".format(_transposedPath))

                            Utility.makeDirectory(_transposedPath)
                            print("creating file:///", _transposedPath)
                        _transposedImage = _transposedImage.convert(
                            "P", palette=Image.ADAPTIVE, colors=15
                        )
                        _transposedImage.save(
                            Graphics.getFCirclePath(
                                circleType=circleType,
                                change=change,
                                colourKey=key,
                                resolution=resolution,
                                invertColour=colourInversion,
                                greyScale=greyScale,
                                includeFilename=True,
                                externalGraphicsPath=externalGraphicsPath
                            )
                        )

                        print(
                            "finished transposing colourKey: file:///",
                            _transposedName,
                            sep="",
                        )

            """for colourScheme in _colourSchemes:
                c = colourScheme['canvas']
                Graphics.drawRCircleToIm(
                    circle=_rootFCircle, im=c,
                    lineProportion=lineProportion,
                    lineAdjust=lineAdjust,
                    greyScale=colourScheme['greyScale'],
                    invertColour=colourScheme['invertColour'],
                )"""

            _rootIm = _bIm.convert("P", palette=Image.ADAPTIVE, colors=26)
            _rootIm.save(_fullname, "PNG")

        if _usingVector:
            bounds = path.path()
            boundsL = _rootFCircle.x - boundsSize
            boundsR = _rootFCircle.x + boundsSize
            boundsT = -_rootFCircle.y - boundsSize
            boundsB = -_rootFCircle.y + boundsSize
            bounds.append(path.moveto(boundsL, boundsT))
            bounds.append(path.lineto(boundsR, boundsT))
            bounds.append(path.lineto(boundsR, boundsB))
            bounds.append(path.lineto(boundsL, boundsB))
            # bounds.append(path.lineto(boundsL, boundsT))
            bounds.append(path.closepath())
            for colourScheme in _colourSchemes:
                c = colourScheme["canvas"]

                c.stroke(bounds, [color.rgb(1, 0.9, 0.9), color.transparency(1)])  # ])

                sc = canvas.canvas()
                # sc.fill(bounds, [color.rgb(0, 0, 1),trafoScale])
                sc.insert(c, [trafoScale])
                # for i, canv in enumerate(canvases):
                #    canvases[i].stroke(bounds, [color.rgb(0, 0, 0), color.transparency(1)])

                if True or (resolution in FCircle.vectorSaveResolutions):
                    _saveSuccess = False

                    for filetype in Graphics.vectorFiletypes:
                        while not _saveSuccess:
                            try:
                                if filetype in filetypes:
                                    pathname = colourScheme["pathname" + filetype]
                                    fullname = colourScheme["fullname" + filetype]
                                    Utility.makeDirectory(pathname)
                                    timeBeforeSave = datetime.datetime.now()
                                    print(
                                        "!{} saving file:///{}".format(
                                            datetime.datetime.now(), fullname
                                        ),
                                        end=". ",
                                    )
                                    print('writing it once')
                                    sc.writePDFfile(fullname)
                                    filesize = os.path.getsize(fullname) / 1024**2
                                    print(
                                        "Done! It took {} to save a file of {} mB at {} mB/sec".format(
                                            datetime.datetime.now() - timeBeforeSave,
                                            round(filesize, 2),
                                            round(
                                                filesize
                                                / max(
                                                    1,
                                                    (
                                                        datetime.datetime.now()
                                                        - timeBeforeSave
                                                    ).seconds,
                                                ),
                                                2,
                                            ),
                                        )
                                    )
                                # del _colourSchemes[_colourSchemes.index(colourScheme)]['canvas']  # Does it still work?
                                _saveSuccess = True
                            except PermissionError as e:
                                print(
                                    e,
                                    "\nmaybe try closing the file if anything is accessing it. \nCheck windows explorer cause it does that if the file is highlighted. Press enter or whatever to try again. :)",
                                    end="",
                                )
                                input()
                            except MemoryError as e:
                                print(
                                    e,
                                    "\nWoah there pardner!! It seems you have filled that RAM up. Try again? :0",
                                    end="",
                                )
                                input()

            print("original render file:///{}".format(_fullnamepdf))
        if returnAsPyXCanvas or any([i in filetypes for i in Graphics.vectorFiletypes]):
            print('righting it twice here')
            sc = pyx.canvas.canvas()
            # input(_colourSchemes[-1]['canvas'])
            # _colourSchemes[-1]['canvas'].writePDFfile('C:\\Users\\Dre\\Desktop\\supergay')
            # input('supergay on desktop')
            # _rootCanvas.stroke(bounds, [color.rgb(0, 0, 0), color.transparency(1)])
            sc.insert(_colourSchemes[-1]["canvas"], [trafoScale])
            # rootcanvas used to work but I changed it to the colourschemes shit after for some reason


            if resolution in FCircle.vectorSaveResolutions:
                sc.writePDFfile(_fullnamepdf)
            if returnAsPyXCanvas:
                return sc

        if "png" in filetypes:
            del _transposedImage
            del _bIm
            del _rootIm
        # if _fIm != None: del _fIm
        if _usingVector:
            del _rootCanvas
        print(
            "finished it at",
            datetime.datetime.now(),
            "it took",
            datetime.datetime.now() - _startTime,
        )
        # Put Data back how it was after making SCircle with modified Graphics and FCircle settings
        if circleType == "SCircle":
            print(
                "putting settings back to default for FCircle cause they were changed on account of making SCircles."
            )
            for setting in _GraphicsClassSettings:
                setattr(Graphics, setting, _GraphicsClassSettings[setting])
            for setting in _FCircleClassSettings:
                setattr(FCircle, setting, _FCircleClassSettings[setting])
        if circleType != "FCircle":
            del _GraphicsClassSettings, _FCircleClassSettings

        # input('chick corea')

    @classmethod
    def renderEmptyCircleToFile(
        cls,
        rootColourKey,
        canvasSize: int,
        canvasBGColour=None,
        circleBGColour=None,
        invertedColours=None,
        lineColour=None,
    ):
        lineProportion = FCircle.lineProportion
        _lineWidth = canvasSize / 2 * lineProportion
        # Default colours
        if circleBGColour is None:
            circleBGColour = FCircle.circleBGColour
        if canvasBGColour is None:
            canvasBGColour = FCircle.canvasBGColour
        if invertedColours is None:
            invertedColours = Colour.getTransposedColours(invertColour=True)
        if lineColour is None:
            lineColour = FCircle.lineColour
        # trying to track down the wrong type of colour
        # if circleBGColour in ((0,0,0,255),(255,255,255,255)): raise TypeError('asdfasdfasdfasdf')
        # defualt for BW mode
        if rootColourKey == "BW":
            _colourTranspose = 0
        else:
            _colourTranspose = JazzNote.distanceFromC(rootColourKey)
        _change = Change([])
        _pathname = Graphics.getFCirclePath(
            _change, colourKey=rootColourKey, resolution=canvasSize
        )
        _rootIm = Image.new("RGBA", (canvasSize, canvasSize), canvasBGColour)
        _filename = Graphics.getCircleFilename(
            _change,
            colourKey=rootColourKey,
            resolution=canvasSize,
            invertedColours=invertedColours,
        )
        if os.path.isdir(_pathname):
            pass
        else:
            Utility.makeDirectory(_pathname)

        _fullname = Graphics.getFCirclePath(
            _change,
            colourKey=rootColourKey,
            resolution=canvasSize,
            includeFilename=True,
        )

        Graphics.drawFCircleToIm(
            FCircle(
                [canvasSize / 2, canvasSize / 2],
                canvasSize / 2,
                Change(["1"]),
                _colourTranspose,
            ),
            im=_rootIm,
            lineProportion=0.0125,
            lineAdjust=0.5,
            drawBlankCircle=True,
        )
        _rootIm.save(_fullname)
        print("finished with:", _fullname, "at", datetime.datetime.now())

    @classmethod
    def PROTOrenderCircleToFile(
        cls,
        change: Change,
        path="C:\\Users\\Edrihan\\PycharmProjects\\Grail Of Scale\\Graphics\\Circles\\",
        canvasSize=100,
        includeBGCircle=True,
        chordAlpha=100,
        lineProportion=0.0125,
        lineTarget=12,
        lineAdjust=0.5,
        maxIterations=99,
        minimumPixelsOfCircle=1,
        rootColourKey=None,
    ):

        _flatten = lambda l: [item for sublist in l for item in sublist]
        _colours = [
            Colour.rgbaTupleByDistance[i.semitonesFromOne() % 12] for i in change.notes
        ]
        _colours = [
            Colour.modifyAlphaChannelOfRGBATuple(i, chordAlpha) for i in _colours
        ]
        _coloursInverted = [
            Colour.rgbaTupleByDistance[i.semitonesFromOne() % 12]
            for i in change.getReverse().notes
        ]
        _coloursInverted = [
            Colour.modifyAlphaChannelOfRGBATuple(i, chordAlpha)
            for i in _coloursInverted
        ]
        if rootColourKey == None:
            rootColourKey = Book.rootColourKey
            # print('rootColourKey: {}'.format(rootColourKey))
        _colourTranspose = JazzNote.distanceFromC(rootColourKey)
        # print('colourTranspose: {}'.format(_colourTranspose))

        _filename = (
            path
            + "Circle no "
            + str(change.getChangeNumber(addOneToBookPage=True, decorateChapter=False))
            + ".png"
        )
        _bChange = change
        print("_bChange: {}".format(_bChange))

        _bPageNumber = _bChange.getChangeNumber(
            addOneToBookPage=True, decorateChapter=False
        )
        _bCircleSize = canvasSize / 2
        _bAngles = _bChange.getAngles(returnDegrees=False, repeatFirstResult=True)
        print(
            "_bAngles:",
            " ".join(
                _bChange.getAngles(
                    returnDegrees=False, repeatFirstResult=True, humanFormat=True
                )
            ),
        )

        # These will be in format ==    [[x,y] ,r]
        _bR = canvasSize / 2

        if len(change.notes) > 2:
            try:
                _bPoly = change.getPolygon(
                    change=change,
                    boundL=0,  # _circleMargin
                    boundT=0,  #
                    boundR=canvasSize,  # canvasSize-_circleMargin
                    boundB=canvasSize,
                    colourTranspose=_colourTranspose,
                    returnFCircle=True,
                    makeReverse=1,
                )

                print("_bPoly a: ", _bPoly)

                # if bounds are -1,-1,1,1 it will give a trig result, meaning that left is negative
                # To plot it normalised change to 0,0,1,1
                # _bPoly = polylabel.polylabel([change.getPolygon(True,0,0,1,1)],precision=1.0,with_distance=True)

                # _polygonCentre = ([canvasSize/2+_polygonCentre[0][0]*canvasSize/2,canvasSize/2+_polygonCentre[0][1]*canvasSize/2],_polygonCentre[1]*canvasSize/2)
                # _bPoly = [[_polygonCentre[0][0]*canvasSize,_polygonCentre[0][1]*canvasSize],_polygonCentre[1]*canvasSize]

                print("_bPoly b: ", _bPoly)
            except:
                # input('bPoly didnt happen')
                _bPoly = None
        else:
            _bPoly = None

        # input()

        _bChords = Graphics.getChordCentres(
            change=_bChange, R=_bR, returnFCircle=True, colourTranspose=_colourTranspose
        )
        print("_bChords:\n", "".join(str(_bChords)))

        # Beginning fractality

        # chord fractality
        _fractality = Graphics.iterationsToConvergence(
            _bR,
            max([i.r for i in _bChords]),
            minPixels=minimumPixelsOfCircle,
            maxIterations=maxIterations,
        )
        print("_fractality: {}".format(_fractality))

        # polygon fractality
        if not _bPoly is None:
            _fractality = max(
                _fractality,
                Graphics.iterationsToConvergence(
                    _bR,
                    _bPoly.r,
                    minPixels=minimumPixelsOfCircle,
                    maxIterations=maxIterations,
                ),
            )
        # Index of _fChords == level of fractality

        # Fractality is the number of iterations AFTER the first BEFORE convergence
        _fChords = [_bChords]
        for f in range(1, _fractality + 1):
            _fChords.append([])
            print(
                _filename, "building locations fractality = ", f, "\nf"
            )  # ,'chords:',_fChords)
            for bIdx, bChords in enumerate(_fChords[f - 1]):
                if type(bChords) != list:
                    _bChords = [bChords]
                else:
                    _bChords = bChord
                _newfpolys = None
                _newfchords = None
                for fIdx, bChord in enumerate(_bChords):
                    # print('f',f,'bChord', fIdx,bChord)#Graphics.getChordCentres(_bChange,bChord[1]))
                    # input()
                    _boundL = bChord.x - bChord.r
                    _boundR = bChord.x + bChord.r
                    _boundT = bChord.y - bChord.r
                    _boundB = bChord.y + bChord.r

                    for fLevel in range(f + 2):
                        pass  # if not type(_fChords[0]) == FCircle:
                        # _fChords=_flatten(_fChords)
                    _modeAdjust = fIdx - (len(_bChange) - 1) * bChord.mode
                    _newfchords = Graphics.getChordCentres(
                        _bChange.mode((_modeAdjust) % len(_bChange)),
                        bChord.r,
                        mode=_modeAdjust,
                        colourTranspose=bChord.colourTranspose + _modeAdjust,
                        returnFCircle=True,
                        topLeftOrigin=False,
                    )
                    # print('newf before:,',_newfchords)
                    _newfchords = [
                        i.movePosition(bChord.x - 2 * bChord.r, bChord.y - 2 * bChord.r)
                        for i in _newfchords
                    ]

                    if not _newfchords is None:
                        _newfpolys = []
                        for ___idx, chord in enumerate(_newfchords):
                            if chord.makeReverse == 1:
                                # _rChange = chord.change.mode(chord.mode%len(change)).getDownwardScale()
                                _rChange = chord.change.getReverse()
                            else:
                                _rChange = chord.change

                            _newfpolys.append(
                                chord.change.getPolygon(
                                    change=chord.change.getReverse(),
                                    boundL=chord.x - chord.r,
                                    boundT=chord.y - chord.r,
                                    boundR=chord.x + chord.r,
                                    boundB=chord.y + chord.r,
                                    returnFCircle=True,
                                    mode=chord.mode,
                                    makeReverse=(chord.makeReverse + 0) % 2,
                                    colourTranspose=chord.colourTranspose,
                                )
                            )
                            if not _newfpolys[-1] is None:
                                # _newfpolys[-1] = _newfpolys[-1].movePosition(chord.x,chord.y)
                                _newfpolys[-1] = _newfpolys[-1].movePosition(
                                    chord.x - 1 * chord.r, chord.y - 1 * chord.r
                                )

                    # Use this next one for interesting shapes
                    # _newfchords = [i.movePosition(bChord.x-2*bChord.r  ,bChord.y-2*bChord.r) for i in _newfchords]

                    # print('newf after:',_newfchords)

                    # print('newf'+str(_newfchords)+'bchord'+str(bChord))

                    _fChords[-1] = _fChords[-1] + [
                        i for i in _newfchords if i.r > minimumPixelsOfCircle
                    ]
                    if (
                        not _newfpolys is None
                        and not _newfchords is None
                        and not None in _newfpolys
                    ):
                        print(_newfpolys)
                        _fChords[-1] = _fChords[-1] + [
                            i for i in _newfpolys if i.r > minimumPixelsOfCircle
                        ]

            # print('_fChords',Graphics.getChordCentres(_bChange,bChord.r,returnFCircle=True,humanOutput=True))

        print("_fChords, numbering {}: {}".format(len(_fChords), _flatten(_fChords)))
        print("blast")
        """for f in range(len(_fChords)):

            print (f)#,_fChords[f])

            for i in _fChords[f]:
                print(i)"""

        im = Image.new("RGBA", (canvasSize, canvasSize), (0, 255, 0, 0))

        # non fractal start
        draw = ImageDraw.Draw(im)
        draw.ellipse([0, 0, canvasSize, canvasSize], fill="black")
        _bDegrees = change.getAngles(
            returnDegrees=True, repeatFirstResult=True, goQuarterTurnAnticlockwise=True
        )

        _bPDegrees = change.getReverse().getAngles(
            returnDegrees=True, repeatFirstResult=True, goQuarterTurnAnticlockwise=True
        )
        for d in range(len(_bDegrees) - 1):
            draw.chord(
                [0, 0, canvasSize, canvasSize],
                _bDegrees[d],
                _bDegrees[d + 1],
                fill=_colours[d],
                outline="black",
                width=2,
            )
        # input('_bPoly about to start drawing {}'.format(_bPoly))
        if not _bPoly is None:

            draw.ellipse(
                [
                    _bPoly.x - _bPoly.r,
                    _bPoly.y - _bPoly.r,
                    _bPoly.x + _bPoly.r,
                    _bPoly.y + _bPoly.r,
                ],
                fill="black",
                outline="black",
            )

            for d in range(len(_bPDegrees) - 1):
                draw.chord(
                    [
                        _bPoly.x - _bPoly.r,
                        _bPoly.y - _bPoly.r,
                        _bPoly.x + _bPoly.r,
                        _bPoly.y + _bPoly.r,
                    ],
                    _bPDegrees[d],
                    _bPDegrees[d + 1],
                    fill=_coloursInverted[d],
                    outline="white",
                )

        # non fractal end

        for f in range(_fractality):
            print("still printing", _filename, "f", f, "/", _fractality)
            for bMode, chord in enumerate(_fChords[f]):
                # TODO: replace black with the change's composite colour
                _bDegrees = chord.change.mode((0) % len(change)).getAngles(
                    returnDegrees=True,
                    repeatFirstResult=True,
                    goQuarterTurnAnticlockwise=True,
                )

                if chord.r > minimumPixelsOfCircle:
                    draw.ellipse(
                        [
                            chord.x - chord.r,
                            chord.y - chord.r,
                            chord.x + chord.r,
                            chord.y + chord.r,
                        ],
                        fill="black",
                        outline="black",
                    )

                    # _fDegrees = chord.change.mode((fMode)%len(change)).getAngles(returnDegrees=True, repeatFirstResult=True,
                    #                                      goQuarterTurnAnticlockwise=True)

                    for d in range(len(_bDegrees) - 1):
                        # _fDegrees = chord.change.mode((d)%len(chord.change)).getAngles(returnDegrees=True,repeatFirstResult=True,goQuarterTurnAnticlockwise=True)
                        _fDegrees = chord.change.mode(
                            (0) % len(chord.change)
                        ).getAngles(
                            returnDegrees=True,
                            repeatFirstResult=True,
                            goQuarterTurnAnticlockwise=True,
                        )

                        draw.chord(
                            [
                                chord.x - chord.r,
                                chord.y - chord.r,
                                chord.x + chord.r,
                                chord.y + chord.r,
                            ],
                            _fDegrees[(d + 0) % len(_fDegrees)],
                            _fDegrees[(d + 1) % len(_fDegrees)],
                            fill=_colours[(d + chord.colourTranspose) % len(_colours)],
                            outline="black",
                            width=2,
                        )

            # Clear up some memory
            # if f >2:
            #    del _fChords[f-2]

        #   _fChords.append() #This is where I left off

        im.save(_filename)
        print("Circles saved to", _filename, "at", datetime.datetime.now())
        return True
        input("holy quacamole")

        _radiansTurned = change.getAngles(goQuarterTurnAnticlockwise=False)
        _colours = [
            Colour.rgbaTupleByDistance[i.semitonesFromOne() % 12] for i in change.notes
        ]
        _colours = [
            Colour.modifyAlphaChannelOfRGBATuple(i, chordAlpha) for i in _colours
        ]
        _polygon = change.getPolygon(
            boundL=_circleMargin,  # _circleMargin
            boundT=_circleMargin,  #
            boundR=canvasSize - _circleMargin,  # canvasSize-_circleMargin
            boundB=canvasSize - _circleMargin,
        )

        im = Image.new("RGBA", (canvasSize, canvasSize), (0, 255, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.ellipse([0, 0, canvasSize, canvasSize], fill="black")

        for d in range(len(_degrees) - 1):
            # print(_colours[d])
            # This is the nonfractal one
            draw.chord(
                [
                    canvasSize - _circleSize,
                    canvasSize - _circleSize,
                    _circleSize,
                    _circleSize,
                ],
                _degrees[d],
                _degrees[d + 1],
                fill=_colours[d],
                outline="black",
                width=int(_circleSize * lineProportion),
            )
        # input('aslfasld')
        if len(change.notes) > 2:
            try:
                # if bounds are -1,-1,1,1 it will give a trig result, meaning that left is negative
                # To plot it normalised change to 0,0,1,1
                _polygonCentre = polylabel.polylabel(
                    [change.getPolygon(True, 0, 0, 1, 1)],
                    precision=1.0,
                    with_distance=True,
                )
                # _polygonCentre = ([canvasSize/2+_polygonCentre[0][0]*canvasSize/2,canvasSize/2+_polygonCentre[0][1]*canvasSize/2],_polygonCentre[1]*canvasSize/2)
                _polygonCentre = (
                    [
                        _polygonCentre[0][0] * canvasSize,
                        _polygonCentre[0][1] * canvasSize,
                    ],
                    _polygonCentre[1] * canvasSize,
                )
            except:
                _polygonCentre = None
        else:
            _polygonCentre = None

        bigR = _circleSize * circleProportion / 2
        _chordCentres = Graphics.getChordCentres(change, R=bigR)
        # Create the fractality
        _fractality = None
        _largestR = max([i[1] for i in _chordCentres])
        _sizeRatio = _largestR / _circleSize
        for f in range(9999):
            if _circleSize * _sizeRatio**f < minimumPixelsOfCircle:
                _fractality = f
                break
        if _fractality == None:
            raise ValueError("sshit fractal fufnt wirk")

        """for modeIdx,cc in enumerate(_chordCentres):
            r = cc[1]
            if r >= minimumPixelsOfCircle:
                _newcc = Graphics.getChordCentres(change),R=r)"""

        _fMode = 0
        _lastCentre = None
        for modeIdx, i in enumerate(_chordCentres):
            _bX = i[0][0]
            _bY = i[0][1]

            for f in range(_fractality):

                if _lastCentre == None:
                    _bCentres = Graphics.getChordCentres(change, R=bigR)
                else:
                    _bCentres = Graphics.getChordCentres(change, R=_lastCentres[1])

                _bAngles = change.mode(modeIdx).getAngles(
                    repeatFirstResult=True, makeRepeatedResultLargerThanOneBefore=True
                )
                _bChord = _bCentres[modeIdx]
                _bX += _bChord[0][0]
                _bY += _bChord[0][1]

                # _fMode = (modeIdx * f) % (len(change.notes)-1)
                # _fMode = ((_fMode+modeIdx+1) % (len(change.notes)))
                # _fMode = int(_fMode)
                _fMode = modeIdx * (f + 1)
                _fMode = _fMode % len(change.notes)
                _bMode = modeIdx
                _fCentres = Graphics.getChordCentres(
                    change.mode(_fMode), R=_bCentres[modeIdx][1]
                )
                # _fChord used to be called i
                _fChord = _fCentres[_fMode]
                _fAngles = change.mode(_fMode).getAngles(
                    repeatFirstResult=True, makeRepeatedResultLargerThanOneBefore=True
                )
                # _fPolygon = change.mode(_fMode).getPolygon(True,_bChord[0][0]-_bChord[1],
                #                                            _bChord[0][0] + _bChord[1],
                #                                            _bChord[0][1] - _bChord[1],
                #                                            _bChord[0][1] + _bChord[1])
                print(
                    "fractalMode: {} change: {}".format(
                        change.mode(_fMode), change.mode(_bMode)
                    )
                )

                # input(str(i)+'bobby')

                # r = i[1]
                r = _fCentres[_fMode][1]

                # r *= circleProportion
                # x = i[0][0] + (1-circleProportion) * _circleSize
                # y = i[0][1] + (1-circleProportion) * _circleSize
                print("fMode", _fMode, "fChord", _fChord, "bCentres", _bCentres)
                # x = _fChord[0][0] + _bChord[0][0] + _bChord[1] - _fChord[1]
                # y = _fChord[0][1] + _bChord[0][1] + _bChord[1] - _fChord[1]
                # x =_fChord[0][0]
                # y = _fChord[0][1]

                x = _bChord[0][0] - _fChord[0][0]
                y = _bChord[0][1] - _fChord[0][1]
                # x = _bX
                # y = _bY

                # input('bchord'+str(_bChord)+'fchord'+str(_fChord)+' fangles '+str(change.mode(_fMode).getAngles(repeatFirstResult=True,makeRepeatedResultLargerThanOneBefore=True,formatForHumans=True))+str(' bangles '+str(change.mode(_bMode).getAngles(repeatFirstResult=True,makeRepeatedResultLargerThanOneBefore=True,formatForHumans=True))))

                # x +=  math.cos(_fAngles[_fMode]) * _bChord[1]/2
                # y +=  math.sin(_fAngles[_fMode]) * _bChord[1]/2

                # x += _bCentres[]
                # x *= circleProportion
                # y *= circleProportion
                x += _circleMargin  # *circleProportion
                y += _circleMargin  # *circleProportion
                # x += _circleMargin
                # y += _circleMargin

                draw.ellipse(
                    [x - r, y - r, x + r, y + r],  # left  # top  # right  # bottom,
                    fill=(0, 0, 0, 255),
                    outline="black",
                )
                # _degrees = change.mode(modeIdx).getAngles(returnDegrees=True, repeatFirstResult=True,goQuarterTurnAnticlockwise=True)
                _degrees = change.mode(_fMode).getAngles(
                    returnDegrees=True,
                    repeatFirstResult=True,
                    goQuarterTurnAnticlockwise=True,
                )

                for d, degree in enumerate(_degrees[:-1]):
                    # draw.ellipse([x - r, y - r, x + r, y + r], fill="black")
                    draw.chord(
                        [x - r, y - r, x + r, y + r],  # left  # top  # right  # bottom
                        _degrees[d],
                        _degrees[d + 1],
                        fill=Colour.modifyAlphaChannelOfRGBATuple(_colours[d], 33),
                        outline="black",
                        width=int(r * lineProportion),
                    )

                """This one just duplicates the original"""
                """for d,degree in enumerate(_degrees[:-1]):
                    draw.chord([(canvasSize - _circleSize), #left
                                canvasSize - _circleSize, #top
                                _circleSize, #right
                                _circleSize], #bottom
                           _degrees[d],_degrees[d+1],
                               fill=Colour.modifyAlphaChannelOfRGBATuple(_colours[d],33),outline="black")"""

                """for d,degree in enumerate(_degrees[:-1]):
                    draw.chord(Graphics.boundingBoxOfCircle(i),
                           _degrees[d],_degrees[d+1],
                               fill=_colours[d],outline="black")"""
            _lastCentres = _bCentres

        print("is it real")
        print(
            " porygon",
            " ".join(change.getPolygon(formatForHumans=True)),
            " degrees",
            " ".join(change.getAngles(returnDegrees=True, humanFormat=True)),
            " radians",
            " ".join(change.getAngles(humanFormat=True)),
            " notes",
            change,
            " polygon centre",
            _polygonCentre,
            " chord centres",
            "\n  ".join([str(i) for i in _chordCentres]),
            " fractality",
            _fractality,
            sep="\n ",
        )

        for i in _chordCentres:
            x = i[0][0]
            y = i[0][1]
            if False:
                draw.point([x, y], fill="cyan")
            size = 128
            # draw.rectangle([x-size,y-size,x+size,y+size], fill='cyan', outline=None, width=200)
        # draw.polygon([(5, 5), (25, 5), (25, 20), (5, 25)], fill="green", outline=None)

        # input(str(change))
        # im.show()
        im.save(path + "Circle no " + str(_pageNumber) + ".png")
        print("Circles saved to", path, "at", datetime.datetime.now())
        return im

    @classmethod
    def get_centroid(cls, poly):
        """Calculates the centroid of a non-intersecting polygon.
        Args:
            poly: a list of points, each of which is a list of the form [x, y].
        Returns:
            the centroid of the polygon in the form [x, y].
        Raises:
            ValueError: if poly has less than 3 points or the points are not
                        formatted correctly.
        """
        # Make sure poly is formatted correctly
        if len(poly) < 3:
            raise ValueError("polygon has less than 3 points")
        for point in poly:
            if type(point) is not list or 2 != len(point):
                raise ValueError("point is not a list of length 2")
        # Calculate the centroid from the weighted average of the polygon's
        # constituent triangles
        area_total = 0
        centroid_total = [float(poly[0][0]), float(poly[0][1])]
        for i in xrange(0, len(poly) - 2):
            # Get points for triangle ABC
            a, b, c = poly[0], poly[i + 1], poly[i + 2]
            # Calculate the signed area of triangle ABC
            area = (
                (a[0] * (b[1] - c[1])) + (b[0] * (c[1] - a[1])) + (c[0] * (a[1] - b[1]))
            ) / 2.0
            # If the area is zero, the triangle's line segments are
            # colinear so we should skip it
            if 0 == area:
                continue
            # The centroid of the triangle ABC is the average of its three
            # vertices
            centroid = [(a[0] + b[0] + c[0]) / 3.0, (a[1] + b[1] + c[1]) / 3.0]
            # Add triangle ABC's area and centroid to the weighted average
            centroid_total[0] = (
                (area_total * centroid_total[0]) + (area * centroid[0])
            ) / (area_total + area)
            centroid_total[1] = (
                (area_total * centroid_total[1]) + (area * centroid[1])
            ) / (area_total + area)
            area_total += area

        return centroid_total

    @classmethod
    def RECENTrenderCircleToFile(
        cls,
        change: Change,
        path="C:\\Users\\Edrihan\\PycharmProjects\\Grail Of Scale\\The Way Of Changes\\Graphics\\Circles\\",
        canvasSize=100,
        includeBGCircle=True,
        circleProportion=1,
        innerCircleProportion=1,
        chordAlpha=100,
        lineProportion=0.0125,
        fractalise=True,
        minimumPixelsOfCircle=1,
    ):

        # canvasSize = 4320 circleProportion=432/440
        # TODO: fractalise, from polylabel import polylabel as well as adding colour transpose
        _pageNumber = change.getChangeNumber(
            addOneToBookPage=True, decorateChapter=False
        )
        _circleSize = canvasSize * circleProportion
        _circleMargin = canvasSize - _circleSize
        _degrees = change.getAngles(returnDegrees=True, goQuarterTurnAnticlockwise=True)
        _degrees = _degrees + [_degrees[0]]

        _radiansTurned = change.getAngles(goQuarterTurnAnticlockwise=False)
        _colours = [
            Colour.rgbaTupleByDistance[i.semitonesFromOne() % 12] for i in change.notes
        ]
        _colours = [
            Colour.modifyAlphaChannelOfRGBATuple(i, chordAlpha) for i in _colours
        ]
        _polygon = change.getPolygon(
            boundL=_circleMargin,  # _circleMargin
            boundT=_circleMargin,  #
            boundR=canvasSize - _circleMargin,  # canvasSize-_circleMargin
            boundB=canvasSize - _circleMargin,
        )

        im = Image.new("RGBA", (canvasSize, canvasSize), (0, 255, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.ellipse([0, 0, canvasSize, canvasSize], fill="black")

        for d in range(len(_degrees) - 1):
            # print(_colours[d])
            # This is the nonfractal one
            draw.chord(
                [
                    canvasSize - _circleSize,
                    canvasSize - _circleSize,
                    _circleSize,
                    _circleSize,
                ],
                _degrees[d],
                _degrees[d + 1],
                fill=_colours[d],
                outline="black",
                width=int(_circleSize * lineProportion),
            )
        # input('aslfasld')
        if len(change.notes) > 2:
            try:
                # if bounds are -1,-1,1,1 it will give a trig result, meaning that left is negative
                # To plot it normalised change to 0,0,1,1
                _polygonCentre = polylabel.polylabel(
                    [change.getPolygon(True, 0, 0, 1, 1)],
                    precision=1.0,
                    with_distance=True,
                )
                # _polygonCentre = ([canvasSize/2+_polygonCentre[0][0]*canvasSize/2,canvasSize/2+_polygonCentre[0][1]*canvasSize/2],_polygonCentre[1]*canvasSize/2)
                _polygonCentre = (
                    [
                        _polygonCentre[0][0] * canvasSize,
                        _polygonCentre[0][1] * canvasSize,
                    ],
                    _polygonCentre[1] * canvasSize,
                )
            except:
                _polygonCentre = None
        else:
            _polygonCentre = None

        bigR = _circleSize * circleProportion / 2
        _chordCentres = Graphics.getChordCentres(change, R=bigR)
        # Create the fractality
        _fractality = None
        _largestR = max([i[1] for i in _chordCentres])
        _sizeRatio = _largestR / _circleSize
        for f in range(9999):
            if _circleSize * _sizeRatio**f < minimumPixelsOfCircle:
                _fractality = f
                break
        if _fractality == None:
            raise ValueError("sshit fractal fufnt wirk")

        """for modeIdx,cc in enumerate(_chordCentres):
            r = cc[1]
            if r >= minimumPixelsOfCircle:
                _newcc = Graphics.getChordCentres(change),R=r)"""

        _fMode = 0
        _lastCentre = None
        for modeIdx, i in enumerate(_chordCentres):
            _bX = i[0][0]
            _bY = i[0][1]

            for f in range(_fractality):

                if _lastCentre == None:
                    _bCentres = Graphics.getChordCentres(change, R=bigR)
                else:
                    _bCentres = Graphics.getChordCentres(change, R=_lastCentres[1])

                _bAngles = change.mode(modeIdx).getAngles(
                    repeatFirstResult=True, makeRepeatedResultLargerThanOneBefore=True
                )
                _bChord = _bCentres[modeIdx]
                _bX += _bChord[0][0]
                _bY += _bChord[0][1]

                # _fMode = (modeIdx * f) % (len(change.notes)-1)
                # _fMode = ((_fMode+modeIdx+1) % (len(change.notes)))
                # _fMode = int(_fMode)
                _fMode = modeIdx * (f + 1)
                _fMode = _fMode % len(change.notes)
                _bMode = modeIdx
                _fCentres = Graphics.getChordCentres(
                    change.mode(_fMode), R=_bCentres[modeIdx][1]
                )
                # _fChord used to be called i
                _fChord = _fCentres[_fMode]
                _fAngles = change.mode(_fMode).getAngles(
                    repeatFirstResult=True, makeRepeatedResultLargerThanOneBefore=True
                )
                # _fPolygon = change.mode(_fMode).getPolygon(True,_bChord[0][0]-_bChord[1],
                #                                            _bChord[0][0] + _bChord[1],
                #                                            _bChord[0][1] - _bChord[1],
                #                                            _bChord[0][1] + _bChord[1])
                print(
                    "fractalMode: {} change: {}".format(
                        change.mode(_fMode), change.mode(_bMode)
                    )
                )

                # input(str(i)+'bobby')

                # r = i[1]
                r = _fCentres[_fMode][1]

                # r *= circleProportion
                # x = i[0][0] + (1-circleProportion) * _circleSize
                # y = i[0][1] + (1-circleProportion) * _circleSize
                print("fMode", _fMode, "fChord", _fChord, "bCentres", _bCentres)
                # x = _fChord[0][0] + _bChord[0][0] + _bChord[1] - _fChord[1]
                # y = _fChord[0][1] + _bChord[0][1] + _bChord[1] - _fChord[1]
                # x =_fChord[0][0]
                # y = _fChord[0][1]

                x = _bChord[0][0] - _fChord[0][0]
                y = _bChord[0][1] - _fChord[0][1]
                # x = _bX
                # y = _bY

                # input('bchord'+str(_bChord)+'fchord'+str(_fChord)+' fangles '+str(change.mode(_fMode).getAngles(repeatFirstResult=True,makeRepeatedResultLargerThanOneBefore=True,formatForHumans=True))+str(' bangles '+str(change.mode(_bMode).getAngles(repeatFirstResult=True,makeRepeatedResultLargerThanOneBefore=True,formatForHumans=True))))

                # x +=  math.cos(_fAngles[_fMode]) * _bChord[1]/2
                # y +=  math.sin(_fAngles[_fMode]) * _bChord[1]/2

                # x += _bCentres[]
                # x *= circleProportion
                # y *= circleProportion
                x += _circleMargin  # *circleProportion
                y += _circleMargin  # *circleProportion
                # x += _circleMargin
                # y += _circleMargin

                draw.ellipse(
                    [x - r, y - r, x + r, y + r],  # left  # top  # right  # bottom,
                    fill=(0, 0, 0, 255),
                    outline="black",
                )
                # _degrees = change.mode(modeIdx).getAngles(returnDegrees=True, repeatFirstResult=True,goQuarterTurnAnticlockwise=True)
                _degrees = change.mode(_fMode).getAngles(
                    returnDegrees=True,
                    repeatFirstResult=True,
                    goQuarterTurnAnticlockwise=True,
                )

                for d, degree in enumerate(_degrees[:-1]):
                    # draw.ellipse([x - r, y - r, x + r, y + r], fill="black")
                    draw.chord(
                        [x - r, y - r, x + r, y + r],  # left  # top  # right  # bottom
                        _degrees[d],
                        _degrees[d + 1],
                        fill=Colour.modifyAlphaChannelOfRGBATuple(_colours[d], 33),
                        outline="black",
                        width=int(r * lineProportion),
                    )

                """This one just duplicates the original"""
                """for d,degree in enumerate(_degrees[:-1]):
                    draw.chord([(canvasSize - _circleSize), #left
                                canvasSize - _circleSize, #top
                                _circleSize, #right
                                _circleSize], #bottom
                           _degrees[d],_degrees[d+1],
                               fill=Colour.modifyAlphaChannelOfRGBATuple(_colours[d],33),outline="black")"""

                """for d,degree in enumerate(_degrees[:-1]):
                    draw.chord(Graphics.boundingBoxOfCircle(i),
                           _degrees[d],_degrees[d+1],
                               fill=_colours[d],outline="black")"""
            _lastCentres = _bCentres

        print("is it real")
        print(
            " porygon",
            " ".join(change.getPolygon(formatForHumans=True)),
            " degrees",
            " ".join(change.getAngles(returnDegrees=True, humanFormat=True)),
            " radians",
            " ".join(change.getAngles(humanFormat=True)),
            " notes",
            change,
            " polygon centre",
            _polygonCentre,
            " chord centres",
            "\n  ".join([str(i) for i in _chordCentres]),
            " fractality",
            _fractality,
            sep="\n ",
        )

        for i in _chordCentres:
            x = i[0][0]
            y = i[0][1]
            if False:
                draw.point([x, y], fill="cyan")
            size = 128
            # draw.rectangle([x-size,y-size,x+size,y+size], fill='cyan', outline=None, width=200)
        # draw.polygon([(5, 5), (25, 5), (25, 20), (5, 25)], fill="green", outline=None)

        # input(str(change))
        # im.show()
        im.save(path + "Circle no " + str(_pageNumber) + ".png")
        print("Circles saved to", path, "at", datetime.datetime.now())
        return im

    @classmethod
    def distanceBetween(
        cls,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        showDebug=False,
        returnDirection=False,
    ) -> float:
        x = x2 - x1
        y = y2 - y1
        if not returnDirection:
            x = abs(x)
            y = abs(y)
        d = (x**2 + y**2) ** (1 / 2)
        if showDebug:
            print(
                "the d between (",
                x1,
                y1,
                ") and (",
                x2,
                y2,
                ") is",
                str(round(d, 2)),
                sep=" ",
            )
        return d

    @classmethod
    def pointInBetween(
        cls, x1: float, y1: float, x2: float, y2: float
    ) -> list[float, float]:
        return [(x1 + x2) / 2, (y1 + y2) / 2]

    @classmethod
    def angleBetween(
        cls, x1: float, y1: float, x2: float, y2: float, returnDegrees=False
    ) -> float:
        if returnDegrees == True:
            return math.degrees(math.atan2(y2 - y1, x2 - x1))
        else:
            return math.atan2(y2 - y1, x2 - x1)

    @classmethod
    def boundingBoxOfCircle(cls, circle: list[list, float], showDebug=False) -> list:
        r = circle[1]
        x1 = circle[0][0] - r
        x2 = circle[0][0] + r
        y1 = circle[0][1] - r
        y2 = circle[0][1] + r
        if showDebug:
            print(" circle", circle, "\nreturning boundingbox", [x1, y1, x2, y2])
        return [x1, y1, x2, y2]

    @classmethod
    def iterationsToConvergence(
        cls, bigSize, smallSize, minPixels, maxIterations=99999
    ):
        """You will get the number of fractal generations (afterrr the seed)"""
        """which are larger than min"""
        if smallSize >= bigSize:
            raise ValueError("small size {} < big size {}".format(smallSize, bigSize))
        # Create the fractality
        _iterations = 0

        _sizeRatio = smallSize / bigSize
        for i in range(maxIterations):
            if bigSize * _sizeRatio**i < minPixels:
                break
            _iterations = i + 2

        if _iterations == None:
            raise ValueError("something happened and there is no fractality")
        return _iterations

    @classmethod
    def getChordCentres(
        cls,
        change: Change,
        R: float,
        showDebug=False,
        returnFCircle=False,
        humanOutput=False,
        colourTranspose=0,
        topLeftOrigin=True,
        useSemitones=True,
    ):
        """Let R == Radius of outer circle"""
        """Let r == distamce between centre of chord and middle of outer circle"""
        """Let h == diameter of chord inner circle"""
        """Let a == the length of chord slice"""
        """Let p1 = the first point of the chord slice"""
        """Let p2 = the second point of the chord slice"""
        # https://www.mathopenref.com/sagitta.html
        # http: // mathworld.wolfram.com / CircularSector.html
        R = R
        # R = R
        # _circlePadding = R * (1 - circleProportion)

        polygon = change.getPolygon(0, 0, R * 2, R * 2, useSemitones=useSemitones)

        # polygon = change.getPolygon(True,-R,-R,R,R)
        if showDebug:
            print("in getchordcentres, polygon: " + str(polygon))
        _chordCentres = []
        if returnFCircle == True:
            _fCircles = []

        # At this point uses (0,0) as centre and radius,-radius as the edges
        # _polygon = change.getPolygon(boundL=-R,boundT=0,boundR=2*R,boundB=2*R)
        # R = R * circleProportion
        _radians = change.getAngles(repeatFirstResult=True)
        # input('radians....'+' '.join(change.getAngles(formatForHumans=True,repeatFirstResult=True))+str(_radians)+str(polygon))
        for chordIdx, chord in enumerate(polygon[:-1]):
            p1 = polygon[chordIdx]
            p2 = polygon[chordIdx + 1]
            centreOfa = Graphics.pointInBetween(p1[0], p1[1], p2[0], p2[1])
            r = abs(Graphics.distanceBetween(R, R, centreOfa[0], centreOfa[1]))

            hSm = abs(R - r)
            hLg = abs(R + r)
            if showDebug:
                print("here is it " + str(_radians) + "  " + str(len(polygon)))
            try:
                _radians = change.getAngles(
                    repeatFirstResult=True, makeRepeatedResultLargerThanOneBefore=True
                )
                if showDebug:
                    print("road left", _radians[-1], _radians[-2])
                if _radians[-1] < _radians[-2]:
                    raise ValueError("asldkfjalskdjf")
                _secondAngle = _radians[(chordIdx + 1) % (len(_radians) - 0)]
                # TODO If using not 12-tone system make this next part calculate the arc length
                if _secondAngle == 0:
                    _secondAngle = 2 * math.pi
                _firstAngle = _radians[chordIdx]
                if _secondAngle > _firstAngle:
                    if _secondAngle - _firstAngle <= math.pi:
                        h = hSm
                    else:
                        h = hLg
                elif _firstAngle < _secondAngle:

                    # h = max(hSm,hLg)
                    if _secondAngle - _firstAngle <= math.pi:
                        h = hSm
                    else:
                        h = hLg

            except:
                input(
                    "this exception is happening index = "
                    + str(_radians)
                    + str(polygon[:-1])
                )
            # hAngle is at right angle to chord angle, hence adding 90 degrees.
            hAngle = Graphics.angleBetween(p1[0], p1[1], p2[0], p2[1]) - math.pi / 2
            # centreX=centreOfa[0] - math.cos(hAngle)*h/2 + R

            # centreY=centreOfa[1] - math.sin(hAngle)*h/2 + R

            # centreX=R+ math.cos(hAngle)*(R-h/4)
            # centreY=R+ math.sin(hAngle)*(R-h/4)
            # centreX=R
            # centreY=R
            centreX = centreOfa[0] + math.cos(hAngle) * h / 2
            centreY = centreOfa[1] + math.sin(hAngle) * h / 2
            if topLeftOrigin == False:
                centreX += R
                centreY += R

            # Right and Down for proportion
            # centreX += _circlePadding
            # centreY += _circlePadding

            # Adjust fo proportion
            # centreX *= circleProportion
            # centreY *= circleProportion

            _chordCentres.append([[centreX, centreY], h / 2])

            if showDebug:
                print(
                    "inside getChordCentres() for change {}, chordSlice {},\n R {},\n r {},\n h {}\n angleOfh{}\n p1 {}\n p2 {}\n centreOfa{}\n".format(
                        change,
                        chordIdx,
                        R,
                        r,
                        h,
                        str(round(hAngle / math.pi, 2)) + "pi",
                        p1,
                        p2,
                        centreOfa,
                    )
                )

            if returnFCircle == True:
                _fCircles.append(
                    FCircle(
                        centre=[centreX, centreY],
                        r=h / 2 / FCircle.proportion,
                        change=change.mode((chordIdx) % len(change)),
                        colourTranspose=(
                            colourTranspose + change.notes[chordIdx].semitonesFromOne()
                        )
                        % 12,
                    )
                )

        if returnFCircle:
            return _fCircles

        return _chordCentres

    @classmethod
    def OLDgetChordCentres(cls, polygon, R: float, showDebug=True):
        # https://www.mathopenref.com/sagitta.html
        # http: // mathworld.wolfram.com / CircularSector.html
        _chordCentres = []
        for i, p in enumerate(polygon[:-1]):
            x1 = p[0]
            y1 = p[1]
            x2 = polygon[i + 1][0]
            y2 = polygon[i + 1][1]
            L = Graphics.distanceBetween(x1, y1, x2, y2) / 2
            S1 = abs(R - ((R**2 - L**2) ** (1 / 2)))
            S2 = abs(R + ((R**2 - L**2) ** (1 / 2)))

            centrex1 = (x1 + x2) / 2
            centrey1 = (y1 + y2) / 2
            chordAngle1 = Graphics.angleBetween(x1, y1, x2, y2)
            chordAngle2 = Graphics.angleBetween(x2, y2, x1, y1)
            sAngle1 = chordAngle1 + math.pi / 2

            _chordCentres.append(
                [
                    [
                        centrex1 * R + math.cos(sAngle1) * S1,
                        centrey1 * R - math.sin(sAngle1) * S1,
                    ],
                    S1 * R,
                ]
            )  # HERE! TODO
            if showDebug:
                print(
                    "x1: {}, y1: {}, x2: {}, y2: {}, L: {}, S1: {}, centreX1:{},  Y1:{}".format(
                        x1, y1, x2, y2, L, S1, centrex1, centrey1
                    )
                )

        if humanOutput:
            return [i for i in _chordCentres]

        return _chordCentres

    @classmethod
    def OLDrenderCircleToFile(
        cls,
        change,
        path="C:\\Users\\Edrihan\\PycharmProjects\\Grail Of Scale\\The Way Of Changes\\Graphics\\Circles\\",
    ):
        _pageNumber = change.getChangeNumber(
            decorateChapter=False,
            addOneToBookPage=True,
        )
        _fileName = "circle " + str(_pageNumber)
        im = Image.new("rgb", (200, 200), "#ddd")
        with open(path + _fileName) as im:
            draw = ImageDraw.Draw(im)

            draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 0, 0, 255))
            del draw
            im.save(_fileName, "PNG")