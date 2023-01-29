from __future__ import annotations, print_function
from JazzNote import JazzNote
from Utility import Utility
input = Utility.input
class Key:
    allFlats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    onlyNaturals = ["C", "D", "E", "F", "G", "A", "B"]
    flatAscii, sharpAscii = "b", "#"
    flat, sharp, doubleFlat, doubleSharp = "♭", "♯", "𝄫", "𝄪"
    useUnicodeChars = True
    useDoubleAccidentals = False

    def __add__(self, n:int) -> Key:
        return Key(Key.allFlats[(self.distanceFromC() + n) % 12])
    def __sub__(self, n:int) -> Key:
        return Key(Key.allFlats[(self.distanceFromC() - n) % 12])
    def __int__(self) -> int:
        return self.distanceFromC()
    def __init__(self, note: str, scaleFunction: JazzNote = None):
        if Key.isValid(note):
            self.note = (
                note.replace(Key.doubleSharp, Key.sharpAscii * 2)
                .replace(Key.doubleFlat, Key.flatAscii * 2)
                .replace(Key.sharp, Key.sharpAscii)
                .replace(Key.flat, Key.flatAscii)
            )
            if scaleFunction != None:
                self.note = self.onJazz(scaleFunction).note
                # input('asdf {} {} {}'.format(self,scaleFunction,self.onJazz(scaleFunction)))
        elif isinstance(note, Key):
            if scaleFunction == None:
                self.note = note.note
            else:
                self.note = self.onJazz(scaleFunction).note
        else:
            raise TypeError(
                "Key expects valid note in str or Key types, not {} {}".format(
                    type(note), note
                )
            )
        assert self.note

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return "Key('" + self.note + "')"

    def __str__(self, useUnicode=None, useDoubleAccidentals=None) -> str:
        if useUnicode == None:
            useUnicode = Key.useUnicodeChars
        if useUnicode == False:
            return self.note
        if useDoubleAccidentals == None:
            useDoubleAccidentals = Key.useDoubleAccidentals
        if useDoubleAccidentals:
            subs = (
                Key.flatAscii * 2,
                Key.sharpAscii * 2,
                Key.flatAscii,
                Key.sharpAscii,
            )
            replacements = (Key.doubleFlat, Key.doubleSharp, Key.flat, Key.sharp)
        else:
            subs = (Key.flatAscii, Key.sharpAscii)
            replacements = (Key.flat, Key.sharp)
        _str = self.note
        for s in range(len(subs)):
            sub, replacement = subs[s], replacements[s]
            _str = _str.replace(sub, replacement)
        return _str

    def __len__(self):
        return len(self.note)
    def __getitem__(self,i):
        return self.note[i]
    

    def inAllFlats(self):
        return Key(Key.allFlats[self.distanceFromC() % 12])

    @classmethod
    def accidentalsStr(cls, step: int, useAscii=True):
        if step < 0:
            return Key.flatAscii * abs(step)
        elif step > 0:
            return Key.sharpAscii * step
        else:
            return ""

    def distanceFromC(self) -> int:
        return Key.allFlats.index(self.note[0]) + JazzNote.accidentalsToDistance(
            self.note[1:]
        )

    def getAccidentalSum(self) -> int:
        return self.note.count(Key.sharpAscii) - self.note.count(Key.flatAscii)

    def removeAccidentals(self) -> Key:
        return Key(self.note[0])

    def onJazz(self, jazz: JazzNote) -> Key:
        scaleDegree = int(jazz.scaleDegree())

        newKeyDegree = Key(Key.onlyNaturals[
                               (Key.onlyNaturals.index(self.note[0]) \
                                + scaleDegree - 1) % len(Key.onlyNaturals)])

        rootDist = (newKeyDegree.distanceFromC() - Key(self.note).distanceFromC()) % 12
        newKeyAccidentals = self.getAccidentalSum() + jazz.getAccidentalSum()
        newKeyAccidentals = Key.accidentalsStr(newKeyAccidentals)
        '''print('self {} jazz {} scaledegree {} newkeydegree {} newKeyAccidentals {} rootdist {} == {}'.format(
            self, jazz, scaleDegree, newKeyDegree, newKeyAccidentals, rootDist, Key(str(newKeyDegree) + newKeyAccidentals)
        ))'''
        return Key(str(newKeyDegree) + newKeyAccidentals)
        return Key(JazzNote(jazz).byWay(self.getASCII()))

    def isBlack(self) -> bool:
        return self.distanceFromC() in (1, 3, 6, 8, 10)

    def isWhite(self) -> bool:
        return not self.distanceFromC() in (1, 3, 6, 8, 10)

    def getEnharmonic(self, keyDegreeTranspose: int):
        root = Key(
            Key.onlyNaturals[
                (Key.onlyNaturals.index(self.note[0]) + keyDegreeTranspose)
                % len(Key.onlyNaturals)
            ]
        )
        accSum = (
            self.getAccidentalSum()
            + self.removeAccidentals().distanceFromC()
            - root.distanceFromC()
        )
        if accSum > 6:
            accSum = -(12 - accSum)
        elif accSum < -6:
            accSum = 12 - abs(accSum)
        return Key(str(root) + Key.accidentalsStr(accSum))
        input("bloop {} {} {} {} ".format(self, keyDegreeTranspose, root, accSum))

    def getAllowedJazz(
        self,
        jazz: JazzNote,
        maxAccidentals=2,
    ) -> [JazzNote]:
        allowedJazz = []
        accSum = self.getAccidentalSum()
        enharmonic = self
        for i in range(7):
            if abs(enharmonic.getAccidentalSum()) <= maxAccidentals:
                allowedJazz.append(enharmonic)
            enharmonic = enharmonic.getEnharmonic(-1)
        """if accSum == 0:
            allowedJazz.append(enharmonic)"""
        # input('fdafdsa {} accSum{} maxAccs{} allowedJazz {}'.format(
        #    self,accSum,maxAccidentals,allowedJazz))
        return allowedJazz

    def getASCII(self):
        return self.note.replace(Key.flat, Key.flatAscii).replace(
            Key.sharp, Key.sharpAscii
        )

    @classmethod
    def isValid(self, note: str):
        if not (type(note) is str):
            # raise TypeError(noteName,' is not str.')
            return False
        if not (note[0] in Key.onlyNaturals):
            # raise ValueError('noteName[0] is not in noteNameNaturals, it is: ',noteName[0])
            return False
        sharps, flats = False, False  # (False,)*2
        sharpChars = (Key.sharp, Key.sharpAscii, Key.doubleSharp)
        flatChars = (Key.flat, Key.flatAscii, Key.doubleFlat)
        if len(note) > 1:
            if note[1] in sharpChars:
                sharps = True
            elif note[1] in flatChars:
                flats = True
            else:
                # raise ValueError(noteName[1]," is not 'b' or '#'")
                return False
            for char in note[1:]:
                if sharps:
                    if not char in sharpChars:
                        raise ValueError("sharps turned into ", char)
                elif flats:
                    if not char in flatChars:
                        raise ValueError("flats turned into ", char)
        return True
