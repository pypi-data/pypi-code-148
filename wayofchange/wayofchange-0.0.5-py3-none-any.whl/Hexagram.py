from __future__ import annotations, print_function
from Utility import Utility
input = Utility.input
class Hexagram:
    validWays = [
        "Change",
        "symbol",
        "braille",
        "name",
        "secondName",
        "chinese",
        "pinyin",
        "number",
        "subChange",
        "codon",
        "subpage",
        "syllable",
        "story",
        "story end",
    ]
    titleWays = [
        "symbol",
        "braille",
        "name",
        "chinese",
        "pinyin",
        "number",
        "subChange",
        "codon",
        "subpage",
    ]


    # input('{} the hexagram book above'.format([i for i in book]))
    # 易經 yì jīng

    #TODO:Move displayHexagrams() somewhere else

    '''
    book = Book(notesToUse=["b2", "2", "b3", "3", "4"], notesToInclude=["1"])
    @classmethod
    def displayHexagrams(self):
        print("here is the book of hexagrams")
        
        for i, c in enumerate(Hexagram.book.sequence):
            print(
                i + 1,
                "   ",
                Hexagram.book[i],
                Hexagram.book[i].getHexagram(
                    ["name", "symbol"], concatenatePerHexagram=True
                )[0],
            )
            i *= -1
            print(
                i - 1,
                "   ",
                Hexagram.book[i],
                Hexagram.book[i].getHexagram(
                    ["name", "symbol"], concatenatePerHexagram=True
                )[0],
            )
        print("end the book of hexagrams")
    ''' #See TODO above this block
    notesets = []
    for i in range(65):
        notesets.append("")
    notesets[2] = []
    notesets[24] = [0]
    notesets[7] = [1]
    notesets[15] = [2]
    notesets[16] = [3]
    notesets[8] = [4]
    notesets[23] = [5]
    notesets[19] = [0, 1]
    notesets[36] = [0, 2]
    notesets[51] = [0, 3]
    notesets[3] = [0, 4]
    notesets[27] = [0, 5]
    notesets[46] = [1, 2]
    notesets[40] = [1, 3]
    notesets[29] = [1, 4]
    notesets[4] = [1, 5]
    notesets[62] = [2, 3]
    notesets[39] = [2, 4]
    notesets[52] = [2, 5]
    notesets[45] = [3, 4]
    notesets[35] = [3, 5]
    notesets[20] = [4, 5]
    notesets[11] = [0, 1, 2]
    notesets[54] = [0, 1, 3]
    notesets[60] = [0, 1, 4]
    notesets[41] = [0, 1, 5]
    notesets[55] = [0, 2, 3]
    notesets[63] = [0, 2, 4]
    notesets[22] = [0, 2, 5]
    notesets[17] = [0, 3, 4]
    notesets[21] = [0, 3, 5]
    notesets[42] = [0, 4, 5]
    notesets[32] = [1, 2, 3]
    notesets[48] = [1, 2, 4]
    notesets[18] = [1, 2, 5]
    notesets[47] = [1, 3, 4]
    notesets[64] = [1, 3, 5]
    notesets[59] = [1, 4, 5]
    notesets[31] = [2, 3, 4]
    notesets[56] = [2, 3, 5]
    notesets[53] = [2, 4, 5]
    notesets[12] = [3, 4, 5]
    notesets[34] = [0, 1, 2, 3]
    notesets[5] = [0, 1, 2, 4]
    notesets[26] = [0, 1, 2, 5]
    notesets[58] = [0, 1, 3, 4]
    notesets[38] = [0, 1, 3, 5]
    notesets[61] = [0, 1, 4, 5]
    notesets[49] = [0, 2, 3, 4]
    notesets[30] = [0, 2, 3, 5]
    notesets[37] = [0, 2, 4, 5]
    notesets[25] = [0, 3, 4, 5]
    notesets[28] = [1, 2, 3, 4]
    notesets[50] = [1, 2, 3, 5]
    notesets[57] = [1, 2, 4, 5]
    notesets[6] = [1, 3, 4, 5]
    notesets[33] = [2, 3, 4, 5]
    notesets[43] = [0, 1, 2, 3, 4]
    notesets[14] = [0, 1, 2, 3, 5]
    notesets[9] = [0, 1, 2, 4, 5]
    notesets[10] = [0, 1, 3, 4, 5]
    notesets[13] = [0, 2, 3, 4, 5]
    notesets[44] = [1, 2, 3, 4, 5]
    notesets[1] = [0, 1, 2, 3, 4, 5]
    namesNoun = ["not a valid hexagram"]
    names = ["not a valid hexagram"]
    names.insert(1, "Creative")  # Force
    namesNoun.insert(1, "Creation")
    names.insert(2, "Receptive")  # Field
    namesNoun.insert(2, "Receptivity")
    names.insert(3, "Sprouting")
    namesNoun.insert(3, "Sprout")
    names.insert(4, "Naïve")  # Formative Learning Enveloping
    namesNoun.insert(4, "Naïvety")
    names.insert(5, "Waiting")  # Biding Waiting Attending
    namesNoun.insert(5, "Wait")
    names.insert(6, "Arguing")
    namesNoun.insert(6, "Argument")
    names.insert(7, "Leading")
    namesNoun.insert(7, "Leader")
    names.insert(8, "Uniting")  # Unity Grouping
    namesNoun.insert(8, "Unity")
    names.insert(9, "Homegrown")  # Small Harvest, Microfarmed
    namesNoun.insert(9, "Homegrow")
    names.insert(10, "Treading")
    namesNoun.insert(10, "Treader")
    names.insert(11, "Peaceful")  # Pervading
    namesNoun.insert(11, "Peace")
    names.insert(12, "Obstructing")
    namesNoun.insert(12, "Obstruction")
    names.insert(13, "Fellow")
    namesNoun.insert(13, "Fellowship")
    names.insert(14, "Prosperous")  # Prosperous Reserving Great Possesion. Prosperous
    namesNoun.insert(
        14, "Prosperity"
    )  # Prosperity Reserving Great Possesion. Prosperous
    names.insert(15, "Humble")  # Humble Humbling
    namesNoun.insert(15, "Humility")  # Humble Humbling
    names.insert(16, "Confident")  # Providing For Enthusiastic
    namesNoun.insert(16, "Confidence")  # Providing For Enthusiastic
    names.insert(17, "Following")
    namesNoun.insert(17, "Follower")
    names.insert(18, "Correcting")
    namesNoun.insert(18, "Correction")
    names.insert(19, "Arriving")  # Nearing
    namesNoun.insert(19, "Arrival")  # Nearing
    names.insert(20, "Seeing")  # Viewing
    namesNoun.insert(20, "Seer")  # Viewing
    names.insert(21, "Biting")  # Nibbling Gnawing Bite
    namesNoun.insert(21, "Bite")  # Nibbling Gnawing Bite
    names.insert(22, "Adorning")
    namesNoun.insert(22, "Adornment")
    names.insert(23, "Splitting")  # Stripping
    namesNoun.insert(23, "Split")
    names.insert(24, "Returning")
    namesNoun.insert(24, "Return")
    names.insert(25, "Integrating")  # Innocence
    namesNoun.insert(25, "Integrity")  # Innocence
    names.insert(26, "Cultivating")  # Great Accumulation
    namesNoun.insert(26, "Cultivation")  # Great Accumulation
    names.insert(27, "Nourishing")  # Swallowing
    namesNoun.insert(27, "Nourishment")  # Swallowing
    names.insert(28, "Excessive")  # Great Exceeding
    namesNoun.insert(28, "Excess")  # Great Exceeding
    names.insert(29, "Chasmic")  # Gorge
    namesNoun.insert(29, "Chasm")  # Gorge
    names.insert(30, "Distanced")  # Distant Radiance
    namesNoun.insert(30, "Distance")  # Distant Radiance
    names.insert(31, "Magnetic")  # Conjoined
    namesNoun.insert(31, "Magnet")
    names.insert(32, "Persevering")
    namesNoun.insert(32, "Perseverance")
    names.insert(33, "Retiring")
    namesNoun.insert(33, "Retirement")
    names.insert(34, "Mighty")  # Great invigorating
    namesNoun.insert(34, "Might")  # Great invigorating
    names.insert(35, "Promoting")
    namesNoun.insert(35, "Promotion")
    names.insert(36, "Eclipsing")  # Intelligence Hidden
    namesNoun.insert(36, "Eclipse")  # Intelligence Hidden
    names.insert(37, "Kindred")  # Dwelling people
    namesNoun.insert(37, "Kin")  # Dwelling people
    names.insert(38, "Polarising")
    namesNoun.insert(38, "Polarity")
    names.insert(39, "Limping")
    namesNoun.insert(39, "Limp")
    names.insert(40, "Delivered")
    namesNoun.insert(40, "Deliverance")
    names.insert(41, "Declining")  # Diminishing
    namesNoun.insert(41, "Decline")
    names.insert(42, "Benefitting")  # Augmenting
    namesNoun.insert(42, "Benefit")
    names.insert(43, "Deciding")  # Displacement
    namesNoun.insert(43, "Decision")  # Displacement
    names.insert(44, "Coupling")
    namesNoun.insert(44, "Couple")
    names.insert(45, "Clustering")
    namesNoun.insert(45, "Cluster")
    names.insert(46, "Ascending")
    namesNoun.insert(46, "Ascent")
    names.insert(47, "Confining")
    namesNoun.insert(47, "Confinement")
    names.insert(48, "Sourced")  # Welling
    namesNoun.insert(48, "Source")  # Welling
    names.insert(49, "Revolving")  # Molting, Skinning
    namesNoun.insert(49, "Revolution")  # Molting, Skinning
    names.insert(50, "Holding")
    namesNoun.insert(50, "Hold")
    names.insert(51, "Thundering")  # Shake
    namesNoun.insert(51, "Thunder")  # Shake
    names.insert(52, "Still")  # Bound
    namesNoun.insert(52, "Stillness")  # Bound
    names.insert(53, "Infiltrating")
    namesNoun.insert(53, "Infiltrator")
    names.insert(54, "Betrothing")  # Converting the Maiden
    namesNoun.insert(54, "Betrothed")  # Converting the Maiden
    names.insert(55, "Abundant")
    namesNoun.insert(55, "Abundance")
    names.insert(56, "Wandering")  # Soujourning
    namesNoun.insert(56, "Wanderer")  # Soujourning
    names.insert(57, "Osmotic")  # Ground Wind
    namesNoun.insert(57, "Osmosis")  # Ground Wind
    names.insert(58, "Joyous")  # Open
    namesNoun.insert(58, "Joy")  # Open
    names.insert(59, "Dispersing")
    namesNoun.insert(59, "Dispersal")
    names.insert(60, "Composed")  # Composed Articulating
    namesNoun.insert(60, "Composition")  # Composed Articulating
    names.insert(61, "True")  # Inner Truth
    namesNoun.insert(61, "Truth")  # Inner Truth
    names.insert(62, "Detailed")
    namesNoun.insert(62, "Detail")
    names.insert(63, "Completed")
    namesNoun.insert(63, "Completion")
    names.insert(64, "Incomplete")  # 'Before-Completion'
    namesNoun.insert(64, "Incompletion")  # 'Before-Completion'
    maxHexagramNameLength = 0
    maxHexagramName = ""

    chinese = []
    pinyin = []
    pinyin.insert(0, "")
    chinese.insert(0, "")  # Easter Egg Error not a valid hexagram
    pinyin.insert(1, "qián")
    chinese.insert(1, "乾")  # ䷀ Creative
    pinyin.insert(2, "kūn")
    chinese.insert(2, "坤")  # ䷁ Receptive
    pinyin.insert(3, "zhūn")
    chinese.insert(3, "屯")  # ䷂ Sprouting
    pinyin.insert(4, "méng")
    chinese.insert(4, "蒙")  # ䷃ Formative
    pinyin.insert(5, "xū")
    chinese.insert(5, "需")  # ䷄ Biding
    pinyin.insert(6, "sòng")
    chinese.insert(6, "訟")  # ䷅ Arguing
    pinyin.insert(7, "shī")
    chinese.insert(7, "師")  # ䷆ Leading
    pinyin.insert(8, "bǐ")
    chinese.insert(8, "比")  # ䷇ Comparing
    pinyin.insert(9, "xiǎo chù")
    chinese.insert(9, "小畜")  # ䷈ Homegrown
    pinyin.insert(10, "lǚ")
    chinese.insert(10, "履")  # ䷉ Treading
    pinyin.insert(11, "tài")
    chinese.insert(11, "泰")  # ䷊ Peace
    pinyin.insert(12, "pǐ")
    chinese.insert(12, "否")  # ䷋ Obstruction fǒu
    pinyin.insert(13, "tóng rén")
    chinese.insert(13, "同人")  # ䷌ Fellowship
    pinyin.insert(14, "dà yǒu")
    chinese.insert(14, "大有")  # ䷍ Prosperous
    pinyin.insert(15, "qiān")
    chinese.insert(15, "謙")  # ䷎ Humble
    pinyin.insert(16, "yù")
    chinese.insert(16, "豫")  # ䷏ Confident
    pinyin.insert(17, "suí")
    chinese.insert(17, "隨")  # ䷐ Following
    pinyin.insert(18, "gǔ")
    chinese.insert(18, "蠱")  # ䷑ Correcting
    pinyin.insert(19, "lín")
    chinese.insert(19, "臨")  # ䷒ Arrived
    pinyin.insert(20, "guān")
    chinese.insert(20, "觀")  # ䷓ Seeing
    pinyin.insert(21, "shì kè")
    chinese.insert(21, "噬嗑")  # ䷔ Biting
    pinyin.insert(22, "bì")
    chinese.insert(22, "賁")  # ䷕ Adorning
    pinyin.insert(23, "bō")
    chinese.insert(23, "剝")  # ䷖ Stripping
    pinyin.insert(24, "fù")
    chinese.insert(24, "復")  # ䷗ Returning
    pinyin.insert(25, "wú wàng")
    chinese.insert(25, "無妄")  # ䷘ Integrity
    pinyin.insert(26, "dà chù")
    chinese.insert(26, "大畜")  # ䷙ Cultivating
    pinyin.insert(27, "yí")
    chinese.insert(27, "頤")  # ䷚ Nourishment
    pinyin.insert(28, "dà guò")
    chinese.insert(28, "大過")  # ䷛ Excess
    pinyin.insert(29, "kǎn")
    chinese.insert(29, "坎")  # ䷜ Chasm
    pinyin.insert(30, "lí")
    chinese.insert(30, "離")  # ䷝ Radiance
    pinyin.insert(31, "xián")
    chinese.insert(31, "咸")  # ䷞ Conjoining
    pinyin.insert(32, "héng")
    chinese.insert(32, "恆")  # ䷟ Persevering
    pinyin.insert(33, "dùn")
    chinese.insert(33, "遯")  # ䷠ Retiring
    pinyin.insert(34, "dà zhuàng")
    chinese.insert(34, "大壯")  # ䷡ Might
    pinyin.insert(35, "jìn")
    chinese.insert(35, "晉")  # ䷢Promotion
    pinyin.insert(36, "míng yí")
    chinese.insert(36, "明夷")  # ䷣ Eclipse
    pinyin.insert(37, "jiā rén")
    chinese.insert(37, "家人")  # ䷤ Family
    pinyin.insert(38, "kuí")
    chinese.insert(38, "睽")  # ䷥polarising
    pinyin.insert(39, "jiǎn")
    chinese.insert(39, "蹇")  # ䷦ Limping
    pinyin.insert(40, "xiè")
    chinese.insert(40, "解")  # ䷧ Deliverance
    pinyin.insert(41, "sǔn")
    chinese.insert(41, "損")  # ䷨ Diminishing
    pinyin.insert(42, "yì")
    chinese.insert(42, "益")  # ䷩ Augmenting
    pinyin.insert(43, "guài")
    chinese.insert(43, "夬")  # ䷪ Decision
    pinyin.insert(44, "gòu")
    chinese.insert(44, "姤")  # ䷫ Coupling
    pinyin.insert(45, "cuì")
    chinese.insert(45, "萃")  # ䷬ Clustering
    pinyin.insert(46, "shēng")
    chinese.insert(46, "升")  # ䷭ Ascending
    pinyin.insert(47, "kùn")
    chinese.insert(47, "困")  # ䷮ Confining
    pinyin.insert(48, "jǐng")
    chinese.insert(48, "井")  # ䷯ Source
    pinyin.insert(49, "gé")
    chinese.insert(49, "革")  # ䷰ Revolution
    pinyin.insert(50, "dǐng")
    chinese.insert(50, "鼎")  # ䷱ Holding
    pinyin.insert(51, "zhèn")
    chinese.insert(51, "震")  # ䷲ Thunder
    pinyin.insert(52, "gèn")
    chinese.insert(52, "艮")  # ䷳ Stillness
    pinyin.insert(53, "jiàn")
    chinese.insert(53, "漸")  # ䷴ Infiltrating
    pinyin.insert(54, "guī mèi")
    chinese.insert(54, "歸妹")  # ䷵ Betrothing
    pinyin.insert(55, "fēng")
    chinese.insert(55, "豐")  # ䷶ Abounding
    pinyin.insert(56, "lǚ")
    chinese.insert(56, "旅")  # ䷷ Wanderer
    pinyin.insert(57, "xùn")
    chinese.insert(57, "巽")  # ䷸ Osmosis
    pinyin.insert(58, "duì")
    chinese.insert(58, "兌")  # ䷹ Joyous
    pinyin.insert(59, "huàn")
    chinese.insert(59, "渙")  # ䷺ Dispersing
    pinyin.insert(60, "jié")
    chinese.insert(60, "節")  # ䷻ Composed
    pinyin.insert(61, "zhōng fú")
    chinese.insert(61, "中孚")  # ䷼ Truth
    pinyin.insert(62, "xiǎo guò")
    chinese.insert(62, "小過")  # ䷽ Detail
    pinyin.insert(63, "jì jì")
    chinese.insert(63, "既濟")  # ䷾ Completed
    pinyin.insert(64, "wèi jì")
    chinese.insert(64, "未濟")  # ䷿ Unfinished

    subChange = []
    subChange.insert(0, 0)  # not a valid hexagram
    subChange.insert(1, 32)  # Creative
    subChange.insert(2, -1)  # Receptive
    subChange.insert(3, 5)  # Sprouting
    subChange.insert(4, -10)  # Naïve
    subChange.insert(5, 18)  # Biding
    subChange.insert(6, -30)  # Arguing
    subChange.insert(7, -2)  # Leading
    subChange.insert(8, -5)  # Comparing
    subChange.insert(9, 29)  # Homegrown
    subChange.insert(10, 30)  # Treading
    subChange.insert(11, 7)  # Peace
    subChange.insert(12, -26)  # Obstruction
    subChange.insert(13, 31)  # Fellowship
    subChange.insert(14, 28)  # Resevoir
    subChange.insert(15, -3)  # Humble
    subChange.insert(16, -4)  # Confident
    subChange.insert(17, 14)  # Following
    subChange.insert(18, -19)  # Correcting
    subChange.insert(19, 2)  # Arrived
    subChange.insert(20, -16)  # Seeing
    subChange.insert(21, 15)  # Biting
    subChange.insert(22, 13)  # Adorning
    subChange.insert(23, -6)  # Stripping
    subChange.insert(24, 1)  # Returning
    subChange.insert(25, 26)  # Integrity
    subChange.insert(26, 19)  # Cultivating
    subChange.insert(27, 6)  # Nourishment
    subChange.insert(28, -27)  # Excess
    subChange.insert(29, -9)  # Chasm
    subChange.insert(30, 24)  # Distanced
    subChange.insert(31, -23)  # Conjoining
    subChange.insert(32, -17)  # Persevering
    subChange.insert(33, -31)  # Retiring
    subChange.insert(34, 17)  # Might
    subChange.insert(35, -15)  # Prospering
    subChange.insert(36, 3)  # Eclipse
    subChange.insert(37, 25)  # Family
    subChange.insert(38, 21)  # Polarising
    subChange.insert(39, -12)  # Limping
    subChange.insert(40, -8)  # Deliverance
    subChange.insert(41, 10)  # Diminishing
    subChange.insert(42, 16)  # Augmenting
    subChange.insert(43, 27)  # Decision
    subChange.insert(44, -32)  # Coupling
    subChange.insert(45, -14)  # Clustering
    subChange.insert(46, -7)  # Ascending
    subChange.insert(47, -20)  # Confining
    subChange.insert(48, -18)  # Source
    subChange.insert(49, 23)  # Revolution
    subChange.insert(50, -28)  # Holding
    subChange.insert(51, 4)  # Thunder
    subChange.insert(52, -13)  # Stillness
    subChange.insert(53, -25)  # Infiltrating
    subChange.insert(54, 8)  # Betrothing
    subChange.insert(55, 11)  # Abounding
    subChange.insert(56, -24)  # Wanderer
    subChange.insert(57, -29)  # Osmosis
    subChange.insert(58, 20)  # Joyous
    subChange.insert(59, -22)  # Dispersing
    subChange.insert(60, 9)  # Composed
    subChange.insert(61, 22)  # Truth
    subChange.insert(62, -11)  # Detail
    subChange.insert(63, 12)  # Completed
    subChange.insert(64, -21)  # Unfinished

    symbol = ["Easter Egg Error"]  # Easter Egg Error
    storyBeginning = []
    storyEnd = []

    storyBeginning.insert(0, """""")
    storyEnd.insert(0, """""")

    symbol.insert(1, "䷀")  # ䷀Creative #Force
    storyBeginning.insert(1, """Full of energy, it emanates from nothing""")
    storyEnd.insert(1, """outwardly expanding this generative force""")

    symbol.insert(2, "䷁")  # ䷁Receptive #Field
    storyBeginning.insert(
        2, """Allowing the external to enter, the reality is fostered"""
    )
    storyEnd.insert(2, """unfolding into the embrace of an enveloping field""")

    symbol.insert(3, "䷂")  # ䷂Sprouting #Birth pangs
    storyBeginning.insert(3, """Beginning the venture is accompanied by birth pangs""")
    storyEnd.insert(3, """in processing disorder, growth occurs""")

    symbol.insert(4, "䷃")  # ䷃Formative Naïve Learning Enveloping
    storyBeginning.insert(4, """To learn mastery is to accept one's failure """)
    storyEnd.insert(4, """although the road to maturity is fraught with folly""")

    symbol.insert(5, "䷄")  # Biding Waiting Attending
    storyBeginning.insert(5, """It isn't what you do, but when you do it""")
    storyEnd.insert(5, """having attended to the future window of opportunity""")

    symbol.insert(6, "䷅")  # ䷅Arguing
    storyBeginning.insert(6, """Disagreement leads to a battle of words""")
    storyEnd.insert(6, """when water opposes the sky and there is conflict""")

    symbol.insert(7, "䷆")  # ䷆Leading
    storyBeginning.insert(7, """The way is shown them by one who knows of it""")
    storyEnd.insert(7, """when plans proceed with unified direction""")

    symbol.insert(8, "䷇")  # ䷇Unity #grouping
    storyBeginning.insert(8, """Wave groups collecting in my voice""")
    storyEnd.insert(8, """where myriad manifestions come from a single source""")

    symbol.insert(9, "䷈")  # ䷈Homegrown #Small Harvest, Microfarmed
    storyBeginning.insert(9, """The road is travelled one footstep at a time""")
    storyEnd.insert(9, """the successful harvest sown of few seeds""")

    symbol.insert(10, "䷉")  # ䷉Treading
    storyBeginning.insert(10, """The dance on the tiger's tail continues""")
    storyEnd.insert(10, """one's head remains above water""")

    symbol.insert(11, "䷊")  # ䷊Peace Pervading
    storyBeginning.insert(
        11, """As people stop fighting the flow abounds"""
    )  # When people stop fighting everything the flow abounds
    storyEnd.insert(
        11, """fulfilling the prosperous tendency of collaboration"""
    )  # and the fulfillment of the natural world bursts prosperously

    symbol.insert(12, "䷋")  # ䷋Obstruction
    storyBeginning.insert(
        12, """Great ideas get buried as lesser rulers construct walls"""
    )
    storyEnd.insert(12, """until tripping on an unseen, protruding object""")

    symbol.insert(13, "䷌")  # ䷌Fellowship
    storyBeginning.insert(13, """There is comraderie in the collective psyche""")
    storyEnd.insert(13, """together doing it with the tribe""")

    symbol.insert(14, "䷍")  # ䷍Prosperous Great Possession
    storyBeginning.insert(14, """Truly rich is the person who needs nothing""")
    storyEnd.insert(14, """having followed a path to great possession.""")

    symbol.insert(15, "䷎")  # ䷎Modest Humbling
    storyBeginning.insert(15, """The master never brags about their strength""")
    storyEnd.insert(15, """unbreaking, like the reed that bends back""")

    symbol.insert(16, "䷏")  # ䷏Enthusiastic Providing For
    storyBeginning.insert(16, """It happens with the spirit of giving""")
    storyEnd.insert(16, """because the joy of providing inspires enthusiasm""")

    symbol.insert(17, "䷐")  # ䷐Following
    storyBeginning.insert(17, """The student learns from the teacher""")
    storyEnd.insert(17, """thus they take their position behind the head""")

    symbol.insert(18, "䷑")  # ䷑Correcting
    storyBeginning.insert(
        18, """Comprehension is enlightened by the detail"""
    )  # There is indeed poison in the air to be filtered
    storyEnd.insert(18, """despite troublesome work in the declining society""")

    symbol.insert(19, "䷒")  # ䷒Nearing
    storyBeginning.insert(19, """You approach the horizon's vanishing point""")
    storyEnd.insert(19, """as the train rolls ever closer to the next station""")

    symbol.insert(20, "䷓")  # ䷓Viewing
    storyBeginning.insert(20, """Observe how it looks so different from this angle""")
    storyEnd.insert(20, """going in and checking it out again""")

    symbol.insert(21, "䷔")  # ䷔Biting Nibbling #Gnawing Bite
    storyBeginning.insert(21, """Cutting through what lies in between""")
    storyEnd.insert(21, """like knives to butter, or rain through stone""")

    symbol.insert(22, "䷕")  # ䷕Adorning
    storyBeginning.insert(22, """The embellishment enhances the pre-existing form""")
    storyEnd.insert(
        22, """ornately presented in its signature style"""
    )  # so dress it signature-style as it proves its real worth

    symbol.insert(23, "䷖")  # ䷖Stripping
    storyBeginning.insert(23, """A veil of deception melts away to reveal the truth""")
    storyEnd.insert(23, """which is how inauthentic things are shown as such""")

    symbol.insert(24, "䷗")  # ䷗Returning
    storyBeginning.insert(24, """Coming back to where the thing really started""")
    storyEnd.insert(24, """making the pilgrimage back to the beginning""")

    symbol.insert(25, "䷘")  # ䷘Integrity Innocence
    storyBeginning.insert(25, """Kindness and honesty have been acted upon""")
    storyEnd.insert(25, """with positive will, the correct action takes place""")

    symbol.insert(26, "䷙")  # ䷙Cultivating # Great Accumulation
    storyBeginning.insert(26, """The idea that we stand on a goldmine has developed""")
    storyEnd.insert(26, """allowing the Earth to provide limitless wealth""")

    symbol.insert(27, "䷚")  # ䷚Nourishment Swallowing
    storyBeginning.insert(27, """Sustenance has thankfully been received""")
    storyEnd.insert(27, """ingesting what is really needed""")  # HERE

    symbol.insert(28, "䷛")  # ䷛Excess Great Exceeding
    storyBeginning.insert(28, """The cup is full to the risk of spilling""")
    storyEnd.insert(28, """and this reality could hardly become greater""")

    symbol.insert(29, "䷜")  # ䷜Chasm Gorge
    storyBeginning.insert(29, """A black hole is observed at the galaxy's edge""")
    storyEnd.insert(29, """while a perilous chasm can be seen nearby""")

    symbol.insert(30, "䷝")  # ䷝Radiance
    storyBeginning.insert(30, """Be careful of exceptional beauty before you""")
    storyEnd.insert(30, """which shines brightly like the light of nature""")

    symbol.insert(31, "䷞")  # ䷞Conjoining
    storyBeginning.insert(31, """The forest's roots have become intertwined.""")
    storyEnd.insert(31, """which has fused ideas that once seemed separate""")

    symbol.insert(32, "䷟")  # ䷟Persevering
    storyBeginning.insert(32, """To reach the end is to continue on the way""")
    storyEnd.insert(32, """so let us keep on keeping on and make it""")

    symbol.insert(33, "䷠")  # ䷠Retiring
    storyBeginning.insert(33, """The day arrives that leaves fall""")
    storyEnd.insert(33, """in the advance towards rest well-deserved""")

    symbol.insert(34, "䷡")  # ䷡Might #Great invigorating
    storyBeginning.insert(34, """The great strength is invigorated""")
    storyEnd.insert(34, """in the way that forceful power shows itself""")

    symbol.insert(35, "䷢")  # ䷢Promotion
    storyBeginning.insert(35, """This one has been selected for advancement""")
    storyEnd.insert(35, """which leads to success and the action rewarded""")

    symbol.insert(36, "䷣")  # ䷣Eclipse  #Intelligence Hidden
    storyBeginning.insert(36, """Intelligence is hidden below the surface""")
    storyEnd.insert(36, """where beneath the film of the seen lies the reality""")

    symbol.insert(37, "䷤")  # ䷤Family
    storyBeginning.insert(37, """We are who we are and with those with us""")
    storyEnd.insert(37, """within the inter-relation of our kind and fellowship""")

    symbol.insert(38, "䷥")  # ䷥Polarising
    storyBeginning.insert(38, """A strong dichotomy in views seperates into camps""")
    storyEnd.insert(38, """being that they are set against each other""")

    symbol.insert(39, "䷦")  # ䷦Limping
    storyBeginning.insert(39, """One side doesn't work like it used to""")
    storyEnd.insert(39, """the journey made without full use of both legs""")

    symbol.insert(40, "䷧")  # ䷧Deliverance
    storyBeginning.insert(40, """Eventually good karma illuminates the struggle""")
    storyEnd.insert(40, """given that fate ultimately shows its light""")

    symbol.insert(41, "䷨")  # ䷨Diminishing
    storyBeginning.insert(41, """The cup spills over its brim, its volume adjusting""")
    storyEnd.insert(41, """in the way that what was becomes less""")

    symbol.insert(42, "䷩")  # ䷩Augmenting
    storyBeginning.insert(
        42, """Whatever it is is increasing"""
    )  # There is an increase happening successfully
    storyEnd.insert(42, """making more of what was already there""")

    symbol.insert(43, "䷪")  # ䷪Decision Displacement
    storyBeginning.insert(43, """There is committal to proceed""")
    storyEnd.insert(43, """and this has been conclusively chosen """)

    symbol.insert(44, "䷫")  # ䷫Coupling
    storyBeginning.insert(44, """Forming union, two have become one""")
    storyEnd.insert(44, """thereby the yin and yang come together""")

    symbol.insert(45, "䷬")  # ䷬Clustering
    storyBeginning.insert(45, """Orbiting planets get pulled to their sun""")
    storyEnd.insert(45, """just how schools of fish murmurate and collect""")

    symbol.insert(46, "䷭")  # ䷭Ascending
    storyBeginning.insert(46, """The journey takes them higher""")
    storyEnd.insert(46, """ascending ever up the stairway""")

    symbol.insert(47, "䷮")  # ䷮Confining
    storyBeginning.insert(47, """The caged bird cannot sail its skies""")
    storyEnd.insert(47, """while being constrained within imposed bounds""")

    symbol.insert(48, "䷯")  # ䷯Source Welling
    storyBeginning.insert(48, """In the beginning the sound became""")
    storyEnd.insert(48, """coming from a place where it all comes from""")

    symbol.insert(49, "䷰")  # ䷰Revolution # Molting, Skinning
    storyBeginning.insert(49, """The old skin is shed as the past is reformed""")
    storyEnd.insert(49, """casting aside the obsolete state""")

    symbol.insert(50, "䷱")  # ䷱Holding
    storyBeginning.insert(50, """A cup is defined by its empy space""")
    storyEnd.insert(50, """As the cauldron transmits fire to its contents""")

    symbol.insert(51, "䷲")  # ䷲Thunder Shake
    storyBeginning.insert(51, """We become shaken as a sonic boom rips the clouds""")
    storyEnd.insert(51, """erupting -BAM!- like a flash of lightning""")

    symbol.insert(52, "䷳")  # ䷳Stillness, Bound
    storyBeginning.insert(52, """Trees see many skies from a single point""")
    storyEnd.insert(52, """like immovable mountains going where their planets go""")

    symbol.insert(53, "䷴")  # ䷴Infiltrating
    storyBeginning.insert(53, """The stranger has sneaked through the front door""")
    storyEnd.insert(53, """which occurs gradually and unbeknownst to them""")

    symbol.insert(54, "䷵")  # ䷵Betrothing #Converting the Maiden
    storyBeginning.insert(
        54, """The bird of paradise woos their mate with every colour"""
    )
    storyEnd.insert(54, """making an idea of love into a real future""")

    symbol.insert(55, "䷶")  # ䷶Abounding
    storyBeginning.insert(55, """The sun at high noon doesn't mind goin' down""")
    storyEnd.insert(55, """with all the sun of the summer solstice""")

    symbol.insert(56, "䷷")  # ䷷Wanderer Soujourning
    storyBeginning.insert(56, """Follow the road, wherever it takes life""")
    storyEnd.insert(56, """in a time of unexpected journeys and adventures""")

    symbol.insert(57, "䷸")  # ䷸Osmosis Wind Ground
    storyBeginning.insert(57, """Slowly it becomes furniture around the place""")
    storyEnd.insert(57, """easing gently through the membrane's boundary""")

    symbol.insert(58, "䷹")  # ䷹Joyous Open
    storyBeginning.insert(58, """Happiness is composed of action and outlook""")
    storyEnd.insert(58, """existing blissfully, open to reality as it comes """)

    symbol.insert(59, "䷺")  # ䷺Dispersing
    storyBeginning.insert(
        59, """The heart's flow turns more ways the further it goes"""
    )
    storyEnd.insert(59, """as an ocean feeds seas, feed rivers, feed tributaries…""")

    symbol.insert(60, "䷻")  # ䷻Composed Articulating
    storyBeginning.insert(
        60, """Instead of melting everyone's minds, things are chill"""
    )
    storyEnd.insert(60, """which can be more subtle than was originally thought""")

    symbol.insert(61, "䷼")  # ䷼Truth #Inner Truth
    storyBeginning.insert(61, """There are things known inside no matter what""")
    storyEnd.insert(61, """and this is irrefutable to the inner spirit""")

    symbol.insert(62, "䷽")  # ䷽Detail
    storyBeginning.insert(62, """Through countless small steps is greatness made""")
    storyEnd.insert(62, """where small successes add up even if slightly""")

    symbol.insert(63, "䷾")  # ䷾Completed
    storyBeginning.insert(63, """The issue is finally concluded""")
    storyEnd.insert(63, """thereby the end has been reached""")

    symbol.insert(64, "䷿")  # ䷿Unfinished
    storyBeginning.insert(64, """The song was never finished, so much as abandoned""")
    storyEnd.insert(64, """the road will ramble ever onward""")

    def __init__(
        self,
    ):
        self.hexagramNumber = 0  # HERE

    @classmethod
    def getSubpage(cls, number: int, decorateSubpage=False) -> int:
        if 1 <= number <= 64:
            pass
        else:
            raise ValueError(
                "getSubpage expects number to be an int which represents the iChing Hexagram number, not "
                + str(number)
            )

    @classmethod
    def makeHexagramList(cls):
        print("hexagram list")
        for i in range(len(Hexagram.notesets)):
            # Remember traditional
            print(
                "notesets[(",
                ",".join([str(n) for n in Hexagram.notesets[i]]),
                ")] = ",
                sep="",
                end="",
            )
            print("'pinyin':'", Hexagram.pinyin[i], "',", sep="", end="")
            print(" 'chinese':'", Hexagram.chinese[i], "',", sep="", end="")
            print(" 'symbol':'", Hexagram.symbol[i], "',", sep="", end="")
            # print(' \'subpage\':\'',)
            print(
                "chinese.insert(" + Hexagram.chinese[i] + ", '') # ",
                Hexagram.symbol[i],
                " ",
                Hexagram.names[i],
                " ",
                Hexagram.namesNoun,
                sep="",
            )

    @classmethod
    def makeHexagramsToChangeChart(cls):
        pass

    @classmethod
    def makeHexagramTable(
        cls,
        useSubSequenceOrder=True,
        useColour=False,
        decorateWithSmallCircle=True,
        rewriteProjectFile=True,
            useTextStyledByWay=True   ):
        print("making hexagramTable...")
        if useSubSequenceOrder:
            _hexagramBook = Book(["1", "b2", "2", "b3", "3", "4"])
            # input(str(_hexagramBook.sequence))
            _positiveHexagrams = [_hexagramBook[i] for i in range(1, 33)]
            _negativeHexagrams = [i.withoutNote("1") for i in _positiveHexagrams]
            # _negativeHexagrams.reverse()
            # _positiveIChing = [Hexagram.notesets[i.getSemitones()] for i in _positiveHexagrams]
            # _negativeIChing = [Hexagram.notesets[i.getSemitones()] for i in _negativeHexagrams]
            
            _columnBreakingWays = ["name","secondName"]
            _hexPrintWays = [
                "subpage",
                "symbol",
                "braille",
                "syllable",
                "name",
                "Change",
                "secondName",
                "Tritone Sub",
            ]
            _hexPrintWays2 = [
                "subpage",
                "symbol",
                "braille",
                "name",
                "number",
                "chinese",
                "pinyin",
                "codon",
                "Tritone Sub Page",
                "subChange",
            ]

            
            print(_hexPrintWays)

            _wayData = {
                "subpage": {'label':Book.unicodeChars["Hexagram Subpage"]},
                "symbol": {'label':Book.unicodeChars["Hexagram"]},
                "braille": {'label':Book.unicodeChars["Braille"]},
                "name": {'label':'Name'},
                "secondName": {'label':'Name 2'},
                "number": {'label':Book.unicodeChars["Index Number"]},
                "chinese": {'label':'hinese'},
                "pinyin": {'label':'pin'},
                "codon": {'label':Book.unicodeChars['Helix']},
                "syllable": {'label':Book.unicodeChars['Word']},
                "subChange": {'label':Book.unicodeChars['Change Number']},

                "Jazz": {'label':'Jazz'},
                "Change": {'label':'Jazz'},
                "Tritone Sub Page": {'label':Book.unicodeChars['Tritone Sub']+Book.unicodeChars['Change Number']},
                "Tritone Sub": {'label':Book.unicodeChars['Tritone Sub']},

            }
            _labels = [
                "subpage",
                "symbol",
                "braille",
                "syllable",
                "name",
                "subChange",
                "Jazz",

                "Tritone Sub Page",
                "Tritone Sub",
            ]
            _labels2 = [
                "subpage",
                "symbol",
                "braille",
                "name",
                "number",
                "chinese",
                "pinyin",
                "codon",
            ]
            #use sumbols for label
            
                
           
            _labelsSymbol = _labels[:]
            
            
            for l in _labels:
                try:
                    _labelsSymbol.append(Book.unicodeChars[l])
                except KeyError:
                    _labelsSymbol.append(l)
            # To get rid of labels: they are too big
            #_labels = ["" for i in _labels]
            #_labels2 = ["" for i in _labels2]

            _str = ""
            _page = 1
            for w in range(len([_hexPrintWays, _hexPrintWays2])):
                ways = [_hexPrintWays, _hexPrintWays2][w]
                #ways.reverse()
                _tabs = len(ways)
                '''if "New Tabular" in ways:
                    if ways.index('New Tabular') > w:
                        _tabs = ways.index('New Tabular',w) - w
                    else:
                        _tabs = len(ways) - w'''
                        
                for hexaIdx,hexagrams in enumerate([_negativeHexagrams, _positiveHexagrams]):
                    #ways.reverse()
                    _str += "\\noindent\\begin{table}[!ht] "
                    if hexagrams == _negativeHexagrams:
                        _str += "\\caption{The 32 Negative Hexagrams "
                    elif hexagrams == _positiveHexagrams:
                        _str += "\\caption{The 32 Positive Hexagrams "
                    _str += "part " + str(math.floor((_page + 1) / 2)) + "}"
                    #_str += "\\begin{tabular}{" + " L " * _tabs + "}\n"

                    _columnTypes = '@{} '
                    for ___w,___way in enumerate(ways):
                        if ___w < len(ways) - 2 and ways[___w+1] in _columnBreakingWays:
                            _columnTypes += 'l @{\extracolsep{\\fill}}'
                        else:
                            _columnTypes += 'l'
                        _columnTypes += ' '
                    _columnTypes += '@{}'
                    
                    _str += "\\begin{tabular*}{\\linewidth}{"+_columnTypes+"}\n"
                    _str += "\\toprule "
                    
                    
                    if set(ways) == set(_hexPrintWays):
                        _labels = [_wayData[i]['label'] for i in _hexPrintWays]
                    elif set(ways) == set(_hexPrintWays2):
                        _labels = [_wayData[i]['label'] for i in _hexPrintWays2]
                    #_str += "{\\textbf "
                    _str += " & ".join(["\\textbf{"+l+'}' for l in _labels])
                    #_str += '}'
                    
                    _str += "\\\\\n\\midrule"
                    for n in hexagrams:
                        #_str += "\\midrule "
                        for w, way in enumerate(ways):
                            if way == "New Tabular":
                                pass#_str += "\\end{tabular}\\begin{tabular}{" + " l" * _tabs + "}\n"
                            elif way in Hexagram.validWays:
                                thing = n.getHexagram(
                                    [way],
                                    decorateWithSmallCircle=decorateWithSmallCircle,
                                    useGraphicSymbol=True,
                                    useTextStyledByWay=useTextStyledByWay,decorateWithUnicode=False
                                )[0]
                                #if way == 'Change': input('hmmmmmm')
                                try:
                                    _str += thing
                                except:
                                    input('thing is not valid: '+str(type(thing))+str(thing))
                                if thing.count('{') != thing.count('}'):
                                    print(n.getHexagram(
                                    [way],
                                    decorateWithSmallCircle=decorateWithSmallCircle,
                                    useGraphicSymbol=True,
                                    useTextStyledByWay=useTextStyledByWay
                                    ))
                                    raise ValueError('way = ' +way + '\nvalue = ' + thing)
                            
                                
                            elif way in Change.validWays:
                                if way == 'Change': raise TypeError('sdfsdf')
                                if type(n.byWays(way)) == list:
                                    _str += " ".join(n.byWays(way,
                                            useTextStyledByWay=useTextStyledByWay))
                                else:
                                    _str += str(n.byWays(way,useTextStyledByWay=useTextStyledByWay))
                            if w + 1 < len(ways):
                                _str += " & "
                            if way == "Jazz":
                                pass#raise TypeError(_str)
                        _str += "\\\\\n"
                    _str += "\\bottomrule "
                    _str += "\\end{tabular*}"
                    _str += "\\end{table}"
                    # _str += '\\clearpage\n'
                    _str += "\\newpage\n"
                    _page += 1
                    # _str += '\\\\\n'
            while Latex.commandStrings["Small Circle Command Start"] in _str:
                _str = _str.replace(
                    Latex.commandStrings["Small Circle Command Start"],
                    "\\protect\\bigtabbingimg{",
                )
        else:
            raise TypeError("figure out how to code this")
        if rewriteProjectFile:
            _filename = os.path.join(Project.directoryTex,Project.hexagramTableFilename)
            text_file = open(_filename, "w",encoding='utf-8')
            text_file.write("%s" % _str)
            text_file.close()
            print("rewrote", _filename)

        #Latex.buildFile('condensedWOC.tex')
        input('done with makeHexagramTable')
        return _str

    @classmethod
    def makeSextaSystemToSemitones(cls):
        print("sexta system")

        for i, v in enumerate(Hexagram.notesets):
            for extraBit in ("FF", "TF", "FT", "TT"):
                _change = Change.makeFromSet(list(v))

                print(
                    "notesets",
                    extraBit,
                    "[",
                    tuple(v),
                    "] = '' # ",
                    Hexagram.symbol[i],
                    " ",
                    Hexagram.names[i],
                    " ",
                    Book.unicodeChars["Index Number"],
                    i,
                    sep="",
                )
                # if you want to print the scale and scale name use the below
                # ' ',_change,' ',_change.getScaleNames()[0],' ',
                # _change.getChangeNumber(decorateChapter=True),sep=':')

    @classmethod
    def makeStoryBlock(cls):
        for i in range(len(cls.symbol)):
            print()
            print(
                "symbol.insert("
                + str(i)
                + ",u'"
                + cls.symbol[i]
                + "') #"
                + cls.symbol[i]
                + cls.names[i]
            )

            print("storyBeginning.insert(" + str(i) + ", '''''')")
            print("storyEnd.insert(" + str(i) + ", '''''')")

        # messengers

    @classmethod
    def replaceBuggyPinyin(cls):
        for r in Latex.pinyinReplacements:
            Hexagram.pinyin = [
                i.replace(r, Latex.pinyinReplacements[r]) for i in Hexagram.pinyin
            ]