from __future__ import annotations, print_function
from collections.abc import Sequence
import numpy as np
import math,sys
'''sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../"))'''
#from JazzNote import JazzNote
from JazzNote import JazzNote
from Colour import Colour
from Unicode import Unicode
from Key import Key
from Utility import Utility
input = Utility.input
print = Utility.print
import warnings

class Change(Sequence):
    useUnicodeChars = True
    rootColourKey = 'C'
    cache = {}
    validVoicingTypes = ('Thirds','Scale')
    allowedNoteNamesAllFlats = [
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
    allowedNoteNamesSimpleJazz = [
        "1",
        "b2",
        "2",
        "b3",
        "3",
        "4",
        "#4",
        "b5",
        "5",
        "#5",
        "b6",
        "6",
        "b7",
        "7",
    ]  # Jazz numbers
    allowedNoteNamesJazz = [
        "1",
        "b2",
        "2",
        "b3",
        "3",
        "4",
        "#4",
        "b5",
        "5",
        "#5",
        "b6",
        "6",
        "b7",
        "7",
        "#2",
        "#6",
    ]  # Include #6 and #2
    allowedNoteNamesCarnatic = allowedNoteNamesJazz + ["bb3", "#2", "#6", "bb7"]
    allowedNoteNamesCarnatic.remove("b5")
    allowedNoteNamesCarnatic.remove("#5")
    allowedNoteNamesCarnatic = list(set(allowedNoteNamesCarnatic))
    allowedNoteNamesSolfege = allowedNoteNamesJazz + ["#1", "#2", "#6"]
    allowedNoteNamesSuperset = list(
        set(allowedNoteNamesCarnatic + allowedNoteNamesJazz)
    )
    allowedNoteNamesFiveAccidentals = list(
        set(
            allowedNoteNamesJazz
            + allowedNoteNamesCarnatic
            + allowedNoteNamesSolfege
            + [
                "##2",
                "###2",
                "####2",
                "bb3",
                "bbb3",
                "bbbb3",
                "#3",
                "##3",
                "###3",
                "####3",
                "b4",
                "bb4",
                "bbb4",
                "bbbb4",
                "##4",
                "###4",
                "####4",
                "b5",
                "bb5",
                "bbb5",
                "bbbb5",
                "##5",
                "###5",
                "####5",
                "b6",
                "bb6",
                "bbb6",
                "bbbb6",
                "#6",
                "##6",
                "##6",
                "###6",
                "##7",
                "###7",
                "####7",
                "b7",
                "bb7",
                "bbb7",
                "bbbb7",
                "bbbbb7",
            ]
        )
    )
    # allowedNoteNamesWeird = [note for note in allowedNoteNamesFiveAccidentals if note not in cls.allowedNoteNamesSimpleJazz]
    allowedNoteNamesWeird = []
    for note in allowedNoteNamesFiveAccidentals:
        if note not in allowedNoteNamesSimpleJazz:
            allowedNoteNamesWeird.append(note)
    validEnharmonicAlphabetNames = [
        ["B#", "C", "Dbb"],
        ["B##", "C#", "Db"],
        ["C##", "D", "Ebb"],
        ["D#", "Eb", "Fbb"],
        ["D##", "E", "Fb"],
        ["E#", "F", "Gbb"],
        ["E##", "F#", "Gb"],
        ["F##", "G", "Abb"],
        ["G#", "Ab"],
        ["G##", "A", "Bbb"],
        ["A#", "Bb", "Cbb"],
        ["A##", "B", "Cb"],
    ]

    validWays = np.array(
        [   "Unique Change Number",
            "Enantiomorph",
            "Change Number",
            "Area",
            "Colour",
            "RNA Codon",
            "DNA Codon",
            "Names",
            "Raga",
            "Word",
            "Changed Note Page",
            "Changed Note Hexagram",
            "Changed Note Word",
            "Changed Note Info",
            "Add Note",
            "Remove Note",
            "Ring Number",
            "Bitmap",
            "Forte Number",
            "Solfege",
            "Carnatic",
            "Mneumonic",
            "Spectra",
            "Notation",
            "Prime",
            "Inverse",
            "Tritone Sub",
            "Tritone Sub Page",
            "Chord Page",
            "Reverse",
            "Mode Semitones",
            "Mode Change Number",
            "Mode Hexagram",
            "Mode Jazz",
            "Mode Name",
            "Mode Quality",
            "Mode Primeness",
            "Mode Word",
            "Chord Quality",
            "Scale Name",
            "Classical",
            "Chord",
            "Third Chord 9ths",
            "Fourth Chord 7ths",
            "Fourth Chord 9ths",
            "Imperfections",
            "Braille",
            "Tetragram",
            "Trigram Symbol",
            "Hexagram",
            "Hexagram Name",
            "Hexagram Number",
            "Hexagram Symbol",
            "Hexagram Symbol Name",
            "Hexagram Subpage",
            "Hexagram Story",
            "Jazz",
            "Step",
            "Info",
            "Info Condensed",
            "Interval Vector",
            "Binomial",
            "Rhythm",
            "Poem",
            "Random Poem",
            "Efficient",
        ]
    )  # ''
    validWays = np.concatenate(
        [validWays, ["Distinct Chord " + str(i) for i in range(1, 10)]]
    )
    validWays = np.concatenate(
        [validWays, ["Distinct Chord Change Number " + str(i) for i in range(1, 10)]]
    )
    validWays = np.concatenate(
        [
            validWays,
            ["Distinct Chord Normalised Change Number " + str(i) for i in range(1, 10)],
        ]
    )
    validWays = np.concatenate(
        [validWays, ["Distinct Chord Word " + str(i) for i in range(1, 10)]]
    )

    condensedInfoWays = {
        "Unique Chapter Change Number": '',
        "Smallest Interval": "🐭",
        "Greatest Interval": "🐘",
        "Variation": "🐡",
        "Imperfections": "🐍",
        "Cohemitonia": "🐞",
        "Hemitonia": "🐜",
        "Contains Self": "🐙",
        "Has Evenness": "🐌",
        "Forte Number": "⨍",
        "Has Myhill": "🐫",
        "Is Deep": "🐳",
        "Has Coherence": "🕊",
        "Interval Vector": "🐰",
        "Binomial": "",
    }
    infoWaySymbols = {
        "Unique Chapter Change Number": '🙉',
        "Mela Number": "🎪",
        "Zodiac": "",
        "Smallest Interval": "\hfill🐭",
        "Greatest Interval": "🐘",
        "Variation": "🐡",
        "Imperfections": "🐍",
        "Cohemitonia": "🐞",
        "Hemitonia": "🐜",
        "Is Palindrome": "🐛",
        "Is Achiral": u"\U0001F980", #Crab
        "Contains Self": "🐙",
        "Has Evenness": "🐌",
        "Is Prime": "🙉",
        "Forte Number": "⨍",
        "Primeness": "🐒",
        "Has Myhill": "🐫",
        "Is Deep": "🐳",
        "Has Coherence": "🕊",
        "Interval Vector": "\\hfill🐰",
        "Alpha Accidentals": "♮",
        "Heliotonia": "🎹",
        "Area": "🐕",
        "Moment": "\\hfill",
        "Binomial": "",
    }
    infoWaysToOmit = ["Mela Number", "Binomial"]
    # Alternate Char ️ 🐌
    # ∫∱⨏⨍⨏🦀
    binaryWays = [
        "Has Myhill",
        "Is Palindrome",
        "Mela Number",
        "Is Deep",
        "Has Coherence",
        "Has Evenness",
        "Is Achiral",
        "Is Prime",
    ]
    # Animals🦔🐡 Ⓧ 🐍 🐠 🐊 🌵 🐉 🐓 🐇 🐒 🙈🙉🙊🐡 🦔🐑 🐐🐊'🐒 🐙 🐚🐚'🐅 🐘 🐁 🐀'🐜 \\🐛 🐜 🐞 🐟 🐠 🐡 🐑 ✌⛰🦁🐦  🐐 🐯 🐚 🐳 🐊 🐙 🐜 🐘  🕊 🐰 🌲 🐕 🐒 🐳 🦀 🐋 🦇 🐍 🐌 🐢 🐊 🐕

    # These don't work yet 🦕 🦖 🦗 🦞
    """Plants ⸙ 🌰 🌱 🌽 🌾 🌿 🍀 🍁 🍂 🍃 🌵 🎄 🎋  🌳 🌴 💮 🌸 🌷 🌹 🌺 🌻 🌼 🥀 🎕 ⚘ 🏵 🏶 🥧
"""

    validWays = np.concatenate([validWays, list(infoWaySymbols.keys())])
    # validWays.extend(infoWaySymbols.keys())
    straightenedWays = ["Solfege", "Jazz", "Classical"]

    # Trichords
    
    def __hash__(self):
        return hash(str(self.notes))
    
    
    def __init__(
        self, notes: [str] = None, ringNumber: int = None, noteset: [int] = None
    ):

        self.notes = []
        self.num = 0
        if type(notes) in (list, np.array, np.ndarray, Change):
            typeOfNotes = ""
            # Check that all notes are JazzNote type or all are JazzNoteStr
            if type(notes) in (str, JazzNote):
                notes = [notes]
            for note in notes:
                self.notes.append(JazzNote(note))
                '''if type(note) == JazzNote:

                    self.notes.append(JazzNote.convertUnicodeAccidentalsToSimpleStr(note))
                    if typeOfNotes == "JazzNoteStr":
                        raise TypeError(
                            "Started out with JazzNote types, then it became JazzNoteStr",
                            notes,
                        )
                    typeOfNotes = "JazzNote"
                elif JazzNote.isJazzNoteStr(note):
                    #self.notes.append(JazzNote.convertUnicodeAccidentalsToSimpleStr(note))
                    self.notes.append(JazzNote.convertUnicodeAccidentalsToSimpleStr(note))
                    if typeOfNotes == "JazzNote":
                        raise TypeError(
                            "Started out with JazzNoteStr types, then it became JazzNote",
                            notes,
                        )
                    typeOfNotes = "JazzNoteStr"'''
            # input(self.notes)
            self.notes = np.array(self.notes)
        elif isinstance(notes, JazzNote):
            self.notes = np.array([notes])
        elif ringNumber != None:
            self.notes = np.array(Change.makeFromRingNumber(ringNumber=ringNumber).notes)
        elif noteset != None:
            self.notes = np.array(Change.makeFromSet(notes=noteset).notes)
        else:
            raise ValueError(
                "you did not supply notes or ring number or set. notes == {} type {}".format(
                    notes, type(notes)
                )
            )

        #input(self,notes,type(notes),type(notes[0]))
        assert all([type(n) is JazzNote for n in self.notes]), [type(n) for n in self.notes]
        super().__init__()

    def __repr__(self):
        # print('inside Change.__repr__', self.notes)
        _reprStr = "Change(["
        for i in self.notes:
            _reprStr += "'" + str(i) + "'"
            if i != self.notes[-1]:
                _reprStr += ","
        _reprStr += "])"
        return _reprStr

    def __str__(self):
        # print('inside Change.__str__', self.notes)
        _strOutput = ""
        for i in self.notes:
            if Change.useUnicodeChars:
                _strOutput += JazzNote.convertNoteToRealUnicodeStr(str(i),useAnyStr=True)
            else:
                _strOutput += i
            if i != self.notes[-1]:
                _strOutput += " "
        return _strOutput

    @classmethod
    def C(cls, n, k):
        """computes nCk, the number of combinations n choose k"""

        result = 1
        for i in range(n):
            result *= i + 1
        for i in range(k):
            result /= i + 1
        for i in range(n - k):
            result /= i + 1
        return result

    @classmethod
    def cgen(cls, i, n, k):
        """
        returns the i-th combination of k numbers chosen from 1,2,...,n
        """
        C = cls.C
        c = []
        r = i + 0
        j = 0
        for s in range(1, k + 1):
            cs = j + 1
            while r - C(n - cs, k - s) > 0:
                r -= C(n - cs, k - s)
                cs += 1
            c.append(cs)
            j = cs
        return c

    def getUniquePage(self,chapterNumber=False):

        _uniquePage = None
        if self != Change([]):
            for m in range(len(self)):
                '''if Project.makingFinalCopies and not Book.makePrimes:
                    raise ValueError(
                        "You are attempting to make a final copy, but you have Book.makePrimes set to False"
                    )'''

                from Book import Book
                try:
                    Change.theBook.sequencePrimes[0]
                except Exception as e:
                    print('Drawing up another Book because ',e)
                    __makePrimesOld = Book.makePrimes
                    Book.makePrimes = 1
                    Change.theBook = Book()
                    Book.makePrimes = __makePrimesOld

                for p, prime in enumerate(Change.theBook.sequencePrimes):
                    if (
                            self.mode(m).getNormalForm().getSemitones()
                            == prime.getSemitones()
                    ):
                        _uniquePage = p
                        break
                if _uniquePage != None:
                    break
        else:
            _uniquePage = "0"
        if chapterNumber:
            _str = self.byWays("Unique Chapter Change Number") + _uniquePage
        else:
            _str = Unicode.chars["Unique Change Number"] + str(_uniquePage)
        return _str

    def getOctaveLimited(self):
        change = self
        for n in range(len(self)):
            acc = change.notes[n].leaveAccidentals()
            deg = int(change.notes[n].note.replace(acc,''))
            while deg > 7:
                deg -= 7
            change.notes[n] = JazzNote(acc + str(deg))
        return change


    def getVoicing(self,voicingType):
        _voicing = self
        if voicingType in Change.validVoicingTypes:
            pass
        else:
            raise TypeError('{} not in Change.voicingTypes {}'.format(voicingType,Change.voicingTypes))
        if voicingType == 'Scale':
            return self
        elif voicingType == 'Thirds':
            if True or len(self) == 12: # Odd
                for n in range(len(self))[1::2]:
                    _voicing.notes[n] = _voicing.notes[n].octaveUp()
            _voicing = _voicing.sortBySemitonePosition()
        else:
            raise ValueError('Have not implemented {} in Change.getVoicing()')
        return _voicing

    def hasScaleName(self):

        return (
            True
            if len(
                self.getScaleNames(
                    defaultWay=False,
                    relateToMainScales=False,
                    rebindRootToNextNoteIfNoOne=False,
                )
            )
            > 0
            else False
        )

    def plainStr(self):
        return [n for n in self.notes]

    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):

        # input()
        num = self.num
        # if self.num < len(self.notes)-1:
        if self.num < len(self.notes):
            self.num += 1
            return self.notes[num]
        else:
            raise StopIteration

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, i):
        return self.notes[i]

    def __eq__(self, value):
        if isinstance(value, Change):
            return np.array_equal(self.notes, value.notes)
        else:
            return False  # raise TypeError('value {} aint a change, but a {}'.format(value, type(value)))


            
    
    def otherMakeChange(self, notesToCheck):
        if type(notesToCheck) == str and JazzNote.isJazzNoteStr(notesToCheck):
            notesToCheck = [JazzNote(notesToCheck)]
        elif type(notesToCheck) == JazzNote:
            notesToCheck = [notesToCheck]
        elif type(notesToCheck) == Change:
            notesToCheck = notesToCheck.notes
        elif type(notesToCheck) == list:
            for i, n in enumerate(notesToCheck):
                if type(n) == JazzNote:
                    pass
                elif type(n) == str and JazzNote.isJazzNoteStr(note):
                    notesToCheck[i] = JazzNote(n)
                else:
                    raise TypeError(
                        "expecting a JazzNote or jazzNoteStr, got", n, type(n)
                    )

    def withAddedNotes(self, notesToAdd, sortAscending=True):
        """If sortAscending == False it will append the added notes to the end"""
        # print('notesToAdd',notesToAdd,type(notesToAdd))

        notesToAdd = Change(notesToAdd)
        _newChange = Change(np.concatenate([self.notes, notesToAdd.notes]))
        if sortAscending:
            _newChange = _newChange.removeDuplicateNotes().sortBySemitonePosition()
        return _newChange

    def withoutNotes(self, *notesToRemove, byAnotherName=True, octaveLimit=1):
        _newChange = self
        if len(notesToRemove) == 0:
            return self
        for noteToRemove in notesToRemove:
            if type(noteToRemove) == Change:
                for note in noteToRemove.notes:
                    _newChange = _newChange.withoutNote(note)
            elif type(noteToRemove) == list:
                for note in noteToRemove:
                    _newChange = _newChange.withoutNote(note)
            elif type(noteToRemove) in (str, JazzNote):
                if type(noteToRemove) == str and JazzNote(noteToRemove):
                    pass
                _newChange = _newChange.withoutNote(noteToRemove)
            else:
                raise TypeError(
                    "You're supposed to provide either notes or notes, not",
                    type(notesToRemove[noteToRemove]),
                    notesToRemove[noteToRemove],
                )
        return _newChange

    def withoutNote(self, noteToRemove, byAnotherName=True, octaveLimit=1):

        if JazzNote.isJazzNoteStr(noteToRemove):
            noteToRemove = JazzNote(noteToRemove)
        elif type(noteToRemove) == JazzNote:
            pass
        else:
            raise TypeError(
                "withoutNote expects JazzNote etc, not, ",
                type(noteToRemove),
                noteToRemove,
            )
        _newNotes = []
        for note in self.notes:
            if byAnotherName:
                if not note.semitonesFromOne(
                    octaveLimit=octaveLimit
                ) == noteToRemove.semitonesFromOne(octaveLimit=octaveLimit):
                    _newNotes.append(note)
            else:
                if not str(note) == str(noteToRemove):
                    _newNotes.append(note)
        return Change(_newNotes)

    def removeDuplicateNotes(self, byAnotherName=True, octaveLimit=False):
        """make it look through all notes to find dupes then delete dupes in the order they appear"""
        # The first note will obviously not be a duplioate
        if len(self) in (0, 1):
            return self
        _notesWithoutDupes = [self.notes[0]]
        for note in self.notes[1:]:
            if byAnotherName:
                # If that note by any name is the same distance from the 1
                if note.semitonesFromOne(octaveLimit=octaveLimit) in [
                    n.semitonesFromOne(octaveLimit=octaveLimit)
                    for n in _notesWithoutDupes
                ]:
                    pass
                else:
                    _notesWithoutDupes.append(note)

        return Change(_notesWithoutDupes)

    def OLDremoveDuplicateNotes(self, byAnotherName=True, octaveLimit=False):
        """make it look through all notes to find dupes then delete dupes in the order they appear"""
        # _currentNote = self.notes[0]
        _notesWithoutDupes = [self.notes[0]]
        for currentNote in self.notes:
            for note in range(len(self.notes)):
                if not byAnotherName:
                    if str(self.notes[note]) == str(currentNote):  # It is a duplicate
                        pass
                    else:
                        # elif not self.notes[note] in _notesWithoutDupes: #It is not duplicate
                        _notesWithoutDupes.append(self.notes[note])
                elif byAnotherName:
                    _st = currentNote.semitonesFromOne(octaveLimit=octaveLimit)
                    if _st == self.notes[note].semitonesFromOne(
                        octaveLimit=octaveLimit
                    ) or _st in [
                        n.semitonesFromOne(octaveLimit=octaveLimit)
                        for n in _notesWithoutDupes
                    ]:
                        pass
                    else:
                        _notesWithoutDupes.append(self.notes[note])
                    # _currentNote = self.notes[note]
        return Change(_notesWithoutDupes)

    def containsNotes(self, *args, byAnotherName=True, anyOfTheNotes=False):
        notesToFind = list(args)
        # Checks to see that the note is a valid jassNoteStr or JazzNote
        for i in range(len(notesToFind)):
            if JazzNote.isJazzNoteStr(notesToFind[i]):
                notesToFind[i] = JazzNote(notesToFind[i])
            elif type(i) == JazzNote:
                pass
            else:
                raise ValueError(
                    "containsNotes expects JazzNote str or JazzNote, not",
                    i,
                    "of type",
                    type(i),
                )
        # Made the notes a JazzNotes that are valid
        _foundNotes = 0
        # If byAnotherName is True then we are looking for the notes chromatically
        if byAnotherName == True:
            for i in self.notes:
                for note in notesToFind:
                    #print(i,type(i),note,type(note))
                    if JazzNote(i).semitonesFromOne(octaveLimit=1) == note.semitonesFromOne(
                        octaveLimit=1
                    ):
                        _foundNotes += 1
        if not byAnotherName:
            for i in self.notes:
                for note in notesToFind:
                    if str(i) == str(note):
                        _foundNotes += 1
        if anyOfTheNotes:
            if _foundNotes >= 1:
                return True
        elif _foundNotes == len(notesToFind):
            return True
        else:
            return False

    def getHomeKeys(self, returnAntiHomeKeys=False):
        _efficientKeys = self.getEfficientKeys(
            maxAccidentals=99, returnFlattenedList=True, reorderByMaxAccidentals=True
        )
        _homeKeys = []
        _antiHomeKeys = []
        _minAccidentals = JazzNote.countAccidentalsInStr(
            _efficientKeys[list(_efficientKeys.keys())[0]]
        )
        _maxAccidentals = JazzNote.countAccidentalsInStr(
            _efficientKeys[list(_efficientKeys.keys())[-1]]
        )
        for i in _efficientKeys.items():
            # print('i ',i,i[0],i[1],)
            if JazzNote.countAccidentalsInStr(i[1]) == _minAccidentals:
                _homeKeys.append(i[0])
            if JazzNote.countAccidentalsInStr(i[1]) == _maxAccidentals:
                _antiHomeKeys.append(i[0])
        # print(_minAccidentals,_maxAccidentals)
        # input(str('within getHomeKeys() '+'\n'+str(_efficientKeys))+'\n'+str(_antiHomeKeys)+'\n'+str(_homeKeys))
        if not returnAntiHomeKeys:
            return _homeKeys
        else:
            return _antiHomeKeys

    def getCodon(self, geneType="RNA", colourResult=False,
                 useTextStyledByWay = False):
        _results = []

        if not geneType in ("RNA", "DNA", "Both"):
            raise ValueError("It needs to be either RNA or DNA, or Both." + rnaOrdna)
        _halfScales = self.divideScaleBy(
            returnChromatically=False, denominator=2, normaliseToSlice=True
        )
        _halfScales = [
            i.getBitMap(
                trueSymbol="1", falseSymbol="0", colourResult=False, notePossibilities=6
            )
            for i in _halfScales
        ]

        try:
            Codon
        except NameError:
            from Codon import Codon

        for i, halfScale in enumerate(_halfScales):
            if geneType == "RNA":
                _results.append(Codon.RNAcodonByHalfScaleInStrBitmap[halfScale])
            elif geneType == "DNA":
                _results.append(Codon.DNAcodonByHalfScaleInStrBitmap[halfScale])
            elif geneType == "Both":
                _results.append(Codon.DNAcodonByHalfScaleInStrBitmap[halfScale])
                if _results[-1].replace("T", "U ") != _results[-1]:
                    _results[-1] += (
                        "/" + Codon.RNAcodonByHalfScaleInStrBitmap[halfScale]
                    )
            if colourResult == True:
                _results[-1] = Latex.makeDataColoured(
                    _results[-1],
                    (6 * i + Book.colourTranspose) % len(Colour.nameByDistanceLt),
                )
        if useTextStyledByWay:
            return [Latex.makeTextStyledByWay(r, "Codon") for r in _results]
        return _results

        # print(_halfScales,self, self.getScaleNames()[0],_results)
        # input('those are halfScales in getCodon')

    def getZodiac(self, spaceOutBySemitone=True, colourResult=True):
        _zodiac = [i.getZodiac() for i in self.notes]
        if spaceOutBySemitone == True:
            _str = ""
            if Latex.on == True:
                _spaceStr = "\\hspace*{"
            else:
                _spaceStr = " "
            _spaces = self.getSemitoneSteps()
            _spaces = [i - 1 for i in _spaces]
            if (
                colourResult == True
                and Latex.on == True
                and Latex.makeTextColoured == True
            ):
                _zodiac = self.returnColouredLatex(
                    _zodiac, "Zodiac", adjustBySemitones=Book.colourTranspose
                )
            for n in range(len(self.notes)):
                _str += _zodiac[n]
                if Latex.on == True:
                    _str += _spaceStr + str(_spaces[n])
                    _str += "ex}"
                else:
                    _str += _spaceStr * _spaces[n]
            return _str
        else:
            return _zodiac

    def getRandomPoem(self):
        from Syllabic import Syllabic
        # https: // pypi.org / project / random - word /
        _consonants = [note.getConsonant() for note in self.notes]
        _words = []

        for consonant in _consonants:
            _word = " "
            while _word[0] != consonant.lower():
                # TODO add part of speech
                _word = Syllabic.getRandomEnglishWord(consonant)
                if " " in _word:
                    _word = _word.split(" ")[0]
                if "-" in _word:
                    _word = _word.split("-")[0]

            _words.append(_word)
        return _words

    @classmethod
    def makeFromRingNumber(cls, ringNumber: int, returnSet=False):
        if not 0 <= ringNumber <= 4095:
            raise ValueError(
                "ringNumber expects an int between 0 and 4096. You provided {} {}".format(
                    ringNumber, type(ringNumber)
                )
            )
        ringNumber = bin(ringNumber)[2:]
        while len(ringNumber) < 12:
            ringNumber = "0" + ringNumber
        noteset = []
        for b, bit in enumerate(ringNumber):
            if bit == "1":
                noteset.append(11 - b)
        noteset.sort()
        if returnSet:
            return noteset
        else:
            return Change.makeFromSet(noteset)

    @classmethod
    def makeFromSet(cls, notes, straighten=False) -> Change:
        noteList = []


        if len(notes) == 0:
            return Change([])
        for note in notes:
           
            noteList.append(JazzNote.makeFromSet(note))


        if straighten:

            return Change(noteList).straightenDegrees()
        elif not straighten:

            return Change(noteList)

    @classmethod
    def makeFromChangeNumber(
        cls, changeNumber: int, chapterNumber=None, rootIsChangeOne=True
    ) -> Change:

        if rootIsChangeOne == False:
            raise ValueError(
                "Converting this to all == True so check the surronding code for change numbers"
            )
        # TODO: Check for using chapterNumber != None

        print('top of makeFromChangeNumber')
        assert type(changeNumber) == int, 'this needs to be int'
        C = cls.C
        cgen = cls.cgen
        if changeNumber <= -1:
            if chapterNumber == None:
                # print('old function negative',Change(Change.makeFromChangeNumber(-changeNumber)).getChangeNumber(returnChapterPage=True))
                return Change.makeFromChangeNumber(
                    -changeNumber, rootIsChangeOne=rootIsChangeOne
                ).withoutNote("1")
            elif type(chapterNumber) == int:
                # If the changeNumber is within that chapter's range
                if abs(changeNumber) <= C(chapterNumber + 1, 11):
                    pass
                else:
                    raise ValueError(
                        "changeNumber is outside of that (negative) chapter's range:,",
                        C(chapterNumber + 1, 11),
                    )
                # The chapter is actually going to be the next one because we are negative
                return Change.makeFromChangeNumber(
                    -changeNumber,
                    chapterNumber + 1,
                ).withoutNote("1")
            else:
                raise TypeError(
                    "chapterNumber is supposed to be an integer, not",
                    type(chapterNumber),
                )

        _pageNumber = changeNumber
        if rootIsChangeOne:
            if _pageNumber >= 0:
                _pageNumber -= 1
            elif _pageNumber < 0:
                _pageNumber += 1
        # If we're recieving the book subChange number
        # Chapter number is one less than it actually is
        _chapter = 0
        _chapterStart = 0
        _chapterNumber = chapterNumber
        # print('in while loop')
        if not chapterNumber is None:
            if type(chapterNumber) != int:
                raise TypeError(
                    "chapterNumber is to be supplied as integer, not",
                    type(chapterNumber),
                )

        while _chapterNumber is None:

            # print('.',end='')
            _chapterStart += C(11, _chapter)
            _chapter += 1
            if _chapterStart + C(11, _chapter) > _pageNumber:
                _chapterNumber = _chapter
                _pageNumber += 1
                _pageNumber -= _chapterStart

        if _chapterNumber == None:
            raise ValueError("chapter not found for", _pageNumber)
        # We know the chapter number and chapter subChange number
        # TODO: This was the thing that I added
        # print(_chapterNumber,'chapterNumber')
        _st = cgen(_pageNumber, 11, _chapterNumber)
        if chapterNumber == None and _pageNumber == 0:
            _st = []
        _st = [0] + _st
        # return _st
        # print('old function', Change.makeFromSet(_st, straighten=False).getChangeNumber(returnChapterPage=True))

        print('made change', Change.makeFromSet(_st, straighten=False,),'returning')
        print('''print('made change', Change.makeFromSet(_st, straighten=False,),'returning')''')
        result = Change.makeFromSet(_st, straighten=False)
        print('ran Change.makeFromSet(_st, straighten=False)')
        return result

    def getAccidentals(self, alphaKey=None, addSymbol=False):
        """if alphaKey == None, it calculates accidentals for every key. Otherwise, just that one key."""
        if JazzNote.isAlphabetNoteStr(alphaKey) or alphaKey is None:
            pass
        else:
            raise TypeError("alphaKey is to be None or an alphabetKey")
        if alphaKey is None:
            _accidentals = 0
            _efficientKeys = self.getEfficientKeys(
                maxAccidentals=99,
                reorderByColourTranspose=False,
                includeOnlyTwelveKeys=True,
            )
            for key in _efficientKeys.items():
                _accidentals += JazzNote.countAccidentalsInStr(key[1])
        # print(len(_efficientKeys),_efficientKeys.items(),_accidentals,sep='\n')
        else:
            _key = self.byWays(alphaKey)
            _accidentals = JazzNote.countAccidentalsInStr(self.byWays(alphaKey))
        if addSymbol:
            return Unicode.chars["Accidentals"] + str(_accidentals)
        else:
            return _accidentals

    def getHeliotonia(self, alphaKey=None, includeSymbol=False):
        """alphaKey can be a str like Bb, A##, or it can be None, in which case all keys are being evaluated.
        Heliotonia will be returned as an integer. It means the maximum accidentals when each note get its own letter.
        include Symbol will insert the unicode symbol before the result"""
        # raise TypeError('I must finish this becv')
        if len(self) == 0:
            if includeSymbol:
                return Change.infoWaySymbols["Heliotonia"]
            else:
                return 0

        if self.getSeptatonicInAscendingGenericIntervals(
            returnTrueIfIsSeptaOrNegaSexta=True
        ):
            _straightenedSelf = self.getSeptatonicInAscendingGenericIntervals()
        else:
            _straightenedSelf = self.straightenDegrees(
                allowedNotes=Change.allowedNoteNamesFiveAccidentals
            )
            # raise TypeError('Heliotonia only applies to septatonic ways, not this: '+str(self))
        _maxAccidentals = 0
        if includeSymbol:
            _prependStr = Change.infoWaySymbols["Heliotonia"]
        else:
            _prependStr = ""
        if alphaKey == None:
            alphaKeys = _straightenedSelf.getEfficientKeys()
            for alphaKey in alphaKeys:
                _maxAccidentals = max(
                    max(
                        [JazzNote.countAccidentalsInStr(n) for n in alphaKeys[alphaKey]]
                    ),
                    _maxAccidentals,
                )
                # input('thelonious '+str(alphaKey)+str(alphaKeys)+' the key '+str(alphaKeys[alphaKey]))
            return _prependStr + str(_maxAccidentals)
        elif JazzNote.isAlphabetNoteStr(alphaKey):
            # only one key
            return _prependStr + str(
                max(
                    [
                        JazzNote.countAccidentalsInStr(n)
                        for n in _straightenedSelf.byWays(alphaKey)
                    ]
                )
            )
        else:
            raise TypeError(
                "The alphaKey must be a single alphabet note (or None for all keys), not "
                + str(alphaKey)
            )

    def getChangeNumber(
        self,
        returnBookPage=True,
        returnChapterPage=False,
        decorateChapter=False,
        decorateWithSmallCircle=False,
        imgTag="tabbingimg",
        key=None,
        combinatoricSize=12,
        addOneToBookPage=True,
        useUnicodeNumerals=True,
        includeChapterSymbol=False,
        includeNormalisedPageForNegatives=False,
        capitaliseNumeral=True,
        surroundPeriodInBrackets=False,
        surroundNormalisedResultInBrackets=False,
        useSpaceBetweenPeriodAndPage=True,
        useSpaceBetweenPageAndPeriod=True,
        diagramType="PCircle",
        filetype="pdf",
        externalGraphicsPath=False,
        renderIfNotFound=True,
        useTextStyledByWay=False
    ):
        # Because we are including the root note in the combinatorics
        combinatoricSize -= 1
        if not addOneToBookPage:
            raise TypeError("here it is using old numbering")
        if key is None:
            key = Change.rootColourKey
        elif "#" in key:
            raise ValueError("key should be expressed in all flats. " + key)
        elif not (JazzNote.isAlphabetNoteStr(key) or key == "BW"):
            raise TypeError("key should be an alphabet note")
        if Colour.useBlackBackground:
            invertColour = True
        else:
            invertColour = False

        if not Colour.makeGraphicsColoured:
            greyScale = True
        else:
            greyScale = False
        if decorateWithSmallCircle:
            decorateChapter = True
        _chapterBeginning = 0
        _chapterIndex = 0
        _indexOffset = 1
        _lastBump = None
        _semitones = self.getSemitones()
        # Make negative pages positive at first
        _forceOne = False
        C = Change.C
        if not 0 in _semitones:
            _semitones.insert(0, 0)
            _forceOne = True
            # print('bal', _semitones)
        for chapter in range(1, len(_semitones)):
            _chapterBeginning += C(combinatoricSize, chapter - 1)
        _semitones = _semitones[1:-1]
        # for chapter in range(1,len(self)):

        for idx, st in enumerate(_semitones):
            if st != idx + _indexOffset:
                _distanceFromExpected = st - _indexOffset - idx
                _indexesAwayFromEnd = len(_semitones) - 1 - idx
                # for i in range(_distanceFromExpected):
                _C = C(11 - _distanceFromExpected, _indexesAwayFromEnd) - 1
                # print(' ',st,'!=',idx + _indexOffset,' in ',_semitones,'(idx = ',idx,') d=',_distanceFromExpected,end='\n')
                _indexOffset += st + 0 - idx - _indexOffset
                # _chapterIndex += _distanceFromExpected * (len(_semitones) - idx)
                for i in range(_distanceFromExpected):
                    _C = C(
                        (combinatoricSize - st + _distanceFromExpected - i),
                        _indexesAwayFromEnd + 1,
                    )
                    _chapterIndex += _C
                    # print(' *c=',int(_C),end = ' ')
                # print('  newIndexoffset ',_indexOffset,'indexesAwayFromEnd',_indexesAwayFromEnd,end = ' ')
        # This adds for the last in the set
        if not len(self) == 0:
            _lastBump = (
                self.notes[-1].semitonesFromOne()
                - self.notes[-min(2, len(self))].semitonesFromOne()
                - 1
            )
        # print('last bump up:', _lastBump,end = '\n ')
        # return int(_chapterIndex + 1)
        _answer = ""
        _bookPage = int(_chapterIndex + _chapterBeginning)

        _chapterPage = int(_chapterIndex + 1)
        if _lastBump != None:
            _bookPage += +_lastBump
            _chapterPage += _lastBump
        # It was having trouble finding the bump offset when no 1
        # Now we'll just hardwire those diads (no 1) in.
        # They are subChange numbers -1 through -11
        if _bookPage == 0 and _chapterPage == 0:
            _bookPage = self.notes[0].semitonesFromOne()
            _chapterPage = _bookPage
        # Make the first one start at one and not zero

        if addOneToBookPage:
            _bookPage += 1
            # if not _forceOne:
            # if _bookPage == 0:
            #    _bookPage += 1
            if _forceOne:
                _chapterPage += 1

        # Reverse Polarity if no one in set
        if _forceOne == True:
            _bookPage *= -1
            _chapterPage = (_chapterPage - 1) * -1

        elif _forceOne == False and addOneToBookPage == False:
            _chapterPage -= 1
        # Hardwire first subChange Ohm
        if len(self) == 1 and self.containsNotes("1"):
            if addOneToBookPage:
                _bookPage = 1
                _chapterPage = 1
            else:
                _bookPage = 0
                _chapterPage = 0
        # Hardwire negative first subChange Silence
        elif len(self.notes) == 0:
            if addOneToBookPage:
                _bookPage = -1
            else:
                _bookPage = None
        # default capitalisation
        _isCapital = True
        if returnChapterPage == True:
            if capitaliseNumeral == True:
                _isCapital = Change.chordHasUpperCaseNumeral(
                    self.getNormalForm().getChordQuality()
                )

        # Dress it up
        if decorateWithSmallCircle == True:
            _pageNumberSymbol = Latex.insertSmallDiagram(
                change=self,
                key=key,
                diagramType=diagramType,
                filetype=filetype,
                imgtag=imgTag,
                externalGraphicsPath=externalGraphicsPath,
                renderIfNotFound=renderIfNotFound,
            )

        if decorateChapter == True:
            if not decorateWithSmallCircle:
                _pageNumberSymbol = Unicode.chars["Change Number"]
            _bookPage = _pageNumberSymbol + str(_bookPage)
            _chapterPage = str(_chapterPage)

            if not len(self) == 0:
                _length = JazzNote(str(len(self))).getRomanNumeral(
                    useUnicodeNumerals=useUnicodeNumerals, returnCapital=_isCapital
                )
            else:
                _length = "nulla"

            if useUnicodeNumerals:
                _length = _length
                if includeChapterSymbol:
                    if useSpaceBetweenPageAndPeriod == True:
                        _length = " " + Unicode.chars["Chapter Number"] + _length
                    elif useSpaceBetweenPageAndPeriod == False:
                        _length = Unicode.chars["Chapter Number"] + _length
                if useSpaceBetweenPeriodAndPage:
                    _length += " "
            else:
                _length = _length
                if includeChapterSymbol:
                    if useSpaceBetweenPageAndPeriod == True:
                        _length = Unicode.chars["Chapter Number"] + " " + _length
                    elif useSpaceBetweenPageAndPeriod == False:
                        _length = Unicode.chars["Chapter Number"] + _length
            _chapterPage = Unicode.chars["Chapter Change Number"] + _chapterPage
        if returnBookPage == True and returnChapterPage == False:
            _answer = _bookPage
        elif returnChapterPage == True and returnBookPage == False:
            _answer = _chapterPage
        elif returnChapterPage == True and returnBookPage == True:
            _answer += str(_bookPage)
            if useSpaceBetweenPageAndPeriod == True:
                _answer += " "
            if decorateChapter == True:
                if surroundPeriodInBrackets:
                    _answer += "("
                _answer += str(_length)
            _answer += str(_chapterPage)
            if decorateChapter == True and surroundPeriodInBrackets:
                _answer += ")"

        if (
            not self.containsNotes("1")
            and includeNormalisedPageForNegatives is True
            and decorateChapter is True
        ):
            if surroundNormalisedResultInBrackets is True:
                _answer += "("
            _answer += Unicode.chars[
                "Normalise"
            ] + self.getNormalForm().getChangeNumber(
                returnBookPage=returnBookPage,
                returnChapterPage=returnChapterPage,
                decorateChapter=decorateChapter,
                addOneToBookPage=addOneToBookPage,
                useUnicodeNumerals=useUnicodeNumerals,
                includeChapterSymbol=includeChapterSymbol,
                includeNormalisedPageForNegatives=False,
                key=key,
                decorateWithSmallCircle=decorateWithSmallCircle,
                renderIfNotFound=renderIfNotFound,
            )

            if surroundNormalisedResultInBrackets is True:
                _answer += ")"

        if useTextStyledByWay:
            _answer = Latex.makeTextStyledByWay(_answer,'Change Number')
        return _answer

        # return _chapterBeginning + _chapterIndex

    def getChord(self, genericInterval: int, chordType: int, complain=True) -> Change:
        # if chordType not in Chord.validTypes: raise ValueError(chordType+' not in '+Chord.validTypes)
        raise TypeError("not actually using this")
        if genericInterval >= len(self):
            raise ValueError(genericInterval + "is outside of this change." + len(self))
        if complain == True:
            if len(Chord.validTypesByLength[len(self)]) < chordType:
                raise ValueError(
                    chordType + " not in " + Chord.validTypesByLength[len(self)]
                )
        _indexes = Chord.chordIndexes(len(self), rootIndex=genericInterval)
        _notes = [self.notes[i] for i in _indexes]
        return Change(_notes)

    def getScaleChord(
        self,
        startingNoteIndex,
        noteIndexStepSize=2,
        numberOfNotes=4,
        returnTypeChange=False,
        complainAboutRedundancy=False,
    ):
        if not type(startingNoteIndex) in (np.int64, int):
            raise TypeError(
                "startingNoteIndex must be an in not {}".format(type(startingNoteIndex))
            )
        _mode = self.getNormalForm().mode(startingNoteIndex)
        # _mode = self.getNormalForm().mode(startingNoteIndex)
        _chordNotes = []
        # print(str(list(range(0, (noteIndexStepSize * numberOfNotes), noteIndexStepSize)))+'hawt shit'+str(self))
        # input()
        for i in range(0, (noteIndexStepSize * numberOfNotes), noteIndexStepSize):
            # for i in range(0,(noteIndexStepSize*numberOfNotes),noteIndexStepSize):
            # +1 somewhere here?
            _chordNote = _mode.notes[i % max((len(self.notes)), 1)]
            if _chordNote not in _chordNotes:
                _chordNotes.append(_chordNote)
        _chordNotes = Change(_chordNotes)
        # _chordNotes = Change(_mode.notes for i in [0, 2%len(self.notes), 4%len(self.notes), 6%len(self.notes) ]).getChordQuality()
        # print('index', startingNoteIndex,'mode', _mode, _chordNotes)
        if len(_chordNotes) != numberOfNotes:
            if complainAboutRedundancy:
                print(
                    "the chord "
                    + str(self)
                    + " :: "
                    + str(_chordNotes)
                    + " ended up with "
                    + str(len(_chordNotes))
                    + " notes instead of "
                    + str(numberOfNotes)
                )
            # raise ValueError('the chord '+str(self)+ ' :: '+str(_chordNotes)+' ended up with '+str(len(_chordNotes)) + ' notes instead of '+str(numberOfNotes))
        else:
            if complainAboutRedundancy:
                print("it found the right number of notes", _chordNotes)
        if returnTypeChange:
            return _chordNotes
        else:
            return _chordNotes.getChordQuality()

    def getRingNumber(self, includePreString=False):
        _total = 0
        for i in self.byWays("Set"):
            _total += 2 ** int(i)
        if includePreString == True:
            return Unicode.chars["Ring Number"] + str(_total)
        else:
            return _total

    def getRingBits(self, colourResult=False):
        return self.getBitMap(
            trueSymbol="1",
            falseSymbol="0",
            eastBitIsRoot=True,
            colourResult=colourResult,
        )

    def getBitMap(
        self,
        notePossibilities=12,
        seperator="",
        trueSymbol=None,
        falseSymbol=None,
        colourResult=True,
        eastBitIsRoot=False,
    ):
        if trueSymbol == None:
            trueSymbol = Unicode.chars["Binary True"]
        if falseSymbol == None:
            falseSymbol = Unicode.chars["Binary False"]

        trueSymbol = str(trueSymbol)
        falseSymbol = str(falseSymbol)

        _bitMap = []
        _set = self.byWays("Set")
        for i in range(notePossibilities):
            if str(i) in _set:
                # True
                _bitMap.append(trueSymbol)
                if Latex.makeTextColoured and colourResult:
                    _bitMap[-1] = JazzNote.makeFromSet(i).makeResultColoured(
                        _bitMap[-1]
                    )
            else:
                # False
                _bitMap.append(falseSymbol)
                if Latex.makeTextColoured and colourResult:
                    _bitMap[-1] = JazzNote.makeFromSet(i).makeResultColoured(
                        _bitMap[-1]
                    )
        if eastBitIsRoot:
            _bitMap = _bitMap[::-1]
        return seperator.join(_bitMap)

    def getForteNumber(self, decorateWithUnicode=False):
        dec = ""
        if decorateWithUnicode:
            dec = Change.infoWaySymbols["Forte Number"]
        if len(self) == 0:
            return dec + "0-1"
        from ScaleNames import ScaleNames
        mydict = ScaleNames.forteNumbers
        return dec + (
            list(mydict.keys())[
                list(mydict.values()).index(
                    self.getPrimeForm(returnInSemitonePositions=True)
                )
            ]
        )  # Prints george
        return (
            dec
            + ScaleNames.forteNumbers[
                ScaleNames.forteNumbers.keys().index(self.getPrimeForm().getSemitones())
            ]
        )

    def getNormalForm(self):
        if self.containsNotes("1"):
            return self
        else:
            return Change.makeFromSet(
                [i - self.notes[0].semitonesFromOne() for i in self.getSemitones()]
            )

    def getTimeOfDay(self, includeMilliseconds=False, capitaliseAMPM=True):
        # 🕐🕜 🕑🕝 🕒🕞 🕓🕟 🕔🕠 🕕🕡 🕖🕢 🕗🕣 🕘🕤 🕙🕥 🕚🕦 🕛🕧
        # 🕐 🕑 🕒 🕓 🕔 🕕 🕖 🕗 🕘 🕙 🕚 🕛
        # 🕜 🕝 🕞 🕟 🕠 🕡 🕢 🕣 🕤 🕥 🕦 🕧

        _pageNumber = self.getChangeNumber(decorateChapter=False, addOneToBookPage=True)
        # changeNumber used to be one less for positives
        _seconds = abs(_pageNumber) * (60 * 60 * 24 / 4096)
        _milliseconds = str(math.floor((_seconds * 1000) % 1000))
        _minutes = str(math.floor((_seconds / 60) % 60))
        _hours = str(math.floor(_seconds / 60**2))
        _seconds = str(math.floor(_seconds % 60))
        if _hours in (0, "0"):
            _hours = "12"

        while len(_minutes) < 2:
            _minutes = "0" + _minutes
        while len(_seconds) < 2:
            _seconds = "0" + _seconds
        while len(_milliseconds) < 3:
            _milliseconds = "0" + _milliseconds

        if _hours == "12":
            _amPm = "am"
        else:
            _amPm = "pm"
        if not self.containsNotes("1"):
            if _amPm == "am":
                _amPm = "pm"
            elif _amPm == "pm":
                _amPm == "am"

        if _hours == "12":
            if int(_minutes) < 30:
                _clock = "🕛"
            else:
                _clock = "🕧"
        elif _hours == "1":
            if int(_minutes) < 30:
                _clock = "🕐"
            else:
                _clock = "🕜"
        elif _hours == "2":
            if int(_minutes) < 30:
                _clock = "🕑"
            else:
                _clock = "🕝"
        elif _hours == "3":
            if int(_minutes) < 30:
                _clock = "🕒"
            else:
                _clock = "🕞"
        elif _hours == "4":
            if int(_minutes) < 30:
                _clock = "🕓"
            else:
                _clock = "🕟"
        elif _hours == "5":
            if int(_minutes) < 30:
                _clock = "🕔"
            else:
                _clock = "🕠"
        elif _hours == "6":
            if int(_minutes) < 30:
                _clock = "🕕"
            else:
                _clock = "🕡"
        elif _hours == "7":
            if int(_minutes) < 30:
                _clock = "🕖"
            else:
                _clock = "🕢"
        elif _hours == "8":
            if int(_minutes) < 30:
                _clock = "🕗"
            else:
                _clock = "🕣"
        elif _hours == "9":
            if int(_minutes) < 30:
                _clock = "🕘"
            else:
                _clock = "🕤"
        elif _hours == "10":
            if int(_minutes) < 30:
                _clock = "🕙"
            else:
                _clock = "🕥"
        elif _hours == "11":
            if int(_minutes) < 30:
                _clock = "🕚"
            else:
                _clock = "🕦"

        if capitaliseAMPM == True:
            _amPm = _amPm.upper()
        if includeMilliseconds:
            return (
                _clock + ":".join([_hours, _minutes, _seconds, _milliseconds]) + _amPm
            )
        elif not includeMilliseconds:
            return _clock + ":".join([_hours, _minutes, _seconds]) + _amPm

    def getPrimeness(
        self, addOne=True, decorate=False, decoratePrimeModeMore=True, showDebug=False
    ):
        if False and not Book.makePrimes:
            warnings.warn(
                "Primeness is being accessed, while Book.makePrimes==False, so something will fuck up to do with it."
            )
        if decorate is True:
            _decorationStr = Change.infoWaySymbols["Primeness"]
        else:
            _decorationStr = ""
        if addOne is True:
            _startingIndex = 1
        else:
            _startingIndex = 0
        if len(self) == 0:
            return _startingIndex
        _modesInSemitones = []
        # indexOfPrimeness returns the nth primeest.. so if it is zero it is the true prime, if it is len(self) it is the least
        _adjustedSelf = self.getNormalForm()
        _modesInSemitones = []
        for mode in range(len(_adjustedSelf)):
            _modesInSemitones.append(tuple(_adjustedSelf.modeInSemitones(mode)))
        _modeCandidates = list(set(_modesInSemitones))
        from operator import itemgetter
        _modeCandidates = sorted(
            _modeCandidates, key=itemgetter(*list(range(len(self) - 1, -1, -1)))
        )
        if showDebug:
            print(_modeCandidates)
        _primeness = _modeCandidates.index(tuple(_adjustedSelf.modeInSemitones(0)))
        if _primeness == 0 and decorate and decoratePrimeModeMore:
            _decorationStr = Change.infoWaySymbols["Is Prime"]
        return _decorationStr + str(_primeness + _startingIndex)

    def getPrimeForm(
        self,
        returnTrueIfPrime=False,
        returnInSemitonePositions=False,
        indexOfPrimeness=0,
    ):
        if len(self) == 0:
            return self
        # indexOfPrimeness returns the nth primeest.. so if it is zero it is the true prime, if it is len(self) it is the least
        _adjustedSelf = self.getNormalForm()

        _modesInSemitones = []
        for mode in range(len(_adjustedSelf)):
            _modesInSemitones.append(tuple(_adjustedSelf.modeInSemitones(mode)))
        _modeCandidates = list(set(_modesInSemitones))
        from operator import itemgetter
        _modeCandidates = sorted(
            _modeCandidates, key=itemgetter(*list(range(len(self) - 1, -1, -1)))
        )
        # print(_modeCandidates)
        if returnTrueIfPrime:
            return (
                _modesInSemitones[indexOfPrimeness] == _modeCandidates[indexOfPrimeness]
            )

        elif returnInSemitonePositions:
            return _modeCandidates[indexOfPrimeness]
        else:
            return Change.makeFromSet(
                _modeCandidates[indexOfPrimeness % len(_modeCandidates)]
            )

    def getSemitones(self):
        return [int(i) for i in self.byWays("Set")]

    def getIntFifthPositions(self, useFourthsInstead=False):
        _sts = self.getSemitones()
        _fifths = []
        if useFourthsInstead == True:
            _specificInterval = 5
        else:
            _specificInterval = 7
        for i in _sts:
            _fifths.append = (_sts * _specificInterval) % 12
        return _fifths

    def getEfficientKeys(
        self,
        maxAccidentals=3,
        showDebug=False,
        autoStraighten=False,
        returnFlattenedList=True,
        returnDictionary=True,
        reorderByColourTranspose=True,
        addHeliotoniaToKeyName=False,
        reorderByMaxAccidentals=False,
        includeOnlyTwelveKeys=False,
    ):
        """returns list of lists
        where the first index is semitone distance,
        and the inner index is any keys that didn't get removed
        It's going to remove any spelling that has more accidentals
        then sort by max accidentals if that is true
        If returnFlattenedList, they will be in same order but simply a list of the keys
        reorderByColourTranspose will shift the root key
        """
        # This will return all 12 keys adjusted for least accidentals
        if len(self) == 0:
            return OrderedDict(
                [
                    ("C", []),
                    ("D♭", []),
                    ("D", []),
                    ("E♭", []),
                    ("E", []),
                    ("F", []),
                    ("F♯", []),
                    ("G", []),
                    ("A♭", []),
                    ("A", []),
                    ("B♭", []),
                    ("B", []),
                ]
            )

        _allKeys = []
        _allKeysRoot = []
        _efficientKeys = []
        _efficientKeysRoots = []
        if returnFlattenedList:
            _flattenedEfficientKeys = []
            _flattenedEfficientRoots = []
        _numberOfAccidentals = []
        _maxNumberOfAccidentals = []
        if autoStraighten:
            if (self.containsNotes("1") and len(self) <= 7) or (
                not self.containsNotes("1") and len(self) <= 6
            ):
                _straightenedSelf = self.straightenDegrees(
                    Change.allowedNoteNamesFiveAccidentals
                )
            else:
                _straightenedSelf = self.straightenDegrees(Change.allowedNoteNamesJazz)
        else:
            _straightenedSelf = self
        for i in range(12):
            _allKeys.append([])
            _allKeysRoot.append([])
            _efficientKeys.append([])
            _efficientKeysRoots.append([])
            _numberOfAccidentals.append([])
            _maxNumberOfAccidentals.append([])

        # for absoluteInterval in range(12):
        for st, noteClass in enumerate(Change.validEnharmonicAlphabetNames):
            for key in noteClass:
                _allKeys[st].append(_straightenedSelf.byWays(key))
                _allKeysRoot[st].append(key)

                # >>> data = ["the foo is all fooed", "the bar is all barred", "foo is now a bar"]
                # >>> sum('foo' in s for s in data)

                # if JazzNote(noteName).semitonesFromOne() -  == absoluteInterval:
                #   absoluteIntervals[absoluteInterval].append(noteName)
        for st, abInterval in enumerate(_allKeys):
            for idx, key in enumerate(abInterval):
                _rootNote = _allKeysRoot[st][idx]
                _thisNoOfAccidentals = 0
                _thisMaxNumberOfAccidentals = 0

                for note in _straightenedSelf.byWays(key[0]):
                    _thisNoOfAccidentals += (
                        note.count("#")
                        + note.count("b")
                        + note.count("♯")
                        + note.count("♭")
                    )
                    _thisMaxNumberOfAccidentals = max(
                        _thisMaxNumberOfAccidentals,
                        note.count("#"),
                        note.count("b"),
                        note.count("♯"),
                        note.count("♭"),
                    )
                _maxNumberOfAccidentals[st].append(_thisMaxNumberOfAccidentals)
                # If the _efficientKeys is empty append,
                if _efficientKeys[st] == []:
                    _efficientKeys[st].append(key)
                    _efficientKeysRoots[st].append(_rootNote)
                    _numberOfAccidentals[st].append(_thisNoOfAccidentals)
                # If the numberOfAccidentals is less, replace
                elif _thisNoOfAccidentals < _numberOfAccidentals[st][0]:
                    _efficientKeys[st][0] = key
                    _efficientKeysRoots[st][0] = _rootNote
                    if showDebug:
                        print(
                            "holy smoke"
                            + str(key)
                            + "    "
                            + str(abInterval)
                            + " "
                            + str(self)
                        )
                    _numberOfAccidentals[st][0] = _thisNoOfAccidentals
                # If it is tied, add both
                elif (
                    _thisNoOfAccidentals == _numberOfAccidentals[st][0]
                    and not includeOnlyTwelveKeys
                ):
                    # Then sort by max number of accidentals
                    # print('blablabla',_maxNumberOfAccidentals)
                    if _thisMaxNumberOfAccidentals > _maxNumberOfAccidentals[st][0]:
                        # spock
                        _efficientKeys[st].insert(0, key)
                        _efficientKeysRoots[st].insert(0, _rootNote)
                        _numberOfAccidentals[st].insert(0, _thisNoOfAccidentals)
                    else:
                        _efficientKeys[st].append(key)
                        # _efficientKeysRoots[st].insert(0,_rootNote)
                        _efficientKeysRoots[st].append(_rootNote)
                        _numberOfAccidentals[st].append(_thisNoOfAccidentals)

                if showDebug:
                    print(
                        "the key",
                        key,
                        _thisNoOfAccidentals,
                        note,
                        "ef",
                        _efficientKeys,
                        _efficientKeysRoots,
                    )
                # answer is _efficientKeys

        if showDebug:
            input("here it is" + str(_efficientKeysRoots))
        if returnFlattenedList:
            for idx, st in enumerate(_efficientKeys):
                for i, k in enumerate(st):
                    _flattenedEfficientKeys.append(k)
                    _flattenedEfficientRoots.append(_efficientKeysRoots[idx][i])
            _keyShift = 0
            if reorderByColourTranspose == True:
                # if Change.rootColourKey in _flattenedEfficientRoots:
                #    _keyShift = _flattenedEfficientRoots.index(Change.rootColourKey)
                for i, r in enumerate(_flattenedEfficientRoots):
                    if JazzNote.distanceFromC(r) == JazzNote.distanceFromC(
                        Change.rootColourKey
                    ):
                        _keyShift = i
            elif reorderByColourTranspose == False:
                _keyShift = 0
            _flattenedEfficientKeys = (
                _flattenedEfficientKeys[_keyShift:]
                + _flattenedEfficientKeys[:_keyShift]
            )
            _flattenedEfficientRoots = (
                _flattenedEfficientRoots[_keyShift:]
                + _flattenedEfficientRoots[:_keyShift]
            )
            if reorderByMaxAccidentals:
                _sortOrder = [
                    JazzNote.countAccidentalsInStr(i) for i in _flattenedEfficientKeys
                ]
                _sortOrder, _flattenedEfficientKeys, _flattenedEfficientRoots = (
                    list(t)
                    for t in zip(
                        *sorted(
                            zip(
                                _sortOrder,
                                _flattenedEfficientKeys,
                                _flattenedEfficientRoots,
                            )
                        )
                    )
                )

                # list1 = [3, 2, 4, 1, 1]
                # list2 = ['three', 'two', 'four', 'one', 'one2']
                # list1, list2 = (list(t) for t in zip(*sorted(zip(list1, list2))))

        if returnDictionary:
            from collections import OrderedDict
            _dict = OrderedDict()
            if returnFlattenedList:
                for i in range(len(_flattenedEfficientKeys)):
                    _keyName = JazzNote.convertNoteToRealUnicodeStr(
                        _flattenedEfficientRoots[i]
                    )
                    if addHeliotoniaToKeyName:
                        _keyName = (
                            self.getHeliotonia(
                                _flattenedEfficientRoots[i], includeSymbol=True
                            )
                            + _keyName
                        )
                    _dict[_keyName] = _flattenedEfficientKeys[i]
            else:
                raise ValueError(
                    "Have not made this yet, where return type is dictionary that isn't flattened."
                )
            return _dict
        else:
            if addHeliotoniaToKeyName:
                return [
                    self.getHeliotonia(i, includeSymbol=True) + i
                    for i in _efficientKeys
                ]
            else:
                return _efficientKeys

    def getBinomial(self):

        _d = self.getIntervalVector(sep=",").split(",")
        _binomial = ""
        _binomialValues = {"1": "D", "2": "S", "3": "N", "4": "M", "5": "P", "6": "T"}
        for i in [5, 4, 3, 2, 1, 6]:
            if _d[i - 1] != "0":
                _binomial += _binomialValues[str(i)]
                _binomial += _d[i - 1]
        # _binomial = _binomial.replace('T', '¹⁰')
        # _binomial = _binomial.replace('E', '¹¹')
        # _binomial = _binomial.replace('10', '¹⁰')
        # _binomial = _binomial.replace('11', '¹¹')
        _binomial = _binomial.replace("1", "¹")  # ³⁴⁵⁶⁷⁸⁹
        _binomial = _binomial.replace("2", "²")
        _binomial = _binomial.replace("3", "³")
        _binomial = _binomial.replace("4", "⁴")
        _binomial = _binomial.replace("5", "⁵")
        _binomial = _binomial.replace("6", "⁶")
        _binomial = _binomial.replace("7", "⁷")
        _binomial = _binomial.replace("8", "⁸")
        _binomial = _binomial.replace("9", "⁹")
        _binomial = _binomial.replace("0", "⁰")
        return _binomial

    def getCirclePositions(
        self,
    ):
        _degrees = [i.semitonesFromOne() * (360 / 12) for i in change.notes]
        _degrees = _degrees + [_degrees[0]]
        _degrees = [(i + 270) % 360 for i in _degrees]

    def getAngles(
        self,
        returnDegrees=False,
        goQuarterTurnAnticlockwise=False,
        repeatFirstResult=False,
        makeRepeatedResultLargerThanOneBefore=False,
        humanFormat=False,
    ):
        if len(self.notes) == 0:
            return []
        if returnDegrees == True:
            _angles = [i * (360 / 12) for i in self.getSemitones()]
        else:
            _angles = [i * (2 * math.pi / 12) for i in self.getSemitones()]
        if goQuarterTurnAnticlockwise == True:
            if returnDegrees == False:
                _angles = [i - math.pi / 2 for i in _angles]
            else:
                _angles = [i - 90 for i in _angles]

        if repeatFirstResult == True:
            _angles = _angles + [_angles[0]]
            if makeRepeatedResultLargerThanOneBefore:
                if _angles[-1] < _angles[-2]:
                    if returnDegrees == True:
                        _angles[-1] += 360
                    else:
                        _angles[-1] += 2 * math.pi

        if humanFormat == True:
            if returnDegrees == False:
                _angles = [str(round(i / math.pi, 2)) + "π" for i in _angles]
            elif returnDegrees == True:
                _angles = [str(round(i, 2)) + "°" for i in _angles]

        return _angles

    def getArea(self):
        _poly = self.getPolygon()

        """Return the area of the polygon whose vertices are given by the
        sequence points.
        https://codereview.stackexchange.com/questions/88010/area-of-an-irregular-polygon

        """
        area = 0
        if _poly == None or len(_poly) < 1:
            return area
        q = _poly[-1]
        for p in _poly:
            area += p[0] * q[1] - p[1] * q[0]
            q = p
        area *= 4 / 3
        return abs(area / 2)

    def getPolygon(
        self,
        boundL: float = 0,
        boundT: float = 0,
        boundR: float = 1,
        boundB: float = 1,
        closePolygon=True,
        formatForHumans=False,
        useTopOrigin=True,
        returnFCircle=False,
        colourTranspose=0,
        useSemitones=True,
        scale=1.0,
        shrinkIntoOrigin=False,
    ) -> list[tuple]:
        """
        Returns list of normalised coordinates in the form [(x0,y0), ...(xn,yn)]
        Does not return the first coordinate twice.
        If useSemitones == False, it will map to the circle of fifths.
        """
        #
        # if len(self) <= 2:
        #    return None
        if returnFCircle:
            scale = 1.0
        if boundR < boundL:
            raise ValueError("It seems right boundary < left boundary ")

        if useTopOrigin:
            if boundB < boundT:
                # raise ValueError('It seems bottom boundary: {}< top boundary: {}, and you are using the top origin.'.format(boundB,boundT))
                boundB, boundT = boundT, boundB
        else:
            if boundB > boundT:
                boundB, boundT = boundT, boundB
                # raise ValueError('It seems bottom boundary: {}> top boundary: {}, and you are using the bottom origin.'.format(boundB,boundT))

        if any([type(i) not in (int, float) for i in (boundL, boundR, boundT, boundB)]):
            raise TypeError(
                "bounds are to be specified in int or float. {} {} {} {} typeBoundT {}".format(
                    boundL, boundR, boundT, boundB, type(boundT)
                )
            )

        # input(scale)
        _radians = self.getAngles(returnDegrees=False)
        xWidth = abs(boundR - boundL)
        yWidth = abs(boundB - boundT)

        xMid = boundL + xWidth / 2
        yMid = boundT + yWidth / 2

        if shrinkIntoOrigin:

            # _x = [math.sin(i)*(scale) for i in _radians]
            _x = [math.sin(i) for i in _radians]
            # _y = [math.cos(i)*(scale) for i in _radians]
            _y = [math.cos(i) for i in _radians]
            # _polyCentreX = sum([i for i in _x]) / len(_x)
        # _polyCentreY = sum([i for i in _y]) / len(_y)
        # requires import gdspy
        # gdPoly = gdspy.Polygon([(_x[i],_y[i]) for i in range(len(_x))])
        # gdPoly.scale(scale,scale,(_polyCentreX,_polyCentreY))
        # input(gdPoly.polygons[0][0][0])
        # for i in gdPoly.polygons[0]:
        # print(i)
        # print('stuff')
        # _x = [float(i[0]) for i in gdPoly.polygons[0]]
        # _y = [float(i[1]) for i in gdPoly.polygons[0]]
        # print(_x,_y,'cowabunga')

        # input('{} {} {} {} {}'.format(
        #    _polyCentreX,_polyCentreY,xMid,xWidth,_x))
        # _newR = Graphics.distanceBetween(
        #    _polyCentreX,_polyCentreY,0,0,returnDirection=False)
        # _newR = 1
        # _x = [i + _polyCentreX *for i in _x]
        # _y = [i + _polyCentreY *for i in _y]
        else:
            _x = [math.sin(i) * scale for i in _radians]
            _y = [math.cos(i) * scale for i in _radians]

        # print('start getPolygon() returnFCircle {} radians {}'.format(returnFCircle,_radians))
        # _polygon = [((xWidth/2)+_x[i]*(xWidth/2), (yWidth/2)+_y[i]*(yWidth)/2) for i in range(len(_radians))]
        if returnFCircle == False:

            if not useTopOrigin:
                _polygon = [
                    (xMid + _x[i] * xWidth / 2, yMid + _y[i] * yWidth / 2)
                    for i in range(len(_radians))
                ]
            else:
                _polygon = [
                    (xMid + _x[i] * xWidth / 2, yMid - _y[i] * yWidth / 2)
                    for i in range(len(_radians))
                ]
            if len(self) == 0:
                return None
            if closePolygon:
                _polygon = _polygon + [_polygon[0]]
            return _polygon

        else:
            xWidth = abs(boundR - boundL)
            yWidth = abs(boundB - boundT)
            xMid = boundL + xWidth / 2
            yMid = boundT + yWidth / 2

            _polygon = [
                (xMid + _x[i] * xWidth / 2, yMid - _y[i] * yWidth / 2)
                for i in range(len(_radians))
            ]

            """if not useTopOrigin:
                _polygon = [(_x[i] * xWidth/2,
                             _y[i] * xWidth/2)
                            for i in range(len(_radians))]
            else:
                _polygon = [((_x[i] + 0.5) * xWidth/2,
                             (_y[i] + 0.5) * xWidth/2)
                            for i in range(len(_radians))]"""

        _polygon = [list(i) for i in _polygon]

        if returnFCircle == True:

            # print('start getPolygon from within itself')
            _poly = _polygon
            """input('v1\n{}\nv2\n{}\n and that was all...'.format(
                _poly, self.getPolygon(boundL=0,
                    boundT=0,
                    boundR=1,
                    boundB=1,returnFCircle=False,)
            ))"""

            """_poly = self.getPolygon(boundL=0,
                    boundT=0,
                    boundR=1,
                    boundB=1,returnFCircle=False,)"""

            _polygonCentre = None

            try:
                _polygonCentre = polylabel([_poly], precision=1, with_distance=True)

            except:
                return None

            if _polygonCentre[1] is None:
                return None
            # Putting
            xWidth = 1
            yWidth = 1
            xMid = 0.5
            yMid = 0.5

            _polygonCentre = (
                [
                    xMid + (_polygonCentre[0][0] - 0.5) * xWidth,
                    yMid + (_polygonCentre[0][1] - 0.5) * xWidth,
                ],
                _polygonCentre[1] * xWidth,
            )

            # print('making _poly')
            _poly = FCircle(
                centre=[_polygonCentre[0][0], _polygonCentre[0][1]],
                r=_polygonCentre[1],
                change=self.getReverse(),
                colourTranspose=colourTranspose,
            )
            # print('done making _poly')

            # _poly.movePosition(_polygonCentre[0][0],_polygonCentre[0][1])

            return _poly
        else:
            pass
        return _polygon

    def getSpectralVariation(self):  # 🐡 monkey
        if len(self) == 0:
            return 0
        _spectraWidths = self.getSpectraVariation(returnSpectraWidths=True)
        _totalWidth = 0

        for width in _spectraWidths:
            _totalWidth += width
        _originalAnswer = round(_totalWidth / len(self), 2)
        _widthVariation = _totalWidth / len(self)
        _fractionPart = _widthVariation - math.floor(_widthVariation)
        _fractionPart = round(_fractionPart, 6)

        _fractionPart = Utility.floatToFraction(_fractionPart, latexFractions=Latex.on)

        _widthVariationInt = int(math.floor(_widthVariation))
        if _widthVariationInt == 0 and _fractionPart != 0:
            _widthVariationInt = ""
        if len(str(_widthVariationInt) + str(_fractionPart)) == 0:
            return "0"
        else:
            return str(_widthVariationInt) + str(_fractionPart)

    def getSpectraVariation(
        self,
        returnDistributionSpectra=False,
        returnSpectraWidths=False,
        returnMyhillProperty=False,
        sortSpectraByOccurences=False,
    ):
        _semitones = self.getSemitones()
        _distributionSpectra = []
        # Build distribution spectra
        for genericInterval in range(1, len(_semitones)):
            _distributionSpectra.append([])
            for note in range(len(_semitones)):
                _specificInterval = (
                    _semitones[(genericInterval + note) % len(_semitones)]
                    - _semitones[note]
                )
                if _specificInterval < 0:
                    _specificInterval += 12
                if not _specificInterval in _distributionSpectra[-1]:
                    _distributionSpectra[-1].append(_specificInterval)

        # Done building distribution
        if returnDistributionSpectra:
            if sortSpectraByOccurences:

                for genericInterval in _distributionSpectra:
                    genericInterval.sort(
                        key=lambda x: self.byWays("Step").count(str(x))
                    )
            return _distributionSpectra
        _spectraWidths = []
        for i in _distributionSpectra:  # Get distance
            _spectraWidths.append(max(i) - min(i))
        if returnSpectraWidths:
            return _spectraWidths
        _totalWidths = 0
        for i in _spectraWidths:
            _totalWidths += i
        if returnMyhillProperty:
            if len(_distributionSpectra) == 0:
                return False
            for i in _distributionSpectra:
                if len(i) == 2:
                    _myhill = True

                else:
                    _myhill = False
                    break
            return _myhill
        return int(_totalWidths / len(self))

        # spectrumVariation

    def getCoherence(self):
        _distributionSpectra = self.getSpectraVariation(returnDistributionSpectra=True)

        _genericIntervalsMax = []
        for genericInterval in range(1, len(_distributionSpectra)):
            _genericIntervalsMax = max(_distributionSpectra[genericInterval - 1])
            if _genericIntervalsMax >= min(
                _distributionSpectra[min(genericInterval, len(_distributionSpectra))]
            ):
                return False
        return True

    def getEnantiomorph(self) -> Change:
        result = self.getChirality(returnEnantiomorph=True)
        if result and result not in [self.mode(m) for m in range(len(self))]:
            return result
        else:
            return self

    def getChirality(self, returnEnantiomorph=False, reverseAnswer=False):
        _answer = False
        _downwards = self.getReverse().getSemitones()
        for rotation in range(len(self)):
            if self.mode(rotation).getSemitones() == _downwards:
                _answer = True  # Meaning that it IS chiral so it has an enantiomorph
                if returnEnantiomorph == True:
                    return self.mode(rotation)
                break
        if reverseAnswer == True:
            _answer = not _answer
        return _answer

    def getCohemitonia(self):  # Max amount of notesets in a row
        _steps = [int(i) for i in self.byWays("Step")]
        if all([int(i) == 1 for i in _steps]):
            return len(self)
        _hemitonesLeadingToTheOne = 0
        # First find the hemitones preceeding the one (below it)
        for i in range(1, len(_steps)):  # Maybe +1
            if _steps[-i] == 1:
                _hemitonesLeadingToTheOne += 1
            else:
                break

        _upwardsHemitones = _hemitonesLeadingToTheOne
        _largestNumberOfHemitones = _upwardsHemitones
        for i in _steps:
            if i == 1:
                _upwardsHemitones += 1
            else:
                _largestNumberOfHemitones = max(
                    _upwardsHemitones, _largestNumberOfHemitones
                )
                _upwardsHemitones = 0
            _largestNumberOfHemitones = max(
                _upwardsHemitones, _largestNumberOfHemitones
            )

        return _largestNumberOfHemitones

    def getImperfections(self):
        _imperfections = 0
        _inSemitones = self.getSemitones()
        for i in range(len(_inSemitones)):
            if not (_inSemitones[i] + 7) % 12 in _inSemitones:
                _imperfections += 1
        return _imperfections

    def getIntervalVector(self, sep="", convert10ToT=False):  # Wrong shit
        # These numbers will be the amount of that size of interval (in notesets)
        # in the change

        if len(self) == 12:
            if not convert10ToT:
                return sep.join(["12", "12", "12", "12", "12", "6"])
            else:
                return sep.join(['T'] * 5 + ['6'])
        _semitones = [int(i) for i in self.byWays("Step")]
        _one = 0
        _two = 0
        _three = 0
        _four = 0
        _five = 0
        _six = 0
        _distributionSpectra = self.getSpectraVariation(returnDistributionSpectra=True)

        # Flatten that list
        _distributionSpectra = [
            item for sublist in _distributionSpectra for item in sublist
        ]
        # print(self, self.getSpectraVariation(returnDistributionSpectra=True))
        _intervalVector = ""
        # 		for baseNote in range(len(_semitones)):
        # 			otherNote = _semitones[(baseNote+1)%len(_semitones)]
        #
        # 			if otherNote == 0: otherNote = 12
        #
        # 	_interval = otherNote-_semitones[baseNote]
        # 	if _interval in (1, 11): _one += 1
        # 	if _interval in (2, 10): _two += 1
        # 	if _interval in (3, 9): _three += 1
        # 	if _interval in (4, 8): _four += 1
        # 	if _interval in (5, 7): _five += 1
        # 	if _interval == 6: _six += 1
        # for i in [_one,_two,_three,_four,_five,_six]: _intervalVector+=str(i)
        # return _intervalVector

        # _one+=_distributionSpectra.count(1)+_distributionSpectra.count(11)
        # _two += _distributionSpectra.count(2)+_distributionSpectra.count(10)
        # _three += _distributionSpectra.count(3)+_distributionSpectra.count(9)
        # _four += _distributionSpectra.count(4)+_distributionSpectra.count(8)
        # _five += _distributionSpectra.count(5)+_distributionSpectra.count(7)
        # _six += _distributionSpectra.count(6)

        _semitones = [int(i) for i in self.byWays("Step")]

        for rootNote in range(len(self)):
            for interval in self.mode(rootNote).byWays("Set"):
                interval = int(interval)
                if interval in (1, 11):
                    _one += 1
                if interval in (2, 10):
                    _two += 1
                if interval in (3, 9):
                    _three += 1
                if interval in (4, 8):
                    _four += 1
                if interval in (5, 7):
                    _five += 1
                if interval == 6:
                    _six += 1

        for i in [_one, _two, _three, _four, _five, _six]:
            if i / 2 < 10:
                _intervalVector += str(int(i / 2))
            elif i / 2 == 11:
                if convert10ToT:
                    _intervalVector += "E"
                else:
                    _intervalVector += str(int(i / 2))
            elif i / 2 == 10:
                if convert10ToT:
                    _intervalVector += "T"
                else:
                    _intervalVector += str(int(i / 2))
            _intervalVector += sep
        return _intervalVector

    def getSeptatonicInAscendingGenericIntervals(
        self, returnTrueIfIsSeptaOrNegaSexta=False
    ):
        _startingIndex = 0
        _forceOne = False
        if self.containsNotes("1"):
            if len(self.notes) != 7:
                if returnTrueIfIsSeptaOrNegaSexta:
                    return False
                else:
                    raise TypeError(
                        self, "is not septatonic! it has length ", len(self)
                    )
            else:
                if returnTrueIfIsSeptaOrNegaSexta:
                    return True
                _adjustedSelf = self
                _startingIndex = 0
        else:  # No '1'
            if len(self) == 6:
                if returnTrueIfIsSeptaOrNegaSexta:
                    return True
                _forceOne = True
                # _adjustedSelf = self.withAddedNotes('1').sortBySemitonePosition()
                _adjustedSelf = self.withAddedNotes(
                    "1"
                ).getSeptatonicInAscendingGenericIntervals()
                _startingIndex = 1
            if len(self.notes) != 6:
                if returnTrueIfIsSeptaOrNegaSexta:
                    return False
                raise TypeError(
                    self,
                    "has no 1, does not have length of 6! it has length ",
                    len(self),
                )

        _noteList = [
            note.inTermsOfScaleDegree(str(i + 1))
            for i, note in enumerate(_adjustedSelf.notes)
        ]
        # print('hooha', _adjustedSelf,_noteList);
        if not _forceOne:
            return Change(_noteList)
        else:
            return Change(_noteList[1:])

    def getDeepness(
        self, binaryResult=True
    ):  # Binary is technically opposite as 0 deepness would mean it is deep
        _distributionSpectra = self.getSpectraVariation(returnDistributionSpectra=True)
        _modesInSemitones = []
        _modeNotesInCommon = []
        _intervalVector = self.getIntervalVector()
        _intervalVectorList = []
        for i in _intervalVector:
            _intervalVectorList.append(i)
        for i in range(len(_intervalVectorList)):
            if _intervalVectorList[i] in _intervalVectorList[i + 1 :]:
                return False
        return True
        _distributionSpectra = [
            item for sublist in _distributionSpectra for item in sublist
        ]
        for i in range(len(self)):
            _modesInSemitones.append(self.modeInSemitones(i))

        for mode in range(len(_modesInSemitones)):
            # Count the number of intervals that are the size of the distance from the root
            # In the mode
            _interval = _modesInSemitones[0][
                mode
            ]  # This grabs the distance from root of the mode's root
            _modesInSemitones[mode]  # This is the mode we're checking

            _modeNotesInCommon.append(0)
            for note in _modesInSemitones[
                mode
            ]:  # Count the interval in the original scale (mode 0)
                if note in _modesInSemitones[0]:
                    _modeNotesInCommon[mode] += 1

        _modeNotesInCommon = set(_modeNotesInCommon)
        # print(self, _modeNotesInCommon, _modesInSemitones)
        # _deepness = len(self)
        # for mode in range(len(_modeNotesInCommon)):
        # 	if str(_modeNotesInCommon[mode]).count(str(mode)) > 1:
        # 		_deepness += 1
        if binaryResult:
            return len(self) - 1 - len(_modeNotesInCommon) == 0
        else:
            return len(self) - 1 - len(_modeNotesInCommon)

    def prototypeChordQuality(self):  # Work here
        # Some way to compare how many alterations from a stock chord symbol
        # Then it would pick them in some order
        # Look through some traids
        # _changeSemitones = self.modeInSemitones(0,octaveLimit=False)
        # First it will look if a 7th chord fits
        # If not it will look for a triad
        # Next it will look for a power chord

        j = JazzNote

        _noFive = True
        _triad = False
        _upperChord = False
        _seventhChord = False
        _second = False
        _third = False
        _fifth = False
        _seventh = False
        _sixth = False
        _ninth = False
        _eleventh = False

        # This will be the added notes
        chordSymbol_ = ""
        _notesToAdd = []
        _notesToRemove = []
        _notesToModify = []
        _notesRemaining = []
        for i in self.notes:
            _notesRemaining.append(i)
        _notesRemaining = Change(_notesRemaining)

        # A major third makes it major
        if len(self.notes) == 1:
            return "unison"
        # Diads will return the interval
        elif len(self.notes) == 2:
            if self.containsNotes("b2"):
                return "mi 2nd"
            if self.containsNotes("2"):
                return "ma 2nd"
            if self.containsNotes("b3", byAnotherName=False):
                return "mi 3rd"
            if self.containsNotes("#2", byAnotherName=False):
                return "aug 2nd"
            if self.containsNotes("3"):
                return "ma 3rd"
            if self.containsNotes("4"):
                return "p 4th"
            if self.containsNotes("#4", byAnotherName=False):
                return "aug 4th"
            if self.containsNotes("b5", byAnotherName=False):
                return "dim 5th"
            if self.containsNotes("5"):
                return "p 5th"
            if self.containsNotes("b6", byAnotherName=False):
                return "mi 6th"
            if self.containsNotes("#5", byAnotherName=False):
                return "aug 5th"
            if self.containsNotes("6"):
                return "ma 6th"
            if self.containsNotes("#6", byAnotherName=False):
                return "aug 6th"
            if self.containsNotes("b7", byAnotherName=False):
                return "mi 7th"
            if self.containsNotes("7"):
                return "ma 7th"

        # Check about the "5"
        if self.containsNotes("5"):
            _fifth = "5"
            # _notesRemaining = _notesRemaining.withoutNote('5')
            if self.containsNotes("#4"):
                pass
            # _notesToAdd.append('#4')
            # _notesRemaining = _notesRemaining.withoutNote('#4')
            if self.containsNotes("b6"):
                pass
            # _notesToAdd.append('b6')
            # _notesRemaining = _notesRemaining.withoutNote('b6')
        if self.containsNotes("#5") and not _fifth:
            _fifth = "#5"
            _notesToModify.append("#5")

        if self.containsNotes("b5"):
            if not _fifth:
                _fifth = "b5"
                _notesToModify.append("b5")
                _notesRemaining = _notesRemaining.withoutNote("b5")

        if not _fifth:
            _notesToRemove.append("5")

        # Check about the triadic third
        if self.containsNotes("3"):
            _third = "3"
            # _notesRemaining = _notesRemaining.withoutNote('3')
            # If it also has the b3 then that is a sharp two
        if self.containsNotes("b3") and not _third:
            _third = "b3"

        if self.containsNotes("4") and not _third:
            _third = "4"
        if self.containsNotes("2") and not _third:
            _third = "2"
        if self.containsNotes("#4") and not _third:
            if _fifth != "b5":
                _third = "#4"
        if self.containsNotes("b2"):
            if not _third:
                _third = "b2"
        if not _third:
            _notesToRemove.append("3")

        # Check out the seventh
        if self.containsNotes("7"):
            _seventh = "7"
        if self.containsNotes("b7") and not _seventh:
            _seventh = "b7"
        # Check out the six
        if self.containsNotes("6"):
            _sixth = "6"

        if _notesRemaining.containsNotes("1"):
            _notesRemaining = _notesRemaining.withoutNote("1")
        # Assign a triad

        if _third == "3":
            _triad = "ma"
            _notesRemaining = _notesRemaining.withoutNote("3")

        elif _third == "b3":
            _triad = "mi"
            if _fifth == "b5":
                _triad = "dim"
                if _seventh == "b7":
                    _triad = "halfdim"
        elif _third == "4":
            _triad = "sus4"
        elif _third == "2":
            _triad = "sus2"
            _notesRemaining = _notesRemaining.withoutNote("2")
        elif _third == "#4":
            _triad = "sus#4"
        elif _third == "b2":
            _triad = "susb2"
        if _fifth == "#5":
            _notesToModify.append("#5")
            # _triad = 'aug'
        elif _fifth == "5":
            pass
        elif _fifth == "b5":
            _notesToModify.append("b5")
        elif not _fifth:
            _notesToRemove.append("5")

        if _third:
            _notesRemaining = _notesRemaining.withoutNote(_third)
        elif not _third:
            _notesToRemove.append("3")
        if _fifth:
            _notesRemaining = _notesRemaining.withoutNote(_fifth)
        elif not _fifth:
            _notesToRemove.append("5")

        if not _triad:
            if _fifth == "5":
                if not _sixth and not _seventh:
                    _triad = _fifth

        # grab the ninth
        if self.containsNotes("2") and not _third == "2":
            _ninth = "9"
        if not _ninth and self.containsNotes("b2") and not _third == "b2":
            _ninth = "b9"
        if not _ninth and self.containsNotes("#2") and not _third == "#2":
            _ninth = "#9"
        # grab the eleventh
        if self.containsNotes("4") and not _third == "4":
            _eleventh = "11"
        if (
            not _eleventh
            and self.containsNotes("#4")
            and not _third == "#4"
            and not _fifth == "b5"
        ):
            _eleventh = "#11"
        # grab the thirteen call it the sixth
        if self.containsNotes("6"):
            _sixth = "6"
        # if self.containsNotes('b6') and not _fifth == '#5' and not _sixth:
        # 	_sixth = 'b6'

        # Build seventh, ninth, eleventh, thirteenth chord from triad plus 7th
        _upperChords = []
        _upperChordExceptions = []
        if _seventh:
            _upperChords.append(_seventh)
            _notesRemaining = _notesRemaining.withoutNote(_seventh)
            _upperChordExceptions.append(len(_notesRemaining) + len(_notesToRemove))
        if _ninth == "9":
            _upperChords.append("9")
            _notesRemaining = _notesRemaining.withoutNote(_ninth)
            _upperChordExceptions.append(len(_notesRemaining) + len(_notesToRemove))
        if _eleventh == "11":
            _upperChords.append("11")
            _notesRemaining = _notesRemaining.withoutNote(_eleventh)
            _upperChordExceptions.append(len(_notesRemaining) + len(_notesToRemove))
        if _sixth == "6":
            _upperChords.append("13")
            _notesRemaining = _notesRemaining.withoutNote(_sixth)
            _upperChordExceptions.append(len(_notesRemaining) + len(_notesToRemove))
        # Find the shortest one
        if len(_upperChords) > 0:
            _upperChord = _upperChords[
                _upperChordExceptions.index(min(_upperChordExceptions))
            ]

        if type(_triad) == str:
            if _upperChord:
                if _triad == "ma":
                    _chordSymbol += _upperChord
                elif "sus" in _triad:
                    _chordSymbol += _upperChord
                    # if _sixth: _chordSymbol += _sixth
                    _chordSymbol += _triad
                else:
                    _chordSymbol += _triad
                    if _triad == "dim":
                        if _seventh == "b7":
                            _triad = "halfdim"

                    _chordSymbol += _upperChord

            else:  # Not a seventh chord

                if _sixth and "sus" in _triad:
                    _chordSymbol += _sixth + _triad
                else:
                    _chordSymbol += _triad
                    if _sixth:
                        _chordSymbol += _sixth
        elif not _triad:
            if _seventhChord:
                _chordSymbol += _seventhChord
            elif _sixth:
                _chordSymbol += _sixth

        # 			else:
        # 				_chordSymbol += _triad
        # Check for b2 if not a sus b2
        if not _triad == "susb2":
            if self.containsNotes("b2"):
                if _seventhChord:
                    _notesToAdd.append("b9")
                else:
                    _notesToAdd.append("b2")
        if not _triad == "sus2":
            if self.containsNotes("2"):
                if _seventhChord:
                    _notesToAdd.append("9")
                else:
                    _notesToAdd.append("2")
        if not _triad == "sus4":
            if self.containsNotes("4"):
                if _seventhChord:
                    if "11" or "4" not in _notesToAdd:
                        _notesToAdd.append("11")
                else:
                    _notesToAdd.append("4")
        if not (_triad == "sus#4" or _triad == "dim" or _fifth == "b5"):
            if self.containsNotes("#4"):
                if _seventhChord:
                    _notesToAdd.append("#11")
                else:
                    if not "#4" in _notesToAdd:
                        _notesToAdd.append("#4")

        # print('seventhChord', _seventhChord, 'notesToAdd',_notesToAdd,'notesToRemove',_notesToRemove,'remaining notes', _notesRemaining)
        # Find the least modifications in chord symbol

        if _notesToAdd or _notesToRemove or _notesToModify:
            _chordSymbol += "("
            if _notesToModify:

                for note in range(len(_notesToModify)):
                    _chordSymbol += _notesToModify[note]
                    if note != len(_notesToModify) - 1:
                        _chordSymbol += ","
            if _notesToAdd:
                if _notesToModify:
                    _chordSymbol += ", "

                _chordSymbol += "add "
                for note in range(len(_notesToAdd)):
                    _chordSymbol += _notesToAdd[note]
                    if note != len(_notesToAdd) - 1:
                        _chordSymbol += ","
            if _notesToRemove:
                if _notesToAdd or _notesToModify:
                    _chordSymbol += ", "
                _chordSymbol += "no "
                for note in range(len(_notesToRemove)):
                    _chordSymbol += _notesToRemove[note]
                    if note != len(_notesToRemove) - 1:
                        _chordSymbol += ","
            _chordSymbol += ")"
        _chordSymbol = _chordSymbol.replace("#", "♯")
        _chordSymbol = _chordSymbol.replace("b", "♭")
        _chordSymbol = _chordSymbol.replace("dim", "°")  # oᴼ
        _chordSymbol = _chordSymbol.replace("halfdim", "⌀")
        # print('triad: ',_triad,'seventhChord: ', _seventhChord,'notesRemaining: ', _notesRemaining,'third: ',_third,'fifth: ',_fifth, 'seventh:',_seventh, 'sixth',_sixth, sep = '\n',end ='\n')
        return _chordSymbol

    def getRelatedScaleNames(self):
        return self.getWillSmithNames(
            useFullScaleNames=True,
            spellAccidentals=False,
            useBracketsAroundAccidentals=True,
        )

    def getWillSmithName(
        self,
        useFullScaleNames=False,
        spellAccidentals=True,
        useBracketsAroundAccidentals=False,
    ):
        output = ""
        changePrefixes = {
            # 7-Note
            "1361": {"prefix": "Majo", "prefixAlt": "Maj"},
            "1325": {"prefix": "Dori", "prefixAlt": "Dor"},
            "1197": {"prefix": "Phrygi", "prefixAlt": "Phryg"},
            "1371": {"prefix": "Lydi", "prefixAlt": "Lyd"},
            "1360": {"prefix": "Mixo", "prefixAlt": "Mix"},
            "1323": {"prefix": "Aeo", "prefixAlt": "A"},
            "1191": {"prefix": "Locri", "prefixAlt": "Loc"},
            "1326": {"prefix": "Jazzo", "prefixAlt": "Jazz"},
            "1171": {"prefix": "Alto", "prefixAlt": "Alt"},
            "1370": {"prefix": "Ovo", "prefixAlt": "Ov"},
            "1405": {"prefix": "Bluesi", "prefixAlt": "Blue"},
            # 8-Note
            "1739": {"prefix": "Dimi", "prefixAlt": "Dim"},
            "1636": {"prefix": "DimDomi", "prefixAlt": "DimDom"},
            "1766": {"prefix": "Bopi", "prefixAlt": "Bop"},
            "1764": {"prefix": "BopMaji", "prefixAlt": "BopMaj"},
        }
        accidentalStrs = {
            "-1": "flat",
            "1": "sharp",
            "-2": "dim",
            "2": "aug",
            "0": "nat",
        }

        def dstToAccStr(dst: int):
            d = dst
            if d == 0:
                return accidentalStrs["0"]
            dir = 1 if d > 0 else -1
            output = ""
            while abs(d) > 1:
                output += accidentalStrs[str(2 * dir)]
                d -= 2 * dir
            if abs(d) == 1:
                output += accidentalStrs[str(dir)]
                d -= dir

            return output

        if len(self) == 7 and self.containsNotes("1"):
            pass
        else:
            return False
        # Chromatic Septachord: Phryg Dim 3 4 Dim Flat 5 Dim Dim 6 Dim Dim b7
        # Every time there's an aug == ##, dim == bb
        straightenedChange = []
        for n in range(7):
            scaleDegree = str(n + 1)
            note = self[n].inTermsOfScaleDegree(scaleDegree)
            straightenedChange.append(note)

        straightenedChange = Change(straightenedChange)

        modeScores = []
        modes = [Change.makeFromChangeNumber(int(c)) for c in changePrefixes.keys()]
        # input('asdfhjasdf {}'.format(modes))

        for m in range(len(modes)):
            modeScores.append(0)
            mode = modes[m]
            for n in range(len(self)):
                refDist = JazzNote.accidentalsToDistance(str(mode[n]))
                dist = JazzNote.accidentalsToDistance(str(straightenedChange[n]))
                # print(mode[n],refDist, dist)
                modeScores[-1] += abs(dist - refDist)
            # print(m,mode)
        lowestScore = min(modeScores)
        bestMode = modes[modeScores.index(lowestScore)]

        for n in range(len(self)):
            changeNote = straightenedChange[n]
            modeNote = bestMode[n]
            modeNoteDst = JazzNote.accidentalsToDistance(str(modeNote))

            changeNoteDst = JazzNote.accidentalsToDistance(str(changeNote))
            dst = changeNoteDst - modeNoteDst
            if dst != 0:
                if spellAccidentals:
                    output += dstToAccStr(changeNoteDst)
                else:

                    output += " "
                    if changeNoteDst == 0:
                        output += Unicode.chars["Natural"]
                    else:
                        output += JazzNote.numberOfAccidentalsToAccidentalsString(
                            changeNoteDst
                        )
                output += modeNote.scaleDegree()
                """input('seee it {}  {}  s.d. {}\n{} --- {} \n{} --- {}'.format(
                    bestMode,
                    modeNoteDst - changeNoteDst, modeNote.scaleDegree(),
                    modeNote,modeNoteDst,
                    changeNote,changeNoteDst,
                ))"""
        # input('{}'.format(output))
        if useBracketsAroundAccidentals:
            output = "(" + output + ")"

        if useFullScaleNames:
            output = bestMode.getScaleNames()[0] + output
        else:
            if any(c.isnumeric() for c in output):
                # if any([[c for c in i] in [str(j) for j in [range(10)]] for i in output]):
                output = (
                    changePrefixes[str(bestMode.getChangeNumber())]["prefix"] + output
                )
            else:
                output = (
                    changePrefixes[str(bestMode.getChangeNumber())]["prefixAlt"]
                    + output
                )
        # input('modeScores {} best {}'.format(
        #    modeScores,bestMode))
        return output
        # return ' '.join([str(i) for i in self.getSemitones()])

    def getWillSmithNames(
        self,
        useFullScaleNames=False,
        spellAccidentals=True,
        useBracketsAroundAccidentals=False,
        useUnicodeAccidentals=True,
        maxMods=1
    ):
        callerParameters = locals()

        if "Will Smith Name" not in Change.cache.keys():
            Change.cache["Will Smith Name"] = {}
        try:
            return Change.cache["Will Smith Name"][str(callerParameters)]
        except KeyError:
            pass

        # output = ''
        outputs = []
        changePrefixes = WillSmithIdeas.changePrefixes

        if str(len(self)) not in changePrefixes.keys():
            warnings.warn(
                str(len(self))
                + " not in "
                + str(changePrefixes)
                + " and so skipping getWillSmithNames() for change "
                + str(self.getChangeNumber())
            )
        accidentalStrs = {
            "-1": "flat",
            "1": "sharp",
            "-2": "dim",
            "2": "aug",
            "0": "nat",
        }

        def dstToAccStr(dst: int):
            d = dst
            if d == 0:
                return accidentalStrs["0"]
            dir = 1 if d > 0 else -1
            output = ""
            while abs(d) > 1:
                output += accidentalStrs[str(2 * dir)]
                d -= 2 * dir
            if abs(d) == 1:
                output += accidentalStrs[str(dir)]
                d -= dir

            return output

        # Chromatic Septachord: Phryg Dim 3 4 Dim Flat 5 Dim Dim 6 Dim Dim b7
        # Every time there's an aug == ##, dim == bb

        straightenedChange = self.straightenDegrees(
            allowedNotes=Change.allowedNoteNamesFiveAccidentals
        )

        modeScores = []
        try:
            modes = [
                Change.makeFromChangeNumber(int(c)).straightenDegrees(
                    allowedNotes=Change.allowedNoteNamesFiveAccidentals
                )
                for c in changePrefixes[str(len(self))].keys()
            ]
        except KeyError:
            return []
        # input('asdfhjasdf {}'.format(modes))
        for m in range(len(modes)):
            modeScores.append(0)
            mode = modes[m]
            for n in range(len(self)):
                if (
                    mode[n].semitonesFromOne()
                    != straightenedChange[n].semitonesFromOne()
                ):
                    modeScores[-1] += 1

                """
                refDist = JazzNote.accidentalsToDistance(str(mode[n]))
                dist = JazzNote.accidentalsToDistance(str(straightenedChange[n]))
                diff = abs(abs(dist) - abs(refDist))if diff == 0:
                    pass#print(str(mode[n]))
                    #input(str(straightenedChange[n]))
                elif diff == 1:
                    modeScores[-1] += 1
                elif diff == 2:
                    modeScores[-1] += 1
                elif diff == 3:
                    modeScores[-1] += 1
                """
                # print(mode[n], straightenedChange[n], refDist, dist,diff)
                # modeScores[-1] += abs(dist - refDist)
            if modeScores[-1] == 0:
                modeScores[-1] = 99
            # print(m,mode)

        lowestScore = min(modeScores)
        candidateIndexes = [
            i for i in range(len(modeScores)) if modeScores[i] == lowestScore and modeScores[i] <= maxMods
        ]

        for candidateIndex in candidateIndexes:
            outputs.append("")
            candidate = modes[candidateIndex]
            for noteIdx in range(len(self)):

                modeNote: JazzNote = candidate[noteIdx]
                changeNote: JazzNote = straightenedChange[noteIdx].inTermsOfScaleDegree(
                    modeNote
                )
                modeNoteDst = JazzNote.accidentalsToDistance(str(modeNote))
                changeNoteDst = JazzNote.accidentalsToDistance(str(changeNote))
                # modeNoteDst = modeNote.semitonesFromOne()
                # changeNoteDst = changeNote.semitonesFromOne()

                dst = changeNoteDst - modeNoteDst
                if modeNote.scaleDegree() != changeNote.scaleDegree():
                    changeNoteDst += 0
                if dst != 0:
                    if spellAccidentals:
                        outputs[-1] += dstToAccStr(changeNoteDst)
                    else:
                        if noteIdx != 0:
                            outputs[-1] += " "
                        if changeNoteDst == 0:
                            outputs[-1] += Unicode.chars["Natural"]
                        else:
                            outputs[
                                -1
                            ] += JazzNote.numberOfAccidentalsToAccidentalsString(
                                changeNoteDst
                            )
                    outputs[-1] += modeNote.scaleDegree()

                    """input('\nseeee it. \nself: {}\nCandidate: {}\n modeNoteDst - changeNoteDst: {}\n  scale deg. {}\nmodeNote: {} --- modeNoteDst: {} \nchangeNote{} --- changeNoteDst: {}'.format(
                        self,
                        candidate.__repr__(),
                        modeNoteDst - changeNoteDst, 
                        modeNote.scaleDegree(),
                        modeNote,modeNoteDst,
                        changeNote,changeNoteDst,
                    ))"""
            # input('{}'.format(output))
            if useBracketsAroundAccidentals:
                if len(outputs[-1]) > 0:
                    if outputs[-1][0] == " ":
                        outputs[-1] = outputs[-1][1:]
                    outputs[-1] = " (" + outputs[-1] + ")"

            if useFullScaleNames:
                outputs[-1] = candidate.getScaleNames()[0] + outputs[-1]
            else:
                if any(c.isnumeric() for c in output):
                    # if any([[c for c in i] in [str(j) for j in [range(10)]] for i in output]):
                    outputs[-1] = (
                        changePrefixes[str(bestMode.getChangeNumber())]["prefix"]
                        + output
                    )
                else:
                    outputs[-1] = (
                        changePrefixes[str(bestMode.getChangeNumber())]["prefixAlt"]
                        + output
                    )
            # input('modeScores {} best {}'.format(
            #    modeScores[candidateIndex],candidate))
            if useUnicodeAccidentals:
                outputs[-1] = outputs[-1].replace("#", "♯")
                outputs[-1] = outputs[-1].replace("b", "♭")

        # assert len(outputs) < 3, str(outputs) + '\n' + str(modeScores) + ' ' + str([i.getScaleNames()[0] for i in modes])
        Change.cache["Will Smith Name"][str(callerParameters)] = outputs
        return outputs
        # return ' '.join([str(i) for i in self.getSemitones()])

    def getScaleNames(
        self,
        defaultWay="Hexagram Name",
        searchForDownward=False,
        searchForNegative=False,
        includeDownwardHexagram=False,
        relateToMainScales=True,
        rebindRootToNextNoteIfNoOne=True,
        replaceDirectionStrWithUnicode=True,
        encloseNamesInCurlies=False,
        includeZodiac=False,
        replaceCarnaticNamesWithSymbols=True,
    ):
        try:
            ScaleNames
        except NameError:
            from ScaleNames import ScaleNames
        _forceOne = False
        _rebindedName = ""
        if len(self.notes) == 0:
            if defaultWay != False:
                _rebindedName = self.byWays(defaultWay)
                # input(_rebindedName)
            if _rebindedName not in ("", " "):
                return [_rebindedName]
            else:
                return ["Silence"]
        if not self.containsNotes("1"):
            # print('This Change doesn\'t have a 1           ',self)
            _adjustedSelf = Change.makeFromSet([0] + self.getSemitones())

            _inSemitones = sorted(_adjustedSelf.getSemitones())
            _forceOne = True
            _attemptedRebinding = self.getNormalForm().getScaleNames(
                searchForDownward=False,
                searchForNegative=False,
                includeDownwardHexagram=False,
            )[0]
            if rebindRootToNextNoteIfNoOne and _forceOne:
                if self.getNormalForm().getHexagramName() not in _attemptedRebinding:
                    # print('this one should have a 1            ',self.getNormalForm(),self,sep=' ,')
                    _rebindedName = (
                        _attemptedRebinding + " (on " + str(self.notes[0]) + ")"
                    )
                else:
                    _rebindedName = self.getHexagramName()

        elif self.containsNotes("1"):
            _inSemitones = self.byWays("Set")
            _adjustedSelf = self

        for i in range(len(_inSemitones)):
            _inSemitones[i] = int(_inSemitones[i])
        # This is probably slow but I can't figure it out yet.
        _indexNumber = list(ScaleNames.semitonesBySequenceIndex).index(_inSemitones)
        # _indexNumber = np.where(ScaleNames.semitonesBySequenceIndex == _inSemitones)
        # _indexNumber = np.where(np.array_equal(ScaleNames.semitonesBySequenceIndex, _inSemitones))

        _name = ""
        _name = ScaleNames.namesBySequenceIndex[_indexNumber]
        if relateToMainScales:
            # for mainScale in Book.mainScales:
            pass

        if rebindRootToNextNoteIfNoOne == True and _forceOne == True:
            _name = _rebindedName + "," + _name
        # if _forceOne and _name != '': _name += '(no 1)'
        _downwardName = ""
        _negativeName = ""

        _allnames = []

        if searchForDownward:
            _downwardInSemitones = _adjustedSelf.getReverse().byWays("Set")
            for i in range(len(_downwardInSemitones)):
                _downwardInSemitones[i] = int(_downwardInSemitones[i])
            _downwardIndexNumber = ScaleNames.semitonesBySequenceIndex.index(
                _downwardInSemitones
            )
            _downwardName = ScaleNames.namesBySequenceIndex[_downwardIndexNumber]

            if (
                _downwardName == "" and includeDownwardHexagram
            ):  # If there is a negative hexagram
                _downwardName = _adjustedSelf.getReverse().getScaleNames(
                    defaultWay="Hexagram Name",
                    searchForDownward=False,
                    searchForNegative=False,
                    includeDownwardHexagram=False,
                )[0]
            if _forceOne:
                _downwardIndexNumber *= -1

        if searchForNegative:
            _negativeInSemitones = self.getInverse().byWays("Set")
            for i in range(len(_negativeInSemitones)):
                _negativeInSemitones[i] = int(_negativeInSemitones[i])
            if not 0 in _negativeInSemitones:
                _negativeInSemitones.insert(0, 0)
            if _forceOne:
                _negativeInSemitones = _adjustedSelf.getSemitones()  # here
            _negativeIndexNumber = ScaleNames.semitonesBySequenceIndex.index(
                _negativeInSemitones
            )
            _negativeName = ScaleNames.namesBySequenceIndex[_negativeIndexNumber]
            if _negativeName == "":
                _negativeName = self.getInverse().getScaleNames(
                    defaultWay="Hexagram Name",
                    searchForDownward=False,
                    searchForNegative=False,
                    includeDownwardHexagram=False,
                )[0]
            if _forceOne:
                _negativeIndexNumber *= -1

        if len(_name) > 0:  # There is a name (or more)
            # Add part where it shows modes of
            # Add part about the downward scale

            _allnames.extend(_name.split(","))
        if _downwardName != "" and searchForDownward == True:
            if "," in _downwardName:
                _downwardName = _downwardName.split(",")[0]
            _allnames.append("↓" + "🐛" + _downwardName)  # ↘↧
        if _negativeName != "" and searchForNegative == True:
            if "," in _negativeName:
                _negativeName = _negativeName.split(",")[0]
            _allnames.append("☯≠" + _negativeName + "")
            # √∉✗➗✋❎⚞Ⓧ⌗⌗↓≠∌✌∄-
        if _rebindedName != "":
            if type(_rebindedName) == list:
                _allnames.append(" ".join(_rebindedName))
            else:
                _allnames.append(_rebindedName)
        if _allnames == [] and not defaultWay == False:
            _defaultName = self.byWays(defaultWay)
            if type(_defaultName) == list:
                _allnames = ["".join(_defaultName)]
            else:
                _allnames = [_defaultName]

        # print('in get scale name, allnames: ',_allnames)
        # Prune out newlines and tabs
        for i in range(len(_allnames)):
            if (
                _forceOne == True
                and _allnames[i] != _rebindedName
                and _rebindedName not in ("", " ")
            ):
                _allnames[i] = _allnames[i] + " (no 1)"
            _allnames[i] = _allnames[i].replace("\t", "")
            _allnames[i] = _allnames[i].replace("\n", "")

        if replaceDirectionStrWithUnicode == True:
            _allnames = [
                n.replace(" (ascending)", " " + Unicode.chars["Ascending"])
                for n in _allnames
            ]
            _allnames = [
                n.replace(" (descending)", " " + Unicode.chars["Descending"])
                for n in _allnames
            ]
        else:
            _allnames = [n.replace(" (ascending)", " Asc.") for n in _allnames]
            _allnames = [n.replace(" (descending)", " Desc.") for n in _allnames]
        if encloseNamesInCurlies == True:
            _allnames = ["{" + i + "}" for i in _allnames]
        if replaceCarnaticNamesWithSymbols:
            _allnames = [
                n.replace("Mela ", Unicode.chars["Mela"] + " ") for n in _allnames
            ]
            _allnames = [
                n.replace("Raga ",Unicode.chars["Raga"] + " ") for n in _allnames
            ]
        if includeZodiac:
            _allnames = _allnames + ["".join(self.byWays("Zodiac"))]

        return _allnames

    def getRhythm(
        self, straightenToSubdivision=[3, 3, 3, 3], showDebug=False, combinatoricSize=12
    ):  # Cause we got the funk
        # 𝄾 𝄽 𝄼 𝄻 𝄾 𝅘𝅥𝅯.
        # TODO: implement straightenToSubdivision

        _inSemitoneSteps = [int(self.byWays("Step")[i]) for i in range(len(self.notes))]
        _wholeNotesOnIndex = []
        _halfNotesOnIndex = []
        _quarterNotesOnIndex = []
        _eighthNotesOnIndex = []
        _changeInRhythms = []
        _rhythmicNoteSymbols = (
            # Unicode.chars['Whole Note'], Unicode.chars['Half Note'], Unicode.chars['Quarter Note'],
            # Unicode.chars['Eighth Note']
            "W",
            "H",
            Unicode.chars["Quarter Note"],
            Unicode.chars["Eighth Note"],
        )
        # 𝆹 𝆺 𝆹𝅥 𝆺𝅥 𝆹𝅥𝅮 𝆺𝅥𝅮 𝆹𝅥𝅯 𝆺𝅥𝅯

        _rhythmicRestSymbols = (
            "w",
            "h",
            "q",
            "e"
            # Unicode.chars['Whole Rest'], Unicode.chars['Half Rest'], Unicode.chars['Quarter Rest'],
            # Unicode.chars['Eighth Rest']
        )
        for stepValue in _inSemitoneSteps:
            _step = stepValue
            _wholeNotes = math.floor(_step / 8)
            _step -= _wholeNotes * 8
            _halfNotes = math.floor(_step / 4)
            _step -= _halfNotes * 4
            _quarterNotes = math.floor(_step / 2)
            _step -= _quarterNotes * 2
            _eighthNotes = _step
            _wholeNotesOnIndex.append(_wholeNotes)
            if showDebug:
                _halfNotesOnIndex.append(_halfNotes)
                _quarterNotesOnIndex.append(_quarterNotes)
                _eighthNotesOnIndex.append(_eighthNotes)
            _makeValueARest = False
            _changeInRhythms.append("")
            for index, item in enumerate(
                [_wholeNotes, _halfNotes, _quarterNotes, _eighthNotes]
            ):
                if item != 0:
                    if not _makeValueARest:
                        _makeValueARest = True
                        _changeInRhythms[-1] += _rhythmicNoteSymbols[index] * item
                        _checkIndexForDot = index + 1
                    elif _makeValueARest == True and index == _checkIndexForDot:
                        _changeInRhythms[-1] += "."
                    else:
                        _changeInRhythms[-1] += _rhythmicRestSymbols[index] * item
        if showDebug:
            print(
                "in get rhythm 𝅝: ",
                _wholeNotesOnIndex,
                "𝅗𝅥:",
                _halfNotesOnIndex,
                "𝅘𝅥:",
                _quarterNotesOnIndex,
                "♪:",
                _eighthNotesOnIndex,
            )
        return _changeInRhythms

    def getReverse(self):
        if self == Change([]):
            return self
        _inSemitoneSteps = [int(self.byWays("Set")[i]) for i in range(len(self.notes))]
        _downwardSemitoneSteps = []
        for i in range(len(_inSemitoneSteps)):
            _downwardSemitoneSteps.append((12 - _inSemitoneSteps[-i]) % 12)

        _newNotes = []
        for i in _downwardSemitoneSteps:
            _newNotes.append(JazzNote.makeFromSet(i))
        return Change(_newNotes).sortBySemitonePosition()

    def getColourGrid(self, adjustToKey="C", adjustBySemitones=0):
        if not JazzNote.isAlphabetNoteStr(adjustToKey):
            raise TypeError("supposed to be alphabetstr not", type(adjustToKey))
        if not type(adjustBySemitones) == int:
            raise TypeError("supposed to be int, not ", type(adjustBySemitones))
        # Consolidate adjustment into the int ajustBysemitones
        adjustBySemitones += JazzNote.distanceFromC(adjustToKey)
        _set = [int(i) for i in self.byWays("Set")]
        _set = [(st + adjustBySemitones) % 12 for st in _set]
        return [Colour.rgbByDistance[i] for i in _set]

    def getColouredSelf(self, adjustBySemitones=0):

        # input('inside getColouredSelf')
        # return Latex.makeDataColoured(_strSelf,makeTextColoured=self.getSemitones(),adjustBySemitones=adjustBySemitones+Book.colourTranspose)
        return self.returnColouredLatex(
            self.notes,
            "Jazz",
        )

    def returnColouredLatex(
        self, changeByWay, way, adjustBySemitones=0, colourType=None
    ):
        """Tag every item of changeByWay with the makeTextColoured that correspond with self, using LaTeX tags"""

        # Set the colour type (box or text) and the shade of colour (light or dark)
        if colourType in Latex.colourTypes:
            pass
        elif colourType is None:
            if Latex.inkSaver:
                colourType = "Colour Text"
                if Latex.blackPaper:
                    darkColours = False
                elif not Latex.blackPaper:
                    darkColours = True
            else:
                colourType = "Colour Cell"
                if Latex.blackPaper:
                    darkColours = True
                elif not Latex.blackPaper:
                    darkColours = False
        else:
            raise ValueError("invalid colourType", Latex.colourTypes)
        if darkColours == True:
            _nameByDistanceLightness = Colour.nameByDistanceDk
        elif darkColours == False:
            _nameByDistanceLightness = Colour.nameByDistanceLt

        if way in Book.colouredWaysSpecific:
            if "Changed Note" in way:
                return [
                    Latex.commandStrings[colourType]
                    + _nameByDistanceLightness[
                        (n + adjustBySemitones) % len(_nameByDistanceLightness)
                    ]
                    + "}{"
                    + str(changeByWay[n])
                    + "}"
                    for n in range(12)
                ]
            if "Zodiac" in way:
                return [
                    Latex.commandStrings[colourType]
                    + _nameByDistanceLightness[
                        (n + adjustBySemitones) % len(_nameByDistanceLightness)
                    ]
                    + "}{"
                    + str(changeByWay[n])
                    + "}"
                    for n in range(len(changeByWay))
                ]

            elif way == "Add Note":
                ___r = [
                    Latex.commandStrings[colourType]
                    + _nameByDistanceLightness[
                        (self.getInverse()[n].semitonesFromOne() + adjustBySemitones)
                        % len(_nameByDistanceLightness)
                    ]
                    + "}{"
                    + str(changeByWay[n])
                    + "}"
                    for n in range(len(self.getInverse().notes))
                ]
                # input(str(self)+' it happened again'+str(___r))
                return [
                    Latex.commandStrings[colourType]
                    + _nameByDistanceLightness[
                        (self.getInverse()[n].semitonesFromOne() + adjustBySemitones)
                        % len(_nameByDistanceLightness)
                    ]
                    + "}{"
                    + str(changeByWay[n])
                    + "}"
                    for n in range(len(self.getInverse().notes))
                ]

        # Check whether way is valid
        elif way in Book.colouredWaysPositional:
            if not len(changeByWay) == len(self.notes):
                raise ValueError(
                    "Colouring lists works when the list has the same length as the change that the makeTextColoured are being derived from "
                    + str(len(self.notes))
                    + "  "
                    + str(len(changeByWay))
                    + "  "
                    + str(self.notes)
                    + str(changeByWay),
                    way,
                )

            if not type(changeByWay) in (list, np.ndarray):
                raise TypeError(
                    "changeByWay is expected to be a list, not", type(changeByWay)
                )

            return [
                Latex.commandStrings[colourType]
                + _nameByDistanceLightness[
                    (self[n].semitonesFromOne() + adjustBySemitones)
                    % len(_nameByDistanceLightness)
                ]
                + "}{"
                + str(changeByWay[n])
                + "}"
                for n in range(len(self.notes))
            ]

        else:
            raise ValueError(way + " not in coloured ways.")

    def getWord(
        self,
        specificInterval=None,
        insertStrBetweenConsonantAndWord="",
        capitaliseConsonant=True,
        capitaliseSyllable=False,
        colourResult=False,
        showDebug=False,
        useTextStyledByWay=False
    ) -> list:

        # ’
        if not specificInterval is None:
            _consonant = JazzNote.numberToConsonant[specificInterval]
            if capitaliseConsonant == True:
                _consonant = _consonant.upper()
            else:
                _consonant = _consonant.lower()

        _syllable = self.getTrigram(
            ["syllable"],
            colourResult=colourResult,
            colourExtraTranspose=specificInterval,
        )

        if type(_syllable) == list:
            _syllable = "".join(_syllable)
        if showDebug:
            print(_consonant + _syllable)
        # TODO: Come back spaceman, put this stuff in trigram
        """if capitaliseConsonant == True:
            _consonant = _consonant.upper()
        else:
            _consonant = _consonant.lower()
        if capitaliseSyllable == True:
            _syllable = _syllable.capitalize()
        else:
            _syllable = _syllable.lower()"""
        if colourResult:
            pass  # _consonant = Latex.makeDataColoured(_consonant, specificInterval + Book.colourTranspose)
        if specificInterval == None:
            _str = _syllable
        else:
            _str = _consonant + insertStrBetweenConsonantAndWord + _syllable
        if useTextStyledByWay:
            _str = Latex.makeTextStyledByWay(_str,'Word')
        return _str

    def getConsonant(self, returnWrittenPoem=False):
        if len(self) == 0:
            return []
        if returnWrittenPoem:
            _consonants = ScaleNames.poemBySequenceIndex[
                abs(self.getChangeNumber(decorateChapter=False))
            ].split(" ")
            if not self.containsNotes("1"):
                _consonants = ScaleNames.poemBySequenceIndexNegative
        else:
            _consonants = [
                JazzNote.numberToConsonant[i.semitonesFromOne()] for i in self.notes
            ]

        return _consonants

    def getInverse(self):
        if len(self) == 0:
            return self
        _inSemitoneSteps = [int(self.byWays("Set")[i]) for i in range(len(self.notes))]
        _negativeSemitoneSteps = []
        _negativeNotes = []
        for i in range(12):
            if not i in _inSemitoneSteps:
                _negativeSemitoneSteps.append(i)
        for i in _negativeSemitoneSteps:
            _negativeNotes.append(JazzNote.makeFromSet(i))

        return Change(_negativeNotes)

    def getTritoneSub(
        self,
    ):
        _semitones = [int(i) for i in self.byWays("Set")]
        for idx, i in enumerate(_semitones):
            if i < 6:
                _semitones[idx] += 6
            elif i >= 6:
                _semitones[idx] -= 6
        _semitones.sort()
        return Change.makeFromSet(_semitones)

        _halfScales = self.divideScaleBy(
            denominator=2, normaliseToSlice=False, returnChromatically=False
        )
        _halfScalesSemitones = []
        for h, halfScale in enumerate(_halfScales):
            _halfScalesSemitones.append([i.semitonesFromOne() for i in halfScale])
        # This will only work with Changes of 12 notesets
        _halfScalesSemitones[0] = [i + 6 for i in _halfScalesSemitones[0]]
        _halfScalesSemitones[1] = [i - 6 for i in _halfScalesSemitones[1]]
        input(
            str(self)
            + " stand up tritone "
            + str(_halfScalesSemitones)
            + str(_halfScalesSemitones[1] + _halfScalesSemitones[0])
            + str(Change.makeFromSet(_halfScalesSemitones[1] + _halfScalesSemitones[0]))
        )
        return Change.makeFromSet(_halfScalesSemitones[1] + _halfScalesSemitones[0])




    def getChordQuality(
        self,
        useWeirdSusSymbols=None,
        useAugmentedChords=None,
        useAugUnicodeSymbol=None,
        useHalfDiminishedChords=None,
        useHalfDiminishedUnicodeSymbols=None,
        useDiminishedUnicodeSymbols=None,
        useMa7Triangle=None,
        capitaliseMajor=None,
        printDebugInfo=None,
        useSixNines=None,
        createPolychordIfNoOne=None,
        moveRootIfNoOne=None,
        useRomanFunction=None,
        useUnicodeRoman=None,
        useCommas=None,
        useAlterationSymbols=None,
        useBrackets=None,
        nameDiadsByIntervalName=None,
        utiliseCaching=None,
        returnAllCandidates=None,
        makeTextMulticoloured=None,
        outlineColourTag=None,
        rootKey=None,
    ):  # Implement polychord, Implement searching multiple possibilities of triads for each extension
        try:
            Chord
        except NameError:
            from Chord import Chord
        if useWeirdSusSymbols == None:
            useWeirdSusSymbols = True
        if useAugmentedChords == None:
            useAugmentedChords = False
        if useAugUnicodeSymbol == None:
            useAugUnicodeSymbol = True
        if useHalfDiminishedChords == None:
            useHalfDiminishedChords = True
        if useHalfDiminishedUnicodeSymbols == None:
            useHalfDiminishedUnicodeSymbols = Chord.qualityDefaults['useHalfDiminishedUnicodeSymbols']
        if useDiminishedUnicodeSymbols == None:
            useDiminishedUnicodeSymbols = Chord.qualityDefaults['useDiminishedUnicodeSymbols']
        if useMa7Triangle == None:
            useMa7Triangle = False
        if capitaliseMajor == None:
            capitaliseMajor = True
        if printDebugInfo == None:
            printDebugInfo = False
        if useSixNines == None:
            useSixNines = True
        if createPolychordIfNoOne == None:
            createPolychordIfNoOne = False
        if moveRootIfNoOne == None:
            moveRootIfNoOne = True
        if useRomanFunction == None:
            useRomanFunction = True
        if useUnicodeRoman == None:
            useUnicodeRoman = True
        if useCommas == None:
            useCommas = False
        if useAlterationSymbols == None:
            useAlterationSymbols = False
        if useBrackets == None:
            useBrackets = True
        if nameDiadsByIntervalName == None:
            nameDiadsByIntervalName = True
        if utiliseCaching == None:
            utiliseCaching = True
        if returnAllCandidates == None:
            returnAllCandidates = False
        if makeTextMulticoloured == None:
            makeTextMulticoloured = False
        if outlineColourTag == None:
            outlineColourTag = 'black'
        if rootKey == None:
            rootKey = "C"
        __useHalfDiminishedUnicodeSymbolsDefault = Chord.qualityDefaults['useHalfDiminishedUnicodeSymbols']
        __useDiminishedUnicodeSymbolsDefault = Chord.qualityDefaults['useDiminishedUnicodeSymbols']
        Chord.qualityDefaults['useHalfDiminishedUnicodeSymbols'] = useHalfDiminishedUnicodeSymbols
        Chord.qualityDefaults['useDiminishedUnicodeSymbols'] = useDiminishedUnicodeSymbols
        callerParameters = locals()
        cachedName = str(self) + '.getChordQuality(' + str(callerParameters) + ')'
        #if not makeTextMultiColoured:
        #    pass


        if utiliseCaching:

            try:
                return Change.cache[cachedName]
                print('did use cached balue')
            except:
                pass

        
            
        if self.containsDuplicateNote():
            return self.removeDuplicateNotes().getChordQuality(
                useWeirdSusSymbols=useWeirdSusSymbols,
                useAugmentedChords=useAugmentedChords,
                useAugUnicodeSymbol=useAugUnicodeSymbol,
                useMa7Triangle=useMa7Triangle,
                printDebugInfo=printDebugInfo,
                useSixNines=useSixNines,
                createPolychordIfNoOne=createPolychordIfNoOne,
                moveRootIfNoOne=moveRootIfNoOne,
                useRomanFunction=useRomanFunction,
                useCommas=useCommas,
                useAlterationSymbols=useAlterationSymbols,
                useBrackets=useBrackets,
            )
        _selfLen = len(self)
        if _selfLen == 0:
            if returnAllCandidates:
                return ["N.C."]
            else:
                return "N.C."
        elif _selfLen == 1:
            _chordQuality = "unison"
            if makeTextMulticoloured:
                _chordQuality = makeTextMulticoloured(
                    _chordQuality, colourTags=[Key(rootKey).inAllFlats().getASCII()], outlineColourTag=outlineColourTag
                )

            if returnAllCandidates:
                return [_chordQuality]
            else:
                return _chordQuality
        # moveRootIFNoOne is fucked
        # if False and moveRootIfNoOne and not self.containsNotes('1'):
        if not self.containsNotes("1"):
            _chordQuality = self.getNormalForm().getChordQuality(
                useWeirdSusSymbols=useWeirdSusSymbols,
                useAugmentedChords=useAugmentedChords,
                useAugUnicodeSymbol=useAugUnicodeSymbol,
                useMa7Triangle=useMa7Triangle,
                printDebugInfo=printDebugInfo,
                useSixNines=useSixNines,
                createPolychordIfNoOne=createPolychordIfNoOne,
                moveRootIfNoOne=moveRootIfNoOne,
                makeTextMulticoloured=makeTextMulticoloured,
                outlineColourTag = outlineColourTag
            )
            if useRomanFunction:
                _functionStr = self.notes[0].getRomanNumeral(
                    returnCapital=Change.chordIsCapitalRoman(_chordQuality)
                )

                _functionStr = JazzNote.convertNoteToRealUnicodeStr(
                    _functionStr, useAnyStr=True, justFlatsAndSharps=True
                )
            else:
                _functionStr = self.notes[0]
            return _functionStr + _chordQuality

        # Diads
        if len(self) == 2 and nameDiadsByIntervalName:
            # input('{} {}'.format(self[1],self[1].note))
            _st = self[1].semitonesFromOne()
            if _st == 1:
                _chordSymbol = "mi2nd"
            elif _st == 2:
                _chordSymbol = "ma2nd"
            elif _st == 3:
                _chordSymbol = "mi3rd"
            elif _st == 4:
                _chordSymbol = "ma3rd"
            elif _st == 5:
                _chordSymbol = "4th"
            elif _st == 6:
                _chordSymbol = "tritone"
            elif _st == 7:
                _chordSymbol = "5th"
            elif _st == 8:
                _chordSymbol = "mi6th"
            elif _st == 9:
                _chordSymbol = "ma6th"
            elif _st == 10:
                _chordSymbol = "mi7th"
            elif _st == 11:
                _chordSymbol = "ma7th"
            if capitaliseMajor:
                _chordSymbol = _chordSymbol.replace("ma", "Ma")
            if makeTextMulticoloured:

                _chordSymbol = makeTextMulticoloured(
                    _chordSymbol,
                    [Key(rootKey, JazzNote.makeFromSet(_st)).inAllFlats().getASCII()],
                    outlineColourTag = outlineColourTag,
                )
            if returnAllCandidates:
                return [_chordSymbol]
            else:
                return _chordSymbol

        # First I'm going to figure out the logic in plain Syllabic
        #
        # Let's find the highest natural extension
        naturalExtensions = []
        naturalExtensionsExclusions = []
        naturalExtensionsModifications = []
        naturalExtensionsAdditions = []
        naturalExtensionsInclusions = []
        _extensionQualities = []
        naturalExtensionsRating = []
        weirdSusNotes = ("b2", "#4")

        # This is trying to find the most inclusive (of number of notes) chord symbol
        # Scratch that. It's actually going to build every combination of chord symbol

        # First build the list of extension-chord-symbols to check
        if useWeirdSusSymbols == True:
            for note in (
                "13",
                "11",
                "9",
                "7",
                "b7",
                "6",
                "5",
                "3",
                "b3",
                "4",
                "2",
                "#4",
                "b2",
                "1",
            ):
                # This doesn't talk about the b6, because that's not a chord symbol
                if self.containsNotes(note):
                    naturalExtensions.append(note)
        elif useWeirdSusSymbols == False:
            for note in ("13", "11", "9", "7", "b7", "6", "5", "3", "b3", "4", "2"):
                # This doesn't talking about the b6, because that's not a chord symbol
                # This doesn't talking about the b6 #4 b2, because that's not a chord symbol
                # or because we have chosen not to include those weird sus chords
                if self.containsNotes(note):
                    naturalExtensions.append(note)

        # Natural extensions is the possibilties in the extension-chord-symbol
        # i.e, 11, 7

        for extension in naturalExtensions:

            naturalExtensionsExclusions.append([])
            naturalExtensionsModifications.append([])
            naturalExtensionsAdditions.append([])
            naturalExtensionsInclusions.append([])
            _extensionQualities.append("")
            naturalExtensionsRating.append(0)

            # Find out the stats for a symbol
            # You'll need to know how many of the symbol's lower parts are not present
            _inclusions = naturalExtensionsInclusions[-1]
            _additions = naturalExtensionsAdditions[-1]
            _exclusions = naturalExtensionsExclusions[-1]
            _modifications = naturalExtensionsModifications[-1]
            _chordSymbol = _extensionQualities[-1]
            rating_ = naturalExtensionsRating[-1]
            _third = False
            _fifth = False
            _seventh = False
            _triad = ""
            _hasThird = False
            # Include the note of the chord symbol
            if extension in (
                "3",
                "b3",
                "2",
                "4",
                "b2",
                "#4",
            ):
                _hasThird = True
                _third = extension
            if extension in ("13", "6", "#4", "4", "5", "3", "b3", "2", "b2", "1"):
                _inclusions.append(extension)

            if extension in ("13", "11"):  # Look at 11th
                
                if self.containsNotes("11"):
                    _inclusions.append("11")
                elif self.containsNotes("#11"):
                    _inclusions.append("#11")
                    _modifications.append("#11")
                else:
                    _exclusions.append("11")
                

            if extension in ("13", "11", "9"):  # Look at 9th
                if self.containsNotes("9") and "9" not in _inclusions:  # Has natural 9
                    if "2" in _inclusions:
                        _inclusions.remove("2")
                    _inclusions.append("9")
                elif (
                    self.containsNotes("b9") and "b2" not in _inclusions
                ):  # no 9 or #9. Does contain b9
                    _inclusions.append("b9")
                    _modifications.append("b9")

                elif self.containsNotes("#9"):  # No natural 9 and has #9
                    _inclusions.append("#9")
                    _modifications.append("#9")

                else:  # No 9 of any sort
                    _exclusions.append("9")

            if extension in ("13", "11", "9", "7", "b7"):  # Look at 7th
                if extension == "7":
                    _inclusions.append("7")
                elif extension == "b7":  # Contains the b7 and no ma7
                    _inclusions.append("b7")
                elif self.containsNotes("7") or self.containsNotes("b7"):
                    if self.containsNotes("7"):  # This is a ma7 but also has the b7
                        _inclusions.append("7")
                    elif self.containsNotes("b7"):  # Contains the b7 and no ma7
                        _inclusions.append("b7")
                else:
                    _exclusions.append("7")
            if extension in (
                "13",
                "11",
                "9",
                "7",
                "b7",
                "6",
                "#4",
                "4",
                "3",
                "b3",
                "2",
                "b2",
            ):  # Look at 5th
                if self.containsNotes("5"):
                    _inclusions.append("5")
                    # Shold I assign the fifth? No.. it'll auto assign it later
                elif self.containsNotes("#5") and not self.containsNotes('b5'):

                    _inclusions.append("#5")
                    _modifications.append("#5")
                    
                elif (
                    self.containsNotes("b5")
                    and not "#11" in _inclusions
                    and not "#4" in _inclusions
                    and not 'b5' in _inclusions
                ):
                    _inclusions.append("b5")
                    #input('yo')
                    _modifications.append("b5")
                    if '#11' in _inclusions:_inclusions.remove('#11')
                    if '#11' in _modifications:_modifications.remove('#11')

                    #_exclusions.append('11')
                    
                    
                else:
                    _exclusions.append("5")
            if extension in (
                "13",
                "11",
                "9",
                "7",
                "b7",
                "6",
                "3",
                "b3",
                "4",
                "2",
            ):  # Look at 3rd

                # If this is true, it's a major third
                if self.containsNotes("3") and _hasThird == False:
                    _inclusions.append("3")
                    _hasThird = True
                    _third = "3"
                # If this is true, it's not a major third
                # Victory Unfinished
                # if self.containsNotes('b3') and not _hasThird and not '#9' in inclusions_:
                if self.containsNotes("b3") and _hasThird == False:
                    if "#9" in _additions:
                        _additions.remove("#9")
                    if "b3" in _additions:
                        _additions.remove("b3")
                    if "#9" in _inclusions:
                        _inclusions.remove("#9")
                        _exclusions.append("9")
                        # newish part
                    if "#9" in _modifications:
                        _modifications.remove("#9")
                        """print('mods {}\t incl {}\t adds {}\t'.format(
                            _modifications, _inclusions, _additions
                        ))"""
                    _hasThird = True
                    _third = "b3"
                    _inclusions.append("b3")
                    # _modifications.append('b3')
                    
                if (
                    self.containsNotes("4")
                    and not "11" in _inclusions
                    and _hasThird == False
                ):
                    if "11" in _additions:
                        _additions.remove("11")
                    if not "11" in _inclusions and not _hasThird:
                        _inclusions.append("4")
                        _third = "4"
                        _hasThird = True
                if self.containsNotes("2") and not "9" in _inclusions and not _hasThird:
                    if "9" in _additions:
                        _additions.remove("9")
                    if not "9" in _inclusions and not _hasThird:
                        _inclusions.append("2")
                        _third = "2"
                        _hasThird = True
                if useWeirdSusSymbols and not _hasThird:
                    if self.containsNotes("#4"):
                        if "#11" in _additions:
                            _additions.remove("#11")
                        if (
                            not "#11" in _inclusions
                            and not "b5" in _inclusions
                            and not _hasThird
                        ):
                            _hasThird = True

                            _inclusions.append("#4")
                    if self.containsNotes("b2") and not _hasThird:
                        if "b9" in _additions:
                            _additions.remove("b9")
                        if (
                            not "b9" in _inclusions
                            and not "b2" in _inclusions
                            and not _hasThird
                        ):
                            _inclusions.append("b2")
                            _hasThird = True
                _noThree = True
                for __i in (
                    "3",
                    "b3",
                    "2",
                    "4",
                    "#4",
                    "b2",
                ):
                    if __i in _inclusions:
                        _noThree = False
                if _noThree == True:
                    # print('what could have no 3???   '+str(self)+' '+str(inclusions_)+str(_third))
                    _exclusions.append("3")
                else:
                    pass  # print(_third)
            # add exclusion for 1
            if not self.containsNotes("1") and createPolychordIfNoOne == False:
                _exclusions.append("1")


            """ Now enter the part where we get the list of additions,
            which is the list of total notes minus those included
            """
            
            for note in self.notes:
                _noteStr = note.note
                if not Change(_inclusions).containsNotes(_noteStr) and _noteStr != "1":
                    _additions.append(_noteStr)

            """Now enter the part where we make the chord symbol"""

            """We will indicate whether there is a ma 7"""
            for thirdCandidate in ["3", "b3", "4", "2", "#4", "b2"]:
                # if thirdCandidate in inclusions_ and _third != False:
                if thirdCandidate in _inclusions:
                    _third = thirdCandidate

                    break
            
            # auto assign the fifth
            for fifthCandidate in ["b5", "5", "#5"]:
                if fifthCandidate in _inclusions:
                    _fifth = fifthCandidate
                    #input('shit {} {} {} {}'.format(_inclusions,_modifications,_additions,_fifth))
            for seventhCandidate in ["b7", "7"]:
                if seventhCandidate in _inclusions:
                    _seventh = seventhCandidate
            
            # print('inclusions ', inclusions_,'third earlier',_third)

            if _third == "3":
                if useAugmentedChords and _fifth == "#5":
                    _triad = "aug"
                    _modifications.remove("#5")
                else:
                    _triad = "ma"
            elif _third == "b3":  # the b3 victory
                # input('beer inc {} mod {} add {} self {} third {} fifth {} seventh {}'.format(
                #    _inclusions,_modifications,_additions,self,_third,_fifth,_seventh))
                # print('it was supposed to be minor, according to the third being b3 and the fifth =',fifth_)

                # input('here is the third {} ninth {}'.format(_third, _ninth))
                # I added this
                _triad = "mi"
                if "b3" in _additions:
                    _additions.remove("b3")
                    _inclusions.remove("#9")
                    _modifications.remove("#9")
                    # would I remove the #9 here?

                if _fifth == "b5":
                    if _seventh == "b7":
                        if useHalfDiminishedChords:
                            _triad = "halfdim"
                            _modifications.remove("b5")
                        else:
                            _triad = "mi"
                            if "b5" not in _modifications:
                                _modifications.append("b5")
                            # _inclusions.remove('b5')
                    else:
                        # Fix dim13 chords
                        if extension == "13":
                            _triad = "mi"
                            _inclusions.remove("b5")
                            _modifications.append("b5")
                            # input('shit {}'.format(_chordSymbol))
                        else:
                            _triad = "dim"
                        _modifications.remove("b5")
                elif _fifth == "#5":

                    _triad == "mi"
                    if self.containsNotes("#4"):
                        # Trade fifth with extension
                        _modifications.remove("#5")
                        _inclusions.remove("#5")
                        _inclusions.append("b5")
                        if '#11' in _inclusions: _inclusions.remove('#11')
                        if '#11' in _modifications: _modifications.remove('#11')
                        _additions.append("b6")
                        _fifth = "b5"
                        _triad = 'dim'

                        #input('hherherher \ninc: {} \nadd: {}\nmod: {}\nfifth:{}'.format(
                        #    _inclusions,_additions,_modifications,_fifth))
                        if "b5" in _additions:
                            _additions.remove("b5")
                        if "#4" in _additions:
                            _additions.remove("#4")
                        if _seventh == "b7" and useHalfDiminishedChords:
                            _triad = "halfdim"
                        else:
                            if _seventh == "b7":
                                _triad = "mi"
                                if "b5" not in _modifications:
                                    _modifications.append("b5")
                            elif _seventh in ("6", "7"):
                                _triad = "dim"
                else:
                    _triad = "mi"
            elif _third == "4":
                _triad = "sus4"
            elif _third == "2":
                _triad = "sus2"
            elif _third == "#4":
                _triad = "sus#4"
            elif _third == "b2":
                _triad = "susb2"

            # print('trying to find triad', _triad,_third)

            # get 5 back in if excluded by accident?
            if '5' in _exclusions:
                if 'b6' in _additions:
                    _additions.remove('b6')
                    _exclusions.remove('5')
                    _modifications.append('#5')
                if any([n in _additions for n in ('#11','#4')]):
                    _additions.remove('#11')
                    _exclusions.remove('5')
                    _modifications.append('b5')
            #print('fifth', _fifth, 'chordquality', _chordSymbol)
            #print('le inclusions', _inclusions)
            #print('le mod', _modifications)
            #print('le adds', _additions)
            #print('le traide', _triad, '\n')
            #print('l\'incunu', _exclusions)
            #input('yo')






            """Start layout of the chord symbol"""
            if "sus" not in _triad and _triad != "ma":
                # if (False):
                _chordSymbol += _triad
                # print('triad now \'',_triad,'\'',sep='')

            if extension in (
                "7",
                "b7",
                "9",
                "11",
                "13",
            ):
                if _seventh == "7" and "ma" not in _chordSymbol:
                    if useMa7Triangle:
                        _chordSymbol += Unicode.chars["Major Seventh Triangle"]
                    else:
                        _chordSymbol += "ma"
                elif _seventh == "b7":
                    _chordSymbol += ""
                if extension != "b7":
                    _chordSymbol += extension
                elif extension == "b7":
                    _chordSymbol += "7"
            elif extension in ("6", "5"):
                _chordSymbol += extension
                if useSixNines == True and extension == "6" and not _triad == "dim":

                    if "9" in _additions:
                        _additions.remove("9")
                        _inclusions.append("9")
                        _chordSymbol += """/9"""

                    if "2" in _additions:
                        _additions.remove("2")
                        _inclusions.append("9")
                        _chordSymbol += """/9"""
            elif extension in ("3",) and _triad != "aug":
                _chordSymbol += _triad
            # elif extension in ('3',) and _triad != 'aug':
            #    _chordSymbol += _triad
            elif extension == "1":
                _chordSymbol += "1"

            if "sus" in _triad:
                _chordSymbol += _triad

            """Straighten out the additions"""
            if "b3" in _additions and "3" in _inclusions:
                _additions.remove("b3")
                _additions.append("#9")

            """Bring 2's up to 9's, 4's up to 11s,  6 to 13 for additions"""
            for i in range(len(_additions)):
                if _additions[i] == "2":
                    _additions[i] = "9"
                elif _additions[i] == "b2":
                    _additions[i] = "b9"
                elif _additions[i] == "#2":
                    _additions[i] = "#9"
                elif _additions[i] == "4":
                    _additions[i] = "11"
                elif _additions[i] == "#4":
                    _additions[i] = "#11"
                elif _additions[i] == "b5":
                    _additions[i] = "#11"

                if (
                    "7" in _inclusions
                    or "b7" in _inclusions
                    or (
                        "6" in _inclusions
                        and "9" in _inclusions
                        and useSixNines == True
                    )
                ):
                    # Put it here if you want it to only raise them an octave if the quality is a seventh
                    if _additions[i] == "6":
                        _additions[i] = "13"
                    if _additions[i] == "b6":
                        _additions[i] = "b13"
                    if _additions[i] == "#6":
                        _additions[i] = "#13"

            """Arrange the additions into ascending chromatic order"""
            _additions = [
                Change(_additions).sortBySemitonePosition().notes[i].note
                for i in range(len(_additions))
            ]
            """Sort the modifications in ascending order"""
            _modifications = [
                Change(_modifications).sortBySemitonePosition().notes[i].note
                for i in range(len(_modifications))
            ]
            """Arrange the exclusions into ascending chromatic order"""
            _exclusions = [
                Change(_exclusions).sortBySemitonePosition().notes[i].note
                for i in range(len(_exclusions))
            ]

            """Add the exclusions, modifications, and additions"""
            if useCommas == True:
                _comma = ", "
            else:
                _comma = " "
            if (
                len(_additions) >= 1
                or len(_modifications) >= 1
                or len(_exclusions) >= 1
            ):
                if useBrackets == True:
                    _chordSymbol += "("

                if _modifications != []:

                    for note in range(len(_modifications)):
                        _chordSymbol += _modifications[note]
                        if note != len(_modifications) - 1:
                            _chordSymbol += " "

                if _exclusions != []:
                    if _modifications != []:
                        _chordSymbol += _comma  # Comma spot
                    if useAlterationSymbols == True:
                        _chordSymbol += Unicode.chars["Remove Note"]
                    else:
                        _chordSymbol += "no "
                    for note in range(len(_exclusions)):
                        _chordSymbol += _exclusions[note]
                        if note != len(_exclusions) - 1:
                            _chordSymbol += " "

                if _additions != []:
                    # Turn notes to add into a change to sort it
                    additionsSorted_ = Change(_additions).sortBySemitonePosition()
                    if _modifications != [] or _exclusions != []:
                        _chordSymbol += _comma  # Comma spot
                    if useAlterationSymbols == True:
                        _chordSymbol += Unicode.chars["Add Note"]
                    else:
                        _chordSymbol += "add "
                    for note in range(len(additionsSorted_)):
                        _chordSymbol += str(additionsSorted_.notes[note])
                        if note != len(_additions) - 1:
                            _chordSymbol += " "

                if useBrackets == True:
                    _chordSymbol += ")"
            if "dim6" in _chordSymbol:
                _chordSymbol = _chordSymbol.replace("dim6", "dim7")
            _chordSymbol = _chordSymbol.replace("#", "♯")
            _chordSymbol = _chordSymbol.replace("b", "♭")
            if useHalfDiminishedUnicodeSymbols:
                _chordSymbol = _chordSymbol.replace(
                    "halfdim", Unicode.chars["half diminished chord"]
                )  #'⌀'
            if useDiminishedUnicodeSymbols:
                _chordSymbol = _chordSymbol.replace(
                    "dim", Unicode.chars["diminished chord"]
                )  #'°' ° oᴼ
            if useAugUnicodeSymbol:
                _chordSymbol = _chordSymbol.replace(
                    "aug", Unicode.chars["augmented chord"]
                )
            if capitaliseMajor:
                _chordSymbol = _chordSymbol.replace("ma", "Ma")

            _extensionQualities[-1] = _chordSymbol

            """Now we will rank the symbols"""
            rating_ = float(
                len(_exclusions) * 1.15
                + len(_additions) * 1
                + len(_modifications) * 0.9
            )
            # rating_ = float(len(_exclusions) * 1.15 + len(_additions) * 1 + len(_modifications) * 1 + len(inclusions_) * (-1))
            if _triad in ("sus#4", "susb2"):
                rating_ += 0.1

            if "sus" in _triad:
                rating_ += 0.1
                if "b3" in _additions or "3" in _additions:
                    rating_ += 0.2
                if extension in ("6", "b7", "7", "9", "11", "13"):
                    rating_ += 0.95
                if "b" in _triad or "#" in _triad:
                    rating_ += 0.5
            if _triad == "mi":
                if "3" in _additions:
                    rating_ += 1
            if _triad in ("halfdim", "dim"):
                if "3" in _additions:
                    rating_ += 1
            if extension == "6":
                if "b7" in _additions or "7" in _additions:
                    rating_ += 0.2
            if "6/9" in _chordSymbol:
                rating_ += 0.4
            if extension == "b7":
                if "7" in _additions:
                    rating_ += 0.3
            if extension == "1":
                rating_ += 10
            if "3" in _exclusions:
                rating_ += 0.5
            if "b7" in _additions or "7" in _additions:
                rating_ += 1
            naturalExtensionsRating[-1] = rating_

            if makeTextMulticoloured:

                _makePlain = Chord.makePlain
                _makeStyled = Chord.makeStyled
                _makeJazzNoteLikeChordSymbolExtension = Chord.makeJazzNoteLikeChordSymbolExtension
                _makeCiphered = Utility.makeNumberCipheredIfPreceededBy
                _makeUnciphered = Utility.makeNumberUnciphered
                _cipherTriggers = (
                    "0",
                    "=",
                    ".",
                    Unicode.chars["Flat"],
                    Unicode.chars["Sharp"],
                )
                """Let us colour code this shit"""
                _colourTags = Key.allFlats
                # input('triad {} extension {}'.format(_triad,extension))
                if _makePlain(_triad) in (
                    "mi",
                    "ma",
                    "Ma",
                    "sus4",
                    "sus2",
                    "susb2",
                    "sus#4",
                    "dim",
                    "aug",
                    "halfdim",
                    
                ) and _triad not in _makePlain(
                    _makeJazzNoteLikeChordSymbolExtension(extension)
                ):

                    if "sus" not in _triad:
                        if (
                            _fifth == "5"
                            or (_fifth == "b5" and _triad in ("dim", "halfdim"))
                            or (_fifth == "#5" and _triad == "aug")
                        ):
                            # _colourTags = [Key(k).inAllFlats().getASCII() for k in _colourTags if Key(k).distanceFromC()  in [Key(d).distanceFromC() for d in Change([_third,_fifth]).byWays(rootKey)]]
                            _colourTags = [
                                Key(rootKey, n).inAllFlats().getASCII()
                                for n in Change([_third, _fifth])
                            ]
                            # input(_colourTags)

                        else:  # has an altered 5th
                            """_colourTags = [Key(k).inAllFlats().getASCII() for k in _colourTags if
                            Key(k).distanceFromC() in [Key(d).distanceFromC() for d in
                                                       Change([_third]).byWays(rootKey)]]"""
                            _colourTags = [Key(rootKey, _third).inAllFlats().getASCII()]
                        if (
                            _triad == "ma"
                            and _seventh == "7"
                            and JazzNote(extension).semitonesFromOne(octaveLimit=2) > 11
                        ):
                            _colourTags.append(
                                Key(rootKey, JazzNote("7")).inAllFlats().getASCII()
                            )
                    elif "sus" in _triad:
                        if _fifth == "5":
                            _colourTags = [
                                Key(rootKey, n).inAllFlats().getASCII()
                                for n in Change([_fifth])
                            ]
                            """_colourTags = [Key(k).getASCII() for k in _colourTags if
                                           Key(k).distanceFromC() in [Key(d).distanceFromC() for d in
                                                                      Change([_fifth]).byWays(rootKey)]]"""
                        else:
                            # raise ValueError('wtf bitch')
                            _colourTags = None
                    else:
                        """_colourTags = [Key(k).getASCII() for k in _colourTags if
                        Key(k).distanceFromC() in [Key(d).distanceFromC() for d in
                                                   Change(['1', _third]).byWays(rootKey)]]"""

                        if _chordSymbol == self.getChordQuality():
                            pass#input('here here')
                        _colourTags = [
                            Key(rootKey, n).inAllFlats().getASCII()
                            for n in Change(["1", _third])
                        ]
                    if _colourTags == None or len(_colourTags) < 1:

                        pass  # raise ValueError('shit. colourTags: {} rootKey: {}\nrandom shit = {}'.format(
                        #    _colourTags,rootKey,Change(['1','3']).byWays('A')))
                    """if _colourTags is None:
                        input('colourtags is {} {} {} {}'.format(_colourTags, self.getChangeNumber(), rootKey, _chordSymbol))
                    else:
                        print('colourtags is', _colourTags, self.getChangeNumber(), rootKey, _chordSymbol)"""
                    # colouring Triad
                    if (_triad) in _makePlain(_extensionQualities[-1]):
                        try:
                            _triadIndex = _extensionQualities[-1].index(
                                _makeStyled(_triad)
                            )
                        except ValueError as e:
                            print(
                                e, _makeStyled(_triad), _extensionQualities[-1]
                            )
                            input("jalapeno")
                        if "sus" in _triad:
                            # input('{} sus in triad: {}'.format(self.getChordQuality(),_triad) )

                            if _fifth == "5":
                                _extensionQualities[
                                    -1
                                ] = _extensionQualities[-1].replace(
                                    "sus",
                                    makeTextMulticoloured(
                                        text="sus", colourTags=_colourTags,outlineColourTag = outlineColourTag,
                                    ),
                                )
                                _replaceStr = "}"
                                # input('before "{}".replace("{}")'.format(
                                #    _extensionQualities[-1],_replaceStr + _makeStyled(_third)))
                            else:
                                _replaceStr = ""
                            if len(_third) == 1:
                                _extensionQualities[-1] = _makeCiphered(
                                    _extensionQualities[-1],
                                    _third,
                                    _cipherTriggers,
                                )
                            _extensionQualities[
                                -1
                            ] = _extensionQualities[-1].replace(
                                _makeStyled(_third),
                                makeTextMulticoloured(
                                    text=_makeStyled(_third),
                                    colourTags=[
                                        Key(JazzNote(_third).byWay(rootKey))
                                        .inAllFlats()
                                        .getASCII()
                                    ],
                                    outlineColourTag=outlineColourTag,
                                ),
                            )
                            if len(_third) == 1:
                                _extensionQualities[-1] = _makeUnciphered(
                                    _extensionQualities[-1], _third
                                )

                            if _chordSymbol.index("sus") != 0:
                                # chord does not start with sus
                                _notes = [
                                    n
                                    for n in _inclusions
                                    if (
                                        n not in _triad
                                        and n not in _modifications
                                        and "5" not in n
                                    )
                                ]
                                _notes = [
                                    n.note
                                    for n in Change(_notes).sortBySemitonePosition(
                                        octaveLimit=1
                                    )
                                ]
                                if "6/9" in _chordSymbol:
                                    _baseExtension = "6/9"
                                elif (
                                    JazzNote(extension).semitonesFromOne(octaveLimit=2)
                                    <= 11
                                ):

                                    _baseExtension = _extensionQualities[-1][
                                        0 : len(
                                            _makeJazzNoteLikeChordSymbolExtension(
                                                extension
                                            )
                                        )
                                    ]
                                else:
                                    if _seventh == "7":  # Ma7th

                                        assert (
                                            _makeStyled("ma")
                                            in _extensionQualities[-1]
                                        )
                                        _maPart = _makeStyled("ma")
                                        _extensionQualities[
                                            -1
                                        ] = _extensionQualities[-1].replace(
                                            _maPart,
                                            makeTextMulticoloured(
                                                _maPart,
                                                Key(rootKey, JazzNote("7"))
                                                .inAllFlats()
                                                .getASCII(),
                                                outlineColourTag=outlineColourTag,
                                            ),
                                        )
                                        _notes.remove("7")
                                        _baseExtension = extension
                                    else:

                                        _baseExtension = _extensionQualities[
                                            -1
                                        ][0 : len(extension)]

                                if len(_baseExtension) == 1:
                                    
                                    _extensionQualities[-1] = _makeCiphered(
                                        _extensionQualities[-1],
                                        _baseExtension,
                                        _cipherTriggers,
                                    )

                                if _baseExtension == "6/9":
                                    _extensionQualities[-1] = _makeCiphered(
                                        _extensionQualities[-1],
                                        6,
                                        _cipherTriggers,
                                    )
                                    _extensionQualities[-1] = _makeCiphered(
                                        _extensionQualities[-1],
                                        9,
                                        _cipherTriggers,
                                    )
                                    _extensionQualities[-1].replace(
                                        "6/9",
                                        makeTextMulticoloured(
                                            "6", Key(rootKey, JazzNote("6")).getASCII(), outlineColourTag = outlineColourTag,
                                        )
                                        + "/"
                                        + makeTextMulticoloured(
                                            "9", Key(rootKey, JazzNote("9")).getASCII(), outlineColourTag = outlineColourTag,
                                        ),
                                    )
                                    _extensionQualities[-1] = _makeCiphered(
                                        _extensionQualities[-1],
                                        6,
                                        _cipherTriggers,
                                    )
                                    _extensionQualities[-1] = _makeCiphered(
                                        _extensionQualities[-1],
                                        9,
                                        _cipherTriggers,
                                    )
                                else:
                                    if len(_baseExtension) == 1:
                                        _extensionQualities[
                                            -1
                                        ] = _makeCiphered(
                                            _extensionQualities[-1],
                                            _baseExtension,
                                            _cipherTriggers,
                                        )
                                    _extensionQualities[
                                        -1
                                    ] = _extensionQualities[-1].replace(
                                        _baseExtension,
                                        makeTextMulticoloured(
                                            _baseExtension,
                                            colourTags=[
                                                Key(rootKey, JazzNote(n))
                                                .inAllFlats()
                                                .getASCII()
                                                for n in _notes
                                            ], outlineColourTag = outlineColourTag,
                                        ),
                                    )
                                    if len(_baseExtension) == 1:
                                        _extensionQualities[
                                            -1
                                        ] = _makeUnciphered(
                                            _extensionQualities[-1],
                                            _baseExtension,
                                        )
                                if len(_baseExtension) == 1:
                                    _extensionQualities[-1] = _makeUnciphered(
                                        _extensionQualities[-1], _baseExtension
                                    )
                                # input('Hello #{} chord: {} \n\nbase extension: {}\n\ninclusions: {}'.format(
                                #   self.getChangeNumber(),_extensionQualities[-1],_baseExtension,_inclusions))
                            # input('after {}'.format(_extensionQualities[-1]))
                            # print()
                        elif "sus" not in _triad:  # sus not in triad

                            if _colourTags not in (None, []):
                                _extensionQualities[
                                    -1
                                ] = Utility.insertSubstringInStr(
                                    _triadIndex,
                                    _extensionQualities[-1][
                                        len(_makeStyled(_triad)) + _triadIndex :
                                    ],
                                    makeTextMulticoloured(
                                        text=_makeStyled(_triad), colourTags=_colourTags,
                                        outlineColourTag=outlineColourTag,
                                    ),
                                )

                            # input(
                            #    'sus aint in triad. chord: {} \nstring: {}\ninclusions: {} \nadditions: {}\nextension:{}\ntriad:{}'.format(
                            #        self.getChordQuality(),
                            #        _extensionQualities[-1], _inclusions, _additions, extension, _triad))

                    if "6/9" in _chordSymbol:
                        # input('{} {} {} {}'.format(_triad,_colourTags,_chordSymbol,_makeStyled(_triad) not in _extensionQualities[-1]))

                        # assert _colourTags, self.getChordQuality() + 'colourTags: ' + str(_colourTags)
                        if _colourTags == None:
                            _colourTags = []
                        _extensionQualities[-1] = _extensionQualities[
                            -1
                        ].replace(
                            "6/9",
                            makeTextMulticoloured(
                                "6",
                                (
                                    _colourTags
                                    if _makeStyled(_triad) not in _chordSymbol
                                    else []
                                )
                                + [Key(rootKey, JazzNote("6")).inAllFlats().getASCII()],
                                outlineColourTag=outlineColourTag,
                            )
                            + "/"
                            + makeTextMulticoloured(
                                "9", Key(rootKey, JazzNote("9")).inAllFlats().getASCII(),
                                outlineColourTag=outlineColourTag,
                            ),
                        )

                    elif _makeJazzNoteLikeChordSymbolExtension(
                        extension
                    ) in _extensionQualities[-1] and extension not in (
                        "b2",
                        "2",
                        "3",
                        "4",
                        "#4",
                    ):


                        if "sus" not in _makePlain(_chordSymbol):
                            
                            if _triad in _makePlain(_chordSymbol):
                                # input('triad {}  in {}'.format(_triad,_chordSymbol))
                                _notes = [
                                    n
                                    for n in _inclusions
                                    if n not in (_modifications + [_third, _fifth])
                                ]
                            else:
                                # input('triad {} aint in {}'.format(_triad,_chordSymbol))
                                _notes = [
                                    n for n in _inclusions if n not in _modifications
                                ]
                            _notes = [
                                n.note
                                for n in Change(_notes).sortBySemitonePosition(
                                    octaveLimit=1
                                )
                            ]
                            if _seventh == "7":
                                if _triad == "ma":

                                    if (
                                        _makeStyled("ma")
                                        in _extensionQualities[-1]
                                    ):
                                        if "3" in _notes:
                                            _notes.remove("3")
                                        if "7" in _notes:
                                            _notes.remove("7")
                                else:

                                    if _makeStyled("ma") in _chordSymbol:
                                        if len(_notes) > 1:
                                            _notes.remove("7")
                                        if (
                                            JazzNote(extension).semitonesFromOne(
                                                octaveLimit=2
                                            )
                                            <= 11
                                        ):
                                            _extensionQualities[
                                                -1
                                            ] = _extensionQualities[
                                                -1
                                            ].replace(
                                                _makeStyled("ma") + extension,
                                                makeTextMulticoloured(
                                                    _makeStyled("ma") + extension,
                                                    [
                                                        Key(rootKey, extension)
                                                        .inAllFlats()
                                                        .getASCII()
                                                    ],
                                                    outlineColourTag=outlineColourTag,
                                                ),
                                            )
                                        else:
                                            print(
                                                "heyyyy",
                                                Key(rootKey, "7")
                                                .inAllFlats()
                                                .getASCII(),
                                            )
                                            _extensionQualities[
                                                -1
                                            ] = _extensionQualities[
                                                -1
                                            ].replace(
                                                _makeStyled("ma"),
                                                makeTextMulticoloured(
                                                    _makeStyled("ma"),
                                                    [
                                                        Key(rootKey, "7")
                                                        .inAllFlats()
                                                        .getASCII()
                                                    ], outlineColourTag = outlineColourTag,
                                                ),
                                            )
                                    else:#Not major triad
                                        pass#print('here and there')
                                        #input('here and there')
                            """input('blah blaah #{} {} extension: {} inclusions:{} notes:{}\n{} third:{}'.format(
                                                            self.getChangeNumber(), self.getChordQuality(),
                                                            _makeJazzNoteLikeChordSymbolExtension(extension), _inclusions, _notes,
                                                            _extensionQualities[-1], _third))"""

                            if (
                                len(_makeJazzNoteLikeChordSymbolExtension(extension))
                                == 1
                            ):
                                _extensionQualities[-1] = _makeCiphered(
                                    _extensionQualities[-1],
                                    _makeJazzNoteLikeChordSymbolExtension(extension),
                                    _cipherTriggers,
                                )
                            _extensionQualities[
                                -1
                            ] = _extensionQualities[-1].replace(
                                _makeJazzNoteLikeChordSymbolExtension(extension),
                                makeTextMulticoloured(
                                    text=_makeJazzNoteLikeChordSymbolExtension(
                                        extension
                                    ),
                                    colourTags=[
                                        Key(rootKey, JazzNote(note))
                                        .inAllFlats()
                                        .getASCII()
                                        for note in _notes
                                    ], outlineColourTag = outlineColourTag,
                                ),
                                1,
                            )
                            _makeJazzNoteLikeChordSymbolExtension(extension)
                            if (
                                len(_makeJazzNoteLikeChordSymbolExtension(extension))
                                == 1
                            ):
                                _extensionQualities[-1] = _makeUnciphered(
                                    _extensionQualities[-1],
                                    _makeJazzNoteLikeChordSymbolExtension(extension),
                                )
                        else:  # this is a sus chord or a chord with no 3, 5
                            # input('are we here yet? {} triad = '.format(_chordSymbol, _triad))
                            _notes = [
                                n
                                for n in _inclusions
                                if n not in (_modifications + [_third, _fifth])
                            ]
                            if _makeStyled("ma") in _chordSymbol:
                                pass
                                """input('anybody out there? {} {}'.format(self.getChordQuality(),_extensionQualities[-1]))
                                _extensionQualities[-1] = _extensionQualities[-1].replace(
                                    _makeStyled('ma'),makeTextMulticoloured(
                                        text=_makeStyled('ma'),
                                    colourTags=[Key(rootKey, JazzNote(note)).inAllFlats().getASCII() for note in ('3','7') if JazzNote(note) in self]))"""

                    if "dim7" in _makePlain(_chordSymbol):
                        '''if self.getChordQuality() == _chordSymbol:
                            input('\ndim7 thing is happening {} {} {}'.format(
                                _chordSymbol, _seventh, extension))'''
                        _extensionQualities[-1] = _makeCiphered(
                            _extensionQualities[-1], 7, _cipherTriggers
                        )
                        _extensionQualities[-1] = _extensionQualities[
                            -1
                        ].replace(
                            "7",
                            makeTextMulticoloured(
                                "7",
                                [Key(rootKey, JazzNote("6")).inAllFlats().getASCII()],
                                outlineColourTag=outlineColourTag,
                            ),
                        )
                        _extensionQualities[-1] = _makeUnciphered(
                            _extensionQualities[-1], 7
                        )

                    else:
                        pass  # if 'dim' in _extensionQualities[-1]:
                        #    input(' got here now.#{} chord: {} triad: {} extension: {} not in thing:{}'.format(self.getChangeNumber(),_chordSymbol,_triad,extension,_extensionQualities[-1]))
                    """if '6/9' in _extensionQualities[-1]:
                                            input('6/9 in ' + self)
                                            _baseExtension = '6/9'
                                            _extensionQualities[-1] = makeTextMulticoloured(
                                                _extensionQualities[-1], colourTags=Key(rootKey, JazzNote('b2')))
                                        else:
                                            #input('6/9 not in ' + _extensionQualities[-1])
                                            _baseExtension = _makePlain(_extensionQualities[-1]).index(_triad)"""

                else:  # triad unknown? C6(♭5 no 3)


                    if extension in _chordSymbol:
                        _notes = [n for n in _inclusions if n not in _modifications]
                        _notes = [
                            n.note
                            for n in Change(_notes).sortBySemitonePosition(
                                octaveLimit=1
                            )
                        ]
                        if (
                            JazzNote(extension).semitonesFromOne(octaveLimit=2) >= 12
                            and _makeStyled("ma") in _chordSymbol
                        ):

                            _extensionQualities[
                                -1
                            ] = _extensionQualities[-1].replace(
                                _makeStyled("ma"),
                                makeTextMulticoloured(
                                    _makeStyled("ma"),
                                    [
                                        Key(rootKey, JazzNote(n)).getASCII()
                                        for n in ("3", "7")
                                        if JazzNote(n) in self
                                    ], outlineColourTag = outlineColourTag,
                                ),
                            )
                            if "3" in _notes:
                                _notes.remove("3")
                            if "7" in _notes:
                                _notes.remove("7")
                        # print('inside getChordQuality() ',self.getChangeNumber(),self,_chordSymbol,_notes)

                        if (
                            all(n in _notes for n in ("3", "5", "7"))
                            and _makeStyled("ma") + "7" in _chordSymbol
                        ):
                            _extensionQualities[
                                -1
                            ] = _extensionQualities[-1].replace(
                                _makeStyled("ma"),
                                makeTextMulticoloured(
                                    _makeStyled("ma"),
                                    colourTags=[
                                        Key(rootKey, JazzNote(note))
                                        .inAllFlats()
                                        .getASCII()
                                        for note in ("3", "5")
                                    ], outlineColourTag = outlineColourTag,
                                ),
                            )
                            _extensionQualities[-1] = _makeCiphered(
                                _extensionQualities[-1], "7", _cipherTriggers
                            )
                            _extensionQualities[
                                -1
                            ] = _extensionQualities[-1].replace(
                                "7",
                                makeTextMulticoloured(
                                    "7",
                                    colourTags=[
                                        Key(rootKey, JazzNote(note))
                                        .inAllFlats()
                                        .getASCII()
                                        for note in ("7",)
                                    ], outlineColourTag = outlineColourTag,
                                ),
                            )
                            _extensionQualities[-1] = _makeUnciphered(
                                _extensionQualities[-1], "7"
                            )
                        else:

                            _extensionQualities[
                                -1
                            ] = _extensionQualities[-1].replace(
                                _makeJazzNoteLikeChordSymbolExtension(extension),
                                makeTextMulticoloured(
                                    _makeJazzNoteLikeChordSymbolExtension(extension),
                                    colourTags=[
                                        Key(rootKey, JazzNote(note))
                                        .inAllFlats()
                                        .getASCII()
                                        for note in _notes
                                    ], outlineColourTag = outlineColourTag,
                                ),
                            )
                        print(
                            '#{}: finding "{}" in  "{}", and so skipping this triad.  Extension={}"'.format(
                                self.getChangeNumber(),
                                _makeJazzNoteLikeChordSymbolExtension(extension),
                                _extensionQualities[-1],
                                extension,
                            )
                        )
                    elif _makeJazzNoteLikeChordSymbolExtension(extension) in _chordSymbol and '7' in extension:
                        pass
                        _extensionQualities[-1] = _makeCiphered(_extensionQualities[-1],_makeJazzNoteLikeChordSymbolExtension(extension),_cipherTriggers)
                        _extensionQualities[-1] = _extensionQualities[-1].replace(
                            _makeJazzNoteLikeChordSymbolExtension(extension),
                            makeTextMulticoloured(_makeJazzNoteLikeChordSymbolExtension(extension),
                                colourTags=[Key('C').onJazz(note).inAllFlats().getASCII() for note in _inclusions],
                                                        outlineColourTag = outlineColourTag,)
                        )
                        
                        #if _chordSymbol == self.getChordQuality(): input(
                        #    'we are here ' + _chordSymbol + ' #' + str(self.getChangeNumber()))

                # Brackets
                _bracketNotes = _modifications + _additions
                _bracketNotes.sort(key=len, reverse=False)
                for t in Utility.numToCipher:
                    trigger = Utility.numToCipher[t]
                    
                    _extensionQualities[-1] = _extensionQualities[-1].replace(trigger,str(t))
                    #print('bigger')
                    #input(_extensionQualities[-1])
                for note in _bracketNotes:
                    for preeceedingChar in (" ", "(", "+", "-"):
                        _extensionQualities[-1] = _extensionQualities[
                            -1
                        ].replace(
                            preeceedingChar + _makeStyled(note),
                            preeceedingChar
                            + makeTextMulticoloured(
                                text=_makeStyled(note),
                                colourTags=[
                                    Key(rootKey, JazzNote(note)).inAllFlats().getASCII()
                                ], outlineColourTag = outlineColourTag,
                            ),
                        )
                    
                if "(" in _extensionQualities[-1]:
                    _bracketsPart = _extensionQualities[-1][
                        _extensionQualities[-1].index("(") + 1 : -1
                    ]
                _totalColoursUsed = []
                for i in self.withoutNote('1').getSemitones():
                    if '='+Key.allFlats[i]+"," in _extensionQualities[-1]:
                        pass
                    elif '('+ Key.allFlats[i] +')' in _extensionQualities[-1]:
                        pass
                    elif _chordSymbol == self.getChordQuality():
                        pass
                        '''
                        err_str = '{}\n\n {} \nChange {} {}'.format(
                            _extensionQualities[-1],_chordSymbol,self.getChangeNumber(),
                        '\nLooking for: '+ '='+Key.allFlats[i]+",")
                        raise ValueError(err_str)'''
                #Outline any uncoloured Parts
                _openCurlies = 0
                _insideCommand = False

                _strsToOutline = Utility.removeNestedParentheses(_extensionQualities[-1],('{','}')).split('\\textpdfrender')
                _strsToOutline = [i.replace(r'\pgfplotsset\TextShadeContour', '') for i in
                                  _strsToOutline if i != '']
                for s in _strsToOutline:
                    if s in (' ',''): continue
                    _indexes = Utility.allIndexes(_extensionQualities[-1],s)

                    if len(_indexes) > 1:
                        #input('here "{}" end of thing "{}"'.format(s,_extensionQualities[-1][-10:]))
                        _indexes = [i for i in _indexes if
                                    _extensionQualities[-1][i - 1] == '}']  # Just closed a tag, so likely to be good
                        print('\nstarcluster',_strsToOutline,_indexes,s,_extensionQualities[-1],sep='\n\n')


                        if len(_indexes) > 1:
                            input('more than one occurence of {}'.format(s))
                            raise TypeError('Figure it out')
                        #input(_extensionQualities[-1])
                        _replacement = Latex.outlineText(s,colourTag=False,strokeColourTag=outlineColourTag,lineWidth=0.5)
                        _extensionQualities[-1] = _extensionQualities[-1][:_indexes[0]] + _replacement +  _extensionQualities[-1][_indexes[0] + len(s):]
                        #input('there "{}" end of thing "{}"'.format(s,_extensionQualities[-1][-10:]))
                        #input(self.getChordQuality())
                    else:
                        '''input('here\n{}\nWe are going to replace {}\n\n\n{}'.format(
                            _extensionQualities[-1],s,
                            _extensionQualities[-1].replace(
                                s,
                                Latex.outlineText(s, colourTag=False, outlineColourTag=outlineColourTag, lineWidth=0.5))
                        ))'''
                        if s in (')',' )'):
                            pass
                            #input('yesyesyes: substr: "{}" count: {}\n{}\n'.format(s, _extensionQualities[-1].count(s),
                            #                                                    _extensionQualities[-1]))
                        #print('replaced',s)
                        _extensionQualities[-1] = _extensionQualities[-1].replace(
                            s,Latex.outlineText(s,colourTag=False,strokeColourTag=outlineColourTag,lineWidth=0.5))


                #input('\nwhat she said was\n{}\nthzt wzx what she said'.format(_extensionQualities[-1]))
                
                
        # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
        def argsort(seq):
            return sorted(range(len(seq)), key=seq.__getitem__)

        rankedExtensionIndexes = argsort(naturalExtensionsRating)

        if printDebugInfo == True:
            for index in rankedExtensionIndexes:
                print(
                    _extensionQualities[index],
                    naturalExtensionsRating[index],
                    "inclusions = ",
                    naturalExtensionsInclusions[index],
                    "exclusions = ",
                    naturalExtensionsExclusions[index],
                    "additions = ",
                    naturalExtensionsAdditions[index],
                    ": modifications = ",
                    naturalExtensionsModifications[index],
                )

        if len(rankedExtensionIndexes) >= 1:
            _str = _extensionQualities[rankedExtensionIndexes[0]]
        else:
            if self.containsNotes("b6"):
                _str = "mi6th"
            else:
                raise ValueError(
                    "apparently this chord doesn't exist..",
                    self,
                )

        if utiliseCaching:  # will chache based on coloured vs. uncoloured

            if True or cachedName not in Change.cache.keys():
                #Change.cache[cachedName] = {}
                Change.cache[cachedName] = _str

        Chord.qualityDefaults['useHalfDiminishedUnicodeSymbols'] = __useHalfDiminishedUnicodeSymbolsDefault
        Chord.qualityDefaults['useDiminishedUnicodeSymbols'] = __useDiminishedUnicodeSymbolsDefault
        if returnAllCandidates:
            return _extensionQualities[1:]
        else:
            if makeTextMulticoloured:

                """#callerParameters['makeTextMulticoloured'] = False
                majorTriad = Change(['1','3','5'])
                #_majorTriadText = Change(['1','b3','5']).getChordQuality(callerParameters)
                _majorTriadStrings = ['Ma','ma']
                _minorTriadStrings = ['mi','-']
                _augTriadStrings = ['aug','Aug',Unicode.chars['augmented chord']]
                _dimTriadStrings = ['dim',Unicode.chars['diminished chord']]
                _halfDimTriadStrings = ['halfdim',Unicode.chars['half diminished chord']]
                _maSevenTriangle = Unicode.chars['Major Seventh Triangle']"""

                """_str = makeTextMulticoloured(
                    text = _str, 
                    colourTags = [Key(k).inAllFlats().getASCII() for k in self.byWays(rootKey)]
                )"""
                # input('chord quality is {}'.format(_str))
                # input(_str)

            return _str

    def OldgetChordQuality(self):  # Work here
        # Some way to compare how many alterations from a stock chord symbol
        # Then it would pick them in some order
        # Look through some traids
        # _changeSemitones = self.modeInSemitones(0,octaveLimit=False)
        # First it will look if a 7th chord fits
        # If not it will look for a triad
        # Next it will look for a power chord

        j = JazzNote

        _noFive = True
        _triad = False
        _seventhChord = False
        _ninthChord = False
        _eleventhChord = False
        _thirteenthChord = False
        _upperChord = False
        _highestNoteWithoutAccidentals = False
        _ninth = False
        _third = False
        _fifth = False
        _eleventh = False
        _seventh = False
        _sixth = False
        # This will be the added notes
        _chordSymbol = ""
        _notesToAdd = []
        _notesToRemove = []
        _notesToModify = []
        _notesRemaining = []
        for i in self.notes:
            _notesRemaining.append(i)
        _notesRemaining = Change(_notesRemaining)
        _notesRemaining = _notesRemaining.withoutNote("1")
        # A major third makes it major
        if len(self.notes) == 1:
            return "unison"

        # Diads will return the interval
        elif len(self.notes) == 2:
            if self.containsNotes("b2"):
                return "mi 2nd"
            if self.containsNotes("2"):
                return "ma 2nd"
            if self.containsNotes("b3", byAnotherName=False):
                return "mi 3rd"
            if self.containsNotes("#2", byAnotherName=False):
                return "aug 2nd"
            if self.containsNotes("3"):
                return "ma 3rd"
            if self.containsNotes("4"):
                return "p 4th"
            if self.containsNotes("#4", byAnotherName=False):
                return "aug 4th"
            if self.containsNotes("b5", byAnotherName=False):
                return "dim 5th"
            if self.containsNotes("5"):
                return "p 5th"
            if self.containsNotes("b6", byAnotherName=False):
                return "mi 6th"
            if self.containsNotes("#5", byAnotherName=False):
                return "aug 5th"
            if self.containsNotes("6"):
                return "ma 6th"
            if self.containsNotes("#6", byAnotherName=False):
                return "aug 6th"
            if self.containsNotes("b7", byAnotherName=False):
                return "mi 7th"
            if self.containsNotes("7"):
                return "ma 7th"

        # Check about the "5"
        if self.containsNotes("5"):
            _fifth = "5"
            _notesRemaining = _notesRemaining.withoutNote("5")
            if self.containsNotes("#4"):
                _notesToAdd.append("#4")
                _notesRemaining = _notesRemaining.withoutNote("#4")
            if self.containsNotes("b6"):
                _notesToAdd.append("b6")
                _notesRemaining = _notesRemaining.withoutNote("b6")
        if self.containsNotes("#5"):
            if not _fifth:
                _fifth = "#5"
                _notesToModify.append("#5")
                _notesRemaining = _notesRemaining.withoutNote("#5")
                if False:  # self.containsNotes('b5'):

                    _notesToAdd.append("#11")
                    _notesRemaining = _notesRemaining.withoutNote("#4")

        if self.containsNotes("b5"):
            if not _fifth:
                _fifth = "b5"
                _notesToModify.append("b5")
                _notesRemaining = _notesRemaining.withoutNote("b5")

        if not _fifth:
            _notesToRemove.append("5")

        # Check about the triadic third
        if self.containsNotes("3"):
            _third = "3"
            _notesRemaining = _notesRemaining.withoutNote("3")
        # If it also has the b3 then that is a sharp two
        if self.containsNotes("b3"):
            if self.containsNotes("3"):
                _notesToAdd.append("#9")
                _notesRemaining = _notesRemaining.withoutNote("b3")
            else:
                _third = "b3"
                _notesRemaining = _notesRemaining.withoutNote("b3")
        if not _third in ("b3", "3"):
            if self.containsNotes("4"):
                _third = "4"
                _notesRemaining = _notesRemaining.withoutNote("4")
            if self.containsNotes("2"):
                if not _third:
                    _third = "2"
                    _notesRemaining = _notesRemaining.withoutNote("2")
                else:  # is sus4 HERE take out the notes to add
                    if not _notesRemaining.containsNotes("2"):
                        _notesToAdd.append("9")
                        _notesRemaining = _notesRemaining.withoutNote("2")
            if self.containsNotes("#4") and not _third:
                if _fifth != "b5":
                    _third = "#4"
                    _notesRemaining = _notesRemaining.withoutNote("#4")

            if self.containsNotes("b2") and not _third:
                if not _third:
                    _third = "b2"
                    _notesRemaining = _notesRemaining.withoutNote("b2")
        if not _third:
            _notesToRemove.append("3")

        # Check out the seventh
        if self.containsNotes("7"):
            _seventh = "7"
            _notesRemaining = _notesRemaining.withoutNote("7")
            if self.containsNotes("b7"):
                _notesToAdd.append("b7")  ##13
                _notesRemaining = _notesRemaining.withoutNote("b7")
        elif self.containsNotes("b7"):
            _seventh = "b7"
            _notesRemaining = _notesRemaining.withoutNote("b7")

        # Check out the six
        if self.containsNotes("6"):
            _sixth = "6"
            _notesRemaining = _notesRemaining.withoutNote("6")

        # Assign a triad
        if _third == "3":
            _triad = "ma"
            _notesRemaining = _notesRemaining.withoutNote("3")
            if _fifth == "#5":
                pass
        # _triad = 'aug'
        # _notesToModify.remove('#5')
        elif _third == "b3":
            _triad = "mi"
            _notesRemaining = _notesRemaining.withoutNote("b3")
            if _fifth == "b5":
                _triad = "dim"
                _notesToModify.remove("b5")
                if _seventh == "b7":
                    _triad = "halfdim"
        elif _third == "4":
            _triad = "sus4"
            _notesRemaining = _notesRemaining.withoutNote("4")
        elif _third == "2":
            # Part about how if the 2 (9) links up to the 11 or 13
            # This note would get changed to the 9th
            # The only way that this note would get upgraded to an extension
            # Is if the extensions above it, starting with the highest natural
            # In the sequence (7 9 11 13) has less than (something) extensions
            # missing under it
            # Devise a way to say: does this note want to go up
            _triad = "sus2"
            _notesRemaining = _notesRemaining.withoutNote("2")
        elif _third == "#4":
            _triad = "sus#4"
            _notesRemaining = _notesRemaining.withoutNote("#4")
            if "b5" in _notesToModify:
                _notesToModify.remove("b5")
            if "#4" in _notesToModify:
                _notesToModify.remove("#4")
            if "b5" in _notesToAdd:
                _notesToAdd.remove("b5")
            if "#4" in _notesToAdd:
                _notesToAdd.remove("#4")
        elif _third == "b2":
            _triad = "susb2"
            _notesRemaining = _notesRemaining.withoutNote("b2")
            if "b2" in _notesToModify:
                _notesToModify.remove("b2")
            if "b2" in _notesToAdd:
                _notesToAdd.remove("b2")
        if not _triad:
            if self.containsNotes("5"):
                if not _sixth and not _seventh:
                    _triad = "5"
                    if "3" in _notesToRemove:
                        _notesToRemove = _notesToRemove.remove("3")
        # grab the ninth
        if self.containsNotes("2") and not _third == "2":
            _ninth = "9"
        if not _ninth and self.containsNotes("#2") and not _third in ("#2", "b3", "#9"):
            _ninth = "#9"
        if not _ninth and self.containsNotes("b2") and not _third in ("b2", "b9"):
            _ninth = "b9"
        # grab the eleventh
        if self.containsNotes("4") and not _third == "4":
            _eleventh = "11"
        if (
            not _eleventh
            and self.containsNotes("#4")
            and not _third == "#4"
            and not _fifth == "b5"
        ):
            _eleventh = "#11"
        # grab the thirteen call it the sixth
        if self.containsNotes("6"):
            _sixth = "6"
        if self.containsNotes("b6") and not _fifth == "#5" and not _sixth:
            # _sixth = 'b6' #I just tried this
            pass
            # _sixth = 'b6'
        # Add nines and shit

        # Check for b2 if not a sus b2
        if not _triad == "susb2":
            if self.containsNotes("b2"):
                if _seventhChord:
                    _notesToAdd.append("b9")
                else:
                    _notesToAdd.append("b9")
        if not _triad == "sus2":
            if self.containsNotes("2"):
                if _seventhChord:
                    _notesToAdd.append("9")
                else:
                    _notesToAdd.append("9")
        if not _triad == "sus4":
            if self.containsNotes("4"):
                if _seventhChord:
                    if "11" or "4" not in _notesToAdd:
                        _notesToAdd.append("11")
                else:
                    _notesToAdd.append("11")
        if not (_triad == "sus#4" or _triad == "dim" or _fifth == "b5"):
            if self.containsNotes("#4"):
                if (
                    _seventhChord
                    and not "#4" in _notesToAdd
                    and not "#11" in _notesToAdd
                ):
                    _notesToAdd.append("#11")  # contains #4 and 7
                elif (
                    not _seventhChord
                    and not "#4" in _notesToAdd
                    and not "#11" in _notesToAdd
                ):
                    _notesToAdd.append("#11")  # contains  #4 but no 7

        # Build seventh, ninth, eleventh, thirteenth chord from triad plus 7th
        if _seventh == "b7":
            _seventhChord = "7"
            _highestNoteWithoutAccidentals = _seventhChord

        elif _seventh == "7":
            _seventhChord = "ma7"
            _highestNoteWithoutAccidentals = _seventhChord

        if _seventhChord:

            if _ninth == "9" or _ninth == "2":
                # print('before removing add 9', _notesToAdd, _notesRemaining)
                if "9" in _notesToAdd:
                    _notesToAdd.remove("9")
                if "2" in _notesToAdd:
                    _notesToAdd.remove("2")
                _notesRemaining = _notesRemaining.withoutNote("2")
                _notesRemaining = _notesRemaining.withoutNote("9")
                if "2" in _notesToAdd:
                    _notesToAdd.remove("2")
                if "9" in _notesToAdd:
                    _notesToAdd.remove("9")
                _notesRemaining = _notesRemaining.withoutNote("2")
                _notesRemaining = _notesRemaining.withoutNote("9")
                if _seventh == "7":
                    _ninthChord = "ma9"
                elif _seventh == "b7":
                    _ninthChord = "9"

                _highestNoteWithoutAccidentals = _ninth

            elif _ninth in ("b2", "b9", "#2", "#9"):
                # Swap the sus
                if _ninth in ("b2", "b9") and _triad == "sus2":
                    _notesToAdd.remove(_ninth)
                    _triad = "susb2"
                    _ninth = "9"

                if _eleventh in ("11", "ma11") or _sixth == "6":
                    while _ninth in _notesToAdd:
                        _notesToAdd.remove(_ninth)
                    _notesRemaining = _notesRemaining.withoutNote(_ninth)
                    if _seventh == "7":
                        _ninthChord = "ma" + _ninth
                    elif _seventh == "b7":
                        _ninthChord = _ninth
            # The next if checks if the ninth could be pulled out of the triad
            elif _ninth == False and _triad in ("sus2", "susb2"):
                # Check if changing the triad will make it more efficient
                if _eleventh in ("11", "ma11") or _sixth == "6":
                    pass
            # Next Line is new
            # elif _ninth:
            # 	if _eleventh == '11':
            # 		_eleventhChord = '11'
            # 		_notesToAdd.remove('11')
            # 		if _ninth in _notesToAdd:_notesToAdd.remove(_ninth)
            # 		#Maybe take next part out
            # Up to here
            if _sixth and not _sixth in _notesToAdd:
                _notesToAdd.append(_sixth)
        # print('a place a nine', _ninth, _ninthChord, _seventh,_seventhChord)
        # if _ninthChord or not _ninth == False:
        if _ninthChord:  # Original of one above
            if _eleventh in ("11", "4", "#11", "#4"):
                _notesRemaining = _notesRemaining.withoutNote(_eleventh)
                while _eleventh in _notesToAdd:
                    _notesToAdd.remove(_eleventh)
                if _eleventh in ("4", "11"):
                    _highestNoteWithoutAccidentals = _eleventh
                    while "11" in _notesToAdd:
                        _notesToAdd.remove("11")
                    while "4" in _notesToAdd:
                        _notesToAdd.remove("4")
                elif _eleventh in ("#4", "#11"):
                    if "#4" in _notesToAdd:
                        _notesToAdd.remove("#4")
                    if "#11" in _notesToAdd:
                        _notesToAdd.remove("#11")
                if _seventh == "b7":  # original
                    _eleventhChord = _eleventh
                elif _seventh == "7":  # ORiginal
                    _eleventhChord = "ma" + _eleventh
                if _ninth in ("b9", "#9"):
                    _notesToModify.append(_ninth)
                #
        if _eleventhChord:
            _notesRemaining = _notesRemaining.withoutNote("11")
            if _sixth:
                if _eleventhChord == "11":
                    _highestNoteWithoutAccidentals = "13"
                    _thirteenthChord = "13"
                    _notesRemaining = _notesRemaining.withoutNote("6")
                    while "6" in _notesToAdd:
                        _notesToAdd.remove("6")
                    while "bb7" in _notesToAdd:
                        _notesToAdd.remove("bb7")
                elif _eleventhChord == "ma11":
                    _thirteenthChord = "ma13"
                    _notesRemaining = _notesRemaining.withoutNote("6")
                    while "6" in _notesToAdd:
                        _notesToAdd.remove("6")
                    while "bb7" in _notesToAdd:
                        _notesToAdd.remove("bb7")
                elif "#11" in _eleventhChord:
                    if "#11" in _notesToAdd:
                        _notesToAdd.remove("#11")
                    _notesToModify.append("#11")
                    if _seventh == "7":
                        _thirteenthChord = "ma13"
                    elif _seventh == "b7":
                        _thirteenthChord = "13"
                _highestNoteWithoutAccidentals = "13"
        if _thirteenthChord:
            _notesRemaining = _notesRemaining.withoutNote("6")
            while "6" in _notesToAdd:
                _notesToAdd.remove("6")
            while "bb7" in _notesToAdd:
                _notesToAdd.remove("bb7")
        # if _highestNoteWithoutAccidentals in ('7','b7'):

        if True:
            _triadExtensionsToCheck = []
            _lingeringUpperExtensions = 0.0
            _ratingOfChordSymbol = [0.0, 0.0, 0.0, 0.0]
            _extensionsInOrder = [_seventh, _ninth, _eleventh, _sixth]
            _typesOfChords = ["seventh", "ninth", "eleventh", "thirteenth"]
            for i in range(len(_extensionsInOrder)):
                if _extensionsInOrder[i] in _notesToAdd:
                    # if _extensionsInOrder[i]!=False:
                    _lingeringUpperExtensions += 1.0
                    _ratingOfChordSymbol[i] += 1.0
                # elif _extensionsInOrder[i] == False:
                else:
                    _ratingOfChordSymbol[i] -= 1.0
                    _triadExtensionsToCheck.append(i)

                if _triadExtensionsToCheck != []:
                    for triadExtension in _triadExtensionsToCheck:
                        if JazzNote.isJazzNoteStr(triadExtension):
                            if self.containsNotes(triadExtension):
                                print("found something")

            # print('rating',_typesOfChords[i],_ratingOfChordSymbol[i])
            # could sub in the traidic third for a ninth or eleventh
            # _lingeringUpperExtensions+=.9
        # print('thing',min(_ratingOfChordSymbol),_typesOfChords[_ratingOfChordSymbol.index(min(_ratingOfChordSymbol))])
        # print('which chord',_ratingOfChordSymbol)
        # print('highest interval', _highestNoteWithoutAccidentals)

        # if True or eleventh != False:
        # Display status of upper extensions
        # print(self,'is a ',_triad,'chord and has a',_highestNoteWithoutAccidentals, 'uppers: ',_lingeringUpperExtensions)

        # 		elif _sixth:
        # 			_seventhChord = _sixth

        # Call a seventh a six

        if type(_triad) == str:
            if _seventhChord or _ninthChord or _eleventhChord or _thirteenthChord:
                if _thirteenthChord:
                    _upperChord = _thirteenthChord
                elif _eleventhChord:
                    _upperChord = _eleventhChord
                elif _ninthChord:
                    _upperChord = _ninthChord
                else:
                    _upperChord = _seventhChord
                if _triad == "ma":
                    _chordSymbol += _upperChord
                elif "sus" in _triad:
                    _chordSymbol += _upperChord
                    # if _sixth: _chordSymbol += _sixth
                    _chordSymbol += _triad
                else:
                    _chordSymbol += _triad
                    if _triad == "dim":
                        if _seventh == "b7":
                            _triad = "halfdim"
                    _chordSymbol += _upperChord
                if _sixth and not _thirteenthChord and not _sixth in _notesToAdd:
                    _notesToAdd.append(_sixth)
            else:  # Not a seventh  or thirteenth chord

                if _sixth and "sus" in _triad:
                    _chordSymbol += _sixth + _triad
                else:
                    _chordSymbol += _triad
                    if _sixth:
                        _chordSymbol += _sixth
        elif not _triad:
            if _seventh:
                _chordSymbol += _seventhChord
            elif _sixth:
                _chordSymbol += _sixth
        # 			else:
        # 				_chordSymbol += _triad
        # print('information: ninth =', _ninth, 'Eleventh =', _eleventh, 'Sixth = ', _sixth, 'third', _third,
        #     '\n 7th chord :', _seventhChord, 'triad', _triad, 'notes to add', _notesToAdd)

        # print('seventhChord', _seventhChord, 'notesToAdd',_notesToAdd,'notesToRemove',_notesToRemove,'remaining notes', _notesRemaining)
        # Find the least modifications in chord symbol

        if _seventhChord:
            pass

        if _notesToAdd or _notesToRemove or _notesToModify:
            _chordSymbol += "("
            if _notesToModify:

                for note in range(len(_notesToModify)):
                    _chordSymbol += _notesToModify[note]
                    if note != len(_notesToModify) - 1:
                        _chordSymbol += " "
            if _notesToRemove:
                if _notesToModify:
                    _chordSymbol += ", "
                _chordSymbol += "no "
                for note in range(len(_notesToRemove)):
                    _chordSymbol += _notesToRemove[note]
                    if note != len(_notesToRemove) - 1:
                        _chordSymbol += " "

            if _notesToAdd:
                # Turn notes to add into a change to sort it
                _changeToAddSorted = Change(_notesToAdd).sortBySemitonePosition()
                if _notesToModify or _notesToRemove:
                    _chordSymbol += ", "
                _chordSymbol += "add "
                for note in range(len(_changeToAddSorted)):
                    _chordSymbol += str(_changeToAddSorted.notes[note])
                    if note != len(_notesToAdd) - 1:
                        _chordSymbol += " "

            _chordSymbol += ")"
        if "dim6" in _chordSymbol:
            _chordSymbol = _chordSymbol.replace("dim6", "dim7")
        _chordSymbol = _chordSymbol.replace("#", "♯")
        _chordSymbol = _chordSymbol.replace("b", "♭")
        _chordSymbol = _chordSymbol.replace("halfdim", "⌀")
        _chordSymbol = _chordSymbol.replace("dim", "°")  # oᴼ
        # print(str(self), _chordSymbol, 'thirteenth chord', _thirteenthChord)
        # print('triad: ',_triad,'seventhChord: ', _seventhChord,'notesRemaining: ', _notesRemaining,'third: ',_third,'fifth: ',_fifth, 'seventh:',_seventh, 'sixth',_sixth, 'ninth',_ninth,sep = '\n',end ='\n')
        return _chordSymbol

    def OldgetChordQualityOriginal(self):  # Work here
        # Some way to compare how many alterations from a stock chord symbol
        # Then it would pick them in some order
        # Look through some traids
        # _changeSemitones = self.modeInSemitones(0,octaveLimit=False)
        # First it will look if a 7th chord fits
        # If not it will look for a triad
        # Next it will look for a power chord

        j = JazzNote

        _noFive = True
        _triad = False
        _seventhChord = False
        _ninthChord = False
        _eleventhChord = False
        _thirteenthChord = False
        _upperChord = False
        _ninth = False
        _third = False
        _fifth = False
        _eleventh = False
        _seventh = False
        _sixth = False
        # This will be the added notes
        _chordSymbol = ""
        _notesToAdd = []
        _notesToRemove = []
        _notesToModify = []
        _notesRemaining = []
        for i in self.notes:
            _notesRemaining.append(i)
        _notesRemaining = Change(_notesRemaining)
        _notesRemaining = _notesRemaining.withoutNote("1")
        # A major third makes it major
        if len(self.notes) == 1:
            return "unison"

        # Diads will return the interval
        elif len(self.notes) == 2:
            if self.containsNotes("b2"):
                return "mi 2nd"
            if self.containsNotes("2"):
                return "ma 2nd"
            if self.containsNotes("b3", byAnotherName=False):
                return "mi 3rd"
            if self.containsNotes("#2", byAnotherName=False):
                return "aug 2nd"
            if self.containsNotes("3"):
                return "ma 3rd"
            if self.containsNotes("4"):
                return "p 4th"
            if self.containsNotes("#4", byAnotherName=False):
                return "aug 4th"
            if self.containsNotes("b5", byAnotherName=False):
                return "dim 5th"
            if self.containsNotes("5"):
                return "p 5th"
            if self.containsNotes("b6", byAnotherName=False):
                return "mi 6th"
            if self.containsNotes("#5", byAnotherName=False):
                return "aug 5th"
            if self.containsNotes("6"):
                return "ma 6th"
            if self.containsNotes("#6", byAnotherName=False):
                return "aug 6th"
            if self.containsNotes("b7", byAnotherName=False):
                return "mi 7th"
            if self.containsNotes("7"):
                return "ma 7th"

        # Check about the "5"
        if self.containsNotes("5"):
            _fifth = "5"
            _notesRemaining = _notesRemaining.withoutNote("5")
            if self.containsNotes("#4"):
                _notesToAdd.append("#4")
                _notesRemaining = _notesRemaining.withoutNote("#4")
            if self.containsNotes("b6"):
                _notesToAdd.append("b6")
                _notesRemaining = _notesRemaining.withoutNote("b6")
        if self.containsNotes("#5"):
            if not _fifth:
                _fifth = "#5"
                _notesToModify.append("#5")
                _notesRemaining = _notesRemaining.withoutNote("#5")
                if False:  # self.containsNotes('b5'):

                    _notesToAdd.append("#11")
                    _notesRemaining = _notesRemaining.withoutNote("#4")

        if self.containsNotes("b5"):
            if not _fifth:
                _fifth = "b5"
                _notesToModify.append("b5")
                _notesRemaining = _notesRemaining.withoutNote("b5")

        if not _fifth:
            _notesToRemove.append("5")

        # Check about the triadic third
        if self.containsNotes("3"):
            _third = "3"
            _notesRemaining = _notesRemaining.withoutNote("3")
        # If it also has the b3 then that is a sharp two
        if self.containsNotes("b3"):
            if self.containsNotes("3"):
                _notesToAdd.append("#9")
                _notesRemaining = _notesRemaining.withoutNote("b3")
            else:
                _third = "b3"
                _notesRemaining = _notesRemaining.withoutNote("b3")
        if not _third in ("b3", "3"):
            if self.containsNotes("4"):
                _third = "4"
                _notesRemaining = _notesRemaining.withoutNote("4")
            if self.containsNotes("2"):
                if not _third:
                    _third = "2"
                    _notesRemaining = _notesRemaining.withoutNote("2")
                else:  # is sus4 HERE take out the notes to add
                    if not _notesRemaining.containsNotes("2"):
                        _notesToAdd.append("9")
                        _notesRemaining = _notesRemaining.withoutNote("2")
            if self.containsNotes("#4"):
                if _fifth != "b5":
                    _third = "#4"
                    _notesRemaining = _notesRemaining.withoutNote("#4")

            if self.containsNotes("b2"):
                if not _third:
                    _third = "b2"
                    _notesRemaining = _notesRemaining.withoutNote("b2")
        if not _third:
            _notesToRemove.append("3")

        # Check out the seventh
        if self.containsNotes("7"):
            _seventh = "7"
            _notesRemaining = _notesRemaining.withoutNote("7")
            if self.containsNotes("b7"):
                _notesToAdd.append("b7")  ##13
                _notesRemaining = _notesRemaining.withoutNote("b7")
        elif self.containsNotes("b7"):
            _seventh = "b7"
            _notesRemaining = _notesRemaining.withoutNote("b7")

        # Check out the six
        if self.containsNotes("6"):
            _sixth = "6"
            _notesRemaining = _notesRemaining.withoutNote("6")

        # Assign a triad
        if _third == "3":
            _triad = "ma"
            _notesRemaining = _notesRemaining.withoutNote("3")
            if _fifth == "#5":
                pass
        # _triad = 'aug'
        # _notesToModify.remove('#5')
        elif _third == "b3":
            _triad = "mi"
            _notesRemaining = _notesRemaining.withoutNote("b3")
            if _fifth == "b5":
                _triad = "dim"
                _notesToModify.remove("b5")
                if _seventh == "b7":
                    _triad = "halfdim"
        elif _third == "4":
            _triad = "sus4"
            _notesRemaining = _notesRemaining.withoutNote("4")
        elif _third == "2":
            _triad = "sus2"
            _notesRemaining = _notesRemaining.withoutNote("2")
        elif _third == "#4":
            _triad = "sus#4"
            _notesRemaining = _notesRemaining.withoutNote("#4")
            if "b5" in _notesToModify:
                _notesToModify.remove("b5")
            if "#4" in _notesToModify:
                _notesToModify.remove("#4")
            if "b5" in _notesToAdd:
                _notesToAdd.remove("b5")
            if "#4" in _notesToAdd:
                _notesToAdd.remove("#4")
        elif _third == "b2":
            _triad = "susb2"
            _notesRemaining = _notesRemaining.withoutNote("b2")
            if "b2" in _notesToModify:
                _notesToModify.remove("b2")
            if "b2" in _notesToAdd:
                _notesToAdd.remove("b2")
        if not _triad:
            if self.containsNotes("5"):
                if not _sixth and not _seventh:
                    _triad = "5"
                    if "3" in _notesToRemove:
                        _notesToRemove = _notesToRemove.remove("3")
        # grab the ninth
        if self.containsNotes("2") and not _third == "2":
            _ninth = "9"
        if not _ninth and self.containsNotes("b2") and not _third == "b2":
            _ninth = "b9"
        if not _ninth and self.containsNotes("#2") and not _third == "#2":
            _ninth = "#9"
        # grab the eleventh
        if self.containsNotes("4") and not _third == "4":
            _eleventh = "11"
        if (
            not _eleventh
            and self.containsNotes("#4")
            and not _third == "#4"
            and not _fifth == "b5"
        ):
            _eleventh = "#11"
        # grab the thirteen call it the sixth
        if self.containsNotes("6"):
            _sixth = "6"
        if self.containsNotes("b6") and not _fifth == "#5" and not _sixth:
            pass
            # _sixth = 'b6'
        # Add nines and shit

        # Check for b2 if not a sus b2
        if not _triad == "susb2":
            if self.containsNotes("b2"):
                if _seventhChord:
                    _notesToAdd.append("b9")
                else:
                    _notesToAdd.append("b9")
        if not _triad == "sus2":
            if self.containsNotes("2"):
                if _seventhChord:
                    _notesToAdd.append("9")
                else:
                    _notesToAdd.append("9")
        if not _triad == "sus4":
            if self.containsNotes("4"):
                if _seventhChord:
                    if "11" or "4" not in _notesToAdd:
                        _notesToAdd.append("11")
                else:
                    _notesToAdd.append("11")
        if not (_triad == "sus#4" or _triad == "dim" or _fifth == "b5"):
            if self.containsNotes("#4"):
                if (
                    _seventhChord
                    and not "#4" in _notesToAdd
                    and not "#11" in _notesToAdd
                ):
                    _notesToAdd.append("#11")  # contains #4 and 7
                elif (
                    not _seventhChord
                    and not "#4" in _notesToAdd
                    and not "#11" in _notesToAdd
                ):
                    _notesToAdd.append("#11")  # contains  #4 but no 7

        # Build seventh, ninth, eleventh, thirteenth chord from triad plus 7th
        if _seventh == "b7":
            _seventhChord = "7"
        elif _seventh == "7":
            _seventhChord = "ma7"

        if _seventhChord:
            if _ninth == "9" or _ninth == "2":
                # print('before removing add 9', _notesToAdd, _notesRemaining)
                if "9" in _notesToAdd:
                    _notesToAdd.remove("9")
                if "2" in _notesToAdd:
                    _notesToAdd.remove("2")
                _notesRemaining = _notesRemaining.withoutNote("2")
                _notesRemaining = _notesRemaining.withoutNote("9")
                if "2" in _notesToAdd:
                    _notesToAdd.remove("2")
                if "9" in _notesToAdd:
                    _notesToAdd.remove("9")
                _notesRemaining = _notesRemaining.withoutNote("2")
                _notesRemaining = _notesRemaining.withoutNote("9")
                if _seventh == "7":
                    _ninthChord = "ma9"
                elif _seventh == "b7":
                    _ninthChord = "9"

        # print('a place a nine', _ninth, _ninthChord, _seventh,_seventhChord)
        if _ninthChord:
            if _eleventh == "11":
                _notesRemaining = _notesRemaining.withoutNote("11")
                while "11" in _notesToAdd:
                    _notesToAdd.remove("11")
                while "4" in _notesToAdd:
                    _notesToAdd.remove("4")
                if _ninthChord == "9":
                    _eleventhChord = "11"
                elif _ninthChord == "ma9":
                    _eleventhChord = "ma11"
        if _eleventhChord:
            _notesRemaining = _notesRemaining.withoutNote("11")
            while "11" in _notesToAdd:
                _notesToAdd.remove("11")
            while "4" in _notesToAdd:
                _notesToAdd.remove("4")
            if _sixth:
                if _eleventhChord == "11":
                    _thirteenthChord = "13"
                    _notesRemaining = _notesRemaining.withoutNote("6")
                    while "6" in _notesToAdd:
                        _notesToAdd.remove("6")
                    while "bb7" in _notesToAdd:
                        _notesToAdd.remove("bb7")
                elif _eleventhChord == "ma11":
                    _thirteenthChord = "ma13"
                    _notesRemaining = _notesRemaining.withoutNote("6")
                    while "6" in _notesToAdd:
                        _notesToAdd.remove("6")
                    while "bb7" in _notesToAdd:
                        _notesToAdd.remove("bb7")

        if _thirteenthChord:
            _notesRemaining = _notesRemaining.withoutNote("6")
            while "6" in _notesToAdd:
                _notesToAdd.remove("6")
            while "bb7" in _notesToAdd:
                _notesToAdd.remove("bb7")

        # 		elif _sixth:
        # 			_seventhChord = _sixth

        # Call a seventh a six

        if type(_triad) == str:
            if _seventhChord or _ninthChord or _eleventhChord or _thirteenthChord:
                if _thirteenthChord:
                    _upperChord = _thirteenthChord
                elif _eleventhChord:
                    _upperChord = _eleventhChord
                elif _ninthChord:
                    _upperChord = _ninthChord
                else:
                    _upperChord = _seventhChord
                if _triad == "ma":
                    _chordSymbol += _upperChord
                elif "sus" in _triad:
                    _chordSymbol += _upperChord
                    # if _sixth: _chordSymbol += _sixth
                    _chordSymbol += _triad
                else:
                    _chordSymbol += _triad
                    if _triad == "dim":
                        if _seventh == "b7":
                            _triad = "halfdim"
                    _chordSymbol += _upperChord
                if _sixth and not _thirteenthChord and not _sixth in _notesToAdd:
                    _notesToAdd.append(_sixth)
            else:  # Not a seventh  or thirteenth chord

                if _sixth and "sus" in _triad:
                    _chordSymbol += _sixth + _triad
                else:
                    _chordSymbol += _triad
                    if _sixth:
                        _chordSymbol += _sixth
        elif not _triad:
            if _seventh:
                _chordSymbol += _seventhChord
            elif _sixth:
                _chordSymbol += _sixth
        # 			else:
        # 				_chordSymbol += _triad

        # print('seventhChord', _seventhChord, 'notesToAdd',_notesToAdd,'notesToRemove',_notesToRemove,'remaining notes', _notesRemaining)
        # Find the least modifications in chord symbol

        if _seventhChord:
            pass

        if _notesToAdd or _notesToRemove or _notesToModify:
            _chordSymbol += "("
            if _notesToRemove:

                _chordSymbol += "no "
                for note in range(len(_notesToRemove)):
                    _chordSymbol += _notesToRemove[note]
                    if note != len(_notesToRemove) - 1:
                        _chordSymbol += " "
            if _notesToModify:
                if _notesToRemove:
                    _chordSymbol += ", "
                for note in range(len(_notesToModify)):
                    _chordSymbol += _notesToModify[note]
                    if note != len(_notesToModify) - 1:
                        _chordSymbol += " "

            if _notesToAdd:
                # Turn notes to add into a change to sort it
                _changeToAddSorted = Change(_notesToAdd).sortBySemitonePosition()
                if _notesToModify or _notesToRemove:
                    _chordSymbol += ", "
                _chordSymbol += "add "
                for note in range(len(_changeToAddSorted)):
                    _chordSymbol += str(_changeToAddSorted.notes[note])
                    if note != len(_notesToAdd) - 1:
                        _chordSymbol += " "

            _chordSymbol += ")"
        if "dim6" in _chordSymbol:
            _chordSymbol = _chordSymbol.replace("dim6", "dim7")
        _chordSymbol = _chordSymbol.replace("#", "♯")
        _chordSymbol = _chordSymbol.replace("b", "♭")
        _chordSymbol = _chordSymbol.replace("halfdim", "⌀")
        _chordSymbol = _chordSymbol.replace("dim", "°")  # oᴼ
        print(str(self), _chordSymbol, "thirteenth chord", _thirteenthChord)
        # print('triad: ',_triad,'seventhChord: ', _seventhChord,'notesRemaining: ', _notesRemaining,'third: ',_third,'fifth: ',_fifth, 'seventh:',_seventh, 'sixth',_sixth, 'ninth',_ninth,sep = '\n',end ='\n')
        return _chordSymbol

    def getSemitoneSteps(self):
        if len(self) == 0:
            return []
        _semitoneSteps = []
        _octaves = (
            math.floor(self.sortBySemitonePosition().notes[-1].semitonesFromOne() / 12)
            + 1
        )
        _currentPosition = self.notes[0].semitonesFromOne()
        for i in range(1, len(self.notes)):
            _semitoneSteps.append(self.notes[i].semitonesFromOne() - _currentPosition)
            _currentPosition = self.notes[i].semitonesFromOne()
        _semitoneSteps.append(
            self.notes[0].semitonesFromOne() - _currentPosition + 12 * _octaves
        )
        return _semitoneSteps

    @classmethod
    def chordHasUpperCaseNumeral(cls, chordQuality: str):
        _lowerCaseChordTriggers = ["mi", "dim", "°", "ᴼ", "halfdim", "⌀"]

        if any(trigger in chordQuality for trigger in _lowerCaseChordTriggers):
            return False
        else:
            return True

    @classmethod
    def chordIsCapitalRoman(cls, _chordQuality):
        _lowerCaseChordTriggers = ["mi", "dim", "°", "ᴼ", "halfdim", "⌀"]
        if any(trigger in _chordQuality for trigger in _lowerCaseChordTriggers):
            return False
        else:
            return True

    def noteIsCapitalRoman(self, scaleDegree):
        """noteNumber is n where n is the nth note in the change"""
        _romanNumeral = ""
        _chordQuality = self.getScaleChord(scaleDegree, 2, 4, returnTypeChange=False)
        if Change.chordIsCapitalRoman(_chordQuality):
            return True
        else:
            return False

    def romanNumerals(
        self, useUnicodeAccidentals=True, useUnicodeNumerals=False, allowedNotes=None
    ):
        """returnSingleIndex is an int."""
        if allowedNotes == None:
            allowedNotes = Change.allowedNoteNamesJazz
        _romanNumerals = []
        _lowerCaseChordTriggers = ["mi", "dim", "°", "ᴼ", "halfdim", "⌀"]
        # _straightenedScale = self.straightenDegrees(allowedNotes)
        _straightenedScale = self.straightenDegrees(allowedNotes=allowedNotes)
        for note in _straightenedScale.notes:
            _romanNumerals.append(note.getRomanNumeral(useUnicodeNumerals))

            _chordQuality = _straightenedScale.getScaleChord(
                np.where(_straightenedScale.notes == note)[0][0], 2, 4
            )
            # _chordQuality = _straightenedScale.getScaleChord(_straightenedScale.notes.index(note),2,4)
            index_of_maximum = np.where(_straightenedScale.notes == note)
            if any(trigger in _chordQuality for trigger in _lowerCaseChordTriggers):
                _romanNumerals[-1] = _romanNumerals[-1].lower()
            if useUnicodeAccidentals:
                _romanNumerals[-1] = JazzNote.convertNoteToRealUnicodeStr(
                    _romanNumerals[-1], useAnyStr=True
                )
            if "mima" in _chordQuality or "mi ma" in _chordQuality:
                _romanNumerals[-1] = _romanNumerals[-1].lower()

        return _romanNumerals

    def getChangedNote(self, position) -> Change:
        """You input a note (in notesets, or JazzNote); if the change contains it, it is removed, if not, it is added then returned"""
        if type(position) == JazzNote:
            position = position.semitonesFromOne()
        _sts = self.getSemitones()
        if position in _sts:
            return self.withoutNotes(JazzNote.makeFromSet(position))
        else:
            return self.withAddedNotes(JazzNote.makeFromSet(position))

    def getRotation(self, steps):
        return Change(noteset=[(i + steps) % 12 for i in self.getSemitones()])

    def mode(
        self, modeNumber, octaveLimit=1, allowedNotes=[], straighten=False
    ) -> Change:
        if 0 <= modeNumber < len(self):
            pass
        else:
            raise ValueError("modeNNumber")
        if allowedNotes == []:
            allowedNotes = Change.allowedNoteNamesJazz
        _modeInSemitones = self.modeInSemitones(modeNumber, octaveLimit=octaveLimit)
        _newModeNotes = []
        for i in range(len(_modeInSemitones)):
            _newModeNotes.append(
                JazzNote.makeFromSet(_modeInSemitones[i], octaveLimit=octaveLimit)
            )

        _newModeChange = Change(_newModeNotes)
        if straighten:
            return _newModeChange.straightenDegrees(allowedNotes=allowedNotes)
        else:
            return _newModeChange

    def modeInSemitones(self, modeNumber, octaveLimit=1):  # 0 is the first mode
        # Add the '1' back in if and keep track of it
        _forcedTheOne = False
        _adjustedNotes = self.notes
        if not self.containsNotes("1"):
            _adjustedNotes = np.concatenate([[JazzNote("1")], self.notes])
            _forcedTheOne = True
        # Convert notes to notesets,
        _semitonePositions = [
            i.semitonesFromOne(octaveLimit=False) for i in _adjustedNotes
        ]
        # Make negatives positive and contrain to octaves
        _semitonePositions = [
            JazzNote.limitSemitonesToNumberOfOctaves(
                i, octaveLimit=octaveLimit, disableNegatives=True
            )
            for i in _semitonePositions
        ]
        # Check for duplicates
        if self.containsDuplicateNote():
            raise ValueError(
                "Mode requires there be no duplicates. There are duplicates in ",
                self.notes,
            )
        # Sort by order of notesets
        _semitonePositions.sort()
        # We will have to subtract the offest of the new root
        _offset = _semitonePositions[modeNumber] - _semitonePositions[0]
        # Now we subtract offset for all notes and modulus over octaveLimit
        for i in range(len(_semitonePositions)):
            _semitonePositions[i] = _semitonePositions[i] - _offset
            if _semitonePositions[i] < 0:
                _semitonePositions[i] += octaveLimit * 12
        # Now we shift the numbers
        for i in range(modeNumber):
            # _semitonePositions.insert(0, _semitonePositions.pop())#Backwards
            _semitonePositions.append(_semitonePositions.pop(0))
        # Now we remove the '1' if it was added
        if _forcedTheOne:
            return _semitonePositions[1:]

        return _semitonePositions

    def getMelaNumber(self):
        _page = self.getChangeNumber(
            decorateChapter=False, includeNormalisedPageForNegatives=False
        )
        from Raga import Raga
        if _page in Raga.pageFromMelaNumber:
            return str(Raga.pageFromMelaNumber.index(_page))
        else:
            return False

    def getContainedRagasOtherDirections(
        self,
        returnNames=False,
        returnIndexes=False,
        lookForOnlyOneDirection=None,
        returnRagasForRootlessChanges=True,
    ) -> list:

        if returnRagasForRootlessChanges == False and not self.containsNotes("1"):
            return []
        if lookForOnlyOneDirection is None:
            lookForOnlyOneDirection = False

        # _allNames = ScaleNames.namesBySequenceIndex[self.getChangeNumber(decorateChapter=False)]
        _allNames = self.getScaleNames(
            searchForDownward=False,
            searchForNegative=False,
            includeDownwardHexagram=False,
            rebindRootToNextNoteIfNoOne=False,
        )
        _indexes = []
        _ragaNames = []
        for name in _allNames:
            try: ScaleNames
            except NameError: from ScaleNames import ScaleNames
            for trigger in ScaleNames.ragaTriggerStrings:
                if trigger in name:
                    _indexes.append(
                        ScaleNames.otherDirectionsOfRaga(
                            name,
                            self,
                            returnRagaIndexes=True,
                            returnRagaNames=False,
                        )
                    )
                    _ragaNames.append(
                        ScaleNames.otherDirectionsOfRaga(
                            name, self, returnRagaIndexes=False, returnRagaNames=True
                        )
                    )

        if returnNames and not returnIndexes:
            return _ragaNames
        elif returnIndexes and not returnNames:
            return _indexes
        elif returnIndexes == True and returnNames == True:
            if len(_indexes) != len(_ragaNames):
                raise TypeError(
                    "Error. there are different number of names {} and indexes{}".format(
                        _ragaNames, _indexes
                    )
                )

        elif returnIndexes == False and returnNames == False:
            raise ValueError("You are not returning anything...")

    def modeNames(
        self,
        defaultWay="Hexagram Name",
        searchForNegative=False,
        searchForDownward=False,
        includeDownwardHexagram=False,
        rebindRootToNextNoteIfNoOne=True,
    ):
        # Add the '1' back in if and keep track of it
        _forcedTheOne = False
        _adjustedNotes = self.notes
        _adjustedSelf = self
        if not rebindRootToNextNoteIfNoOne and not self.containsNotes("1"):
            _adjustedNotes = [JazzNote("1")] + self.notes
            _adjustedSelf = Change(_adjustedNotes)
            _forcedTheOne = True
        _modeNames = []
        for i in range(len(_adjustedNotes)):
            _modeNames.append(
                _adjustedSelf.mode(i).getScaleNames(
                    defaultWay=defaultWay,
                    searchForNegative=searchForNegative,
                    searchForDownward=searchForDownward,
                    includeDownwardHexagram=False,
                    rebindRootToNextNoteIfNoOne=rebindRootToNextNoteIfNoOne,
                )[0]
            )
            # Get rid of negative hexagrams
            if (
                not includeDownwardHexagram
                and _adjustedSelf.getReverse().getHexagramName() in _modeNames[i]
            ):
                _modeNames[i] = _adjustedSelf.getHexagramName()
        if _forcedTheOne:
            _modeNames = [_modeNames[i] + " (no 1)" for i in _modeNames]

        return _modeNames

    def modeQuality(self, modeNumber,):
        return self.mode(modeNumber).getChordQuality()

    def getBraille(self, colourResult=False, useOnlyFFBraille=True, bottomToTop=False):
        from Braille import Braille

        if bottomToTop:
            raise TypeError("legacy option")
        # TODO: make convert to subChange change function to handle changes that are not in order
        _halfScales = self.divideScaleBy()
        _semitoneDistanceHalfScales = []
        _counter = 0
        for _halfScale in _halfScales:
            _semitoneDistanceHalfScales.append([])
            for _note in _halfScale.notes:
                _semitoneDistanceHalfScales[-1].append(
                    _note.semitonesFromOne(octaveLimit=False) - 6 * _counter
                )
                if bottomToTop == True:
                    if _semitoneDistanceHalfScales[-1][-1] == 0:
                        _semitoneDistanceHalfScales[-1][-1] = 4
                    elif _semitoneDistanceHalfScales[-1][-1] == 1:
                        _semitoneDistanceHalfScales[-1][-1] = 5
                    elif _semitoneDistanceHalfScales[-1][-1] == 4:
                        _semitoneDistanceHalfScales[-1][-1] = 0
                    elif _semitoneDistanceHalfScales[-1][-1] == 5:
                        _semitoneDistanceHalfScales[-1][-1] = 1
            if bottomToTop == True:
                _semitoneDistanceHalfScales[-1].sort()
            _counter += 1
        # print('inside getBraille.. _stdhalfscales=',_semitoneDistanceHalfScales)
        _braille = []
        for i, _halfScale in enumerate(_semitoneDistanceHalfScales):
            _halfScale = tuple(_halfScale)
            # print(i,'braille grail',type(i))
            if useOnlyFFBraille:
                _braille.append(Braille.semitonesFF[_halfScale])
            elif not useOnlyFFBraille:
                if i == 0:
                    # print(Braille.semitonesFF,Braille.semitonesFT,Braille.semitonesTF,Braille.semitonesTT,sep='\n\n')
                    # input('i = 0 and stuff')
                    _braille.append(Braille.semitonesFF[_halfScale])
                elif i == 1:

                    _braille.append(Braille.semitonesTF[_halfScale])
                elif i == 2:

                    _braille.append(Braille.semitonesFT[_halfScale])
                elif i == 3:

                    _braille.append(Braille.semitonesTT[_halfScale])
                else:
                    raise ValueError(
                        "did not make it loop back around yet. only supports scales up to two octaves,",
                        self,
                    )
            if colourResult:
                _braille[-1] = Latex.makeDataColoured(
                    _braille[-1],
                    (i * 6 + Book.colourTranspose) % len(Colour.nameByDistanceLt),
                )

        return _braille

    def getTrigram(
        self,
        trigramWays=["symbol"],
        concatenatePerTrigram=False,
        insertStrBetweenAnswers=" ",
        insertStrBetweenSections=None,
        groupByPrependingCharacter=True,
        colourResult=False,
        colourExtraTranspose=0,
        omitStrBetweenAnswers=["symbol", "syllable", "other syllable", "both syllable"],
        beginSyllableWithVowel=True,
        capitaliseFirstLetterOfSyllable=False,
        decorateWithSmallCircle=False,
        useTabbingImg=False,
        normaliseTrigramToRoot=False,
        useLatexReplacementPinyinCharacters=True,
        decorateSymbolWith=False,
        decorateSyllableWith=False,
        externalGraphicsPath=False,
        filetype="pdf",
        key=None,
        textOutlineStrokeWidth=0.2,
        inkColour="black",
        paperColour="white",
    ):
        from Trigram import Trigram
        if key == None:
            key = Change.rootColourKey
        if decorateSymbolWith != False and decorateSymbolWith not in (
            Graphics.validDiagrams
        ):
            raise TypeError(
                "decorateSymbolWith {} not+in Graphics.validDiagrams {}".format(
                    decorateSymbolWith, Graphics.validDiagrams
                )
            )
        if insertStrBetweenSections == None:
            insertStrBetweenSections = Unicode.chars["Chinese Seperator"]

        for way in trigramWays:
            if way in Trigram.allowedWays:
                pass
            else:
                raise ValueError(way, "not in", Trigram.allowedWays)
        _minimumTrigrams = max(4, 1 + (self.getHighestNote(returnSemitone=True) // 3))
        _quarterScales = self.divideScaleBy(
            denominator=4,
            describeSemitones=3 * _minimumTrigrams,
            returnChromatically=False,
        )
        _semitoneDistanceQuarterScales = []
        byWays = []
        if "symbol" in trigramWays:
            _symbols = []
        if "pinyin" in trigramWays:
            _pinyins = []
        if "chinese" in trigramWays:
            _chineses = []
        if "name" in trigramWays:
            _names = []
        if "subpage" in trigramWays:
            _subpages = []
        if "subChange" in trigramWays:
            _pages = []
        if "both syllable" in trigramWays:
            _syllables = []
            _otherSyllables = []
            _bothSyllables = []
        else:
            if "syllable" in trigramWays:
                _syllables = []
            if "other syllable" in trigramWays:
                _otherSyllables = []

        _counter = 0
        for _quarterScale in _quarterScales:
            _semitoneDistanceQuarterScales.append([])
            for _note in _quarterScale.notes:
                _semitoneDistanceQuarterScales[-1].append(
                    _note.semitonesFromOne(octaveLimit=False) - 3 * _counter
                )
            _semitoneDistanceQuarterScales[-1] = tuple(
                _semitoneDistanceQuarterScales[-1]
            )
            _counter += 1

        for i, quarterScale in enumerate(_semitoneDistanceQuarterScales):
            if quarterScale in Trigram.notesets:
                # print(Trigram.notesets[quarterScale])
                if "symbol" in trigramWays:
                    _symbols.append(Trigram.notesets[quarterScale]["symbol"])
                    if colourResult:
                        _symbols[-1] = Latex.makeDataColoured(
                            _symbols[-1],
                            (i * 3 + Book.colourTranspose + colourExtraTranspose) % 12,
                        )

                    if decorateSymbolWith != False:
                        _symbols[-1] = Latex.textGraphic(
                            text=_symbols[-1],
                            graphPath=Graphics.getDiagramPath(
                                change=_quarterScales[i],
                                key=key,
                                diagramType=decorateSymbolWith,
                                filetype=filetype,
                            ),
                            diagramType=decorateSymbolWith,
                            lineWidth=0.1,
                        )

                if "pinyin" in trigramWays:
                    _pinyins.append(Trigram.notesets[quarterScale]["pinyin"])
                    if useLatexReplacementPinyinCharacters:
                        pass
                    else:
                        for replacement in Latex.pinyinReplacements.keys():
                            _pinyins[-1] = _pinyins[-1].replace(
                                Latex.pinyinReplacements[replacement], replacement
                            )
                    if colourResult:
                        _pinyins[-1] = Latex.makeDataColoured(
                            _pinyins[-1],
                            (i * 3 + Book.colourTranspose + colourExtraTranspose) % 12,
                        )
                if "chinese" in trigramWays:
                    _chineses.append(Trigram.notesets[quarterScale]["chinese"])
                    if colourResult:
                        _chineses[-1] = Latex.makeDataColoured(
                            _chineses[-1],
                            (i * 3 + Book.colourTranspose + colourExtraTranspose) % 12,
                        )
                if "name" in trigramWays:
                    _names.append(Trigram.notesets[quarterScale]["name"])
                    if colourResult:
                        _names[-1] = Latex.makeDataColoured(
                            _names[-1],
                            (i * 3 + Book.colourTranspose + colourExtraTranspose) % 12,
                        )
                if "subpage" in trigramWays:
                    _subpages.append(Trigram.notesets[quarterScale]["subpage"])
                    if True or not groupByPrependingCharacter:
                        _subpages[-1] = Unicode.chars["Trigram Subpage"] + str(
                            _subpages[-1]
                        )
                    if colourResult:
                        _subpages[-1] = Latex.makeDataColoured(
                            _subpages[-1],
                            (i * 3 + Book.colourTranspose + colourExtraTranspose) % 12,
                        )
                if "syllable" in trigramWays or "both syllable" in trigramWays:
                    if beginSyllableWithVowel == True:
                        _syllableSounds = ("vowel", "consonant")
                    else:
                        _syllableSounds = ("consonant", "vowel")
                    if i % 2 == 0:
                        _syllables.append(
                            Trigram.notesets[quarterScale][_syllableSounds[0]]
                        )
                        if i == 0 and capitaliseFirstLetterOfSyllable == True:
                            _syllables[-1] = _syllables[-1].capitalize()
                    else:
                        _syllables.append(
                            Trigram.notesets[quarterScale][_syllableSounds[1]]
                        )
                    if colourResult:

                        """_syllables[-1] = Latex.makeDataColoured(_syllables[-1], (
                        i * 3 + Book.colourTranspose + colourExtraTranspose) % 12)"""
                        _colourTags = [
                            Key.allFlats[
                                (
                                    i * 3
                                    + Book.colourTranspose
                                    + colourExtraTranspose
                                    + c
                                    + Key(key).distanceFromC()
                                )
                                % 12
                            ]
                            for c in range(12)
                            if c in quarterScale
                        ]
                        if len(_colourTags) > 0:
                            _syllables[-1] = Latex.makeTextMulticoloured(
                                text=_syllables[-1],
                                colourTags=_colourTags,
                                lineWidth=textOutlineStrokeWidth,
                            )
                        else:
                            _syllables[-1] = Latex.outlineText(
                                _syllables[-1],
                                
                                lineWidth=textOutlineStrokeWidth,
                                strokeColourTag="gray",colourTag=paperColour
                            )
                    if decorateSyllableWith != False:
                        _syllables[-1] = Latex.textGraphic(
                            text=_syllables[-1],
                            graphPath=Graphics.getDiagramPath(
                                change=_quarterScales[i],
                                key=key,
                                diagramType=decorateSyllableWith,
                                filetype=filetype,
                                externalGraphicsPath=externalGraphicsPath,
                            ),
                            diagramType=decorateSyllableWith,
                            sizeMultiplier=0.84,
                            endStr="\\hspace{1.1ex}",
                            trimRight=0,
                            moveUp=-0.1,
                            imgTransparency=0.75,
                            lineWidth=0.04,
                            outlineText=True,
                            colourTag=Colour.nameByDistanceDk[
                                (JazzNote.distanceFromC(key) + i * 3) % 12
                            ],
                        )
                if "other syllable" in trigramWays or "both syllable" in trigramWays:
                    if not beginSyllableWithVowel == True:
                        _syllableSounds = ("vowel", "consonant")
                    else:
                        _syllableSounds = ("consonant", "vowel")
                    if i % 2 == 0:
                        _otherSyllables.append(
                            Trigram.notesets[quarterScale][_syllableSounds[0]]
                        )
                        if i == 0:
                            _otherSyllables[-1] = _otherSyllables[-1].capitalize()
                    else:
                        _otherSyllables.append(
                            Trigram.notesets[quarterScale][_syllableSounds[1]]
                        )
                    if colourResult:
                        _otherSyllables[-1] = Latex.makeDataColoured(
                            _otherSyllables[-1],
                            (i * 3 + Book.colourTranspose + colourExtraTranspose) % 12,
                        )
                if "subChange" in trigramWays:
                    if normaliseTrigramToRoot:
                        _denormaliseSemitones = 0
                    else:
                        _denormaliseSemitones = 3
                        _semitonesDenormalised = [
                            (note + _denormaliseSemitones * i) % 12
                            for note in quarterScale
                        ]
                        _semitonesDenormalised = Change.makeFromSet(
                            _semitonesDenormalised
                        )
                        # print('_semitonesDenormalised =',_semitonesDenormalised)
                        _quarterScalePage = _semitonesDenormalised.getChangeNumber(
                            addOneToBookPage=True
                        )
                        # print('_quarterScalePage = ',_quarterScalePage)
                    _pages.append(
                        _semitonesDenormalised.getChangeNumber(
                            addOneToBookPage=True,
                            decorateChapter=True,
                            decorateWithSmallCircle=decorateWithSmallCircle,
                            imgTag="tabbingimg",
                            includeNormalisedPageForNegatives=False,
                        )
                    )
                    _pages[-1] = str(_pages[-1])
                    # print('_pages[-1] =',_pages[-1],end='\n\n')
                    if colourResult:
                        _pages[-1] = Latex.makeDataColoured(
                            _pages[-1],
                            (i * 3 + Book.colourTranspose + colourExtraTranspose) % 12,
                        )
            else:
                raise ValueError(
                    quarterScale,
                    "not found in Trigram.notesets",
                    Trigram.notesets,
                    "self",
                    self,
                )
        # input(' '.join(_symbols))
        _byWays = []
        # This loop makes it keep its order from the trigramWays
        for i in trigramWays:
            if i == "symbol":
                _byWays.append(_symbols)
            elif i == "pinyin":
                _byWays.append(_pinyins)
            elif i == "chinese":
                _byWays.append(_chineses)
            elif i == "name":
                _byWays.append(_names)
            elif i == "subpage":
                _byWays.append(_subpages)
            elif i == "subChange":
                _byWays.append(_pages)
            elif i == "syllable":
                _byWays.append(_syllables)
            elif i == "other syllable":
                _byWays.append(_otherSyllables)
            elif i == "both syllable":
                _byWays.append("".join(_syllables) + " " + "".join(_otherSyllables))
            # _byWays.append([_syllables[syl] + ' ' + _otherSyllables[syl] for syl in range(len(_syllables))])

        if len(_byWays) == 1:
            return _byWays[0]
        elif len(_byWays) == 0:
            raise ValueError("did not provide ways")
        elif len(_byWays) > 1:
            if concatenatePerTrigram:
                _concatenatedTrigrams = []
                for t in range(len(_byWays[0])):
                    _concatenatedTrigrams.append("")
                    for l in range(len(_byWays)):
                        _concatenatedTrigrams[-1] += _byWays[l][t]
                        if l != len(_byWays) - 1:
                            _concatenatedTrigrams[-1] += insertStrBetweenAnswers

                        if trigramWays[l] == "syllable":
                            pass
                        # _concatenatedTrigrams[-1] = _concatenatedTrigrams[-1].lower().capitalize()
                    if l != len(_byWays[0]) - 1:
                        _concatenatedTrigrams[-1] += insertStrBetweenSections
                return _concatenatedTrigrams
            elif not concatenatePerTrigram:

                _concatenatedWays = []
                for i, l in enumerate(_byWays):
                    if trigramWays[i] not in omitStrBetweenAnswers:
                        # print('trigram ways',trigramWays[i])
                        _concatenatedWays.append(" ".join(l))
                    elif trigramWays[i] in omitStrBetweenAnswers:
                        _concatenatedWays.append("".join(l))
                    if trigramWays[i] == "syllable":
                        pass
                    # _concatenatedWays[-1] = _concatenatedWays[-1].lower().capitalize()
                    if i != len(_byWays) - 1:
                        _concatenatedWays[-1] += insertStrBetweenSections

                if groupByPrependingCharacter:
                    # print('eye is equals', i)
                    if "number" in trigramWays:
                        _indexOfNumberWay = trigramWays.index("number")
                        _concatenatedWays[_indexOfNumberWay] = [
                            i.replace(Unicode.chars["Index Number"], "")
                            for i in _concatenatedWays[_indexOfNumberWay]
                        ]
                        _concatenatedWays[_indexOfNumberWay] = (
                            Unicode.chars["Index Number"]
                            + " "
                            + "".join(_concatenatedWays[_indexOfNumberWay])
                        )
                    if "subChange" in trigramWays:
                        _indexOfNumberWay = trigramWays.index("subChange")
                        # print('asdfasdf {}'.format(_concatenatedWays[_indexOfNumberWay] ))
                        """_concatenatedWays[_indexOfNumberWay] = Unicode.chars['Change Number'] + ' ' + ''.join(
                            _concatenatedWays[_indexOfNumberWay])
                        _concatenatedWays[_indexOfNumberWay] = [i.replace(Unicode.chars['Change Number'], '') for i in
                                                                _concatenatedWays[_indexOfNumberWay]]"""
                        if decorateWithSmallCircle == False:
                            _concatenatedWays[_indexOfNumberWay] = (
                                Unicode.chars["Change Number"]
                                + " "
                                + "".join(_concatenatedWays[_indexOfNumberWay]).replace(
                                    Unicode.chars["Change Number"], ""
                                )
                            )
                        if decorateWithSmallCircle == True:
                            # override the subChange number because graphic subChange numbers have been added to each answer
                            _concatenatedWays[_indexOfNumberWay] = "".join(
                                _concatenatedWays[_indexOfNumberWay]
                            )
                            # _concatenatedWays[_indexOfNumberWay] = \
                            #    [i.replace(Unicode.chars['Change Number'],'') for i in _concatenatedWays[_indexOfNumberWay]]

                        # input('diiii {}'.format(_concatenatedWays))
                        # input('asdfasdf {}'.format(_concatenatedWays[_indexOfNumberWay]))

                    if "subpage" in trigramWays:
                        _indexOfNumberWay = trigramWays.index("subpage")
                        _concatenatedWays[_indexOfNumberWay] = [
                            i.replace(Unicode.chars["Trigram Subpage"], "")
                            for i in _concatenatedWays[_indexOfNumberWay]
                        ]
                        _concatenatedWays[_indexOfNumberWay] = (
                            Unicode.chars["Trigram Subpage"]
                            + " "
                            + "".join(_concatenatedWays[_indexOfNumberWay])
                        )

                # print('here is the big one of concatenated ways:\n'+''.join(_concatenatedWays))
                return _concatenatedWays

            """                #Add this block
                if groupByPrependingSymbol:
                    if 'number' in tetragramWays:
                        _indexOfNumberWay = tetragramWays.index('number')
                        _concatenatedWays[_indexOfNumberWay] = [i.replace(Book.unicodeCharConstants['Index Number'],'') for i in _concatenatedWays[_indexOfNumberWay]]
                        _concatenatedWays[_indexOfNumberWay] = Book.unicodeCharConstants['Index Number'] + ' ' + ''.join(_concatenatedWays[_indexOfNumberWay])

                if includePageNumber:
                    _concatenatedWays.append(insertStrBetweenAnswers.join(_pages))
                    #Add this part
                    _concatenatedWays[-1] = Book.unicodeCharConstants['Change Number']+' '+_concatenatedWays[-1]
                return _concatenatedWays"""

    def getTetragram(
        self,
        tetragramWays=["symbol"],
        concatenatePerTetragram=False,
        insertStrBetweenAnswers=" ",
        insertStrBetweenSections="。",
        groupByPrependingCharacter=True,
        colourResult=False,
        decorateWithSmallCircle=False,
        normaliseHexagramToRoot=False,
        omitStrBetweenAnswers=["symbol"],
        useLatexReplacementPinyinCharacters=True,
    ):
        from Tetragram import Tetragram
        # print('tetragramways being used',tetragramWays)
        if insertStrBetweenSections == None:
            insertStrBetweenSections = Unicode.chars["Chinese Seperator"]
        for way in tetragramWays:
            if way in Tetragram.allowedWays:
                pass
            else:
                raise ValueError(way, "not in", Tetragram.allowedWays)
        _minimumTetragrams = max(3, 1 + (self.getHighestNote(returnSemitone=True) // 4))
        _thirdScales = self.divideScaleBy(
            denominator=3,
            describeSemitones=4 * _minimumTetragrams,
            returnChromatically=False,
            normaliseToSlice=False,
        )
        # input(_thirdScales)
        _semitoneDistanceThirdScales = []
        byWays = []
        if "symbol" in tetragramWays:
            _symbols = []
        if "pinyin" in tetragramWays:
            _pinyins = []
        if "chinese" in tetragramWays:
            _chineses = []
        if "name" in tetragramWays:
            _names = []
        if "number" in tetragramWays:
            _numbers = []
        if "subpage" in tetragramWays:
            _subpages = []
        if "subChange" in tetragramWays:
            _pages = []

        _counter = 0
        for _thirdScale in _thirdScales:
            _semitoneDistanceThirdScales.append([])
            for _note in _thirdScale.notes:
                _semitoneDistanceThirdScales[-1].append(
                    _note.semitonesFromOne(octaveLimit=False) - 4 * _counter
                )
            _semitoneDistanceThirdScales[-1] = tuple(_semitoneDistanceThirdScales[-1])
            _counter += 1

        for i, thirdScale in enumerate(_semitoneDistanceThirdScales):
            if thirdScale in Tetragram.semitones:
                # print(Tetragram.notesets[thirdScale])
                if "symbol" in tetragramWays:
                    _symbols.append(Tetragram.semitones[thirdScale]["symbol"])
                    if colourResult:
                        _symbols[-1] = Latex.makeDataColoured(
                            _symbols[-1], (i * 4 + Book.colourTranspose) % 12
                        )
                if "pinyin" in tetragramWays:
                    _pinyins.append(Tetragram.semitones[thirdScale]["pinyin"])
                    if useLatexReplacementPinyinCharacters:
                        pass
                    else:
                        for replacement in Latex.pinyinReplacements.keys():
                            _pinyins[-1] = _pinyins[-1].replace(
                                Latex.pinyinReplacements[replacement], replacement
                            )
                    if colourResult:
                        _pinyins[-1] = Latex.makeDataColoured(
                            _pinyins[-1], (i * 4 + Book.colourTranspose) % 12
                        )
                if "chinese" in tetragramWays:
                    _chineses.append(Tetragram.semitones[thirdScale]["chinese"])
                    if colourResult:
                        _chineses[-1] = Latex.makeDataColoured(
                            _chineses[-1], (i * 4 + Book.colourTranspose) % 12
                        )
                if "name" in tetragramWays:
                    _names.append(Tetragram.semitones[thirdScale]["name"])
                    if colourResult:
                        _names[-1] = Latex.makeDataColoured(
                            _names[-1], (i * 4 + Book.colourTranspose) % 12
                        )
                if "number" in tetragramWays:
                    _numbers.append(
                        Unicode.chars["Index Number"]
                        + Tetragram.semitones[thirdScale]["number"]
                    )
                    if colourResult:
                        _numbers[-1] = Latex.makeDataColoured(
                            _numbers[-1], (i * 4 + Book.colourTranspose) % 12
                        )
                if "subpage" in tetragramWays:
                    _subpages.append(
                        Unicode.chars["Tetragram Subpage"]
                        + str(Tetragram.semitones[thirdScale]["subpage"])
                    )
                    if colourResult:
                        _subpages[-1] = Latex.makeDataColoured(
                            _subpages[-1], (i * 4 + Book.colourTranspose) % 12
                        )
                if "subChange" in tetragramWays:
                    if normaliseHexagramToRoot:
                        _denormaliseSemitones = 0
                    else:
                        _denormaliseSemitones = 4
                        _semitonesDenormalised = [
                            (note + _denormaliseSemitones * i) % 12
                            for note in thirdScale
                        ]
                        _semitonesDenormalised = Change.makeFromSet(
                            _semitonesDenormalised
                        )

                    _pages.append(
                        _semitonesDenormalised.getChangeNumber(
                            addOneToBookPage=True,
                            decorateChapter=True,
                            decorateWithSmallCircle=decorateWithSmallCircle,
                            includeNormalisedPageForNegatives=False,
                        )
                    )
                    _pages[-1] = str(_pages[-1])
                    # laurelle
                    if colourResult:
                        _pages[-1] = Latex.makeDataColoured(
                            _pages[-1], (i * 4 + Book.colourTranspose) % 12
                        )
            else:
                raise ValueError(
                    thirdScale,
                    "not found in Tetragram.notesets",
                    Tetragram.semitones,
                    "self",
                    self,
                )
        # input(' '.join(_symbols))
        _byWays = []
        # This loop makes it keep its order from the tetragramWays
        for i in tetragramWays:
            if i == "symbol":
                _byWays.append(_symbols)
            elif i == "pinyin":
                _byWays.append(_pinyins)
            elif i == "chinese":
                _byWays.append(_chineses)
            elif i == "name":
                _byWays.append(_names)
            elif i == "number":
                _byWays.append(_numbers)
            elif i == "subpage":
                _byWays.append(_subpages)  # ;print('sp',_subpages)
            elif i == "subChange":
                _byWays.append(_pages)  # ;print('pg',_pages)
        if len(_byWays) == 1:
            return _byWays[0]
        elif len(_byWays) == 0:
            raise ValueError("did not provide ways")
        elif len(_byWays) > 0:
            if concatenatePerTetragram:
                _concatenatedTetragrams = []
                #input("sssssss" + str(tetragramWays))
                for t in range(len(_byWays[0])):
                    _concatenatedTetragrams.append("")
                    for l in range(len(_byWays)):
                        _concatenatedTetragrams[-1] += _byWays[l][t]

                        if l != len(_byWays) - 1:

                            if tetragramWays[l] not in omitStrBetweenAnswers:
                                _concatenatedTetragrams[-1] += insertStrBetweenAnswers
                    if t != len(_byWays[0]) - 1:
                        _concatenatedTetragrams[-1] += insertStrBetweenSections
                return _concatenatedTetragrams
            elif not concatenatePerTetragram:
                _concatenatedWays = []
                for i, l in enumerate(_byWays):
                    # print(str(omitStrBetweenAnswers),'tetragramWays',tetragramWays[i],'  l: ',str(l))
                    # input('kitty')
                    if tetragramWays[i] not in omitStrBetweenAnswers:
                        _concatenatedWays.append(insertStrBetweenAnswers.join(l))
                    elif tetragramWays[i] in omitStrBetweenAnswers:
                        _concatenatedWays.append("".join(l))
                    if i != len(_byWays) - 1:
                        _concatenatedWays[-1] += insertStrBetweenSections

                # Add this block
                if groupByPrependingCharacter:
                    if "number" in tetragramWays:
                        _indexOfNumberWay = tetragramWays.index("number")
                        _concatenatedWays[_indexOfNumberWay] = [
                            i.replace(Unicode.chars["Index Number"], "")
                            for i in _concatenatedWays[_indexOfNumberWay]
                        ]
                        _concatenatedWays[_indexOfNumberWay] = (
                            Unicode.chars["Index Number"]
                            + " "
                            + "".join(_concatenatedWays[_indexOfNumberWay])
                        )
                    if "subChange" in tetragramWays:
                        _indexOfNumberWay = tetragramWays.index("subChange")

                        _concatenatedWays[_indexOfNumberWay] = "".join(
                            _concatenatedWays[_indexOfNumberWay]
                        )
                        if decorateWithSmallCircle == True:
                            _concatenatedWays[_indexOfNumberWay] = "".join(
                                _concatenatedWays[_indexOfNumberWay]
                            )
                            _concatenatedWays[_indexOfNumberWay] = "".join(
                                [
                                    i.replace(Unicode.chars["Change Number"], "")
                                    for i in _concatenatedWays[_indexOfNumberWay]
                                ]
                            )
                        else:
                            _concatenatedWays[_indexOfNumberWay] = (
                                Unicode.chars["Change Number"]
                                + " "
                                + _concatenatedWays[_indexOfNumberWay].replace(
                                    Unicode.chars["Change Number"], ""
                                )
                            )
                    if "subpage" in tetragramWays:
                        _indexOfNumberWay = tetragramWays.index("subpage")
                        _concatenatedWays[_indexOfNumberWay] = [
                            i.replace(Unicode.chars["Tetragram Subpage"], "")
                            for i in _concatenatedWays[_indexOfNumberWay]
                        ]
                        _concatenatedWays[_indexOfNumberWay] = (
                            Unicode.chars["Tetragram Subpage"]
                            + " "
                            + "".join(_concatenatedWays[_indexOfNumberWay])
                        )
                    # Add this part
                    # _concatenatedWays[-1] = Unicode.chars['Change Number'] + ' ' + _concatenatedWays[-1]
                return _concatenatedWays

    def getChangedHexagram(
        self,
    ):
        # Only work on one octave
        pass

    def getHexagram(
        self,
        hexagramWays=["symbol"],
        concatenatePerHexagram=False,
        insertStrBetweenAnswers=" ",
        insertStrBetweenSections=None,
        groupByPrependingCharacter=True,
        colourResult=False,
        decorateWithSmallCircle=False,
        normaliseHexagramToRoot=False,
        omitStrBetweenAnswers=["symbol", "braille", "symbol"],
        useLatexReplacementPinyinCharacters=True,
        includeNounFormForName=True,
        beginWithNounForm=False,
        decorateWithUnicode=True,
        decorateSymbolWith=False,
        useGraphicSymbol=False,
        externalGraphicsPath=False,
        invertColour=False,
        filetype="pdf",
        useTextStyledByWay=False,
        key=None,
    ):
        if key == None:
            key = Change.rootColourKey
        if decorateSymbolWith != False and decorateSymbolWith not in (
            Graphics.validDiagrams
        ):
            raise TypeError(
                "decorateSymbolWith {} not+in Graphics.validDiagrams {}".format(
                    decorateSymbolWith, Graphics.validDiagrams
                )
            )
        if insertStrBetweenSections == "\\hfill":
            raise ValueError("add a space after \\hfill so it doesnt fuck things up")
        if insertStrBetweenSections == None:
            insertStrBetweenSections = Unicode.chars["Chinese Seperator"]
        if insertStrBetweenAnswers == None:
            insertStrBetweenAnswers = " "
        for way in hexagramWays:
            from Hexagram import Hexagram
            if way in Hexagram.validWays:
                pass
            else:
                raise ValueError(way, "not in Hexagram.allowedWays", Hexagram.validWays)
        _minimumHexagrams = max(2, 1 + (self.getHighestNote(returnSemitone=True) // 6))
        _halfScales = self.divideScaleBy(
            denominator=2,
            describeSemitones=6 * _minimumHexagrams,
            returnChromatically=False,
            normaliseToSlice=False,
        )

        # input(_halfScales)
        _semitoneDistanceHalfScales = []
        byWays = []
        if "symbol" in hexagramWays:
            _symbols = []
        if "pinyin" in hexagramWays:
            _pinyins = []
        if "chinese" in hexagramWays:
            _chineses = []
        if "name" in hexagramWays:
            _names = []
        if "secondName" in hexagramWays:
            _secondNames = []
        if "number" in hexagramWays:
            _numbers = []
        if "story" in hexagramWays:
            _stories = []
        if "story end" in hexagramWays:
            _storyEnds = []
        if "subpage" in hexagramWays:
            _subpages = []
        if "subChange" in hexagramWays:
            _pages = []
        if "braille" in hexagramWays:
            _brailles = []
        if "codon" in hexagramWays:
            _codons = []
        if "syllable" in hexagramWays:
            _syllables = []
        if "Change" in hexagramWays:
            _changes = []
        _counter = 0
        for _halfScale in _halfScales:
            _semitoneDistanceHalfScales.append([])
            for _note in _halfScale.notes:
                _semitoneDistanceHalfScales[-1].append(
                    _note.semitonesFromOne(octaveLimit=False) - 6 * _counter
                )
            # Don't need next line because Hexagram uses list, unlike tetra and tri which use tuple
            # _semitoneDistanceHalfScales[-1] = tuple(_semitoneDistanceHalfScales[-1])
            _counter += 1

        for i, halfScale in enumerate(_semitoneDistanceHalfScales):
            if halfScale in Hexagram.notesets:
                # _hexagramColour = JazzNote.makeFromSet(6*i,octaveLimit=True).getColour(adjustBySemitones=JazzNote.distanceFromC(Book.rootKey))

                _hexagramColour = (6 * i + Key(Change.rootColourKey).distanceFromC()) % len(
                    Colour.nameByDistanceLt
                )
                _hexagramNumber = Hexagram.notesets.index(halfScale)

                # print(Hexagram.notesets[halfScale])
                if "Change" in hexagramWays:
                    _changes.append(Change.makeFromSet([s + i * 6 for s in halfScale]))
                    if useTextStyledByWay:
                        _changes[-1] = Latex.makeTextStyledByWay(_changes[-1],'Jazz')
                        #input('here')
                if "symbol" in hexagramWays:
                    if not useGraphicSymbol:
                        _symbols.append(Hexagram.symbol[_hexagramNumber])
                    else:
                        _symbols.append(
                            Latex.insertSmallDiagram(
                                change=Change(noteset=halfScale),
                                key=Key.allFlats[
                                    (Key(key).distanceFromC() + 6 * i) % 12
                                ],
                                diagramType="Hexagram",
                                externalGraphicsPath=externalGraphicsPath,
                                filetype=filetype,
                                invertColour=invertColour,
                                imgtag="hexagramimg",
                            )
                        )
                    # add makeTextColoured here
                    if colourResult and not useGraphicSymbol:
                        _symbols[-1] = Latex.makeDataColoured(
                            _symbols[-1], _hexagramColour
                        )
                    if decorateSymbolWith:
                        _symbols[-1] = Latex.textGraphic(
                            text=_symbols[-1],
                            graphPath=Graphics.getDiagramPath(
                                change=_halfScales[i],
                                key=key,
                                diagramType=decorateSymbolWith,
                                filetype=filetype,
                                externalGraphicsPath=externalGraphicsPath,
                            ),
                            diagramType=decorateSymbolWith,
                            sizeMultiplier=1.2,
                        )
                        # input('this is not working {}'.format(_symbols[-1]))
                if "pinyin" in hexagramWays:
                    _pinyins.append(Hexagram.pinyin[_hexagramNumber])
                    if useLatexReplacementPinyinCharacters:
                        pass
                    else:
                        for replacement in Latex.pinyinReplacements.keys():
                            _pinyins[-1] = _pinyins[-1].replace(
                                Latex.pinyinReplacements[replacement], replacement
                            )
                    if colourResult:
                        _pinyins[-1] = Latex.makeDataColoured(
                            _pinyins[-1], _hexagramColour
                        )
                if "chinese" in hexagramWays:
                    _chineses.append(Hexagram.chinese[_hexagramNumber])
                    if colourResult:
                        _chineses[-1] = Latex.makeDataColoured(
                            _chineses[-1], _hexagramColour
                        )
                if "name" in hexagramWays:

                    _name = self.getHexagramNames(
                        includeNounFormForName=includeNounFormForName,
                        beginWithNounForm=beginWithNounForm,
                        useTextStyledByWay=useTextStyledByWay
                    )
                    #input('frikkkk   '+_name)
                    _names.append(_name[i])
                    
                    if colourResult:
                        _names[-1] = Latex.makeDataColoured(_names[-1], _hexagramColour)
                if "secondName" in hexagramWays:
                    
                    '''_secondName = self.getHexagramNames(
                        includeNounFormForName=includeNounFormForName,
                        beginWithNounForm=i% 2 == 1,
                        useTextStyledByWay=useTextStyledByWay
                    )'''
                    
                    
                
                    _secondName = Change(noteset=halfScale).getHexagramNames(
                        includeNounFormForName=includeNounFormForName,
                        beginWithNounForm=True,
                        useTextStyledByWay=useTextStyledByWay
                    )[0]
                    #input(_secondName)
                    #input(str(self) + _secondName[i])
                    _secondNames.append(_secondName)
                    if colourResult:
                        _secondNames[-1] = Latex.makeDataColoured(_secondNames[-1], _hexagramColour)

                if "number" in hexagramWays:
                    _numbers.append(str(_hexagramNumber))
                    if decorateWithUnicode:
                        _numbers[-1] = Unicode.chars["Index Number"] + _numbers[-1]
                     
                    if colourResult:
                        _numbers[-1] = Latex.makeDataColoured(
                            _numbers[-1], _hexagramColour
                        )
                if "subpage" in hexagramWays:
                    _subpages.append(str(Hexagram.subChange[_hexagramNumber]))
                    if decorateWithUnicode:
                        _subpages[-1] = Unicode.chars["Hexagram Subpage"] + str(
                            _subpages[-1]
                        )
                    if colourResult:
                        _subpages[-1] = Latex.makeDataColoured(
                            _subpages[-1], _hexagramColour
                        )
                if "story" in hexagramWays:
                    # if even number (in computer numbers, so beginning is 0)
                    if i % 2 == 0:
                        _stories.append(Hexagram.storyBeginning[_hexagramNumber])
                    else:
                        _stories.append(Hexagram.storyEnd[_hexagramNumber])
                    if colourResult:
                        _stories[-1] = Latex.makeDataColoured(
                            _stories[-1], _hexagramColour
                        )
                if "story end" in hexagramWays:
                    # always the end

                    _storyEnds.append(Hexagram.storyEnd[_hexagramNumber])
                    if colourResult:
                        _storyEnds[-1] = Latex.makeDataColoured(
                            _storyEnds[-1], _hexagramColour
                        )
                if "subChange" in hexagramWays:
                    if normaliseHexagramToRoot:
                        _denormaliseSemitones = 0
                    else:
                        _denormaliseSemitones = 6
                        _semitonesDenormalised = [
                            (note + _denormaliseSemitones * i) % 12
                            for note in halfScale
                        ]
                        _semitonesDenormalised = Change.makeFromSet(
                            _semitonesDenormalised
                        )

                    _pages.append(
                        _semitonesDenormalised.getChangeNumber(
                            decorateChapter=True,
                            decorateWithSmallCircle=decorateWithSmallCircle,
                            externalGraphicsPath=externalGraphicsPath,
                            includeNormalisedPageForNegatives=False,
                            useTextStyledByWay=useTextStyledByWay

                        )
                    )
                    if colourResult:
                        _pages[-1] = Latex.makeDataColoured(_pages[-1], _hexagramColour)
                if "braille" in hexagramWays:
                    _brailles = self.getBraille(colourResult=colourResult,
                                
                    )
                if "codon" in hexagramWays:
                    _codons = self.getCodon(geneType="Both", colourResult=colourResult,
                                             useTextStyledByWay=useTextStyledByWay)
                if "syllable" in hexagramWays:
                    _fullWord = self.getWord(colourResult=colourResult,
                                             )
                    _syllables = []
                    for s in range(0, len(_fullWord), 2):
                        _syllables.append(Latex.makeTextStyledByWay(_fullWord[s : s + 2],'Word'))
                        #input(_syllables)
            else:
                raise ValueError(
                    halfScale,
                    "not found in Hexagram.notesets",
                    Hexagram.notesets,
                    "self",
                    self,
                )
        
        # input(' '.join(_symbols))
        
        _byWays = []
        # This loop makes it keep its order from the hexagramWays
        for i in hexagramWays:
            if i == "symbol":
                _byWays.append(_symbols)
            elif i == "pinyin":
                _byWays.append(_pinyins)
            elif i == "chinese":
                _byWays.append(_chineses)
            elif i == "name":
                _byWays.append(_names)
            elif i == "secondName":
                _byWays.append(_secondNames)
            elif i == "number":
                _byWays.append(_numbers)
            elif i == "story":
                _byWays.append(_stories)
            elif i == "story end":
                _byWays.append(_storyEnds)
            elif i == "subpage":
                _byWays.append(_subpages)
            elif i == "subChange":
                _byWays.append(_pages)
            elif i == "braille":
                _byWays.append(_brailles)
            elif i == "codon":
                _byWays.append(_codons)
            elif i == "syllable":
                _byWays.append(_syllables)
            elif i == "Change":
                _byWays.append(_changes)
        for way in _byWays:
            for answer in way:
                if str(answer).count('{') != str(answer).count('}'):
                    raise ValueError('answer === ' + answer + '\n' + str(_byWays))


        if len(_byWays) == 1:
            return _byWays[0]
        elif len(_byWays) == 0:
            raise ValueError("add way to list above ways")


        elif len(_byWays) > 1:
            if concatenatePerHexagram:
                _concatenatedHexagrams = []
                for h in range(len(_byWays[0])):
                    _concatenatedHexagrams.append("")
                    for l in range(len(_byWays)):
                        _concatenatedHexagrams[-1] += _byWays[l][h]
                        if insertStrBetweenAnswers and l != len(_byWays) - 1:
                            _concatenatedHexagrams[-1] += insertStrBetweenAnswers
                    if insertStrBetweenAnswers and h != len(_byWays) - 1:
                        _concatenatedHexagrams[-1] += insertStrBetweenSections
                return _concatenatedHexagrams
            elif not concatenatePerHexagram:
                _concatenatedWays = []
                for i, l in enumerate(_byWays):
                    if hexagramWays[i] not in omitStrBetweenAnswers:
                        _concatenatedWays.append(insertStrBetweenAnswers.join(l))
                    elif hexagramWays[i] in omitStrBetweenAnswers:
                        _concatenatedWays.append("".join(l))
                    if i != len(_byWays) - 1:
                        _concatenatedWays[-1] += insertStrBetweenSections

                if groupByPrependingCharacter:
                    if "number" in hexagramWays:
                        _indexOfNumberWay = hexagramWays.index("number")
                        _concatenatedWays[_indexOfNumberWay] = [
                            i.replace(Unicode.chars["Index Number"], "")
                            for i in _concatenatedWays[_indexOfNumberWay]
                        ]
                        _concatenatedWays[_indexOfNumberWay] = (
                            Unicode.chars["Index Number"]
                            + " "
                            + "".join(_concatenatedWays[_indexOfNumberWay])
                        )
                    if "subChange" in hexagramWays:
                        _indexOfNumberWay = hexagramWays.index("subChange")
                        _concatenatedWays[_indexOfNumberWay] = [
                            i.replace(Unicode.chars["Change Number"], "")
                            for i in _concatenatedWays[_indexOfNumberWay]
                        ]
                        if decorateWithSmallCircle == True:
                            _concatenatedWays[_indexOfNumberWay] = "".join(
                                _concatenatedWays[_indexOfNumberWay]
                            )
                        else:
                            _concatenatedWays[_indexOfNumberWay] = (
                                Unicode.chars["Change Number"]
                                + " "
                                + "".join(_concatenatedWays[_indexOfNumberWay])
                            )
                    if "subpage" in hexagramWays:
                        _indexOfNumberWay = hexagramWays.index("subpage")
                        _concatenatedWays[_indexOfNumberWay] = [
                            i.replace(Unicode.chars["Hexagram Subpage"], "")
                            for i in _concatenatedWays[_indexOfNumberWay]
                        ]
                        _concatenatedWays[_indexOfNumberWay] = (
                            Unicode.chars["Hexagram Subpage"]
                            + " "
                            + "".join(_concatenatedWays[_indexOfNumberWay])
                        )
                return _concatenatedWays

    def getHexagramNumbers(self):
        _minimumHexagrams = max(2, 1 + (self.getHighestNote(returnSemitone=True) // 6))
        _halfScales = self.divideScaleBy(describeSemitones=6 * _minimumHexagrams)
        # print('blamoz',_halfScales)
        _semitoneDistanceHalfScales = []
        _hexagramNumbers = []
        _counter = 0
        for _halfScale in _halfScales:
            _semitoneDistanceHalfScales.append([])
            for _note in _halfScale.notes:
                _semitoneDistanceHalfScales[-1].append(
                    _note.semitonesFromOne(octaveLimit=False) - 6 * _counter
                )
            _counter += 1

        for _halfScale in _semitoneDistanceHalfScales:
            from Hexagram import Hexagram
            _hexagramNumbers.append(Hexagram.notesets.index(_halfScale))

        # print('see what happens', _hexagramNumbers)

        return _hexagramNumbers

    def getHexagramName(self):
        return ' '.join(self.getHexagramNames())
    
    def getHexagramNames(self, includeNounFormForName=True, beginWithNounForm=False, useTextStyledByWay=False):
        # Bleep bloob
        _names = []
        _hexagramNumbers = self.getHexagramNumbers()
        for h, hexaNumber in enumerate(_hexagramNumbers):
            try:
                Hexagram
            except NameError:
                from Hexagram import Hexagram
            _whichNames = Hexagram.names
            if includeNounFormForName:
                if h % 2 == 0:
                    if beginWithNounForm:
                        _whichNames = Hexagram.namesNoun
                    else:
                        _whichNames = Hexagram.names
                else:
                    if beginWithNounForm:
                        _whichNames = Hexagram.names
                    else:
                        _whichNames = Hexagram.namesNoun

            _names.append(_whichNames[hexaNumber])

        if useTextStyledByWay:
            
            _names = [Latex.makeTextStyledByWay(n,'Hexagram') for n in _names]
            
            #input('frug '+_name)
        return _names

    def getHexagramSymbols(self, insertSpaceBetweenHexagrams=True, colourResult=False):
        from Hexagram import Hexagram
        if colourResult:
            raise ValueError("use the getHexagram() function instead")
        # _symbols = ''
        _symbols = []
        _hexagramNumbers = self.getHexagramNumbers()
        for _hexaNumber in _hexagramNumbers:
            # print('_hexaNumber in getHexagramSymbols: ',_hexaNumber)
            _symbols.append(Hexagram.symbol[_hexaNumber])
            # if insertSpaceBetweenHexagrams == True and\
            # _hexagramNumbers.index(_hexaNumber) != len(_hexagramNumbers)-1:
        return _symbols

    def OLDgetHalfScales(
        self, octaveLimit=False, returnChromatically=False, minimumHexagrams=2
    ):
        _halfScales = []
        if len(self) > 0:
            _maxSemitoneIndex = max(
                self.notes, key=lambda x: x.semitonesFromOne(octaveLimit=octaveLimit)
            )
            _maxSemitoneIndex = _maxSemitoneIndex.semitonesFromOne(
                octaveLimit=octaveLimit
            )
        else:
            _maxSemitoneIndex = 0
        # print('_maxSemitonIndex ',_maxSemitoneIndex)
        for i in range(max(math.floor(_maxSemitoneIndex / 6) + 1, minimumHexagrams)):
            _halfScales.append([])
            for note in range(len(self.notes)):
                # print('note',note)
                # print(self.notes[note].semitonesFromOne(octaveLimit=octaveLimit), (i+1) * 6)
                if (
                    self.notes[note].semitonesFromOne(octaveLimit=octaveLimit)
                    < (i + 1) * 6
                ):
                    # print(self.notes[note].semitonesFromOne(octaveLimit=octaveLimit) >= i * 6)
                    if (
                        self.notes[note].semitonesFromOne(octaveLimit=octaveLimit)
                        >= i * 6
                    ):
                        _halfScales[-1].append(self.notes[note])

        for i in range(len(_halfScales)):
            _halfScales[i] = Change(_halfScales[i])
        # print('in return to halfscales',_halfScales)
        if returnChromatically:
            _chromaticChange = []
            for i in _halfScales:
                _chromaticChange.append([])
                for note in i:
                    _chromaticChange[-1].append(
                        note.semitonesFromOne(octaveLimit=octaveLimit)
                    )
            return _chromaticChange

        return _halfScales

    def divideScaleBy(
        self,
        octaveLimit=False,
        returnChromatically=False,
        denominator=2,
        describeSemitones=12,
        normaliseToSlice=False,
        colourResult=False,
    ):
        _scaleSlices = []
        _sliceSize = describeSemitones // denominator
        _minimumSymbols = denominator

        if len(self) > 0:
            _maxSemitoneIndex = max(
                self.notes, key=lambda x: x.semitonesFromOne(octaveLimit=octaveLimit)
            )
            _maxSemitoneIndex = _maxSemitoneIndex.semitonesFromOne(
                octaveLimit=octaveLimit
            )
        else:
            _maxSemitoneIndex = 0
        # print('_maxSemitonIndex ',_maxSemitoneIndex)
        for i in range(denominator):
            _scaleSlices.append([])
            for note in range(len(self.notes)):
                # print('note',note)
                # print(self.notes[note].semitonesFromOne(octaveLimit=octaveLimit), (i+1) * 6)
                if (
                    self.notes[note].semitonesFromOne(octaveLimit=octaveLimit)
                    < (i + 1) * _sliceSize
                ):
                    # print(self.notes[note].semitonesFromOne(octaveLimit=octaveLimit) >= i * 6)
                    if (
                        self.notes[note].semitonesFromOne(octaveLimit=octaveLimit)
                        >= i * _sliceSize
                    ):
                        if normaliseToSlice:
                            _scaleSlices[-1].append(
                                JazzNote.makeFromSet(
                                    self.notes[note].semitonesFromOne()
                                    - _sliceSize * (len(_scaleSlices) - 1)
                                )
                            )
                        elif not normaliseToSlice:
                            _scaleSlices[-1].append(self.notes[note])

        for i in range(len(_scaleSlices)):
            _scaleSlices[i] = Change(_scaleSlices[i])
        # print('in return to scaleSlices',_scaleSlices)
        if returnChromatically:
            raise TypeError("apparently returnChromatically does not work :(")
            _chromaticChange = []
            for i in _scaleSlices:
                _chromaticChange.append([])
                for note in i:
                    _chromaticChange[-1].append(
                        note.semitonesFromOne(octaveLimit=octaveLimit)
                    )
            if normaliseToSlice:
                pass  # _chromaticChange = [i%(describeSemitones/denominator) for i in _chromaticChange]
            return _chromaticChange
        if colourResult:
            for s, slic in enumerate(_scaleSlices):
                for n, note in enumerate(slic):
                    pass
                    # _scaleSlices[s][n] = Latex.makeDataColoured(_scaleSlices[s][n],note.semitonesFromOne(),adjustBySemitones=adjustBySemitones)
        return _scaleSlices

    def totalNumberOfAccidentals(self, root=None):
        """If root is None, it's in jazz, but otherwise it's in an alphabet key"""
        _accidentals = 0
        if root is None:
            for i in self.notes:
                _accidentals += len(i.leaveAccidentals())
        elif JazzNote.isAlphabetNoteStr(root):
            for note in self.byWays(root):
                _accidentals += (
                    note.count("#")
                    + note.count("b")
                    + note.count("♯")
                    + note.count("♭")
                )
        else:
            raise ValueError("Supposed to be None (for Jazz) or alphabetKeys.")
        return _accidentals

    def highestNumberOfAccidentals(self):
        """return the length of the string of accidentals, eg. Change('bbbbb5','##2') -> 5"""
        return max([len(n.leaveAccidentals()) for n in self.notes])

    def containingDisallowedNoteNames(self, allowedNotes, returnDisallowedChange=False):
        """If returnDisallowedChange==False it will return whether there was a banned note,
        otherwise if returnDisallowedChange==True it will return the notes that were disallowed"""
        allowedNotes = Change(allowedNotes)
        # Only using this memory if we need it
        if returnDisallowedChange:
            _disallowedNotes = []
        for i in self.notes:
            if i in allowedNotes.notes:
                pass
            else:
                if returnDisallowedChange == False:
                    return True
                elif returnDisallowedChange:
                    _disallowedNotes.append(i)
        if returnDisallowedChange == False:
            return False
        elif returnDisallowedChange:
            return Change(_disallowedNotes)

    def getClumps(self, returnLeftSide=True):
        _clumps = []
        _genericIntervals = self.getScaleDegrees()
        _genericIntervals = _genericIntervals + [_genericIntervals[0] + 7]
        for i in range(len(_genericIntervals) - 1):
            if _genericIntervals[i] == _genericIntervals[i + 1]:
                _clumps.append(i)
        if returnLeftSide:
            return _clumps
        else:
            return [i + 1 for i in _clumps]

    def getSkips(self, returnLeftSide=True, noteIndex=None):
        """If you supply a note to it, it will go in whatever direction provided in return left side
        And then go from that note till it finds the skip (in generic interval), returning the index where that skip starts
        """
        _genericIntervals = self.getScaleDegrees()
        _genericIntervals = _genericIntervals + [_genericIntervals[0] + 7]
        _skips = []
        _nextSkip = None
        for i in range(len(self)):
            # If the distance between the next note and this one is more than 1
            if _genericIntervals[i + 1] - _genericIntervals[i] > 1:
                if returnLeftSide:
                    _skips.append(i)
                else:
                    _skips.append(i + 1)
        # If the note is provided by index
        if noteIndex != None:
            # If it is provided as a note index
            if any([isinstance(noteIndex, t) for t in (np.int64, int)]):
                # If the note is within the range of the change
                if 0 <= noteIndex < len(self):
                    # If we are searching left
                    if returnLeftSide:
                        # search backwards from the note right to the beginning
                        for i in range(noteIndex, -1, -1):
                            # print('searching backwards from',noteIndex)
                            # Until meeting the right side of a skip
                            if i - 1 in _skips:
                                _nextSkip = i
                                break
                    # If we are searching right
                    else:
                        # search forwards from the note to the end
                        for i in range(noteIndex, len(self)):
                            # Until meeting with the left side of a skip
                            if i + 1 in _skips:
                                _nextSkip = i
                                break
                    # There is not a skip
                    if _nextSkip == None:
                        return None
                    else:
                        return _nextSkip
                else:
                    raise ValueError(
                        "expecting an index of type int, which == {} of type {},within the change, which == {},".format(
                            noteIndex, type(noteIndex), self
                        )
                    )
            else:
                raise ValueError(
                    "expecting an index of type int, which == {} of type {},within the change, which == {},".format(
                        noteIndex, type(noteIndex), self
                    )
                )
        return _skips

    def getBrickWalls(self, allowedNotes, returnMovableNotesInstead=False):
        _genericIntervals = self.getScaleDegrees(returnAsString=True)
        _genericIntervalsWithCeiling = _genericIntervals + [
            str(int(_genericIntervals[0]) + 7)
        ]

        # Check generic intervals' lengths
        if len(self) != len(_genericIntervals):
            raise ValueError("length of these is not equal", _genericIntervals, self)
        # Find the walls that are due to there being only one possibility
        _brickWalls = []
        for idx, interval in enumerate(_genericIntervals):
            _note = self[idx].inTermsOfScaleDegree(interval)
            # If there is only one spelling for the note (ex. the '5')
            if len(_note.notesWithinNoteNamesAllowed(allowedNotes)) == 1:
                # Then make that a wall
                _brickWalls.append(idx)
                # print(_note.notesWithinNoteNamesAllowed(allowedNotes), 'There was only one option')
        # Sort them ascendingly
        genericIntervals = sorted([int(i) for i in _genericIntervals])
        # back to str
        genericIntervals = [str(i) for i in genericIntervals]
        # find walls from left
        for x in range(len(_genericIntervals)):
            # Add ones that are due to the scale already being sequential
            if x + 1 == int(_genericIntervals[x]):
                _brickWalls.append(x)
            else:
                break
            # If the next note has the same interval as this one
            if _genericIntervals[x] == _genericIntervalsWithCeiling[x + 1]:
                _brickWalls.append(x)
            # print('the scale is sequential to', x, genericIntervals)
        # find walls from right
        for x in range(1, len(_genericIntervals)):
            if 8 - x == int(_genericIntervals[-x]):

                _brickWalls.append(len(self) - x)
            else:
                break
            # If the previous note has the same interval as this one
            if _genericIntervals[-x] == _genericIntervals[-(min(1 + x, len(self) - 1))]:
                _brickWalls.append(len(self) - x)
                # print('the scale is backwards sequential to', len(self) - x, _genericIntervals)

        # Now add the first note if it is a 1 (1 ,b1, #1)
        if self[0].inTermsOfScaleDegree(_genericIntervals[0]).scaleDegree() == "1":
            _brickWalls.append(0)
            # pass
        # Remove dupes and sort
        _brickWalls = list(set([n for n in sorted(_brickWalls)]))

        if returnMovableNotesInstead:  # It is the opposite
            return [i for i in range(len(self)) if i not in _brickWalls]
        else:
            return _brickWalls

    def changeGenericIntervals(self, genericIntervals):
        # Check if the genericIntervals are the same length as change
        if not len(self) == len(genericIntervals):
            raise ValueError(genericIntervals, "were not the same length as", self)
        return Change(
            [
                self[i].inTermsOfScaleDegree(genericIntervals[i])
                for i in range(len(self))
            ]
        )

    def getEnharmonicMatrix(
        self, allowedNotes, returnGenericIntervals=True, returnStr=False
    ):
        # TODO:Make it check the validity of allowed notes
        _genericIntervalMatrix = []
        for i in range(len(self)):

            _genericIntervalMatrix.append(
                self[i].notesWithinNoteNamesAllowed(allowedNotes)
            )
            if returnGenericIntervals:
                for note in range(len(_genericIntervalMatrix[-1])):
                    _genericIntervalMatrix[-1][note] = int(
                        _genericIntervalMatrix[-1][note].scaleDegree()
                    )
            if returnStr:
                _genericIntervalMatrix[-1] = [
                    str(i) for i in _genericIntervalMatrix[-1]
                ]
        if len(_genericIntervalMatrix) != len(self):
            raise ValueError("lengths dont match")

        return _genericIntervalMatrix

    def containsDistinctGenericIntervals(self, n=None):
        """where 0 <= n <=7, Get whether there are n distinct generic intervals.
        If n is not supplied, returns the number of distinct intervals"""
        if n != None and len(self) < n:
            return False
        _genericIntervals = self.getScaleDegrees()
        if n != None:
            return len(set(_genericIntervals)) == n
        elif type(n) == int and 0 <= n <= 7:
            return len(set(_genericIntervals))
        else:
            raise TypeError("Expecting int, got", type(n))

    def getHighestNote(self, returnSemitone=False):
        if returnSemitone == False:
            if len(self) == 0:
                return None
            return max(self.notes, key=lambda n: n.semitonesFromOne(octaveLimit=False))
        else:
            if len(self) == 0:
                return 0
            return max([n.semitonesFromOne(octaveLimit=False) for n in self.notes])

    def getScaleDegrees(self, returnAsString=False):
        """Get the scale degrees in the change. Where Change('1','b2','#3') would return [1,2,3].
        If returnAsString is true then it would return ['1','2','3'] instead."""
        _genericIntervals = [int(self[i].scaleDegree()) for i in range(len(self))]
        if returnAsString:
            return [str(i) for i in _genericIntervals]
        else:
            return _genericIntervals

    def forceChangeIntoAllowedNotes(self, allowedNotes, showDebug=False) -> Change:
        """Make sure the scale contains only allowedNotes to start"""

        _genericIntervals = []
        for i, noteName in enumerate(self.notes):
            # if the note name is not within allowed notes

            if noteName.plainStr() in allowedNotes:
                _genericIntervals.append(noteName.scaleDegree())
                if showDebug:
                    print(noteName, " in allowed notes")
            else:  # This note will be adjusted so that it is within allowed notes
                # Find our options for notes
                # Now go through those options and find the closest to the original
                noteOptions = noteName.notesWithinNoteNamesAllowed(allowedNotes)
                if noteOptions in ([], False, None):
                    raise ValueError(
                        "it seems",
                        noteName,
                        "does not have an enharmonic in",
                        allowedNotes,
                    )
                if showDebug:
                    print(
                        "note options for the note before filtering:",
                        noteName,
                        noteOptions,
                    )
                # Compare the distance in generic interval for each option
                noteOptions = sorted(
                    noteOptions,
                    key=lambda n: abs(
                        int(JazzNote(n).scaleDegree()) - int(noteName.scaleDegree())
                    ),
                )
                if showDebug:
                    print(
                        "note options for the note after sorting by interval distance:",
                        noteName,
                        noteOptions,
                    )
                # The minimum distance = d

                # Get rid of possibilities that 'cross over' the next interval
                for noteOption in noteOptions:
                    # If the note became larger than the next one over
                    if len(noteOptions) > 1 and int(
                        JazzNote(noteOption).scaleDegree()
                    ) < int(self[min(len(self) - 1, i - 1)].scaleDegree()):
                        noteOptions.remove(noteOption)
                        if showDebug:
                            print(
                                noteOption, "was less than the note before and removed!"
                            )
                        pass
                    # if int(JazzNote(noteOption).scaleDegree()) > int(
                    if len(noteOptions) > 1 and int(
                        JazzNote(noteOption).scaleDegree()
                    ) > int(self[min(i + 1, len(self) - 1)].scaleDegree()):
                        noteOptions.remove(noteOption)
                        if showDebug:
                            print(
                                noteOption, "was more than the note after and removed!"
                            )
                    if showDebug:
                        print(
                            "help me nina",
                            self,
                            "noteoptions",
                            noteOption,
                            "trigger",
                            int(JazzNote(noteOption).scaleDegree())
                            > int(self[min(i + 1, len(self) - 1)].scaleDegree()),
                        )

                if showDebug:
                    print("debugging force {} ".format(noteOptions))
                # Get rid of any possibilities which are further away in generic interval
                _minD = abs(
                    int(noteOptions[0].scaleDegree()) - int(noteName.scaleDegree())
                )
                noteOptions = filter(
                    lambda n: _minD
                    >= abs(
                        int(JazzNote(n).scaleDegree()) - int(noteName.scaleDegree())
                    ),
                    noteOptions,
                )
                noteOptions = list(noteOptions)
                # noteOptions = list(filter(lambda n: abs(int(JazzNote(n).scaleDegree()) - int(noteName.scaleDegree())),noteOptions))
                if showDebug:
                    print("sorted note options for the note:", noteName, noteOptions)
                # Pick the first one left (only one?)
                _genericIntervals.append(noteOptions[0].scaleDegree())
                # Now the thing has started out using notes that it can use
                if showDebug:
                    print(noteName, "not in allowed notes")
                    # print(self.getChangeNumber(addOneToBookPage=True), self, self.getScaleNames())
        return self.changeGenericIntervals(_genericIntervals)

    def preferNotes(
        self, preferSharpFive, preferSharpFour, preferSharpTwo, allowedNotes
    ):
        _adjustedSelf = self
        _genericIntervals = self.getScaleDegrees()
        # Obviously we are preferring it over the b6
        if allowedNotes == None:
            allowedNotes = Change.allowedNoteNamesJazz
        if preferSharpFive:
            # If the change includes the b6
            if _adjustedSelf.containsNotes("b6", byAnotherName=False):

                _noteToChange = np.where(_adjustedSelf.notes == JazzNote("b6"))[0][0]
                # print(self)
                # input(_noteToChange)
                # _noteToChange = _adjustedSelf.notes.index(JazzNote('b6'))

                # if there is not a 5 there
                if not 5 in _genericIntervals and "#5" in allowedNotes:
                    # Then make it a #5
                    _adjustedSelf.notes[_noteToChange] = JazzNote("#5")
                elif _adjustedSelf.getSkips(noteIndex=_noteToChange) != None:
                    _nextSkipLeft = _adjustedSelf.getSkips(noteIndex=_noteToChange)
                    if all(
                        [
                            _adjustedSelf[i]
                            .inTermsOfScaleDegree(_genericIntervals[i] - 1)
                            .plainStr()
                            in Change.allowedNoteNamesSimpleJazz
                            and _adjustedSelf[i]
                            .inTermsOfScaleDegree(_genericIntervals[i] - 1)
                            .plainStr()
                            in allowedNotes
                            for i in range(_nextSkipLeft, _noteToChange + 1)
                        ]
                    ):
                        # Then for each of them
                        for i in range(_nextSkipLeft, _noteToChange + 1):
                            # Lower their generic interval by 1
                            _adjustedSelf.notes[i] = _adjustedSelf.notes[
                                i
                            ].inTermsOfScaleDegree(_genericIntervals[i] - 1)
            else:
                # does not contain a b6
                pass
        # It only uses #4 if there is also a 4 and 5
        if preferSharpFour:
            if _adjustedSelf.containsNotes("5", "b5", "4", byAnotherName=False):
                if "#4" in allowedNotes:
                    # _adjustedSelf.notes[_adjustedSelf.notes.index(JazzNote('b5'))] = JazzNote('#4')
                    _adjustedSelf.notes[
                        np.where(_adjustedSelf.notes == JazzNote("b5"))
                    ] = JazzNote("#4")

        if preferSharpTwo:
            if _adjustedSelf.containsNotes("b3", "3", byAnotherName=False):
                if not _adjustedSelf.containsNotes("2", "b2", byAnotherName=False):
                    # _adjustedSelf.notes[_adjustedSelf.notes.index(JazzNote('b3'))] = JazzNote('#2')
                    _adjustedSelf.notes[
                        np.where(_adjustedSelf.notes == JazzNote("b3"))
                    ] = JazzNote("#2")
        return _adjustedSelf

    def straightenDegrees(
        self,
        allowedNotes=None,
        showDebug=False,
        forceOne=True,
        preferSharpFive=True,
        preferSharpFour=True,
        preferSharpTwo=True,
        preferSupersetOverLessAccidentals=False,
        firstTimeThroughTheFunction=True,
    ) -> Change:

        callerParameters = locals()
        callerParameters.__delitem__("self")

        cachedName = (
            self.__repr__()
            + ".straightenDegrees("
            + str(list(callerParameters.values()))[1:-1]
            + ")"
        )

        try:
            return Change.cache[cachedName]
        except KeyError:
            pass

        # TODO:make #54 use #4 and #5, following prefer sharp five better
        _didAddOne = False
        _adjustedSelf = self
        if allowedNotes == None:
            allowedNotes = Change.allowedNoteNamesJazz
        else:  # Allowed Notes were specified
            # If the allowed notes specified has all 12 notes
            if Change.hasAllTwelveNotes(allowedNotes):
                pass
            else:  # allowed notes doesn't have all twelve notes
                raise ValueError(
                    allowedNotes, "does not contain a note for each of the 12 notesets"
                )
        # If there is no one
        if forceOne and not self.containsNotes("1"):
            # Add a one
            return (
                Change(np.concatenate([[JazzNote("1")], self.notes]))
                .straightenDegrees(allowedNotes)
                .withoutNote("1")
            )
        else:
            # (The change contains a '1') Don't do nothin' cause it's all g
            pass

        # If this set contains all the jazz notes
        # and the allowed notes are not jazz (so as not to make an infinite loop)
        if (
            all([i in allowedNotes for i in Change.allowedNoteNamesJazz])
            and allowedNotes != Change.allowedNoteNamesJazz
        ):
            _jazzSelf = self.straightenDegrees(Change.allowedNoteNamesJazz)
            if _jazzSelf.containsDistinctGenericIntervals(min(7, len(self))):
                return _jazzSelf.preferNotes(
                    preferSharpFive, preferSharpFour, preferSharpTwo, allowedNotes
                )
            _leftSkips = _jazzSelf.getSkips(returnLeftSide=True)
            _rightSkips = _jazzSelf.getSkips(returnLeftSide=False)
            _leftClumps = _jazzSelf.getClumps(returnLeftSide=True)
            _rightClumps = _jazzSelf.getClumps(returnLeftSide=False)
            _enharmonicMatrix = _jazzSelf.getEnharmonicMatrix(allowedNotes)
            _genericIntervals = _jazzSelf.getScaleDegrees()

            if len(_rightSkips) > 0:
                if showDebug:
                    print(
                        "there are skips happening",
                        _jazzSelf,
                        "rightclumps",
                        _rightClumps,
                        "leftclumps",
                        _leftClumps,
                        "rightskips",
                        _rightSkips,
                        "leftskips",
                        _leftSkips,
                        _jazzSelf.getScaleDegrees(),
                    )
                # if all([i in _leftClumps or i+1 in _rightClumps for i in _leftSkips]):
                for i in _leftSkips:
                    if showDebug:
                        print("a rightclump coexists with a left skip")
                    # If the note before the clump is a skip
                    if i in _rightClumps:
                        if showDebug:
                            input(
                                "press Enter. we propose panacea to the Decrease"
                                + str(_jazzSelf)
                                + "  note"
                                + str(_jazzSelf.notes[i])
                                + " i"
                                + str(i)
                            )
                        if _genericIntervals[i] - 1 in _enharmonicMatrix[i]:
                            _diminishedNote = _jazzSelf.notes[i].inTermsOfScaleDegree(
                                _genericIntervals[i] - 1
                            )
                            _diminishedJazzSelf = _jazzSelf
                            _diminishedJazzSelf.notes[i] = _diminishedJazzSelf.notes[
                                i
                            ].inTermsOfScaleDegree(_genericIntervals[i] - 1)

                            if len(_diminishedNote.leaveAccidentals()) < 2:
                                if showDebug:
                                    print(
                                        "diminishing because the skip is to the right,(Decrease) ",
                                        _jazzSelf.notes[i],
                                        end=" ",
                                    )
                                _jazzSelf.notes[i] = _diminishedNote
                            if showDebug:
                                input("becomes" + str(_jazzSelf.notes[i]))
                            if _diminishedJazzSelf.containsDistinctGenericIntervals(
                                min(7, len(_jazzSelf))
                            ):
                                return _diminishedJazzSelf.preferNotes(
                                    preferSharpFive,
                                    preferSharpFour,
                                    preferSharpTwo,
                                    allowedNotes,
                                )
                for i in _rightClumps:
                    if i in _leftSkips:
                        if showDebug:
                            input(
                                "press Enter. there is a right clump at "
                                + str(_rightClumps[0])
                                + " and right skip at "
                                + str(_rightSkips[0])
                            )
                        if _genericIntervals[i] + 1 in _enharmonicMatrix[i]:
                            _augmentedNote = _jazzSelf.notes[i].inTermsOfScaleDegree(
                                _genericIntervals[i] + 1
                            )
                            if showDebug:
                                print("the augmented note is allowed", _augmentedNote)
                            # if len(_augmentedNote.leaveAccidentals()) < 2:
                            _augmentedJazzSelf = _jazzSelf
                            _augmentedJazzSelf.notes[i] = _augmentedJazzSelf.notes[
                                i
                            ].inTermsOfScaleDegree(_genericIntervals[i] + 1)
                            if _jazzSelf.containsDistinctGenericIntervals(
                                min(7, len(self))
                            ):  # Add and see if it fixes generic intervals
                                if showDebug:
                                    print(
                                        "augmenting because the skip is to the right,(Increase)",
                                        _jazzSelf.notes[i],
                                        end=" ",
                                    )
                                _jazzSelf.notes[i] = _augmentedNote
                                if showDebug:
                                    input("becomes" + str(_jazzSelf.notes[i]))
                            if _augmentedJazzSelf.containsDistinctGenericIntervals(
                                min(7, len(_jazzSelf))
                            ):
                                return _augmentedJazzSelf.preferNotes(
                                    preferSharpFive,
                                    preferSharpFour,
                                    preferSharpTwo,
                                    allowedNotes,
                                )

        # Sort by semitone position
        _adjustedSelf = _adjustedSelf.sortBySemitonePosition()
        # TODO: make it so it saves the difference in order so that it can restore it at the end"
        "that is so that it can straighten the numbers of a non-sequential change "
        "and put them back into (dis)order at the end. For now it forces them into order"

        # now that the self is adjusted, what are its notes' name-matrixes
        _genericIntervalMatrix = _adjustedSelf.getEnharmonicMatrix(allowedNotes)

        if str(_adjustedSelf) != str(
            _adjustedSelf.forceChangeIntoAllowedNotes(allowedNotes)
        ):
            if showDebug:
                print(
                    "adjusted notes to make them only contain allowed ones",
                    _adjustedSelf,
                    "into",
                    _adjustedSelf.forceChangeIntoAllowedNotes(allowedNotes),
                )

        # Replace notes that are not allowed (because they are not in allowed notes)
        _adjustedSelf = _adjustedSelf.forceChangeIntoAllowedNotes(allowedNotes)

        if _adjustedSelf.containsDistinctGenericIntervals(len(self)):
            return _adjustedSelf.preferNotes(
                preferSharpFive, preferSharpFour, preferSharpTwo, allowedNotes
            )
        # Refresh
        _needsRefresh = False
        _genericIntervals = _adjustedSelf.getScaleDegrees()
        _genericIntervalsWithCeiling = _genericIntervals + [_genericIntervals[0] + 7]
        _clumps = _adjustedSelf.getClumps(returnLeftSide=True)
        _movableNotes = _adjustedSelf.getBrickWalls(
            allowedNotes, returnMovableNotesInstead=True
        )
        _skips = _adjustedSelf.getSkips()

        # Fix notes that are one away first
        # For every note in order
        for note in range(1, len(_adjustedSelf)):
            # Find the first skip going backwards
            _nextSkipLeft = _adjustedSelf.getSkips(returnLeftSide=True, noteIndex=note)
            # Find the first skip going fowards
            _nextSkipRight = _adjustedSelf.getSkips(
                returnLeftSide=False, noteIndex=note
            )
            # if _nextSkipRight != None: input(str(_adjustedSelf)+str(_nextSkipRight)+' nextSkipRight')

            # if the previous note is the same as this one,
            if _genericIntervals[note - 1] == _genericIntervals[note]:
                # If the next note is over 1 away,
                if (
                    _genericIntervalsWithCeiling[note + 1] - _genericIntervals[note]
                    >= 2
                ):
                    # if this note can move, and increasing it is valid.
                    if (
                        note in _movableNotes
                        and _genericIntervals[note] + 1 in _genericIntervalMatrix[note]
                    ):
                        # it's allowed and it's movable
                        # Then raise this note up by one
                        _adjustedSelf.notes[note] = _adjustedSelf.notes[
                            note
                        ].inTermsOfScaleDegree(_genericIntervals[note] + 1)
                        # and refresh before next note
                        _genericIntervals = _adjustedSelf.getScaleDegrees()
                        _genericIntervalsWithCeiling = _genericIntervals + [
                            _genericIntervals[0] + 7
                        ]
                        _movableNotes = _adjustedSelf.getBrickWalls(
                            allowedNotes, returnMovableNotesInstead=True
                        )
                        _nextSkipLeft = _adjustedSelf.getSkips(
                            returnLeftSide=True, noteIndex=note
                        )
                        _nextSkipRight = _adjustedSelf.getSkips(
                            returnLeftSide=False, noteIndex=note
                        )
                # else there is a string of notes that can be augmented leading to a skip (going right)
                elif (
                    _nextSkipRight != None
                    and not _adjustedSelf.containsDistinctGenericIntervals(
                        min(7, len(self))
                    )
                ):
                    # If all the notes leading to the skip can be augmented by 1
                    if all(
                        [
                            _genericIntervals[i] + 1 in _genericIntervalMatrix[i]
                            for i in range(note, _nextSkipRight + 1)
                        ]
                    ):
                        # TODO: make it check if it's making things worse
                        # If doing so would not make things worse
                        # If the series of adjustments would introduce extra accidentals
                        # by lead
                        if True:
                            # Then for each of them
                            for i in range(note, _nextSkipRight + 1):
                                # Raise their generic interval by 1
                                _adjustedSelf.notes[i] = _adjustedSelf.notes[
                                    i
                                ].inTermsOfScaleDegree(_genericIntervals[i] + 1)
                            # and refresh before next note
                            _genericIntervals = _adjustedSelf.getScaleDegrees()
                            _genericIntervalsWithCeiling = _genericIntervals + [
                                _genericIntervals[0] + 7
                            ]
                            _movableNotes = _adjustedSelf.getBrickWalls(
                                allowedNotes, returnMovableNotesInstead=True
                            )
                            _nextSkipLeft = _adjustedSelf.getSkips(
                                returnLeftSide=True, noteIndex=note
                            )
                            _nextSkipRight = _adjustedSelf.getSkips(
                                returnLeftSide=False, noteIndex=note
                            )

            # if the next note is the same as this one, or this note has interval of 7 and the next does too
            if _genericIntervals[note] == _genericIntervalsWithCeiling[note + 1] or (
                _genericIntervals[note] == 7
                and _genericIntervalsWithCeiling[note + 1] == 7
            ):  # or \
                # (preferSharpFive and _adjustedSelf[note] == JazzNote('b6') ):
                # if the previous note is over 1 away, (The skip is to the left of the clump)
                if _genericIntervals[note] - _genericIntervals[note - 1] >= 2:
                    # if it's movable and can be diminished
                    if (
                        note in _movableNotes
                        and _genericIntervals[note] - 1 in _genericIntervalMatrix[note]
                    ):
                        # Then drop this note down by one
                        _adjustedSelf.notes[note] = _adjustedSelf.notes[
                            note
                        ].inTermsOfScaleDegree(_genericIntervals[note] - 1)
                        # and refresh before next note
                        _genericIntervals = _adjustedSelf.getScaleDegrees()
                        _genericIntervalsWithCeiling = _genericIntervals + [
                            _genericIntervals[0] + 7
                        ]
                        _movableNotes = _adjustedSelf.getBrickWalls(
                            allowedNotes, returnMovableNotesInstead=True
                        )
                        _nextSkipLeft = _adjustedSelf.getSkips(
                            returnLeftSide=True, noteIndex=note
                        )
                        _nextSkipRight = _adjustedSelf.getSkips(
                            returnLeftSide=False, noteIndex=note
                        )
                # else there is a string of notes that can be diminished leading to a skip (going left)
                elif (
                    _nextSkipLeft != None
                    and not _adjustedSelf.containsDistinctGenericIntervals(
                        min(7, len(self))
                    )
                ):
                    # raise TypeError('it is happening with', _adjustedSelf, 'note', _adjustedSelf[note], 'next skip left',
                    #                _adjustedSelf[_nextSkipLeft], 'skips', _adjustedSelf.getSkips(),'slice we\'re talking about adjusting',_adjustedSelf.notes[_nextSkipLeft:note+1],_genericIntervals[note]-1 in _genericIntervalMatrix[note])

                    # If all the notes leading to the skip can be diminished by 1
                    if all(
                        [
                            _genericIntervals[i] - 1 in _genericIntervalMatrix[i]
                            for i in range(_nextSkipLeft, note + 1)
                        ]
                    ):
                        # raise TypeError(_adjustedSelf[_nextSkipLeft:note+1],'all of them in a row can be adjusted')
                        # Then for each of them
                        for i in range(_nextSkipLeft, note + 1):
                            # Lower their generic interval by 1
                            _adjustedSelf.notes[i] = _adjustedSelf.notes[
                                i
                            ].inTermsOfScaleDegree(_genericIntervals[i] - 1)
                        # and refresh before next note
                        _genericIntervals = _adjustedSelf.getScaleDegrees()
                        _genericIntervalsWithCeiling = _genericIntervals + [
                            _genericIntervals[0] + 7
                        ]
                        _movableNotes = _adjustedSelf.getBrickWalls(
                            allowedNotes, returnMovableNotesInstead=True
                        )
                        _nextSkipLeft = _adjustedSelf.getSkips(
                            returnLeftSide=True, noteIndex=note
                        )
                        _nextSkipRight = _adjustedSelf.getSkips(
                            returnLeftSide=False, noteIndex=note
                        )

        # Get rid of the extra accidentals
        # If The change contains 1 2 3 4 5 6 7 as generic intervals and double of notes

        # check the change before fixing it after
        if _adjustedSelf.containingDisallowedNoteNames(allowedNotes):
            raise ValueError(
                "if _adjustedSelf.containingDisallowedNoteNames(allowedNotes), and it happened in the main part of the code ;("
            )

        if _adjustedSelf.containsDistinctGenericIntervals(min(7, len(_adjustedSelf))):
            # If jazz notes are a subset of allowed notes
            # but allowed notes is not the jazz notes
            if (
                all([i in allowedNotes for i in Change.allowedNoteNamesJazz])
                and allowedNotes != Change.allowedNoteNamesJazz
            ):

                _jazzSelf = self.straightenDegrees(Change.allowedNoteNamesJazz)
                if _jazzSelf.containsDistinctGenericIntervals(
                    min(7, len(_adjustedSelf))
                ):
                    return _jazzSelf.preferNotes(
                        preferSharpFive, preferSharpFour, preferSharpTwo, allowedNotes
                    )
                """else:
                    _jazzLeftSkips = _jazzSelf.getSkips(returnLeftSide=True)
                    _jazzRightSkips = _jazzSelf.getSkips(returnLeftSide=False)
                    print('jazzrightskips',_jazzRightSkips,'jazzleftskips',_jazzLeftSkips)
                    for leftClump in _jazzSelf.getClumps():
                        _leftSkip = leftClump - 1
                        _rightClump = leftClump + 1
                        _rightSkip = _rightClump + 1
                        if _genericIntervals[_rightSkip] + 1 in _genericIntervalMatrix[_rightSkip]:
                            _jazzSelf.notes[_rightSkip] = _jazzSelf.notes[_rightSkip].inTermsOfScaleDegree(_genericIntervals[_rightSkip] + 1)
                        elif _genericIntervals[_leftSkip] - 1 in _genericIntervalMatrix[_leftSkip]:
                            _jazzSelf.notes[_leftSkip] = _jazzSelf.notes[_leftSkip].inTermsOfScaleDegree(
                                _genericIntervals[_leftSkip] - 1)
                    if _jazzSelf.containsDistinctGenericIntervals(min(7, len(_adjustedSelf))):
                        return _jazzSelf"""

            _firstClump = None
            # print('before "removing" accidentals ;)',_adjustedSelf)
            for i in range(len(self) - 1, -1, -1):
                # print(_genericIntervals,_genericIntervalsWithCeiling,_adjustedSelf,self,'bro',sep=', ')
                # if this note is the same as the one to the right
                if _genericIntervals[i] == _genericIntervalsWithCeiling[i + 1]:
                    # That is the first clump from the right
                    _firstClump = i
                    break
            # This loop goes left from the first clumped note to the third note
            _leftNoteToChange = None
            _notesToReduce = []
            _notesCanReduce = []
            if _firstClump == None:
                _firstClump = 0  # That just disables the loop
            for n in range(_firstClump, 1, -1):
                # IF this note being one less makes it better
                _adjustedInterval = _genericIntervals[n] - 1
                # If taking away 1 in generic interval is allowed
                if _adjustedInterval in _genericIntervalMatrix[n]:
                    _adjustedNote = _adjustedSelf[n].inTermsOfScaleDegree(
                        _adjustedInterval
                    )
                    _originalNote = _adjustedSelf[n]
                    # print('comparing big notes with reduced ones,',_adjustedSelf[n].plainStr(),_adjustedNote.note)
                    if len(_originalNote.note) > len(_adjustedNote.note) or (
                        _adjustedNote.note in Change.allowedNoteNamesSuperset
                        and not _originalNote.note in Change.allowedNoteNamesSuperset
                    ):  # yoda
                        _notesToReduce.append(n)
                    elif (
                        len(_originalNote.note) <= len(_adjustedNote.note)
                        and _adjustedNote.note in Change.allowedNoteNamesSuperset
                    ):
                        _notesCanReduce.append(n)
                    if not (
                        (_adjustedSelf[n].plainStr() in Change.allowedNoteNamesSuperset)
                        or len(_adjustedSelf[n].note) > len(_adjustedNote.note)
                    ) and (
                        _adjustedNote.note
                        in Change.allowedNoteNamesJazz + Change.allowedNoteNamesCarnatic
                        or len(_adjustedSelf[n].note) < len(_adjustedNote.note)
                    ):
                        # if the old note has more accidentals than the adjusted note ^
                        _leftNoteToChange = n

            # print(_adjustedSelf,_firstClump,sep=' , ',end='\n')
            if False:  # _leftNoteToChange != None:
                # print('before adjusting',_adjustedSelf)
                # print('happening',list(range(_firstClump,_leftNoteToChange-1,-1)))
                for n in range(_firstClump, _leftNoteToChange - 1, -1):
                    _adjustedSelf.notes[n] = _adjustedSelf[n].inTermsOfScaleDegree(
                        _genericIntervals[n] - 1
                    )

                # and refresh before next note
                _genericIntervals = _adjustedSelf.getScaleDegrees()
                _genericIntervalsWithCeiling = _genericIntervals + [
                    _genericIntervals[0] + 7
                ]
                _movableNotes = _adjustedSelf.getBrickWalls(
                    allowedNotes, returnMovableNotesInstead=True
                )
                _nextSkipLeft = _adjustedSelf.getSkips(
                    returnLeftSide=True, noteIndex=note
                )
                _nextSkipRight = _adjustedSelf.getSkips(
                    returnLeftSide=False, noteIndex=note
                )
            if len(_notesToReduce) > 0 and len(_adjustedSelf.getClumps()) > 0:
                _possibleNotesToReduceTo = _notesToReduce + _notesCanReduce
                if showDebug:
                    print(
                        "clumpos",
                        _adjustedSelf,
                        _adjustedSelf.getClumps(),
                        "notes to reduce",
                        _notesToReduce,
                    )
                _largerNotes = Change(
                    [
                        _adjustedSelf[i]
                        for i in range(
                            min(_notesToReduce), _adjustedSelf.getClumps()[-1] + 1
                        )
                    ]
                )
                _smallerNotes = Change(
                    [
                        _adjustedSelf[i].inTermsOfScaleDegree(_genericIntervals[i] - 1)
                        for i in range(
                            min(_notesToReduce), _adjustedSelf.getClumps()[-1] + 1
                        )
                    ]
                )
                if showDebug:
                    print(
                        "length of accidentals",
                        _largerNotes.highestNumberOfAccidentals(),
                        _smallerNotes.highestNumberOfAccidentals(),
                        _largerNotes.totalNumberOfAccidentals(),
                        _smallerNotes.totalNumberOfAccidentals(),
                    )
                # if there is a string of either notes to reduce or notes that can leading to a clump
                if (
                    all(
                        [
                            i in _possibleNotesToReduceTo
                            for i in range(
                                min(_notesToReduce), _adjustedSelf.getClumps()[-1] + 1
                            )
                        ]
                    )
                    and _smallerNotes.totalNumberOfAccidentals()
                    <= _largerNotes.totalNumberOfAccidentals()
                ):
                    # for all the notes that need to be reduced
                    # print('there there is a string of either notes to reduce or notes that can leading to a clump')
                    for n in range(
                        min(_notesToReduce), _adjustedSelf.getClumps()[-1] + 1
                    ):
                        # Drop all the notes to reduce by one
                        _adjustedSelf.notes[n] = _adjustedSelf.notes[
                            n
                        ].inTermsOfScaleDegree(_genericIntervals[n] - 1)
                        # Debug info
                        if n in _notesToReduce:
                            _notesToReduce.remove(n)
                        if n in _notesCanReduce:
                            _notesCanReduce.remove(n)
                    # DEBUG INFO
                    _notesToReduce = []
                    # and refresh before next note
                    _genericIntervals = _adjustedSelf.getScaleDegrees()
                    _genericIntervalsWithCeiling = _genericIntervals + [
                        _genericIntervals[0] + 7
                    ]
                    _movableNotes = _adjustedSelf.getBrickWalls(
                        allowedNotes, returnMovableNotesInstead=True
                    )
                    _nextSkipLeft = _adjustedSelf.getSkips(
                        returnLeftSide=True, noteIndex=note
                    )
                    _nextSkipRight = _adjustedSelf.getSkips(
                        returnLeftSide=False, noteIndex=note
                    )

                # elif the bigger notes have a higher maximum amount of accidentals
                # or the bigger notes have more accidentals than the littler ones
                elif (
                    _largerNotes.highestNumberOfAccidentals()
                    > _smallerNotes.highestNumberOfAccidentals()
                    or _largerNotes.totalNumberOfAccidentals()
                    > _smallerNotes.totalNumberOfAccidentals()
                    and not _smallerNotes.containingDisallowedNoteNames(allowedNotes)
                ):

                    if showDebug:
                        print(
                            "deciding between",
                            str(_smallerNotes) + " vs. " + str(_largerNotes),
                        )

                    # if we're preferring notes within the superset (they are in jazz or carnatic)

                    if preferSupersetOverLessAccidentals:
                        # if the smaller notes contain notes outside of the superset #and the big ones don't
                        if _smallerNotes.containingDisallowedNoteNames(
                            Change.allowedNoteNamesSuperset
                        ) and not _largerNotes.containingDisallowedNoteNames(
                            Change.allowedNoteNamesSuperset
                        ):
                            # Then leave things as they are on the bigger numbers
                            pass
                        # if the larger notes contain notes outside of the superset #and the small ones don't
                        elif _largerNotes.containingDisallowedNoteNames(
                            Change.allowedNoteNamesSuperset
                        ) and not _smallerNotes.containingDisallowedNoteNames(
                            Change.allowedNoteNamesSuperset
                        ):
                            # Then diminish the numbers
                            for n in range(
                                min(_notesToReduce), _adjustedSelf.getClumps()[-1] + 1
                            ):
                                # Drop all the notes to reduce by one
                                _adjustedSelf.notes[n] = _adjustedSelf.notes[
                                    n
                                ].inTermsOfScaleDegree(_genericIntervals[n] - 1)
                                # Debug info
                                if n in _notesToReduce:
                                    _notesToReduce.remove(n)
                                if n in _notesCanReduce:
                                    _notesCanReduce.remove(n)

                            # and refresh before next note
                            _genericIntervals = _adjustedSelf.getScaleDegrees()
                            _genericIntervalsWithCeiling = _genericIntervals + [
                                _genericIntervals[0] + 7
                            ]
                            _movableNotes = _adjustedSelf.getBrickWalls(
                                allowedNotes, returnMovableNotesInstead=True
                            )
                            _nextSkipLeft = _adjustedSelf.getSkips(
                                returnLeftSide=True, noteIndex=note
                            )
                            _nextSkipRight = _adjustedSelf.getSkips(
                                returnLeftSide=False, noteIndex=note
                            )

                    # elif we are not preferring the superset, (then we're preferring less accidentals)
                    elif not preferSupersetOverLessAccidentals:
                        # If the original larger numbers were allowed but the reduced ones were not
                        if _smallerNotes.containingDisallowedNoteNames(
                            allowedNotes
                        ) and not _largerNotes.containingDisallowedNoteNames(
                            allowedNotes
                        ):
                            # Then leave things as they are on the bigger numbers
                            if showDebug:
                                print(
                                    "it could have passed right by, as nothing was done, because changing the notes would have brought them out of being allowed"
                                )
                        # If the original larger numbers were not allowed but the reduced ones were allowed
                        elif _largerNotes.containingDisallowedNoteNames(
                            allowedNotes
                        ) and not _smallerNotes.containingDisallowedNoteNames(
                            allowedNotes
                        ):
                            raise ValueError(
                                "Things should not have ended up here, because the original notes should have been valid"
                            )
                        # if the smaller numbers contain fewer max accidentals than the larger
                        elif (
                            _smallerNotes.highestNumberOfAccidentals()
                            < _largerNotes.highestNumberOfAccidentals()
                        ):
                            # then diminish the series
                            for n in range(
                                min(_notesToReduce), _adjustedSelf.getClumps()[-1] + 1
                            ):
                                # Drop all the notes to reduce by one
                                _adjustedSelf.notes[n] = _adjustedSelf.notes[
                                    n
                                ].inTermsOfScaleDegree(_genericIntervals[n] - 1)
                                # Debug info
                                if n in _notesToReduce:
                                    _notesToReduce.remove(n)
                                if n in _notesCanReduce:
                                    _notesCanReduce.remove(n)

                            # and refresh before next note
                            _genericIntervals = _adjustedSelf.getScaleDegrees()
                            _genericIntervalsWithCeiling = _genericIntervals + [
                                _genericIntervals[0] + 7
                            ]
                            _movableNotes = _adjustedSelf.getBrickWalls(
                                allowedNotes, returnMovableNotesInstead=True
                            )
                            _nextSkipLeft = _adjustedSelf.getSkips(
                                returnLeftSide=True, noteIndex=note
                            )
                            _nextSkipRight = _adjustedSelf.getSkips(
                                returnLeftSide=False, noteIndex=note
                            )

                        # elif the larger number contain fewer max accidentals than the smaller
                        elif (
                            _smallerNotes.highestNumberOfAccidentals()
                            > _largerNotes.highestNumberOfAccidentals()
                        ):
                            # Then leave things as they are
                            pass
                        # else they contain the same max amount of accidentals
                        elif (
                            _smallerNotes.highestNumberOfAccidentals()
                            == _largerNotes.highestNumberOfAccidentals()
                        ):
                            # If the smaller numbers contain fewer total accidentals
                            if (
                                _smallerNotes.totalNumberOfAccidentals()
                                < _largerNotes.totalNumberOfAccidentals()
                            ):
                                # Diminish the series
                                for n in range(
                                    min(_notesToReduce),
                                    _adjustedSelf.getClumps()[-1] + 1,
                                ):
                                    # Drop all the notes to reduce by one
                                    _adjustedSelf.notes[n] = _adjustedSelf.notes[
                                        n
                                    ].inTermsOfScaleDegree(_genericIntervals[n] - 1)
                                    # Debug info
                                    if n in _notesToReduce:
                                        _notesToReduce.remove(n)
                                    if n in _notesCanReduce:
                                        _notesCanReduce.remove(n)

                                # and refresh before next note
                                _genericIntervals = _adjustedSelf.getScaleDegrees()
                                _genericIntervalsWithCeiling = _genericIntervals + [
                                    _genericIntervals[0] + 7
                                ]
                                _movableNotes = _adjustedSelf.getBrickWalls(
                                    allowedNotes, returnMovableNotesInstead=True
                                )
                                _nextSkipLeft = _adjustedSelf.getSkips(
                                    returnLeftSide=True, noteIndex=note
                                )
                                _nextSkipRight = _adjustedSelf.getSkips(
                                    returnLeftSide=False, noteIndex=note
                                )

                            # Elif the larger numbers contain fewer accidentals
                            elif (
                                _smallerNotes.totalNumberOfAccidentals()
                                > _largerNotes.totalNumberOfAccidentals()
                            ):
                                pass
                                # Leave them how they are
                            # if they are tied for total number of accidentals
                            else:
                                # if the smaller notes contain fewer superset notes than the larger
                                if len(
                                    _smallerNotes.containingDisallowedNoteNames(
                                        Change.allowedNoteNamesSuperset,
                                        returnDisallowedChange=True,
                                    )
                                ) < len(
                                    _largerNotes.containingDisallowedNoteNames(
                                        Change.allowedNoteNamesSuperset,
                                        returnDisallowedChange=True,
                                    )
                                ):
                                    # Diminish the series
                                    for n in range(
                                        min(_notesToReduce),
                                        _adjustedSelf.getClumps()[-1] + 1,
                                    ):
                                        # Drop all the notes to reduce by one
                                        _adjustedSelf.notes[n] = _adjustedSelf.notes[
                                            n
                                        ].inTermsOfScaleDegree(_genericIntervals[n] - 1)
                                        # Debug info
                                        if n in _notesToReduce:
                                            _notesToReduce.remove(n)
                                        if n in _notesCanReduce:
                                            _notesCanReduce.remove(n)

                                    # and refresh before next note
                                    _genericIntervals = _adjustedSelf.getScaleDegrees()
                                    _genericIntervalsWithCeiling = _genericIntervals + [
                                        _genericIntervals[0] + 7
                                    ]
                                    _movableNotes = _adjustedSelf.getBrickWalls(
                                        allowedNotes, returnMovableNotesInstead=True
                                    )
                                    _nextSkipLeft = _adjustedSelf.getSkips(
                                        returnLeftSide=True, noteIndex=note
                                    )
                                    _nextSkipRight = _adjustedSelf.getSkips(
                                        returnLeftSide=False, noteIndex=note
                                    )
                                # if the larger notes contain fewer superset notes than the smaller
                                elif len(
                                    _largerNotes.containingDisallowedNoteNames(
                                        Change.allowedNoteNamesSuperset,
                                        returnDisallowedChange=True,
                                    )
                                ) < len(
                                    _smallerNotes.containingDisallowedNoteNames(
                                        Change.allowedNoteNamesSuperset,
                                        returnDisallowedChange=True,
                                    )
                                ):
                                    # leave them how they are
                                    pass
                                # else if they are tied for superset notes
                                else:
                                    input("they are tied for superset notes")

                # if the rightmost note of those that need to be brought down is same as next note
                elif (
                    _genericIntervals[_notesToReduce[0]]
                    == _genericIntervalsWithCeiling[_notesToReduce[0] + 1]
                ):
                    # for all the notes that need to be reduced
                    for n in _notesToReduce:
                        # Drop all the notes to reduce by one
                        _adjustedSelf.notes[n] = _adjustedSelf.notes[
                            n
                        ].inTermsOfScaleDegree(_genericIntervals[n] - 1)

                    # DEBUG INFO
                    _notesToReduce = []

                    # and refresh before next note
                    _genericIntervals = _adjustedSelf.getScaleDegrees()
                    _genericIntervalsWithCeiling = _genericIntervals + [
                        _genericIntervals[0] + 7
                    ]
                    _movableNotes = _adjustedSelf.getBrickWalls(
                        allowedNotes, returnMovableNotesInstead=True
                    )
                    _nextSkipLeft = _adjustedSelf.getSkips(
                        returnLeftSide=True, noteIndex=note
                    )
                    _nextSkipRight = _adjustedSelf.getSkips(
                        returnLeftSide=False, noteIndex=note
                    )
                # otherwise if the next note can be brought down because it is movable and next to a skip
                elif (
                    _notesToReduce[0] + 1 in _notesCanReduce
                    and _genericIntervals[_notesToReduce[0] + 1]
                    == _genericIntervalsWithCeiling[_notesToReduce[0] + 2]
                ):
                    # for all the notes that need to be reduced plus the one that can be reduced because of the reason above
                    for n in _notesToReduce + [_notesToReduce[0] + 1]:
                        # Drop all the notes to reduce by one
                        _adjustedSelf.notes[n] = _adjustedSelf.notes[
                            n
                        ].inTermsOfScaleDegree(_genericIntervals[n] - 1)
                    # DEBUG INFO
                    _notesCanReduce.remove(_notesToReduce[0] + 1)
                    _notesToReduce = []

                    # and refresh before next note
                    _genericIntervals = _adjustedSelf.getScaleDegrees()
                    _genericIntervalsWithCeiling = _genericIntervals + [
                        _genericIntervals[0] + 7
                    ]
                    _movableNotes = _adjustedSelf.getBrickWalls(
                        allowedNotes, returnMovableNotesInstead=True
                    )
                    _nextSkipLeft = _adjustedSelf.getSkips(
                        returnLeftSide=True, noteIndex=note
                    )
                    _nextSkipRight = _adjustedSelf.getSkips(
                        returnLeftSide=False, noteIndex=note
                    )

            if len(_notesToReduce) > 0:
                if showDebug:
                    print(
                        "notes to reduce",
                        _notesToReduce,
                        "next note is clumped with this one",
                        _genericIntervals[min(len(self) - 1, _notesToReduce[0] + 1)]
                        == _genericIntervalsWithCeiling[_notesToReduce[0]],
                    )

            if len(_notesCanReduce) > 0 and showDebug:
                print(
                    "notes that can reduce",
                    _notesCanReduce,
                    "next left side of clump ",
                    _adjustedSelf.getClumps(),
                )
                if len(_notesCanReduce) >= 2:
                    print("there are multiple notes that can reduce")

            # print('length is > 7 and change contains all seven generic intervals!')

        """#Then fix the rest of them (hard ones)

        _clumps = _adjustedSelf.getClumps(returnLeftSide=True)
        for clumpLeft in _clumps:
            #TODO: make sure that this thing extends all the way left

            #the right side of the clump is the index after the left ;)
            _clumpRight = clumpLeft + 1
            #Refresh generic intervals because things may have changed since the last clump
            _genericIntervals = _adjustedSelf.getScaleDegrees()
            _genericIntervalsWithCeiling = _genericIntervals + [_genericIntervals[0]+7]
            _clumps = _adjustedSelf.getClumps(returnLeftSide=True)
            _movableNotes = _adjustedSelf.getBrickWalls(allowedNotes, returnMovableNotesInstead=True)
            _skips = _adjustedSelf.getSkips()
            _leftSkip = None
            _clumpLeft = None
            _needsRefresh = False

            print('clumpleft',clumpLeft)
            # Find the skip to the left of the left clump
            #If there is more than 1 in generic interval between the left of the clump and the one left of that
            #(if this note's stacked up and there's room behind it)
            if _genericIntervals[clumpLeft] - _genericIntervals[clumpLeft - 1] >= 2 \
                    and clumpLeft - 1 in _movableNotes and _genericIntervals[clumpLeft-1] + 1 in _genericIntervalMatrix[clumpLeft-1]:
                #and it's allowed and it's movable
                # Then knock this one down
                _adjustedSelf.notes[clumpLeft-1] = _adjustedSelf.notes[clumpLeft-1].inTermsOfScaleDegree(_genericIntervals[clumpLeft-1]+1)
                _needsRefresh = True
            elif _genericIntervalsWithCeiling[_clumpRight+1] - _genericIntervals[_clumpRight] >= 2\
                and _clumpRight in _movableNotes and _genericIntervals[_clumpRight] + 1 in _genericIntervalMatrix[_clumpRight]:
                _needsRefresh = True
                _adjustedSelf.notes[_clumpRight] = _adjustedSelf.notes[_clumpRight].inTermsOfScaleDegree(
                    _genericIntervalsWithCeiling[_clumpRight] + 1)

            if _needsRefresh:
                # the right side of the clump is the index after the left ;)
                _clumpRight = clumpLeft + 1
                # Refresh generic intervals because things may have changed since the last clump
                _genericIntervals = _adjustedSelf.getScaleDegrees()
                _genericIntervalsWithCeiling = _genericIntervals + [_genericIntervals[0] + 7]
                _clumps = _adjustedSelf.getClumps(returnLeftSide=True)
                _movableNotes = _adjustedSelf.getBrickWalls(allowedNotes, returnMovableNotesInstead=True)
                _skips = _adjustedSelf.getSkips()
                _leftSkip = None
                _clumpLeft = None
                _needsRefresh = False


            for i in range(clumpLeft, 0, -1):
                # If the note can move around, and if it can be lowered in generic interval by 1
                print('rey',_genericIntervals[i],_genericIntervalMatrix[i])
                if _genericIntervals[i] - 1 in _genericIntervalMatrix[i]:
                    print(_genericIntervals[i] - 1,
                          ' in _genericIntervalMatrix[',i,']',str(_genericIntervalMatrix[i]),' grande!- comntinuing clumpleft search')
                else:
                    print(_genericIntervals[i] - 1, ' not in _genericIntervalMatrix[',i,']',str(_genericIntervalMatrix[i]),' bailing on clumpleft search')
                    print('generic intervals',_genericIntervals)
                    break
                # This will find the right side of the left skip
                if i  in _skips:
                    _leftSkip = i + 1
                    break


            if _leftSkip != None:
                #print("_leftSkip != None, it is _leftskip =",_leftSkip,"clump left = ",clumpLeft,'generic',_genericIntervals)
                for i in range(_leftSkip,clumpLeft + 1):
                    #print('within _leftSkip == True i', i, 'adjusted', _adjustedSelf.notes[i], 'to',
                     #     _adjustedSelf.notes[i].inTermsOfScaleDegree(_genericIntervals[i] - 1), 'clumpleft', clumpLeft,
                      #    'generic intervals', _genericIntervals)
                    _adjustedSelf.notes[i] = _adjustedSelf.notes[i].inTermsOfScaleDegree(_genericIntervals[i]-1)



            #Look left
                #If theres a brickwall in the way, abort,
                #If there's no room, abort
                #If there's no skip before it, abort

                #On the other hand, if there is either
                 #a) more than 2 between this and last
                # b) a skip preceeding this
                    #Then do the adjustment
        """
        _adjustedSelf = _adjustedSelf.preferNotes(
            preferSharpFive, preferSharpFour, preferSharpTwo, allowedNotes
        )

        # return the adjusted change
        # print self, generic intervals, brick walls, antibricks, clumps, skips

        if (
            allowedNotes == Change.allowedNoteNamesFiveAccidentals
            and len(self) == 7
            and _adjustedSelf.getScaleDegrees() != [i for i in range(1, 8)]
        ):
            print("\n\n\nshit's bad bro.")
        if showDebug:
            print(
                "print self, generic intervals, brick walls, antibricks, clumps, skips, generic matrix"
            )
            return (
                str(_adjustedSelf),
                _adjustedSelf.getScaleDegrees(),
                _adjustedSelf.getBrickWalls(allowedNotes),
                _adjustedSelf.getBrickWalls(allowedNotes, True),
                _adjustedSelf.getClumps(),
                _adjustedSelf.getSkips(),
                _adjustedSelf.getEnharmonicMatrix(allowedNotes, returnStr=True),
            )
        else:
            if not _adjustedSelf.containingDisallowedNoteNames(allowedNotes):
                Change.cache[cachedName] = _adjustedSelf
                return _adjustedSelf
            else:
                raise ValueError(
                    "Somehow the straightening has fucked up and given notes outside of those allowed",
                    _adjustedSelf,
                    allowedNotes,
                )

    def OLDstraightenNumbers(self, allowedNotes=None, showDebug=True):
        # TODO add part where it sorts in ascending order while keeping track of that sort and reverse sorting at the end
        def getBrickWalls(genericIntervals, genericIntervalsWithCeiling, doLeft=True):
            # Find the walls that are due to there being only one possibility
            _brickWalls = []
            for idx, interval in enumerate(genericIntervals):
                _note = self[idx].inTermsOfScaleDegree(interval)
                # If there is only one spelling for the note (ex. the '5')
                if len(_note.notesWithinNoteNamesAllowed(allowedNotes)) == 1:
                    if True:
                        print(
                            _note.notesWithinNoteNamesAllowed(allowedNotes),
                            "There was only one option",
                        )
                    # Then make that a wall
                    _brickWalls.append(idx)
            # Sort them ascendingly
            genericIntervals = sorted([int(i) for i in genericIntervals])
            # back to str
            genericIntervals = [str(i) for i in genericIntervals]
            if doLeft:
                for x in range(len(genericIntervals)):
                    # Add ones that are due to the scale already being sequential
                    if x + 1 == int(genericIntervals[x]):
                        _brickWalls.append(x)
                    else:
                        break
                    # If the next note has the same interval as this one
                    if genericIntervals[x] == genericIntervalsWithCeiling[x + 1]:
                        _brickWalls.append(x)
                    # print('the scale is sequential to', x, genericIntervals)
            else:  # Do Right
                for x in range(1, len(genericIntervals)):
                    if 8 - x == int(genericIntervals[-x]):

                        _brickWalls.append(len(self) - x)
                    else:
                        break
                    # If the previous note has the same interval as this one
                    if (
                        genericIntervals[-x]
                        == genericIntervals[-(min(1 + x, len(self) - 1))]
                    ):
                        _brickWalls.append(len(self))
                        print(
                            "the scale is backwards sequential to",
                            len(self) - x,
                            genericIntervals,
                        )

            # Now add the first note if it is a 1 (1 ,b1, #1)
            if self[0].inTermsOfScaleDegree(genericIntervals[0]).scaleDegree() == "1":
                _brickWalls.append(0)
                # pass
            return list(set([n for n in sorted(_brickWalls)]))

        if showDebug:
            print(
                "straightening... ",
                self.getChangeNumber(addOneToBookPage=True),
                self,
                self.getScaleNames(),
                "\n",
            )
            if showDebug:
                print("allowed notes = ", allowedNotes)
        _semitoneChecklist = list((False,) * 12)
        _genericIntervals = []
        _clumps = []
        _brickWalls = []
        if allowedNotes == None:
            allowedNotes = Change.allowedNoteNamesJazz
        else:  # allowedNotes was specified
            for i, noteName in enumerate(allowedNotes):
                # check if every note is in allowed notes
                _semitoneChecklist[JazzNote(noteName).semitonesFromOne()] = True
                if type(noteName) == JazzNote:
                    pass
                elif JazzNote.isJazzNoteStr(noteName):
                    pass
                else:
                    # Not a valid note
                    raise TypeError(
                        "allowedNotes should be list or Change and each note is a JazzNote or jazznotestring",
                        allowedNotes[i],
                        type(allowedNotes[i]),
                    )
            # Now check if that set of allowed notes contains all 12 semitone positions
            if False in _semitoneChecklist:
                raise ValueError(
                    allowedNotes,
                    "did not contain all 12 semitone possitions",
                    _semitoneChecklist,
                )
        # Make the list a list of strings which use b and # for accidentals (not unicode)
        allowedNotes = JazzNote.convertUnicodeAccidentalsToSimpleStr(allowedNotes)
        # Make sure the scale contains only allowedNotes to start

        for i, noteName in enumerate(self.notes):
            # if the note name is not within allowed notes

            if noteName.plainStr() in allowedNotes:
                _genericIntervals.append(noteName.scaleDegree())
                if showDebug:
                    print(noteName, " in allowed notes")
            else:  # This note will be adjusted so that it is within allowed notes
                # Find our options for notes
                # Now go through those options and find the closest to the original
                noteOptions = noteName.notesWithinNoteNamesAllowed(allowedNotes)
                if showDebug:
                    print(
                        "note options for the note before filtering:",
                        noteName,
                        noteOptions,
                    )
                # Compare the distance in generic interval for each option
                noteOptions = sorted(
                    noteOptions,
                    key=lambda n: abs(
                        int(JazzNote(n).scaleDegree()) - int(noteName.scaleDegree())
                    ),
                )
                if showDebug:
                    print(
                        "note options for the note after sorting by interval distance:",
                        noteName,
                        noteOptions,
                    )
                # The minimum distance = d

                # Get rid of possibilities that 'cross over' the next interval
                for noteOption in noteOptions:
                    # If the note became larger than the next one over
                    if int(JazzNote(noteOption).scaleDegree()) < int(
                        self[min(len(self) - 1, i - 1)].scaleDegree()
                    ):
                        noteOptions.remove(noteOption)
                        if showDebug:
                            print(
                                noteOption, "was less than the note before and removed!"
                            )
                        pass
                    if int(JazzNote(noteOption).scaleDegree()) > int(
                        self[min(i + 1, len(self) - 1)].scaleDegree()
                    ):
                        noteOptions.remove(noteOption)
                        if showDebug:
                            print(
                                noteOption, "was more than the note after and removed!"
                            )
                # Get rid of any possibilities which are further away in generic interval
                _minD = abs(
                    int(noteOptions[0].scaleDegree()) - int(noteName.scaleDegree())
                )
                noteOptions = filter(
                    lambda n: _minD
                    >= abs(
                        int(JazzNote(n).scaleDegree()) - int(noteName.scaleDegree())
                    ),
                    noteOptions,
                )
                noteOptions = list(noteOptions)
                # noteOptions = list(filter(lambda n: abs(int(JazzNote(n).scaleDegree()) - int(noteName.scaleDegree())),noteOptions))
                if showDebug:
                    print("sorted note options for the note:", noteName, noteOptions)
                # Pick the first one left (only one?)
                _genericIntervals.append(noteOptions[0].scaleDegree())
                # Now the thing has started out using notes that it can use
                if showDebug:
                    print(noteName, "not in allowed notes")
                    # print(self.getChangeNumber(addOneToBookPage=True), self, self.getScaleNames())

        # Add an '8' interval if it was a '1' to help calculate brick walls or octave up from first note (for negatives)
        _genericIntervalsWithCeiling = _genericIntervals + [
            str(int(self[0].scaleDegree()) + 7)
        ]

        # Find the clumps. The list of clumps will be the index of the first value of the clump

        for i in range(1, len(_genericIntervals)):
            # Is this generic interval the same as the next one
            if _genericIntervals[i] == _genericIntervals[i - 1]:
                # Found a clump
                _clumps.append(i - 1)
                """
        #Find the walls that are due to there being only one possibility
        for idx,interval in enumerate(_genericIntervals):
            _note = self[idx].inTermsOfScaleDegree(interval)
            #If there is only one spelling for the note (ex. the '5')
            if len(_note.notesWithinNoteNamesAllowed(allowedNotes)) == 1:
                if showDebug:
                    print(_note.notesWithinNoteNamesAllowed(allowedNotes),'There was only one option')"""

        _brickWalls = getBrickWalls(_genericIntervals, _genericIntervalsWithCeiling)

        for idx, interval in enumerate(_genericIntervals[:]):
            _note = self[idx].inTermsOfScaleDegree(interval)
            print(
                "looking at note",
                _note.inTermsOfScaleDegree(_genericIntervals[idx]),
                '"',
                _note,
            )
            # If there is only one spelling for the note (ex. the '5')
            if len(_note.notesWithinNoteNamesAllowed(allowedNotes)) == 1:
                pass
            else:  # There are options
                # Real quick see if  n - 1 < n < n + 1 (the generic interval is in between its neighbors)
                if showDebug:
                    print(
                        self[idx],
                        "stuffer int(interval) <= int(_genericIntervals[idx-1])",
                        int(_genericIntervals[idx - 1]),
                        int(interval),
                        int(_genericIntervalsWithCeiling[idx + 1]),
                    )

                # search for wall to the left
                _leftBrickWall = _brickWalls[0]

                # Update brickwalls
                _brickWalls = getBrickWalls(
                    _genericIntervals, _genericIntervalsWithCeiling
                )

                for i in _brickWalls:
                    # if i >= _leftBrickWall and i <= idx:
                    if i <= idx:
                        _leftBrickWall = i
                print(
                    "left brick wall is",
                    _leftBrickWall,
                    "because",
                    _genericIntervals,
                    _brickWalls,
                    "i",
                    i,
                )
                print(
                    "at this point the left brick walls are",
                    _brickWalls,
                    "before being updated",
                )

                print(
                    "starting search within this left brick",
                    self[idx].inTermsOfScaleDegree(_genericIntervals[idx]),
                    _brickWalls,
                    _leftBrickWall,
                )
                # search for skip to the left
                _leftSkip = False
                # If the next generic interval is same as this one
                if _genericIntervalsWithCeiling[idx + 1] == _genericIntervals[idx]:
                    _leftCluster = idx
                    # for i in range(idx - 1, _leftBrickWall, -1):
                    for i in range(idx - 1, _leftBrickWall, -1):
                        print(
                            "idx =",
                            idx,
                            self[idx],
                            "n =",
                            _note,
                            "range",
                            list(range(len(self) - idx, 0, -1)),
                            "leftBrickwall",
                            _leftBrickWall,
                        )
                        if i in _brickWalls:
                            _leftSkip = False
                            break
                        # If this note is expressable with as itself -1 generic interval
                        if (
                            self[i]
                            .inTermsOfScaleDegree(str(int(_genericIntervals[i]) - 1))
                            .plainStr()
                            in allowedNotes
                        ):
                            print(
                                "jump in idx",
                                idx,
                                "i",
                                i,
                                _note,
                                self[i].inTermsOfScaleDegree(
                                    str(int(_genericIntervals[i]) - 1)
                                ),
                                "in allowed notes",
                                _genericIntervals,
                            )

                            if (
                                int(_genericIntervals[i])
                                - int(_genericIntervals[i - 1])
                                > 1
                            ):
                                _leftSkip = i

                                print(
                                    "leftSkip = ",
                                    _leftSkip,
                                    "left cluster",
                                    _leftCluster,
                                    "generic",
                                    _genericIntervals,
                                )
                        else:
                            print(
                                "jump right out of finding a skip idx:",
                                idx,
                                "because",
                                self[i]
                                .inTermsOfScaleDegree(
                                    str(int(_genericIntervals[i]) - 1)
                                )
                                .plainStr(),
                                "not in allowedNotes: ",
                                allowedNotes,
                            )
                            print(
                                type(
                                    self[i]
                                    .inTermsOfScaleDegree(
                                        str(int(_genericIntervals[i]) - 1)
                                    )
                                    .plainStr()
                                )
                            )
                            _leftSkip = False
                            _leftSteps = False
                            break

                # King Crimson
                # If  generic intervals under this one lead sequentially to a skip
                # elif _leftSkip != False and all([int(_genericIntervals[idx-n]) <= int(_genericIntervals[idx-n-1]) for n in range()]:
                elif _leftSkip:
                    print(
                        "there is a gap in the code",
                        "generic before",
                        _genericIntervals,
                        end="",
                    )

                    for i in range(_leftSkip, _leftCluster + 1):
                        _genericIntervals[i] = str(int(_genericIntervals[i]) - 1)
                        _genericIntervalsWithCeiling[i] = str(
                            int(_genericIntervals[i]) - 1
                        )
                    print("generics after", _genericIntervals)
                # elif all(_genericIntervals[idx-i] for i in _distanceToSkip)

                # Update brickwalls
                _brickWalls = getBrickWalls(
                    _genericIntervals, _genericIntervalsWithCeiling, doLeft=False
                )
                for i in range(idx, len(self)):
                    # if i >= _leftBrickWall and i <= idx:
                    if i in _brickWalls:
                        _rightBrickWall = i
                if _rightBrickWall:
                    print(
                        "right brick wall is",
                        _rightBrickWall,
                        "because",
                        _genericIntervals,
                        _brickWalls,
                        "i",
                        i,
                    )

                # search for skip to the right
                _rightSkip = False
                _rightCluster = False
                # If the last generic interval is same as this one
                if _genericIntervalsWithCeiling[idx - 1] == _genericIntervals[idx]:
                    _rightCluster = idx
                    # for i in range(idx - 1, _leftBrickWall, -1):
                    for i in range(idx, _rightBrickWall):
                        print(
                            "idx =",
                            idx,
                            self[idx],
                            "n =",
                            _note,
                            "range",
                            list(range(idx, _rightBrickWall)),
                            "rightBrickwall",
                            _rightBrickWall,
                        )
                        if i in _brickWalls:
                            _rightSkip = False
                            break
                        # If this note is expressable with as itself +1 generic interval
                        if (
                            self[i]
                            .inTermsOfScaleDegree(str(int(_genericIntervals[i]) + 1))
                            .plainStr()
                            in allowedNotes
                        ):
                            print(
                                "jump  > in idx",
                                idx,
                                "i",
                                i,
                                _note,
                                self[i].inTermsOfScaleDegree(
                                    str(int(_genericIntervals[i]) + 1)
                                ),
                                "in allowed notes",
                                _genericIntervals,
                            )
                            if (
                                int(_genericIntervals[i + 1])
                                - int(_genericIntervals[i])
                                > 1
                            ):
                                _rightSkip = i
                                print(
                                    "rightSkip = ",
                                    _rightSkip,
                                    "right cluster",
                                    _rightCluster,
                                    "generic",
                                    _genericIntervals,
                                )
                        else:
                            print(
                                "jump right out of finding a skip idx:",
                                idx,
                                "because",
                                self[idx]
                                .inTermsOfScaleDegree(
                                    str(int(_genericIntervals[i]) + 1)
                                )
                                .plainStr(),
                                "not in allowedNotes: ",
                                allowedNotes,
                            )
                            print(
                                type(
                                    self[i]
                                    .inTermsOfScaleDegree(
                                        str(int(_genericIntervals[i]) + 1)
                                    )
                                    .plainStr()
                                )
                            )
                            _leftSkip = False
                            _leftSteps = False
                            break

                _brickWalls = getBrickWalls(
                    _genericIntervals, _genericIntervalsWithCeiling, doLeft=False
                )
                if _rightCluster:
                    # Find the right brick wall - this is the yellow brick road
                    for i in range(_rightCluster, len(self)):
                        if i in _brickWalls:
                            _rightBrickWall = i

                # If this generic interval == the note under it
                if int(_genericIntervals[idx]) <= int(_genericIntervals[idx - 1]):
                    if showDebug:
                        print("equal or less than the note before it")
                    # Is the next note two or more higher in generic interval?
                    if (
                        int(_genericIntervalsWithCeiling[idx + 1])
                        - int(_genericIntervals[idx])
                        >= 2
                    ):
                        # Is the in between note allowed?
                        if (
                            str(
                                self[idx]
                                .inTermsOfScaleDegree(
                                    str(int(_genericIntervals[idx]) + 1)
                                )
                                .plainStr()
                            )
                            in allowedNotes
                        ):
                            _genericIntervals[idx] = str(
                                int(_genericIntervals[idx]) + 1
                            )
                            _genericIntervalsWithCeiling[idx] = str(
                                int(_genericIntervals[idx]) + 1
                            )
                            if showDebug:
                                print("raised", self[idx], " by 1")

                # If there is a skip to the right
                elif _rightSkip:
                    for i in range(_rightCluster, _rightSkip):
                        print("right cluster", _rightCluster, "right skip", _rightSkip)
                        _genericIntervals[i] = str(int(_genericIntervals[i]) + 1)
                        _genericIntervalsWithCeiling[i] = str(
                            int(_genericIntervals[i]) + 1
                        )

                # If a number in between is an option, use it

                """# If this generic interval == the note above it
                if int(_genericIntervals[idx]) >= int(_genericIntervalsWithCeiling[idx+1]):
                    if showDebug: print('equal or more than the note after it')
                    # Is the previous note two or more lower in generic interval?
                    if int(_genericIntervals[idx]) - int(_genericIntervalsWithCeiling[max(idx - 1,0)]) > 1:
                        if True:
                            print('previous note two or more lower',str(self[idx].inTermsOfScaleDegree(str(max(1,int(interval) - 1)))),)
                        # Is the in between note allowed?
                        if str(self[idx].inTermsOfScaleDegree(str(max(1,int(interval) - 1))).plainStr()) in allowedNotes:
                            print('now the note has been lowered',str(self[idx].inTermsOfScaleDegree(str(max(1,int(interval) - 1)))))
                            _genericIntervals[idx] = str(int(_genericIntervals[idx]) - 1)
                            _genericIntervalsWithCeiling[idx] = str(int(_genericIntervals[idx]) - 1)
                            if showDebug: print('lowered', self[idx], ' by 1')"""

                # If this generic interval == the note above it
                """if int(_genericIntervals[idx]) >= int(_genericIntervalsWithCeiling[idx + 1]):
                    if showDebug: print('equal or more than the note after it')
                    # Is the previous note two or more lower in generic interval?
                    if int(_genericIntervals[idx]) - int(_genericIntervalsWithCeiling[max(idx - 1, 0)]) > 1:
                        if True:
                            print('previous note two or more lower',
                                  str(self[idx].inTermsOfScaleDegree(str(max(1, int(interval) - 1)))), )
                        # Is the above note augmented note allowed?
                        if str(self[idx + 1].inTermsOfScaleDegree(
                                str(max(1, int(_genericIntervalsWithCeiling[idx+1]) - +))).plainStr()) in allowedNotes:
                            print('now the note has been lowered',
                                  str(self[idx].inTermsOfScaleDegree(str(max(1, int(interval) - 1)))))
                            _genericIntervals[idx] = str(int(_genericIntervals[idx]) - 1)
                            _genericIntervalsWithCeiling[idx] = str(int(_genericIntervals[idx]) - 1)
                            if showDebug: print('lowered', self[idx], ' by 1')"""

                if showDebug:
                    print(
                        _note.notesWithinNoteNamesAllowed(allowedNotes),
                        "There was multiple options",
                    )
        # For every clump find the brick wall (a direction that cannot be passed through)
        for clump in _clumps:
            # Find the left wall
            pass
            # Find the right wall

        if showDebug:
            print(_clumps, "are where clumps start")
            print(
                _brickWalls,
                " are where brickwalls are",
                _genericIntervals,
                " are teh generic intervals ",
                self.getChangeNumber(addOneToBookPage=True),
                self,
                self.getScaleNames(),
            )

        for i in range(len(_genericIntervals)):
            if _genericIntervals[i]:
                pass

        if (
            allowedNotes == Change.allowedNoteNamesFiveAccidentals
            and len(self) == 7
            and _genericIntervals != [str(i) for i in range(1, 8)]
        ):
            print("\n\n\nshit's bad bro.")
        else:
            print("things are well")
        return Change(
            [
                self[n].inTermsOfScaleDegree(_genericIntervals[n])
                for n in range(len(self))
            ]
        )

    def str8ghtenOutNumbers(self, allowedNotes=None, showDebug=False):
        if len(self.notes) in (0, 1):
            return self

        if allowedNotes == None:
            allowedNotes = Change(Change.allowedNoteNamesJazz)
        else:
            allowedNotes = Change(allowedNotes)
        _changeLength = len(self.notes)

        _newNotes = []
        # remove notes that are not allowed
        _notesWithoutBannedNotes = []
        for note in self.notes:
            if note in [
                item
                for item in allowedNotes.notes
                if item in Change.allowedNoteNamesSimpleJazz
            ]:
                _notesWithoutBannedNotes.append(note)
            else:
                # print('fudge sundae',note,note.notesWithinNoteNamesAllowed(allowedNotes), allowedNotes)
                # If you want a different name use another index

                _notesWithoutBannedNotes.append(
                    note.notesWithinNoteNamesAllowed(
                        [
                            item
                            for item in allowedNotes.notes
                            if item not in Change.allowedNoteNamesWeird
                        ]
                    )[0]
                )
                # _notesWithoutBannedNotes.append(note.notesWithinNoteNamesAllowed(allowedNotes.withoutNotes(Change.allowedNoteNamesWeird))[0])
        _notesWithoutBannedNotes = Change(_notesWithoutBannedNotes)

        _thisNumber = int(_notesWithoutBannedNotes.notes[0].scaleDegree())
        _previousNumber = int(_notesWithoutBannedNotes.notes[0].scaleDegree())
        _nextNumber = int(
            _notesWithoutBannedNotes.notes[min(1, _changeLength - 1)].scaleDegree()
        )
        for noteIndex in range(len(_notesWithoutBannedNotes.notes)):
            # If not the first note
            if noteIndex != 0:
                if _lastAdjustedNumber:
                    _previousNumber = _lastAdjustedNumber
                else:
                    _previousNumber = int(
                        _notesWithoutBannedNotes.notes[noteIndex - 1].scaleDegree()
                    )
            # print('it happened', noteIndex, _changeLength)
            _thisNumber = int(_notesWithoutBannedNotes.notes[noteIndex].scaleDegree())
            if noteIndex != _changeLength - 1:
                _nextNumber = int(
                    _notesWithoutBannedNotes.notes[noteIndex + 1].scaleDegree()
                )

            else:

                _nextNumber = 8
                # print('fuck sake',noteIndex)

            _lastAdjustedNumber = False
            if showDebug:
                print(
                    "pn",
                    _previousNumber,
                    "tn",
                    _thisNumber,
                    "nn",
                    _nextNumber,
                    end="   ",
                )
            if (
                (_previousNumber <= _thisNumber - 2)
                or (_nextNumber >= _thisNumber + 2)
                or (noteIndex == len(self.notes) - 1)
                or True
            ):

                # if (_thisNumber == _nextNumber and _previousNumber <= _thisNumber-2) or (_thisNumber == _previousNumber and _nextNumber >= _thisNumber+2):
                _usingAdjustedNumber = False
                # 				if _thisNumber == _nextNumber and _previousNumber <= _thisNumber-2:
                # if _previousNumber <= _thisNumber-2 and _nextNumber - _thisNumber > _thisNumber - _lastAdjustedNumber:
                # if _previousNumber <= _thisNumber - 2:

                # Give a step down if there is a cluster above
                for i in range(noteIndex + 1, len(self)):
                    if (
                        _notesWithoutBannedNotes.notes[i].scaleDegree()
                        == _notesWithoutBannedNotes.notes[i - 1].scaleDegree()
                    ):
                        _thisNumber -= 1
                        if showDebug:
                            print("-1cluster ", end="")
                        break

                if _nextNumber >= _thisNumber + 2 and _thisNumber - _previousNumber < 1:
                    # elif _nextNumber >= _thisNumber + 2:
                    _thisNumber += 1
                    if showDebug:
                        print("raised her ", end="")

                elif (
                    _thisNumber - _previousNumber >= 1 and _nextNumber - _thisNumber < 1
                ):
                    _thisNumber -= 1
                    if showDebug:
                        print("lowered her ", end="")

                # 				elif _thisNumber == _previousNumber and _nextNumber >= _thisNumber+2:

                if noteIndex + 1 == len(self.notes):

                    if _newNotes:
                        if int(_newNotes[noteIndex - 1].scaleDegree()) == _thisNumber:
                            _thisNumber += 1
                            if showDebug:
                                print("brought her up 1", end="")
                    else:
                        if (
                            int(
                                _notesWithoutBannedNotes.notes[
                                    noteIndex - 1
                                ].scaleDegree()
                            )
                            == _thisNumber
                        ):
                            _thisNumber += 1
                            if showDebug:
                                print("brought her up (1)", end="")
                    # Give a step down if it is the highest note and can smoosh back in, downwards
                    if (
                        _previousNumber + 1 < _thisNumber
                        and (
                            _notesWithoutBannedNotes.notes[
                                noteIndex
                            ].inTermsOfScaleDegree(JazzNote(str(_thisNumber - 1)))
                        )
                        in allowedNotes.notes
                    ):
                        _thisNumber -= 1

                        if showDebug:
                            print("it happened - 1")
                        # input()

                # print("mah",noteIndex,self.notes)
                _potentialNoteName = _notesWithoutBannedNotes.notes[
                    noteIndex
                ].inTermsOfScaleDegree(JazzNote(str(_thisNumber)))

                # print("stuff",repr(_potentialNoteName), allowedNotes.notes)
                for i in allowedNotes:
                    if str(i) == str(_potentialNoteName):
                        # print('success',i,_potentialNoteName)
                        _usingAdjustedNumber = True
                        _newNotes.append(_potentialNoteName)
                        _lastAdjustedNumber = int(_potentialNoteName.scaleDegree())
                        break

                # Next line mostly worked
                # if repr(_potentialNoteName) in allowedNotes.notes:#fuck
                if (
                    repr(_potentialNoteName) in Change.allowedNoteNamesSimpleJazz
                ):  # fuck
                    # print('shit good _potentialNoteName in allowedNotes. booya', _potentialNoteName,allowedNotes.notes)
                    _newNotes.append(_potentialNoteName)

                elif repr(_potentialNoteName) in allowedNotes.notes:
                    _newNotes.append(_potentialNoteName)

                if not _usingAdjustedNumber:
                    # print('shit bad _potentialNoteName',_potentialNoteName,'not in _allowedNotes', allowedNotes.notes)
                    _newNotes.append(_notesWithoutBannedNotes.notes[noteIndex])

            else:
                _newNotes.append(_notesWithoutBannedNotes.notes[noteIndex])

            # print('this',_thisNumber,'next',_nextNumber, 'previous', _previousNumber)
            if int(self.notes[noteIndex].scaleDegree()):
                pass
            if showDebug:
                print("note", noteIndex + 1)
        # 	if Change(_newNotes) != Change(_newNotes).straightenDegrees(allowedNotes=allowedNotes):
        # 		return Change(_newNotes).straightenDegrees(allowedNotes=allowedNotes)
        # Something about doing it again
        return Change(_newNotes)

    def getDistinctChordTypes(
        self,
        removeChordsWithOneLessLength=True,
        includeModesForDiads=False,
        showDebug=False,
    ):
        _l = len(self)
        _types = []
        if _l == 0:
            _types = []
        if _l in (1, 2):
            if includeModesForDiads:
                _types = ["quartal Diad"]
        elif _l == 3:
            # This will be gone if removeChordsWithOneLessLength==True
            _types = ["triadic Diad"]
        elif _l == 4:
            _types = ["triadic Diad", "quartal Diad"]
            if not removeChordsWithOneLessLength:
                _types.append("quartal 7th")
        elif _l == 5:
            _types = ["triadic Triad", "quartal Triad"]
            if not removeChordsWithOneLessLength:
                _types += ["triadic 7th", "quartal 7th"]
        elif _l == 6:
            _types = ["triadic Triad", "quartal Diad"]
        elif _l == 8:
            _types = ["triadic 7th", "quartal 7th"]
        elif _l in (7, 9, 10, 11, 12):
            _types = ["triadic 7th", "triadic Triad", "triadic 9th"]

        if showDebug:
            print(self, Chord.chordIndexes(len(self)), sep=" ")
        return _types
        # return Chord.getChordTypesForLength(len(self),maxChordTypes)
        # return Chord.validTypesByLength[len(self)]

    @classmethod
    def makeDistinctChordStrPrintable(
        cls, chordStr: str, change: Change, useSpaceAfterSymbol=False, removeStrs=[]
    ) -> str:
        _numberPartOfDistinctChord = int(chordStr[-1])
        if useSpaceAfterSymbol:
            _spaceStr = " "
        else:
            _spaceStr = ""
        chordStr = chordStr.replace(
            "Distinct Chord",
            change.getDistinctChordTypes()[_numberPartOfDistinctChord - 1],
        )
        chordStr = chordStr.replace(
            "quartal ", Unicode.chars["Quartal Chord"] + _spaceStr
        )
        chordStr = chordStr.replace(
            "triadic ", Unicode.chars["Triadic Chord"] + _spaceStr
        )
        chordStr = (
            chordStr.replace("1", "").replace("2", "").replace("3", "").replace("4", "")
        )
        for removeStr in removeStrs:
            chordStr = chordStr.replace(removeStr, "")

        chordStr = chordStr.replace(" Word", Unicode.chars["Word"])
        return chordStr

    def getDistinctScaleChord(
        self,
        rootIndex=0,
        chordTypeNumber: int = 0,
        normaliseResult=True,
        removeChordsWithOneLessLength=False,
        includeModesForDiads=False,
        returnChordQuality=True,
        useHalfDiminishedChords=None,
        makeTextMulticoloured=False,
        rootKey="C",
    ):
        from Chord import Chord
        _chordTypes = self.getDistinctChordTypes(
            removeChordsWithOneLessLength=removeChordsWithOneLessLength,
            includeModesForDiads=includeModesForDiads,
        )
        if chordTypeNumber < len(_chordTypes):

            if normaliseResult == True:
                _chordIndexes = Chord.chordIndexes(
                    len(self), 0, chordType=_chordTypes[chordTypeNumber]
                )
                _chordNotes = Change(
                    [self.mode(rootIndex).notes[i] for i in _chordIndexes]
                )
                _chordNotes = _chordNotes.getNormalForm()
            else:

                _chordIndexes = Chord.chordIndexes(
                    len(self), rootIndex, chordType=_chordTypes[chordTypeNumber]
                )
                try:
                    _chordNotes = Change([self.notes[i] for i in _chordIndexes])
                except:
                    input("holy hannah {} {}".format(self, _chordIndexes))
                # print('{} {}'.format(_chordIndexes, _chordNotes))
            # input(Utility.printPrettyVars(_chordNotes,normaliseResult))
            if returnChordQuality == True:
                # input(Key(rootKey,self[rootIndex]).getASCII())
                return _chordNotes.getChordQuality(
                    useHalfDiminishedChords=useHalfDiminishedChords,
                    makeTextMulticoloured=makeTextMulticoloured,
                    rootKey=Key(rootKey, self[rootIndex]).inAllFlats().getASCII(),
                )
            else:
                if isinstance(_chordNotes, Change):
                    return _chordNotes
                else:
                    raise TypeError("adsfgaasadf")
        else:
            # return 'None'
            # raise ValueError(str(self) +' does not have this many ({}) types of distinct chords, as it has {} notes.'.format(len(self.getDistinctChordTypes()),len(self)))
            return Change([])

    def getNoteNameMatrixOfKey(self, alphabetKey: str, maxAccidentals: int):
        if JazzNote.isAlphabetNoteStr(alphabetKey):
            pass
        else:
            raise ValueError(
                "expecing alphabetKey == some sort of alphabet note string, instead got:",
                alphabetKey,
            )
        if maxAccidentals < 1:
            raise ValueError(
                "It would be tough to describe a key with less than 1 accidental.",
                numberOfAccidentals,
            )

        _nameMatrix = []
        # TODO: right now it's not even looking at the alphabet notes, just the jazz numbers
        for i, n in enumerate(self.notes):
            _nameMatrix.append([])
            _alphabetNote = n.byWay(alphabetKey)
            _numberOfAccidentals = len(n.leaveAccidentals())
            _accidentals = n.leaveAccidentals()
            if _numberOfAccidentals <= maxAccidentals:
                _nameMatrix[i].append(n.note)
                # Then try the one aways
            # Going from the note to the end of the notes
            if "b" in _accidentals or "♭" in _accidentals:
                while _numberOfAccidentals > maxAccidentals:
                    _diminishedNote = n.inTermsOfScaleDegree(
                        str((int(n.scaleDegree()) - 1) % 8)
                    )
                    _accidentals = _diminishedNote.leaveAccidentals()
                    _numberOfAccidentals = len(n.leaveAccidentals())
                    if _numberOfAccidentals <= maxAccidentals:
                        _nameMatrix[i].append(_diminishedNote.note)
                    # We have crossed over
                    if (
                        "#" in _accidentals or "♯" in _accidentals
                    ) and _numberOfAccidentals > maxAccidentals:
                        break

            _accidentals = n.leaveAccidentals()
            if "#" in _accidentals or "♯" in _accidentals:
                while _numberOfAccidentals > maxAccidentals:
                    _augmentedNote = n.inTermsOfScaleDegree(
                        str((int(n.scaleDegree()) + 1) % 8)
                    )
                    _accidentals = _augmentedNote.leaveAccidentals()
                    _numberOfAccidentals = len(n.leaveAccidentals())
                    if _numberOfAccidentals <= maxAccidentals:
                        _nameMatrix[i].append(_augmentedNote.note)
                    # We have crossed over
                    if (
                        "b" in _accidentals
                        or "♭" in _accidentals
                        and _numberOfAccidentals > maxAccidentals
                    ):
                        break
        return _nameMatrix

    def getPositionsOfWay(self, way):
        if way in Book.tabularWays and not way in Book.specificPositionalWays:
            return self.getSemitones()
        elif way in Book.specificPositionalWays:
            if way == "Remove Note":
                return self.getSemitones()
            elif way == "Add Note":
                return self.getInverse().getSemitones()
            elif "Changed Note" in way:
                return [i for i in range(12)]
            else:
                raise ValueError(
                    way
                    + " in Book.specificPositionalWays, but does not have its positions defined."
                )

    def makePdfLink(self, linkCode="cbw",sep=" | "):
        'the linkCode lets you link to this with \hyperref[linkCode]{Click text}'
        def _scaleNameFunc(change:Change) -> str:
            _names = change.getScaleNames(
                defaultWay=False,
                searchForDownward=False,
                searchForNegative=False,
                includeDownwardHexagram=False,
                rebindRootToNextNoteIfNoOne=True,
                replaceCarnaticNamesWithSymbols=False,
                replaceDirectionStrWithUnicode=False,
            )
            if len(_names) > 0:
                _scaleName = _names[0]
            else:
                _scaleName = " ".join(self.getHexagram(["name"]))
            return _scaleName

        _scaleName = _scaleNameFunc(change=self)
        _str = "\\belowpdfbookmark{"
        if linkCode == 'cbw':
            indexNumber = str(
                self.getChangeNumber()
            )
            #_str += "\\phantomsection"
            _str += "Change " + indexNumber + sep + "".join(self.byWays("Word")) + sep
            _str += _scaleName
        elif linkCode in ('mf','modefamilty'):
            indexNumber = ''.join([c for c in str(self.byWays(['Unique Change Number'])) if c.isdigit() ])
            #print('yo',self.byWays(['Unique Change Number']),self.getUniquePage())
            #input(indexNumber)
            _str += "Mode Family " + indexNumber + sep
            for n in range(len(self)):
                _mode = self.mode(n)
                _modeName = _scaleNameFunc(change=_mode)
                _str += _modeName
                if n != (len(self) - 1):
                    _str += sep
        _str += "}{" + linkCode + "_" + str(indexNumber) + "}"
        if linkCode== 'mf':pass#input('asdfasd {}'.format(_str))
        return _str


    def byWays(self, ways, useTextStyledByWay=False,colourResult=False):
        funcSignature = '{}.byWays(ways={},useTextStyledByWay={},colourResult={})'.format(
            self,ways,useTextStyledByWay,colourResult)
        try:
            return Change.cache[funcSignature]
        except KeyError:
            pass
        if Latex.makeTextColoured == False:
            colourResult = False
        if not type(ways) == list:
            ways = [ways]
        _byWays = []
        for way in ways:
            _notesByWay = []

            if Change.isValidWay(way):  # Is a way of note set
                if 'Hexagram' in way:
                    from Hexagram import Hexagram
                elif 'Tetragram' in way:
                    from Tetragram import Tetragram



                if way == "Area":
                    _notesByWay = str(round(self.getArea(), 3))[0:5]
                elif way == 'Enantiomorph':
                    _notesByWay = self.getEnantiomorph()
                elif way == "Unique Chapter Change Number":
                    #TODO Remove the dependancy on Book
                    from Book import Book
                    try:
                        Change.theBook.sequencePrimes[0]
                    except Exception:
                        print('making another Book()')
                        Change.makePrimes = 1
                        Change.theBook = Book()
                    try:
                        _notesByWay = str(len(self)) + "-"+ str(1 + Change.theBook.sequencePrimesByLength[len(self)].index(self.forceChangeIntoAllowedNotes(allowedNotes=Change.allowedNoteNamesAllFlats).getPrimeForm()))
                    except ValueError as e:
                        input("a):\n{}:\n{}\n{}".format(
                            e, Change.theBook.sequencePrimesByLength[len(self)], self.forceChangeIntoAllowedNotes(allowedNotes=Change.allowedNoteNamesAllFlats).getPrimeForm()))

                elif way == "Ring Number":
                    _notesByWay = self.getRingNumber()
                elif way == "Change Number":
                    _notesByWay = self.getChangeNumber(
                        returnChapterPage=False,
                        decorateChapter=True,
                        addOneToBookPage=True,
                        includeChapterSymbol=False,
                        imgTag="tabbingimg",
                        decorateWithSmallCircle=Latex.useSmallCircles,
                        useTextStyledByWay=useTextStyledByWay,

                    )
                elif way == "Bitmap":
                    _notesByWay = self.getBitMap(colourResult=colourResult)
                elif way == "Spectra":
                    _notesByWay = [[0]] + self.getSpectraVariation(
                        returnDistributionSpectra=True, sortSpectraByOccurences=True
                    )
                    for n in range(len(_notesByWay)):
                        _notesByWay[n] = ",".join([str(i) for i in _notesByWay[n]])
                    if False:
                        for g in range(len(_notesByWay)):
                            _notesByWay[g] = [
                                str(JazzNote.makeFromSet(s, g + 1))
                                for s in _notesByWay[g]
                            ]
                            # input('here')
                            _notesByWay[g] = " ".join(_notesByWay[g])
                elif way == "Step":
                    _notesByWay = self.getSemitoneSteps()
                elif way == "Prime":
                    _notesByWay = self.getPrimeForm()
                elif way == "Forte Number":
                    _notesByWay = self.getForteNumber()
                elif way == "Mode Semitones":
                    for note in self.notes:
                        #_notesByWay.append(self.modeInSemitones(self.notes.index(note)))
                        _notesByWay.append(self.modeInSemitones(np.where(self.notes==note)[0][0]))
                elif way == "Mode Word":
                    for n, note in enumerate(self.notes):
                        _notesByWay.append(self.mode(n).getWord(useTextStyledByWay=useTextStyledByWay))
                        if colourResult:
                            _notesByWay[-1] = Latex.makeDataColoured(
                                results=_notesByWay[-1],
                                colours=note.semitonesFromOne() + Book.colourTranspose,
                            )
                elif way == "Mode Jazz":
                    for note in range(len(self.notes)):
                        _notesByWay.append(self.mode(note).straightenDegrees())
                        
                        if colourResult:
                            # raise ValueError('finally got here')
                            _thisMode = _notesByWay[-1]
                            _colours = [
                                i
                                + Book.colourTranspose
                                + self.notes[note].semitonesFromOne()
                                for i in _thisMode.getSemitones()
                            ]
                            _notesByWay[-1] = [str(i) for i in _thisMode.notes]
                            _notesByWay[-1] = Latex.makeDataColoured(
                                results=_notesByWay[-1], colours=_colours
                            )
                            _notesByWay[-1] = " ".join(_notesByWay[-1])
                            # input('they are now '+ _notesByWay[-1])
                            # makeTextColoured = self.notes[note].semitonesFromOne()+Book.colourTranspose
                elif way == "Mode Change Number":
                    if Latex.useSmallCirclesMultiColourSchemes:
                        _notesByWay = [
                            self.mode(i).getChangeNumber(
                                decorateChapter=True,
                                decorateWithSmallCircle=Latex.useSmallCircles,
                                addOneToBookPage=True,  # This won't quite work with negatives
                                key=Latex.getTransposedColourKey(
                                    self.notes[i].semitonesFromOne()
                                ),
                                useTextStyledByWay=useTextStyledByWay,
                            )
                            for i in range(len(self.notes))
                        ]
                    else:
                        _notesByWay = [
                            self.mode(i).getChangeNumber(
                                decorateChapter=True,
                                decorateWithSmallCircle=Latex.useSmallCircles,
                                addOneToBookPage=True,
                                colourKey=None,
                                useTextStyledByWay= useTextStyledByWay
                            )
                            for i in range(len(self.notes))
                        ]

                elif way == "Mode Name":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            self.mode(note).getScaleNames(
                                searchForDownward=False,
                                searchForNegative=False,
                                includeDownwardHexagram=False,
                            )[0]
                        )
                        if colourResult:
                            _notesByWay[-1] = Latex.makeDataColoured(
                                results=_notesByWay[-1],
                                colours=self.notes[note].semitonesFromOne()
                                + Book.colourTranspose,
                            )
                elif way == "Mode Quality":
                    for note in range(len(self.notes)):
                        _notesByWay.append(self.mode(note).getChordQuality())
                elif (
                    way == "Mode Hexagram"
                ):  # This is fucking up by sometimes repeating the first answer
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            self.mode(note).getHexagramSymbols(
                                insertSpaceBetweenHexagrams=False
                            )
                        )
                        if Latex.on and colourResult == True:
                            _notesByWay[-1] = Latex.makeDataColoured(
                                _notesByWay[-1],
                                colours=[
                                    self.notes[note].semitonesFromOne()
                                    + Book.colourTranspose,
                                    self.notes[note].semitonesFromOne()
                                    + Book.colourTranspose
                                    + 6,
                                ],
                            )
                        _notesByWay[-1] = "".join(_notesByWay[-1])
                elif way == "Mode Primeness":
                    for note in range(len(self.notes)):
                        _notesByWay.append(self.mode(note).getPrimeness(decorate=True))
                    if colourResult:
                        _notesByWay[-1] = Latex.makeDataColoured(
                            results=_notesByWay[-1],
                            colours=self.notes[note].semitonesFromOne()
                            + Book.colourTranspose,
                        )
                elif way == "Raga":
                    _notesByWay = self.getContainedRagasOtherDirections(
                        returnNames=True, returnIndexes=True
                    )
                elif way == "Reverse":
                    _notesByWay = self.getReverse()
                elif way == "Inverse":
                    _notesByWay = self.getInverse()
                elif way == "Tritone Sub":
                    _notesByWay = self.getTritoneSub().straightenDegrees()
                elif way == "Tritone Sub Page":
                    _notesByWay = self.getTritoneSub().getChangeNumber(
                        addOneToBookPage=True, decorateWithSmallCircle=True,
                        useTextStyledByWay=True
                        
                    )
                elif "Info" in way:
                    # Animals '🐍' '🐊'  '🐉' '🐓' '🐌' '🐒''🐙''🐚' '🐘''🐁''🐀' 🐛 🐜 🐞 🐟 🐠 🐡
                    # ⟳
                    infoWays = Change.infoWaySymbols
                    if "Condensed" in way:
                        infoWays = Change.condensedInfoWays
                    for infoWay in infoWays.keys():
                        if (
                            infoWay != "Contains Self"
                            or self.byWays("Contains Self") != 1
                        ):
                            # if (infoWay != 'Is Palindrome' or self.byWays('Is Palindrome') == True):
                            if (
                                not infoWay in Change.binaryWays
                                or self.byWays(infoWay) != False
                            ):
                                if (
                                    infoWay in Change.binaryWays
                                    and self.byWays(infoWay) == True
                                ):
                                    _notesByWay.append(Change.infoWaySymbols[infoWay])
                                elif infoWay in Change.binaryWays and self.byWays(
                                    infoWay
                                ) not in (True, False):
                                    _notesByWay.append(
                                        Change.infoWaySymbols[infoWay]
                                        + ""
                                        + str(self.byWays(infoWay))
                                    )
                                else:
                                    _notesByWay.append(
                                        Change.infoWaySymbols[infoWay]
                                        + ""
                                        + str(self.byWays(infoWay))
                                    )
                                if infoWay in Change.infoWaysToOmit:
                                    _notesByWay = _notesByWay[:-1]


                elif way == "Moment":
                    _notesByWay = self.getTimeOfDay()
                elif way == "Has Coherence":  # Info
                    _notesByWay = self.getCoherence()
                elif way == "Deepness":  # Amount Of Deepness
                    _notesByWay = self.getDeepness()
                elif way == "Is Deep":
                    _notesByWay = self.getDeepness(True)
                elif way == "Binomial":
                    _notesByWay = self.getBinomial()
                elif way == "Interval Vector":
                    _notesByWay = self.getIntervalVector(convert10ToT=True)
                elif way == "Variation":
                    _notesByWay = self.getSpectralVariation()
                elif way == "Has Myhill":  # Info
                    _notesByWay = self.getSpectraVariation(returnMyhillProperty=True)
                elif way == "Has Evenness":  # Info
                    _notesByWay = str(self.getSpectralVariation()) == "0"
                elif way == "Imperfections":  # info
                    _notesByWay = self.getImperfections()
                elif way == "Cohemitonia":
                    _notesByWay = self.getCohemitonia()
                elif way == "Hemitonia":
                    _notesByWay = self.getSemitoneSteps().count(1)
                elif way == "Tritonia":
                    _notesByWay = self.getSemitoneSteps().count(6)
                elif way == "Heliotonia":
                    _notesByWay = self.getHeliotonia()
                elif way == "Alpha Accidentals":
                    _notesByWay = self.getAccidentals()
                elif way == "Is Chiral":
                    _notesByWay = self.getChirality()
                elif way == "Is Achiral":
                    _notesByWay = self.getChirality(reverseAnswer=True)
                elif way == "Is Prime":
                    _notesByWay = self.getPrimeForm(returnTrueIfPrime=True)
                elif way == "Primeness":
                    _notesByWay = self.getPrimeness()
                elif way == "Add Note":
                    for note in self.getInverse().notes:
                        # print('where in the world',self.withAddedNotes(str(note)))
                        _s = self.withAddedNotes(note)
                        _notesByWay.append(_s.getScaleNames()[0])
                    if colourResult:
                        _notesByWay = Latex.makeDataColoured(
                            _notesByWay,
                            [
                                i + Book.colourTranspose
                                for i in self.getInverse().getSemitones()
                            ],
                        )
                elif way == "Remove Note":
                    for note in range(len(self.notes)):
                        # input('shit'+str(self)+'  '+str(self.withoutNote(self.notes[note])))
                        _s: Change = self.withoutNote(self.notes[note])
                        _notesByWay.append(_s.getScaleNames()[0])
                    if colourResult:
                        _notesByWay = Latex.makeDataColoured(
                            _notesByWay, [i + Book.colourTranspose for i in range(12)]
                        )
                elif way == "Changed Note":
                    _notesByWay = [self.getChangedNote(i) for i in range(12)]
                    if colourResult:
                        _notesByWay = Latex.makeDataColoured(
                            _notesByWay, [i + Book.colourTranspose for i in range(12)]
                        )
                elif way == "Changed Note Word":
                    _notesByWay = [self.getChangedNote(i).getWord() for i in range(12)]
                    if colourResult:
                        _notesByWay = Latex.makeDataColoured(
                            _notesByWay, [i + Book.colourTranspose for i in range(12)]
                        )
                elif way == "Changed Note Page":
                    _notesByWay = [
                        self.getChangedNote(i).getChangeNumber(
                            addOneToBookPage=True,
                            decorateWithSmallCircle=Latex.useSmallCircles,
                        )
                        for i in range(12)
                    ]
                    if colourResult:
                        _notesByWay = Latex.makeDataColoured(
                            _notesByWay, [i + Book.colourTranspose for i in range(12)]
                        )
                elif way == "Changed Note Hexagram":
                    _notesByWay = [
                        "".join(self.getChangedNote(i).getHexagram()) for i in range(12)
                    ]
                    if colourResult:
                        _notesByWay = Latex.makeDataColoured(
                            _notesByWay, [i + Book.colourTranspose for i in range(12)]
                        )
                elif way == "Changed Note Info":
                    _notesByWay = [
                        self.getChangedNote(i).getHexagram()
                        + " "
                        + self.getChangedNote(i).getChangeNumber(addOneToBookPage=True)
                        for i in range(12)
                    ]
                    if colourResult:
                        _notesByWay = Latex.makeDataColoured(
                            _notesByWay, [i + Book.colourTranspose for i in range(12)]
                        )
                elif way == "Greatest Interval":  # info
                    if len(self) == 0:
                        return 0
                    _notesByWay = max([int(i) for i in self.byWays("Step")])
                elif way == "Smallest Interval":  # info
                    if len(self) == 0:
                        return 0
                    _notesByWay = min([int(i) for i in self.byWays("Step")])
                elif way == "Contains Self":  # info
                    _repititions = 0
                    for note in range(len(self.notes)):
                        if self.mode(note).byWays("Set") == self.byWays("Set"):
                            _repititions += 1
                    _notesByWay = _repititions
                elif way == "Is Palindrome":
                    if self.containsNotes("1"):
                        _notesByWay = (
                            self.getSemitoneSteps() == self.getSemitoneSteps()[::-1]
                        )
                    else:  # negative subChange
                        _notesByWay = (
                            self.getSemitoneSteps() == self.getSemitoneSteps()[::-1]
                        )
                elif "Distinct Chord Change Number" in way:
                    # Finish normalised option
                    _numPartOfDistinctChord = int(way[-1])

                    if not len(self.getDistinctChordTypes()) >= _numPartOfDistinctChord:
                        _notesByWay = []
                        continue
                    _numPartOfDistinctChord -= 1
                    if Latex.useSmallCirclesMultiColourSchemes:

                        for n in range(len(self.notes)):
                            if (
                                len(self.getDistinctChordTypes())
                                >= _numPartOfDistinctChord
                            ):
                                _notesByWay.append(
                                    self.getDistinctScaleChord(
                                        n,
                                        _numPartOfDistinctChord,
                                        returnChordQuality=False,
                                    ).getChangeNumber(
                                        addOneToBookPage=True,
                                        decorateWithSmallCircle=Latex.useSmallCircles,
                                        key=Latex.getTransposedColourKey(
                                            self.notes[n].semitonesFromOne()
                                        ),
                                    )
                                )
                    else:
                        for n in range(len(self.notes)):
                            _notesByWay.append(
                                self.getDistinctScaleChord(
                                    n, _numPartOfDistinctChord, returnChordQuality=False
                                ).getChangeNumber(
                                    addOneToBookPage=True,
                                    decorateWithSmallCircle=Latex.useSmallCircles,
                                )
                            )
                elif "Distinct Chord Word" in way:
                    _numPartOfDistinctChord = int(way[-1])
                    _numPartOfDistinctChord -= 1
                    for n in range(len(self.notes)):
                        _notesByWay.append(
                            self.getDistinctScaleChord(
                                n, _numPartOfDistinctChord, returnChordQuality=False
                            ).getWord(
                                specificInterval=self.notes[n].semitonesFromOne(),
                                colourResult=colourResult,
                            )
                        )
                elif "Distinct Chord Normalised Change Number" in way:
                    _numPartOfDistinctChord = int(way[-1])
                    _numPartOfDistinctChord -= 1
                    for n in range(len(self.notes)):
                        _notesByWay.append(
                            self.getDistinctScaleChord(
                                n, _numPartOfDistinctChord, returnChordQuality=False
                            ).getChangeNumber()
                        )
                elif "Distinct Chord Change Number" in way:
                    _numPartOfDistinctChord = int(way[-1])
                    _numPartOfDistinctChord -= 1
                    for n in range(len(self.notes)):
                        _notesByWay.append(
                            self.getDistinctScaleChord(
                                n,
                                _numPartOfDistinctChord,
                                returnChordQuality=False,
                                normaliseResult=False,
                            ).getChangeNumber()
                        )
                elif "Distinct Chord" in way:
                    _numPartOfDistinctChord = int(way[-1])
                    _numPartOfDistinctChord -= 1
                    for n in range(len(self.notes)):
                        _notesByWay.append(
                            self.getDistinctScaleChord(n, _numPartOfDistinctChord)
                        )
                elif way == "Chord":
                    for note in range(len(self.notes)):
                        _notesByWay.append(self.getScaleChord(note))
                elif way == "Chord Page":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            self.getScaleChord(
                                note, returnTypeChange=True
                            ).getChangeNumber(addOneToBookPage=True)
                        )
                elif way == "Third Chord 9ths":
                    for note in range(len(self.notes)):
                        _notesByWay.append(self.getScaleChord(note, numberOfNotes=5))
                elif way == "Fourth Chord 7ths":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            self.getScaleChord(note, noteIndexStepSize=3)
                        )
                elif way == "Fourth Chord 9ths":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            self.getScaleChord(
                                note, noteIndexStepSize=3, numberOfNotes=5
                            )
                        )
                elif way == "Braille":
                    _notesByWay = self.getBraille()
                elif way == "Tetragram":
                    _notesByWay = self.getTetragram(
                        tetragramWays=Tetragram.allowedWays,
                        concatenatePerTetragram=True,
                        decorateWithSmallCircle=Latex.useSmallCircles,
                    )
                elif way == "Trigram Symbol":
                    _notesByWay = self.getTrigram(trigramWays=['symbol'])
                elif way == "Hexagram":
                    _notesByWay = self.getHexagram(
                        hexagramWays=Hexagram.titleWays,
                        concatenatePerHexagram=True,
                        decorateWithSmallCircle=Latex.useSmallCircles,
                    )
                elif way == "Hexagram Symbol":
                    _notesByWay = self.getHexagram(hexagramWays=["symbol"])
                    # _notesByWay=self.getHexagramSymbols()
                elif way == "Hexagram Symbol Name":
                    _notesByWay = self.getHexagram(
                        hexagramWays=["symbol", "name"],
                        concatenatePerHexagram=True,
                        insertStrBetweenSections="",
                        insertStrBetweenAnswers="",
                    )
                elif way == "Hexagram Name":
                    _notesByWay = self.getHexagramName()
                elif way == "Hexagram Number":
                    _notesByWay = self.getHexagramNumbers()
                elif way == "Hexagram Subpage":
                    _notesByWay = self.getHexagram(["subpage"])
                elif way == "RNA Codon":
                    _notesByWay = self.getCodon("RNA")
                elif way == "DNA Codon":
                    _notesByWay = self.getCodon("DNA")
                elif way == "Hexagram Story":
                    _hexagramNumbers = self.byWays("Hexagram Number")
                    _counter = 0
                    _storyStr = []
                    _hexagramNames = self.getHexagram(["name"])
                    # print(_hexagramNumbers)
                    # input('here in byWays("Hexagram Story")')
                    for idx, hexagramNumber in enumerate(_hexagramNumbers):
                        # print('clue',hexagramNumber, _hexagramNumbers)
                        # Then making the pilgramage > Making the pilgramage

                        _halfScale = _counter
                        if (_counter % 2) == 0:

                            _semitonesUp = 6
                            _thisSideStory = Hexagram.storyBeginning
                        elif (_counter % 2) == 1:
                            _halfScale = _counter
                            _semitonesUp = 0
                            _thisSideStory = Hexagram.storyEnd
                            # print('this happened in the first', _counter)

                        _inversionalHexagram = Hexagram.notesets[hexagramNumber]
                        _inversionalHexagram = [
                            i + _semitonesUp for i in _inversionalHexagram
                        ]
                        _inversionalHexagram = Change.makeFromSet(
                            _inversionalHexagram, straighten=True
                        )
                        _rightAlignLatex = "\\hfill "
                        _braille = self.getBraille()
                        # floof
                        if Latex.on:
                            pass  # _rightAlignLatex = ' \\hfill '
                        from Book import Book
                        _colourShift = _semitonesUp + Book.colourTranspose + 6
                        _storyStr.append(
                            # Hexagram.names[hexagramNumber] +
                            Latex.makeDataColoured(
                                Hexagram.symbol[hexagramNumber]
                                + _braille[idx]
                                + _hexagramNames[idx]
                                + Unicode.chars["Way Seperator"]
                                + "("
                                + Unicode.chars["Index Number"]
                                + str(hexagramNumber)
                                + ")"
                                + Unicode.chars["Way Seperator"],
                                colours=_colourShift,
                            )
                        )
                        _scaleSlice = self.divideScaleBy()[
                            (_halfScale) % len(self.divideScaleBy())
                        ].straightenDegrees()
                        # spoof
                        _storyStr[-1] += " ".join(
                            [
                                Latex.makeDataColoured(
                                    str(i), i.semitonesFromOne() + Book.colourTranspose
                                )
                                for i in _scaleSlice.notes
                            ]
                        )
                        _storyStr[-1] += Latex.makeDataColoured(
                            "\\hfill "
                            + Unicode.chars["Tritone Sub"]
                            + Hexagram.symbol[hexagramNumber],
                            colours=_colourShift + 6,
                        )

                        _storyStr[-1] += (
                            " ".join(
                                [
                                    Latex.makeDataColoured(
                                        results=str(i),
                                        colours=int(i.semitonesFromOne())
                                        + int(Book.colourTranspose),
                                    )
                                    for i in _inversionalHexagram.notes
                                ]
                            )
                            + Latex.makeDataColoured(
                                "\\hfill ", colours=_colourShift + 6
                            )
                            + " "
                            + _rightAlignLatex
                            + _thisSideStory[hexagramNumber]
                            + _rightAlignLatex
                            + _inversionalHexagram.getChangeNumber(
                                decorateWithSmallCircle=Latex.useSmallCircles,
                                addOneToBookPage=True,
                                includeNormalisedPageForNegatives=True,
                            )
                        )

                        # input('inversianal'+str(_inversionalHexagram))

                        _rightAlignLatex = ""

                        _counter += 1
                    # This controls which hexagrasm is on the bottom
                    if False:
                        _notesByWay = [_storyStr[0], _storyStr[1]]
                    else:
                        _notesByWay = [_storyStr[1], _storyStr[0]]
                elif way == "Random Poem":
                    _notesByWay = self.getRandomPoem()
                elif way == "Poem":
                    _notesByWay = self.getConsonant()
                elif way == "Word":
                    _notesByWay = self.getTrigram(["syllable"])
                    if type(_notesByWay) == list: _notesByWay = ''.join(_notesByWay)
                elif way == "Colour":
                    _notesByWay = self.getColourGrid()
                elif way == "Classical":
                    _notesByWay = self.romanNumerals(
                        allowedNotes=Change.allowedNoteNamesJazz
                    )

                # elif way == "All Flats Number":
                # 	for note in range(len(self.notes)):
                # 		_notesByWay.append(str(self.straightenDegrees(allowedNotes=Change.allowedNoteNamesAllFlats).notes[note]))
                elif way == "Chord Quality":

                    _notesByWay = self.getChordQuality()

                elif way == "Jazz":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            str(
                                self.straightenDegrees(
                                    allowedNotes=Change.allowedNoteNamesJazz
                                ).notes[note]
                            )
                        )
                    if colourResult:
                        _notesByWay = self.returnColouredLatex(
                            _notesByWay, way, adjustBySemitones=Book.colourTranspose
                        )
                elif way == "Zodiac":
                    _notesByWay = " ".join(self.getZodiac(spaceOutBySemitone=False))

                    if colourResult:
                        _notesByWay = self.returnColouredLatex(
                            _notesByWay, way, adjustBySemitones=Book.colourTranspose
                        )

                elif way == "Rhythm":
                    _notesByWay = self.getRhythm()

                elif way == "Scale Name":
                    _notesByWay = self.getScaleNames(defaultWay="Hexagram Name")
                elif way in JazzNote.carnaticWays:
                    for note in self.straightenDegrees(
                        allowedNotes=Change.allowedNoteNamesCarnatic
                    ).notes:
                        _notesByWay.append(note.byWay(way))
                elif way == "Carnatic" and self.straightenDegrees(
                    allowedNotes=Change.allowedNoteNamesCarnatic
                ) != str(self):
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            str(
                                self.straightenDegrees(
                                    allowedNotes=Change.allowedNoteNamesCarnatic
                                ).notes[note]
                            )
                        )
                    if colourResult:
                        _notesByWay = self.returnColouredLatex(
                            _notesByWay, way, adjustBySemitones=Book.colourTranspose
                        )
                elif way == "Notation":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            str(
                                self.straightenDegrees(
                                    allowedNotes=Change.allowedNoteNamesCarnatic
                                )
                                .byWays("Notation")
                                .notes[note]
                            )
                        )
                elif way == "Mneumonic":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            str(
                                self.straightenDegrees(
                                    allowedNotes=Change.allowedNoteNamesCarnatic
                                )
                                .byWays("Mneumonic")
                                .notes[note]
                            )
                        )

                elif way == "Mela Number":
                    _notesByWay = self.getMelaNumber()

                elif way == "Right Align":
                    _notesByWay = "\\hfill "

                elif way == "Solfege":
                    for note in range(len(self.notes)):
                        _notesByWay.append(
                            str(
                                self.straightenDegrees(
                                    allowedNotes=Change.allowedNoteNamesSolfege
                                )
                                .notes[note]
                                .byWay("Solfege")
                            )
                        )

                elif way == "Names":
                    # TODO: Does not work with rootless changes
                    # _names = self.getScaleNames(searchForDownward=True)
                    _notesByWay = self.getScaleNames(
                        defaultWay=False,
                        searchForDownward=False,
                        searchForNegative=False,
                        includeDownwardHexagram=False,
                        rebindRootToNextNoteIfNoOne=True,
                    )
                elif way == "Efficient":
                    _notesByWay = self.getEfficientKeys()

                elif way == "Unique Change Number":
                    _notesByWay = self.getUniquePage()
                else:
                    raise TypeError("not done the note set way:", way)
            elif JazzNote.isValidWay(way):  # Is a way of individual notes
                # print(way, "made indian numbers",Book.carnaticWays)
                if way in JazzNote.carnaticWays:

                    for note in self.straightenDegrees(Change.allowedNoteNamesCarnatic):
                        _notesByWay.append(note.byWay(way))
                elif way == "Jazz":
                    """for note in self.straightenDegrees(Change.allowedNoteNamesJazz):
                    _notesByWay.append(note.byWay(way))"""
                    _notesByWay = self.straightenDegrees(Change.allowedNoteNamesJazz)
                elif way == "Original Numbers":  # Shit taht's not a thing
                    for note in Change(
                        self.straightenDegrees(Change.allowedNoteNamesAllFlats)
                    ).notes:
                        _notesByWay.append(note.byWay(way))
                elif way == "Solfege":
                    for note in self.straightenDegrees(Change.allowedNoteNamesSolfege):
                        print("in the thing")
                        _notesByWay.append(note.byWayOf(way))
                else:
                    for note in self.notes:
                        _notesByWay.append(note.byWay(way))

                # print('inside byWays: ',_notesByWay,type(_notesByWay))
            elif Key.isValid(way):#JazzNote.isAlphabetNoteStr(way):
                for note in self.notes:
                    _notesByWay.append(note.byWay(way))
            else:
                raise ValueError(
                    type(way),
                    way,
                    " is not in Change.changeValidWays",
                    JazzNote.isAlphabetNoteStr(way),
                    Change.validWays,
                    JazzNote._validWays,
                )
            
                
                #print(way,_byWays)
                #_notesByWay = [Latex.makeTextStyledByWay(i,way) for i in _notesByWay]
                #input(_byWays)
            #print(_notesByWay)
            if _notesByWay and type(_notesByWay) is Change and all([type(n) is JazzNote for n in _notesByWay]):
                #input(str(type(_notesByWay)) + ' ' + str(_notesByWay))
                _notesByWay = Latex.makeTextStyledByWay(str(_notesByWay),"Jazz")
        _byWays.append(_notesByWay)

        if len(_byWays) == 1:
            Change.cache[funcSignature] = _byWays[0]
            return _byWays[0]
        # print('hoola hoop', _byWays)
        Change.cache[funcSignature] = _byWays
        return _byWays

    def printToText(
        self, ways, wayLabels=True, spacesBetweenWords=6, printToScreen=False
    ):
        _textOutput = "\n"
        waysMaxStrLen = max([len(i) for i in ways])

        # _textOutput += "waysMaxStrLen: "+str(waysMaxStrLen)
        for way in ways:
            # fix alphabet note accidentals
            if JazzNote.isAlphabetNoteStr(way):
                _lineOutput = JazzNote.convertNoteToRealUnicodeStr(way) + ": "
            else:
                _lineOutput = way + ": "

            _lineOutput += " " * (waysMaxStrLen - len(way))
            # _lineOutput += str(self.byWays(way))
            _noteOutput = ""
            for note in range(len(self.notes)):

                _noteOutput = str(self.byWays(way)[note])  # Prints name of note
                _lineOutput += _noteOutput  # Prints the note to line
                _adjustment = (
                    len(_lineOutput) - waysMaxStrLen + 1
                ) % spacesBetweenWords
                _noteOutput += " " * _adjustment
                _lineOutput += " " * _adjustment
                # Prints spaces
                if len(_noteOutput) > spacesBetweenWords:
                    _noteExtraLines = []

                # _lineOutput += _noteOutput

                # _noteOutput +=	 ' '#Prints spaces
            _lineOutput += _noteOutput
            _lineOutput += "\n"
            _textOutput += _lineOutput
            """
            find the distance between the starts of a names

            If the label doesn't fit in the line with the spaced out names
            it gets its own line
            """

        if printToScreen:
            print(_textOutput)
        return _textOutput

    def sortBySemitonePosition(self, octaveLimit=False):
        # return self.notes.sorted(key=lambda i: (i.semitonesFromOne(), int(i.scaleDegree())))
        # not using numpy
        return Change(
            sorted(
                self.notes,
                key=lambda note: (
                    JazzNote(note).semitonesFromOne(
                        octaveLimit=octaveLimit, disableNegatives=False
                    ),
                    int(JazzNote(note).scaleDegree()),
                ),
            )
        )


        '''# Create a numpy array of the notes
        notes_array = np.array(self.notes)
        
        # Create a numpy array of the semitones from the reference note
        semitones_array = np.array([JazzNote(note).semitonesFromOne(octaveLimit=octaveLimit, disableNegatives=False) for note in self.notes])

        # Create a numpy array of the scale degree of each note
        scale_degree_array = np.array([int(JazzNote(note).scaleDegree()) for note in self.notes])

        # Use numpy's argsort to get the indices that would sort the notes based on the semitones and scale degree
        sort_indices = np.lexsort((scale_degree_array, semitones_array))

        # Use the sort_indices to sort the notes array
        sorted_notes = notes_array[sort_indices]

        # Return the sorted notes wrapped in a Change object

        return Change(sorted_notes)'''

    def containsDuplicateNote(self, octaveLimit=1):
        for note in self.notes:
            _semitoneList = [
                i.semitonesFromOne(octaveLimit=octaveLimit) for i in self.notes
            ]
            _semitoneList.remove(note.semitonesFromOne(octaveLimit=octaveLimit))
            # print(note,self.notes,_semitoneList)
            for noteToCompare in [i for i in _semitoneList]:
                if note.semitonesFromOne(octaveLimit=octaveLimit) == noteToCompare:
                    return True
        return False

        """_noteList = self.notes
        print('huz', _noteList,self.notes)
        for note in self.notes:
            _noteList = _noteList.remove(self.notes.index(note))
            #print(self.notes,'asldkfsda',_noteList)
            for i in _noteList:
                if( note is i):
                    _noteList = self.notes.remove(note)
                elif note != i:
                    if note.semitonesFromOne(octaveLimit=False) == i.semitonesFromOne(octaveLimit=False):
                        return True
            _noteList = self.notes
        return False"""

    @classmethod
    def hasAllTwelveNotes(cls, allowedNotes):
        _semitoneChecklist = [False for i in range(12)]
        for i, noteName in enumerate(allowedNotes):
            # check if every note is in allowed notes
            _semitoneChecklist[JazzNote(noteName).semitonesFromOne()] = True
            if type(noteName) == JazzNote:
                pass
            elif JazzNote.isJazzNoteStr(noteName):
                pass
            else:
                # Not a valid note
                raise TypeError(
                    "allowedNotes should be list or Change and each note is a JazzNote or jazznotestring",
                    allowedNotes[i],
                    type(allowedNotes[i]),
                )
        # Now check if that set of allowed notes contains all 12 semitone positions
        if False in _semitoneChecklist:
            return False
        else:
            return True

    @classmethod
    def makeFromCarnaticNotation(cls, carnaticNotation): # -> Change:
        # Check Types
        if type(carnaticNotation) == str:
            # Make a str a list
            while carnaticNotation[0] == " ":
                carnaticNotation = carnaticNotation[1:]
            carnaticNotation = carnaticNotation.split(" ")
        elif type(carnaticNotation) == list:
            pass
        else:
            raise TypeError(
                "function expects a carnatic note string not type:",
                type(carnaticNotation),
            )

        _change = []
        while "❟" in carnaticNotation:
            carnaticNotation.remove("❟")
        while "❟ " in carnaticNotation:
            carnaticNotation.remove("❟ ")

        for i, swara in enumerate(carnaticNotation):
            carnaticNotation[i] = carnaticNotation[i].replace("₃", "3")
            carnaticNotation[i] = carnaticNotation[i].replace("₁", "1")
            carnaticNotation[i] = carnaticNotation[i].replace("₂", "2")
            carnaticNotation[i] = carnaticNotation[i].replace("Ṡ", "S")
            carnaticNotation[i] = carnaticNotation[i].replace("Ṙ", "R")
            carnaticNotation[i] = carnaticNotation[i].replace("Ṇ", "N")
            carnaticNotation[i] = carnaticNotation[i].strip()

        for swara in carnaticNotation:
            # Is it a valid notation note
            while swara[0] == " ":
                swara = swara.strip()
            if not swara in JazzNote.jazzNoteToWayTable["Notation"].values():
                # raise ValueError(swara+' is not in list:', JazzNote.jazzNoteToWayTable['Notation'])
                return (
                    'try again buddy it did not work, this swara not cool: "'
                    + swara
                    + '".'
                    + ",".join(carnaticNotation)
                )
            for jazzNote, notationSwara in JazzNote.jazzNoteToWayTable[
                "Notation"
            ].items():
                if notationSwara == swara:
                    _change.append(jazzNote)

        # Remove duplicates
        def remove_duplicates(li):
            my_set = set()
            res = []
            for e in li:
                if e not in my_set:
                    res.append(e)
                    my_set.add(e)
            return res

        _change = remove_duplicates(_change)
        _change = Change(_change).sortBySemitonePosition()
        return (_change.getChangeNumber(addOneToBookPage=True), _change)

    @classmethod
    def modeOfSet(cls, set, modeNumber, returnInt=False):
        answer = (
            Change.makeFromSet(set, straighten=False).mode(modeNumber).byWays("Set")
        )
        if returnInt:
            return [int(i) for i in answer]
        else:
            return answer

    @classmethod
    def isValidWay(cls, way):
        # added the second part? (after the +)
        

        try:
            if way in Change.validWays:
                return True
            elif JazzNote.isValidWay(way):
                return False
                # raise ValueError(way," is a valid JazzNote way, but not a valid Change way, which would be one of these: ",Change.changeValidWays)
            else:
                return False
        except ValueError as e:
            print('way that made it crach ==',way.__repr__())
            raise e

from Latex import Latex
