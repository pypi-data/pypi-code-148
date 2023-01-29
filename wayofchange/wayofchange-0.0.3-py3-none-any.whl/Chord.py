from __future__ import annotations, print_function

class Chord:
    useQuartalChords = True
    validTypes = [
        "triadic Diad",
        "triadic Triad",
        "triadic 7th",
        "triadic 9th",
        "triadic 11th",
        "triadic 13th",
        "triadic 15th",
        "triadic 17th",
        "triadic 19th",
        "triadic 21st",
    ]

    if useQuartalChords == True:
        validTypes += [
            "quartal Diad",
            "quartal Triad",
            "quartal 7th",
            "quartal 9th",
            "quartal 11th",
            "quartal 13th",
            "quartal 15th",
            "quartal 17th",
            "quartal 19th",
            "quartal 21st",
        ]
    # affects Change.getChordQuality and cls.makePlain and cls.makeStyled
    qualityDefaults = {
        'useHalfDiminishedUnicodeSymbols': True,
        'useDiminishedUnicodeSymbols': False,
    }

    @classmethod
    def makePlain(cls, text):
        return (
            text.replace(Book.unicodeChars["Flat"], "b")
            .replace(Book.unicodeChars["Sharp"], "#")
            .replace("Ma", "ma")
            .replace(Book.unicodeChars["diminished chord"], "dim")
            .replace(Book.unicodeChars["half diminished chord"], "halfdim")
        )

    @classmethod
    def makeStyled(cls, text, **kwargs):
        '''Pass This useHalfDiminishedUnicodeSymbols or 'useDiminishedUnicodeSymbols'''
        if useUnicodeChars:
            text = (
                str(text)
                .replace("b", Book.unicodeChars["Flat"])
                .replace("#", Book.unicodeChars["Sharp"])
                .replace("ma", "Ma")
            )
            if 'useHalfDiminishedUnicodeSymbols' in kwargs.keys():
                useHalfDiminishedUnicodeSymbols = kwargs['useHalfDiminishedUnicodeSymbols']
            else:
                useHalfDiminishedUnicodeSymbols = Chord.qualityDefaults['useHalfDiminishedUnicodeSymbols']
            if 'useDiminishedUnicodeSymbols' in kwargs.keys():
                useDiminishedUnicodeSymbols = kwargs['useDiminishedUnicodeSymbols']
            else:
                useDiminishedUnicodeSymbols = Chord.qualityDefaults['useDiminishedUnicodeSymbols']
            if useHalfDiminishedUnicodeSymbols:
                text = text.replace(
                    "halfdim", Book.unicodeChars["half diminished chord"]
                )
            if useDiminishedUnicodeSymbols:
                text = text.replace(
                    "dim", Book.unicodeChars["diminished chord"]
                )
            return text
        else:
            return text

    @classmethod
    def makeJazzNoteLikeChordSymbolExtension(cls, jazzNote, **kwargs):
        '''Pass This useHalfDiminishedUnicodeSymbols or 'useDiminishedUnicodeSymbols'''
        jazzNote = JazzNote(jazzNote)
        if jazzNote in Change(["7"]):
            return cls.makeStyled("ma7")
        elif jazzNote == JazzNote("b7"):
            return "7"
        else:
            return cls.makeStyled(jazzNote, **kwargs)

    @classmethod
    def chordQualityToChange(cls, quality: str) -> Change:
        _notes = []
        _triadTypes = ('dim', 'aug', 'sus', 'mi', 'ma',)
        _triad = False
        _triadIndex = None
        _extension = False
        _triadFound = False
        _third = False
        _strBeforeExtension = False
        plainQuality = Chord.makePlain(quality)
        if quality == 'Ma(no 5 add 9)': pass  # input(plainQuality)
        for triad in _triadTypes:
            if _triadFound: break
            if not _triadFound and triad in plainQuality:

                if triad in ('mi',):
                    _notes.extend(['b3', '5'])
                    _triad = triad
                    _triadFound = True
                    _third = 'b3'
                    _fifth = '5'

                elif triad == 'dim':
                    _notes.extend(['b3', 'b5'])
                    _triad = triad
                    _triadFound = True
                    _third = 'b3'
                    _fifth = 'b5'

                elif triad in ('sus', 'Sus'):
                    if '(' in quality:
                        _third = quality[quality.index(triad) + len(triad):quality.index('(')]
                    else:
                        _third = quality[quality.index(triad) + len(triad):]
                    _third = Chord.makePlain(_third)
                    _triad = triad.lower() + JazzNote.convertUnicodeAccidentalsToSimpleStr(_third)
                    _notes.append(Chord.makePlain(_third))
                    print('appended third and fifth', Chord.makePlain(_third))
                    _notes.append('5')
                    _fifth = '5'
                    _triadFound = True
                elif triad in ('ma', 'Ma'):
                    print('appended 3 and 5 because ma is the triad(?)')
                    _notes.extend(['3', '5'])
                    _triad = triad
                    _triadFound = True
                    _third = '3'
                    _fifth = '5'
        if _triadFound and 'sus' in _triad:

            try:
                _triadIndex = plainQuality.index(_triad)
            except:
                input('_triad {} not found in quality {}\n{}'.format(_triad, quality,
                                                                     JazzNote.convertUnicodeAccidentalsToSimpleStr(
                                                                         quality)))
            print('sus happened. triad {}. triadIndex {}'.format(_triad, _triadIndex))
            if _triadIndex != 0:
                _extension = plainQuality[:_triadIndex].lower()
                print('grabbed triad index {}'.format(_triadIndex))
        elif _triadFound and 'sus' not in _triad:
            pass  # input('herrrrrrrrrrrrrrrre')
            _triadIndex = plainQuality.index(_triad)
            if '(' in quality:
                _searchEnd = quality.index('(')
            else:
                _searchEnd = len(quality)
            if plainQuality[_triadIndex + len(_triad):_searchEnd]:
                _extension = plainQuality[_triadIndex + len(_triad):_searchEnd]

        elif not _triadFound:

            _char = quality[0]
            _twoChars = quality[0:2]
            _threeChars = quality[0:3]
            print('yoyoyoyoyoyo')
            # input(_threeChars)
            if _threeChars == '6/9':
                print('added 3 5 6 9')
                _notes.extend(['3', '6', '9'])
                _third = '3'
                _fifth = '5'
                _extension = '6/9'
            elif _char == '6':
                _notes.extend(['3', '6', '5'])
                # I do not know why the nexxxt line used the minor third before
                _third = '3'
                _fifth = '5'
                # input('_notes == {} and triad was not found for {}'.format(_notes,quality))
            elif _char == '7':
                _notes.extend(['3', '5', 'b7'])
                _third = '3'
                _fifth = '5'
            elif _char == '5':
                _fifth = '5'
                _notes.append('5')

            elif _char == '9':
                # NOT doing anything
                # _notes.append([_third,'5','b7','9'])
                _fifth = '5'
                _third = '3'
                _extension = '9'
                # _notes.append('5')
            elif _twoChars == '11':
                # _notes.extend(['3','5','7','9','11'])

                _fifth = '5'
                _third = '3'
                _extension = '11'
            elif _twoChars == '13':
                _fifth = '5'
                _third = '3'
                _extension = '13'

            else:
                raise ValueError('shit, triad {} not found in {}'.format(_triad, quality))

        else:

            _triadIndex = plainQuality.index(_triad)
            print('\n_notes == {}  _third == {} _fifth == {} _triad == {} _extension == {} _triadIndex {}'.format(
                _notes, _third, _fifth, _triad, _extension, _triadIndex, )
            )
            # print('thinnnnngs',plainQuality,_triadIndex)
            # input()
            if _triadIndex > 0:
                if '(' not in quality:
                    _extension = plainQuality[_triadIndex:]
                else:
                    _extension = plainQuality[_triadIndex + len(_triad):quality.index('(')]

            # input('sus not in _triad: {}.. _extension: "{}" _triadIndex: {}'.format(_triad,_extension,_triadIndex))
            pass  # input('extension {} not found in {}'.format(_extension,quality[:_triadIndex]))

        if _extension: _extension = Chord.makePlain(_extension)
        if _extension in ('dim7',):
            _notes.append('6')
        if _extension in ('6/9', '5', '6', '7', 'ma7', '9', 'mi9', 'ma9', '11', 'mi11', 'ma11', '13', 'mi13', 'ma13'):
            # print(plainQuality,_extension)
            if '5' not in _notes and _triad != 'dim':
                if '5' not in _notes: _notes.append('5')
            if _extension.isnumeric():

                _strBeforeExtension = plainQuality[plainQuality.index(_extension) - 2:plainQuality.index(_extension)]
            else:
                if '6/9' not in quality:
                    _strBeforeExtension = _extension[:2]
                else:
                    _strBeforeExtension = ''
            if _extension in ('9', 'mi9', 'ma9', '11', 'mi11', 'ma11', '13', 'ma13'):
                if _triad != 'dim':
                    if '5' not in _notes: _notes.append('5')

            if _extension == '6/9':
                if '6' not in _notes: _notes.append('6')
                if '9' not in _notes: _notes.append('9')
            if _extension.lower() in ('7', 'ma7', '9', 'mi9', 'ma9', '11', 'mi11', 'ma11', '13', 'mi13', 'ma13'):
                # _notes.extend(['1','3','5','7'])
                print('added b7')
                _notes.append('b7')
                if _third not in _notes: _notes.append(_third)
                print('added _third', _third)
            if _extension.lower() in ('9', 'mi9', 'ma9', '11', 'mi11', 'ma11', '13', 'ma13'):
                # NOT doing anything
                # _notes.extend([_third,'5','9'])
                # _notes.extend(['9'])
                _notes.append('9')
                print('added 9')

                _fifth = '5'
            if _extension.lower() in ('11', 'mi11', 'ma11', '13', 'mi13', 'ma13'):
                _notes.append('11')
            if _extension.lower() in ('13', 'ma13', 'mi13'):
                _notes.append('13')
                # _notes.append('5')
            if _extension in ('6', 'ma6'):
                _notes.append('6')
                # _notes.extend([_third,_fifth,'6'])
                print('added _extension: "{}" to _notes: {}'.format(_extension, _notes))
            if _extension == '5':
                print('added the 5')
                _notes.append('5')
            '''else:
                raise ValueError(_extension)
                print('added _extension: "{}" to _notes: {}'.format(_extension,_notes))
                _notes.append(_extension)'''
            if _strBeforeExtension in ('Ma', 'ma') or 'ma' in _extension:
                _notes.remove('b7')
                _notes.append('7')
            if _extension in ('7', '9', '11', '13') and _triad == 'dim':
                _notes.remove('b7')
                _notes.append('6')
            if _strBeforeExtension == 'mi' or 'mi' in _extension:
                if '7' in _notes:
                    _notes.remove('7')
                    _notes.append('b7')
                    # input('wooooooo')
            else:
                pass  # input('hoooooo {}'.format(_extension))
            if '6/9' in quality:
                pass
                # input('here man {}'.format(_notes))
                # _notes.extend(['6','9'])
            print('before applying bracket mods, notes == ', _notes)
        else:
            pass
            print('we could not do the extension', _extension)
        # input('_notes get set to : {} for {}'.format(_notes,quality))
        _bracketElements = []
        if '(' in quality:
            _bracketElements = (quality[quality.index('(') + 1:-1]).split(' ')
            # input(_bracketElements)
        _bracketMod = False
        for e, el in enumerate(_bracketElements):
            # print(e,el)
            if (e == 0 and el not in ('no', 'add')) \
                    or (_bracketMod == 'modify' and el not in ('no', 'add')):
                _bracketMod = 'modify'
                if JazzNote(el).scaleDegree() in _notes:
                    _noteToRemove = JazzNote(el).scaleDegree()
                elif el in _notes:
                    _noteToRemove = el
                elif 'b' + el in _notes:
                    _noteToRemove = 'b' + el
                else:
                    input('_noteToRemove: {} not in _notes: {}'.format(JazzNote(el).scaleDegree(), _notes))
                _noteToAdd = Chord.makePlain(el)
                try:
                    _notes.remove(_noteToRemove)

                    if _noteToAdd not in _notes and JazzNote(_noteToAdd).limitSemitonesToNumberOfOctaves(
                            1) not in _notes:
                        _notes.append(_noteToAdd)
                    print('replaced {} with {} cause mod is in brackets'.format(_noteToRemove, _noteToAdd))
                except:
                    raise ValueError('_noteToRemove: {} not in _notes {}'.format(_noteToRemove, _notes))

                continue
            elif el in ('no', 'add'):
                print('set bracketmod to', _bracketMod)
                _bracketMod = el
                continue
            if _bracketMod == 'no':
                if _triad != 'dim' and el in _notes:
                    print('removed', el, 'from', _notes, 'because brackets told me to')
                    _notes.remove(el)
                    # input(_notes)
                elif _triad == 'dim' and el == '7':

                    _notes.remove('6')
                    print('removed 6 from', _notes, 'because brackets told me to by saying "no 7" on a dim chord')

                elif 'b' + el in _notes:
                    _notes.remove('b' + el)
                    print('removed', el, 'from', _notes, 'because brackets told me to')

                else:
                    # raise TypeError('could not remove note {} not in _notes: {} for {} extension == {}'.format(el,_notes,quality,_extension))

                    pass
                    # input('el: {} not in _notes: {} for {}'.format(el,_notes,quality))
            elif _bracketMod == 'add':
                _notes.append(Chord.makePlain(el))
                print('added note {}. Notes == {}'.format(el, _notes))
                # input('shit')
            # input('{} {} {}'.format(e,el,_bracketMod))
        print('_notes {} became _notes {}'.format(_notes, Change(_notes)))
        _notes = Change(_notes)
        # input(_notes)
        # print('Change({}) == {}'.format(_notes,Change(_notes)))
        # constrain to octave
        test = Change(['1', '5'])

        semitones = [0] + [n % 12 for n in _notes.getSemitones()]
        # print('Change({}).getSemitones() == {}'.format(_notes,_notes.getSemitones()))
        semitones.sort()
        change = Change(noteset=semitones)
        print(
            '{}  {}  \n_notes == {}  _third == {} _triad == {} semitones == {} _extension == {} _bracketmod == {} _bracketelements {} _traidIndex {} _strBeforeExtension {}'.format(
                change.getChangeNumber(), change, _notes, _third, _triad, semitones, _extension, _bracketMod,
                _bracketElements, _triadIndex, _strBeforeExtension)
        )
        return change

    @classmethod
    def otherGetDistinctChordTypes(
            cls, changeLength: int, includeTriadic=True, includeQuartal=True
    ):
        """If there are no distincts for that length, will return None"""
        _chordTypes = []
        if _len in (
                0,
                1,
                2,
        ):
            return None
        elif _len == 3:
            _chordTypes += ["triadic Diad"]
        elif _len == 4:
            _chordTypes += ["quartal Diad", "triadic Diad"]
        elif _len == 5:
            _chordTypes += [
                "quartal Triad",
                "triadic Triad",
                "triadic Diad",
                "triadic 7th",
            ]
        elif _len == 6:
            _chordTypes += ["triadic Tiad", "quartal Diad"]
        elif _len == 7:
            _chordTypes += [
                "triadic 9th",
                "triadic 7th",
                "triadic Diad",
                "triadic Triad",
                "triadic 11th",
            ]
        elif _len == 8:
            _chordTypes += [
                "triadic 7th",
                "quartal 7th",
                "triadic Diad",
                "triadic Triad",
            ]
        elif _len >= 9:
            _chordTypes += [
                "triadic 7th",
                "triadic 9th",
                "triadic Diad",
                "triadic Triad",
                "triadic 11th",
                "triadic 13th",
                "triadic 15th",
            ]
        return _chordTypes

    @classmethod
    def chordIndexes(
            cls,
            changeLength: int,
            rootIndex: int = 0,
            chordType="triadic 7th",
            showDebug=False,
    ):
        if rootIndex != 0:
            pass  # raise ValueError('not supposed to happen')
        if not chordType in cls.validTypes:
            raise ValueError(
                "Chord must be in validTypes" + chordType + str(Chord.validTypes)
            )

        if changeLength in (0, 1):
            return []
        if "triadic" in chordType:
            _d = 2
        elif "quartal" in chordType:
            _d = 3

        if " Diad" in chordType:
            _n = 2
        elif " Triad" in chordType:
            _n = 3
        elif " 7th" in chordType:
            _n = 4
        elif " 9th" in chordType:
            _n = 5
        elif " 11th" in chordType:
            _n = 6
        elif " 13th" in chordType:
            _n = 7
        elif " 15th" in chordType:
            _n = 8
        elif " 17th" in chordType:
            _n = 9
        elif " 19th" in chordType:
            _n = 10
        elif " 21st" in chordType:
            _n = 11

        _indexes = []

        for n in range(_n):
            _indexes.append((n * _d + rootIndex) % (changeLength))
        if showDebug:
            print("n=", _n, "chordtype", chordType, "indexes", _indexes, end="\n")

        elif changeLength == 0:
            _indexes = []
        _indexes = list(set(_indexes))
        _indexes.sort()

        return _indexes

    @classmethod
    def makeValidChordList(cls, removeChordsWithOneNoteLessThanTotal=True):

        validTypesByLength = []
        validIndexesByLength = []
        print("testing chord indexes")
        for n in range(13):
            print(
                "length",
                n,
            )
            validTypesByLength.append([])
            validIndexesByLength.append([])

            for chordType in Chord.validTypes:
                _indexes = Chord.chordIndexes(changeLength=n, chordType=chordType)
                if (
                        not _indexes in validIndexesByLength[-1]
                        and _indexes != list(range(n))
                        and len(_indexes) > 1
                ):
                    if (
                            removeChordsWithOneNoteLessThanTotal == False
                            or len(_indexes) != n - 1
                    ):
                        validIndexesByLength[-1].append(_indexes)
                        validTypesByLength[-1].append(chordType)

                # print('type', chordType, 'indexes',_indexes)
        # input('thars the list uv chords')
        for i, n in enumerate(validTypesByLength):
            # pass
            print(
                "flex",
                i,
                n,
            )  # validIndexesByLength[i])
        # input('thars the list uv chords')
        Chord.validIndexesByLength = validIndexesByLength
        Chord.validTypesByLength = validTypesByLength

    @classmethod
    def getChordTypesForLength(cls, length, maxChordTypes=99):
        _types = []

        if len(Chord.validTypesByLength[length]) <= maxChordTypes:
            _types = Chord.validTypesByLength[length]
        else:  # There are more chords available than the maxChordTypes
            print("asd")
            # input('asdfasdf')
            _types = Chord.validTypesByLength[length]

            if not _types in ([], None):
                for chordType in ["triadic ", "quartal "]:
                    print(
                        "jethro "
                        + str(_types)
                        + chordType
                        + str(("triadic " + "Diad") in _types)
                    )
                    if (chordType + "Diad") in _types:
                        if (chordType + "7th") in _types:
                            print("tull")
                            _types.remove(chordType + "Diad")
                    if (chordType + "Triad") in _types:
                        if (chordType + "9th") in _types:
                            print(_types, "before")
                            _types.remove(chordType + "Triad")
                            print(_types, "after")
            return _types[:maxChordTypes]
        return _types[:maxChordTypes]

from classFiles.Change import Change