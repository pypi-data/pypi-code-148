class Braille:
    """Originally, I entered these in from top to bottom, meaning that the root position st was at the top left, and the fourth interval was bottom right."""

    ###Braille⠀
    # ⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿
    # ⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿
    # ⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿
    # ⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿'''
    ##
    # http: // www.brailleauthority.org / ueb / symbols_list.pdf

    @classmethod
    def convertToTrigramatic(self):
        keys = Braille.semitonesFF.keys()
        kinds = (
            Braille.semitonesFF,
            Braille.semitonesFT,
            Braille.semitonesTF,
            Braille.semitonesTT,
        )

        for kind in kinds:
            print("{} = {{}}".format(kind))

        for key in keys:
            # for key in ((0,),(1,),(2,),(3,),(4,),(5,)):
            newKey = []
            for st in key:
                if st == 0:
                    newKey.append(4)
                if st == 1:
                    newKey.append(2)
                if st == 2:
                    newKey.append(0)
                if st == 3:
                    newKey.append(5)
                if st == 4:
                    newKey.append(3)
                if st == 5:
                    newKey.append(1)
            newKey.sort()

            newKey = tuple(newKey)
            # input(str(key)  + str(newKey) +  Braille.semitonesFF[key]+Braille.semitonesFF[newKey])
            for kind in kinds:
                if kind == Braille.semitonesFF:
                    kindName = "semitonesFF"
                elif kind == Braille.semitonesFT:
                    kindName = "semitonesFT"
                elif kind == Braille.semitonesTF:
                    kindName = "semitonesTF"
                elif kind == Braille.semitonesTT:
                    kindName = "semitonesTT"

                # input(str(key) + ' ' + str(kind))

                if True or key == (1, 3, 5):
                    print(
                        "{}[{}] = '{}' #{}{} {}".format(
                            kindName,
                            key,
                            kind[newKey],
                            Change(noteset=key).getHexagram(["symbol"])[0],
                            Change(noteset=key).getHexagram(["name"])[0],
                            kind[key],
                            key,
                        )
                    )
        input("copy paste that into Braille class")

    semitonesFF = {}
    semitonesFT = {}
    semitonesTF = {}
    semitonesTT = {}
    semitonesFF[(0, 1, 2, 3, 4, 5)] = "⠿"  # ䷀Creative ⠿
    semitonesFT[(0, 1, 2, 3, 4, 5)] = "⢿"  # ䷀Creative ⢿
    semitonesTF[(0, 1, 2, 3, 4, 5)] = "⡿"  # ䷀Creative ⡿
    semitonesTT[(0, 1, 2, 3, 4, 5)] = "⣿"  # ䷀Creative ⣿
    semitonesFF[()] = " "  # ䷁Receptive
    semitonesFT[()] = "⢀"  # ䷁Receptive ⢀
    semitonesTF[()] = "⡀"  # ䷁Receptive ⡀
    semitonesTT[()] = "⣀"  # ䷁Receptive ⣀
    semitonesFF[(0, 4)] = "⠔"  # ䷂Sprouting ⠅
    semitonesFT[(0, 4)] = "⢔"  # ䷂Sprouting ⢅
    semitonesTF[(0, 4)] = "⡔"  # ䷂Sprouting ⡅
    semitonesTT[(0, 4)] = "⣔"  # ䷂Sprouting ⣅
    semitonesFF[(1, 5)] = "⠊"  # ䷃Naïve ⠨
    semitonesFT[(1, 5)] = "⢊"  # ䷃Naïve ⢨
    semitonesTF[(1, 5)] = "⡊"  # ䷃Naïve ⡨
    semitonesTT[(1, 5)] = "⣊"  # ䷃Naïve ⣨
    semitonesFF[(0, 1, 2, 4)] = "⠗"  # ䷄Waiting ⠏
    semitonesFT[(0, 1, 2, 4)] = "⢗"  # ䷄Waiting ⢏
    semitonesTF[(0, 1, 2, 4)] = "⡗"  # ䷄Waiting ⡏
    semitonesTT[(0, 1, 2, 4)] = "⣗"  # ䷄Waiting ⣏
    semitonesFF[(1, 3, 4, 5)] = "⠺"  # ䷅Arguing ⠼
    semitonesFT[(1, 3, 4, 5)] = "⢺"  # ䷅Arguing ⢼
    semitonesTF[(1, 3, 4, 5)] = "⡺"  # ䷅Arguing ⡼
    semitonesTT[(1, 3, 4, 5)] = "⣺"  # ䷅Arguing ⣼
    semitonesFF[(1,)] = "⠂"  # ䷆Leading ⠈
    semitonesFT[(1,)] = "⢂"  # ䷆Leading ⢈
    semitonesTF[(1,)] = "⡂"  # ䷆Leading ⡈
    semitonesTT[(1,)] = "⣂"  # ䷆Leading ⣈
    semitonesFF[(4,)] = "⠐"  # ䷇Uniting ⠄
    semitonesFT[(4,)] = "⢐"  # ䷇Uniting ⢄
    semitonesTF[(4,)] = "⡐"  # ䷇Uniting ⡄
    semitonesTT[(4,)] = "⣐"  # ䷇Uniting ⣄
    semitonesFF[(0, 1, 2, 4, 5)] = "⠟"  # ䷈Homegrown ⠯
    semitonesFT[(0, 1, 2, 4, 5)] = "⢟"  # ䷈Homegrown ⢯
    semitonesTF[(0, 1, 2, 4, 5)] = "⡟"  # ䷈Homegrown ⡯
    semitonesTT[(0, 1, 2, 4, 5)] = "⣟"  # ䷈Homegrown ⣯
    semitonesFF[(0, 1, 3, 4, 5)] = "⠾"  # ䷉Treading ⠽
    semitonesFT[(0, 1, 3, 4, 5)] = "⢾"  # ䷉Treading ⢽
    semitonesTF[(0, 1, 3, 4, 5)] = "⡾"  # ䷉Treading ⡽
    semitonesTT[(0, 1, 3, 4, 5)] = "⣾"  # ䷉Treading ⣽
    semitonesFF[(0, 1, 2)] = "⠇"  # ䷊Peaceful ⠋
    semitonesFT[(0, 1, 2)] = "⢇"  # ䷊Peaceful ⢋
    semitonesTF[(0, 1, 2)] = "⡇"  # ䷊Peaceful ⡋
    semitonesTT[(0, 1, 2)] = "⣇"  # ䷊Peaceful ⣋
    semitonesFF[(3, 4, 5)] = "⠸"  # ䷋Obstructing ⠴
    semitonesFT[(3, 4, 5)] = "⢸"  # ䷋Obstructing ⢴
    semitonesTF[(3, 4, 5)] = "⡸"  # ䷋Obstructing ⡴
    semitonesTT[(3, 4, 5)] = "⣸"  # ䷋Obstructing ⣴
    semitonesFF[(0, 2, 3, 4, 5)] = "⠽"  # ䷌Fellow ⠷
    semitonesFT[(0, 2, 3, 4, 5)] = "⢽"  # ䷌Fellow ⢷
    semitonesTF[(0, 2, 3, 4, 5)] = "⡽"  # ䷌Fellow ⡷
    semitonesTT[(0, 2, 3, 4, 5)] = "⣽"  # ䷌Fellow ⣷
    semitonesFF[(0, 1, 2, 3, 5)] = "⠯"  # ䷍Prosperous ⠻
    semitonesFT[(0, 1, 2, 3, 5)] = "⢯"  # ䷍Prosperous ⢻
    semitonesTF[(0, 1, 2, 3, 5)] = "⡯"  # ䷍Prosperous ⡻
    semitonesTT[(0, 1, 2, 3, 5)] = "⣯"  # ䷍Prosperous ⣻
    semitonesFF[(2,)] = "⠁"  # ䷎Humble ⠂
    semitonesFT[(2,)] = "⢁"  # ䷎Humble ⢂
    semitonesTF[(2,)] = "⡁"  # ䷎Humble ⡂
    semitonesTT[(2,)] = "⣁"  # ䷎Humble ⣂
    semitonesFF[(3,)] = "⠠"  # ䷏Confident ⠐
    semitonesFT[(3,)] = "⢠"  # ䷏Confident ⢐
    semitonesTF[(3,)] = "⡠"  # ䷏Confident ⡐
    semitonesTT[(3,)] = "⣠"  # ䷏Confident ⣐
    semitonesFF[(0, 3, 4)] = "⠴"  # ䷐Following ⠕
    semitonesFT[(0, 3, 4)] = "⢴"  # ䷐Following ⢕
    semitonesTF[(0, 3, 4)] = "⡴"  # ䷐Following ⡕
    semitonesTT[(0, 3, 4)] = "⣴"  # ䷐Following ⣕
    semitonesFF[(1, 2, 5)] = "⠋"  # ䷑Correcting ⠪
    semitonesFT[(1, 2, 5)] = "⢋"  # ䷑Correcting ⢪
    semitonesTF[(1, 2, 5)] = "⡋"  # ䷑Correcting ⡪
    semitonesTT[(1, 2, 5)] = "⣋"  # ䷑Correcting ⣪
    semitonesFF[(0, 1)] = "⠆"  # ䷒Arriving ⠉
    semitonesFT[(0, 1)] = "⢃"  # ䷒Arriving ⢉
    semitonesTF[(0, 1)] = "⡃"  # ䷒Arriving ⡉
    semitonesTT[(0, 1)] = "⣃"  # ䷒Arriving ⣉
    semitonesFF[(4, 5)] = "⠘"  # ䷓Seeing ⠤
    semitonesFT[(4, 5)] = "⢘"  # ䷓Seeing ⢤
    semitonesTF[(4, 5)] = "⡘"  # ䷓Seeing ⡤
    semitonesTT[(4, 5)] = "⣘"  # ䷓Seeing ⣤
    semitonesFF[(0, 3, 5)] = "⠬"  # ䷔Biting ⠱
    semitonesFT[(0, 3, 5)] = "⢬"  # ䷔Biting ⢱
    semitonesTF[(0, 3, 5)] = "⡬"  # ䷔Biting ⡱
    semitonesTT[(0, 3, 5)] = "⣬"  # ䷔Biting ⣱
    semitonesFF[(0, 2, 5)] = "⠍"  # ䷕Adorning ⠣
    semitonesFT[(0, 2, 5)] = "⢍"  # ䷕Adorning ⢣
    semitonesTF[(0, 2, 5)] = "⡍"  # ䷕Adorning ⡣
    semitonesTT[(0, 2, 5)] = "⣍"  # ䷕Adorning ⣣
    semitonesFF[(5,)] = "⠈"  # ䷖Splitting ⠠
    semitonesFT[(5,)] = "⢈"  # ䷖Splitting ⢠
    semitonesTF[(5,)] = "⡈"  # ䷖Splitting ⡠
    semitonesTT[(5,)] = "⣈"  # ䷖Splitting ⣠
    semitonesFF[(0,)] = "⠄"  # ䷗Returning ⠁
    semitonesFT[(0,)] = "⢄"  # ䷗Returning ⢁
    semitonesTF[(0,)] = "⡄"  # ䷗Returning ⡁
    semitonesTT[(0,)] = "⣄"  # ䷗Returning ⣁
    semitonesFF[(0, 3, 4, 5)] = "⠼"  # ䷘Integrating ⠵
    semitonesFT[(0, 3, 4, 5)] = "⢼"  # ䷘Integrating ⢵
    semitonesTF[(0, 3, 4, 5)] = "⡼"  # ䷘Integrating ⡵
    semitonesTT[(0, 3, 4, 5)] = "⣼"  # ䷘Integrating ⣵
    semitonesFF[(0, 1, 2, 5)] = "⠏"  # ䷙Cultivating ⠫
    semitonesFT[(0, 1, 2, 5)] = "⢏"  # ䷙Cultivating ⢫
    semitonesTF[(0, 1, 2, 5)] = "⡏"  # ䷙Cultivating ⡫
    semitonesTT[(0, 1, 2, 5)] = "⣏"  # ䷙Cultivating ⣫
    semitonesFF[(0, 5)] = "⠌"  # ䷚Nourishing ⠡
    semitonesFT[(0, 5)] = "⢌"  # ䷚Nourishing ⢡
    semitonesTF[(0, 5)] = "⡌"  # ䷚Nourishing ⡡
    semitonesTT[(0, 5)] = "⣌"  # ䷚Nourishing ⣡
    semitonesFF[(1, 2, 3, 4)] = "⠳"  # ䷛Excessive ⠞
    semitonesFT[(1, 2, 3, 4)] = "⢳"  # ䷛Excessive ⢞
    semitonesTF[(1, 2, 3, 4)] = "⡳"  # ䷛Excessive ⡞
    semitonesTT[(1, 2, 3, 4)] = "⣳"  # ䷛Excessive ⣞
    semitonesFF[(1, 4)] = "⠒"  # ䷜Chasmic ⠌
    semitonesFT[(1, 4)] = "⢒"  # ䷜Chasmic ⢌
    semitonesTF[(1, 4)] = "⡒"  # ䷜Chasmic ⡌
    semitonesTT[(1, 4)] = "⣒"  # ䷜Chasmic ⣌
    semitonesFF[(0, 2, 3, 5)] = "⠭"  # ䷝Distanced ⠳
    semitonesFT[(0, 2, 3, 5)] = "⢭"  # ䷝Distanced ⢳
    semitonesTF[(0, 2, 3, 5)] = "⡭"  # ䷝Distanced ⡳
    semitonesTT[(0, 2, 3, 5)] = "⣭"  # ䷝Distanced ⣳
    semitonesFF[(2, 3, 4)] = "⠱"  # ䷞Magnetic ⠖
    semitonesFT[(2, 3, 4)] = "⢱"  # ䷞Magnetic ⢖
    semitonesTF[(2, 3, 4)] = "⡱"  # ䷞Magnetic ⡖
    semitonesTT[(2, 3, 4)] = "⣱"  # ䷞Magnetic ⣖
    semitonesFF[(1, 2, 3)] = "⠣"  # ䷟Persevering ⠚
    semitonesFT[(1, 2, 3)] = "⢣"  # ䷟Persevering ⢚
    semitonesTF[(1, 2, 3)] = "⡣"  # ䷟Persevering ⡚
    semitonesTT[(1, 2, 3)] = "⣣"  # ䷟Persevering ⣚
    semitonesFF[(2, 3, 4, 5)] = "⠹"  # ䷠Retiring ⠶
    semitonesFT[(2, 3, 4, 5)] = "⢹"  # ䷠Retiring ⢶
    semitonesTF[(2, 3, 4, 5)] = "⡹"  # ䷠Retiring ⡶
    semitonesTT[(2, 3, 4, 5)] = "⣹"  # ䷠Retiring ⣶
    semitonesFF[(0, 1, 2, 3)] = "⠧"  # ䷡Mighty ⠛
    semitonesFT[(0, 1, 2, 3)] = "⢧"  # ䷡Mighty ⢛
    semitonesTF[(0, 1, 2, 3)] = "⡧"  # ䷡Mighty ⡛
    semitonesTT[(0, 1, 2, 3)] = "⣧"  # ䷡Mighty ⣛
    semitonesFF[(3, 5)] = "⠨"  # ䷢Promoting ⠰
    semitonesFT[(3, 5)] = "⢨"  # ䷢Promoting ⢰
    semitonesTF[(3, 5)] = "⡨"  # ䷢Promoting ⡰
    semitonesTT[(3, 5)] = "⣨"  # ䷢Promoting ⣰
    semitonesFF[(0, 2)] = "⠅"  # ䷣Eclipsing ⠃
    semitonesFT[(0, 2)] = "⢅"  # ䷣Eclipsing ⢃
    semitonesTF[(0, 2)] = "⡅"  # ䷣Eclipsing ⡃
    semitonesTT[(0, 2)] = "⣅"  # ䷣Eclipsing ⣃
    semitonesFF[(0, 2, 4, 5)] = "⠝"  # ䷤Kindred ⠧
    semitonesFT[(0, 2, 4, 5)] = "⢝"  # ䷤Kindred ⢧
    semitonesTF[(0, 2, 4, 5)] = "⡝"  # ䷤Kindred ⡧
    semitonesTT[(0, 2, 4, 5)] = "⣝"  # ䷤Kindred ⣧
    semitonesFF[(0, 1, 3, 5)] = "⠮"  # ䷥Polarising ⠹
    semitonesFT[(0, 1, 3, 5)] = "⢮"  # ䷥Polarising ⢹
    semitonesTF[(0, 1, 3, 5)] = "⡮"  # ䷥Polarising ⡹
    semitonesTT[(0, 1, 3, 5)] = "⣮"  # ䷥Polarising ⣹
    semitonesFF[(2, 4)] = "⠑"  # ䷦Limping ⠆
    semitonesFT[(2, 4)] = "⢑"  # ䷦Limping ⢃
    semitonesTF[(2, 4)] = "⡑"  # ䷦Limping ⡃
    semitonesTT[(2, 4)] = "⣑"  # ䷦Limping ⣃
    semitonesFF[(1, 3)] = "⠢"  # ䷧Delivered ⠘
    semitonesFT[(1, 3)] = "⢢"  # ䷧Delivered ⢘
    semitonesTF[(1, 3)] = "⡢"  # ䷧Delivered ⡘
    semitonesTT[(1, 3)] = "⣢"  # ䷧Delivered ⣘
    semitonesFF[(0, 1, 5)] = "⠎"  # ䷨Declining ⠩
    semitonesFT[(0, 1, 5)] = "⢎"  # ䷨Declining ⢩
    semitonesTF[(0, 1, 5)] = "⡎"  # ䷨Declining ⡩
    semitonesTT[(0, 1, 5)] = "⣎"  # ䷨Declining ⣩
    semitonesFF[(0, 4, 5)] = "⠜"  # ䷩Benefitting ⠥
    semitonesFT[(0, 4, 5)] = "⢜"  # ䷩Benefitting ⢥
    semitonesTF[(0, 4, 5)] = "⡜"  # ䷩Benefitting ⡥
    semitonesTT[(0, 4, 5)] = "⣜"  # ䷩Benefitting ⣥
    semitonesFF[(0, 1, 2, 3, 4)] = "⠷"  # ䷪Deciding ⠟
    semitonesFT[(0, 1, 2, 3, 4)] = "⢷"  # ䷪Deciding ⢟
    semitonesTF[(0, 1, 2, 3, 4)] = "⡷"  # ䷪Deciding ⡟
    semitonesTT[(0, 1, 2, 3, 4)] = "⣷"  # ䷪Deciding ⣟
    semitonesFF[(1, 2, 3, 4, 5)] = "⠻"  # ䷫Coupling ⠾
    semitonesFT[(1, 2, 3, 4, 5)] = "⢻"  # ䷫Coupling ⢾
    semitonesTF[(1, 2, 3, 4, 5)] = "⡻"  # ䷫Coupling ⡾
    semitonesTT[(1, 2, 3, 4, 5)] = "⣻"  # ䷫Coupling ⣾
    semitonesFF[(3, 4)] = "⠰"  # ䷬Clustering ⠔
    semitonesFT[(3, 4)] = "⢰"  # ䷬Clustering ⢔
    semitonesTF[(3, 4)] = "⡰"  # ䷬Clustering ⡔
    semitonesTT[(3, 4)] = "⣰"  # ䷬Clustering ⣔
    semitonesFF[(1, 2)] = "⠃"  # ䷭Ascending ⠊
    semitonesFT[(1, 2)] = "⢃"  # ䷭Ascending ⢊
    semitonesTF[(1, 2)] = "⡃"  # ䷭Ascending ⡊
    semitonesTT[(1, 2)] = "⣃"  # ䷭Ascending ⣊
    semitonesFF[(1, 3, 4)] = "⠲"  # ䷮Confining ⠜
    semitonesFT[(1, 3, 4)] = "⢲"  # ䷮Confining ⢜
    semitonesTF[(1, 3, 4)] = "⡲"  # ䷮Confining ⡜
    semitonesTT[(1, 3, 4)] = "⣲"  # ䷮Confining ⣜
    semitonesFF[(1, 2, 4)] = "⠓"  # ䷯Sourced ⠎
    semitonesFT[(1, 2, 4)] = "⢓"  # ䷯Sourced ⢎
    semitonesTF[(1, 2, 4)] = "⡓"  # ䷯Sourced ⡎
    semitonesTT[(1, 2, 4)] = "⣓"  # ䷯Sourced ⣎
    semitonesFF[(0, 2, 3, 4)] = "⠵"  # ䷰Revolving ⠗
    semitonesFT[(0, 2, 3, 4)] = "⢵"  # ䷰Revolving ⢗
    semitonesTF[(0, 2, 3, 4)] = "⡵"  # ䷰Revolving ⡗
    semitonesTT[(0, 2, 3, 4)] = "⣵"  # ䷰Revolving ⣗
    semitonesFF[(1, 2, 3, 5)] = "⠫"  # ䷱Holding ⠺
    semitonesFT[(1, 2, 3, 5)] = "⢫"  # ䷱Holding ⢺
    semitonesTF[(1, 2, 3, 5)] = "⡫"  # ䷱Holding ⡺
    semitonesTT[(1, 2, 3, 5)] = "⣫"  # ䷱Holding ⣺
    semitonesFF[(0, 3)] = "⠤"  # ䷲Thundering ⠑
    semitonesFT[(0, 3)] = "⢤"  # ䷲Thundering ⢑
    semitonesTF[(0, 3)] = "⡤"  # ䷲Thundering ⡑
    semitonesTT[(0, 3)] = "⣤"  # ䷲Thundering ⣑
    semitonesFF[(2, 5)] = "⠉"  # ䷳Still ⠢
    semitonesFT[(2, 5)] = "⢉"  # ䷳Still ⢢
    semitonesTF[(2, 5)] = "⡉"  # ䷳Still ⡢
    semitonesTT[(2, 5)] = "⣉"  # ䷳Still ⣢
    semitonesFF[(2, 4, 5)] = "⠙"  # ䷴Infiltrating ⠦
    semitonesFT[(2, 4, 5)] = "⢙"  # ䷴Infiltrating ⢦
    semitonesTF[(2, 4, 5)] = "⡙"  # ䷴Infiltrating ⡦
    semitonesTT[(2, 4, 5)] = "⣙"  # ䷴Infiltrating ⣦
    semitonesFF[(0, 1, 3)] = "⠦"  # ䷵Betrothing ⠙
    semitonesFT[(0, 1, 3)] = "⢦"  # ䷵Betrothing ⢙
    semitonesTF[(0, 1, 3)] = "⡦"  # ䷵Betrothing ⡙
    semitonesTT[(0, 1, 3)] = "⣦"  # ䷵Betrothing ⣙
    semitonesFF[(0, 2, 3)] = "⠥"  # ䷶Abundant ⠓
    semitonesFT[(0, 2, 3)] = "⢥"  # ䷶Abundant ⢓
    semitonesTF[(0, 2, 3)] = "⡥"  # ䷶Abundant ⡓
    semitonesTT[(0, 2, 3)] = "⣥"  # ䷶Abundant ⣓
    semitonesFF[(2, 3, 5)] = "⠩"  # ䷷Wandering ⠲
    semitonesFT[(2, 3, 5)] = "⢩"  # ䷷Wandering ⢲
    semitonesTF[(2, 3, 5)] = "⡩"  # ䷷Wandering ⡲
    semitonesTT[(2, 3, 5)] = "⣩"  # ䷷Wandering ⣲
    semitonesFF[(1, 2, 4, 5)] = "⠛"  # ䷸Osmotic ⠮
    semitonesFT[(1, 2, 4, 5)] = "⢛"  # ䷸Osmotic ⢮
    semitonesTF[(1, 2, 4, 5)] = "⡛"  # ䷸Osmotic ⡮
    semitonesTT[(1, 2, 4, 5)] = "⣛"  # ䷸Osmotic ⣮
    semitonesFF[(0, 1, 3, 4)] = "⠶"  # ䷹Joyous ⠝
    semitonesFT[(0, 1, 3, 4)] = "⢶"  # ䷹Joyous ⢝
    semitonesTF[(0, 1, 3, 4)] = "⡶"  # ䷹Joyous ⡝
    semitonesTT[(0, 1, 3, 4)] = "⣶"  # ䷹Joyous ⣝
    semitonesFF[(1, 4, 5)] = "⠚"  # ䷺Dispersing ⠬
    semitonesFT[(1, 4, 5)] = "⢚"  # ䷺Dispersing ⢬
    semitonesTF[(1, 4, 5)] = "⡚"  # ䷺Dispersing ⡬
    semitonesTT[(1, 4, 5)] = "⣚"  # ䷺Dispersing ⣬
    semitonesFF[(0, 1, 4)] = "⠖"  # ䷻Composed ⠍
    semitonesFT[(0, 1, 4)] = "⢖"  # ䷻Composed ⢍
    semitonesTF[(0, 1, 4)] = "⡖"  # ䷻Composed ⡍
    semitonesTT[(0, 1, 4)] = "⣖"  # ䷻Composed ⣍
    semitonesFF[(0, 1, 4, 5)] = "⠞"  # ䷼True ⠭
    semitonesFT[(0, 1, 4, 5)] = "⢞"  # ䷼True ⢭
    semitonesTF[(0, 1, 4, 5)] = "⡞"  # ䷼True ⡭
    semitonesTT[(0, 1, 4, 5)] = "⣞"  # ䷼True ⣭
    semitonesFF[(2, 3)] = "⠡"  # ䷽Detailed ⠒
    semitonesFT[(2, 3)] = "⢡"  # ䷽Detailed ⢒
    semitonesTF[(2, 3)] = "⡡"  # ䷽Detailed ⡒
    semitonesTT[(2, 3)] = "⣡"  # ䷽Detailed ⣒
    semitonesFF[(0, 2, 4)] = "⠕"  # ䷾Completed ⠇
    semitonesFT[(0, 2, 4)] = "⢕"  # ䷾Completed ⢇
    semitonesTF[(0, 2, 4)] = "⡕"  # ䷾Completed ⡇
    semitonesTT[(0, 2, 4)] = "⣕"  # ䷾Completed ⣇
    semitonesFF[(1, 3, 5)] = "⠪"  # ䷿Incomplete ⠸
    semitonesFT[(1, 3, 5)] = "⢪"  # ䷿Incomplete ⢸
    semitonesTF[(1, 3, 5)] = "⡪"  # ䷿Incomplete ⡸
    semitonesTT[(1, 3, 5)] = "⣪"  # ䷿Incomplete ⣸