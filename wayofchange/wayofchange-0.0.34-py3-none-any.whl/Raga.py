from Utility import Utility
input = Utility.input
class Raga:
    """Ragas are like Changes, but they have two directions,
    with possible multiple options per direction
    They also have articulations that may occur before, during, or after notes.
    They may have Tala (rhythmic figure[s]) associated with it
    Melkarta Ragas (Melas) have a mela number associated with them
    Finally, they will have a name, and possible alternate names"""

    # https: // asmp - eurasipjournals.springeropen.com / articles / 10.1186 / s13636 - 016 - 00    83 - z  # Fig2
    melaNameByMelaNumber = []
    melaNameByMelaNumber.insert(0, "Mela Error")
    melaNameByMelaNumber.insert(1, "Kanakangi")
    melaNameByMelaNumber.insert(2, "Ratnangi")
    melaNameByMelaNumber.insert(3, "Ganamurti")
    melaNameByMelaNumber.insert(4, "Vanaspati,Venaspati")
    melaNameByMelaNumber.insert(5, "Manavati,Tenarupi")
    melaNameByMelaNumber.insert(6, "Tanarupi,Tenarupi")
    melaNameByMelaNumber.insert(7, "Senavati")
    melaNameByMelaNumber.insert(8, "Hanumatodi,Hanumattodi")
    melaNameByMelaNumber.insert(9, "Dhenuka")
    melaNameByMelaNumber.insert(10, "Natakapriya")
    melaNameByMelaNumber.insert(11, "Kokilapriya")
    melaNameByMelaNumber.insert(12, "Rupavati")
    melaNameByMelaNumber.insert(13, "Gayakapriya")
    melaNameByMelaNumber.insert(14, "Vakulabharanam")
    melaNameByMelaNumber.insert(15, "Mayamalavagowla,Mayamalavagaula")
    melaNameByMelaNumber.insert(16, "Chakravakam,Cakravka")
    melaNameByMelaNumber.insert(17, "Suryakantam")
    melaNameByMelaNumber.insert(18, "Hatakambari")
    melaNameByMelaNumber.insert(19, "Jhankaradhwani")
    melaNameByMelaNumber.insert(20, "Natabhairavi")
    melaNameByMelaNumber.insert(21, "Keeravani")
    melaNameByMelaNumber.insert(22, "Kharaharapriya")
    melaNameByMelaNumber.insert(23, "Gourimanohari")
    melaNameByMelaNumber.insert(24, "Varunapriya")
    melaNameByMelaNumber.insert(25, "Mararanjani")
    melaNameByMelaNumber.insert(26, "Charukesi")
    melaNameByMelaNumber.insert(27, "Sarasangi")
    melaNameByMelaNumber.insert(28, "Harikambhoji")
    melaNameByMelaNumber.insert(
        29, "Dheerasankarabaranam,Shankarabharanam,Dhirasankarabharana"
    )
    melaNameByMelaNumber.insert(30, "Naganandini,Ragavardhini")
    melaNameByMelaNumber.insert(31, "Yagapriya")
    melaNameByMelaNumber.insert(32, "Ragavardhini")
    melaNameByMelaNumber.insert(33, "Gangeyabhushani")
    melaNameByMelaNumber.insert(
        34, "Vagadheeswari,Vagadhisvari,Vagadheeswari,Vagadhibhusani"
    )
    melaNameByMelaNumber.insert(35, "Shulini,Sulini")
    melaNameByMelaNumber.insert(36, "Chalanata")
    melaNameByMelaNumber.insert(37, "Salagam,Salaga")
    melaNameByMelaNumber.insert(38, "Jalarnavam,Jalarnava")
    melaNameByMelaNumber.insert(39, "Jhalavarali,Jhalavarli")
    melaNameByMelaNumber.insert(40, "Navaneetam,Navanitam")
    melaNameByMelaNumber.insert(41, "Pavani")
    melaNameByMelaNumber.insert(42, "Raghupriya")
    melaNameByMelaNumber.insert(43, "Gavambhodi,Gavambodhi")
    melaNameByMelaNumber.insert(44, "Bhavapriya")
    melaNameByMelaNumber.insert(
        45, "Shubhapantuvarali,Subhapantuvarali,Shubhapanturavali"
    )
    melaNameByMelaNumber.insert(46, "Shadvidamargini,Shubhapanturavali")
    melaNameByMelaNumber.insert(47, "Suvarnangi")
    melaNameByMelaNumber.insert(48, "Divyamani,Dvyamani")
    melaNameByMelaNumber.insert(49, "Dhavalambari")
    melaNameByMelaNumber.insert(50, "Namanarayani")
    melaNameByMelaNumber.insert(51, "Kamavardani,Kamavardhani")
    melaNameByMelaNumber.insert(52, "Ramapriya")
    melaNameByMelaNumber.insert(53, "Gamanashrama,Gamanasrama")
    melaNameByMelaNumber.insert(54, "Vishwambari,Visvambhari")
    melaNameByMelaNumber.insert(55, "Shamalangi,Syamalangi")
    melaNameByMelaNumber.insert(56, "Shanmukhapriya,Sanmukhapriya")
    melaNameByMelaNumber.insert(57, "Simhendramadhyamam,Simhendramadhyama")
    melaNameByMelaNumber.insert(58, "Hemavati")
    melaNameByMelaNumber.insert(59, "Dharmavati")
    melaNameByMelaNumber.insert(60, "Neetimati,Nitimati")
    melaNameByMelaNumber.insert(61, "Kantamani")
    melaNameByMelaNumber.insert(62, "Rishabhapriya,Risabhapriya")
    melaNameByMelaNumber.insert(63, "Latangi")
    melaNameByMelaNumber.insert(64, "Vachaspati,Vacaspati")
    melaNameByMelaNumber.insert(65, "Mechakalyani,Mechakalyani,Mecakalyani")
    melaNameByMelaNumber.insert(66, "Chitrambari,Chitrambari,Citrambari")
    melaNameByMelaNumber.insert(67, "Sucharitra,Sucaritra")
    melaNameByMelaNumber.insert(68, "Jyoti swarupini,Jyotisvarupini")
    melaNameByMelaNumber.insert(69, "Dhatuvardani,Dhatuvardhani")
    melaNameByMelaNumber.insert(70, "Nasikabhushani,Nasikabhusani")
    melaNameByMelaNumber.insert(71, "Kosalam")
    melaNameByMelaNumber.insert(72, "Rasikapriya")

    @classmethod
    def makeFestivalSounds(
        cls,
        includeAssociatedChords=True,
        includeAssociatedModes=False,
        sortByPageNumber=True,
        showDebug=False,
    ) -> [int]:
        """returns subChange numbers of melaNameByMelaNumber and associated changes."""
        _melaPages = [Raga.pageFromMelaNumber[i] for i in range(73)][1:]
        _chordPages = []


        _numOfDistinctChordsIncluded = 2
        if includeAssociatedChords:
            for melaPage in _melaPages:
                from .Change import Change
                _mela = Change.makeFromChangeNumber(melaPage)
                if showDebug:
                    print(
                        "Mela: {}\nnum{}\nmelaP{}".format(
                            _mela,
                            _numOfDistinctChordsIncluded,
                            _mela.getDistinctChordTypes(),
                        )
                    )
                _chordTypes = min(
                    _numOfDistinctChordsIncluded, len(_mela.getDistinctChordTypes())
                )

                for chordType in range(_chordTypes):
                    for note in range(len(_mela)):
                        _chord = _mela.getDistinctScaleChord(
                            note, chordType, returnChordQuality=False
                        )
                        if showDebug:
                            print("as " + str(_chord))
                        _chordPages.append(
                            _chord.getChangeNumber(decorateChapter=False)
                        )
        _chordPages = list(set(_chordPages))
        if showDebug:
            input(
                "Mela Pages {} \nCHord Pages{}".format(
                    [Change.makeFromChangeNumber(i) for i in _melaPages], _chordPages
                )
            )

        if includeAssociatedModes:
            _modePages = []
            for p in _melaPages:
                _mela = Change.makeFromChangeNumber(p)
                for n in range(len(_mela.notes)):
                    _mode = _mela.mode(n)
                    _modePage = _mode.getChangeNumber(decorateChapter=False)
                    if not _modePage in _modePages:
                        _modePages.append(_modePage)
            _melaPages = _melaPages + _modePages
        if includeAssociatedChords:
            _melaPages = _melaPages + _chordPages
            if showDebug:
                print("Chord Pages", _chordPages)

        _melaPages = list(set(_melaPages))
        if sortByPageNumber:
            _melaPages.sort()
        return _melaPages

    @classmethod
    def shortenRagaNameWithSymbols(
        cls,
        ragaName: str,
        replaceDirections=True,
        replaceRagaAndMela=True,
        useSpaces=True,
    ) -> str:
        if useSpaces:
            _space = " "
        else:
            _space = ""
        if replaceDirections:
            ragaName = ragaName.replace(
                " (ascending)", _space + Book.unicodeChars["Ascending"]
            ).replace(" (descending)", _space + Book.unicodeChars["Descending"])
        if replaceRagaAndMela:
            ragaName = ragaName.replace(
                "Raga ", Book.unicodeChars["Raga"] + _space
            ).replace("Mela ", Book.unicodeChars["Mela"] + _space)
        return ragaName

    @classmethod
    def makeMelaIndexes(cls) -> [int]:
        # these subChange numbers start at 1, not 0. Change 1 = Root
        indexes = []
        indexes.insert(0, False)
        indexes.insert(1, 1126)
        indexes.insert(2, 1127)
        indexes.insert(3, 1128)
        indexes.insert(4, 1129)
        indexes.insert(5, 1130)
        indexes.insert(6, 1131)
        indexes.insert(7, 1196)
        indexes.insert(8, 1197)
        indexes.insert(9, 1198)
        indexes.insert(10, 1199)
        indexes.insert(11, 1200)
        indexes.insert(12, 1201)
        indexes.insert(13, 1231)
        indexes.insert(14, 1232)
        indexes.insert(15, 1233)
        indexes.insert(16, 1234)
        indexes.insert(17, 1235)
        indexes.insert(18, 1236)
        indexes.insert(19, 1322)
        indexes.insert(20, 1323)
        indexes.insert(21, 1324)
        indexes.insert(22, 1325)
        indexes.insert(23, 1326)
        indexes.insert(24, 1327)
        indexes.insert(25, 1357)
        indexes.insert(26, 1358)
        indexes.insert(27, 1359)
        indexes.insert(28, 1360)
        indexes.insert(29, 1361)
        indexes.insert(30, 1362)
        indexes.insert(31, 1413)
        indexes.insert(32, 1414)
        indexes.insert(33, 1415)
        indexes.insert(34, 1416)
        indexes.insert(35, 1417)
        indexes.insert(36, 1418)
        indexes.insert(37, 1136)
        indexes.insert(38, 1137)
        indexes.insert(39, 1138)
        indexes.insert(40, 1139)
        indexes.insert(41, 1140)
        indexes.insert(42, 1141)
        indexes.insert(43, 1206)
        indexes.insert(44, 1207)
        indexes.insert(45, 1208)
        indexes.insert(46, 1209)
        indexes.insert(47, 1210)
        indexes.insert(48, 1211)
        indexes.insert(49, 1241)
        indexes.insert(50, 1242)
        indexes.insert(51, 1243)
        indexes.insert(52, 1244)
        indexes.insert(53, 1245)
        indexes.insert(54, 1246)
        indexes.insert(55, 1332)
        indexes.insert(56, 1333)
        indexes.insert(57, 1334)
        indexes.insert(58, 1335)
        indexes.insert(59, 1336)
        indexes.insert(60, 1337)
        indexes.insert(61, 1367)
        indexes.insert(62, 1368)
        indexes.insert(63, 1369)
        indexes.insert(64, 1370)
        indexes.insert(65, 1371)
        indexes.insert(66, 1372)
        indexes.insert(67, 1423)
        indexes.insert(68, 1424)
        indexes.insert(69, 1425)
        indexes.insert(70, 1426)
        indexes.insert(71, 1427)
        indexes.insert(72, 1428)
        return indexes

    @classmethod
    def getMelaIndexesFromScaleNames(cls, showDebug=False) -> [int]:
        # This wasn't working so fuck it
        _melaIndexes = []
        for m, mela in enumerate(cls.melaNameByMelaNumber[1:]):
            print(mela)
            _melaFound = False
            for i in range(2048):
                melaOptions = mela.split(",")
                for melaOption in melaOptions:
                    if melaOption in ScaleNames.namesBySequenceIndex[i]:
                        _melaFound = True
                        cls.pageFromMelaNumber.append(i)
                        break
                    else:
                        pass
                if _melaFound == True:
                    _melaIndexes.append(i)
                    Raga.pageFromMelaNumber.append(i)
            if not _melaFound:
                # print(Change.makeFromCarnaticNotation(input('Enter the carnatic notation: ')))
                raise TypeError(
                    mela + " not found in ScaleNames.namesBySequenceIndex\n"
                )
        if showDebug:
            print("here is Raga.pageFromMelaNumber: {}".format(Raga.pageFromMelaNumber))
        return _melaIndexes
Raga.pageFromMelaNumber = Raga.makeMelaIndexes()