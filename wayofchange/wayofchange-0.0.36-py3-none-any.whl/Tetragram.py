from Latex import Latex
from Utility import Utility
input = Utility.input
class Tetragram:
    # Tetragrams come from 太玄經 Tài Xuán Jīng
    # Characters from http://www.chinaknowledge.de/Literature/Daoists/taixuanjing.html
    # 首 Tetragrams Head/divisions

    # 樂 short for 樂經／乐经 (Yuèjīng, “Classic of Music”).
    allowedWays = [
        "symbol",
        "name",
        "chinese",
        "pinyin",
        "number",
        "subChange",
        "subpage",
    ]
    semitones = {}
    ternaryList = {}
    #book = Book(
    #    notesToUse=["b2", "2", "b3"],
    #    notesToInclude=["1"],
    #)

    # Digrams
    # ⚌    ⚎    𝌃    ⚍    ⚏    𝌁    𝌂    𝌄    𝌅
    # 1     2     6     4    5     7    3     8    9
    # None are the third bit
    semitones[(0, 1, 2, 3,)] = {
        "number": "1",
        "symbol": "𝌆",
        "name": "Centre",
        "pinyin": "zhōng",
        "chinese": "中",
        "subpage": 8,
    }
    semitones[(1, 2, 3,)] = {
        "number": "2",
        "symbol": "𝌇",
        "name": "Full-Circle",
        "pinyin": "zhōu",
        "chinese": "周",
        "subpage": -8,
    }
    ternaryList[(None, True, True, True)] = {
        "number": "3",
        "symbol": "𝌈",
        "name": "Mired",
        "pinyin": "xián",
        "chinese": "礥",
    }
    semitones[(0, 2, 3,)] = {
        "number": "4",
        "symbol": "𝌉",
        "name": "Barrier",
        "pinyin": "xián",
        "chinese": "閑",
        "simplified": "闲",
        "subpage": 7,
    }  # 閑
    semitones[(2, 3,)] = {
        "number": "5",
        "symbol": "𝌊",
        "name": "Keeping-Small",
        "pinyin": "shǎo",
        "chinese": "少",
        "subpage": -7,
    }
    ternaryList[(None, False, True, True)] = {
        "number": "6",
        "symbol": "𝌋",
        "name": "Contrariety",
        "pinyin": "lì",
        "chinese": "戾",
    }
    ternaryList[(True, None, True, True)] = {
        "number": "7",
        "symbol": "𝌌",
        "name": "Ascent",
        "pinyin": "shàng",
        "chinese": "上",
    }
    ternaryList[(True, None, True, True)] = {
        "number": "8",
        "symbol": "𝌍",
        "name": "Opposition",
        "pinyin": "gàn",
        "chinese": "幹",
    }
    ternaryList[(None, None, True, True)] = {
        "number": "9",
        "symbol": "𝌎",
        "name": "Branching",
        "pinyin": "shū",
        "chinese": "𤕠",
    }
    semitones[(0, 1, 3)] = {
        "number": "10",
        "symbol": "𝌏",
        "name": "Distortion",
        "pinyin": "xiàn",
        "chinese": "羨",
        "subpage": 6,
    }  # Defectiveness
    semitones[(1, 3)] = {
        "number": "11",
        "symbol": "𝌐",
        "name": "Divergence",
        "pinyin": "chà",
        "chinese": "差",
        "subpage": -6,
    }  # M.c. says like 'lack'
    ternaryList[(None, True, False, True)] = {
        "number": "12",
        "symbol": "𝌑",
        "name": "Youthfulness",
        "pinyin": "tóng",
        "chinese": "童",
    }
    semitones[(0, 3)] = {
        "number": "13",
        "symbol": "𝌒",
        "name": "Increase",
        "pinyin": "zēng",
        "chinese": "增",
        "subpage": 4,
    }
    semitones[(3,)] = {
        "number": "14",
        "symbol": "𝌓",
        "name": "Penetration",
        "pinyin": "ruì",
        "chinese": "銳",
        "subpage": -4,
    }
    ternaryList[(None, False, False, True)] = {
        "number": "15",
        "symbol": "𝌔",
        "name": "Reach",
        "pinyin": "dá",
        "chinese": "達",
        "simplified": "达",
    }
    ternaryList[(True, None, False, True)] = {
        "number": "16",
        "symbol": "𝌕",
        "name": "Contact",
        "pinyin": "jiāo",
        "chinese": "交",
    }
    ternaryList[(False, None, False, True)] = {
        "number": "17",
        "symbol": "𝌖",
        "name": "Holding Back",
        "pinyin": "ruǎn",
        "chinese": "耎",
    }
    ternaryList[(None, None, False, True)] = {
        "number": "18",
        "symbol": "𝌗",
        "name": "Waiting",
        "pinyin": "xī",
        "chinese": "徯",
    }
    ternaryList[(True, True, None, True)] = {
        "number": "19",
        "symbol": "𝌘",
        "name": "Following",
        "pinyin": "cóng",
        "chinese": "從",
    }
    ternaryList[(False, True, None, True)] = {
        "number": "20",
        "symbol": "𝌙",
        "name": "Advance",
        "pinyin": "jìn",
        "chinese": "進",
    }
    ternaryList[(None, True, None, True)] = {
        "number": "21",
        "symbol": "𝌚",
        "name": "Release",
        "pinyin": "shì",
        "chinese": "釋",
    }
    ternaryList[(True, False, None, True)] = {
        "number": "22",
        "symbol": "𝌛",
        "name": "Resistance",
        "pinyin": "gé",
        "chinese": "格",
    }
    ternaryList[(False, False, None, True)] = {
        "number": "23",
        "symbol": "𝌜",
        "name": "Ease",
        "pinyin": "yí",
        "chinese": "夷",
    }
    ternaryList[(None, False, None, True)] = {
        "number": "24",
        "symbol": "𝌝",
        "name": "Joy",
        "pinyin": "lè",
        "chinese": "樂",
    }  # Edrihan
    ternaryList[(True, None, None, True)] = {
        "number": "25",
        "symbol": "𝌞",
        "name": "Contention",
        "pinyin": "zhēng",
        "chinese": "爭",
    }
    ternaryList[(False, None, None, True)] = {
        "number": "26",
        "symbol": "𝌟",
        "name": "Endeavor",
        "pinyin": "wù",
        "chinese": "務",
    }
    ternaryList[(None, None, None, True)] = {
        "number": "27",
        "symbol": "𝌠",
        "name": "Duties",
        "pinyin": "shì",
        "chinese": "事",
    }
    semitones[(0, 1, 2)] = {
        "number": "28",
        "symbol": "𝌡",
        "name": "Change",
        "pinyin": "gēng",
        "chinese": "更",
        "subpage": 5,
    }  # jīng
    semitones[(1, 2)] = {
        "number": "29",
        "symbol": "𝌢",
        "name": "Decisiveness",
        "pinyin": "duàn",
        "chinese": "斷",
        "subpage": -5,
    }
    ternaryList[(None, True, True, False)] = {
        "number": "30",
        "symbol": "𝌣",
        "name": "Bold Resolution",
        "pinyin": "yì",
        "chinese": "毅",
    }
    semitones[(0, 2)] = {
        "number": "31",
        "symbol": "𝌤",
        "name": "Packing",
        "pinyin": "zhuāng",
        "chinese": "裝",
        "subpage": 3,
    }
    semitones[(2,)] = {
        "number": "32",
        "symbol": "𝌥",
        "name": "Legion",
        "pinyin": "zhòng",
        "chinese": "衆",
        "subpage": -3,
    }
    ternaryList[(None, False, True, False)] = {
        "number": "33",
        "symbol": "𝌦",
        "name": "Closeness",
        "pinyin": "mì",
        "chinese": "密",
    }
    ternaryList[(True, None, True, False)] = {
        "number": "34",
        "symbol": "𝌧",
        "name": "Kinship",
        "pinyin": "qīn",
        "chinese": "親",
    }
    ternaryList[(True, None, True, False)] = {
        "number": "35",
        "symbol": "𝌨",
        "name": "Gathering",
        "pinyin": "liǎn",
        "chinese": "斂",
    }  # liàn
    ternaryList[(None, None, True, False)] = {
        "number": "36",
        "symbol": "𝌩",
        "name": "Strength",
        "pinyin": "qiáng",
        "chinese": "強",
    }  # qiǎng jiàng
    semitones[(0, 1,)] = {
        "number": "37",
        "symbol": "𝌪",
        "name": "Purity",
        "pinyin": "suì",
        "chinese": "睟",
        "subpage": 2,
    }
    semitones[(1,)] = {
        "number": "38",
        "symbol": "𝌫",
        "name": "Fullness",
        "pinyin": "chéng",
        "chinese": "盛",
        "subpage": -2,
    }  # shèng
    ternaryList[(None, None, True, False)] = {
        "number": "39",
        "symbol": "𝌬",
        "name": "Residence",
        "pinyin": "jū",
        "chinese": "居",
    }
    semitones[(0,)] = {
        "number": "40",
        "symbol": "𝌭",
        "name": "Law",
        "pinyin": "fǎ",
        "chinese": "法",
        "subpage": 1,
    }  # Model  fǎ, fā, fá, fà
    semitones[()] = {
        "number": "41",
        "symbol": "𝌮",
        "name": "Response",
        "pinyin": "yīng",
        "chinese": "應",
        "subpage": -1,
    }  # yìng
    ternaryList[(None, False, False, False)] = {
        "number": "42",
        "symbol": "𝌯",
        "name": "Going to Meet",
        "pinyin": "yù",
        "chinese": "遇",
    }
    ternaryList[(True, None, False, False)] = {
        "number": "43",
        "symbol": "𝌰",
        "name": "Encounters",
        "pinyin": "yíng",
        "chinese": "迎",
    }
    # Note that in traditional Chinese (Taiwan), this character is classified as a variant form of 灶. (44)
    ternaryList[(False, None, False, False)] = {
        "number": "44",
        "symbol": "𝌱",
        "name": "Stove",
        "pinyin": "zào",
        "chinese": "竈",
        "simplified": "灶",
    }
    """ dài
    Used in 大夫 (dàifu, “doctor”).
    Used in 大城(Dàichéng, “Daicheng, Hebei”).
    Used in 大王(dàiwáng, “(in operas, old novels)
    king; ringleader”)."""
    ternaryList[(None, None, False, False)] = {
        "number": "45",
        "symbol": "𝌲",
        "name": "Greatness",
        "pinyin": "dà",
        "chinese": "大",
    }
    ternaryList[(True, True, None, False)] = {
        "number": "46",
        "symbol": "𝌳",
        "name": "Enlargement",
        "pinyin": "kuò",
        "chinese": "廓",
    }
    ternaryList[(False, True, None, False)] = {
        "number": "47",
        "symbol": "𝌴",
        "name": "Pattern",
        "pinyin": "wén",
        "chinese": "文",
    }
    ternaryList[(None, True, None, False)] = {
        "number": "48",
        "symbol": "𝌵",
        "name": "Ritual",
        "pinyin": "lǐ",
        "chinese": "禮",
    }
    ternaryList[(True, False, None, False)] = {
        "number": "49",
        "symbol": "𝌶",
        "name": "Flight",
        "pinyin": "táo",
        "chinese": "逃",
    }
    ternaryList[(False, False, None, False)] = {
        "number": "50",
        "symbol": "𝌷",
        "name": "Vastness",
        "pinyin": "táng",
        "chinese": "唐",
    }  # Wasting
    ternaryList[(None, False, None, False,)] = {
        "number": "51",
        "symbol": "𝌸",
        "name": "Constancy",
        "pinyin": "cháng",
        "chinese": "常",
    }
    ternaryList[(True, None, None, False)] = {
        "number": "52",
        "symbol": "𝌹",
        "name": "Measure",
        "pinyin": "dù",
        "chinese": "度",
    }
    ternaryList[(False, None, None, False)] = {
        "number": "53",
        "symbol": "𝌺",
        "name": "Eternity",
        "pinyin": "yǒng",
        "chinese": "永",
    }
    ternaryList[(None, None, None, False)] = {
        "number": "54",
        "symbol": "𝌻",
        "name": "Unity",
        "pinyin": "kūn",
        "chinese": "昆",
    }
    ternaryList[(True, True, True, None)] = {
        "number": "55",
        "symbol": "𝌼",
        "name": "Diminishment",
        "pinyin": "jiǎn",
        "chinese": "減",
    }
    ternaryList[(False, True, True, None)] = {
        "number": "56",
        "symbol": "𝌽",
        "name": "Closed Mouth",
        "pinyin": "jìn",
        "chinese": "唫",
    }
    ternaryList[(None, False, False, None)] = {
        "number": "57",
        "symbol": "𝌾",
        "name": "Guardedness",
        "pinyin": "shǒu",
        "chinese": "守",
    }
    ternaryList[(True, False, True, None)] = {
        "number": "58",
        "symbol": "𝌿",
        "name": "Gathering In",
        "pinyin": "xī",
        "chinese": "翕",
    }
    ternaryList[(False, False, True, None)] = {
        "number": "59",
        "symbol": "𝍀",
        "name": "Massing",
        "pinyin": "jù",
        "chinese": "聚",
    }
    ternaryList[(None, False, True, None)] = {
        "number": "60",
        "symbol": "𝍁",
        "name": "Accumulation",
        "pinyin": "jī",
        "chinese": "積",
    }
    ternaryList[(True, None, True, None)] = {
        "number": "61",
        "symbol": "𝍂",
        "name": "Embellishment",
        "pinyin": "shì",
        "chinese": "飾",
    }
    ternaryList[(False, None, True, None)] = {
        "number": "62",
        "symbol": "𝍃",
        "name": "Doubt",
        "pinyin": "yí",
        "chinese": "疑",
    }  # níng
    ternaryList[(None, None, True, None)] = {
        "number": "63",
        "symbol": "𝍄",
        "name": "Watch",
        "pinyin": "shì",
        "chinese": "視",
    }
    ternaryList[(True, True, False, None)] = {
        "number": "64",
        "symbol": "𝍅",
        "name": "Sinking",
        "pinyin": "shěn",
        "chinese": "沈",
    }  # Cenkner
    ternaryList[(False, True, False, None)] = {
        "number": "65",
        "symbol": "𝍆",
        "name": "Inner",
        "pinyin": "nèi",
        "chinese": "內",
    }
    ternaryList[(None, True, False, None)] = {
        "number": "66",
        "symbol": "𝍇",
        "name": "Departure",
        "pinyin": "qù",
        "chinese": "去",
    }
    ternaryList[(True, False, False, None)] = {
        "number": "67",
        "symbol": "𝍈",
        "name": "Darkening",
        "pinyin": "huì",
        "chinese": "晦",
    }
    ternaryList[(False, False, False, None)] = {
        "number": "68",
        "symbol": "𝍉",
        "name": "Dimming",
        "pinyin": "méng",
        "chinese": "瞢",
    }
    ternaryList[(None, False, False, None)] = {
        "number": "69",
        "symbol": "𝍊",
        "name": "Exhaustion",
        "pinyin": "qióng",
        "chinese": "窮",
    }
    ternaryList[(True, None, False, None)] = {
        "number": "70",
        "symbol": "𝍋",
        "name": "Severence",
        "pinyin": "gē",
        "chinese": "割",
    }
    ternaryList[(False, None, False, None)] = {
        "number": "71",
        "symbol": "𝍌",
        "name": "Stoppage",
        "pinyin": "zhǐ",
        "chinese": "止",
    }
    ternaryList[(None, None, False, None)] = {
        "number": "72",
        "symbol": "𝍍",
        "name": "Hardness",
        "pinyin": "jiān",
        "chinese": "堅",
    }
    ternaryList[(True, True, None, None,)] = {
        "number": "73",
        "symbol": "𝍎",
        "name": "Completion",
        "pinyin": "chéng",
        "chinese": "成",
    }
    ternaryList[(False, True, None, None,)] = {
        "number": "74",
        "symbol": "𝍏",
        "name": "Closure",
        "pinyin": "zhì",
        "chinese": "䦯",
    }
    ternaryList[(None, True, None, None,)] = {
        "number": "75",
        "symbol": "𝍐",
        "name": "Failure",
        "pinyin": "shī",
        "chinese": "失",
    }
    ternaryList[(True, False, None, None,)] = {
        "number": "76",
        "symbol": "𝍑",
        "name": "Aggravation",
        "pinyin": "jù",
        "chinese": "劇",
    }  # jí
    ternaryList[(False, False, None, None,)] = {
        "number": "77",
        "symbol": "𝍒",
        "name": "Compliance",
        "pinyin": "",
        "chinese": "馴",
    }
    ternaryList[(None, False, None, None,)] = {
        "number": "78",
        "symbol": "𝍓",
        "name": "Verging",
        "pinyin": "xùn",
        "chinese": "將",
    }  # xún On the verge
    ternaryList[(True, None, None, None,)] = {
        "number": "79",
        "symbol": "𝍔",
        "name": "Difficulties",
        "pinyin": "nán",
        "chinese": "難",
    }  # nàn
    ternaryList[(False, None, None, None,)] = {
        "number": "80",
        "symbol": "𝍕",
        "name": "Labouring",
        "pinyin": "qín",
        "chinese": "勤",
    }
    ternaryList[(False, None, None, None,)] = {
        "number": "81",
        "symbol": "𝍖",
        "name": "Fostering",
        "pinyin": "yǎng",
        "chinese": "養",
    }

    if Latex.on and Latex.replaceBuggyPinyinChars:
        for i in semitones:
            for replacement in Latex.pinyinReplacements:
                semitones[i]["pinyin"] = semitones[i]["pinyin"].replace(
                    replacement, Latex.pinyinReplacements[replacement]
                )
        for i in ternaryList:
            for replacement in Latex.pinyinReplacements:
                ternaryList[i]["pinyin"] = ternaryList[i]["pinyin"].replace(
                    replacement, Latex.pinyinReplacements[replacement]
                )

    @classmethod
    def makeTable(
        cls, arrangePositionsByWay=True, flipAxes=False, rewriteFile=True
    ) -> str:
        printWays = Tetragram.allowedWays
        _str = ""
        rows = []
        for t, tetragram in enumerate(Tetragram.semitones):
            rows.append([])
            for way in printWays:
                if way in Tetragram.semitones[tetragram].keys():
                    # rows[-1].append(Tetragram.notesets[tetragram][way])
                    rows[-1].append(
                        Change.makeFromSet(tetragram).getTetragram(
                            [way], decorateWithSmallCircle=True
                        )[0]
                    )
                else:
                    # print(Change.isValidWay('Change Number'))
                    # input('else' + way)

                    if way == "subChange":
                        way = "Change Number"
                    if Change.isValidWay(way):
                        # input('is valid change way')
                        for t, transposition in enumerate((0, 4, 8)):
                            _change = Change.makeFromSet(
                                [s + transposition for s in tetragram]
                            )
                            rows[-1].append(_change.byWays(way))
                    else:
                        raise TypeError("{} is not a validWay of Change".format(way))

        if flipAxes:
            rows = Utility.flipAxesOfList(rows)
        _str += Latex.makeTabular(rows)
        if rewriteFile:
            _filename = Project.tetragramTableFilename
            text_file = open(_filename, "w")
            text_file.write("%s" % _str)
            text_file.close()
            print("rewrote", _filename)
        print(_str)
        input("thar be rows")

    @classmethod
    def allPinyin(cls):
        for i in cls.semitones.keys():
            print(cls.semitones[i]["pinyin"])
        for i in cls.ternaryList.keys():
            print(cls.ternaryList[i]["pinyin"])