from __future__ import print_function
import math, sys
sys.path.append('../')
from Utility import Utility

import pprint

input = Utility.input
print = Utility.print
class JazzNote:
    useUnicodeChars = True
    carnaticWays = [
        "Mneumonic",
        "Notation",
        "Swara",
        "North Indian Sargam",
        "South Indian Sargam",
        "Carnatic",
    ] # Remove this var from Book eventually
    unicodeChars = {
        "Natural": "♮",
        "Flat": "♭",
        "Sharp": "♯",
        "Double Flat": "𝄫",
        "Double Sharp": "𝄪",
    }
    cache = {}
    _validWays = [
        "Classical",
        "Set",
        "All Flats Number",
        "Poem",
        "Carnatic",
        "Notation",
        "Mneumonic",
        "Gibberish",
        "Zodiac",
    ]
    numberOctaveDiatonicDistance = {
        "1": 0,
        "2": 2,
        "3": 4,
        "4": 5,
        "5": 7,
        "6": 9,
        "7": 11,
    }
    numberOctaveDiatonic = ["1", "2", "3", "4", "5", "6", "7"]
    numberOctaveFlats = [
        "1",
        "b2",
        "2",
        "b3",
        "3",
        "4",
        "b5",
        "5",
        "b6",
        "6",
        "b7",
        "7",
    ]
    noteNameNaturals = ["C", "D", "E", "F", "G", "A", "B"]
    noteNameFlats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    accidentalsChars = ["#", "b", "♯", "♭"]
    jazzNumberToNoteNameTable = {
        "C": {"1": "C", "2": "D", "3": "E", "4": "F", "5": "G", "6": "A", "7": "B"},
        "D": {"1": "D", "2": "E", "3": "F#", "4": "G", "5": "A", "6": "B", "7": "C#"},
        "E": {"1": "E", "2": "F#", "3": "G#", "4": "A", "5": "B", "6": "C#", "7": "D#"},
        "F": {"1": "F", "2": "G", "3": "A", "4": "Bb", "5": "C", "6": "D", "7": "E"},
        "G": {"1": "G", "2": "A", "3": "B", "4": "C", "5": "D", "6": "E", "7": "F#"},
        "A": {"1": "A", "2": "B", "3": "C#", "4": "D", "5": "E", "6": "F#", "7": "G#"},
        "B": {
            "1": "B",
            "2": "C#",
            "3": "D#",
            "4": "E",
            "5": "F#",
            "6": "G#",
            "7": "A#",
        },
    }
    jazzNoteToWayTable = {
        "Solfege": {
            "1": "Do",
            "2": "Re",
            "3": "Mi",
            "4": "Fa",
            "5": "Sol",
            "6": "La",
            "7": "Ti",
            "b2": "Ra",
            "b3": "Me",
            "b5": "Se",
            "b6": "Le",
            "b7": "Te",
            "#1": "De",
            "#2": "Ri",
            "#4": "Fi",
            "#5": "Si",
            "#6": "Li",
        },
        "North Indian Sargam": {
            "1": "Sadja",
            "2": "Shuddha Re",
            "3": "Shuddha Ga",
            "4": "Shuddha Ma",
            "5": "Panchama",
            "6": "Shuddha Dha",
            "7": "Shuddha Ni",
            "b2": "Komal Re",
            "b3": "Komal Ga",
            "b6": "Komal Dha",
            "b7": "Komal Ni",
            "#4": "Teevra ma",
        },
        "Notation": {
            "1": "S",
            "b2": "R1",
            "2": "R2",
            "#2": "R3",
            "bb3": "G1",
            "b3": "G2",
            "3": "G3",
            "4": "M1",
            "#4": "M2",
            "5": "P",
            "b6": "D1",
            "6": "D2",
            "#6": "D3",
            "bb7": "N1",
            "b7": "N2",
            "7": "N3",
        },
        "South Indian Sargam": {
            "1": "Sadja",
            "2": "Catussruti Ri",
            "3": "Antara Ga",
            "4": "Suddha Ma",
            "5": "Pancama",
            "6": "Catussruti Dha",
            "7": "Kakali Ni",
            "b2": "Suddha Ri",
            "b3": "Sadharana Ga",
            "b6": "Suddha Dha",
            "b7": "Kaisiki Ni",
            "#2": "Satsruti Ri",
            "#4": "Prati Ma",
            "#6": "Satsruti Dha",
            "bb3": "Suddha Ga",
            "bb7": "Suddha Ni",
        },
        "Swara": {
            "1": "Shadja",
            "b2": "Shuddha Rishabha",
            "2": "Chatushruti Rishabha",
            "bb3": "Shuddha Gandhara",
            "#2": "Shatshruti Rishabha",
            "b3": "Sadharana Gandhara",
            "3": "Antara Gandhara",
            "4": "Shuddha Madhyama",
            "#4": "Prati Madhyama",
            "5": "Pancham",
            "b6": "Shuddha Dhaivata",
            "6": "Chatushruti Dhaivata",
            "bb7": "Shuddha Nishada",
            "#6": "Shatshruti Dhaivata",
            "b7": "Kaisiki Nishada",
            "7": "Kakali Nishada",
        },
        "Mneumonic": {
            "1": "Sa",
            "2": "Ri",
            "3": "Gu",
            "4": "Ma",
            "5": "Pa",
            "6": "Di",
            "7": "Nu",
            "b2": "Ra",
            "b3": "Gi",
            "b6": "Da",
            "b7": "Ni",
            "#2": "Ru",
            "#4": "Mi",
            "#6": "Du",
            "bb3": "Ga",
            "bb7": "Na",
        },
    }
    numberToConsonant = [
        "b",
        "d",
        "f",
        "g",
        "j",
        "k",
        "l",
        "m",
        "n",
        "p",
        "r",
        "s",
        "t",
        "v",
        "w",
        "y",
        "z",
        "ch",
        "sh",
        "th",
        "h",
    ]
    numberToConsonant = [i.upper() for i in numberToConsonant]
    ##################### 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18   19   20  ( 21) -> ash, thorn



    # Roman Numerals ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯⅰⅱⅲⅳⅶⅷⅸⅹⅺⅻⅼⅽⅾⅿ

    def __init__(self, note):
        if type(note) == JazzNote:
            self.note = note.note
        elif JazzNote.isJazzNoteStr(JazzNote.convertUnicodeAccidentalsToSimpleStr(note)):
            self.note = JazzNote.convertUnicodeAccidentalsToSimpleStr(note)
        
        elif not JazzNote.isJazzNoteStr(note):
            raise ValueError(
                "Constructor expects a valid Jazz Note in style ##6, got instead: ",
                note,
                "of type",
                type(note),
            )
        elif not (type(note) == str):
            raise ValueError("expect a string in constructor", note, type(note))
        
        else:
            '''print('holy fuck {} {}\n JazzNote.isJazzNoteStr({}) == {}'.format(
                type(note),note,note,JazzNote.isJazzNoteStr(note)))'''
            self.note = note
        if not JazzNote.isJazzNoteStr(self.note):
            raise ValueError('shit')

    def __int__(self):
        return self.semitonesFromOne(octaveLimit=False)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        print("The hash of the JazzNote is:")
        return hash(str(self.note))

    def __str__(self, useUnicodeChars=True, colourOutput=False):
        if useUnicodeChars:
            noteStr = JazzNote.convertNoteToRealUnicodeStr(self.note)
        else:
            noteStr = str(self.note)
        return noteStr

    def __repr__(self):
        return "JazzNote('" + self.note + "')"

    @classmethod
    def makeAlphabetNoteUseSingleFlats(cls, note):
        if JazzNote.isAlphabetNoteStr(note):
            if note in JazzNote.noteNameFlats:
                return note
            else:
                return JazzNote.noteNameFlats[JazzNote.distanceFromC(note) % 12]
        else:
            raise TypeError("{} is not a valid alphabet note name str".format(note))


    def octaveUp(self):# -> JazzNote:
        acc = self.leaveAccidentals()
        deg = int(self.note.replace(acc,''))+7
        return JazzNote(acc+str(deg))

    def plainStr(self):
        # Not needed, just use the note property
        return JazzNote.convertUnicodeAccidentalsToSimpleStr(str(self))

    def getAngle(
        self, returnDegrees=False, goQuarterTurnAnticlockwise=False, humanFormat=False
    ):

        if returnDegrees == True:
            _angle = self.semitonesFromOne() * (360 / 12)
        else:
            _angle = self.semitonesFromOne() * (2 * math.pi / 12)
        if goQuarterTurnAnticlockwise == True:
            if returnDegrees == False:
                _angle -= math.pi / 2
            else:
                _angle -= 90

        if humanFormat == True:
            if returnDegrees == False:
                _angle = str(round(i / math.pi, 2)) + "π"
            elif returnDegrees == True:
                _angle = str(round(i, 2)) + "°"

        return _angle

    def getZodiac(self, adjustBySemitones=0):
        from Zodiac import Zodiac
        return Zodiac.semitoneToZodiac[
            (self.semitonesFromOne() + adjustBySemitones) % 12
        ]

    def getColour(self, adjustBySemitones=0, darkColours=None):
        if darkColours == True or Latex.blackPaper == False:
            return Colour.nameByDistanceDk[
                (self.semitonesFromOne() + adjustBySemitones) % 12
            ]
        elif darkColours == False or Latex.blackPaper == True:
            return Colour.nameByDistanceLt[
                (self.semitonesFromOne() + adjustBySemitones) % 12
            ]
        else:
            raise TypeError("need boolean")

    def makeResultColoured(self, result, adjustBySemitones=0):
        return (
            "\\textcolor{"
            + self.getColour(adjustBySemitones + Book.colourTranspose)
            + "}{"
            + result
            + "}"
        )

    def notesWithinNoteNamesAllowed(self, allowedNotes):  # zelda
        _goodNotes = []
        # forceFancyAccidentals = False
        # forceSimpleAccidentals = False
        '''if not type(allowedNotes) == Change:
            allowedNotes = Change(allowedNotes)'''

        for note in allowedNotes:
            if JazzNote.convertUnicodeAccidentalsToSimpleStr(
                str(note)
            ) == JazzNote.convertUnicodeAccidentalsToSimpleStr(str(self)):
                if not note in _goodNotes:
                    _goodNotes.append(self)
            elif JazzNote(note).semitonesFromOne(octaveLimit=0) == self.semitonesFromOne(
                octaveLimit=0
            ):
                if not note in _goodNotes:
                    _goodNotes.append(JazzNote(note))
        else:

            _semitonePosition = self.semitonesFromOne(octaveLimit=False)
            for note in allowedNotes:
                note = JazzNote(note)
                if note.semitonesFromOne() == _semitonePosition:
                    if note not in _goodNotes:
                        _goodNotes.append(note)

        assert all([type(n) == JazzNote for n in _goodNotes]), 'damnit'
        return _goodNotes

    def byWay(self, way):  # Work HERE
        # Check if it's a valid way
        if JazzNote.isValidWay(way):
            pass
        else:
            raise ValueError(way, "is not a valid way")

        if Key.isValid(way):  # Start for keys like Ab, B#
            return Key(way).onJazz(self).getASCII()

            """These are if the way is a note like, Ab, G###########, Fb"""


            '''wayRootNoAccidentals = JazzNote.genericIntervalFromNoteName(way)
            selfRootNoAccidentals = int(self.scaleDegree())
            while selfRootNoAccidentals > 7:  # Make the number fit into one octave
                selfRootNoAccidentals -= 7
            keyNoteName = JazzNote.jazzNumberToNoteNameTable[wayRootNoAccidentals][
                str(selfRootNoAccidentals)
            ]
            accidentals = 0
            accidentalsStr = ""
            for char in way:
                if char in ("#", "♯"):
                    accidentals += 1
                elif char in ("b", "♭"):
                    accidentals -= 1
            for char in self.note:
                if char in ("#", "♯"):
                    accidentals += 1
                elif char in ("b", "♭"):
                    accidentals -= 1
            for char in keyNoteName:
                if char in ("#", "♯"):
                    accidentals += 1
                elif char in ("b", "♭"):
                    accidentals -= 1
            if accidentals > 0:
                accidentalsStr += "#" * accidentals
            elif accidentals < 0:
                accidentalsStr += "b" * abs(accidentals)
            elif accidentals == 0:
                accidentalsStr = ""

            return JazzNote.convertNoteToRealUnicodeStr(
                JazzNote.genericIntervalFromNoteName(keyNoteName) + accidentalsStr
            )'''
        elif way == "Set":  # Set'''
            return str(self.semitonesFromOne(octaveLimit=False, disableNegatives=False))
        elif way == "Classical":
            return self.getRomanNumeral()
        elif way == "Jazz" or way == "Carnatic" or way == "All Flats Number":
            return JazzNote.convertNoteToRealUnicodeStr(self.note)
        elif way == "Gibberish":
            # return '!'*random.randint(1, 10)#Random length string
            return "11"
        elif way == "Zodiac":
            return self.getZodiac()
        elif way == "Poem":
            return self.getConsonant()
        # 		elif way == 'Chord Quality':
        # 			return self.getChordQuality()
        elif way in list(JazzNote.jazzNoteToWayTable.keys()):
            thisWay = JazzNote.jazzNoteToWayTable[way]

            if self.note in thisWay:
                return thisWay[self.note]
            else:
                octaveRangeOfWay = 1  # Fix here Hope this works
                for i in thisWay.keys():
                    if JazzNote(i).semitonesFromOne(octaveLimit=False) >= (
                        12 * octaveRangeOfWay
                    ):
                        octaveRangeOfWay += 1

                semitones = self.semitonesFromOne()
                # Constrain notesets to range of way
                semitones = JazzNote.limitSemitonesToNumberOfOctaves(
                    semitones, octaveLimit=octaveRangeOfWay, disableNegatives=True
                )
                enharmonicPossibilities = []
                for i in thisWay.keys():
                    if semitones == JazzNote(i).semitonesFromOne():
                        enharmonicPossibilities.append(i)
                if len(enharmonicPossibilities) == 1:
                    return thisWay[enharmonicPossibilities[0]]
                elif len(enharmonicPossibilities) > 1:
                    highestEnharmonicPossibility = enharmonicPossibilities[0]
                    lowestEnharmonicPossibility = enharmonicPossibilities[0]
                    for (
                        i
                    ) in (
                        enharmonicPossibilities
                    ):  # Here the way it gets lowest and highest doesn't quite work
                        if JazzNote(i).leaveAccidentals() == self.leaveAccidentals():
                            return thisWay[i]
                        if int(self.scaleDegree()) > int(
                            JazzNote(highestEnharmonicPossibility).scaleDegree()
                        ):  # if function higher
                            pass
                            # print('sum sheeeit', i)
                        if int(JazzNote(i).scaleDegree()) > int(
                            JazzNote(highestEnharmonicPossibility).scaleDegree()
                        ):
                            highestEnharmonicPossibility = i
                            # print('trigga', i)
                        if int(self.scaleDegree()) < int(
                            JazzNote(lowestEnharmonicPossibility).scaleDegree()
                        ):
                            pass
                            # print('sum otha shit',i)
                        if int(JazzNote(i).scaleDegree()) < int(
                            JazzNote(lowestEnharmonicPossibility).scaleDegree()
                        ):
                            # print('trigga', i)
                            lowestEnharmonicPossibility = i

                    # print (enharmonicPossibilities,'highestEnharmonicPossibility',highestEnharmonicPossibility,lowestEnharmonicPossibility)
                    if int(self.scaleDegree()) > int(
                        JazzNote(highestEnharmonicPossibility).scaleDegree()
                    ):
                        finalEnharmonic = highestEnharmonicPossibility
                    elif int(self.scaleDegree()) < int(
                        JazzNote(lowestEnharmonicPossibility).scaleDegree()
                    ):
                        finalEnharmonic = lowestEnharmonicPossibility
                    if self.semitonesFromOne(disableNegatives=False) < 0:
                        finalEnharmonic = highestEnharmonicPossibility

                    # print(finalEnharmonic)
                    return thisWay[finalEnharmonic]

                else:
                    raise ValueError("There was no result for the way")

                return enharmonicPossibilities
            # Put way in


        else:
            raise ValueError("way ", way, "was not a valid way")

        # print(selfRootNoAccidentals,wayRootNoAccidentals, keyNoteName,accidentalsStr, accidentals)

    def OldinKeyOfNumber(
        self, newRoot
    ):  # see notes if there are too many accidentals over 6 not working

        # print('self',self,'newRoot',newRoot)
        if type(newRoot) is JazzNote:
            newRoot = str(newRoot)
        elif JazzNote.isJazzNoteStr(newRoot):
            pass
        else:
            raise TypeError("newInKeyOfNumber expects JazzNote or valid str")
        noteSelfJazzNumber = self.scaleDegree()  #
        # print('newRoot', newRoot,'noteSelfJazzNumber', noteSelfJazzNumber,self)
        noteOriginalAccidentals = self.leaveAccidentals()
        midiIndex = self.semitonesDistanceFromRoot(
            noteSelfJazzNumber
        )  # Change to function
        for i in noteOriginalAccidentals:
            if i == "#":
                midiIndex += 1
            if i == "b":
                midiIndex -= 1

        newAccidentals = (
            midiIndex
            - self.semitonesDistanceFromRoot(newRoot)
            - JazzNote(newRoot).semitonesDistanceFromRoot("1")
        )  # subtracts pos of root

        # print('new number semi tones from root',JazzNote(newRoot).semitonesDistanceFromRoot('1'))
        # print(self.s-+ |/*--emiTonesUpFromRoot)
        # print('newAccidentals',newAccidentals)
        if newAccidentals > 6:  # maxes the new accidentals at 6 and reverses them
            newAccidentals = (12 - newAccidentals) * -1
        elif newAccidentals < -6:
            newAccidentals = (-12 - newAccidentals) * -1
        if newAccidentals > 0:  # newAccidentals becomes the string
            newAccidentals = "#" * newAccidentals
        elif newAccidentals < 0:
            newAccidentals = "b" * (-newAccidentals)
        elif newAccidentals == 0:
            newAccidentals = ""

        # print('newAccidentals',newAccidentals)

        print(self, "inKeyOfNumber", newRoot, newAccidentals, newRoot)
        return newAccidentals + newRoot

    def OldsemitonesUpFromRoot(self, rootNote="1", octaveLimit=True):

        # print('rootNote in semitonesDistanceFromRoot', type(rootNote))
        if JazzNote.isJazzNoteStr(rootNote):
            rootNote = JazzNote(rootNote)
        elif type(rootNote) is JazzNote:
            pass
        else:
            raise ValueError("semi tones up from root takes a jazzNote or jazzString")
        # rootNote is JazzNote type
        semitones = 0

        rootNote = str(rootNote)
        # rootNote is str
        selfNumber = self.scaleDegree()
        selfNumber = int(selfNumber)
        # print('rootNote is', rootNote,'selfNumber is',selfNumber)
        if JazzNote.numberOctaveFlats.index(str(((selfNumber - 1) % 7) + 1)) != 0:
            semitones += JazzNote.numberOctaveFlats.index(
                str(int(selfNumber - 1) % 7 + 1)
            )  # Here make it work above octave
        semitones += 12 * (math.floor(int(selfNumber - 1) / 7))
        for char in self.leaveAccidentals():
            if char == "b":
                semitones -= 1
            if char == "#":
                semitones += 1
        # new block of code

        # rootNote is str
        rootNumber = JazzNote(rootNote).scaleDegree()
        rootNumber = int(rootNumber)
        if JazzNote.numberOctaveFlats.index(str(((rootNumber - 1) % 8) + 1)) != 0:
            # notesets -= JazzNote.numberOctaveFlats.index(str(int(rootNumber-1) % 7+1)) #Here make it work above octave
            semitones -= JazzNote.numberOctaveFlats.index(str(int(rootNumber) % 7 + 1))
        semitones += 12 * (math.floor(int(rootNumber - 1) / 7))
        for char in JazzNote(rootNote).leaveAccidentals():
            if char == "b":
                semitones -= 1
            if char == "#":
                semitones += 1
        if rootNumber > selfNumber:
            semitones += 0
            print(
                "root is higher than comparison rootNumber",
                rootNumber,
                "selfNumber",
                selfNumber,
            )
            octavesAway = math.floor(rootNumber / 7) + 1  # finish
            # notesets += 12 * octavesAway

        return semitones

    def inTermsOfScaleDegree(
        self, newRoot, maxAccidentals=False
    ):  # see notes if there are too many accidentals over 6 not working
        # WORK here because
        newRoot = JazzNote.makeNoteOrStrIntoJazzNote(str(newRoot))
        newRoot = JazzNote(newRoot.scaleDegree())
        # print('self',self,'newRoot',newRoot)
        selfScaleDegree = self.scaleDegree()  #
        # print('newRoot', newRoot,'selfScaleDegree', selfScaleDegree,self)
        selfOriginalAccidentals = self.leaveAccidentals()
        midiIndex = self.semitonesTo(selfScaleDegree)
        for i in selfOriginalAccidentals:
            if i == "#":
                midiIndex += 1
            if i == "b":
                midiIndex -= 1
        newAccidentals = (
            midiIndex - self.semitonesTo(newRoot) - newRoot.semitonesTo(newRoot)
        )  # subtracts pos of root
        # print('new number semi tones from root',JazzNote(newRoot).semitonesDistanceFromRoot('1'))
        # print(self.s-+ |/*--emiTonesUpFromRoot)
        # print('newAccidentals',newAccidentals)
        if newAccidentals > 0:  # newAccidentals becomes the string
            newAccidentals = "#" * newAccidentals
        elif newAccidentals < 0:
            newAccidentals = "b" * (-newAccidentals)
        elif newAccidentals == 0:
            newAccidentals = ""
        # print('newAccidentals',newAccidentals)
        # print(self,'inKeyOfNumber',newRoot, newAccidentals,newRoot)
        # maxes the new accidentals at 6 and reverses them
        if maxAccidentals:
            if newAccidentals > maxAccidentals:
                newAccidentals = (12 - newAccidentals) * -1
            elif newAccidentals < -maxAccidentals:
                newAccidentals = (-12 - newAccidentals) * -1
        return JazzNote(newAccidentals + newRoot.note)

    def changeScaleDegreeBy(
        self, change, octaveLimit=1, allowDiminishingBelowRoot=False
    ):
        """If you had a JazzNote('b2') and change == 1, it becomes 'bbb3'.
        if change was -1 you would get '#1'
        if you had '1' and change == -2, octaveLimit=1, (and allowDiminishingBelowRoot == True)
        -> '###6'
        if you had '1' and change == -2, octaveLimit=2, (and allowDiminishingBelowRoot == True)
        -> '###13'
        if you had 'b7' and change == 2, octaveLimit=1,
        -> 'bbbb2'"""
        pass

    def scaleDegree(self, key=None):
        """If key is specified, it's returning the Alphabetic scale degree, i.e 'A' or 'D'."""
        _scaleDegree = ""
        if key == None:
            _note = self.note
        elif JazzNote.isAlphabetNoteStr(key):
            _note = self.byWay(key)
        else:
            raise TypeError(
                "was expecting nothing, meaning process the jazz note, or a key (alphabet), got instead",
                key,
            )
        for char in _note:
            if not char in JazzNote.accidentalsChars:
                _scaleDegree += char
        # input(_scaleDegree)
        return _scaleDegree

    def removeAccidentals(self):
        return [char for char in self.note if char.isnumeric()]

    def leaveAccidentals(self, key=None, useUnicodeAccidentals=False):  # Works
        _accidentals = ""
        if key == None:
            _note = self.note
        elif JazzNote.isAlphabetNoteStr(key):
            _note = self.byWay(key)
        else:
            raise TypeError(
                "was expecting nothing, meaning process the jazz note, or a key (alphabet), got instead",
                key,
            )
        for char in _note:
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                pass
            elif char in JazzNote.accidentalsChars:
                _accidentals += char
        if useUnicodeAccidentals:
            _accidentals.replace("#", "♯")
            _accidentals.replace("b", "♭")
        return _accidentals

    def semitonesFromOne(self, octaveLimit=1, disableNegatives=True):  # Works
        """octaveLimit can take false"""

        try:
            return JazzNote.cache['{}.semitonesFromOne({},{})'.format(
                self.__repr__(),octaveLimit,disableNegatives)]
        except KeyError:
            pass

        #print('this jazznote is',self)
        #input(self)
        noAccidentals = int(self.scaleDegree())
        octaves = 1
        # Make first octave value first
        firstOctaveNumber = noAccidentals
        selfAccidentalSteps = 0
        sharps, flats = (0,) * 2
        for char in self.leaveAccidentals():
            if char in ("b",JazzNote.unicodeChars['Flat']):
                selfAccidentalSteps -= 1
                flats += 1
            if char in ("#",JazzNote.unicodeChars['Sharp']):
                selfAccidentalSteps += 1
                sharps += 1
        # This makes it go to the first octave
        while firstOctaveNumber > 7:
            firstOctaveNumber -= 7
            octaves += 1
        selfAccidentalSteps += 12 * (octaves - 1)
        # Then add for note number semi tone value
        selfAccidentalSteps += JazzNote.numberOctaveFlats.index(str(firstOctaveNumber))
        # Then Add for octaves
        selfAccidentalSteps = JazzNote.limitSemitonesToNumberOfOctaves(
            selfAccidentalSteps, octaveLimit, disableNegatives
        )
        # print('inside semitonesFromOne for ',self,'firstOctaveNumber ',firstOctaveNumber,'octaves ',octaves,'selfAccidentalSteps',selfAccidentalSteps)
        JazzNote.cache['{}.semitonesFromOne({},{})'.format(
            self.__repr__(), octaveLimit, disableNegatives)] = selfAccidentalSteps
        return selfAccidentalSteps

    def semitonesTo(self, targetNote="1", octaveLimit=False):
        targetNote = JazzNote.makeNoteOrStrIntoJazzNote(targetNote)
        return JazzNote.limitSemitonesToNumberOfOctaves(
            targetNote.semitonesFromOne(octaveLimit=False, disableNegatives=False)
            - self.semitonesFromOne(octaveLimit=False, disableNegatives=False),
            octaveLimit=octaveLimit,
            disableNegatives=False,
        )

    def semitonesUpTo(
        self, targetNote="1", octaveLimit=1
    ):  # Works; If the targetnote is lower it just grabs self x octaves up
        if JazzNote.isJazzNoteStr(targetNote):
            targetNote = JazzNote(targetNote)
        elif type(targetNote) is JazzNote:
            pass
        else:
            raise TypeError()
        targetNoteSemitone = targetNote.semitonesFromOne(
            octaveLimit=False, disableNegatives=True
        )
        selfSemitone = self.semitonesFromOne(octaveLimit=False, disableNegatives=True)
        # print('stu2',selfSemitone,targetNoteSemitone)
        if targetNoteSemitone >= selfSemitone:
            pass  # Target is higher or even no prob
        else:
            while targetNoteSemitone < selfSemitone:
                targetNoteSemitone += 12
        distanceUp = targetNoteSemitone - selfSemitone
        distanceUp = JazzNote.limitSemitonesToNumberOfOctaves(
            distanceUp, octaveLimit=octaveLimit
        )
        return distanceUp

    def getConsonant(self):
        return JazzNote.numberToConsonant[self.semitonesFromOne(octaveLimit=False)]

    def getRomanNumeral(self, useUnicodeNumerals=False, returnCapital=True):
        number = int(self.scaleDegree())
        if not 0 < number < 4000:
            raise ValueError("Argument must be between 1 and 3999", number)
        ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
        nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
        result = ""
        for i in range(len(ints)):
            count = int(number / ints[i])
            result += nums[i] * count
            number -= ints[i] * count

        _scaleDegree = int(self.scaleDegree())
        if _scaleDegree <= 12 and useUnicodeNumerals == True:
            from Unicode import Unicode
            if returnCapital == True:
                result = Unicode.romanNumeralCapitals[_scaleDegree]
            elif returnCapital == False:
                result = Unicode.romanNumeralLowercase[_scaleDegree]
        elif not useUnicodeNumerals == True:
            if returnCapital == True:
                pass
            else:
                result = result.lower()
        # Add flats and sharps
        result = self.leaveAccidentals(useUnicodeAccidentals=True) + result
        # print(str(self)+self.leaveAccidentals()+'blablablabla')
        # input()
        return result

    @classmethod
    def numberOfAccidentalsToAccidentalsString(cls, accidentals):
        if type(accidentals) == int:
            pass
        else:
            raise TypeError(
                "accidentals was supposed to be int, it was",
                accidentals,
                " of type ",
                type(accidentals),
            )
        if accidentals > 0:
            return "#" * accidentals
        elif accidentals < 0:
            return "b" * abs(accidentals)
        elif accidentals == 0:
            return ""

    @classmethod
    def convertAlphabetToJazzNote(cls, key="C"):# -> JazzNote:
        if not JazzNote.isAlphabetNoteStr(key):
            raise TypeError("key expects valid Alphabet note:", type(key))
        raise TypeError("not done")

    @classmethod
    def makeFromSet(
        cls, semitonePosition: int, numberPart=None, octaveLimit=False
    ):# -> JazzNote:
        """Return a JazzNote which is in the numberkey of numberPart from a semitone position
        if semitonePosition == 9 and numberPart == 5:
            return JazzNote('##5')

        """

        if not numberPart:
            _noteName = ""
            _accidentals = 0
            _octavesUp = math.floor(semitonePosition / 12)
            _firstOctaveSemitonePosition = semitonePosition % 12
            for note in JazzNote.numberOctaveDiatonicDistance.keys():
                if (
                    JazzNote.numberOctaveDiatonicDistance[note]
                    == _firstOctaveSemitonePosition
                ):
                    _firstOctaveNumberPart = int(note)
                    break
                elif (
                    JazzNote.numberOctaveDiatonicDistance[note]
                    == _firstOctaveSemitonePosition + 1
                ):
                    _firstOctaveNumberPart = int(note)
                    _accidentals -= 1
            _noteName = _firstOctaveNumberPart
            if not octaveLimit:
                _noteName += _octavesUp * 7
            _noteName = JazzNote.numberOfAccidentalsToAccidentalsString(
                _accidentals
            ) + str(_noteName)
            return JazzNote(_noteName)

        if not type(numberPart) == JazzNote:
            numberPart = JazzNote(str(numberPart))
        numberPart = JazzNote(
            numberPart.scaleDegree()
        )  # numberPart is a JazzNote of the number
        _numberPartSemitonesUp = numberPart.semitonesFromOne()
        _accidentals = JazzNote.numberOfAccidentalsToAccidentalsString(
            semitonePosition - _numberPartSemitonesUp
        )
        # make a accidentals to accidentals
        return JazzNote(_accidentals + numberPart.scaleDegree())

    @classmethod
    def limitSemitonesToNumberOfOctaves(
        cls, semitones, octaveLimit=1, disableNegatives=True
    ):  # works
        """Works well, negatives re-modulus into that range..
        if notesets is -1 octaveLimit is 2 and disableNegatives is True
        you would get 23"""

        # print('inside limit octave function, notesets ',notesets,'octaveLimit ',octaveLimit,'disableNegatives ',disableNegatives)
        semitoneLimit = 12 * octaveLimit
        octavesInInput = math.floor(abs(semitones) / 12)
        if octaveLimit:
            if semitones > 0:
                while semitones >= (semitoneLimit):
                    semitones = semitones % (semitoneLimit)
            elif semitones < 0:
                while semitones <= -semitoneLimit:
                    semitones += 12 * octavesInInput
        if disableNegatives and semitones < 0:
            semitones = octaveLimit * 12 - (
                (abs(semitones) % 12) + (12 * octavesInInput)
            )
            while semitones < 0:
                semitones += 12
        return semitones

    def getAccidentalSum(self):
        return self.note.count(Key.sharpAscii) - self.note.count(Key.flatAscii)

    @classmethod
    def countAccidentalsInStr(
        cls,
        string,
        includeFlats=True,
        includeSharps=True,
        includeDoubleAccidentals=True,
    ):
        _accidentals = 0
        if type(string) == list:
            if not all(type(i) == str for i in string):
                raise TypeError("either provide a str or lst of strings")
            string = "".join(string)

        if includeFlats:
            for char in string:
                if char in ("b", "♭"):
                    _accidentals += 1
                if includeDoubleAccidentals:
                    if char == JazzNote.unicodeChars["Double Flat"]:
                        _accidentals += 2
        if includeSharps:
            for char in string:
                if char in ("#", "♯"):
                    _accidentals += 1
                if includeDoubleAccidentals:
                    if char == JazzNote.unicodeChars["Double Sharp"]:
                        _accidentals += 2
        return _accidentals

    @classmethod
    def makeNoteOrStrIntoJazzNote(cls, jazzNote):  # Checks and returns JazzNote
        if JazzNote.isJazzNoteStr(jazzNote):
            return JazzNote(jazzNote)
        elif type(jazzNote) is JazzNote:
            return jazzNote
        else:
            raise TypeError("invalid jazzNote or jazzNoteStr: ", jazzNote)

    @classmethod
    def turnListOfStrToListOfJazzNotes(cls, noteList):
        if not type(noteList) is list:
            raise TypeError(
                "turnListOfStrToListOfJazzNotes is supposed to get a list, you gave, ",
                noteList,
            )
        listOfJazzNotes = []
        for i in noteList:
            listOfJazzNotes.append(JazzNote.makeNoteOrStrIntoJazzNote(i))
        return listOfJazzNotes

    @classmethod
    def isValidWay(cls, way):
        # Check if it's a valid way

        if Key.isValid(way):
            pass
        elif way in JazzNote.jazzNoteToWayTable.keys():
            pass
        elif way in JazzNote._validWays:
            pass
        else:
            # raise ValueError ("way was not either a note name or a defined way, it was,",way)
            return False
        return True

    @classmethod
    def isJazzNoteStr(cls, jazzNote, numberLimit=False):
        try:
            return JazzNote.cache['isJazzNoteStr({},{})'.format(jazzNote,numberLimit)]
        except KeyError:
            pass
        cacheKey = 'isJazzNoteStr({},{})'.format(jazzNote,numberLimit)
        originalJazzNote = jazzNote
        if not (type(jazzNote) is str):
            JazzNote.cache[cacheKey] = False
            return False
            raise TypeError(jazzNote, " is not str.")
        sharps, flats = (False,) * 2
        numberPart = ""
        for char in jazzNote[::-1]:  # handy way to reverse
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                numberPart = char + numberPart
        if numberPart == "":
            # raise ValueError("There was none of these at the beginning: ['0','1','2','3','4','5','6','7','8','9'] therefore it is not a like bb7")
            JazzNote.cache[cacheKey] = False
            return False
        if numberPart[0] == "0":
            # raise ValueError("number part should not start with 0")
            JazzNote.cache[cacheKey] = False
            return False
        if "b" in jazzNote:
            flats = True
        if "#" in jazzNote:
            sharps = True
        if flats and sharps:
            raise ValueError("flats and sharps in jazzNote", originalJazzNote)
        jazzNote = jazzNote.replace(numberPart, "")
        for char in jazzNote:
            if sharps and not char == "#":
                if char not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    raise ValueError("was sharps, turned into, ", char)
            if flats and not char == "b":
                if not (char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                    raise ValueError("was flats, turned into,", char)
            if not (char.isnumeric() or char in ('#','b')):
                JazzNote.cache[cacheKey] = False
                return False
                #raise ValueError('this is not it dude {}'.format(jazzNote))
        if numberLimit:
            if int(numberPart) > numberLimit:
                raise ValueError("jazz number part is > numberLimit:", numberLimit)
        if sharps:
            if originalJazzNote[0] != "#":
                raise ValueError(
                    "accidentals are supposed to go before number. That is not so in ",
                    originalJazzNote,
                )
        if flats:
            if originalJazzNote[0] != "b":
                raise ValueError(
                    "accidentals are supposed to go before number. That is not so in ",
                    originalJazzNote,
                )


        JazzNote.cache[cacheKey] = True
        return True

    @classmethod
    def isAlphabetNoteStr(cls, noteName):  # This works
        if not (type(noteName) is str):
            # raise TypeError(noteName,' is not str.')
            return False
        if not (noteName[0] in JazzNote.noteNameNaturals):
            # raise ValueError('noteName[0] is not in noteNameNaturals, it is: ',noteName[0])
            return False
        sharps, flats = False, False  # (False,)*2
        if len(noteName) > 1:
            if noteName[1] in ("#", "♯"):
                sharps = True
            elif noteName[1] in ("b", "♭"):
                flats = True
            else:
                # raise ValueError(noteName[1]," is not 'b' or '#'")
                return False
            for char in noteName[1:]:
                if sharps:
                    if not char in ("#", "♯"):
                        raise ValueError("sharps turned into ", char)
                elif flats:
                    if not char in ("b", "♭"):
                        raise ValueError("flats turned into ", char)
        return True

    @classmethod
    def genericIntervalFromNoteName(cls, noteName):
        noteNameWithoutAccidentals = ""
        for char in noteName:
            if not char in JazzNote.accidentalsChars:
                noteNameWithoutAccidentals += char
        return noteNameWithoutAccidentals

    @classmethod
    def convertUnicodeAccidentalsToSimpleStr(cls, noteStr):
        try:
            return JazzNote.cache['convertUnicodeAccidentalsToSimpleStr({})'.format(noteStr.__repr__())]
        except KeyError:
            cacheKey = 'convertUnicodeAccidentalsToSimpleStr({})'.format(noteStr.__repr__())
        if type(noteStr) == str:
            JazzNote.cache[cacheKey] = noteStr.replace("♭", "b").replace("♯", "#").replace("𝄪", "##").replace("𝄫", "bb")
            return JazzNote.cache[cacheKey]
        elif type(noteStr) == JazzNote:
            JazzNote.cache[cacheKey] = JazzNote.convertUnicodeAccidentalsToSimpleStr(str(noteStr))
            #input(JazzNote.cache[cacheKey])
            return JazzNote.cache[cacheKey]
        elif type(noteStr) in (Change, list):
            _newNoteStrs = []
            for i in noteStr:
                _newNoteStrs.append(
                    i.replace("♭", "b")
                    .replace("♯", "#")
                    .replace("𝄪", "##")
                    .replace("𝄫", "bb")
                )

        JazzNote.cache[cacheKey] =  _newNoteStrs
        return JazzNote.cache[cacheKey]

    @classmethod
    def accidentalsToDistance(cls, accidentalsStr=""):
        _distance = 0
        for i in accidentalsStr:
            if i in ("#", "♯"):
                _distance += 1
            if i in ("b", "♭"):
                _distance -= 1
        return _distance

    @classmethod
    def distanceFromC(cls, alphabetNote):
        # THIS has been ported to the Key class
        if not JazzNote.isAlphabetNoteStr(alphabetNote):
            raise TypeError(
                "alphabetNote is to be supplied in form Ab, C##, not",
                alphabetNote,
                type(alphabetNote),
            )
        return JazzNote.noteNameFlats.index(
            alphabetNote[0]
        ) + JazzNote.accidentalsToDistance(alphabetNote[1:])

    @classmethod
    def convertNoteToRealUnicodeStr(
        cls, noteStr: str, useAnyStr=False, justFlatsAndSharps=False
    ) -> object:
        
        try:
            return JazzNote.cache['convertNoteToRealUnicodeStr({},{},{})'.format(
                noteStr, useAnyStr, justFlatsAndSharps 
            )]
        except KeyError:
            cacheKey = 'convertNoteToRealUnicodeStr({},{},{})'.format(
                noteStr, useAnyStr, justFlatsAndSharps 
            )
        
        _stringsToReplace = ("b", "#", "dim", "halfdim")
        _stringsReplacements = ("♭", "♯", "°", "⌀")
        if not type(noteStr) == str:
            raise TypeError("expects a str")
        if JazzNote.isJazzNoteStr(noteStr) or JazzNote.isAlphabetNoteStr(noteStr):
            pass
        elif useAnyStr:
            if justFlatsAndSharps:
                noteStr = noteStr.replace("b", "♭")
                noteStr = noteStr.replace("#", "♯")
                JazzNote.cache[cacheKey] = noteStr
                return JazzNote.cache[cacheKey]
            for i in _stringsToReplace:
                noteStr = noteStr.replace(
                    i, _stringsReplacements[_stringsToReplace.index(i)]
                )
            JazzNote.cache[cacheKey] = noteStr
            return JazzNote.cache[cacheKey]
        else:
            raise ValueError("convertNoteToRealUnicodeStr expects a valid jazznote or alphabet note, not,", noteStr)

        if JazzNote.useUnicodeChars:
            _doubleSharpChar = "\U0001D12A"
            _doubleFlatChar = "\U0001D12B"
            _flatChar = "♭"
            _sharpChar = "♯"
            _flats = noteStr.count("b")
            _sharps = noteStr.count("#")
            _doubleSharps = ""
            _doubleFlats = ""
            if not justFlatsAndSharps:
                _doubleSharps = _doubleSharpChar * math.floor(_sharps / 2)
                _doubleFlats = _doubleFlatChar * math.floor(_flats / 2)
                _singleSharps = _sharpChar * (_sharps % 2)
                _singleFlats = _flatChar * (_flats % 2)
            else:
                _singleFlats = _flatChar * _flats
                _singleSharps = _sharpChar * _sharps
            _accidentalStr = _doubleSharps + _doubleFlats + _singleSharps + _singleFlats
            _noteNameStr = noteStr.replace("b", "").replace("#", "")
            if JazzNote.isJazzNoteStr(noteStr):
                JazzNote.cache[cacheKey] = _accidentalStr + _noteNameStr
                return JazzNote.cache[cacheKey]
            elif JazzNote.isAlphabetNoteStr(noteStr):
                JazzNote.cache[cacheKey] = _noteNameStr + _accidentalStr
                return JazzNote.cache[cacheKey]
        else:
            JazzNote.cache[cacheKey] = noteStr
            return noteStr


from Key import Key