from __future__ import annotations, print_function
import numpy as np
from Unicode import Unicode
from Utility import Utility
input = Utility.input
class ScaleNames:

    import scaleNamesLists as scaleNamesLists
    doValidateScaleNames = True
    namesBySequenceIndex = scaleNamesLists.namesBySequenceIndex
    namesBySequenceIndexNegative = scaleNamesLists.namesBySequenceIndexNegative
    semitonesBySequenceIndex = scaleNamesLists.semitonesBySequenceIndex
    poemBySequenceIndex = scaleNamesLists.poemBySequenceIndex
    poemAuthors = scaleNamesLists.poemAuthors

    namesBySequenceIndex = np.array(namesBySequenceIndex, dtype="object")
    namesBySequenceIndexNegative = np.array(
        namesBySequenceIndexNegative, dtype="object"
    )
    semitonesBySequenceIndex = np.array(semitonesBySequenceIndex, dtype="object")
    poemBySequenceIndex = np.array(poemBySequenceIndex)
    poemAuthors = np.array(poemAuthors, dtype="object")
    ragaTriggerStrings = [
        "(ascending)",
        "(descending)",
        "(first octave)",
        "(second octave)",
        Unicode.chars["Ascending"],
        Unicode.chars["Descending"],
    ]

    def __init__(self):

        print("in ScaleNames and stuck cause input command", namesBySequenceIndex[1])
        input()
        # for change in range(len(Book().sequence)):
        #    print('classes',cls)

    @classmethod
    # def printBlankCanvas(cls, theTwentyFourtyEight=Book()):
    def printBlankCanvas(cls, resetPoems=True):
        text = "#Blank Canvas For Scale Names"
        _namesAdded = 0
        # for i in range(len(theTwentyFourtyEight.sequence)):
        for i in range(2048):
            # _thisScale = theTwentyFourtyEight.sequence[i]
            _thisScale = Change.makeFromChangeNumber(i)
            print("#", i + 1, sep="", end=": ")

            for noteInC in _thisScale.straightenDegrees(
                allowedNotes=Change.allowedNoteNamesJazz
            ).byWays("C"):
                print(noteInC, " ", sep="", end="")
            # print(':'+' '.join(theTwentyFourtyEight.sequence[i].byWays('Set')),end='')
            print(":" + " ".join(_thisScale.byWays("Set")), end="")
            # print(':',_thisScale.straightenDegrees(allowedNotes=Change.allowedNoteNamesJazz),' : ',theTwentyFourtyEight.sequence[i].getChordQuality())
            print(
                ": ",
                _thisScale.straightenDegrees(allowedNotes=Change.allowedNoteNamesJazz),
                ": ",
                _thisScale.getChordQuality(),
                sep="",
            )

            print("namesBySequenceIndex[", i, "] = '''", sep="", end="")

            _nameToAdd = ""
            _thisScaleInSemitones = _thisScale.byWays("Set")
            _thisScaleInSemitones = [int(x) for x in _thisScaleInSemitones]
            for pitchSet in ScaleNames.pitchSets:
                if len(pitchSet) == len(_thisScaleInSemitones):
                    for pitchSetMode in range(len(pitchSet)):
                        _pitchSetModeSemitones = Change.modeOfSet(
                            sorted(pitchSet), pitchSetMode
                        )
                        _pitchSetModeSemitones = [
                            int(pitch) for pitch in _pitchSetModeSemitones
                        ]
                        # print('_thisScaleInSemitones,_pitchSetModeSemitones',_thisScaleInSemitones,_pitchSetModeSemitones, _thisScaleInSemitones==_pitchSetModeSemitones)
                        if _thisScaleInSemitones == _pitchSetModeSemitones:
                            _namesAdded += 1
                            _nameToAdd = ScaleNames.names[
                                ScaleNames.pitchSets.index(pitchSet)
                            ][
                                pitchSetMode
                                % len(
                                    ScaleNames.names[
                                        ScaleNames.pitchSets.index(pitchSet)
                                    ]
                                )
                            ]

            # if cls.namesBySequenceIndex[i] != 'unnamed':

            print(cls.namesBySequenceIndex[i], end="")
            if _nameToAdd != "" and _nameToAdd not in cls.namesBySequenceIndex[i].split(
                ","
            ):
                if cls.namesBySequenceIndex[i] == "":
                    print(_nameToAdd, end="")
                else:
                    print("," + _nameToAdd, end="")

            print("'''", end="\n", sep="")
            _semitonePositions = _thisScale.byWays("Set")
            for position in range(len(_semitonePositions)):
                _semitonePositions[position] = int(_semitonePositions[position])
            print("namesBySequenceIndexNegative[{}] = ''''''".format(i))
            print(
                "semitonesBySequenceIndex[",
                i,
                "] = ",
                _semitonePositions,
                sep="",
                end="\n",
            )
            if resetPoems:
                print(
                    "poemBySequenceIndex["
                    + str(i)
                    + "] = '''"
                    + " ".join(_thisScale.getConsonant())
                    + "'''"
                )
                print("poemAuthors[{}] = ''''''".format(i))
            else:
                print(
                    "poemBySequenceIndex["
                    + str(i)
                    + "] = '''"
                    + " ".join(_thisScale.byWays("Poem"))
                    + "'''"
                )
                if cls.poemAuthors[i] not in ("", None):
                    _poemAuthors = cls.poemAuthors[i]
                else:
                    _poemAuthors = ""
                print("poemAuthors[{}] = '''{}'''".format(i, _poemAuthors))
            print(
                "#",
                i + 1,
                ": ",
                "".join(Change.makeFromChangeNumber(i).getHexagramSymbols()),
                " ",
                Change.makeFromChangeNumber(i).getHexagramName(),
                sep="",
                end=": ",
            )
            for semitone in _thisScale.byWays("Step"):
                print(semitone, " ", sep="", end="")
            print(" : ", end="")
            for carnaticShortHand in _thisScale.byWays("Notation"):
                print(carnaticShortHand, " ", sep="", end="")
            print(": " + "".join(_thisScale.byWays("Word")))
            print("\n", end="")
        print("The number of scale names added:", _namesAdded)

    @classmethod
    def getMainScaleNameForIndex(
        cls, indexNumber, defaultWay="", defaultReplacement="           "
    ):
        _scaleNames = cls.namesBySequenceIndex[indexNumber].split(",")[0]
        if _scaleNames == None:
            _scaleNames = [""]
        if _scaleNames == [""]:
            if defaultWay != "":
                if Change.isValidWay(defaultWay) or JazzNote.isValidWay(defaultWay):
                    return Change.makeFromChangeNumber(indexNumber).byWays(defaultWay)
                else:
                    raise ValueError("Default way provided is invalid", defaultWay)
            else:
                return defaultReplacement



    @classmethod
    def otherChangesWithName(cls, name):
        pass

    @classmethod
    def otherDirectionsOfRaga(
        cls,
        raagName,
        change: Change,
        returnRagaNames=False,
        returnRagaIndexes=True,
        searchEntireBookForMultipleDirections=None,
        showDebug=False,
    ):
        """ if searchEntireBookForMultipleDirections == None, it will default.\
        """
        if searchEntireBookForMultipleDirections is None:
            searchEntireBookForMultipleDirections = True
        _indexes = []
        _nameIsFound = False
        if " (descending)" in raagName:
            targetDirection = " (ascending)"
            thisDirection = " (descending)"
            raagName = raagName.replace(" (descending)", "")
        elif " (ascending)" in raagName:
            targetDirection = " (descending)"
            thisDirection = " (ascending)"
            raagName = raagName.replace(" (ascending)", "")
        elif " (first octave)" in raagName:
            targetDirection = " (second octave)"
            thisDirection = " (first octave)"
            raagName = raagName.replace(" (first octave)", "")
        elif " (second octave)" in raagName:
            targetDirection = " (first octave)"
            thisDirection = " (second octave)"
            raagName = raagName.replace(" (second octave)", "")
        elif Unicode.chars["Descending"] in raagName:
            targetDirection = " (ascending)"
            thisDirection = " (descending)"
            raagName = raagName.replace(Unicode.chars["Descending"], "")
        elif Unicode.chars["Ascending"] in raagName:
            targetDirection = " (descending)"
            thisDirection = " (ascending)"
            raagName = raagName.replace(Unicode.chars["Ascending"], "")
        else:
            raise ValueError(
                "Ragas supported are in the form 'Nameyname (ascending)' or (descending)"
            )

        # input('asdfasdfas {} {} {} {}'.format(raagName, targetDirection, raagName + targetDirection,[raagName + targetDirection]))
        _namesToFind = [raagName + targetDirection.replace("  ", " ")]
        _namesToFind[0] = _namesToFind[0].replace("  ", " ")
        _namesToFind[0] = _namesToFind[0].replace(Unicode.chars["Raga"], "Raga")
        _namesToFind[0] = _namesToFind[0].replace(Unicode.chars["Mela"], "Mela")
        _namesFound = []
        if searchEntireBookForMultipleDirections == True:
            _namesToFind.append(_namesToFind[0].replace(targetDirection, thisDirection))

        for index, name in enumerate(cls.namesBySequenceIndex):
            if _namesToFind[0].replace(
                "(no 1) ", ""
            ) in name and index != change.getChangeNumber(decorateChapter=False):
                # Check if it's the same one first.

                _indexes.append(index)
                _namesFound.append(_namesToFind[0])
                if "(no 1) " in _namesToFind[0]:
                    _indexes[-1] = -_indexes[-1]
                if searchEntireBookForMultipleDirections:
                    if _namesToFind[1].replace(
                        "(no 1) ", ""
                    ) in name and index != change.getChangeNumber(
                        decorateChapter=False
                    ):
                        _indexes.append(index)
                        _namesFound.append(_namesToFind[1])
                else:
                    break
        if len(_indexes) == 0:
            raise ValueError(
                "name: "
                + str(raagName)
                + "targetDir: "
                + str(targetDirection)
                + "nameToFind: "
                + str(_namesToFind)
                + ". (Raga Not Found)"
            )
        else:
            if showDebug:
                print("in it now for the win {} ".format(_indexes))

            if returnRagaNames == True and returnRagaIndexes == False:
                return _namesFound
            elif returnRagaNames == False and returnRagaIndexes == True:
                return _indexes
            elif returnRagaNames == True and returnRagaIndexes == True:
                _dictRagas = {}
                for idx, i in enumerate(_indexes):
                    _dictRagas[_indexes] = _namesFound[i]
                return _dictRagas
            else:
                raise TypeError(
                    "What exactly are you returning if neither ragaNames nor ragaIndexes"
                )

    @classmethod
    def getWrittenPoems(cls):
        _poems = []
        for i in range(2048):
            _poem = cls.poemBySequenceIndex[i]
            _thisChange = Change.makeFromChangeNumber(i)
            _consonant = " ".join(_thisChange.getConsonant(returnWrittenPoem=False))
            print("Does {} == {}? {}".format(_poem, _consonant, _poem == _consonant))
            if _poem != _consonant:
                _poems.append(
                    "#"
                    + str(i + 1)
                    + " "
                    + str(_thisChange.straightenDegrees())
                    + " "
                    + " ".join(_thisChange.getHexagram(["symbol", "name"]))
                    + " : "
                    + _thisChange.getScaleNames()[0]
                    + "\n"
                    + "oldPoem["
                    + str(i)
                    + "] = '''"
                    + _poem
                    + "'''\n"
                )

        input("thats all she wrote: \n{}".format("\n".join(_poems)))
        return _poems

    # Check shit out
    def validateScaleNames(self):
        _biggestScaleName = ""
        _biggestMainScaleName = ""
        for names in namesBySequenceIndex:
            if ", " in names:
                input(names + "contains a comma-space and shouldn't")
            if "  " in names:
                input(names + "contains a double-space and shouldn't")
            if len(names) > 0 and names[-1] == ",":
                input(names + "ends with a comma and shouldn't")
            _namesLst = names.split(",")
            if "Other" in names:
                input(
                    "We aren't using 'Other' anymore, now designate the main scale with the number 1 or no ending, and the second with it's number, and so on. Other was found in {}".format(
                        names
                    )
                )
            for n, name in enumerate(_namesLst):
                name = name.replace(
                    " (ascending)", " " + Unicode.chars["Ascending"]
                )
                name = name.replace(
                    " (descending)", " " + Unicode.chars["Descending"]
                )
                if n == 0 and len(name) > len(_biggestMainScaleName):
                    _biggestMainScaleName = name
                    print(_biggestMainScaleName, "is longer than the last one.")
                if len(name) > len(_biggestScaleName):
                    _biggestScaleName = name
        input(
            "\nbiggest scale name: {}\nbiggest main scale name: {}\ndone verifying scale names.".format(
                _biggestScaleName, _biggestMainScaleName
            )
        )
    forteNumbers = {
        "0-1": (),
        "1-1": (0,),
        "2-1": (0, 1),
        "2-2": (0, 2),
        "2-3": (0, 3),
        "2-4": (0, 4),
        "2-5": (0, 5),
        "2-6": (0, 6),
        "3-1": (0, 1, 2),  # 2,1,0,0,0,0
        "3-2A": (0, 1, 3),  # 1,1,1,0,0,0
        "3-2B": (0, 2, 3),
        "3-3A": (0, 1, 4),  # 1,0,1,1,0,0
        "3-3B": (0, 3, 4),
        "3-4A": (0, 1, 5),  # 1,0,0,1,1,0
        "3-4B": (0, 4, 5),  # 1,0,0,1,1,0
        "3-5A": (0, 1, 6),  # 1,0,0,0,1,1
        "3-5B": (0, 5, 6),  # 1,0,0,0,1,1
        "3-6": (0, 2, 4),  # 0,2,0,1,0,0
        "3-7A": (0, 2, 5),  # 0,1,1,0,1,0
        "3-7B": (0, 3, 5),
        "3-8A": (0, 2, 6),  # 0,1,0,1,0,1
        "3-8B": (0, 4, 6),
        "3-9": (0, 2, 7),  # 0,1,0,0,2,0
        "3-10": (0, 3, 6),  # 0,0,2,0,0,1
        "3-11A": (0, 3, 7),  # 0,0,1,1,1,0
        "3-11B": (0, 4, 7),  # 0,0,1,1,1,0
        "3-12": (0, 4, 8),  # 0,0,0,3,0,0
        "4-1": (0, 1, 2, 3),  # 3,2,1,0,0,0
        "4-2A": (0, 1, 2, 4),  # 2,2,1,1,0,0
        "4-2B": (0, 2, 3, 4),
        "4-3": (0, 1, 3, 4),  # 2,1,2,1,0,0
        "4-4A": (0, 1, 2, 5),  # 2,1,1,1,1,0
        "4-4B": (0, 3, 4, 5),
        "4-5A": (0, 1, 2, 6),  # 2,1,0,1,1,1
        "4-5B": (0, 4, 5, 6),  # 2,1,0,1,1,1
        "4-6": (0, 1, 2, 7),  # 2,1,0,0,2,1
        "4-7": (0, 1, 4, 5),  # 2,0,1,2,1,0
        "4-8": (0, 1, 5, 6),  # 2,0,0,1,2,1
        "4-9": (0, 1, 6, 7),  # 2,0,0,0,2,2
        "4-10": (0, 2, 3, 5),  # 1,2,2,0,1,0
        "4-11A": (0, 1, 3, 5),  # 1,2,1,1,1,0
        "4-11B": (0, 2, 4, 5),
        "4-12A": (0, 2, 3, 6),  # 1,1,2,1,0,1
        "4-12B": (0, 3, 4, 6),
        "4-13A": (0, 1, 3, 6),  # 1,1,2,0,1,1
        "4-13B": (0, 3, 5, 6),
        "4-14A": (0, 2, 3, 7),  # 1,1,1,1,2,0
        "4-14B": (0, 4, 5, 7),
        "4-z15A": (0, 1, 4, 6),  # 1,1,1,1,1,1
        "4-z15B": (0, 2, 5, 6),
        "4-16A": (0, 1, 5, 7),  # 1,1,0,1,2,1
        "4-16B": (0, 2, 6, 7),
        "4-17": (0, 3, 4, 7),  # 1,0,2,2,1,0
        "4-18A": (0, 1, 4, 7),  # 1,0,2,1,1,1
        "4-18B": (0, 3, 6, 7),
        "4-19A": (0, 1, 4, 8),  # 1,0,1,3,1,0
        "4-19B": (0, 3, 4, 8),
        "4-20": (0, 1, 5, 8),  # 1,0,1,2,2,0
        "4-21": (0, 2, 4, 6),  # 0,3,0,2,0,1
        "4-22A": (0, 2, 4, 7),  # 0,2,1,1,2,0
        "4-22B": (0, 3, 5, 7),
        "4-23": (0, 2, 5, 7),  # 0,2,1,0,3,0
        "4-24": (0, 2, 4, 8),  # 0,2,0,3,0,1
        "4-25": (0, 2, 6, 8),  # 0,2,0,2,0,2
        "4-26": (0, 3, 5, 8),  # 0,1,2,1,2,0
        "4-27A": (0, 2, 5, 8),  # 0,1,2,1,1,1
        "4-27B": (0, 3, 6, 8),
        "4-28": (0, 3, 6, 9),  # 0,0,4,0,0,2
        "4-z29A": (0, 1, 3, 7),  # 1,1,1,1,1,1
        "4-z29B": (0, 4, 6, 7),
        "5-1": (0, 1, 2, 3, 4),  # 4,3,2,1,0,0
        "5-2A": (0, 1, 2, 3, 5),  # 3,3,2,1,1,0
        "5-2B": (0, 2, 3, 4, 5),
        "5-3A": (0, 1, 2, 4, 5),  # 3,2,2,2,1,0
        "5-3B": (0, 1, 3, 4, 5),
        "5-4A": (0, 1, 2, 3, 6),  # 3,2,2,1,1,1
        "5-4B": (0, 3, 4, 5, 6),
        "5-5A": (0, 1, 2, 3, 7),  # 3,2,1,1,2,1
        "5-5B": (0, 4, 5, 6, 7),
        "5-6A": (0, 1, 2, 5, 6),  # 3,1,1,2,2,1
        "5-6B": (0, 1, 4, 5, 6),
        "5-7A": (0, 1, 2, 6, 7),  # 3,1,0,1,3,2
        "5-7B": (0, 1, 5, 6, 7),
        "5-8": (0, 2, 3, 4, 6),  # 2,3,2,2,0,1
        "5-9A": (0, 1, 2, 4, 6),  # 2,3,1,2,1,1
        "5-9B": (0, 2, 4, 5, 6),
        "5-10A": (0, 1, 3, 4, 6),  # 2,2,3,1,1,1
        "5-10B": (0, 2, 3, 5, 6),
        "5-11A": (0, 2, 3, 4, 7),  # 2,2,2,2,2,0
        "5-11B": (0, 3, 4, 5, 7),
        "5-z12": (0, 1, 3, 5, 6),  # 2,2,2,1,2,1
        "5-13A": (0, 1, 2, 4, 8),  # 2,2,1,3,1,1
        "5-13B": (0, 2, 3, 4, 8),
        "5-14A": (0, 1, 2, 5, 7),  # 2,2,1,1,3,1
        "5-14B": (0, 2, 5, 6, 7),
        "5-15": (0, 1, 2, 6, 8),  # 2,2,0,2,2,2
        "5-16A": (0, 1, 3, 4, 7),  # 2,1,3,2,1,1
        "5-16B": (0, 3, 4, 6, 7),
        "5-z17": (0, 1, 3, 4, 8),  # 2,1,2,3,2,0
        "5-z18A": (0, 1, 4, 5, 7),  # 2,1,2,2,2,1
        "5-z18B": (0, 2, 3, 6, 7),
        "5-19A": (0, 1, 3, 6, 7),  # 2,1,2,1,2,2
        "5-19B": (0, 1, 4, 6, 7),
        "5-20A": (0, 1, 5, 6, 8),  # 2,1,1,2,3,1
        "5-20B": (0, 2, 3, 7, 8),
        "5-21A": (0, 1, 4, 5, 8),  # 2,0,2,4,2,0
        "5-21B": (0, 3, 4, 7, 8),
        "5-22": (0, 1, 4, 7, 8),  # 2,0,2,3,2,1
        "5-23A": (0, 2, 3, 5, 7),  # 1,3,2,1,3,0
        "5-23B": (0, 2, 4, 5, 7),
        "5-24A": (0, 1, 3, 5, 7),  # 1,3,1,2,2,1
        "5-24B": (0, 2, 4, 6, 7),
        "5-25A": (0, 2, 3, 5, 8),  # 1,2,3,1,2,1
        "5-25B": (0, 3, 5, 6, 8),
        "5-26A": (0, 2, 4, 5, 8),  # 1,2,2,3,1,1
        "5-26B": (0, 3, 4, 6, 8),
        "5-27A": (0, 1, 3, 5, 8),  # 1,2,2,2,3,0
        "5-27B": (0, 3, 5, 7, 8),
        "5-28A": (0, 2, 3, 6, 8),  # 1,2,2,2,1,2
        "5-28B": (0, 2, 5, 6, 8),
        "5-29A": (0, 1, 3, 6, 8),  # 1,2,2,1,3,1
        "5-29B": (0, 2, 5, 7, 8),
        "5-30A": (0, 1, 4, 6, 8),  # 1,2,1,3,2,1
        "5-30B": (0, 2, 4, 7, 8),
        "5-31A": (0, 1, 3, 6, 9),  # 1,1,4,1,1,2
        "5-31B": (0, 2, 3, 6, 9),
        "5-32A": (0, 1, 4, 6, 9),  # 1,1,3,2,2,1
        "5-32B": (0, 2, 5, 6, 9),
        "5-33": (0, 2, 4, 6, 8),  # 0,4,0,4,0,2
        "5-34": (0, 2, 4, 6, 9),  # 0,3,2,2,2,1
        "5-35": (0, 2, 4, 7, 9),  # 0,3,2,1,4,0
        "5-z36A": (0, 1, 2, 4, 7),  # 2,2,2,1,2,1
        "5-z36B": (0, 3, 5, 6, 7),
        "5-z37": (0, 3, 4, 5, 8),  # 2,1,2,3,2,0
        "5-z38A": (0, 1, 2, 5, 8),  # 2,1,2,2,2,1
        "5-z38B": (0, 3, 6, 7, 8),
        "6-1": (0, 1, 2, 3, 4, 5),  # 5,4,3,2,1,0
        "6-2A": (0, 1, 2, 3, 4, 6),  # 4,4,3,2,1,1
        "6-2B": (0, 2, 3, 4, 5, 6),
        "6-z3A": (0, 1, 2, 3, 5, 6),  # 4,3,3,2,2,1
        "6-z3B": (0, 1, 3, 4, 5, 6),
        "6-z4": (0, 1, 2, 4, 5, 6),  # 4,3,2,3,2,1
        "6-5A": (0, 1, 2, 3, 6, 7),  # 4,2,2,2,3,2
        "6-5B": (0, 1, 4, 5, 6, 7),
        "6-z6": (0, 1, 2, 5, 6, 7),  # 4,2,1,2,4,2
        "6-7": (0, 1, 2, 6, 7, 8),  # 4,2,0,2,4,3
        "6-8": (0, 2, 3, 4, 5, 7),  # 3,4,3,2,3,0
        "6-9A": (0, 1, 2, 3, 5, 7),  # 3,4,2,2,3,1
        "6-9B": (0, 2, 4, 5, 6, 7),
        "6-z10A": (0, 1, 3, 4, 5, 7),  # 3,3,3,3,2,1
        "6-z10B": (0, 2, 3, 4, 6, 7),
        "6-z11A": (0, 1, 2, 4, 5, 7),  # 3,3,3,2,3,1
        "6-z11B": (0, 2, 3, 5, 6, 7),
        "6-z12A": (0, 1, 2, 4, 6, 7),  # 3,3,2,2,3,2
        "6-z12B": (0, 1, 3, 5, 6, 7),
        "6-z13": (0, 1, 3, 4, 6, 7),  # 3,2,4,2,2,2
        "6-14A": (0, 1, 3, 4, 5, 8),  # 3,2,3,4,3,0
        "6-14B": (0, 3, 4, 5, 7, 8),
        "6-15A": (0, 1, 2, 4, 5, 8),  # 3,2,3,4,2,1
        "6-15B": (0, 3, 4, 6, 7, 8),
        "6-16A": (0, 1, 4, 5, 6, 8),  # 3,2,2,4,3,1
        "6-16B": (0, 2, 3, 4, 7, 8),
        "6-z17A": (0, 1, 2, 4, 7, 8),  # 3,2,2,3,3,2
        "6-z17B": (0, 1, 4, 6, 7, 8),
        "6-18A": (0, 1, 2, 5, 7, 8),  # 3,2,2,2,4,2
        "6-18B": (0, 1, 3, 6, 7, 8),
        "6-z19A": (0, 1, 3, 4, 7, 8),  # 3,1,3,4,3,1
        "6-z19B": (0, 1, 4, 5, 7, 8),
        "6-20": (0, 1, 4, 5, 8, 9),  # 3,0,3,6,3,0
        "6-21A": (0, 2, 3, 4, 6, 8),  # 2,4,2,4,1,2
        "6-21B": (0, 2, 4, 5, 6, 8),
        "6-22A": (0, 1, 2, 4, 6, 8),  # 2,4,1,4,2,2
        "6-22B": (0, 2, 4, 6, 7, 8),
        "6-z23": (0, 2, 3, 5, 6, 8),  # 2,3,4,2,2,2
        "6-z24A": (0, 1, 3, 4, 6, 8),  # 2,3,3,3,3,1
        "6-z24B": (0, 2, 4, 5, 7, 8),
        "6-z25A": (0, 1, 3, 5, 6, 8),  # 2,3,3,2,4,1
        "6-z25B": (0, 2, 3, 5, 7, 8),
        "6-z26": (0, 1, 3, 5, 7, 8),  # 2,3,2,3,4,1
        "6-27A": (0, 1, 3, 4, 6, 9),  # 2,2,5,2,2,2
        "6-27B": (0, 2, 3, 5, 6, 9),
        "6-z28": (0, 1, 3, 5, 6, 9),  # 2,2,4,3,2,2
        "6-z29": (0, 2, 3, 6, 7, 9),  # 2,2,4,2,3,2
        "6-30A": (0, 1, 3, 6, 7, 9),  # 2,2,4,2,2,3
        "6-30B": (0, 2, 3, 6, 8, 9),
        "6-31A": (0, 1, 4, 5, 7, 9),  # 2,2,3,4,3,1
        "6-31B": (0, 2, 4, 5, 8, 9),
        "6-32": (0, 2, 4, 5, 7, 9),  # 1,4,3,2,5,0
        "6-33A": (0, 2, 3, 5, 7, 9),  # 1,4,3,2,4,1
        "6-33B": (0, 2, 4, 6, 7, 9),
        "6-34A": (0, 1, 3, 5, 7, 9),  # 1,4,2,4,2,2
        "6-34B": (0, 2, 4, 6, 8, 9),
        "6-35": (0, 2, 4, 6, 8, 10),  # 0,6,0,6,0,3
        "6-z36A": (0, 1, 2, 3, 4, 7),  # 4,3,3,2,2,1
        "6-z36B": (0, 3, 4, 5, 6, 7),
        "6-z37": (0, 1, 2, 3, 4, 8),  # 4,3,2,3,2,1
        "6-z38": (0, 1, 2, 3, 7, 8),  # 4,2,1,2,4,2
        "6-z39A": (0, 2, 3, 4, 5, 8),  # 3,3,3,3,2,1
        "6-z39B": (0, 3, 4, 5, 6, 8),
        "6-z40A": (0, 1, 2, 3, 5, 8),  # 3,3,3,2,3,1
        "6-z40B": (0, 3, 5, 6, 7, 8),
        "6-z41A": (0, 1, 2, 3, 6, 8),  # 3,3,2,2,3,2
        "6-z41B": (0, 2, 5, 6, 7, 8),
        "6-z42": (0, 1, 2, 3, 6, 9),  # 3,2,4,2,2,2
        "6-z43A": (0, 1, 2, 5, 6, 8),  # 3,2,2,3,3,2
        "6-z43B": (0, 2, 3, 6, 7, 8),
        "6-z44A": (0, 1, 2, 5, 6, 9),  # 3,1,3,4,3,1
        "6-z44B": (0, 1, 4, 5, 6, 9),
        "6-z45": (0, 2, 3, 4, 6, 9),  # 2,3,4,2,2,2
        "6-z46A": (0, 1, 2, 4, 6, 9),  # 2,3,3,3,3,1
        "6-z46B": (0, 2, 4, 5, 6, 9),
        "6-z47A": (0, 1, 2, 4, 7, 9),  # 2,3,3,2,4,1
        "6-z47B": (0, 2, 3, 4, 7, 9),
        "6-z48": (0, 1, 2, 5, 7, 9),  # 2,3,2,3,4,1
        "6-z49": (0, 1, 3, 4, 7, 9),  # 2,2,4,3,2,2
        "6-z50": (0, 1, 4, 6, 7, 9),  # 2,2,4,2,3,2
        "7-1": (0, 1, 2, 3, 4, 5, 6),  # 6,5,4,3,2,1
        "7-2A": (0, 1, 2, 3, 4, 5, 7),  # 5,5,4,3,3,1
        "7-2B": (0, 2, 3, 4, 5, 6, 7),
        "7-3A": (0, 1, 2, 3, 4, 5, 8),  # 5,4,4,4,3,1
        "7-3B": (0, 3, 4, 5, 6, 7, 8),
        "7-4A": (0, 1, 2, 3, 4, 6, 7),  # 5,4,4,3,3,2
        "7-4B": (0, 1, 3, 4, 5, 6, 7),
        "7-5A": (0, 1, 2, 3, 5, 6, 7),  # 5,4,3,3,4,2
        "7-5B": (0, 1, 2, 4, 5, 6, 7),
        "7-6A": (0, 1, 2, 3, 4, 7, 8),  # 5,3,3,4,4,2
        "7-6B": (0, 1, 4, 5, 6, 7, 8),
        "7-7A": (0, 1, 2, 3, 6, 7, 8),  # 5,3,2,3,5,3
        "7-7B": (0, 1, 2, 5, 6, 7, 8),
        "7-8": (0, 2, 3, 4, 5, 6, 8),  # 4,5,4,4,2,2
        "7-9A": (0, 1, 2, 3, 4, 6, 8),  # 4,5,3,4,3,2
        "7-9B": (0, 2, 4, 5, 6, 7, 8),
        "7-10A": (0, 1, 2, 3, 4, 6, 9),  # 4,4,5,3,3,2
        "7-10B": (0, 2, 3, 4, 5, 6, 9),
        "7-11A": (0, 1, 3, 4, 5, 6, 8),  # 4,4,4,4,4,1
        "7-11B": (0, 2, 3, 4, 5, 7, 8),
        "7-z12": (0, 1, 2, 3, 4, 7, 9),  # 4,4,4,3,4,2
        "7-13A": (0, 1, 2, 4, 5, 6, 8),  # 4,4,3,5,3,2
        "7-13B": (0, 2, 3, 4, 6, 7, 8),
        "7-14A": (0, 1, 2, 3, 5, 7, 8),  # 4,4,3,3,5,2
        "7-14B": (0, 1, 3, 5, 6, 7, 8),
        "7-15": (0, 1, 2, 4, 6, 7, 8),  # 4,4,2,4,4,3
        "7-16A": (0, 1, 2, 3, 5, 6, 9),  # 4,3,5,4,3,2
        "7-16B": (0, 1, 3, 4, 5, 6, 9),
        "7-z17": (0, 1, 2, 4, 5, 6, 9),  # 4,3,4,5,4,1
        "7-z18A": (0, 1, 4, 5, 6, 7, 9),  # 4,3,4,4,4,2
        "7-z18B": (0, 2, 3, 4, 5, 8, 9),
        "7-19A": (0, 1, 2, 3, 6, 7, 9),  # 4,3,4,3,4,3
        "7-19B": (0, 1, 2, 3, 6, 8, 9),
        "7-20A": (0, 1, 2, 5, 6, 7, 9),  # 0, 2, 3, 4, 7, 8, 9  # 4,3,3,4,5,2
        "7-20B": (0, 2, 3, 4, 7, 8, 9),  # 0, 1, 2, 5, 7, 8, 9
        "7-21A": (0, 1, 2, 4, 5, 8, 9),  # 4,2,4,6,4,1
        "7-21B": (0, 1, 3, 4, 5, 8, 9),
        "7-22": (0, 1, 2, 5, 6, 8, 9),  # 4,2,4,5,4,2
        "7-23A": (0, 2, 3, 4, 5, 7, 9),  # 3,5,4,3,5,1
        "7-23B": (0, 2, 4, 5, 6, 7, 9),
        "7-24A": (0, 1, 2, 3, 5, 7, 9),  # 3,5,3,4,4,2
        "7-24B": (0, 2, 4, 6, 7, 8, 9),
        "7-25A": (0, 2, 3, 4, 6, 7, 9),  # 3,4,5,3,4,2
        "7-25B": (0, 2, 3, 5, 6, 7, 9),
        "7-26A": (0, 1, 3, 4, 5, 7, 9),  # 3,4,4,5,3,2
        "7-26B": (0, 2, 4, 5, 6, 8, 9),
        "7-27A": (0, 1, 2, 4, 5, 7, 9),  # 3,4,4,4,5,1
        "7-27B": (0, 2, 4, 5, 7, 8, 9),
        "7-28A": (0, 1, 3, 5, 6, 7, 9),  # 3,4,4,4,3,3
        "7-28B": (0, 2, 3, 4, 6, 8, 9),
        "7-29A": (0, 1, 2, 4, 6, 7, 9),  # 3,4,4,3,5,2
        "7-29B": (0, 2, 3, 5, 7, 8, 9),
        "7-30A": (0, 1, 2, 4, 6, 8, 9),  # 3,4,3,5,4,2
        "7-30B": (0, 1, 3, 5, 7, 8, 9),
        "7-31A": (0, 1, 3, 4, 6, 7, 9),  # 0, 2, 3, 5, 6, 8, 9 # 3,3,6,3,3,3
        "7-31B": (0, 2, 3, 5, 6, 8, 9),
        "7-32A": (0, 1, 3, 4, 6, 8, 9),  # 3,3,5,4,4,2
        "7-32B": (0, 1, 3, 5, 6, 8, 9),
        "7-33": (0, 1, 2, 4, 6, 8, 10),  # 2,6,2,6,2,3
        "7-34": (0, 1, 3, 4, 6, 8, 10),  # 2,5,4,4,4,2
        "7-35": (0, 1, 3, 5, 6, 8, 10),  # 2,5,4,3,6,1
        "7-z36A": (0, 1, 2, 3, 5, 6, 8),  # 4,4,4,3,4,2
        "7-z36B": (0, 2, 3, 5, 6, 7, 8),
        "7-z37": (0, 1, 3, 4, 5, 7, 8),  # 4,3,4,5,4,1
        "7-z38A": (0, 1, 2, 4, 5, 7, 8),  # 4,3,4,4,4,2
        "7-z38B": (0, 1, 3, 4, 6, 7, 8),
        "8-1": (0, 1, 2, 3, 4, 5, 6, 7),  # 7,6,5,4,4,2
        "8-2A": (0, 1, 2, 3, 4, 5, 6, 8),  # 6,6,5,5,4,2
        "8-2B": (0, 2, 3, 4, 5, 6, 7, 8),
        "8-3": (0, 1, 2, 3, 4, 5, 6, 9),  # 6,5,6,5,4,2
        "8-4A": (0, 1, 2, 3, 4, 5, 7, 8),  # 6,5,5,5,5,2
        "8-4B": (0, 1, 3, 4, 5, 6, 7, 8),
        "8-5A": (0, 1, 2, 3, 4, 6, 7, 8),  # 6,5,4,5,5,3
        "8-5B": (0, 1, 2, 4, 5, 6, 7, 8),
        "8-6": (0, 1, 2, 3, 5, 6, 7, 8),  # 6,5,4,4,6,3
        "8-7": (0, 1, 2, 3, 4, 5, 8, 9),  # 6,4,5,6,5,2
        "8-8": (0, 1, 2, 3, 4, 7, 8, 9),  # 6,4,4,5,6,3
        "8-9": (0, 1, 2, 3, 6, 7, 8, 9),  # 6,4,4,4,6,4
        "8-10": (0, 2, 3, 4, 5, 6, 7, 9),  # 5,6,6,4,5,2
        "8-11A": (0, 1, 2, 3, 4, 5, 7, 9),  # 5,6,5,5,5,2
        "8-11B": (0, 2, 4, 5, 6, 7, 8, 9),  # 5,6,5,5,5,2
        "8-12A": (0, 1, 3, 4, 5, 6, 7, 9),  # 5,5,6,5,4,3
        "8-12B": (0, 2, 3, 4, 5, 6, 8, 9),
        "8-13A": (0, 1, 2, 3, 4, 6, 7, 9),  # 5,5,6,4,5,3
        "8-13B": (0, 2, 3, 5, 6, 7, 8, 9),
        "8-14A": (0, 1, 2, 4, 5, 6, 7, 9),  # 5,5,5,5,6,2
        "8-14B": (0, 2, 3, 4, 5, 7, 8, 9),
        "8-z15A": (0, 1, 2, 3, 4, 6, 8, 9),  # 5,5,5,5,5,3
        "8-z15B": (0, 1, 3, 5, 6, 7, 8, 9),
        "8-16A": (0, 1, 2, 3, 5, 7, 8, 9),  # 5,5,4,5,6,3
        "8-16B": (0, 1, 2, 4, 6, 7, 8, 9),
        "8-17": (0, 1, 3, 4, 5, 6, 8, 9),  # 5,4,6,6,5,2
        "8-18A": (0, 1, 2, 3, 5, 6, 8, 9),  # 5,4,6,5,5,3
        "8-18B": (0, 1, 3, 4, 6, 7, 8, 9),
        "8-19A": (0, 1, 2, 4, 5, 6, 8, 9),  # 5,4,5,7,5,2
        "8-19B": (0, 1, 3, 4, 5, 7, 8, 9),
        "8-20": (0, 1, 2, 4, 5, 7, 8, 9),  # 5,4,5,6,6,2
        "8-21": (0, 1, 2, 3, 4, 6, 8, 10),  # 4,7,4,6,4,3
        "8-22A": (0, 1, 2, 3, 5, 6, 8, 10),  # (0, 1, 2, 3, 5, 6, 8, 10) 4,6,5,5,6,2
        "8-22B": (0, 1, 3, 4, 5, 6, 8, 10),  # 0, 1, 2, 3, 5, 7, 9, 10
        "8-23": (0, 1, 2, 3, 5, 7, 8, 10),  # 4,6,5,4,7,2
        "8-24": (0, 1, 2, 4, 5, 6, 8, 10),  # 4,6,4,7,4,3
        "8-25": (0, 1, 2, 4, 6, 7, 8, 10),  # 4,6,4,6,4,4
        "8-26": (0, 1, 3, 4, 5, 7, 8, 10),  # 4,5,6,5,6,2
        "8-27A": (0, 1, 2, 4, 5, 7, 8, 10),  # 0, 1, 2, 4, 5, 7, 8, 10  # 4,5,6,5,5,3
        "8-27B": (0, 1, 3, 4, 6, 7, 8, 10),  # 0, 1, 2, 4, 6, 7, 9, 10
        "8-28": (0, 1, 3, 4, 6, 7, 9, 10),  # 4,4,8,4,4,4
        "8-z29A": (0, 1, 2, 3, 5, 6, 7, 9),  # 5,5,5,5,5,3
        "8-z29B": (0, 2, 3, 4, 6, 7, 8, 9),
        "9-1": (0, 1, 2, 3, 4, 5, 6, 7, 8),  # 8,7,6,6,6,3
        "9-2A": (0, 1, 2, 3, 4, 5, 6, 7, 9),  # 7,7,7,6,6,3
        "9-2B": (0, 2, 3, 4, 5, 6, 7, 8, 9),
        "9-3A": (0, 1, 2, 3, 4, 5, 6, 8, 9),  # 7,6,7,7,6,3
        "9-3B": (0, 1, 3, 4, 5, 6, 7, 8, 9),
        "9-4A": (0, 1, 2, 3, 4, 5, 7, 8, 9),  # 7,6,6,7,7,3
        "9-4B": (0, 1, 2, 4, 5, 6, 7, 8, 9),
        "9-5A": (0, 1, 2, 3, 4, 6, 7, 8, 9),  # 7,6,6,6,7,4
        "9-5B": (0, 1, 2, 3, 5, 6, 7, 8, 9),
        "9-6": (0, 1, 2, 3, 4, 5, 6, 8, 10),  # 6,8,6,7,6,3
        "9-7A": (0, 1, 2, 3, 4, 5, 7, 8, 10),  # 0, 1, 2, 3, 4, 5, 7, 8, 10 6,7,7,6,7,3
        "9-7B": (0, 1, 3, 4, 5, 6, 7, 8, 10),  # 0, 1, 2, 3, 4, 5, 7, 9, 10
        "9-8A": (
            0,
            1,
            2,
            3,
            4,
            6,
            7,
            8,
            10,
        ),  # 0, 1, 2, 3, 4, 6, 7, 8, 10 # 6,7,6,7,6,4
        "9-8B": (0, 1, 2, 4, 5, 6, 7, 8, 10),  # 0, 1, 2, 3, 4, 6, 8, 9, 10
        "9-9": (0, 1, 2, 3, 5, 6, 7, 8, 10),  # 6,7,6,6,8,3
        "9-10": (0, 1, 2, 3, 4, 6, 7, 9, 10),  # 6,6,8,6,6,4
        "9-11A": (
            0,
            1,
            2,
            3,
            5,
            6,
            7,
            9,
            10,
        ),  # 0, 1, 2, 3, 5, 6, 7, 9, 10  # 6,6,7,7,7,3
        "9-11B": (0, 1, 2, 4, 5, 6, 7, 9, 10),  # 0, 1, 2, 3, 5, 6, 8, 9, 10
        "9-12": (0, 1, 2, 4, 5, 6, 8, 9, 10),  # 6,6,6,9,6,3
        "10-1": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        "10-2": (0, 1, 2, 3, 4, 5, 6, 7, 8, 10),
        "10-3": (0, 1, 2, 3, 4, 5, 6, 7, 9, 10),
        "10-4": (0, 1, 2, 3, 4, 5, 6, 8, 9, 10),
        "10-5": (0, 1, 2, 3, 4, 5, 7, 8, 9, 10),
        "10-6": (0, 1, 2, 3, 4, 6, 7, 8, 9, 10),
        "11-1": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "12-1": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
    }

    pitchSets = []
    names = []
    # 3 Notes
    pitchSets.append([0, 4, 8])
    names.append(["Minoric"])
    # 4 Notes
    pitchSets.append([0, 4, 7, 9])
    names.append(["Epathic", "Mynic", "Rothic", "Eporic"])
    pitchSets.append([0, 4, 7, 11])
    names.append(["Thaptic", "Lothic", "Phratic", "Aerathic"])
    pitchSets.append([0, 4, 6, 9])
    names.append(["Saric", "Zoptic", "Aeraphic", "Byptic"])
    pitchSets.append([0, 4, 7, 10])
    names.append(["Epathaic", "Mynaic", "Rothaic", "Eporaic"])
    pitchSets.append([0, 4, 8, 9])
    names.append(["Aeoloric", "Gonic", "Dalic", "Dygic"])
    pitchSets.append([0, 4, 8, 11])
    names.append(["Zyphic", "Epogic", "Lanic", "Pyrric"])
    pitchSets.append([0, 3, 6, 9])
    names.append(["Phrynic"])
    pitchSets.append([0, 4, 6, 10])
    names.append(["Stathic", "Dadic"])
    pitchSets.append([0, 4, 8, 10])
    names.append(["Aeolic", "Koptic", "Mixolyric", "Lydic"])
    # 5 Notes
    pitchSets.append([0, 3, 5, 8, 10])
    names.append(
        ["Epathitonic", "Mynitonic", "Rocritonic", "Pentatonic", "Thaptitonic"]
    )
    pitchSets.append([0, 4, 5, 7, 9])
    names.append(["Lothitonic", "Phratonic", "Aerathitonic", "Saritonic", "Zoptitonic"])
    pitchSets.append([0, 4, 5, 7, 10])
    names.append(
        ["Aeracritonic", "Byptitonic", "Daritonic", "Lonitonic", "Ionycritonic"]
    )
    pitchSets.append([0, 4, 5, 9, 10])
    names.append(["Phraditonic", "Aeoloritonic", "Gonitonic", "Dalitonic", "Dygitonic"])
    pitchSets.append([0, 4, 6, 7, 11])
    names.append(["Zolitonic", "Epogitonic", "Lanitonic", "Paptitonic", "Ionacritonic"])
    pitchSets.append([0, 4, 6, 9, 11])
    names.append(
        ["Gathitonic", "Ionitonic", "Phrynitonic", "Stathitonic", "Thalitonic"]
    )
    pitchSets.append([0, 4, 7, 9, 11])
    names.append(
        ["Magitonic", "Daditonic", "Aeolyphritonic", "Gycritonic", "Pyritonic"]
    )
    pitchSets.append([0, 3, 6, 7, 10])
    names.append(["Lyditonic", "Mythitonic", "Sogitonic", "Gothitonic", "Rothitonic"])
    pitchSets.append([0, 3, 6, 8, 10])
    names.append(
        ["Kataritonic", "Sylitonic", "Thonitonic", "Phropitonic", "Staditonic"]
    )
    pitchSets.append([0, 3, 6, 8, 11])
    names.append(["Thoditonic", "Dogitonic", "Phralitonic", "Garitonic", "Soptitonic"])
    pitchSets.append([0, 4, 5, 6, 9])
    names.append(["Ionyptitonic", "Gyritonic", "Zalitonic", "Stolitonic", "Bylitonic"])
    pitchSets.append([0, 4, 5, 8, 9])
    names.append(
        ["Zothitonic", "Phrolitonic", "Ionagitonic", "Aeolapritonic", "Kyritonic"]
    )
    pitchSets.append([0, 4, 5, 8, 10])
    names.append(["Epygitonic", "Zaptitonic", "Kagitonic", "Zogitonic", "Epyritonic"])
    pitchSets.append([0, 4, 5, 8, 11])
    names.append(["Lycritonic", "Daptitonic", "Kygitonic", "Mocritonic", "Zynitonic"])
    pitchSets.append([0, 4, 6, 7, 9])
    names.append(
        ["Aeolacritonic", "Zythitonic", "Dyritonic", "Koptitonic", "Thocritonic"]
    )
    pitchSets.append([0, 4, 6, 8, 11])  #
    names.append(["Aeolanitonic", "Danitonic", "Ionaritonic", "Dynitonic", "Zyditonic"])
    pitchSets.append([0, 4, 6, 10, 11])
    names.append(
        ["Zathitonic", "Raditonic", "Stonitonic", "Syptitonic", "Ionythitonic"]
    )
    pitchSets.append([0, 4, 7, 8, 9])
    names.append(
        ["Aeolyritonic", "Goritonic", "Aeoloditonic", "Doptitonic", "Aeraphitonic"]
    )
    pitchSets.append([0, 4, 7, 8, 11])
    names.append(["Zacritonic", "Laritonic", "Thacritonic", "Styditonic", "Loritonic"])
    pitchSets.append([0, 4, 7, 9, 10])
    names.append(
        ["Ionaditonic", "Bocritonic", "Gythitonic", "Pagitonic", "Aeolythitonic"]
    )
    pitchSets.append([0, 4, 7, 10, 11])
    names.append(["Molitonic", "Staptitonic", "Mothitonic", "Aeritonic", "Ragitonic"])
    pitchSets.append([0, 4, 8, 9, 11])
    names.append(["Dolitonic", "Poritonic", "Aerylitonic", "Zagitonic", "Lagitonic"])
    pitchSets.append([0, 3, 6, 9, 10])
    names.append(["Thyritonic", "Thoptitonic", "Bycritonic", "Pathitonic", "Myditonic"])
    pitchSets.append([0, 3, 6, 9, 11])
    names.append(
        ["Mixitonic", "Phrothitonic", "Katycritonic", "Ionalitonic", "Loptitonic"]
    )
    pitchSets.append([0, 4, 6, 7, 10])
    names.append(["Ionoditonic", "Bogitonic", "Mogitonic", "Docritonic", "Epaditonic"])
    pitchSets.append([0, 4, 6, 8, 9])
    names.append(
        ["Aerynitonic", "Palitonic", "Stothitonic", "Aerophitonic", "Katagitonic"]
    )
    pitchSets.append([0, 4, 6, 9, 10])
    names.append(["Phronitonic", "Banitonic", "Aeronitonic", "Golitonic", "Dyptitonic"])
    pitchSets.append([0, 4, 7, 8, 10])
    names.append(["Ryphitonic", "Gylitonic", "Aeolycritonic", "Pynitonic", "Zanitonic"])
    pitchSets.append([0, 4, 8, 9, 10])
    names.append(["Ranitonic", "Laditonic", "Poditonic", "Ionothitonic", "Kanitonic"])
    pitchSets.append([0, 4, 8, 10, 11])
    names.append(["Zylitonic", "Zoditonic", "Zaritonic", "Phrythitonic", "Rolitonic"])
    pitchSets.append([0, 4, 6, 8, 10])
    names.append(["Bolitonic", "Bothitonic", "Kataditonic", "Koditonic", "Tholitonic"])
    # 6 Notes
    pitchSets.append([0, 3, 5, 7, 8, 10])
    names.append(
        ["Epathimic", "Mynimic", "Rocrimic", "Eporimic", "Thaptimic", "Lothimic"]
    )
    pitchSets.append([0, 3, 5, 6, 8, 10])
    names.append(
        ["Phracrimic", "Aerathimic", "Sarimic", "Zoptimic", "Zeracrimic", "Byptimic"]
    )
    pitchSets.append([0, 3, 5, 7, 9, 10])
    names.append(
        ["Darmic", "Lonimic", "Ionycrimic", "Phradimic", "Aeolorimic", "Gonimic"]
    )
    pitchSets.append([0, 3, 5, 7, 10, 11])
    names.append(["Dalimic", "Dygimic", "Zolimic", "Epogimic", "Lanimic", "Paptimic"])
    pitchSets.append([0, 3, 5, 8, 9, 10])
    names.append(
        ["Ionacrimic", "Gathimic", "Ionynimic", "Phrynimic", "Stathimic", "Thatimic"]
    )
    pitchSets.append([0, 3, 5, 8, 10, 11])
    names.append(
        ["Mixolimic", "Dadimic", "Aeolyphimic", "Gycrimic", "Pyrimic", "Lydimic"]
    )
    pitchSets.append([0, 4, 5, 6, 9, 11])
    names.append(["Mythimic", "Sogimic", "Gogimic", "Rothimic", "Katarimic", "Sylimic"])
    pitchSets.append([0, 4, 5, 6, 10, 11])
    names.append(["Thonimic", "Stadimic", "Thodimic"])
    pitchSets.append([0, 4, 5, 7, 9, 10])
    names.append(
        ["Garimic", "Soptimic", "Ionyptimic", "Gyrimic", "Zalimic", "Stolimic"]
    )
    pitchSets.append([0, 4, 5, 7, 9, 11])
    names.append(
        ["Bylimic", "Zothimic", "Phrolimic", "Ionagimic", "Aeolaphimic", "Kycrimic"]
    )
    pitchSets.append([0, 4, 5, 7, 10, 11])
    names.append(["Epygimic", "Zaptimic", "Kagimic", "Zogimic", "Epyrimic", "Lycrimic"])
    pitchSets.append([0, 4, 5, 9, 10, 11])
    names.append(["Daptimic", "Kygimic", "Mocrimic", "Zynimic", "Aeolimic", "Zythimic"])
    pitchSets.append([0, 4, 6, 7, 9, 11])
    names.append(
        ["Dyrimic", "Koptimic", "Thocrimic", "Aeolanimic", "Danimic", "Ionarimic"]
    )
    pitchSets.append([0, 3, 4, 7, 8, 10])
    names.append(["Dynimic", "Zydimic", "Zathimic", "Radimic", "Stonimic", "Syptimic"])
    pitchSets.append([0, 3, 4, 7, 8, 11])
    names.append(["Ionythimic", "Aeologimic"])
    pitchSets.append([0, 3, 5, 6, 8, 11])
    names.append(
        ["Zacrimic", "Larimic", "Thacrimic", "Stydimic", "Lorimic", "Ionadimic"]
    )
    pitchSets.append([0, 3, 5, 6, 9, 10])
    names.append(
        ["Bocrimic", "Gythimic", "Pagimic", "Aeolythimic", "Molimic", "Staptimic"]
    )
    pitchSets.append([0, 3, 5, 7, 8, 11])
    names.append(
        ["Mothimic", "Aeranimic", "Ragimic", "Dolimic", "Porimic", "Aerylimic"]
    )
    pitchSets.append([0, 3, 6, 7, 8, 10])
    names.append(
        ["Zagimic", "Lagimic", "Thyrimic", "Thothimic", "Bycrimic", "Pathimic"]
    )
    pitchSets.append([0, 3, 6, 7, 8, 11])
    names.append(
        ["Mydimic", "Thyptimic", "Phrothimic", "Katycrimic", "Ionalimic", "Loptimic"]
    )
    pitchSets.append([0, 3, 6, 7, 10, 11])
    names.append(
        ["Ionodimic", "Bogimic", "Mogimic", "Docrimic", "Epadimic", "Aerynimic"]
    )
    pitchSets.append([0, 3, 6, 8, 10, 11])
    names.append(
        ["Palimic", "Stothimic", "Aeronimic", "Katagimic", "Phronimic", "Banimic"]
    )
    pitchSets.append([0, 4, 5, 6, 7, 9])
    names.append(
        ["Aeronimic", "Golimic", "Dyptimic", "Ryrimic", "Gylimic", "Aeolycrimic"]
    )
    pitchSets.append([0, 4, 5, 6, 7, 10])
    names.append(["Pynimic", "Zanimic", "Ranimic", "Ladimic", "Podimic", "Ionothimic"])
    pitchSets.append([0, 4, 5, 6, 8, 11])
    names.append(["Kanimic", "Zylimic", "Zodimic", "Zarimic", "Phrythimic", "Rorimic"])
    pitchSets.append([0, 4, 5, 6, 9, 10])
    names.append(["Bolimic", "Bothimic", "Katadimic", "Kodimic", "Tholimic", "Ralimic"])
    pitchSets.append([0, 4, 5, 7, 8, 9])
    names.append(
        ["Syrimic", "Stodimic", "Ionocrimic", "Zycrimic", "Ionygimic", "Katathimic"]
    )
    pitchSets.append([0, 4, 5, 7, 8, 10])
    names.append(
        ["Modimic", "Barimic", "Poptimic", "Sagimic", "Aelothimic", "Socrimic"]
    )
    pitchSets.append([0, 4, 5, 7, 8, 11])
    names.append(
        ["Laptimic", "Lygimic", "Logimic", "Lalimic", "Sothimic", "Phrocrimic"]
    )
    pitchSets.append([0, 4, 5, 8, 9, 10])
    names.append(
        ["Thogimic", "Rythimic", "Donimic", "Aeoloptimic", "Panimic", "Lodimic"]
    )
    pitchSets.append([0, 4, 5, 8, 9, 11])
    names.append(
        ["Solimic", "Ionolimic", "Ionophimic", "Aeologimic", "Zadimic", "Sygimic"]
    )
    pitchSets.append([0, 4, 5, 8, 10, 11])
    names.append(
        ["Phralimic", "Phrogimic", "Rathimic", "Katocrimic", "Phryptimic", "Katynimic"]
    )
    pitchSets.append([0, 4, 6, 7, 8, 11])
    names.append(
        ["Aerycrimic", "Ganimic", "Eparimic", "Lyrimic", "Phraptimic", "Bacrimic"]
    )
    pitchSets.append([0, 4, 6, 7, 10, 11])
    names.append(
        ["Katythimic", "Madimic", "Aerygimic", "Pylimic", "Ionathimic", "Morimic"]
    )
    pitchSets.append([0, 4, 6, 8, 9, 11])
    names.append(
        ["Rycrimic", "Ronimic", "Stycrimic", "Katorimic", "Epythimic", "Kaptimic"]
    )
    pitchSets.append([0, 4, 6, 9, 10, 11])
    names.append(
        ["Stalimic", "Stoptimic", "Zygimic", "Kataptimic", "Aeolaptimic", "Pothimic"]
    )
    pitchSets.append([0, 4, 7, 8, 9, 11])
    names.append(
        ["Bygimic", "Thycrimic", "Aeoladimic", "Dylimic", "Eponimic", "Katygimic"]
    )
    pitchSets.append([0, 4, 7, 9, 10, 11])
    names.append(
        ["Starimic", "Phrathimic", "Saptimic", "Aerodimic", "Macrimic", "Rogimic"]
    )
    pitchSets.append([0, 3, 4, 6, 8, 10])
    names.append(
        ["Boptimic", "Stogimic", "Thynimic", "Aeolathimic", "Bythimic", "Padimic"]
    )
    pitchSets.append([0, 3, 4, 6, 9, 10])
    names.append(["Lythimic", "Dodimic", "Katalimic"])
    pitchSets.append([0, 3, 5, 6, 9, 11])
    names.append(["Aeradimic", "Zyrimic", "Stylimic"])
    pitchSets.append([0, 3, 5, 7, 9, 11])
    names.append(
        ["Aeragimic", "Epothimic", "Salimic", "Lyptimic", "Katonimic", "Gygimic"]
    )
    pitchSets.append([0, 3, 5, 8, 9, 11])
    names.append(["Stythimic", "Kothimic", "Pygimic", "Rodimic", "Sorimic", "Monimic"])
    pitchSets.append([0, 3, 6, 7, 9, 10])
    names.append(
        ["Thalimic", "Stygimic", "Aeolygimic", "Aerogimic", "Dacrimic", "Baptimic"]
    )
    pitchSets.append([0, 3, 6, 7, 9, 11])
    names.append(
        ["Dagimic", "Aeolydimic", "Parimic", "Ionaptimic", "Thylimic", "Lolimic"]
    )
    pitchSets.append([0, 3, 6, 8, 9, 10])
    names.append(
        ["Thagimic", "Kolimic", "Dycrimic", "Epycrimic", "Gocrimic", "Katolimic"]
    )
    pitchSets.append([0, 3, 6, 8, 9, 11])
    names.append(
        ["Thoptimic", "Bagimic", "Kyrimic", "Sonimic", "Aeolonimic", "Rygimic"]
    )
    pitchSets.append([0, 3, 6, 9, 10, 11])
    names.append(
        ["Epynimic", "Ionogimic", "Kydimic", "Gaptimic", "Tharimic", "Ionaphimic"]
    )
    pitchSets.append([0, 4, 5, 6, 8, 9])
    names.append(
        ["Aerothimic", "Stagimic", "Dorimic", "Phrycrimic", "Kyptimic", "Ionylimic"]
    )
    pitchSets.append([0, 4, 5, 6, 8, 10])
    names.append(
        ["Mycrimic", "Ionorimic", "Phrydimic", "Zyptimic", "Katothimic", "Phrylimic"]
    )
    pitchSets.append([0, 4, 6, 7, 8, 9])
    names.append(["Kocrimic", "Korimic", "Lynimic", "Malimic", "Synimic", "Phragimic"])
    pitchSets.append([0, 4, 6, 7, 9, 10])
    names.append(["Manimic", "Marimic", "Locrimic", "Rylimic", "Epatimic", "Byrimic"])
    pitchSets.append([0, 4, 6, 8, 10, 11])
    names.append(
        ["Katanimic", "Katyrimic", "Rynimic", "Pogimic", "Aeraptimic", "Epylimic"]
    )
    pitchSets.append([0, 4, 7, 8, 9, 10])
    names.append(
        ["Galimic", "Kathimic", "Lylimic", "Epalimic", "Epacrimic", "Sathimic"]
    )
    pitchSets.append([0, 4, 7, 8, 10, 11])
    names.append(
        ["Lathimic", "Aeralimic", "Kynimic", "Stynimic", "Epytimic", "Katoptimic"]
    )
    pitchSets.append([0, 4, 8, 9, 10, 11])
    names.append(["Ponimic", "Kadimic", "Gynimic", "Thydimic", "Polimic", "Thanimic"])
    pitchSets.append([0, 4, 6, 7, 8, 10])
    names.append(
        ["Gacrimic", "Borimic", "Sycrimic", "Gadimic", "Aeolocrimic", "Phrygimic"]
    )
    pitchSets.append([0, 4, 6, 8, 9, 10])
    names.append(
        ["Dathimic", "Epagimic", "Raptimic", "Epolimic", "Sythimic", "Sydimic"]
    )
    pitchSets.append([0, 2, 4, 6, 8, 10])
    names.append(["Kylimic"])
    # 7 Notes
    pitchSets.append([0, 2, 4, 6, 7, 9, 11])
    names.append(
        ["Lydian", "Mixolydian", "Aeolian", "Locrian", "Ionian", "Dorian", "Phrygian"]
    )
    pitchSets.append([0, 3, 4, 5, 7, 8, 10])
    names.append(
        ["Aerathian", "Sarian", "Zoptian", "Aeracrian", "Byptian", "Darian", "Lonian"]
    )
    pitchSets.append([0, 3, 4, 5, 7, 9, 10])
    names.append(
        ["Ionycrian", "Phradian", "Aeolorian", "Gonian", "Dalian", "Dygian", "Zolian"]
    )
    pitchSets.append([0, 3, 4, 5, 8, 9, 10])
    names.append(
        [
            "Epogian",
            "Lanian",
            "Paptian",
            "Ionacrian",
            "Gathian",
            "Ionyphian",
            "Phrynian",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 8, 10])
    names.append(
        [
            "Stathian",
            "Mixonyphian",
            "Magian",
            "Dadian",
            "Aeolylian",
            "Gycrian",
            "Pyrian",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 10, 11])
    names.append(
        ["Epathian", "Mythian", "Sogian", "Gogian", "Rothian", "Katarian", "Stylian"]
    )
    pitchSets.append([0, 3, 5, 6, 8, 10, 11])
    names.append(
        ["Thonian", "Phrorian", "Stadian", "Thodian", "Dogian", "Mixopyrian", "Garian"]
    )
    pitchSets.append([0, 3, 5, 7, 8, 9, 10])
    names.append(
        ["Soptian", "Ionyptian", "Gyrian", "Zalian", "Stolian", "Bylian", "Zothian"]
    )
    pitchSets.append([0, 3, 5, 7, 8, 10, 11])
    names.append(
        ["Phrolian", "Ionagian", "Aeodian", "Kycrian", "Epygian", "Zaptian", "Kagian"]
    )
    pitchSets.append([0, 4, 5, 6, 7, 9, 11])
    names.append(
        ["Zogian", "Epyrian", "Lycrian", "Daptian", "Kygian", "Mocrian", "Zynian"]
    )
    pitchSets.append([0, 4, 5, 6, 7, 10, 11])
    names.append(
        [
            "Aeolacrian",
            "Zythian",
            "Dyrian",
            "Koptian",
            "Thocrian",
            "Aeolanian",
            "Danian",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 9, 10, 11])
    names.append(
        ["Ionarian", "Dynian", "Zydian", "Zathian", "Radian", "Stonian", "Syptian"]
    )
    pitchSets.append([0, 4, 5, 7, 9, 10, 11])
    names.append(
        [
            "Ionythian",
            "Aeolyrian",
            "Gorian",
            "Aeolodian",
            "Doptian",
            "Aeraphian",
            "Zacrian",
        ]
    )
    pitchSets.append([0, 2, 4, 6, 8, 9, 11])
    names.append(
        ["Larian", "Lythian", "Stydian", "Lorian", "Ionadian", "Bocrian", "Mixolythian"]
    )
    pitchSets.append([0, 3, 4, 5, 6, 8, 10])
    names.append(
        ["Pagian", "Aeolythian", "Molian", "Staptian", "Mothian", "Aeranian", "Ragian"]
    )
    pitchSets.append([0, 3, 4, 5, 7, 9, 11])
    names.append(
        ["Dolian", "Porian", "Aerylian", "Zagian", "Lagian", "Tyrian", "Mixonorian"]
    )
    pitchSets.append([0, 3, 4, 6, 7, 9, 11])
    names.append(
        [
            "Bycrian",
            "Pathian",
            "Mydian",
            "Thyptian",
            "Phrothian",
            "Katycrian",
            "Ionalian",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 7, 10, 11])
    names.append(
        ["Loptian", "Ionodian", "Bogian", "Mogian", "Docrian", "Epadian", "Aerynian"]
    )
    pitchSets.append([0, 3, 4, 6, 8, 9, 11])
    names.append(
        ["Palian", "Stothian", "Aerorian", "Katagian", "Phronian", "Banian", "Aeronian"]
    )
    pitchSets.append([0, 3, 4, 6, 8, 10, 11])
    names.append(
        ["Golian", "Dyptian", "Ryphian", "Gylian", "Aeolycrian", "Pynian", "Zanian"]
    )
    pitchSets.append([0, 3, 4, 6, 9, 10, 11])
    names.append(
        ["Ranian", "Ladian", "Podian", "Ionothian", "Kanian", "Zylian", "Zodian"]
    )
    pitchSets.append([0, 3, 4, 7, 8, 9, 10])
    names.append(
        ["Zarian", "Phrythian", "Rorian", "Bolian", "Bothian", "Katadian", "Kodian"]
    )
    pitchSets.append([0, 3, 4, 7, 8, 9, 11])
    names.append(
        ["Tholian", "Ralian", "Syrian", "Stodian", "Ionocrian", "Zycrian", "Ionygian"]
    )
    pitchSets.append([0, 3, 4, 7, 8, 10, 11])
    names.append(
        [
            "Katathian",
            "Modian",
            "Barian",
            "Mixolocrian",
            "Sagian",
            "Aeolothian",
            "Socrian",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 8, 11])
    names.append(
        ["Laptian", "Lygian", "Logian", "Lalian", "Sothian", "Phrocrian", "Thogian"]
    )
    pitchSets.append([0, 3, 5, 6, 7, 9, 10])
    names.append(
        ["Rythian", "Donian", "Aeoloptian", "Panian", "Lodian", "Solian", "Ionolian"]
    )
    pitchSets.append([0, 3, 5, 6, 8, 9, 10])
    names.append(
        ["Ionopian", "Aeologian", "Zadian", "Sygian", "Phralian", "Phrogian", "Rathian"]
    )
    pitchSets.append([0, 3, 5, 6, 9, 10, 11])
    names.append(
        [
            "Katocrian",
            "Phryptian",
            "Katynian",
            "Aerycrian",
            "Ganian",
            "Eparian",
            "Lyrian",
        ]
    )
    pitchSets.append([0, 3, 5, 7, 9, 10, 11])
    names.append(
        [
            "Phraptian",
            "Bacrian",
            "Katythian",
            "Madian",
            "Aerygian",
            "Pylian",
            "Ionathian",
        ]
    )
    pitchSets.append([0, 3, 5, 8, 9, 10, 11])
    names.append(
        ["Morian", "Rycrian", "Ronian", "Stycrian", "Katorian", "Epythian", "Kaptian"]
    )
    pitchSets.append([0, 3, 6, 7, 8, 10, 11])
    names.append(
        [
            "Stalian",
            "Stoptian",
            "Zygian",
            "Kataptian",
            "Aeolaptian",
            "Pothian",
            "Bygian",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 8, 11])
    names.append(
        [
            "Thycrian",
            "Aeoladian",
            "Dylian",
            "Eponian",
            "Katygian",
            "Starian",
            "Phrathian",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 9, 10])
    names.append(
        ["Saptian", "Aerodian", "Macrian", "Rogian", "Boptian", "Stogian", "Thynian"]
    )
    pitchSets.append([0, 4, 5, 6, 8, 9, 11])
    names.append(
        ["Aeolathian", "Bythian", "Padian", "Rolian", "Pydian", "Thygian", "Katalian"]
    )
    pitchSets.append([0, 4, 5, 6, 8, 10, 11])
    names.append(
        [
            "Thacrian",
            "Dodian",
            "Aeolyptian",
            "Aeolonian",
            "Aeradian",
            "Aeolagian",
            "Zyrian",
        ]
    )
    pitchSets.append([0, 4, 5, 7, 8, 9, 10])
    names.append(
        ["Stylian", "Aeragian", "Epothian", "Salian", "Lyptian", "Katonian", "Gyphian"]
    )
    pitchSets.append([0, 4, 5, 7, 8, 9, 11])
    names.append(
        ["Stythian", "Kothian", "Pygian", "Rodian", "Sorian", "Monian", "Thalian"]
    )
    pitchSets.append([0, 4, 5, 7, 8, 10, 11])
    names.append(
        [
            "Stygian",
            "Aeolygian",
            "Aerogian",
            "Dacrian",
            "Baptian",
            "Dagian",
            "Aeolydian",
        ]
    )
    pitchSets.append([0, 4, 5, 8, 9, 10, 11])
    names.append(
        ["Parian", "Ionaptian", "Thylian", "Lolian", "Thagian", "Kolian", "Dycrian"]
    )
    pitchSets.append([0, 4, 6, 7, 8, 9, 11])
    names.append(
        ["Epycrian", "Gocrian", "Katolian", "Thoptian", "Bagian", "Kyrian", "Sonian"]
    )
    pitchSets.append([0, 4, 6, 7, 9, 10, 11])
    names.append(
        ["Aeopian", "Rygian", "Epynian", "Ionogian", "Kydian", "Gaptian", "Tharian"]
    )
    pitchSets.append([0, 3, 4, 6, 7, 8, 10])
    names.append(
        [
            "Ionanian",
            "Aerothian",
            "Stagian",
            "Lothian",
            "Phrycrian",
            "Kyptian",
            "Ionylian",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 7, 9, 10])
    names.append(
        [
            "Mycrian",
            "Ionorian",
            "Phrydian",
            "Zyptian",
            "Katothian",
            "Phrylian",
            "Kocrian",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 8, 9, 10])
    names.append(
        ["Korian", "Lynian", "Malian", "Synian", "Phragian", "Manian", "Marian"]
    )
    pitchSets.append([0, 3, 5, 6, 7, 9, 11])
    names.append(
        ["Eporian", "Rylian", "Epaptian", "Byrian", "Katanian", "Katyrian", "Rynian"]
    )
    pitchSets.append([0, 3, 5, 6, 8, 9, 11])
    names.append(
        ["Pogian", "Aeraptian", "Epylian", "Gamian", "Kathian", "Lylian", "Epalian"]
    )
    pitchSets.append([0, 3, 5, 7, 8, 9, 11])
    names.append(
        ["Epacrian", "Sathian", "Lathian", "Aeralian", "Kynian", "Stynian", "Epyphian"]
    )
    pitchSets.append([0, 3, 6, 7, 8, 9, 10])
    names.append(
        ["Katoptian", "Ponian", "Kadian", "Gynian", "Thyphian", "Polian", "Thanian"]
    )
    pitchSets.append([0, 3, 6, 7, 8, 9, 11])
    names.append(
        [
            "Gacrian",
            "Borian",
            "Sycrian",
            "Gadian",
            "Aeolocrian",
            "Mixodorian",
            "Dathian",
        ]
    )
    pitchSets.append([0, 3, 6, 7, 9, 10, 11])
    names.append(
        ["Epagian", "Raptian", "Epolian", "Sythian", "Sydian", "Epocrain", "Kylian"]
    )
    pitchSets.append([0, 3, 6, 8, 9, 10, 11])
    names.append(
        ["Bonian", "Badian", "Katodian", "Sadian", "Dothian", "Moptian", "Aeryrian"]
    )
    pitchSets.append([0, 4, 5, 6, 7, 8, 9])
    names.append(
        [
            "Katyptian",
            "Epodian",
            "Mygian",
            "Pacrian",
            "Aerocrian",
            "Aeolarian",
            "Kythian",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 8, 10])
    names.append(
        ["Stanian", "Epanian", "Konian", "Stocrian", "Kalian", "Phroptian", "Dydian"]
    )
    pitchSets.append([0, 4, 5, 6, 8, 9, 10])
    names.append(
        ["Katacrian", "Sodian", "Bathian", "Mylian", "Godian", "Thorian", "Zocrian"]
    )
    pitchSets.append([0, 4, 6, 7, 8, 10, 11])
    names.append(
        [
            "Katogian",
            "Stacrian",
            "Styrian",
            "Ionyrian",
            "Phrodian",
            "Pycrian",
            "Gyptian",
        ]
    )
    pitchSets.append([0, 4, 6, 8, 9, 10, 11])
    names.append(
        ["Pythian", "Katylian", "Bydian", "Bynian", "Galian", "Zonian", "Myrian"]
    )
    pitchSets.append([0, 4, 7, 8, 9, 10, 11])
    names.append(
        ["Thadian", "Sanian", "Ionydian", "Epydian", "Katydian", "Mathian", "Aeryptian"]
    )
    pitchSets.append([0, 2, 4, 6, 8, 10, 11])
    names.append(
        [
            "Aeolynian",
            "Aeroptian",
            "Phryrian",
            "Gothian",
            "Storian",
            "Pyptian",
            "Thydian",
        ]
    )
    pitchSets.append([0, 4, 6, 7, 8, 9, 10])
    names.append(
        ["Gydian", "Kogian", "Rarian", "Aerolian", "Karian", "Myptian", "Rydian"]
    )
    # 8 Notes
    pitchSets.append([0, 2, 4, 5, 7, 9, 10, 11])
    names.append(
        [
            "Aerycryllic",
            "Gadyllic",
            "Solyllic",
            "Zylyllic",
            "Mixodyllic",
            "Soryllic",
            "Godyllic",
            "Epiphyllic",
        ]
    )
    pitchSets.append([0, 2, 4, 5, 7, 8, 9, 11])
    names.append(
        [
            "Ionoptyllic",
            "Aeoloryllic",
            "Thydyllic",
            "Gycryllic",
            "Lyryllic",
            "Mogyllic",
            "Katodyllic",
            "Moptyllic",
        ]
    )
    pitchSets.append([0, 2, 4, 6, 7, 8, 9, 11])
    names.append(
        [
            "Ionocryllic",
            "Gocryllic",
            "Epiryllic",
            "Aeradyllic",
            "Staptyllic",
            "Danyllic",
            "Goptyllic",
            "Epocryllic",
        ]
    )
    pitchSets.append([0, 2, 4, 6, 7, 9, 10, 11])
    names.append(
        [
            "Rocryllic",
            "Zyryllic",
            "Sagyllic",
            "Epinyllic",
            "Katagyllic",
            "Ragyllic",
            "Gothyllic",
            "Lythyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 8, 10, 11])
    names.append(
        [
            "Bacryllic",
            "Aerygyllic",
            "Dathyllic",
            "Boptyllic",
            "Bagyllic",
            "Mathyllic",
            "Styptyllic",
            "Zolyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 9, 10, 11])
    names.append(["Sydyllic", "Katogyllic", "Zygyllic", "Aeralyllic"])
    pitchSets.append([0, 3, 4, 5, 7, 8, 9, 10])
    names.append(
        [
            "Dagyllic",
            "Katalyllic",
            "Katoryllic",
            "Dodyllic",
            "Zogyllic",
            "Madyllic",
            "Dycryllic",
            "Aeologyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 7, 8, 10, 11])
    names.append(
        [
            "Dydyllic",
            "Thogyllic",
            "Rygyllic",
            "Bycryllic",
            "Zacryllic",
            "Panyllic",
            "Dyryllic",
            "Zathyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 7, 9, 10, 11])
    names.append(
        [
            "Eponyllic",
            "Thocryllic",
            "Lacryllic",
            "Katynyllic",
            "Maryllic",
            "Mothyllic",
            "Mixothyllic",
            "Bodyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 8, 9, 10, 11])
    names.append(
        [
            "Kalyllic",
            "Ionodyllic",
            "Bythyllic",
            "Epagyllic",
            "Gaptyllic",
            "Aeroptyllic",
            "Mylyllic",
            "Galyllic",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 8, 10, 11])
    names.append(
        [
            "Pothyllic",
            "Phronyllic",
            "Stynyllic",
            "Rathyllic",
            "Aeryptyllic",
            "Zydyllic",
            "Katolyllic",
            "Rythyllic",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 9, 10, 11])
    names.append(
        [
            "Pynyllic",
            "Bocryllic",
            "Kogyllic",
            "Raryllic",
            "Zycryllic",
            "Mycryllic",
            "Laptyllic",
            "Pylyllic",
        ]
    )
    pitchSets.append([0, 2, 4, 5, 6, 8, 10, 11])
    names.append(["Roryllic", "Epotyllic", "Epidyllic", "Kaptyllic"])
    pitchSets.append([0, 2, 4, 5, 7, 8, 10, 11])
    names.append(
        [
            "Stogyllic",
            "Ionidyllic",
            "Stonyllic",
            "Stalyllic",
            "Poryllic",
            "Mocryllic",
            "Aeolyryllic",
            "Baryllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 8, 10])
    names.append(
        [
            "Kataryllic",
            "Aerocryllic",
            "Zanyllic",
            "Aeolonyllic",
            "Aeonyllic",
            "Kyryllic",
            "Sythyllic",
            "Katycryllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 9, 10])
    names.append(
        [
            "Tharyllic",
            "Sylyllic",
            "Lothyllic",
            "Daryllic",
            "Monyllic",
            "Styryllic",
            "Aeolacryllic",
            "Raptyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 9, 11])
    names.append(
        [
            "Gythyllic",
            "Pyryllic",
            "Rycryllic",
            "Phrathyllic",
            "Badyllic",
            "Phrocryllic",
            "Staryllic",
            "Zothyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 8, 9, 11])
    names.append(
        [
            "Aeolathyllic",
            "Aeolocryllic",
            "Phroptyllic",
            "Kodyllic",
            "Epaptyllic",
            "Ionoyllic",
            "Gyptyllic",
            "Aerythyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 8, 9, 11])
    names.append(
        [
            "Phragyllic",
            "Aeranyllic",
            "Dothyllic",
            "Lygyllic",
            "Stadyllic",
            "Byptyllic",
            "Stodyllic",
            "Zynyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 7, 8, 9, 11])
    names.append(
        [
            "Lonyllic",
            "Sathyllic",
            "Layllic",
            "Saryllic",
            "Thacryllic",
            "Aeolynyllic",
            "Thadyllic",
            "Lynyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 7, 8, 9, 11])
    names.append(
        [
            "Doptyllic",
            "Ionilyllic",
            "Manyllic",
            "Polyllic",
            "Stanyllic",
            "Mixotharyllic",
            "Eporyllic",
            "Aerynyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 7, 8, 10, 11])
    names.append(
        [
            "Thyptyllic",
            "Ionogyllic",
            "Aeolaryllic",
            "Katygyllic",
            "Ganyllic",
            "Kyptyllic",
            "Salyllic",
            "Sanyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 7, 9, 10, 11])
    names.append(
        [
            "Maptyllic",
            "Aeraptyllic",
            "Katadyllic",
            "Magyllic",
            "Phrylyllic",
            "Epigyllic",
            "Molyllic",
            "Ponyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 8, 9, 10, 11])
    names.append(
        [
            "Aeolothyllic",
            "Ionyryllic",
            "Rydyllic",
            "Gonyllic",
            "Rolyllic",
            "Katydyllic",
            "Zyptyllic",
            "Modyllic",
        ]
    )
    pitchSets.append([0, 3, 4, 7, 8, 9, 10, 11])
    names.append(
        [
            "Ioniptyllic",
            "Kycryllic",
            "Aeolaptyllic",
            "Rodyllic",
            "Ionathyllic",
            "Pythyllic",
            "Zonyllic",
            "Ryryllic",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 8, 9, 11])
    names.append(
        [
            "Aeronyllic",
            "Pycryllic",
            "Mygyllic",
            "Lylyllic",
            "Daptyllic",
            "Ioninyllic",
            "Epaphyllic",
            "Lolyllic",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 9, 10, 11])
    names.append(
        [
            "Zoryllic",
            "Phrolyllic",
            "Kolyllic",
            "Thodyllic",
            "Socryllic",
            "Aeolyllic",
            "Zythyllic",
            "Aeoryllic",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 8, 9, 10, 11])
    names.append(
        [
            "Lydyllic",
            "Radyllic",
            "Stagyllic",
            "Ionoryllic",
            "Phrodyllic",
            "Aeoryllic",
            "Banyllic",
            "Epothyllic",
        ]
    )
    pitchSets.append([0, 3, 5, 7, 8, 9, 10, 11])
    names.append(
        [
            "Phranyllic",
            "Stydyllic",
            "Zadyllic",
            "Zalyllic",
            "Zocryllic",
            "Katocryllic",
            "Aerathyllic",
            "Stoptyllic",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 8, 9, 11])
    names.append(
        [
            "Phroryllic",
            "Thyphyllic",
            "Poptyllic",
            "Mixonyllic",
            "Paptyllic",
            "Storyllic",
            "Phrycryllic",
            "Palyllic",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 8, 10, 11])
    names.append(
        [
            "Aeoladyllic",
            "Kocryllic",
            "Lodyllic",
            "Bynyllic",
            "Kydyllic",
            "Bygyllic",
            "Phryptyllic",
            "Ionayllic",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 8, 9, 10, 11])
    names.append(
        [
            "Thagyllic",
            "Thoptyllic",
            "Phraptyllic",
            "Gylyllic",
            "Phralyllic",
            "Dygyllic",
            "Ronyllic",
            "Epogyllic",
        ]
    )
    pitchSets.append([0, 4, 5, 7, 8, 9, 10, 11])
    names.append(
        [
            "Dolyllic",
            "Moryllic",
            "Bydyllic",
            "Pocryllic",
            "Phracryllic",
            "Gyryllic",
            "Phrygyllic",
            "Dogyllic",
        ]
    )
    pitchSets.append([0, 2, 3, 5, 6, 8, 9, 11])
    names.append(["Epadyllic", "Ladyllic"])
    pitchSets.append([0, 2, 4, 5, 6, 8, 10, 11])
    names.append(["Thalyllic", "Saptyllic", "Pygyllic", "Rogyllic"])
    pitchSets.append([0, 2, 4, 6, 7, 8, 10, 11])
    names.append(
        [
            "Racryllic",
            "Epicryllic",
            "Stygyllic",
            "Syryllic",
            "Stythyllic",
            "Aerothyllic",
            "Mixoryllic",
            "Thanyllic",
        ]
    )
    pitchSets.append([0, 2, 4, 6, 8, 9, 10, 11])
    names.append(
        [
            "Thyryllic",
            "Gygyllic",
            "Sodyllic",
            "Goryllic",
            "Bothyllic",
            "Gynyllic",
            "Ionaptyllic",
            "Phryryllic",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 7, 8, 9, 10])
    names.append(
        [
            "Stacryllic",
            "Doryllic",
            "Kadyllic",
            "Rynyllic",
            "Aerogyllic",
            "Rothyllic",
            "Kagyllic",
            "Stathyllic",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 8, 9, 11])
    names.append(
        [
            "Phrydyllic",
            "Dadyllic",
            "Aeodyllic",
            "Aerolyllic",
            "Zoptyllic",
            "Epanyllic",
            "Katoptyllic",
            "Podyllic",
        ]
    )
    pitchSets.append([0, 3, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Zaryllic",
            "Dythyllic",
            "Ionaryllic",
            "Laryllic",
            "Kataptyllic",
            "Sonyllic",
            "Pathyllic",
            "Loryllic",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 8, 9, 10])
    names.append(
        [
            "Stolyllic",
            "Logyllic",
            "Dacryllic",
            "Thynyllic",
            "Gydyllic",
            "Eparyllic",
            "Dynyllic",
            "Ionyllic",
        ]
    )
    pitchSets.append([0, 4, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Stycryllic",
            "Ionothyllic",
            "Mythyllic",
            "Aerylyllic",
            "Bonyllic",
            "Tholyllic",
            "Katyryllic",
            "Sadyllic",
        ]
    )
    # 9 Notes
    pitchSets.append([0, 2, 4, 5, 6, 7, 9, 10, 11])
    names.append(
        [
            "Aerycrygic",
            "Gadygic",
            "Solygic",
            "Zylygic",
            "Garygic",
            "Sorygic",
            "Godygic",
            "Epithygic",
            "Ionoptygic",
        ]
    )
    pitchSets.append([0, 2, 3, 5, 6, 7, 8, 10, 11])
    names.append(
        [
            "Aeolorygic",
            "Thydygic",
            "Gycrygic",
            "Lyrygic",
            "Modygic",
            "Katodygic",
            "Moptygic",
            "Ionocrygic",
            "Gocrygic",
        ]
    )
    pitchSets.append([0, 2, 3, 5, 6, 7, 9, 10, 11])
    names.append(
        [
            "Epyrygic",
            "Aeradygic",
            "Staptygic",
            "Danygic",
            "Goptygic",
            "Epocrygic",
            "Rocrygic",
            "Zyrygic",
            "Sadygic",
        ]
    )
    pitchSets.append([0, 2, 4, 5, 6, 7, 8, 9, 11])
    names.append(
        [
            "Apinygic",
            "Katagygic",
            "Radygic",
            "Gothygic",
            "Lythygic",
            "Bacrygic",
            "Aerygic",
            "Dathygic",
            "Boptygic",
        ]
    )
    pitchSets.append([0, 2, 4, 5, 7, 8, 9, 10, 11])
    names.append(
        [
            "Bagygic",
            "Mathygic",
            "Styptygic",
            "Zolygic",
            "Sydygic",
            "Katygic",
            "Zyphygic",
            "Aeralygic",
            "Ryptygic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 8, 10, 11])
    names.append(
        [
            "Loptygic",
            "Katylygic",
            "Phradygic",
            "Mixodygic",
            "Katalygic",
            "Katorygic",
            "Dogygic",
            "Zodygic",
            "Madygic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 9, 10, 11])
    names.append(
        [
            "Dycrygic",
            "Aeolygic",
            "Dydygic",
            "Tholygic",
            "Rynygic",
            "Bycrygic",
            "Zacrygic",
            "Panygic",
            "Dyrygic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 8, 9, 10, 11])
    names.append(
        [
            "Zathygic",
            "Epitygic",
            "Thocrygic",
            "Lacrygic",
            "Katynygic",
            "Marygic",
            "Mothygic",
            "Thophygic",
            "Bodygic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 7, 8, 9, 10, 11])
    names.append(
        [
            "Kalygic",
            "Ionodygic",
            "Bythygic",
            "Mixolygic",
            "Gaptygic",
            "Aeroptygic",
            "Mylygic",
            "Galygic",
            "Pothygic",
        ]
    )
    pitchSets.append([0, 2, 3, 4, 6, 7, 8, 10, 11])
    names.append(["Phronygic", "Stynygic", "Zydygic"])
    pitchSets.append([0, 2, 3, 5, 6, 8, 9, 10, 11])
    names.append(
        [
            "Koptygic",
            "Raphygic",
            "Zycrygic",
            "Mycrygic",
            "Laptygic",
            "Pylygic",
            "Rodygic",
            "Epolygic",
            "Epidygic",
        ]
    )
    pitchSets.append([0, 2, 4, 5, 6, 7, 8, 10, 11])
    names.append(
        [
            "Kaptygic",
            "Sacrygic",
            "Padygic",
            "Epilygic",
            "Kynygic",
            "Stophygic",
            "Ionidygic",
            "Stonygic",
            "Stalygic",
        ]
    )
    pitchSets.append([0, 2, 4, 5, 6, 8, 9, 10, 11])
    names.append(
        [
            "Porygic",
            "Mocrygic",
            "Aeolyrigic",
            "Barygic",
            "Katarygic",
            "Aerocrygic",
            "Zanygic",
            "Aeolonygic",
            "Aeolanygic",
        ]
    )
    pitchSets.append([0, 2, 4, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Kyrygic",
            "Sythygic",
            "Katycrygic",
            "Tharygic",
            "Sylygic",
            "Lothygic",
            "Darygic",
            "Monygic",
            "Styrygic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 8, 9, 10])
    names.append(
        [
            "Aeolacrygic",
            "Raptygic",
            "Gythygic",
            "Pyrygic",
            "Rycrygic",
            "Phrathygic",
            "Badygic",
            "Phrocrygic",
            "Starygic",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 8, 9, 11])
    names.append(
        [
            "Zothygic",
            "Aeolathygic",
            "Aeolocrygic",
            "Phroptygic",
            "Kodygic",
            "Eparygic",
            "Ionygic",
            "Gyptygic",
            "Aerythygic",
        ]
    )
    pitchSets.append([0, 3, 4, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Phrygic",
            "Aeranygic",
            "Dothygic",
            "Lydygic",
            "Stadygic",
            "Byptygic",
            "Stodygic",
            "Zynygic",
            "Lonygic",
        ]
    )
    pitchSets.append([0, 3, 5, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Sathygic",
            "Ladygic",
            "Sarygic",
            "Thacrygic",
            "Aeolynygic",
            "Thadygic",
            "Lynygic",
            "Doptygic",
            "Ionilygic",
        ]
    )
    pitchSets.append([0, 4, 5, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Manygic",
            "Polygic",
            "Stanygic",
            "Thaptygic",
            "Eporygic",
            "Aerynygic",
            "Thyptygic",
            "Ionogygic",
            "Aeolarygic",
        ]
    )
    # 10 Notes
    pitchSets.append([0, 2, 3, 4, 5, 7, 8, 9, 10, 11])
    names.append(
        [
            "Aerycryllian",
            "Gadyllian",
            "Solyllian",
            "Zyphyllian",
            "Garyllian",
            "Soryllian",
            "Godyllian",
            "Epityllian",
            "Ionyllian",
            "Aeoryllian",
        ]
    )
    pitchSets.append([0, 2, 3, 4, 5, 6, 8, 9, 10, 11])
    names.append(["Thydyllian", "Epiryllian", "Lyryllian", "Mogyllian", "Katodyllian"])
    pitchSets.append([0, 2, 3, 4, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Staptyllian",
            "Danyllian",
            "Goptyllian",
            "Epocryllian",
            "Rocryllian",
            "Zyryllian",
            "Sagyllian",
            "Epinyllian",
            "Katagyllian",
            "Ragyllian",
        ]
    )
    pitchSets.append([0, 2, 3, 5, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Gothyllian",
            "Lythyllian",
            "Bacryllian",
            "Aerygyllian",
            "Dathyllian",
            "Boptyllian",
            "Bagyllian",
            "Mathyllian",
            "Styptyllian",
            "Zolyllian",
        ]
    )
    pitchSets.append([0, 2, 4, 5, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Sydyllian",
            "Katogyllian",
            "Mixodyllian",
            "Aeradyllian",
            "Ryptyllian",
            "Loptyllian",
            "Kataphyllian",
            "Phradyllian",
            "Dagyllian",
            "Katyllian",
        ]
    )
    pitchSets.append([0, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Katoryllian",
            "Dodyllian",
            "Zogyllian",
            "Madyllian",
            "Dycryllian",
            "Aeogyllian",
            "Dydyllian",
            "Thogyllian",
            "Rygyllian",
            "Bathyllian",
        ]
    )
    pitchSets.append([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    names.append(
        [
            "Aerycratic",
            "Monatic",
            "Solatic",
            "Zylatic",
            "Mixolatic",
            "Soratic",
            "Godatic",
            "Eptatic",
            "Ionatic",
            "Aeolatic",
            "Thydatic",
        ]
    )
    pitchSets.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    names.append(["Chromatic"])