from __future__ import annotations, print_function
from collections.abc import Mapping
from JazzNote import JazzNote
from Change import Change
from Latex import Latex
from Project import Project
from Utility import Utility
from tqdm import tqdm
import itertools
input = Utility.input
print = Utility.print
def f(n):
	return 'from .{} import {}'.format(n,n)
print(f('Project'))
import os




#input('here in Book')
class Book(Mapping):
    """From a Change create a sequence of all possible combinations
    other than keeping some note[s] static.

    Keyword arguments:
    notesToUse -- These are the notes to recombine
    notesToInclude -- These are the notes to keep in every set

    Internal variables:
    self.sequence =

    if notesToInclude == '1' and noteToUse = '1,2,3,4:
    self.sequenceNumber = [[1],[1,2],[1,3],[1,4],[1,2,3],[1,2,4],[1,2,3,4]]
    except that they are Change (s) of those values
    """

    # Specify in sharps to make sure that enharmonics are grouped together
    # Flat keys will make the enharmonic tie have on result at the top and one at the bottom

    rootIsChangeOneForIndexing = True
    #directory = os.path.join(Project.directory, "The Way Of Changes\\")
    makePrimes = 0 #Have to keep this on for now
    rootColourKey = "C"
    charsLimitPerLine = 80
    kernEvenPagesLeft = False
    colourTranspose = JazzNote.distanceFromC(rootColourKey)
    beSlowAndThourough = True
    cachedWays = {}
    if beSlowAndThourough:
        Latex.numberOfCells = 15
    # This one uses root is subChange 1
    changesForBeginners = [
        1,
        8,
        27,
        34,
        35,
        42,
        43,
        48,
        154,
        164,
        165,
        169,
        170,
        189,
        190,
        191,
        1191,
        1197,
        1323,
        1233,
        1324,
        1325,
        1360,
        1361,
        1371,
        1326,
        393,
        465,
        785,
        1739,
        1636,
        1171,
        936,
        1333,
        1334,
        1370,
        849,
        1358,
        2048,
        1735,
        1736,
        1766,
        1764,
    ]
    changesBeingPlatonic = [1, 7, 43, 164, 849, 2048]
    changesForBeginners.sort()
    validWays = [
        "Change Number",
        "Chapter Page",
        "Mode Chapter Page",
        "Mode Info",
        "Unique Change Number",
        "Instrument Graphics",
    ]
    validWays += [
        (n + " Keys Diagram")
        for n in ("Piano", "Guitar", "Accordion FCircle Guitar Piano")
    ]

    carnaticWays = [
        "Mneumonic",
        "Notation",
        "Swara",
        "North Indian Sargam",
        "South Indian Sargam",
        "Carnatic",
    ]
    # input(validWays)
    tShirtWays = ["Hexagram Name", "Hexagram Symbol"]
    titleWays = [
        "Book Page",
        "Right Align",
        "Bitmap",
        "Right Align",
        "Main Scale Name",
        "Mela Number",
        "Right Align",
        "Chord Quality",
        "Right Align",
        "Ring Number",
        "Right Align",
        "Unique Change Number",
        "Right Align",
        "Word",
        "Line Break",
        "Other Names",
    ]  # "Scale Name",
    moreTitleWays = [
        "Line Break",
        "Hexagram",
        "Right Align",
        "Line Break",
        "Tetragram",
        "Line Break",
        "Trigram",
        "Line Break",
        "Info",
        "Condensed Info"
    ]
    if not makePrimes:
        # titleWays = titleWays + ['Unique Change Number']
        # Change.infoWaySymbols['Unique Change Number'] = 'P'
        # Get rid of right align
        # titleWays.remove(titleWays[titleWays.index('Unique Change Number')-1])
        titleWays.remove("Unique Change Number")

    # 'Scale Name', was at the beginning
    printWays = [
        "Jazz",
        "Distinct Chord 1",
        "Distinct Chord Word 1",
        "Distinct Chord Change Number 1",
        "Set",
        "Step",
        "Rhythm",
        "Line Break",
        "Classical",
        "Distinct Chord 2",
        "Distinct Chord Word 2",
        "Distinct Chord Change Number 2",
        "Line Break",
        "Chord Quality",
        "Line Break",
        "Efficient",
        "Line Break",
        "Mode Name",
        "Mode Jazz",
        "Mode Quality",
        "Mode Primeness",
        "Mode Hexagram",
        "Mode Word",
        "Mode Change Number",
        "Line Break",
        "Remove Note",
        "Changed Note Hexagram",
        "Changed Note Word",
        "Changed Note Page",
        "Add Note",
        "Poem",
        "Solfege",
        "Carnatic",
        "Notation",
        "Mneumonic",
        "Raga",
        "Reverse",
        "Inverse",
        "Tritone Sub",
        "Hexagram Story",
    ]  # 'Guitar Keys Diagram', 'Instrument Graphics'# #  #'Chord Page', Taken out because pointless now with distinct chord replacing it

    musicFontWays = ["Jazz"]
    pageCreatingWays = ["Instrument Graphics"]
    """ #V.9 OF GRAIL OF SCALE VALUES
    tableOfContentsLabelWays = ['Main Scale Name','Mela Number','Tab To 0.24','Jazz','Tab To 0.52','Chord Quality', 'Line Break',
                                     'Hexagram Name','Tab To 0.18','Hexagram Symbol', 'Tab To 0.23', 'Bitmap','Tab To 0.41','Braille','Tab To 0.45','Word','Tab To 0.53','Hexagram Subpage','Tab To 0.64', 'Unique Change Number','Primeness'
                                     ]
    """
    tableOfContentsLabelWays = [
        "Main Scale Name",
        "Mela Number",
        "Tab To 0.26",
        "Jazz",
        "Tab To 0.55",
        "Chord Quality",
        "Line Break",
        "Hexagram Name",
        "Tab To 0.19",
        "Hexagram Symbol",
        "Tab To 0.26",
        "Bitmap",
        "Tab To 0.48",
        "Braille",
        "Tab To 0.55",
        "Word",
        "Tab To 0.65",
        "Unique Change Number",
        "Primeness",
    ]
    if not makePrimes:
        tableOfContentsLabelWays.remove("Unique Change Number")
        tableOfContentsLabelWays.remove("Primeness")
    colouredWaysSpecific = [
        "Hexagram",
        "Hexagram Symbol",
        "Mode Jazz",
        "Mode Hexagram",
        "Mode Info",
        "Add Note",
        "Word",
        "Mode Hexagram",
    ]
    colouredWaysSpecific += ["Distinct Chord Word " + str(i) for i in range(1, 10)]
    colouredWaysPositional = [
                                 "Jazz",
                                 "Chord",
                                 "Third Chord 9ths",
                                 "Classical",
                                 "Solfege",
                                 "Set",
                                 "Chord Page",
                                 "Mode Name",
                                 "Mode Change Number",
                                 "Mode Quality",
                                 "Mode Primeness",
                                 "Poem",
                                 "Remove Note",
                                 "Zodiac",
                             ] + carnaticWays
    colouredWaysPositional += ["Distinct Chord " + str(i) for i in range(1, 10)]
    colouredWaysPositional += [
        "Distinct Chord Change Number " + str(i) for i in range(1, 10)
    ]

    SmallCircleWays = ["Book Page", "Mode Change Number"]
    # 'Tab To 0.12','Word',
    '''condensedWays = [
        "Tab To 0.00",
        "Change Number",
        "Tab To 0.16",
        "Jazz",
        "Tab To .6",
        "Scale Name",
        "Line Break",
        "Tab To 0.00",
        "Hexagram Symbol Name",
        "Tab To 0.50",
        "Word",
        "Tab To 0.64",
        "Chord Quality",
        "Line Break",
        "Distinct Chord 1",  # Line Break MUST before Distinct Chord or it will fuck up

    ]'''
    condensedWaysModeFamily = [
        # "Tab To 0.00",
        'Unique Change Number', '\\hfill ',

        'Condensed Info', '\\hfill ', 'Prime Enantiomorph', '\\hfill ', 'Prime Inverse',
        "Mode Family",
    ]

    condensedWays = [
        "Tab To 0.00",
        "Change Number",
        "\\hfill",
        "Jazz",
        "\\hfill",
        "Scale Name",
        "\\hfill ",
        "Chord Quality",
        "Line Break",
        "Tab To 0.00",
        "Hexagram Symbol Name",
        "\\hfill",
        "Word",
        "\\hfill",
        "C",
        "Line Break",
        "Distinct Chord 1",  # Line Break MUST before Distinct Chord or it will fuck up
        "Line Break", "Distinct Chord Piano 1",
        "Graphics Banner"
    ]

    condensedTableOfContentsWays = [
        "Book Page",
        "Chord Quality",
        "Tab To 0.5",
        "Scale Name",
        'Line Break'
    ]
    oneLineWays = ["Prime", "Reverse", "Enantiomorph", "Inverse", "Tritone Sub"]
    oneLineWaysConditional = []

    tabularWays = carnaticWays + [
        "Mode Change Number",
        "Mode Chapter Page",
        "Mode Info",
        "Mode Name",
        "Mode Jazz",
        "Mode Word",
        "Jazz",
        "Chord",
        "Classical",
        "Solfege",
        "Set",
        "Carnatic",
        "Notation",
        "Mneumonic",
        "Chord Page",
        "Third Chord 9ths",
        "Step",
        "Mode Change Number",
        "Mode Quality",
        "Mode Hexagram",
        "Mode Primeness",
        "Poem",
        "Random Poem",
        "Step",
        "Rhythm",
        "Spectra",
        "Remove Note",
        "Add Note",
        "Changed Note",
        "Changed Note Page",
        "Changed Note Hexagram",
        "Changed Note Info",
        "Changed Note Word",
    ]
    tabularWays += ["Distinct Chord " + str(i) for i in range(1, 10)]
    tabularWays += ["Distinct Chord Change Number " + str(i) for i in range(1, 10)]
    tabularWays += [
        "Distinct Chord Normalised Change Number" + str(i) for i in range(1, 10)
    ]

    tabularWays += ["Distinct Chord Word " + str(i) for i in range(1, 10)]
    waysToForceIntoOneLine = ["Changed Note Page"]
    specificPositionalWays = [
        "Add Note",
        "Changed Note",
        "Changed Note Page",
        "Changed Note Hexagram",
        "Changed Note Info",
        "Changed Note Word",
    ]

    # centredWays = ['Step','Rhythm']
    centredWays = ["Step", "Rhythm"]

    nonTitlePrintingWays = ["Efficient", "Hexagram Story", "Raga", "Line Break"]
    unicodeChars = {
        "Natural": "♮",
        "Flat": "♭",
        "Sharp": "♯",
        "Double Flat": "𝄫",
        "Double Sharp": "𝄪",
        "minor chord": "-",
        "augmented chord": "+",
        "diminished chord": "⚬",
        "half diminished chord": "⌀",
        "Major Seventh Triangle": "Δ",
        "Whole Note": "𝅝",
        "Half Note": "𝅗𝅥",
        "Quarter Note": "♩",
        "Eighth Note": "♪",
        "Whole Rest": "𝄻",
        "Half Rest": "𝄼",
        "Quarter Rest": "𝄽",
        "Eighth Rest": "𝄾",
        "Way Seperator": ". ",
        "Chinese Seperator": "。",
        "Diad": "◐",
        "Triad": "△",
        "Tetrad": "◇",
        "Pentad": "⬠",
        "Sextad": "⬡",
        "Septad": "✷",
        "Change Number": "⭘",
        "Chapter Number": "🗋",
        "Chapter Change Number": "",
        "Unique Change Number": "❄",
        "Unique Chapter Change Number": '🙉',
        "Index Number": "№",
        "Ring Number": "□",  # 💻
        "Tritone Sub": "⇅",
        "Ascending": "🠥",
        "Descending": "🠧",
        "Braille": "⣿",
        "Binary True": "▣",
        "Binary False": "◻",
        "Key": "🗝",
        "Key Lock": "🔐",
        "Lock": "🔒",
        "Piano": "🎹",
        "Keyboard": "🎘",
        "Mode": "↻",
        "Normalise": "⭳",
        "Wheel": "☸",
        "Abacus": "🧮",
        "Chord": "⦻",
        "Quartal Chord": "➿",
        "Triadic Chord": "➰",
        "Helix": "☤",
        "Step": "±",
        "Treble Clef": "𝄞",
        "Home": "🏠",
        "Hexagram": "卦",
        "Hexagram Chinese": "卦",
        "Tetragram Chinese": "首",
        "Trigram Chinese": "卦",
        "Hexagram Subpage": "🗎",
        "Trigram Subpage": "🗎",
        "Tetragram Subpage": "🗎",
        "Add Note": "+",
        "Remove Note": "-",
        "No Note": "№ ",
        "Mela": "🎪",
        "Raga": "🌈",
        "Word": "🗨",
        "IChing Chinese": "易經",
        "twelve o’clock": "🕛",
        "twelve-thirty": "🕧",
        "one o’clock": "🕐",
        "one-thirty": "🕜",
        "two o’clock": "🕑",
        "two-thirty": "🕝",
        "three o’clock": "🕒",
        "three-thirty": "🕞",
        "four o’clock": "🕓",
        "four-thirty": "🕟",
        "five o’clock": "🕔",
        "five-thirty": "🕠",
        "six o’clock": "🕕",
        "six-thirty": "🕡",
        "seven o’clock": "🕖",
        "seven-thirty": "🕢",
        "eight o’clock": "🕗",
        "eight-thirty": "🕣",
        "nine o’clock": "🕘",
        "nine-thirty": "🕤",
        "ten o’clock": "🕙",
        "ten-thirty": "🕥",
        "eleven o’clock": "🕚",
        "eleven-thirty": "🕦",
        'yin-yang': '☯',
        'giraffe': '🦒'
    }

    unicodeChars["Changed Note"] = (
            unicodeChars["Add Note"] + "/" + unicodeChars["Remove Note"]
    )
    # 🎨 ⌗ » Mela: 🎪⛺ italian🍎 🗍 🗘 ⟳
    # 🔄 🔑 🖽 💻 🖣 🖢 🕮 Power:⏻ Toggle Power:⏼ Power On:⏽ Power Off:⭘ ⏾ 🖳🖰
    """Mela(Sanskrit: मेला) is a
    Sanskrit
    word
    meaning
    'gathering' or 'to meet' or a
    'fair'.It is used in the
    Indian
    subcontinent
    for all sizes of gatherings and can be religious, commercial, cultural or sport-related."""
    # 🜨⊕ ﹣⃠    ⅋ ∪
    """'Mode Name':'Mode '+unicodeChars['Mode'],
                        'Mode Jazz':unicodeChars['Mode']+' Jazz',
                        'Mode Qua᪾lity':unicodeChars['Mode']+' Quality',"""

    wayNameSubs = {
        "Mode ": unicodeChars["Mode"],
        "Solfege": "Solfège",
        "Third Chord 9ths": "9th " + unicodeChars["Chord"],
        "Chord": unicodeChars["Chord"],
        "Tritone": unicodeChars["Tritone Sub"],
        "Change Number": unicodeChars["Change Number"],
        "Changed Note": unicodeChars["Changed Note"],
        "Add Note": unicodeChars["Add Note"] + " Note",
        "Remove Note": unicodeChars["Remove Note"] + " Note",
        "Hexagram": unicodeChars["Hexagram"],
        "Classical": "Roman",
        "Primeness": Change.infoWaySymbols["Primeness"],
        "Quality": unicodeChars["Triadic Chord"] + "/" + unicodeChars["Quartal Chord"],
        "Mneumonic": unicodeChars["Raga"] + "Solfège",
        "Diad": unicodeChars["Diad"],
        "Triad": unicodeChars["Triad"],
        "Tetrad": unicodeChars["Tetrad"],
        "Pentad": unicodeChars["Pentad"],
        "7th": unicodeChars["Tetrad"],
        "9th": unicodeChars["Pentad"],
        "Random Poem": "Rando",
        "Word": unicodeChars["Word"],
    }

    # ◻ ◼ 🗌 ☝ ☟ ☖ ☗ ⬚ ⮾ 🖻 🗏 ☯ 🗌 ☯ ▣

    prependingChars = [
        unicodeChars["Change Number"],
        unicodeChars["Chapter Number"],
        unicodeChars["Chapter Change Number"],
        unicodeChars["Index Number"],
        unicodeChars["Flat"],
        unicodeChars["Sharp"],
    ]
    # http: // phrontistery.info / numbers.html
    # monad dyad triad tetrad pentad hexad heptad octad ennead decad(e) *hendecad dodecad(e)
    chapterHeadings = [
        "Nihilistic Finales. Nonad, a.k.a \\enquote{Silence}",
        "Single Unary Solos. The Monads, a.k.a \\enquote{A Note}",
        "Double Binary Duets. Bitonic Dyads, a.k.a \\enquote{Double Stops}",
        "Triple Ternary Trios. Tritonic Triads, a.k.a \\enquote{Chords}",
        "Quadruple Quaternary Quartets. Tetratonic Tetrads, a.k.a \\enquote{Seventh Chords}",
        "Pentads: Quintuple Quinquenary Quintets.",
        "Six-Note Hexads: Sextuple Senary Sextets. (they're Sextatonic)",
        "Seven-Note Heptads: Septuple Septenary Septets.",
        "Octonary Octets. Octads",
        "Nonary Nonets. Enneads Nantatonic",
        "Denary Dectets. Decads",
        "Undenary Undectetss. Hendecads",
        "Duodenary Duodectets. Dodecads a.k.a \\enquote{Chromatic}",
    ]
    # unus
    """duo
    tres, tria
    quattuor
    quinque
    sex
    septem
    octo
    novem
    decem
    undecim
    duodecim"""

    # Book/Page symbols 🗌 🗋 🗍 🖻 📗 📘 📖 📕 📔 📓 📒 📑 📂 📁 📋 📋 📝 📚 📒 📃 📄  🗎 🗏 🗐 🗒 🗓 🗔
    # Arrows: ⭚ ⭛ ⭜ ⭝ ⭞ ⭟ ⭠ ⭡ ⭢ ⭣ ⭤ ⭦ ⭥ ⭦ ⭧ ⭨ ⭩ ⭪ ⭫ ⭬ ⭭ ⭮ ⭯ ⭰ ⭱ ⭲ ⭳ ⭶ ⭷ ⭸ ⭹ ⭺ ⭻ ⭼ ⭽ ⭾ ⭿ ⮀
    # ⮁ ⮂ ⮃ ⮄ ⮅ ⮆ ⮇ ⮈ ⮉ ⮊ ⮋ ⮌ ⮍ ⮎ ⮏ ⮐ ⮑ ⮒ ⮓ ⮔ ⮕ ⮘ ⮙ ⮚ ⮛ ⮜ ⮝ ⮞ ⮟ ⮠ ⮡ ⮢ ⮣ ⮤ ⮥ ⮦ ⮧ ⮨ ⮩ ⮪ ⮫ ⮬⮭
    # ⮮ ⮯ ⮰ ⮱ ⮲ ⮳ ⮴ ⮵ ⮶ ⮷ ⮸
    # binary indicators: ☑☒ ■□ ◻◼
    # Astrological signs: ♈     ♉      ♊      ♋      ♌   ♍     ♎     ♏       ♐           ♑         ♒        ♓
    #                    Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces
    #                    0     1      2      3      4   5     6     7       8           9         10       11

    # Shapes with n sides ❍⚪⚬⚫🌢 🌙❘❙❚ ⛛ ⯁⯀❏❐❑❒ ⯂⬟⬠☖☗⛉⛊ ⬡⬢⬣⯃ ⛫ ⯄ ✩✪✫✬✭✮✯✰✶✴✵✷✸
    # Shapes with points ✹✺✻✼✽✾✿❀❁❂❃❄❅❆❇❈❉❊❋❌
    # Roman Numerals ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯⅰⅱⅲⅳⅶⅷⅸⅹⅺⅻⅼⅽⅾⅿ
    # Hand signals ☚ ☛ ☜ ☝ ☞ ☟ ✊ ✋ ✌ ✍
    # Notes 𝅝𝅗𝅥𝅘𝅥𝅘𝅥𝅮𝅘𝅥𝅯𝅘𝅥𝅰𝅘𝅥𝅱𝅘𝅥𝅲𝄺𝄻𝄼𝄽𝄾𝄿𝅀𝅁𝅂
    #      ♩♪♫♬♭♮♯
    # Misc №⁺₊

    # ☯⇅🗘
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

    def __init__(
            self,
            notesToUse=["1", "b2", "2", "b3", "3", "4", "b5", "5", "b6", "6", "b7", "7"],
            notesToInclude=["1"],
            showDebug=False,
    ):

        self.sequence = [Change(notesToInclude)]
        self.sequenceByLength = []
        self.sequenceIndexByLengthIndex = []
        self.sequenceLengthRanges = []
        self.sequencePrimes = []
        self.sequencePrimesByLength = []

        # for i in range(len(notesToInclude)):
        # 	self.sequenceByLength.append([])
        # 	print('times that it tried to extend the empty space i: ',i)
        for i in range(len(notesToInclude)):
            self.sequenceByLength.append([])
            self.sequenceIndexByLengthIndex.append([])
        self.sequenceByLength.append([Change(notesToInclude)])
        self.sequenceIndexByLengthIndex.append([0])
        self.sequenceLengthRanges.append({"start": -1, "end": -1})
        self.sequenceLengthRanges.insert(len(notesToInclude), {"start": 0, "end": 0})

        _notesToCombine = []
        for (
                i
        ) in (
                notesToUse
        ):  # Gets rid of notes that won't change, for combination to only affect changing ones
            if not (i in notesToInclude):
                _notesToCombine.append(i)
        print(
            "notes to include, use, combine, ",
            notesToInclude,
            notesToUse,
            _notesToCombine,
        )
        print("building scales ", end="")
        if Book.makePrimes or Project.makingFinalCopies:
            makePrimes = True
            print("and getting primes...")
            self.sequencePrimes.append(Change([]))
            self.sequencePrimes.append(Change(notesToInclude))
            self.sequencePrimesByLength = [[Change([])], [Change(notesToInclude)]]
        else:
            makePrimes = False
            print("while ignoring primes...")

        _counter = 0
        _primeCounter = 0
        for combinationLength in tqdm(range(1, len(_notesToCombine) + 1)):

            _actualCombinationLength = combinationLength + len(notesToInclude)
            self.sequenceLengthRanges.insert(
                _actualCombinationLength, {"start": _counter + 1}
            )
            self.sequenceByLength.insert(_actualCombinationLength, [])
            self.sequenceIndexByLengthIndex.insert(_actualCombinationLength, [])
            self.sequencePrimesByLength.insert(_actualCombinationLength, [])

            for thisCombination in itertools.combinations(
                    _notesToCombine, combinationLength
            ):

                _thisCombinationWithIncludedNotes = Change(
                    notesToInclude + list(thisCombination)
                ).sortBySemitonePosition()

                self.sequence.append(_thisCombinationWithIncludedNotes)
                # If this one is a prime scale
                if makePrimes and _thisCombinationWithIncludedNotes.byWays("Is Prime"):
                    self.sequencePrimes.append(_thisCombinationWithIncludedNotes)
                    self.sequencePrimesByLength[-1].append(
                        _thisCombinationWithIncludedNotes
                    )
                    # TODO: mirror that sequenceIndexByLengthIndex for primes and rename cause it's confusing ;/
                    # print('this combo',_thisCombinationWithIncludedNotes,type(_thisCombinationWithIncludedNotes),'seems like its prime, in other words',Change(_thisCombinationWithIncludedNotes))
                self.sequenceByLength[-1].append(_thisCombinationWithIncludedNotes)

                self.sequenceIndexByLengthIndex[-1].append(_counter + 1)
                _counter += 1
                # print('inside LevesqueIndex',_thisCombinationWithIncludedNotes,_counter)
            self.sequenceLengthRanges[-1]["end"] = _counter

            if showDebug:
                print(
                    _actualCombinationLength,
                    _counter,
                    _thisCombinationWithIncludedNotes,
                )
        if showDebug:
            print("sequenceLengthRanges: ", self.sequenceLengthRanges)
        _lastPageNumber = False
        """print(
            'primes for notes {}:\n{}\n thems the primes. There were {} of em.'.format(
                notesToUse, self.sequencePrimes,
                len(self.sequencePrimes)))"""
        if len(self.sequencePrimes) > 0:
            print("and the primes are:")
        else:
            print("skipped making primes because Book.makePrimes == False")
        for idx, i in enumerate(self.sequencePrimes):
            print(idx, i, i.getChangeNumber(addOneToBookPage=True), end=" ")
            if showDebug:
                if _lastPageNumber:
                    print(
                        "the distance since last: ",
                        i.getChangeNumber(decorateChapter=False) - _lastPageNumber,
                    )
                else:
                    print()
                _lastPageNumber = i.getChangeNumber(decorateChapter=False)
        if makePrimes:
            print(
                "that concludes the generation and derivation of primes for this book.", end=' '
            )
        else:
            print("that concludes the generation of the book.", end=' ')
        print("\nnotesToUse: {}".format(notesToUse))
        # print(self.sequencePrimesByLength)

    def __len__(self):
        # return len(self.sequence)
        return len(self.sequence)

    linesWhereGetItemHappened = []

    def __getitem__(self, item) -> Change:
        rootIsChangeOne = self.rootIsChangeOneForIndexing
        #add import inspect and stuff if enabling, (to requirements)
        '''frameinfo = getframeinfo(currentframe())
        frameinfoEnc = inspect.stack()[1][2]
        if frameinfoEnc not in Book.linesWhereGetItemHappened:
            Book.linesWhereGetItemHappened.append(frameinfoEnc)'''
        # print(traceback.print_stack(),end='\n\n')
        # print('Gonna change these {} fram {} ln {}. \nin {}'.format(frameinfo,frameinfo.filename, frameinfo.lineno,frameinfoEnc))

        # input('Gonna change these')
        if rootIsChangeOne:
            if type(item) is int:
                pass
            else:
                raise TypeError(
                    "indexing expects int, not type {} for {}".format(type(item), item)
                )
            if abs(item) <= len(self.sequence):
                pass
            else:
                raise IndexError(
                    "{} exceeds the bounds ({}) of this book. {}".format(
                        item, len(self), self
                    )
                )
            if item == 0:
                return Change([])
            elif item > 0:
                return self.sequence[item - 1]
            elif item < 0:
                return self.sequence[-item - 1].withoutNote("1")

        else:
            if type(item) is int:
                if item < 2048 and item > -2048:
                    pass
                else:
                    raise IndexError(
                        "Book.rootIsChangeOneForIndexing ==",
                        Book.rootIsChangeOneForIndexing,
                        "therefore specify indexes between -2047 and +2047",
                    )
            if type(item) is int and item >= 0:
                # Item is positive or 0
                return self.sequence[item]
            elif item == "None":
                return Change([])
            elif item == 0:
                return Change([])
            else:
                # Item is negative
                return self.sequence[-item].withoutNote("1")

    def __iter__(self):
        """if Book.rootIsChangeOneForIndexing:
            self.num = -1 * len(self.sequence)
        else:
            self.num = -1 * (len(self.sequence) - 1)
        return self"""
        if self.rootIsChangeOneForIndexing:
            self.num = -1 * len(self.sequence)
        else:
            self.num = -1 * (len(self.sequence) - 1)
        return self

    def __next__(self):
        self.num = num = self.num
        if num == -1 and self.rootIsChangeOneForIndexing:
            self.num += 2
        else:
            self.num += 1
        try:
            self[num]
        except IndexError:
            raise StopIteration()
        return self[num]

    def getAllDistinctScaleChords(self, chordTypes=[0]):
        try:
            return self.allDistinctScaleChords[tuple(chordTypes)]
        except Exception as e:
            pass
        distinctChords = []
        print('starting to calculate totl distinct chords')
        for i in tqdm(range(2049)):
            change = self[i]
            for n in range(len(change)):
                for chordType in chordTypes:
                    distinctChords.append(
                        change.getDistinctScaleChord(n, chordType, returnChordQuality=False).getChangeNumber())
        try:
            self.allDistinctScaleChords

        except:
            self.allDistinctScaleChords = {}
        self.allDistinctScaleChords[tuple(chordTypes)] = list(set(distinctChords))
        self.allDistinctScaleChords[tuple(chordTypes)].sort()
        return self.allDistinctScaleChords[tuple(chordTypes)]

    def addPageToTableOfContents(
            self,
            change: Change,
            captionType="figure",
            ways=None,
            includeSheetNumber=False,
            replaceSheetNumber=True,
            replaceSheetNumberWithWays=["Book Page"],
            linkInPdfBookmarks=True,
            externalGraphicsPath=False,
            renderIfNotFound=False,
    ):
        _validCaptionTypes = (
            "figure",
            "chapter",
            "section",
            "subsection",
            "subsubsection",
            "table",
        )
        if captionType not in _validCaptionTypes:
            raise ValueError("{} not in {}".format(captionType, _validCaptionTypes))
        if captionType in ("chapter", "section", "subsection", "subsubsection"):
            _captionContainer = "toc"
        elif captionType in ("figure", "table"):
            _captionContainer = "lof"
        _captionTypeCommandStr = "{" + _captionContainer + "}{" + captionType + "}"
        if ways == None:
            ways = Book.tableOfContentsLabelWays
        _pageTitle = self.getTitle(
            # _change, Book.tableOfContentsLabelWays,protectCommands=True,seperator='\\hfill ')
            change,
            ways,
            protectCommands=True,
            seperator=" ",
            externalGraphicsPath=externalGraphicsPath,
            renderIfNotFound=renderIfNotFound,
        )
        _str = ""
        # input('_pageTitle is:\n'+_pageTitle)
        # _pageStr += '\\caption{' + self.getTitle(_change,Book.tableOfContentsLabelWays) + '}'+ '\n'

        # _captionStr = '\\caption{' + _pageTitle + '}'+ '\n'
        # This was what I just just using
        _captionStr = "\\captionlistentry[" + captionType + "]{" + _pageTitle + "}"

        indexNumber = change.getChangeNumber()
        if (
                (indexNumber % 2 == 1 and indexNumber >= 0)
                or (indexNumber % 2 == 0 and indexNumber < 0)
        ) or Book.kernEvenPagesLeft == False:  # == 1 if we're moving right, ==0 if moving text left
            # _kernEvenPagesLeft='\\protect\\space '
            _kernEvenPagesLeft = "\\hspace*{-1.5cm}"
            # _kernEvenPagesLeft = '\\noindent'
            # _kernEvenPagesLeft= '\\indent'
            # _kernEvenPagesLeft = '\\protect\\kern -4em'
        else:
            _kernEvenPagesLeft = "\\hspace*{-0.75cm}"
        # if _kernEvenPagesLeft != '':input(_pageTitle+'frozen in time')
        _pageTitle = _kernEvenPagesLeft + _pageTitle.replace(
            "protect\\\\\n", "protect\\\\\n" + _kernEvenPagesLeft
        )
        # if _kernEvenPagesLeft != '':input(str(_pageTitle)+'Here is it')
        # _str = '\\addcontentsline'+_captionTypeCommandStr+'{' + _pageTitle + '}%\n'
        # _pageStr += '\\cftaddtitleline{lof}{figure}{'+_pageTitle+'}{'+self.getTitle(_change,ways=['Book Page'],)+'}'
        # input(_pageTitle)
        # This was also what I was just using
        _str = (
                "\\cftaddnumtitleline"
                + _captionTypeCommandStr
                + "{\\protect\\numberline{}}{"
                + _pageTitle
                + "}"
        )
        # _str = '\\phantomsection\\addcontentsline'+_captionTypeCommandStr+'{'+_pageTitle+'}'

        if "cftaddnumtitleline" in _str:
            if replaceSheetNumber:
                _str += (
                        "{"
                        + self.getTitle(
                    change,
                    ways=replaceSheetNumberWithWays,
                )
                        + "}"
                )
            else:
                _str += "{\\thepage}"
        # _str =  '\\cftaddtitleline'+_captionTypeCommandStr+'{\\protect\\numberline{}}{'+_pageTitle+'}'
        # This needs to use \\ for line breaks, not \\[-.1\baselineskip]
        for command in (
                "Line Break",
                "Line Break With Space",
                "Line Break",
                "Line Break Small",
        ):
            _str = _str.replace(
                Latex.commandStrings[command], "\\\\\n\\noindent " + _kernEvenPagesLeft
            )
        if linkInPdfBookmarks:
            _str += change.makePdfLink()
        print("the string")

        return _str

    def sortChanges(
            self, changes: [Changes], sortByWays: [len], sortIntoSublistByResult=True
    ):
        print("asdf", Book.isValidWay("Cohemitonia"))
        for i in sortByWays:
            if Book.isValidWay(i):
                pass
            elif hasattr(i, "__call__"):
                pass
            elif i in list(Change.infoWaySymbols):
                pass
            else:
                raise TypeError("not a valid sort {} {}".format(i, type(i)))
        _changesByResult = {}
        _sortedChanges = []
        for sortWay in sortByWays:
            for change in changes:
                if Book.isValidWay(sortWay):
                    _result = change.byWays(sortWay)
                elif sortWay in list(Change.infoWaySymbols):
                    _result = change.byWays(sortWay)
                else:
                    _result = sortWay(change)
                if not _result in _changesByResult:
                    _changesByResult[_result] = []
                _changesByResult[_result].append(change)

            if Book.isValidWay(sortWay) or sortWay in list(Change.infoWaySymbols):
                _changesByResult[_result].sort(key=lambda obj: obj.byWays(sortWay))
            else:
                _changesByResult[_result].sort(key=sortWay)
        _rows = []

        if sortIntoSublistByResult:
            for i in sorted(list(_changesByResult.keys())):
                _rows.append([])
                _rows[-1] = _changesByResult[i]
            return _rows
        else:
            return _changesByResult

    @classmethod
    def makeWayNamePrintable(cls, wayName: str) -> str:
        for sub in Book.wayNameSubs.items():
            wayName = wayName.replace(sub[0], sub[1])
        return wayName

    def getTitle(
            self,
            change: Change,
            ways=[],
            beginningStr="",
            seperator="",
            addOne=1,
            latexCommands=True,
            protectCommands=False,
            externalGraphicsPath=False,
            renderIfNotFound=False,
    ):
        if seperator == None:
            seperator = Book.unicodeChars["Way Seperator"]
        if not isinstance(change, Change):
            raise TypeError(
                "change {} should be type Change, but is type=={}.".format(
                    change, type(change)
                )
            )
        # Fix chapter # and index
        if not change.containsNotes("1"):
            addOne = -1
        _str = ""
        if len(ways) == 0:
            ways = Book.titleWays
        if beginningStr:
            _str += beginningStr

        for way in ways:
            _willPrintSeperator = (
                    ways[min(ways.index(way) + 1, len(ways) - 1)]
                    not in ("Line Break", "Right Align")
                    and ways.index(way) != len(ways) - 1
                    and way != "Line Break"
            )
            # and ways[ways.index(way) - 1] != 'Line Break'
            if way == "Change Number":
                raise TypeError("use book subChange instead")
                _str += Book.unicodeChars["Change Number"] + str(
                    self.getSequenceNumberFromChange(change) + addOne
                )
            if "Tab To " in way:
                _str += Latex.tabTo(way)
            elif way == "Book Page":
                _str += change.getChangeNumber(
                    returnChapterPage=True,
                    includeChapterSymbol=True,
                    decorateWithSmallCircle=Latex.useSmallCircles,
                    externalGraphicsPath=externalGraphicsPath,
                    renderIfNotFound=renderIfNotFound,
                )
                """_str += change.getChangeNumber(addOneToBookPage=True)
                _chapterNumber = str(len(change))
                _str += ' '
                #_str += Book.unicodeChars['Chapter Number']  #
                _isCapital = Change.chordHasUpperCaseNumeral(change.getNormalForm().getChordQuality())
                #if change.byWays('Classical')[0] == change.byWays('Classical')[0].lower():
                if len(change) > 0 and _isCapital:
                    _str += JazzNote(_chapterNumber).getRomanNumeral()
                elif len(change) > 0 and not _isCapital:
                    _str += JazzNote(_chapterNumber).getRomanNumeral().lower()
                else:
                    _str += _chapterNumber
                #_str += Book.unicodeChars["Index Number"]
                _str += ' '

                _indexNumber = self.getIndexNumberInChapterFromChange(change)+addOne
                _str += str(_indexNumber)
                _str += ')'
                """
            elif way == "Unique Change Number":
                _str += change.getUniquePage(chapterNumber=False)

            elif way == 'Unique Chapter Change Number':
                _str += change.getUniquePage(chapterNumber=True)
                print('soggy sock')
                #input(_str)
            elif way == "Primeness":
                _str += str(change.getPrimeness(decorate=True))
            elif way == "Ring Number":
                _str += str(change.getRingNumber(includePreString=True))
            elif way == "Bitmap":
                _str += change.getBitMap()
            elif way == "Right Align":
                _str += seperator
                if latexCommands:
                    if not protectCommands:
                        _str += "\\hfill "
                    else:
                        _str += "\\protect\\hfill "
                    _willPrintSeperator = False
            elif way == "Line Break":
                if latexCommands:
                    if protectCommands == True:
                        _str += "\\protect" + Latex.commandStrings["Line Break"]
                    else:
                        _str += Latex.commandStrings["Line Break"]
            elif way == "Trigram":
                _str += " ".join(
                    change.getTrigram(
                        trigramWays=Trigram.printWays,
                        colourResult=latexCommands,
                        decorateWithSmallCircle=Latex.useSmallCircles,
                        insertStrBetweenSections="\\hfill",
                        externalGraphicsPath=externalGraphicsPath,
                    )
                )
                # _str += '\n'+' '.join(change.getTrigram(trigramWays=Trigram.allowedWays,concatenatePerTrigram=True))
            elif way == "Trigram Symbol":
                _str += "".join(change.getTrigram(trigramWays=["symbol"]))
            elif way == "Tetragram":
                _str += " ".join(
                    change.getTetragram(
                        tetragramWays=Tetragram.allowedWays,
                        colourResult=latexCommands,
                        decorateWithSmallCircle=Latex.useSmallCircles,
                        insertStrBetweenSections="\\hfill",
                        externalGraphicsPath=externalGraphicsPath,
                    )
                )
                # _str += '\n'+' '.join(change.getTetragram(tetragramWays=Tetragram.allowedWays,concatenatePerTetragram=True))
            elif way == "RNA Codon":
                _str += Book.unicodeChars["Helix"] + " ".join(
                    change.getCodon("RNA", colourResult=latexCommands)
                )
            elif way == "DNA Codon":
                _str += Book.unicodeChars["Helix"] + " ".join(
                    change.getCodon("DNA", colourResult=latexCommands)
                )
                _str += Book.unicodeChars["Helix"] + " ".join(
                    change.getCodon(geneType="Both", colourResult=latexCommands)
                )
            elif way == "Jazz":
                # slow version below, switch to if straightening jazz doesnt
                # _str += ' '.join(change.straightenDegrees().byWays('Jazz', colourResult=latexCommands))
                _str += " ".join(change.byWays("Jazz", colourResult=latexCommands))
            elif way == "Hexagram":
                if Latex.on:
                    _str += "".join(
                        change.getHexagram(
                            hexagramWays=Hexagram.titleWays,
                            colourResult=latexCommands,
                            decorateWithSmallCircle=Latex.useSmallCircles,
                            insertStrBetweenSections="\\hfill ",
                            externalGraphicsPath=externalGraphicsPath,
                        )
                    )
                else:
                    _str += "".join(
                        change.getHexagram(
                            hexagramWays=Hexagram.titleWays,
                            colourResult=latexCommands,
                            insertStrBetweenAnswers=None,
                            externalGraphicsPath=externalGraphicsPath,
                        )
                    )

            elif way == "Hexagram Symbol":
                _str += "".join(
                    change.getHexagram(
                        hexagramWays=["symbol"],
                        colourResult=latexCommands,
                        externalGraphicsPath=externalGraphicsPath,
                    )
                )
            elif way == "Hexagram Subpage":
                _str += " ".join(
                    change.getHexagram(
                        hexagramWays=["subpage"],
                        colourResult=latexCommands,
                        externalGraphicsPath=externalGraphicsPath,
                    )
                )
            elif way == "Hexagram Name":
                _str += " ".join(
                    change.getHexagram(
                        hexagramWays=["name"],
                        colourResult=latexCommands,
                        externalGraphicsPath=externalGraphicsPath,
                    )
                )
            elif way == "Word":
                _str += Book.unicodeChars["Word"] + "".join(
                    change.getTrigram(
                        trigramWays=["syllable"], colourResult=latexCommands
                    )
                )
            elif way == "Consonant":
                _str += "".join(change.getConsonant())
            elif way == "Imperfections":
                _str += str(change.getImperfections()) + "🐍"
            elif way == "Chord Quality":
                _str += change.getChordQuality()
            elif way == "Braille":
                _str += "".join(change.getBraille(colourResult=latexCommands))
            elif way == "Moment":
                _str += change.getTimeOfDay()
            elif "Info" in way:
                if "Condensed" in way:
                    _str += " ".join(
                        change.byWays("Info Condensed", )
                    )

                else:
                    _str += " ".join(
                        change.byWays("Info", externalGraphicsPath=externalGraphicsPath)
                    )
            elif way == "Scale Name":
                _scaleNames = change.getScaleNames(
                    searchForDownward=False, searchForNegative=False
                )
                if _scaleNames[0] == change.getHexagramName():
                    _str += ""
                elif _scaleNames[0] == "":
                    pass
                    # _str += '              '
                else:
                    _str += _scaleNames[0]
            elif way == "Zodiac":
                _str += "".join(
                    change.getZodiac(
                        spaceOutBySemitone=False, colourResult=latexCommands
                    )
                )
            elif way == "Main Scale Name":
                if (
                        change.getScaleNames(
                            searchForDownward=False,
                            searchForNegative=False,
                        )[0]
                        == change.getHexagramName()
                ):
                    # _str += change.getScaleNames(searchForDownward=False, searchForNegative=False, )[0]
                    if latexCommands == False:
                        _str += "_" * 10
                    if latexCommands == True:
                        _str += "\\underline{\\hspace*{1.3cm}}"
                        # _str += '\_'*10
                else:
                    _str += (
                            "\\underline{\\smash{"
                            + change.getScaleNames(
                        searchForDownward=False,
                        searchForNegative=False,
                    )[0]
                            + "}}"
                    )

            elif way == "Mela Number":
                if change.getMelaNumber():
                    _str += " " + Book.unicodeChars["Mela"] + change.getMelaNumber()
            elif way in Change.infoWaySymbols.keys():
                _str += change.byWays(way)
            elif way == "Other Names":
                _realName = change.getScaleNames(
                    searchForDownward=False, searchForNegative=False
                )
                if (
                        _realName not in ("", " ")
                        and change.getHexagramName() not in _realName
                ):
                    _names = change.byWays("Names")[1:]
                else:
                    _names = change.byWays("Names")[:]
                if Latex.on:
                    # _namesSeperator = '\\hfill '
                    # this will be replaced after
                    _namesSeperator = ",  "
                else:
                    _namesSeperator = ", "
                _charsLimitPerLine = Book.charsLimitPerLine
                _lineBreak = Latex.commandStrings["Line Break Scale Names"]
                _otherNames = ""
                _charsSoFarThisLine = 0
                for idx, name in enumerate(_names):
                    if Latex.on == True:
                        # TODO: move this into getScaleNames
                        _modifiedName = name.replace(" ", "~")
                        _modifiedName = "{" + _modifiedName + "}"
                    if not Latex.on:
                        raise TypeError("I thought it was alwas online..")
                        _charsSoFarThisLine = len(_str.split("\n")[-1])
                    if _charsSoFarThisLine < _charsLimitPerLine:
                        _otherNames += _modifiedName
                        _charsSoFarThisLine += len(name) + len(_namesSeperator)
                    else:  # linebreak
                        if Latex.on:
                            # input('blooob sofar{} limit{} _str{}'.format(_charsSoFarThisLine,_charsLimitPerLine,_str))
                            if (
                                    idx != len(_names) - 1
                                    and _charsSoFarThisLine > _charsLimitPerLine
                                    and idx != 0
                            ):
                                if protectCommands:
                                    _otherNames += "\\protect"
                                _otherNames += _lineBreak + _modifiedName
                                _charsSoFarThisLine = len(name) + len(_namesSeperator)
                            else:
                                _otherNames += _modifiedName
                                _charsSoFarThisLine = len(name) + len(_namesSeperator)
                        else:
                            _str += "\n" + " " * len(beginningStr) + name
                        # input('lasdt part of subChange:\n{} charsThisLine: {}'.format(_str[-300:],_charsSoFarThisLine))
                    if idx != len(_names) - 1:
                        _otherNames += _namesSeperator
                if not Latex.on == True:
                    _otherNames += "\n"
                else:  # len(_names) != 0:
                    _otherNames += Latex.commandStrings["Line Break Scale Names"]
                # input('\ngrimp: {}\nmaxCharsPerLine: {}'.format(_otherNames,Book.charsLimitPerLine))

                # _otherNames = _otherNames.replace(_namesSeperator,',\\hfill ')
                _str += _otherNames
            else:
                _str += " ".join(self.byMoreWays(change, way))
                raise ValueError(
                    way,
                    "not finished in titleWays. You have to implement it within getTitle().:",
                    Book.titleWays,
                )
            if _willPrintSeperator:
                _str += seperator
        return _str

    def OldgetTitle(
            self,
            change,
            beginningStr="⌗",
            seperator=": ",
            sequenceNumber=True,
            hexagramName=True,
            hexagramSymbol=True,
            otherScaleName=True,
            chapterNumberAndIndex=True,
            chordQuality=True,
            addOne=1,
    ):
        # Fix chapter # and index
        _str = ""
        if beginningStr:
            _str += beginningStr
        if sequenceNumber:
            print(
                "sequence number",
                self.getSequenceNumberFromChange(change) + addOne,
                "change",
                change,
            )
            _str += str(self.getSequenceNumberFromChange(change) + addOne) + seperator
        if chapterNumberAndIndex:
            _chapterNumber = str(len(change))
            if change.byWays("Classical")[0] == change.byWays("Classical")[0].lower():
                _str += JazzNote(_chapterNumber).getRomanNumeral().lower()
            else:
                _str += JazzNote(_chapterNumber).getRomanNumeral()

            _str += "("
            _indexNumber = self.getIndexNumberInChapterFromChange(change) + addOne
            _str += str(_indexNumber)
            _str += ")"
            _str += seperator

        if hexagramSymbol:
            _str += change.getHexagramSymbols() + seperator
        if hexagramName:
            _str += change.getHexagramName() + seperator

        if chordQuality:
            _str += change.getChordQuality()
        if otherScaleName:
            pass  # HERE you will add the part about Ionian Lydian Gypsy Minor names
        return _str

    def getSequenceNumberFromChange(self, change: Change):
        return change.getChangeNumber(decorateChapter=False)

    def getIndexNumberInChapterFromChange(self, change: Change):
        return change.getChangeNumber(False, True, False)

    def modesIndexNumbers(self, change: Change):
        _modeIndexNumbers = []

        for i in range(len(change)):
            _thisMode = change.mode(i)
            _modeIndexNumbers.append(self.getSequenceNumberFromChange(_thisMode))

        return _modeIndexNumbers

    """'@classmethod
    def multiLineFormatOld(cls,inputList, preDataTitle = 'test title:',distanceBetweenAnswers = 4):
        #First find out how many lines
        if type(inputList) != list: inputList = [inputList]
        maxResultLength = len(max(inputList, key=len))
        print('maxResultLength', maxResultLength)
        _lines = 1 + math.floor((maxResultLength + 1)/distanceBetweenAnswers)
        _linesStr = []
        for i in range(_lines): _linesStr.append('')
        for line in range(_lines ):
            if line == 0:
                _linesStr.append(preDataTitle)
                for resultIndex in range(len(inputList)):
                    if resultIndex % _lines == 0:
                        _linesStr[0] += inputList[resultIndex]
                        _linesStr[0] += ' '*(distanceBetweenAnswers - len(inputList[resultIndex]))
                    else:
                        _linesStr[0] += ' '*distanceBetweenAnswers
            else: #Second or third line
                _linesStr[line] = (' '*len(preDataTitle))
                for resultIndex in range(len(inputList)):
                    if ((resultIndex)%_lines == line):
                        _linesStr[line] += inputList[resultIndex]
                        _linesStr[line] += ' '*(distanceBetweenAnswers - len(inputList[resultIndex]))
                        print('abba',resultIndex,line,_lines)
                    else:
                        _linesStr[-1] += ' '*distanceBetweenAnswers
        _outputStr = ''
        for line in _linesStr:
            _outputStr += line + '\n'
        print('inside multiLineFormat _lines',_lines,_linesStr)
        return _outputStr"""

    @classmethod
    def multiLineFormat(
            cls,
            inputList,
            preDataTitle="test title:",
            distanceBetweenAnswers=False,
            titleMinimumLength=12,
    ):
        if not distanceBetweenAnswers:
            distanceBetweenAnswers = 3
        if titleMinimumLength < len(preDataTitle):
            titleMinimumLength = len(preDataTitle)
        # print(titleMinimumLength,'titleMinimumLength')
        # First find out how many lines
        if type(inputList) != list:
            inputList = [str(inputList)]
        for i in range(len(inputList)):
            inputList[i] = str(inputList[i])
        # print('inside multiLineFormat, inputList',inputList)
        maxResultLength = len(max(inputList, key=len))
        maxResultLength = 0

        # print('maxResultLength', maxResultLength)
        # Get this number right and add it to the next one

        # If the string starts with accidentals then we need to subtract the number
        # of accidentals that preceded the longest one from
        # (maxResultLength + 1) which follows this in _lines =
        _numOfPreAccidentals = 0

        _lines = 0 + math.floor((maxResultLength + 1) / distanceBetweenAnswers)
        _linesStr = []
        _linesDataIndexToAdd = []
        # print('holy shit')

        for line in range(1, _lines + 1):
            _linesDataIndexToAdd.append([])
            for index in range(1, len(inputList) + 1):
                # print(index, _lines, line, 'print(index, _lines, line)','index % _lines == line',index % _lines == line)
                if index % _lines == 1:
                    # print(index, _lines, line)
                    _linesDataIndexToAdd[-1].append(index + line - 2)
        # It wasn't doing the last one so do it here
        # print('data',_linesDataIndexToAdd)

        for i in range(_lines):
            _linesStr.append("")
        for line in range(_lines):
            if line == 0:
                _linesStr[line] = preDataTitle
            elif line != _lines:
                _linesStr[line] = " " * len(preDataTitle)
            _linesStr[line] += " " * (titleMinimumLength - len(preDataTitle))
            _linesStr[line] += " " * 0
            # print('title min',titleMinimumLength,'spaces',len(preDataTitle)-titleMinimumLength)
            for resultIndex in range(len(inputList)):
                if resultIndex in _linesDataIndexToAdd[line]:
                    _linesStr[line] += inputList[resultIndex]
                    _linesStr[line] += " " * (
                            distanceBetweenAnswers - len(inputList[resultIndex])
                    )
                elif line != _lines:
                    _linesStr[line] += " " * distanceBetweenAnswers

        _outputStr = ""
        for line in _linesStr:
            _outputStr += line + "\n"
        # print('inside multiLineFormat _lines',_lines,_linesStr)
        print("in multiline, lines:", _lines)
        return _outputStr

    @classmethod
    def renderTitleAndListOfAnswers(
            self,
            inputList=[
                "there's",
                "a",
                "lady",
                "who",
                "knows",
                "all",
                "that",
                "glitters",
                "is",
                "gold",
                "and",
                "she's",
                "buying",
                "a",
                "stairway",
                "to",
                "heaven",
            ],
            title="Stupid Title",
            titleAdjustedLength=3,
            cellSize=6,
            minimumSpaceBetweenItems=0,
            excludeAccidentalsInAlignment=True,
            wayNameSeperator=None,
            prependResultWithStr="",  # ·
            constrainToWidthAndNotAlignToGrid=False,
            constrainToWidth=0,
            latexCommands=False,
    ):
        if wayNameSeperator == None:
            wayNameSeperator = Book.unicodeChars["Way Seperator"]

        if constrainToWidthAndNotAlignToGrid and constrainToWidth == 0:
            raise ValueError(
                "In renderTitleAndListOfAnswers you picked constainToWidthAndNotAlignToGrid but did not specify a constrain width"
            )

        # print('debug',title,wayNameSeperator)
        _titleWithSpace = title + wayNameSeperator
        if len(_titleWithSpace) != titleAdjustedLength:
            _titleWithSpace += " " * minimumSpaceBetweenItems
        if titleAdjustedLength < len(_titleWithSpace):
            titleAdjustedLength = len(_titleWithSpace)  # + len(wayNameSeperator)
        if len(_titleWithSpace) < titleAdjustedLength:
            _titleWithSpace += " " * (titleAdjustedLength - len(_titleWithSpace))

        _textSoFar = ""
        # _textSoFar = _titleWithSpace

        if type(inputList) == list or type(inputList) == Change:  # Multiple Values
            if type(inputList) == Change:
                inputList = [str(i) for i in inputList]
            if type(inputList) == list:
                for i in range(len(inputList)):
                    inputList[i] = str(inputList[i])

                # while inputList[i][0] == ' ': #Get rid of spaces before str
                # 	inputList[i] = inputList[i][1:]
                # while inputList[i][-1] == ' ': #Get rid of spaces after str
                # 	inputList[i] = inputList[i][:-1]

            if len(inputList) == 1:  # Only One value but in list form
                return _titleWithSpace + inputList[0]  # + '\n'

            # There's a list of answers
            if inputList:
                resultLengths = []
                for valueIndex, value in enumerate(inputList):
                    _hexagramStringWithSpaces = ""
                    _addedASpace = False
                    resultLengths.append(len(value))
                    for charIndex, char in enumerate(value):
                        # This is letting accidentals go before strings
                        if char in ("b,", "#", "♭", "♯"):
                            resultLengths[-1] -= 1
                        else:  # new
                            break
                    for charIndex in range(len(inputList[valueIndex])):
                        if inputList[valueIndex][charIndex] in Hexagram.symbol:
                            _hexagramStringWithSpaces += inputList[valueIndex][
                                charIndex
                            ]
                            if not _addedASpace:
                                _hexagramStringWithSpaces += " "  # ' '#Hexagram space
                                _addedASpace = True

                    if _hexagramStringWithSpaces != "":
                        # This was where the hexagram bug was
                        # inputList[valueIndex] = inputList[valueIndex]+_hexagramStringWithSpaces
                        inputList[valueIndex] = inputList[valueIndex]

                maxResultLength = max(resultLengths)
                if _addedASpace:
                    maxResultLength += 1
                """if len(inputList[0]) > 1 and type(inputList[0]) == str:
                    #print('hunt',inputList, max(inputList, key=len))
                    if max(inputList, key=len)[0] in ('♭','♯','#','b'):
                        maxResultLength -= 1"""
            else:
                maxResultLength = 1

            if constrainToWidthAndNotAlignToGrid:
                lineText = [""]
                lineText += titleWithSpace
                for i in inputList:
                    pass  # Work HERE

            amountOfLines = 1 + math.floor(
                (maxResultLength + minimumSpaceBetweenItems - 1) / cellSize
            )
            # amountOfLines = 1 + math.floor((maxResultLength + minimumSpaceBetweenItems ) / (cellSize+ minimumSpaceBetweenItems))
            # amountOfLines = 1 + math.floor((maxResultLength + minimumSpaceBetweenItems) / (cellSize + minimumSpaceBetweenItems))
            amountOfLines = min(amountOfLines, len(inputList))

            lineText = []
            lineInputIndexes = []
            for line in range(amountOfLines):  # Build List of Index Inputs
                lineInputIndexes.append([])
                for inputListIndex in range(line, len(inputList), amountOfLines):
                    lineInputIndexes[line].append(inputListIndex)
            for line in range(amountOfLines):
                lineText.append("")
                if line == 0:
                    lineText[0] += _titleWithSpace
                else:  # We are into the multiple lines
                    lineText[line] += " " * len(_titleWithSpace)
                for inputListIndex in range(len(inputList)):
                    if (
                            inputListIndex in lineInputIndexes[line]
                    ):  # If we are printing this value onto this line
                        _charPositionOfInput = (
                                titleAdjustedLength
                                + inputListIndex * cellSize
                                + len(prependResultWithStr)
                        )  # Move the print cursor

                        # _charPositionOfInput -= 1
                        # To after the title, then 'tabbed' by however many values over we're supposed to be times the space between
                        if (
                                excludeAccidentalsInAlignment
                        ):  # If we are lining numbers and roman numerals by their number and not by their accidental
                            for i in range(len(inputList[inputListIndex])):
                                if (
                                        inputList[inputListIndex][i]
                                        in ["#", "b", "♯", "♭"] + Book.prependingChars
                                ):
                                    _charPositionOfInput -= 1
                                else:
                                    break

                        # print('minsk', inputListIndex, inputList[inputListIndex], _charPositionOfInput)
                        while (
                                len(lineText[line]) + len(prependResultWithStr)
                                < _charPositionOfInput
                        ):
                            lineText[line] += " "
                        # lineText[line] += ' '* (inputListIndex * cellSize -(0))
                        lineText[line] += (
                                prependResultWithStr + inputList[inputListIndex]
                        )
            for line in lineText:
                _textSoFar += line
                _lineIndex = lineText.index(line)
                if amountOfLines > 1 and not amountOfLines == lineText.index(line) + 1:
                    if not _lineIndex > len(inputList):
                        if latexCommands:
                            _textSoFar += Latex.commandStrings["Line Break"]
                        _textSoFar += "\n"

            while _textSoFar.endswith(" " * titleAdjustedLength):
                _textSoFar = _textSoFar[:-titleAdjustedLength]
            while _textSoFar.endswith("\n"):
                _textSoFar = _textSoFar[:-1]
            # print('really',amountOfLines,end='')
            return _textSoFar

        else:  # Only one value
            return _textSoFar + str(inputList)

    def printToTextOld(
            self,
            indexNumbersToUse,
            printToScreenLive=True,
            ways=[
                "Solfege",
                "Jazz",
                "Chord",
                "Classical",
                "Chord Quality",
                "Set",
                "Step",
                "C",
                "C#",
                "Db",
                "D",
                "D#",
                "Eb",
                "E",
                "F",
                "F#",
                "Gb",
                "G",
                "G#",
                "Ab",
                "A",
                "A#",
                "Bb",
                "B",
                "Mneumonic",
                "Carnatic",
                "Notation",
                "Mode Jazz",
                "Mode Page",
                "Hexagram Symbol",
                "Hexagram Name",
            ],
    ):
        _wayNameSeperator = ": "
        for way in ways:
            if JazzNote.isValidWay(way):
                pass
            elif Change.isValidWay(way):
                pass
            elif Book.isValidWay(way):
                pass
            else:
                raise ValueError("ways contained", way, "and should not.")
        if indexNumbersToUse[-1] >= len(self.sequence):
            raise ValueError("sequence does not contain ", indexNumbersToUse[-1])

        _text = "The Keymaster's Grail Of Scale\n"
        for thisIndex in indexNumbersToUse:

            _thisIndexText = "\n"
            _text += "\n  "
            _text += self.getTitle(
                self.sequence[thisIndex],
                hexagramName="Hexagram" in ways,
                chordQuality="Chord Quality" in ways,
                addOne=True,
                seperator=_wayNameSeperator,
            )
            _thisIndexText = self.getTitle(
                self.sequence[thisIndex],
                hexagramName="Hexagram" in ways,
                chordQuality="Chord Quality" in ways,
                addOne=True,
                seperator=_wayNameSeperator,
            )

            print(thisIndex, "of", indexNumbersToUse[-1])

            _text += "\n"
            _thisIndexText += "\n"
            _wayNameMaxCharLength = 1
            for way in ways:
                _wayNameMaxCharLength = max(len(way), _wayNameMaxCharLength)
            for way in ways:
                _excludeThisWay = False
                _wayNameCharLength = len(way)
                if way not in ("Hexagram Symbol", "Hexagram Name", "Chord Quality"):
                    if way in ("Carnatic", "All Flats Number"):
                        if self.sequence[thisIndex].byWays(way) == self.sequence[
                            thisIndex
                        ].byWays("Jazz"):

                            _excludeThisWay = True
                        else:
                            _text += "\n" + way + ":"
                            _thisIndexText += "\n" + way + ":"
                    else:
                        if JazzNote.isAlphabetNoteStr(way):
                            _text += (
                                    "\n" + JazzNote.convertNoteToRealUnicodeStr(way) + ":"
                            )
                            _thisIndexText += (
                                    "\n" + JazzNote.convertNoteToRealUnicodeStr(way) + ":"
                            )
                        else:  # Not a note like A Bb
                            _text += "\n" + way + ":"
                            _thisIndexText += "\n" + way + ":"

                _temporaryText = []
                for i in self.byMoreWays(self.sequence[thisIndex], way):
                    if not _excludeThisWay:

                        _thisChange = self.sequence[thisIndex]
                        _temporaryText.append(str(i))
                        if way == "Step":
                            _temporaryText[-1] = " " * 2 + "+" + _temporaryText[-1]

                    # _text+= str(i) + " "
                    # ('%-2s ' * len(l))[:-1] % tuple(l)
                    # for i in _temporaryText:
                    # 	_text += "{:3d} {:4d} {:5d}".format(*_temporaryText)
                    #
                    # my_args = ["foo", "bar", "baz"]
                # _text += " %s" % '  '.join(_temporaryText)
                _text += " " * (
                        _wayNameMaxCharLength - _wayNameCharLength + len(_wayNameSeperator)
                )
                _thisIndexText += "\n" + way + ":"

                _strFormatter = "{:<8s}" * len(_temporaryText)
                _text += _strFormatter.format(*_temporaryText)
                _thisIndexText += _strFormatter.format(*_temporaryText)

                if ways[-1] == way:
                    _text += "\n"
                    _thisIndexText += "\n"
            if printToScreenLive:
                print(_thisIndexText)
        return _text

    def displayChapterInfo(
            self, change: Change, latexCommands=True, disableBuggyUnicode=False, rootKey='C'
    ):
        chapterNumber = len(change)
        if not change.containsNotes("1"):
            chapterNumber = -chapterNumber
        _rootless = not change.containsNotes("1")
        if not disableBuggyUnicode:
            _emoji = self.returnCuteSymbolFromInt(chapterNumber)
        else:
            _emoji = ""
        if _rootless:
            _chapterLength = str(len(self.sequenceByLength[-chapterNumber + 1]))
        else:
            _chapterLength = str(len(self.sequenceByLength[abs(chapterNumber)]))
        if _chapterLength in (1, "1"):
            _beingVerb = "is"
            _pronoun = "it"
            _object = "it"
            _pluralise = ""
            _reversePluralise = "s"
            _possessive = "its"
        else:
            _beingVerb = "are"
            _pronoun = "they"
            _object = "them"
            _pluralise = "s"
            _reversePluralise = ""
            _possessive = "their"

        if len(change) > 0:
            _chapterStr = JazzNote(str(abs(chapterNumber))).getRomanNumeral()
        else:
            _chapterStr = "nulla"
        if _rootless:
            _chapterStr = "-" + _chapterStr

        _addOneToChapterStart = 1 if self.sequenceLengthRanges[1]["start"] == 0 else 0
        _txt = ""
        if latexCommands:
            pass  # _txt += "\\begin{minipage}{\\linewidth}"
        if not disableBuggyUnicode:
            _txt += _emoji + "  "
        _txt += "Welcome to Chapter " + _chapterStr
        if not disableBuggyUnicode:
            _txt += "  " + _emoji
        _txt += "\n\nThere {} {} change{} in this chapter. {} start{} on change {}, and end{} on change {}.".format(
            _beingVerb,
            _chapterLength,
            _pluralise,
            _pronoun.title(),
            _reversePluralise,
            str(
                self.sequenceLengthRanges[len(change)]["start"]
                + (_addOneToChapterStart if not _rootless else -_addOneToChapterStart)
            ),
            _reversePluralise,
            str(
                self.sequenceLengthRanges[len(change)]["end"]
                + (_addOneToChapterStart if not _rootless else -_addOneToChapterStart)
            ),
        )
        if Book.makePrimes:
            _txt += "\n\nThere {} {} change {} in Chapter {}. That makes {} {}\% unique. ".format(
                _beingVerb,
                len(self.sequencePrimesByLength[chapterNumber]),
                "family" if len(self.sequencePrimesByLength[chapterNumber]) == 1 else 'families',
                _chapterStr,
                _object,
                round(
                    100
                    * len(self.sequencePrimesByLength[chapterNumber])
                    / int(_chapterLength),
                    2,
                ),
            )
            _txt += "{} prime form{} {}:\\\\\n".format(
                _possessive.title(), _pluralise, _beingVerb
            )
            _primeForms = []

            for primeIdx, prime in tqdm(enumerate(self.sequencePrimesByLength[chapterNumber])):
                # print('prime is',prime,primeIdx)
                _heightMod = ''
                if chapterNumber in (6, 7): _heightMod = ',height=.49\\textheight'

                _txt += prime.makePdfLink(linkCode='mf')
                # print('doing Graphics.getChordsOfChangePath(change={},'.format(prime))
                _txt += '\\includegraphics[keepaspectratio,width=\\textwidth' + _heightMod + ']{' + Graphics.getChordsOfChangePath(
                    change=prime,
                    tabuliseBySemitonePosition=False,
                    rootKey=rootKey,

                    invertColour=False,
                    useColour=True,
                    includeDirectory=True,
                    includeFilename=True,
                    chordsOfChangeType='Mode Family', includeExtension=False,
                ).replace('\\', '/') + '}\\\\\n'
                # input(_txt)
                for n in range(len(prime)):
                    pass  # _primeMode = prime.mode(n)

                    # _txt += Project.makeCondensedChangeTex(change=_primeMode,ways=Book.condensedWaysModeFamily) + '\\\\\n'
                    '''_txt += Latex.tabTo('0')
                    _txt += Latex.insertSmallDiagram(change=_primeMode, diagramType='SCircle', filetype='pdf',
                                                     key=Book.rootColourKey,imgtag='bigpianoimg')
                    _txt += Latex.tabTo('.3')
                    _txt += str(primeIdx) +': '+str(_primeMode)+ Latex.tabTo('.7')+ str(_primeMode.getChangeNumber())

                    _txt += Latex.insertSmallDiagram(change=_primeMode, diagramType='Piano', filetype='pdf',
                                                     key=Book.rootColourKey,imgtag='bigpianoimg')

                    _txt += ' \\\\\n'


                _txt += '\\\\\n' '''

            '''for i, p in enumerate(self.sequencePrimesByLength[chapterNumber]):
                # _txt += str(i) +': '+str(p)+p.getChangeNumber(addOneToBookPage=True)+'\n'
                # _txt += Latex.insertSmallDiagram(change=p,diagramType='PCircle',filetype='pdf',key=Book.rootColourKey)
                _primeForms.append(
                    Latex.textGraphic(
                        sizeMultiplier=1.5,
                        endStr="\\hspace{1.3em}",
                        text=str(
                            p.getChangeNumber(
                                addOneToBookPage=True, decorateChapter=False
                            )
                        ),
                        graphPath=Graphics.getDiagramPath(
                            change=p,
                            diagramType="PCircle",
                            filetype="pdf",
                            key=Book.rootColourKey,
                        ),
                    )
                )
            # input(Utility.turnLstToMatrix(_primeForms,12))
            _txt += "\n\n" + Latex.makeTabular(
                rows=Utility.turnLstToMatrix(_primeForms, 10),
                tableCaption="Prime Changes In Chapter " + _chapterStr,
                fillHorSpaceWithTabularX=True,
            )'''

        else:
            warnings.warn(
                "you dont have Book.makesPrimes == True, so we cant make full chapter info"
            )
        if latexCommands:
            # _txt += "\\end{minipage}\\clearpage "
            _txt += "\\clearpage "
            # input(_txt)
        return _txt

    def displayByForteNumber(self) -> str:
        def remove_duplicates(li):
            my_set = set()
            res = []
            for e in li:
                if e not in my_set:
                    res.append(e)
                    my_set.add(e)
            return res

        _pageTxt = (
            "Z-related sets:\n"
            "(It means that the sets have the same interval vector)\n"
            "The interval vector will be six numbers in a row that describe\n"
            "the scale's makeup of intervals, including inversions, which is why there are six.\n"
            "Each line is a modal family (scales that are modes of each other)\n"
            "Each modal family's scales are arranged in Prime Order.\n"
            "This means that the most compressed scales are listed first.\n"
            "They are compressed by the right.\n\n"
        )

        fn = ScaleNames.forteNumbers
        _iVectors = {}
        for i in fn.keys():
            _txt = ""
            _txt += Change.infoWaySymbols["Forte Number"] + i + ": "
            _txt += ",".join(map(str, fn[i])) + ": "
            if len(fn[i]) > 0:
                _change = Change.makeFromSet(fn[i]).getPrimeForm()
                _txt += " ".join(_change.byWays("Jazz"))
                _intervalVector = _change.getIntervalVector(convert10ToT=True)
                _names = []
                for i in range(len(_change)):
                    # _names.append(_change.mode(i).getScaleNames(defaultWay='Hexagram Name',searchForDownward=False,
                    _names.append(
                        _change.getPrimeForm(indexOfPrimeness=i).getScaleNames(
                            defaultWay="Hexagram Name",
                            searchForDownward=False,
                            searchForNegative=False,
                            includeDownwardHexagram=False,
                        )[0]
                    )
                _txt += " " + _change.getChangeNumber(addOneToBookPage=True) + " "
                _txt += ", ".join(remove_duplicates(_names))
            else:
                _intervalVector = "000000"
            _txt += "\n"
            if not _intervalVector in _iVectors:
                _iVectors[_intervalVector] = _txt
            else:
                _iVectors[_intervalVector] += _txt
        for iv in _iVectors.keys():
            _pageTxt += "  Interval Vector: " + iv + ":\n"
            _pageTxt += _iVectors[iv]
            # _pageTxt += _txt
        return _pageTxt

    def makeBitMapChart(self, useSmallCirclePageNumbers=True):
        _str = "\\begin{tabbing}\n"
        if Colour.makeGraphicsColoured:
            _colourKey = "C"
        else:
            _colourKey = "C"
        if useSmallCirclePageNumbers:
            _str += (
                    Latex.insertSmallCircleFromPageNumber(-2048, tabbingimg=True)
                    + "\\quad\\quad\\="
                    + self[-2047].getBitMap(colourResult=Latex.makeTextColoured)
                    + "\\\\\n"
            )

        else:
            _str += (
                    Book.unicodeChars["Change Number"]
                    + str(1)
                    + "\\quad\\quad\\="
                    + theBook[0].getBitMap()
                    + "\\\\\n"
            )
        for i in range(-2046, 2048):
            # print(Book.unicodeCharConstants['Change Number'],i+1,'\\texttt{ '+'\space '*(2-len(str(i+1)))+theBook.sequence[i].getBitMap()+'}\\\\',sep='')
            # This next line would output without SmallCircles
            if i < 0:
                _signedOne = -1
            else:
                _signedOne = 1
            if useSmallCirclePageNumbers:
                # print('doohikee',self[i],i)
                if i + _signedOne == 1:
                    _str += (
                            Latex.insertSmallCircleFromPageNumber(-1, tabbingimg=True)
                            + "\\>"
                            + Change([]).getBitMap(colourResult=Latex.makeTextColoured)
                            + "\\\\\n"
                    )
                _str += (
                        Latex.insertSmallCircleFromPageNumber(
                            i + _signedOne, colourKey=_colourKey, tabbingimg=True
                        )
                        + "\\>"
                        + self[i].getBitMap()
                        + "\\\\\n"
                )
            else:
                _str += (
                        Book.unicodeChars["Change Number"]
                        + i
                        + _signedOne
                        + "\\>"
                        + self[i].getBitMap()
                        + "\\\\\n"
                )

        _str += "\\end{tabbing}"
        print(_str)
        return _str

    def makeSimpleBook(self, keys=['C'], ways=
    ['Change Number', '  ', "Jazz", "  ", "Scale Name", "  ", "Chord Quality", "  ", 'C', "  ", "Bitmap", "Line Break",
     "  ", "Distinct Chord 1", "Line Break", "Line Break"]):
        '''You can use "Space","Line Break", in between ways'''
        path = 'simple_book.txt'
        result = "Here contained:\nThe (mostly)-ASCII text version of the super-condensed Way Of Change, by Édrihan Lévesque\nTIP: An easy way to find changes if the spelling is ambiguous, i.e, the difference between {} and {}, use the bitstring.\n\n\n\n".format(
            Book.unicodeChars['Sharp'] + '4', Book.unicodeChars['Flat'] + '5')
        changeRange = range(-12, 2049)
        noteCount = -1
        sectionDecorator = '-' * 20
        sectionIndent = '      '
        for c in tqdm(changeRange):
            if c == 0:
                continue
            change: Change = Change.makeFromChangeNumber(c).straightenDegrees()

            if len(change) != noteCount:
                result += '{}{}\n{}{}-note Changes:\n{}{}\n\n\n'.format(
                    sectionIndent, sectionDecorator, sectionIndent, len(change), sectionIndent, sectionDecorator)
                noteCount = len(change)
            for way in ways:
                if way == 'Line Break':
                    changeByWay = '\n'
                elif way == 'Space':
                    changeByWay = ' '
                elif all([char == ' ' for char in way]) or way == ':':
                    changeByWay = way
                elif way == 'Change Number':
                    changeByWay = '#' + str(change.getChangeNumber(decorateChapter=False))
                elif way == 'Jazz':
                    changeByWay = ' '.join(change.byWays(['Jazz']))
                elif way == 'Scale Name':
                    changeByWay = ', '.join(change.getScaleNames(replaceCarnaticNamesWithSymbols=False))
                elif way == 'Bitmap':
                    changeByWay = change.getBitMap(trueSymbol='1', falseSymbol='0', colourResult=False)
                elif 'Distinct Chord' in way:
                    changeByWay = [str(change[n]) + ' ' + str(note) for n, note in enumerate(change.byWays([way]))]
                    changeByWay = ', '.join(changeByWay)
                elif Key.isValid(way):
                    changeByWay = change.byWays([way])
                elif Change.isValidWay(way):
                    changeByWay = str(change.byWays([way], useTextStyledByWay=False))
                else:
                    raise ValueError('{} is not a valid way here so come fix it.'.format(way))

                if type(changeByWay) in (list, tuple):
                    changeByWay = ' '.join([str(i) for i in changeByWay])
                result += str(changeByWay)

        result += '''Copyright © 2019 Édrihan Lévesque
All rights reserved. 2022'''
        with open(path, 'w', encoding='UTF8') as output:
            output.write(result)
        print('saved {}'.format(path))
        return result

    def makeLittleBook(self, rootKey="C"):
        for i, change in enumerate(self.sequence):
            # for i, change in enumerate((Change(['1','2','3','4','5','6','7']),)):
            change: Change = change.straightenDegrees(
                allowedNotes=Change.allowedNoteNamesSuperset
            )

            names = change.getScaleNames(
                defaultWay=False,
                replaceDirectionStrWithUnicode=False,
                replaceCarnaticNamesWithSymbols=False,
            )
            if len(names) > 0:
                name = names[0]
            else:
                name = "*"
            _hexagramStuff = ": ".join(
                change.getHexagram(
                    ["name", "symbol", "chinese"],
                    concatenatePerHexagram=False,
                    insertStrBetweenSections="",
                )
            )

            _str = ""
            _str += "------\nListing Title:\nVortex #{}({}) - {}\n\nListing subtitle:\nThe Way Of Change Vortices\n\n".format(
                change.getChangeNumber(),
                rootKey,
                " ".join(change.getHexagram(["name"])),
            )

            _str += "Listing Description:\nThe Way Of Change is a new way of looking at sounds. \nIt brings geometry, colour, sound and language together to unify our understanding of music, and beyond.\n\n"

            _str += "A Change is a combination. It can be seen in many ways.\nThis Change(#{}), as a series of bits is {}.\nIf we play it in {} on a piano, we'd play {}. That's also called a {}{}".format(
                change.getChangeNumber(),
                change.getBitMap(colourResult=False, trueSymbol="1", falseSymbol="0"),
                rootKey,
                ", ".join(change.byWays(rootKey)),
                rootKey,
                change.getChordQuality(),
            )
            _scaleNames = change.getScaleNames(defaultWay=False)
            if len(_scaleNames) > 1:
                _str += ", or " + change.getScaleNames()[0]
            _str += ".\n"
            _str += "In this piece, Change #{} is drawn as a Vortex, which is a fractal based on rotations of its circular geometry.\n".format(
                change.getChangeNumber()
            )
            _str += "If we split it in half and consulted the ancient Book Of Changes we would find the first to be {}({}), and second {}({})".format(
                change.getHexagram(["name"])[0],
                change.getHexagram(["number"])[0],
                change.getHexagram(["name"])[1],
                change.getHexagram(["number"])[1],
            )
            # _str += '\nThis particular Change is called {}, which comes from the I-Ching. '.format(
            #    ' '.join(change.getHexagram(['name'])))
            """_str += '\n{}: \n{}:\n{}: {}: {}: {}:\n{}:\n{}:\n{}{}{}:\n{}'.format(
                _hexagramStuff,': '.join(change.getTrigram(['name','symbol','chinese','syllable'],insertStrBetweenSections='')),
                ', '.join([str(j) for j in change]), change.getChordQuality(), ', '.join(change.byWays(['Solfege'])), 'C '+name,
                ', '.join([str(change[chordIdx].byWay('C')) + ' '+ str(change.getDistinctScaleChord(chordIdx,0,removeChordsWithOneLessLength=False,)) for chordIdx in range(len(change))]),
                ', '.join(
                    [str(change[chordIdx].getConsonant()) + change.getDistinctScaleChord(chordIdx, 0, returnChordQuality=False,removeChordsWithOneLessLength=False).getWord() for chordIdx in
                     range(len(change))]), 
            'Change ', i + 1,' in the key of C', '"'+'\n... '.join(change.getHexagram(['story']))+'"')"""

            _str = _str.replace(": C *", "")
            _str = _str.replace(" :", ":")
            _str = _str.replace(" ,", ",")
            print(_str)

            """print(Book.unicodeChars['Change Number'], i + 1, ': ', name, ': ' + str(change),
                  ': ' + ' '.join(change.getHexagramSymbols()), ': ' + change.getHexagramName(),
                  ' ' + Change.infoWaySymbols['Primeness'], str(change.getPrimeness()), ' ',
                  change.getRingNumber(includePreString=True), sep='')"""

            # print('     '.join(change.getConsonant()))
            # print(self.renderTitleAndListOfAnswers(change.getConsonant(), title='', titleAdjustedLength=1, cellSize=8,
            #                                       wayNameSeperator=''))

    def getEmptyPage(self):
        _pageStr = "This is the empty subChange."

        _change = Change([])
        _pageTitle = self.getTitle(
            _change,
            Book.tableOfContentsLabelWays,
            protectCommands=True,
            seperator=" \\hfill ",
        )
        _pageTitle += self.addPageToTableOfContents(_change)
        _pageTitle = "\\hspace*{-1.5cm}" + _pageTitle.replace(
            "protect\\\\\n", "protect\\\\\n" + "\\hspace*{-1.5cm}"
        )
        for w in Book.printWays:
            if "Keys Diagram" in w:
                print(w, w.index("Keys Diagram"))
                _diagramTypes = w.replace(" Keys Diagram", "").split(" ")

                if not isinstance(_diagramTypes, (list,)):
                    raise ValueError("balasdfg")
                # _str += '\\FloatBarrier \\newpage'
                _diagramPage = Latex.commandStrings["Start Figure"]
                _diagramPage += Latex.insertKeysDiagram(
                    change=Change([]),
                    diagramTypes=_diagramTypes,
                )
                _diagramPage += Latex.commandStrings["End Figure"]
                _diagramPage += "\\newpage\n"
        return _pageStr + _pageTitle + _diagramPage

    def makeCondensed(
            self,
            changes: list,
            book: Book,
            strBetweenWays=None,
            linesInTitle=2,
            cols=3,
            useChaptersForChangeLength=True,
            tabuliseBySemitonePosition=True,
            showDebug=True,
            padVertSpaceBetweenChanges=True,
            rootKey="C",
            externalGraphicsPath=True,
            renderEachPageSeperately=False,
            useCircleBehindJazzNotes=False,
            useCircleBehindWayOfWord=False,
            useCircleBeforeScaleChords=False,
            useCircleBehindHexagram=False,
            invertColour=False,
            useColour=True,
    ):
        print("calling Book.makeCondensed({})".format(locals()))
        if useCircleBehindWayOfWord:
            raise ValueError("this will probably fuck up at change -1361")

        _lineBreak = "\\\\\n"
        if strBetweenWays == None:
            strBetweenWays = ""
            # strBetweenWays = '\\hfill '
            # strBetweenWays = '\\hfill '+Book.unicodeChars['Chinese Seperator']+'\\hfill '
        _str = ""
        """_str += '\\tcbset{enhanced,colback=red!5!white,boxrule=0.1pt,'
        _str += 'colframe=red!75!black,'
        _str += 'fonttitle=\\bfseries}""" ""

        if showDebug:
            print("condensedWays ==", Book.condensedWays)
        if changes == None:
            # changes = self.sequenceByLength[7]
            changes = range(2011, 2025)
            # changes = (2,3)
        print("going through changes....", changes)
        if useChaptersForChangeLength == None:
            useChaptersForChangeLength = sorted(list(changes)) == list(changes)
        if padVertSpaceBetweenChanges:
            _fillBetweenChanges = "\\vfill"
        else:
            _fillBetweenChanges = ""
        _pastChangeLength = -1
        _colorboxSettings = "\\tcbset{boxrule=0.2pt,toptitle=.5cm,bottomtitle=-.6cm,top=0cm,bottom=-0.1cm,left=0mm,colback=gray!5}"
        _smallColorBoxSettings = (
            "\\definecolor{blankNameColour}{rgb}{0.122, 0.435, 0.698}"
        )
        _smallColorBoxSettings += "\\newtcbox{\\nameBox}{on line,  colframe=blankNameColour,colback=blankNameColour!10!white,boxrule=0.5pt,arc=4pt,boxsep=0pt,left=12pt,right=150pt,top=16pt,bottom=3pt}"
        _multiColouredLatex = "\\newlength{\\lengthofmulticolourtext}\n"
        _multiColouredLatex += "\\newlength{\\heightofmulticolourtext}\n"

        _str += _multiColouredLatex + _colorboxSettings + _smallColorBoxSettings

        _colours = Colour.getTransposedColours(
            colourTranspose=JazzNote.distanceFromC(rootKey)
        )
        _colourTags = Colour.getTransposedColourTags(
            colourTranspose=JazzNote.distanceFromC(rootKey), neutralColours=True
        )
        _outlinedTextLineWidth = 0.5
        if invertColour:
            _inkColourTag = "white"
            _paperColourTag = "black"
        else:
            _inkColourTag = "black"
            _paperColourTag = "white"

        for changeIdx, change in enumerate(changes):
            if renderEachPageSeperately:
                changeStr = _colorboxSettings + _smallColorBoxSettings
            if change == 0:
                continue
            _changeLengthData = ""
            _pageStr = ""
            _titleStr = ""
            if type(change) == Change:
                c = change.getChangeNumber()
            else:
                c = change
                change = self[change]
            # Now type(c) == int and type(change) == Change

            if (len(change) != _pastChangeLength) and useChaptersForChangeLength:
                if c < 0:
                    _numOfNotesStr = "-" + str(len(change))
                else:
                    _numOfNotesStr = str(len(change))
                _sectionNameStr = (
                        _numOfNotesStr + " " + Book.chapterHeadings[len(change)]
                )
                _changeLengthData += "\\clearpage\\section*{" + _sectionNameStr + "}"
                _changeLengthData += (
                        "\\addcontentsline{toc}{section}{" + _sectionNameStr + "}"
                )
                _changeLengthData += book.displayChapterInfo(change)

                # _changeLengthDescriptor = str(len(change)) + ' notes'
                # _str += '\\pdfbookmark[section]{' + _changeLengthDescriptor + '}{toc}'
                # _changeLengthData = '\\section*{Introduction}\\label{sec:intro}\\addcontentsline{toc}{section}{\\nameref{sec:intro}}' + _str + '}'
                # _changeLengthData = '\\section*{'+Book.chapterHeadings[len(change)]+'} \n'
            _pastChangeLength = len(change)
            if c in Book.changesForBeginners:
                # _featuredChangeStr = '\\addcontentsline{toc}{subsection}{' + self.getTitle(change,['Book Page','Scale Name','Chord Quality'])+'}'#
                _featuredChangeStr = self.addPageToTableOfContents(
                    change=change,
                    captionType="subsection",
                    ways=Book.condensedTableOfContentsWays,
                    replaceSheetNumber=False,
                    externalGraphicsPath=externalGraphicsPath,
                )
                _pdfBookmark = ""
                print("featuredChange:", _featuredChangeStr)
            else:
                _featuredChangeStr = ""
                _pdfBookmark = change.makePdfLink()

            print(str(c), end=", ")
            for w, way in enumerate(Book.condensedWays):

                if showDebug and changeIdx == 0:
                    print("making", way, end=":  ")
                # input(change.byWays('Hexagram Symbol'))
                _changeByWay = ""
                if way == "Line Break":
                    _changeByWay = _lineBreak
                elif way == "Hexagram Symbol Name":
                    _changeByWay = change.getHexagram(
                        hexagramWays=["symbol", "name"],
                        concatenatePerHexagram=True,
                        insertStrBetweenSections="",
                        insertStrBetweenAnswers="",
                        decorateSymbolWith="PCircle"
                        if useCircleBehindHexagram
                        else False,
                        useGraphicSymbol=True,
                        filetype="pdf",
                        externalGraphicsPath=externalGraphicsPath,
                        invertColour=invertColour,
                    )

                    _changeByWay = [
                        "{"
                        + ("\\hspace{0.3cm}" if useCircleBehindHexagram else "")
                        + "\\"
                        + FontMap.fontByWay["Hexagram"]["latexName"]
                        + " "
                        + Latex.outlineText(
                            text=h,
                            colourTag=_paperColourTag,
                            strokeColourTag=_inkColourTag,
                            lineWidth=_outlinedTextLineWidth,
                        )
                        + "}"
                        for h in _changeByWay
                    ]

                    # input('geaorg "\n{}\n"'.format(_changeByWay))
                    # input('"{}"'.format(_changeByWay[0]))
                elif way == "Word":
                    # _changeByWay = ''.join(change.getHexagram(['syllable']))
                    if useCircleBehindWayOfWord:
                        _changeByWay = "".join(
                            change.getTrigram(
                                ["syllable"],
                                decorateSyllableWith="PCircle",
                                externalGraphicsPath=externalGraphicsPath,
                            )
                        )
                    else:
                        _changeByWay = "".join(
                            change.getTrigram(["syllable"], colourResult=True)
                        )
                        """_changeByWay = Latex.outlineText(text=_changeByWay,
                                                     colourTag=_paperColourTag,
                                                     outlineColourTag=_inkColourTag,
                                                     lineWidth=_outlinedTextLineWidth)"""
                elif way == "Jazz":
                    _changeByWay = []
                    _notesByWay = change.straightenDegrees(
                        Change.allowedNoteNamesSuperset + Change.allowedNoteNamesWeird
                    )
                    """input('yazz {}\nbazz {}\ndazz{}'.format(
                        _notesByWay.__iter__(),
                        [i for i in _notesByWay],
                        _notesByWay.notes))"""

                    # Add notes graphic behind answer
                    _diagramPaths = []
                    # print('poopoo')
                    # input('{} {}'.format(_notesByWay,type(_notesByWay)))
                    for n in range(len(change)):
                        # print(n,_notesByWay,change)
                        # input(Change(_notesByWay[n]).getColouredSelf())

                        if useCircleBehindJazzNotes:
                            _diagramPaths.append(
                                Graphics.getDiagramPath(
                                    change=Change([_notesByWay[n]]),
                                    key=rootKey,
                                    diagramType="PCircle",
                                    filetype="pdf",
                                    resolution=FCircle.vectorSmallResolution,
                                    externalGraphicsPath=externalGraphicsPath,
                                )
                            )
                            _changeByWay.append(
                                Latex.textGraphic(
                                    text=_notesByWay[n],
                                    graphPath=_diagramPaths[n],
                                    diagramType="PCircle",
                                    outlineText=True,
                                    colourTag=_colourTags[change[n].semitonesFromOne()],
                                    lineColourTag=_inkColourTag,
                                    lineWidth=_outlinedTextLineWidth,
                                )
                            )

                        else:
                            _changeByWay.append(
                                Latex.outlineText(
                                    text=_notesByWay[n],
                                    colourTag=_colourTags[change[n].semitonesFromOne()],
                                    strokeColourTag=_inkColourTag,
                                    lineWidth=_outlinedTextLineWidth,
                                )
                            )
                    # _changeByWay = change.straightenDegrees(Change.allowedNoteNamesSuperset + Change.allowedNoteNamesWeird)
                    # _changeByWay = ['\\raisebox{-\\height/4}{%\n\\begin{tikzpicture}\\draw (0, 0)[use as bounding box] node[inner sep=0] {\\includegraphics[width=1.1em,clip,trim=left bottom right top]{'
                    # +_diagramPaths[n]+'}};\n\\draw (0, 0)[use as bounding box] node {'+ str(_changeByWay[n]) +'};\end{tikzpicture}}'
                    # for n in range(len(change)) ]
                    # input(_changeByWay[0])
                elif way == "Change Number":
                    _changeByWay = change.getChangeNumber(
                        decorateWithSmallCircle=True,
                        externalGraphicsPath=externalGraphicsPath,
                        imgTag="bigimg",
                    )
                    _changeByWay = Latex.outlineText(
                        text=_changeByWay,
                        colourTag=_paperColourTag,
                        strokeColourTag=_inkColourTag,
                        lineWidth=_outlinedTextLineWidth,
                    )

                elif way == "Scale Name":
                    _changeByWay = change.getScaleNames(
                        defaultWay="Word", replaceCarnaticNamesWithSymbols=False
                    )
                    if type(_changeByWay) == list:
                        _changeByWay = _changeByWay[0]
                    _changeByWay = Latex.outlineText(
                        text="\\bfseries{" + _changeByWay + "}",
                        colourTag=_paperColourTag,
                        strokeColourTag=_inkColourTag,
                        lineWidth=_outlinedTextLineWidth,
                    )
                elif way == "Chord Quality":
                    _changeByWay = change.getChordQuality(
                        useHalfDiminishedUnicodeSymbols=False,
                        useHalfDiminishedChords=False,
                        rootKey=rootKey,
                        makeTextMulticoloured=useColour,
                    )
                    """_changeByWay = Latex.outlineText(text=_changeByWay,
                                                     colourTag=_paperColourTag,
                                                     outlineColourTag=_inkColourTag,
                                                     lineWidth=_outlinedTextLineWidth)"""
                    """if useColour:
                        _changeByWay = Latex.makeTextMulticoloured(text=_changeByWay,
                                                         colourTags=[i for i in _colourTags if i in change.byWays(rootKey)],
                                                         outlineColourTag=_inkColourTag,
                                                         lineWidth=_outlinedTextLineWidth)"""
                    # input('BEGIN\n{}'.format(_changeByWay))
                elif "Distinct Chord" in way:
                    # add mbox{} around results if not later tabulising
                    # _changeByWay = change.byWays(way)
                    _numPartOfDistinctChord = int(way[-1])
                    _numPartOfDistinctChord -= 1
                    _changeByWay = [
                        change.getDistinctScaleChord(
                            n,
                            _numPartOfDistinctChord,
                            removeChordsWithOneLessLength=False,
                            includeModesForDiads=True,
                            useHalfDiminishedChords=False,
                            makeTextMulticoloured=useColour,
                            rootKey=rootKey,
                        )
                        for n in range(len(change))
                    ]

                    # change.romanNumerals(True,)[n]
                    if useCircleBeforeScaleChords:
                        _changeByWay = [
                            "\\mbox{"
                            + Latex.insertSmallDiagram(
                                change=change.getDistinctScaleChord(
                                    n,
                                    _numPartOfDistinctChord,
                                    removeChordsWithOneLessLength=False,
                                    includeModesForDiads=True,
                                    useHalfDiminishedChords=False,
                                    returnChordQuality=False,
                                    normaliseResult=False,
                                ),
                                key=rootKey,
                                diagramType="PCircle",
                                filetype="pdf",
                                externalGraphicsPath=externalGraphicsPath,
                                imgtag="bigimg",
                            )
                            + "{\\bfseries\\jazzA "
                            + Latex.outlineText(
                                text=change.byWays("Jazz")[n],
                                colourTag=_colourTags[change[n].semitonesFromOne()],
                            )
                            + "}"
                            + "\\hspace{1ex}"
                            + "{\\jazzA "
                            + note.replace("°", "dim")
                            + "}"
                            + "}"
                            + Latex.insertSmallDiagram(
                                change=change.getDistinctScaleChord(
                                    n,
                                    _numPartOfDistinctChord,
                                    removeChordsWithOneLessLength=False,
                                    includeModesForDiads=True,
                                    useHalfDiminishedChords=False,
                                    returnChordQuality=False,
                                    normaliseResult=True,
                                ),
                                key=Key(rootKey).onJazz(change[n]),
                                externalGraphicsPath=externalGraphicsPath,
                                diagramType="PCircle",
                                filetype="pdf",
                                imgtag="bigimg",
                            )
                            + "\\hfill "
                            for n, note in enumerate(_changeByWay)
                        ]
                    else:  # useScaleChordsForGraphics==False

                        _changeByWay = [
                            "\\mbox{{\\jazzA "
                            + Latex.outlineText(
                                text=change.byWays("Jazz")[n],
                                colourTag=_colourTags[change[n].semitonesFromOne()],
                                lineWidth=_outlinedTextLineWidth,
                            )
                            + "}"
                            + "\\hspace{1ex}"
                            + "{\\jazzA "
                            + note.replace("°", "dim")
                            + "}}"
                            for n, note in enumerate(_changeByWay)
                        ]
                        # input(_changeByWay[0])
                        # input(_changeByWay)
                    # _changeByWay = [change.byWays('Classical')[n] + ' ' + note for n, note in enumerate(_changeByWay)]
                    _resultMatrix = []
                    if tabuliseBySemitonePosition:
                        _st = change.getSemitones()
                        _scaleDegree = 0
                        for n in range(12):
                            if n % cols == 0:
                                _resultMatrix.append([])
                            if n in _st:
                                _resultMatrix[-1].append(_changeByWay[_scaleDegree])
                                _scaleDegree += 1
                            else:
                                # _resultMatrix[-1].append('╏ \hspace{0.7em}') # ╎╎
                                _resultMatrix[-1].append(
                                    "\\mbox{"
                                    + Latex.outlineText(
                                        text="╏ \\hspace{0.7em}",
                                        lineWidth=_outlinedTextLineWidth,
                                        colourTag=_paperColourTag,
                                        strokeColourTag=_inkColourTag,
                                    )
                                    + "}"
                                )  # ╎╎ ╏'''

                    else:
                        for n, note in enumerate(_changeByWay):
                            if n % cols == 0:
                                _resultMatrix.append([])
                            _resultMatrix[-1].append(note)
                            # http://www.fontineed.com/font/JazzText_Regular
                    # input(_changeByWay)
                    _changeByWay = Latex.makeTabular(
                        _resultMatrix,
                        tableCaption=None,
                        enclosingHorizontalLines=False,
                        enclosingVerticalLines=False,
                        fillHorSpaceWithTabularX=True,
                        useHorizontalLines=False,
                        useVerticalLines=False,
                        centreResults=False,
                    )

                    # input(_changeByWay)
                elif way in Book.titleWays:
                    if showDebug and changeIdx == 0:
                        print("titleway is valid for", way)
                    _changeByWay += self.getTitle(change, [way])
                    # if way == 'Line Break': _changeByWay += '\\noindent '
                elif Change.isValidWay(way):
                    if showDebug and changeIdx == 0:
                        print("change is valid for", way)
                    # input(change.byWays('Word'))
                    _changeByWay = change.byWays(way)
                elif "Tab To" in way:
                    _changeByWay = self.getTitle(change, [way])
                elif way == "\\hfill":
                    _changeByWay = "\\hfill "
                else:
                    raise ValueError("Didn't find way: ".format(way))
                    _changeByWay += self.printToText([c], ways=[way])
                    if showDebug:
                        print(_changeByWay)
                #################Adding FONTS###############

                if type(_changeByWay) == list:
                    _changeByWay = " ".join(_changeByWay)

                if way in ("Chord Quality"):
                    _changeByWay = (
                            "{\\"
                            + FontMap.fontFamilies["jazzA"]["latexName"]
                            + " "
                            + str(_changeByWay).replace("°", "dim")
                            + "}"
                    )
                if way in ("Jazz",):
                    _changeByWay = (
                            "{\\"
                            + FontMap.fontFamilies["jazzA"]["latexName"]
                            + " "
                            + str(_changeByWay).replace("°", "dim")
                            + "}"
                    )
                if way in ("Word",):
                    _changeByWay = (
                            "{\\"
                            + FontMap.fontByWay["Word"]["latexName"]
                            + " "
                            + _changeByWay
                            + "}"
                    )
                if way == "Scale Name":
                    _changeByWay = (
                            "{\\"
                            + FontMap.fontByWay["Scale Name"]["latexName"]
                            + " "
                            + _changeByWay
                            + "}"
                    )
                    # Substitute blank box if scale is unnamed
                    if not change.hasScaleName():
                        """input('scale name {} == defualt way {}'.format(
                            _changeByWay,change.getWord()
                        ))"""
                        # _changeByWay = "\\nameBox{\\hspace{3cm}}"
                    # _changeByWay = '{\\bfseries ' + _changeByWay + '}'
                if way == "Change Number":
                    """if '-' in _changeByWay:
                    # _changeByWay = '{\\testA ' + _changeByWay.replace(str(c),str(c)) + '}'
                    # Set the font only after the '-'
                    _changeByWay = _changeByWay[:-len(str(c))] + '{\\' + FontMap.fontByWay['Change Number'][
                        'latexName'] + ' -}' + '{\\' + FontMap.fontByWay['Change Number'][
                                       'latexName'] + ' ' + str(c).replace('-', '') + '}"""

                    # _changeByWay = '{\\testA ' +_changeByWay.replace('}{\\testF -}{\\testA ','') + '}'

                    pass
                    """else:
                        _changeByWay = '{\\'  +FontMap.fontByWay['Change Number'][
                                           'latexName']+' ' + _changeByWay + '}"""

                if w == 0 or Book.condensedWays[w - 1] == "Line Break":
                    pass  # _pageStr += '\\noindent'
                if (
                        _pageStr.count(_lineBreak) + _titleStr.count(_lineBreak)
                ) < linesInTitle:
                    # input('line breaks: {}'.format(_pageStr.count(_lineBreak)))

                    # print(_changeByWay)
                    _titleStr += str(_changeByWay)
                else:

                    _pageStr += _changeByWay
                    # input('happengin {} happening'.format(_pageStr))

                if (
                        w != len(Book.condensedWays) - 1
                        and Book.condensedWays[w + 1] != "Line Break"
                        and way != "Line Break"
                ):
                    # Book.condensedWays[min(0,w - 1)] != 'Line Break':

                    _pageStr += strBetweenWays

                # input('BEWGIN BLA\n\n\n {} \n way = {} '.format(_titleStr,way))
            # input('subChange string\n{}\nendpagestring'.format(_pageStr))
            _fCirclePath = Graphics.getFCirclePath(
                change=change,
                colourKey="C",
                resolution=256,
                includeFilename=True,
                filetype="pdf",
                externalGraphicsPath=externalGraphicsPath,
            )
            # Put Transparent image behind
            _fCircleSize = 3
            if tabuliseBySemitonePosition:
                if cols == 3:
                    _fCircleSize = 4.8
                elif cols == 4:
                    _fCircleSize = 4.2

            _fCircleStr = (
                    "\\tikz[remember picture,overlay] \\node[opacity=0.05,inner sep=0pt] at (15,1){\\includegraphics[width="
                    + str(_fCircleSize)
                    + "cm,height="
                    + str(_fCircleSize)
                    + "cm]{"
                    + _fCirclePath
                    + "}};"
            )
            _pageStr = (
                    "\\noindent\\begin{minipage}{\\linewidth}\\begin{tcolorbox}[title="
                    + _titleStr
                    + "]"
                    + _fCircleStr
                    + _pageStr
                    + "\\end{tcolorbox}\\end{minipage}"
            )
            # _pageStr = '\\noindent\\begin{minipage}{0.85\\linewidth}\\begin{tcolorbox}[title=My title,watermark graphics=Basilica_5.png,watermark opacity=0.25,watermark text app=Basilica,watermark color=Navy]sdfgsdfgsdfgsdfg}\\end{minipage}'
            # Put image beside table
            # _fCircleStr = '\\includegraphics[height=1.6cm,trim=0cm +3.8cm 0 -3.8cm]{' + _fCirclePath + '}'

            _pageStr += _fCircleStr
            # input(_pageStr)
            # Where the fuck did that ] come from!
            # _pageStr = _pageStr.replace(']\\tikz','\\tikz')
            # _pageStr = _pageStr.replace('\n]\\tikz','\n\\tikz')
            # raise ValueError('fuck it.')
            # _str += _pageStr + '\n'

            _str += _changeLengthData
            _str += _featuredChangeStr
            if not renderEachPageSeperately:
                _str += _pdfBookmark
            _str += (
                    "\\noindent\\begin{tabular}{c r}"
                    + _pageStr
                    + " & "
                    + _fCircleStr
                    + "\\end{tabular}"
                    + _fillBetweenChanges
                    + "\n"
            )

            if renderEachPageSeperately:
                _changeFilename = Latex.getTexPath(
                    change=change,
                    key=Book.rootColourKey,
                    includeFilename=True,
                    outputType="ChordsOfChange",
                    externalGraphicsPath=externalGraphicsPath,
                )
                _changeDirectory = Latex.getTexPath(
                    change=change,
                    key=Book.rootColourKey,
                    includeFilename=False,
                    outputType="ChordsOfChange",
                    externalGraphicsPath=externalGraphicsPath,
                )
                Project.makeDirectory(_changeDirectory)

                with open(_changeFilename, "w+", encoding="utf-8") as _texChangeFile:
                    _texChangeFile.write(
                        Latex.wrapChangeDataWithPreambleEtc(
                            _pageStr, outputType="ChordsOfChange"
                        )
                    )

                    _texChangeFile.write(_pageStr)
                    _texChangeFile.close()
                    print("wrote to ////file:{}".format(_texChangeFile))

                print(
                    "{}\nWrote GOS (Grail Of Scale) file {}".format(
                        _changeFilename,
                        Latex.wrapChangeDataWithPreambleEtc(
                            _pageStr, outputType="ChordsOfChange"
                        ),
                    )
                )
                print(
                    "rendering chords of change pdf from single change #{}".format(
                        change.getChangeNumber()
                    )
                )
                Latex.buildFile(
                    filepath=_changeFilename,
                    openFileWhenDone=True,
                    options=["--shell-escape -output-directory=" + _changeDirectory],
                    args=[],
                    iterations=2,
                )
                input("built file {}".format(_changeFilename))

        return _str

    def printToText(
            self,
            indexNumbersToUse,
            printToScreenLive=False,
            ways=None,
            cellPadding=4,
            _wayNameSeperator=": ",
            titleWays=None,
            printResult=False,
            useTwelveCells=True,
            insertInfoForChangeLengths=None,
            renderEachPageSeperately=True,
    ):
        if insertInfoForChangeLengths == None:
            insertInfoForChangeLengths = sorted(indexNumbersToUse) == indexNumbersToUse
        indexNumbersToUse = list(indexNumbersToUse)

        _numberOfPagesRendered = 0
        _numberOfPagesSuccessful = 0
        _str = ""
        _extraCells = 0
        # for i in len(range(Change.))
        # Add back in mode name

        if titleWays == None:
            titleWays = Book.titleWays
        if ways == None:
            ways = Book.printWays

        _wayNameMaxCharLength = 1
        for way in ways:
            if way not in (titleWays + Book.nonTitlePrintingWays):
                _wayNameMaxCharLength = max(len(way), _wayNameMaxCharLength)

        _printingFirstPage = True

        # print('largest way length is: ',_wayNameMaxCharLength, 'ways:',ways)
        for idx, indexNumber in enumerate(indexNumbersToUse):
            if indexNumber == 0:
                continue
            while True:
                try:
                    # if indexNumber == 0 and indexNumbersToUse[indexNumbersToUse.index(indexNumber)-1] == -1:
                    #    _str += self.getEmptyPage()
                    _changeLengthInfoStr = ""
                    if True and insertInfoForChangeLengths:
                        _changeLengthDescriptor = str(len(self[indexNumber])) + " notes"
                        _changeLengthInfoStr += (
                                "\\addcontentsline{toc}{chapter}{length"
                                + _changeLengthDescriptor
                                + "}\n"
                        )
                        _changeLengthInfoStr += (
                                "\\pdfbookmark[section]{"
                                + _changeLengthDescriptor
                                + "}{toc}"
                        )
                    _pageStr = ""
                    _numberOfPagesRendered += 1
                    _latexTabularOpen = False
                    _change = self[indexNumber]

                    if Latex.on:
                        _pageStr += Latex.setHStretch(len(_change.notes))
                        _printingFirstPage = False

                        _pageStr += (
                                Latex.commandStrings["No Indent"]
                                + Latex.commandStrings["Start Figure"]
                        )
                        # BGFCircle was here
                    if Latex.insertBackgroundDiagram == True:
                        _pageStr += Latex.insertDiagramToPageBackground(_change)
                    _change.makePdfLink()

                    # Title gere
                    _pageStr += self.getTitle(_change, titleWays) + "\\\\"  # + '\n'

                    for way in ways:
                        # print('way',way)
                        if way in Change.straightenedWays:
                            _change: Change = _change.straightenDegrees()

                        if "Distinct Chord" in way:
                            _numberPartOfDistinctChord = int(way[-1])
                            if (
                                    len(_change.getDistinctChordTypes())
                                    >= _numberPartOfDistinctChord
                            ):
                                pass
                            else:
                                continue

                        if way == "Line Break":
                            if Latex.on:
                                if Latex.lineBreakClosesTabular == True:
                                    if (
                                            _latexTabularOpen
                                            and not way in Book.tabularWays
                                    ):
                                        _pageStr += Latex.commandStrings["End Tabular"]
                                        _latexTabularOpen = False
                                    else:
                                        _pageStr += Latex.commandStrings[
                                            "Line Break With Space"
                                        ]
                                elif Latex.lineBreakClosesTabular == False:
                                    if (
                                            _latexTabularOpen
                                            and not way in Book.tabularWays
                                    ):
                                        if Latex.lineBreakWithLine:
                                            _pageStr += "\\hline\n"
                                        else:
                                            _pageStr += Latex.commandStrings[
                                                "Line Break With Space"
                                            ]
                            else:
                                _pageStr += "\n"

                        if Latex.on:
                            if way in Book.tabularWays + ["Efficient", "Line Break"]:
                                if not _latexTabularOpen:
                                    # Enable next line for the original way
                                    # _pageStr += Latex.makeTabular(len(_change))
                                    # Now the way of space is enabled
                                    # remove preceeding linebreak

                                    if _pageStr[-2:] == "\\\\":
                                        _pageStr = _pageStr[:-2]
                                    _pageStr += Latex.makeTabularThirteenCells(
                                        extraCells=_extraCells
                                    )
                                    _latexTabularOpen = True
                            else:
                                if _latexTabularOpen:
                                    _pageStr += Latex.commandStrings["End Tabular"]
                                    _latexTabularOpen = False

                        if not way in titleWays:
                            prependStr = ""
                            _changeByWay = self.byMoreWays(_change, way)

                            # print(_change,_changeByWay,way)
                            # if len(_change) != len(_changeByWay):
                            #    pass#input('Length of change != len of change by way\n{} \n{} \n{}'.format(_change, way, _changeByWay))
                            if Latex.makeTextColoured and Latex.on:
                                if (
                                        way in Book.colouredWaysPositional
                                        or JazzNote.isAlphabetNoteStr(way)
                                ):
                                    _changeByWay = _change.returnColouredLatex(
                                        _changeByWay, way
                                    )
                                elif way in Book.colouredWaysSpecific:
                                    _changeByWay = self.byMoreWays(
                                        _change, way, colourResult=True
                                    )
                            if way == "Hexagram Story":
                                for halfStory in _change.byWays("Hexagram Story"):
                                    _pageStr += halfStory
                                    if Latex.on:
                                        _pageStr += Latex.commandStrings[
                                            "Line Break Small"
                                        ]

                            elif way == "Step":
                                if Latex.on:
                                    prependStr = Book.unicodeChars["Step"]
                                    _changeByWay = [
                                        Book.unicodeChars["Step"] + str(i)
                                        for i in _changeByWay
                                    ]
                                else:
                                    prependStr = (
                                            " " * (math.floor(cellPadding / 2) - 1)
                                            + Book.unicodeChars["Step"]
                                    )
                                for i in range(len(_changeByWay)):
                                    pass
                                    # Come here and delete for loop
                                    # _changeByWay[i] = ' '*(math.floor(cellPadding/2))+'±'+str(_changeByWay[i])
                            elif way == "Rhythm":
                                prependStr = " " * (math.floor(cellPadding / 2) - 1)

                            elif way == "Carnatic":
                                if str(_change.byWays("Carnatic")) == str(
                                        _change.byWays("Jazz")
                                ):
                                    continue
                            elif way == "Efficient":
                                if _change.getSeptatonicInAscendingGenericIntervals(
                                        returnTrueIfIsSeptaOrNegaSexta=True
                                ):
                                    _change = (
                                        _change.getSeptatonicInAscendingGenericIntervals()
                                    )
                                    _efficientKeys = (
                                        _change.getSeptatonicInAscendingGenericIntervals().getEfficientKeys()
                                    )
                                    _homeKeys = (
                                        _change.getSeptatonicInAscendingGenericIntervals().getHomeKeys()
                                    )
                                    _antiHomeKeys = _change.getSeptatonicInAscendingGenericIntervals().getHomeKeys(
                                        returnAntiHomeKeys=True
                                    )
                                else:
                                    _efficientKeys = _change.straightenDegrees(
                                        Change.allowedNoteNamesJazz
                                    ).getEfficientKeys()
                                    _homeKeys = _change.straightenDegrees(
                                        Change.allowedNoteNamesJazz
                                    ).getHomeKeys()
                                    _antiHomeKeys = _change.straightenDegrees(
                                        Change.allowedNoteNamesJazz
                                    ).getHomeKeys(returnAntiHomeKeys=True)
                                for root, scale in _efficientKeys.items():
                                    if not Latex.on:
                                        _pageStr += Book.renderTitleAndListOfAnswers(
                                            scale,
                                            root,
                                            titleAdjustedLength=_wayNameMaxCharLength
                                                                + len(_wayNameSeperator),
                                            wayNameSeperator=_wayNameSeperator,
                                            cellSize=cellPadding,
                                            minimumSpaceBetweenItems=1,
                                            prependResultWithStr=prependStr,
                                            latexCommands=latexCommands,
                                        )
                                    else:  # Yes, latex tables!
                                        """if root in _homeKeys:
                                            prependStr = Book.unicodeChars['Key']
                                        elif root in _antiHomeKeys:
                                            prependStr = Book.unicodeChars['Lock']
                                        else:
                                            prependStr = Book.unicodeChars['Piano']"""
                                        if (
                                                "Instrument Graphics" not in ways
                                                and "Piano Keys Diagram" not in ways
                                        ):
                                            prependStr = Piano().insertGraphic(
                                                _change, key=root, filetype="svg"
                                            )
                                        else:
                                            prependStr = ""
                                        _accidentalsInKey = (
                                            _change.totalNumberOfAccidentals(root)
                                        )
                                        _data = [
                                                    prependStr
                                                    + root
                                                    + " "
                                                    + Book.unicodeChars["Natural"]
                                                    + str(_accidentalsInKey)
                                                ] + scale
                                        # james brown
                                        # _colours = [JazzNote.distanceFromC(root)] + _change.getSemitones()
                                        _colours = [0] + _change.getSemitones()
                                        _colours = [
                                            i + JazzNote.distanceFromC(root)
                                            for i in _colours
                                        ]
                                        if Latex.forceColourCells:
                                            _cellColours = _colours
                                        else:
                                            _cellColours = None
                                        _dataColoured = Latex.makeDataColoured(
                                            results=_data, colours=_colours
                                        )
                                        # input('eh here {} {}'.format(_data,_dataColoured))
                                        _pageStrbefore = _pageStr
                                        _pageStr += Latex.arrangeRowInColumns(
                                            data=_data,
                                            positions=[
                                                int(i) for i in _change.byWays("Set")
                                            ],
                                            cellColours=_cellColours,
                                            dataColoured=_dataColoured,
                                            centreResults=way in Book.centredWays,
                                            extraCells=_extraCells,
                                        )
                                        # print('str after',_pageStr.replace(_pageStrbefore,''))
                                        # This is if there are as many cells as results
                                        """_pageStr += Book.unicodeCharConstants['Key']+root
                                        for i in scale:
                                            _pageStr+=' & ' + str(i)
                                        _pageStr += '\n'
                                        _pageStr += Latex.commandStrings['Table Line Break']"""

                            elif JazzNote.isAlphabetNoteStr(way):
                                raise TypeError(
                                    "I thought I was using the efficient keys function instead these days."
                                )
                                if _change.getSeptatonicInAscendingGenericIntervals(
                                        returnTrueIfIsSeptaOrNegaSexta=True
                                ):
                                    _changeByWay = self.byMoreWays(
                                        _change.getSeptatonicInAscendingGenericIntervals(),
                                        way,
                                    )

                                    if Latex.makeTextColoured:
                                        _changeByWay = _change.returnColouredLatex(
                                            _changeByWay, JazzNote.distanceFromC(way)
                                        )
                                    # print('it has happened')
                                way = "Key Of " + JazzNote.convertNoteToRealUnicodeStr(
                                    way
                                )

                            elif way == "Chord 🗍":
                                prependStr = Book.unicodeChars["Change Number"]  # '•'
                            elif way == "Mode Change Number":
                                pass
                            if way in (Book.colouredWaysPositional) or not Latex.on:
                                if not Latex.on:
                                    _pageStr += Book.renderTitleAndListOfAnswers(
                                        _changeByWay,
                                        way,
                                        titleAdjustedLength=_wayNameMaxCharLength
                                                            + len(_wayNameSeperator),
                                        wayNameSeperator=_wayNameSeperator,
                                        cellSize=cellPadding,
                                        minimumSpaceBetweenItems=1,
                                        prependResultWithStr=prependStr,
                                        latexCommands=latexCommands,
                                    )

                                else:
                                    # HERE put the table rows for latex output
                                    # _pageStr += Latex.makeEmphasised(way)
                                    if useTwelveCells:

                                        # I wish this were somewhere else
                                        _wayName = way
                                        _data = self.byMoreWays(_change, way)
                                        _data = [prependStr + str(i) for i in _data]
                                        if "Distinct Chord" in way:
                                            _wayName = (
                                                Change.makeDistinctChordStrPrintable(
                                                    _wayName, _change
                                                )
                                            )
                                        for replacement in Book.wayNameSubs.items():
                                            _wayName = _wayName.replace(
                                                replacement[0], replacement[1]
                                            )
                                            # if _wayName != way: break
                                        _data = [_wayName] + _data

                                        if way in Book.colouredWaysPositional:
                                            _colours = [False] + [
                                                i + Book.colourTranspose
                                                for i in _change.getSemitones()
                                            ]
                                        if way in Book.colouredWaysSpecific:
                                            if way == "Add Note":
                                                _colours = [False] + [
                                                    i + Book.colourTranspose
                                                    for i in _change.getInverse().getSemitones()
                                                ]
                                            elif "Changed Note" in way:

                                                _colours = [False] + [
                                                    i + Book.colourTranspose
                                                    for i in range(12)
                                                ]
                                            else:
                                                raise TypeError(
                                                    "The way of "
                                                    + way
                                                    + " has no makeTextColoured defined here."
                                                )
                                        if Latex.forceColourCells:
                                            _cellColours = _colours
                                        else:
                                            _cellColours = None

                                        _pageStr += Latex.arrangeRowInColumns(
                                            data=_data,
                                            positions=_change.getSemitones(),
                                            dataColoured=Latex.makeDataColoured(
                                                _data, _colours
                                            ),
                                            cellColours=_cellColours,
                                            centreResults=way in Book.centredWays,
                                            extraCells=_extraCells,
                                        )
                                    else:
                                        _wayName = way
                                        if "Distinct Chord" in way:
                                            _wayName = (
                                                Change.makeDistinctChordStrPrintable(
                                                    _wayName, _change
                                                )
                                            )
                                        for replacement in Book.wayNameSubs:
                                            _wayName = _wayName.replace(
                                                replacement[0], replacement[1]
                                            )
                                        _pageStr += wayName
                                        for i in _changeByWay:
                                            _pageStr += " & " + str(i)
                                        _pageStr += Latex.commandStrings[
                                            "Table Line Break"
                                        ]

                            elif (
                                    way in Book.tabularWays
                                    and way not in Book.colouredWaysPositional
                            ):
                                # Custom colouring
                                _data = [
                                    prependStr + str(i)
                                    for i in self.byMoreWays(_change, way)
                                ]
                                _wayName = way
                                if "Distinct Chord" in way:
                                    _wayName = Change.makeDistinctChordStrPrintable(
                                        _wayName, _change
                                    )
                                for replacement in Book.wayNameSubs.items():
                                    _wayName = _wayName.replace(
                                        replacement[0], replacement[1]
                                    )
                                _data = [_wayName] + _data

                                _dataColoured = [_wayName] + [
                                    prependStr + str(i)
                                    for i in self.byMoreWays(
                                        _change, way, colourResult=True
                                    )
                                ]
                                if way not in Book.specificPositionalWays:
                                    _positions = _change.getSemitones()
                                else:
                                    _positions = _change.getPositionsOfWay(way)
                                # if len(_change) == 0: _positions = [0]
                                # input('De way is '+way+str(_data)+str(_dataColoured))

                                _pageStr += Latex.arrangeRowInColumns(
                                    data=_data,
                                    positions=_positions,
                                    dataColoured=_dataColoured,
                                    centreResults=way in Book.centredWays,
                                    extraCells=_extraCells,
                                )  # lamar

                            elif way in ("Names",):  # Do not line up to the grid
                                _pageStr += (
                                        way
                                        + _wayNameSeperator
                                        + " " * (_wayNameMaxCharLength - len(way))
                                )
                                _theNames = _change.getScaleNames()
                                _theNamesStr = ""
                                for n, name in enumerate(_theNames):

                                    _theNamesStr += name
                                    if (
                                            len(_theNamesStr.split("\n")[-1])
                                            > Book.maxResultLength
                                    ):
                                        _theNamesStr += "\n"
                                    elif not n == len(_theNames) - 1:
                                        _theNamesStr += ", "
                                    else:
                                        pass  # print ('\n')
                                input("_theNamesStr: {}".format(_theNamesStr))
                                _pageStr += _theNamesStr
                                if Latex.on:
                                    _pageStr += Latex.commandStrings["Line Break"]

                            if way == "Raga":
                                _raagNames = _change.getContainedRagasOtherDirections(
                                    returnNames=True
                                )

                                _raagIndexes = _change.getContainedRagasOtherDirections(
                                    returnIndexes=True,
                                )
                                _raagNames = Utility.flattenList(_raagNames)
                                _raagIndexes = Utility.flattenList(_raagIndexes)

                                # print('rnames{} ridx{}'.format(_raagNames, _raagIndexes))
                                if len(_raagNames) == 1:
                                    print(
                                        "raagNames{} ridx{}".format(
                                            _raagNames, _raagIndexes
                                        )
                                    )
                                    print("""blabh len(_raagNames) > 0""")
                                    Book.oneLineWaysConditional.append("Raga")
                                elif len(_raagNames) > 1:
                                    # input('_raagNames has multiple values {}'.format(_raagNames))
                                    for rdx, r in enumerate(_raagIndexes):

                                        _raagName = _raagNames[rdx]
                                        _pageStr += (
                                                Book.convertRagaDirectionToUnicode(
                                                    _raagNames[rdx]
                                                )
                                                + " "
                                                + _wayNameSeperator
                                        )
                                        _pageStr += (
                                                str(self[r])
                                                + Book.unicodeChars["Change Number"]
                                                + str(r + 1)
                                        )

                                        if r < (len(_raagIndexes) - 1):
                                            _pageStr += "\\hfill "
                                    if Latex.on:
                                        _pageStr += Latex.commandStrings[
                                            "Line Break Small"
                                        ]

                        if (
                                way in Book.oneLineWays
                                or way in Book.oneLineWaysConditional
                        ):
                            if Latex.on == True:
                                # pass
                                _wayNameSeperator = " \\hfill "
                            if way == "Raga":
                                _modifiedChange: Change = self[_raagIndexes[0]]
                                _pageStr += Raga.shortenRagaNameWithSymbols(
                                    _raagNames[0]
                                )
                                _pageStr += _wayNameSeperator
                                Book.oneLineWaysConditional.remove("Raga")
                            else:
                                _modifiedChange: Change = _change.byWays(way)
                                _pageStr += (
                                        Book.makeWayNamePrintable(way) + _wayNameSeperator
                                )

                            _pageStr += " " * (_wayNameMaxCharLength - len(way))
                            if way == "Raga":
                                if Latex.makeTextColoured:
                                    _pageStr += " ".join(
                                        _modifiedChange.straightenDegrees(
                                            allowedNotes=Change.allowedNoteNamesCarnatic
                                        ).getColouredSelf()
                                    )
                                else:
                                    _pageStr += " ".join(
                                        [
                                            str(i) + " "
                                            for i in _modifiedChange.straightenDegrees(
                                            allowedNotes=Change.allowedNoteNamesCarnatic
                                        )
                                        ]
                                    )
                                _pageStr += _wayNameSeperator
                            else:
                                if not isinstance(_modifiedChange, Change):
                                    print(
                                        "change",
                                        _change,
                                        "modifiedChange",
                                        _modifiedChange,
                                        "way",
                                        way,
                                    )
                                    input("blkasjdflkajsdlfkjaslkdjf")
                                _pageStr += (
                                        " ".join(
                                            _modifiedChange.byWays(
                                                "Jazz", colourResult=Latex.on
                                            )
                                        )
                                        + _wayNameSeperator
                                )
                            # print('smokin doobs',_modifiedChange)
                            _pageStr += (
                                    "".join(
                                        _modifiedChange.getHexagram(colourResult=Latex.on)
                                    )
                                    + _wayNameSeperator
                            )

                            _pageStr += (
                                    _modifiedChange.getScaleNames(
                                        searchForDownward=False,
                                        searchForNegative=False,
                                        includeDownwardHexagram=False,
                                    )[0]
                                    + _wayNameSeperator
                            )

                            _pageStr += (
                                    _modifiedChange.getChordQuality() + _wayNameSeperator
                            )
                            _pageStr += _modifiedChange.getChangeNumber(
                                addOneToBookPage=True,
                                returnChapterPage=False,
                                decorateChapter=True,
                                decorateWithSmallCircle=Latex.useSmallCircles,
                                includeNormalisedPageForNegatives=True,
                            )
                            if Latex.on:
                                _pageStr += (
                                    "\\\\"  # Latex.commandStrings['Line Break Small']
                                )

                            """print(Book.unicodeCharConstants['Change Number'] + str(
                                self.byMoreWays(_modifiedChange, 'Change Number') + 1), end='(')
                            print(self.byMoreWays(_modifiedChange, 'Chapter Page'), end=')')"""

                            """print(' '.join(_change.byWays(way).byWays('Jazz')),end =' ')
                            print(Book.renderTitleAndListOfAnswers(self.getTitle(_change.byWays(way)), way,
                                                                               titleAdjustedLength=_wayNameMaxCharLength + len(
                                                                                   _wayNameSeperator),
                                                                               wayNameSeperator=_wayNameSeperator,
                                                                               cellSize=cellPadding,
                                                                               minimumSpaceBetweenItems=1,
                                                                               prependResultWithStr=''
                                                                               ))"""
                    _pageStr += self.getTitle(_change, Book.moreTitleWays)  # + '\\\\'
                    if Latex.on:
                        if _latexTabularOpen:
                            _pageStr += Latex.commandStrings["End Tabular"]

                        _pageStr += self.addPageToTableOfContents(change=_change)
                        # _pageStr += '\\label{fig:Change ' + str(_change.getChangeNumber(addOneToBookPage=True,decorateChapter=False)) + '}\n'
                        # _pageStr += '\\FloatBarrier'
                        # could implement it as the next line
                        # if not any([w in Book.pageCreatingWays for w in ways]):
                        # input('{}\n== _pageStr\n'.format(_pageStr))
                        _pageStr += Latex.commandStrings["End Figure"]
                        if "Instrument Graphics" not in ways and not any(
                                "Keys Diagram" in w for w in ways
                        ):
                            _pageStr += "\\FloatBarrier "
                            _pageStr += "\\newpage\n"
                            # input(_pageStr)

                    _lineBreaks = Latex.getLineBreaks(_pageStr)

                    if True:  # _lineBreaks > Latex.linesPerPage:
                        _pageStr = Latex.changeHStretch(
                            _pageStr, _lineBreaks, showDebug=True
                        )
                    print("for subChange", str(indexNumber + 1))

                    _str += _pageStr

                    if "Instrument Graphics" in ways:
                        _instrumentPage = ""

                        # _instrumentPage += '\\FloatBarrier '
                        _instrumentPage += Latex.commandStrings["Start Figure"]

                        # _instrumentPage += '\\newpage '

                        # _instrumentPage += '\\pagebreak '

                        _instrumentPage += Latex.makeChangeGraphicTable(_change)
                        _instrumentPage += Latex.commandStrings["End Figure"]
                        _instrumentPage += "\\newpage\n"
                        # _instrumentPage += '\\clearpage'
                        _str += _instrumentPage

                    for w in ways:
                        if "Keys Diagram" in w:
                            print(w, w.index("Keys Diagram"))
                            _diagramTypes = w.replace(" Keys Diagram", "").split(" ")

                            if not isinstance(_diagramTypes, (list,)):
                                raise ValueError("balasdfg")
                            # _str += '\\FloatBarrier \\newpage'
                            _str += Latex.commandStrings["Start Figure"]
                            _str += Latex.insertKeysDiagram(
                                change=_change,
                                diagramTypes=_diagramTypes,
                            )
                            _str += Latex.commandStrings["End Figure"]
                            _str += "\\newpage\n"

                    if printToScreenLive:
                        print(_pageStr)
                    _numberOfPagesSuccessful += 1
                    _changeFilename = Latex.getTexPath(
                        change=_change, key=Book.rootColourKey, includeFilename=True
                    )
                    _changeDirectory = Latex.getTexPath(
                        change=_change, key=Book.rootColourKey, includeFilename=False
                    )
                    Project.makeDirectory(_changeDirectory)

                    _texChangeFile = open(_changeFilename, "w+")
                    _texChangeFile.write(Latex.wrapChangeDataWithPreambleEtc(_pageStr))
                    _texChangeFile.close()
                    print("Wrote GOS (Grail Of Scale) file {}".format(_changeFilename))
                    if renderEachPageSeperately:
                        print("rendering pdf from single subChange")
                        Latex.buildFile(
                            filepath=_changeFilename,
                            openFileWhenDone=True,
                            options=[
                                "--shell-escape -output-directory=" + _changeDirectory
                            ],
                            args=[],
                            iterations=3,
                        )
                        input("built file {}".format(_changeFilename))
                    # _addOneQuick = 1
                    # if indexNumber<0: _addOneQuick = -1
                    # input('lines where getItem heppened {}'.format(Book.linesWhereGetItemHappened))
                    # [35005, 35174, 35366, 35367, 10304, 10583]
                    print(
                        "finished making",
                        Book.unicodeChars["Change Number"],
                        str(indexNumber),
                        "/".join(self[indexNumber].getScaleNames()),
                        self[indexNumber],
                        "done ",
                        str(_numberOfPagesSuccessful) + " of",
                        len(indexNumbersToUse),
                        "pages.\nThat is",
                        str(
                            round(
                                100 * _numberOfPagesSuccessful / len(indexNumbersToUse),
                                2,
                            )
                        ),
                        "% complete). + extras total: "
                        + str(_numberOfPagesRendered - _numberOfPagesSuccessful),
                    )
                    input(
                        "{}\n which is _pageStr for {}\nThat is great!!".format(
                            _pageStr, _changeFilename
                        )
                    )
                    break
                except ResultsTooWideError:
                    _extraCells += 1
                    print("results too wide so adding {} cell(s)".format(_extraCells))
                    pass
            _extraCells = 0

            if printResult:
                print(_pageStr)
        """if Latex.useSmallCircles == True:
            print('replacing subChange numbers with circles.')
            for i in range(3):
                _str = Latex.replacePageStrsBySmallCircles(_str)"""
        # Ithink this should be moved into the change loop
        if Latex.makeTexFilesSubfiles:
            _str = Latex.makeTexASubfile(_str)

        return _str
        # if indexNumber != indexNumbersToUse[-1]:
        #    pass
        # print('',end='')
        # print('↡',end='')
        # print('\f',end='') #
        # print('\n')

    def byMoreWays(
            self,
            change: Change,
            ways,
            colourResult=False,
    ):
        if not type(ways) == list:
            ways = [ways]
        if not type(change) == Change:
            raise TypeError(
                change, "should be of type Change, but it is ", type(change)
            )
        for way in ways:
            if JazzNote.isValidWay(way):
                pass
            elif Change.isValidWay(way):
                pass
            elif Book.isValidWay(way):
                pass
            # elif self.getTitle(change=Change(['1']),ways=[way]):
            #    pass
            else:
                raise ValueError(way, " is not a supported way.")
        # change = change.straightenDegrees()

        _byWays = []
        for way in ways:
            _notesByWay = []
            if Book.isValidWay(way):
                if way == "Mode Info":
                    # TODO: Move this into Change
                    # raise ValueError('Use the Change method for that instead of the Book method.')
                    # _modeNames = change.modeNames(searchForDownward=False,includeDownwardHexagram=False,)
                    _modeNames = change.byWays("Mode Name", colourResult=colourResult)

                    # _modeIndexes = self.byMoreWays(change, 'Mode Change Number', colourResult=colourResult)
                    _modeIndexes = [
                        change.mode(i).getChangeNumber(
                            decorateWithSmallCircle=Latex.useSmallCircles,
                            addOneToBookPage=True,
                        )
                        for i in range(len(change.notes))
                    ]
                    # input('_mode indexes {}'.format(_modeIndexes))

                    _modeHexagrams = change.byWays(
                        "Mode Hexagram", colourResult=colourResult
                    )
                    # print('..1',_modeHexagrams)
                    _modeHexagrams = ["".join(i_) for i_ in _modeHexagrams]
                    _modePrimeness = [
                        change.mode(scale).getPrimeness()
                        for scale in range(len(change))
                    ]
                    # print('..2', _modeHexagrams)

                    for note in range(len(change.notes)):
                        _notesByWay.append(
                            _modeHexagrams[note]
                            + " "
                            + Change.infoWaySymbols["Primeness"]
                            + str(_modePrimeness[note])
                            + " "
                            + str(_modeIndexes[note])
                        )

                elif way == "Mode Info Old":

                    _modeNames = change.modeNames()
                    _modeIndexes = self.byMoreWays(change, "Mode Change Number")
                    _modeIndexes = [str(i__) for i__ in _modeIndexes]
                    _modeHexagrams = change.byWays("Mode Hexagram")
                    _modeHexagrams = [" ".join(i_) for i_ in _modeHexagrams]

                    # _notesByWay=self.getTitle(change,self.condensedWays,beginningStr='',seperator='')
                    for i in range(len(_modeHexagrams)):
                        # _str = _modeNames[i] + ' ' + _modeIndexes[i] + ' ' + str(_modeHexagrams[i][0])
                        _str = (
                                _modeNames[i] + " #" + _modeIndexes[i] + _modeHexagrams[i]
                        )
                        # _str = _modeHexagrams[i] +'asdf'
                        _notesByWay.append(_str)
                    # print(_str,_notesByWay[i],'wtfwtf')

                elif way == "Mode Page":
                    # raise ValueError('Use the Change method for that instead of the Book method.')

                    # _modeIndexes = self.modesIndexNumbers(change)
                    _modeIndexes = [
                        change.mode(i).getChangeNumber(
                            decorateWithSmallCircle=Latex.useSmallCircles,
                            addOneToBookPage=True,
                        )
                        for i in range(len(change.notes))
                    ]

                    _notesByWay = _modeIndexes

                # elif way == 'Mode Names':
                # 	for i in range(len(change)):
                #       TODO:Now you're going to have to fix the next line because that first function changed
                # 		_name = ScaleNames.getMainScaleNameForIndex(self.getSequenceNumberFromChange(change.mode(i)),self,defaultWay = 'Hexagram Name')
                # 		if name == '' or name == 'unnamed':
                # 			_name = change.getHexagramName()
                # 		_notesByWay.append(_name)
                elif way == "Change Number":
                    _notesByWay = self.getSequenceNumberFromChange(change)
                    raise ValueError(
                        "Use the Change method for that instead of the Book method."
                    )

                elif way == "Chapter Page":
                    raise ValueError(
                        "Use the Change method for that instead of the Book method."
                    )
                    if len(change.notes) > 0:
                        _notesByWay = JazzNote(str(len(change))).getRomanNumeral()
                        _scaleRomanNumeral = change.byWays("Classical")[0]
                        if _scaleRomanNumeral.lower() == _scaleRomanNumeral:
                            _notesByWay = (
                                JazzNote(str(len(change))).getRomanNumeral().lower()
                            )
                    else:  # Empty Set
                        _notesByWay = "nulla"
                        _scaleRomanNumeral = _notesByWay

                    _notesByWay += "»"
                    _notesByWay += str(
                        self.getIndexNumberInChapterFromChange(change) + 1
                    )
                    # _notesByWay += ')'

                elif way == "Mode Chapter Page":
                    raise ValueError(
                        "Use the Change method for that instead of the Book method."
                    )
                    _modes = []
                    for i in range(len(change)):
                        _modes.append(change.mode(i))
                        _notesByWay.append(self.byMoreWays(_modes[i], "Chapter Page"))
                        # Add one
                elif way == "Chord 🗍":
                    raise ValueError(
                        "Use the Change method for that instead of the Book method."
                    )
                    for i in range(len(change)):
                        _notesByWay.append(
                            1
                            + self.getSequenceNumberFromChange(
                                change.getScaleChord(i, returnTypeChange=True)
                            )
                        )
                elif way == "Piano Diagram":
                    _notesByWay = Latex.insertKeysDiagram(change, ["Piano"])
            elif Change.isValidWay(way):
                if way in Book.carnaticWays:
                    _notesByWay = change.straightenDegrees(
                        allowedNotes=Change.allowedNoteNamesCarnatic
                    ).byWays(way, colourResult=colourResult)
                elif way == "Original Numbers":
                    _notesByWay = change.straightenDegrees(
                        allowedNotes=Change.allowedNoteNamesAllFlats
                    ).byWays(way, colourResult=colourResult)
                else:
                    _notesByWay = change.byWays(way, colourResult=colourResult)

            elif JazzNote.isValidWay(way):
                if way in Change.straightenedWays:
                    if (way) == "Solfege":
                        _allowedNotes = Change.allowedNoteNamesSolfege
                    if (way) == "Jazz":
                        _allowedNotes = Change.allowedNoteNamesJazz
                elif JazzNote.isAlphabetNoteStr(way):
                    _allowedNotes = Change.allowedNoteNamesJazz
                    if change.getSeptatonicInAscendingGenericIntervals(
                            returnTrueIfIsSeptaOrNegaSexta=True
                    ):
                        _notesByWay = (
                            change.getSeptatonicInAscendingGenericIntervals().byWays(
                                way
                            )
                        )
                    else:
                        _notesByWay.append(
                            change.straightenDegrees(allowedNotes=_allowedNotes)
                            .notes[0]
                            .byWay(way)
                        )
                        for note in change.straightenDegrees(
                                allowedNotes=_allowedNotes
                        ):  # for some reason it wasn't including the 1 so I added it in the line before.
                            _notesByWay.append(note.byWayOf(way))
                if not JazzNote.isAlphabetNoteStr(way):
                    """if len(change) > 0:
                        _notesByWay.append(change.notes[0].byWay(way))
                    else:
                        pass"""
                    for (
                            note
                    ) in (
                            change
                    ):  # for some reason it wasn't including the 1 so I added it in the line before.
                        _notesByWay.append(note.byWayOf(way))
            # print('shit', way, change, change.byWays(way))
            _byWays.append(_notesByWay)
        # print('stuff and stuff',_byWays,_byWays[-1])

        if len(ways) == 1 or type(ways) == str:
            return _byWays[0]

        return _byWays

    @classmethod
    def returnCuteSymbolFromInt(cls, integer, cute="plants"):
        _plants = ["🔮", "🍂", "🌱", "🌵", "🍀", "🏵", "🌿", "🌴", "❂", "🏯", "👐", "🍁", "🌹"]
        if cute == "plants":
            if integer > len(_plants):
                raise ValueError("returnCuteSymbol expects a number below twelve")

            return _plants[integer]  # 🐉 🔥  🍁
        # 𐄙𐄚𐄛𐄜𐄝𐄞𐄟𐄠𐄡 🎹

    @classmethod
    def isValidWay(cls, way):
        if way in Book.validWays:
            return True
        # elif Change.isValidWay(way):
        # 	return True
        # elif JazzNote.isValidWay(way):
        # 	return True
        else:
            return False

    @classmethod
    def convertRagaDirectionToUnicode(
            cls, ragaDirectionName: str, directionInBrackets=False
    ):
        _name = ragaDirectionName
        if type(_name) != str:
            raise TypeError(
                "{} .. supposed to be string, but is {}".format(_name, type(_name))
            )
        _name = _name.replace("(ascending)", "(" + Book.unicodeChars["Ascending"] + ")")
        _name = _name.replace(
            "(descending)", "(" + Book.unicodeChars["Descending"] + ")"
        )
        if directionInBrackets == False:
            _name = _name.replace("(", "")
            _name = _name.replace(")", "")
        return _name

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
        c = []
        r = i + 0
        j = 0
        C = Book.C
        for s in range(1, k + 1):
            cs = j + 1
            while r - C(n - cs, k - s) > 0:
                r -= C(n - cs, k - s)
                cs += 1
            c.append(cs)
            j = cs
        return c


Book.theBook = Book()