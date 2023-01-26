#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Constants for mcfonts.

This contains templates for providers, charlists, etc.
Old versions are not stored, and only the latest release is included.
As of this release, 1.19.3 is the latest.

Use :const:`RELEASE_DEFAULT` when looking to template a Vanilla resource without a provider.
"""
import re

import lxml.etree

XML_FONT_TEMPLATE: lxml.etree._Element = lxml.etree.XML(
    b"""<?xml version="1.0" encoding="UTF-8"?>
<ttFont sfntVersion="OTTO" ttLibVersion="4.34">
<GlyphOrder>
<GlyphID id="0" name=".notdef"/>
</GlyphOrder>
<head>
<tableVersion value="1.0"/>
<fontRevision value="1.0"/>
<checkSumAdjustment value="0x910274da"/>
<magicNumber value="0x5f0f3cf5"/>
<flags value="00000000 00001011"/>
<unitsPerEm value="1000"/>
<created value="Mon Jan  1 00:00:00 0000"/>
<modified value="Mon Jan  1 00:00:00 0000"/>
<xMin value="-12500"/>
<yMin value="-12500"/>
<xMax value="12500"/>
<yMax value="12500"/>
<macStyle value="00000000 00000000"/>
<lowestRecPPEM value="8"/>
<fontDirectionHint value="0"/>
<indexToLocFormat value="0"/>
<glyphDataFormat value="0"/>
</head>
<hhea>
<tableVersion value="0x00010000"/>
<ascent value="1000"/>
<descent value="0"/>
<lineGap value="250"/>
<advanceWidthMax value="12500"/>
<minLeftSideBearing value="0"/>
<minRightSideBearing value="0"/>
<xMaxExtent value="1000"/>
<caretSlopeRise value="1"/>
<caretSlopeRun value="0"/>
<caretOffset value="0"/>
<reserved0 value="0"/>
<reserved1 value="0"/>
<reserved2 value="0"/>
<reserved3 value="0"/>
<metricDataFormat value="0"/>
<numberOfHMetrics value="1"/>
</hhea>
<maxp>
<tableVersion value="0x5000"/>
<numGlyphs value="0"/>
</maxp>
<OS_2>
<!-- The fields 'usFirstCharIndex' and 'usLastCharIndex'
will be recalculated by the compiler -->
<version value="4"/>
<xAvgCharWidth value="660"/>
<usWeightClass value="400"/>
<usWidthClass value="5"/>
<fsType value="00000000 00000000"/>
<ySubscriptXSize value="650"/>
<ySubscriptYSize value="700"/>
<ySubscriptXOffset value="0"/>
<ySubscriptYOffset value="140"/>
<ySuperscriptXSize value="650"/>
<ySuperscriptYSize value="700"/>
<ySuperscriptXOffset value="0"/>
<ySuperscriptYOffset value="480"/>
<yStrikeoutSize value="50"/>
<yStrikeoutPosition value="256"/>
<sFamilyClass value="0"/>
<panose>
<bFamilyType value="2"/>
<bSerifStyle value="0"/>
<bWeight value="5"/>
<bProportion value="9"/>
<bContrast value="0"/>
<bStrokeVariation value="0"/>
<bArmStyle value="0"/>
<bLetterForm value="0"/>
<bMidline value="10"/>
<bXHeight value="10"/>
</panose>
<ulUnicodeRange1 value="11111111 11111111 11111111 11111111"/>
<ulUnicodeRange2 value="11111111 11111111 11111111 11111111"/>
<ulUnicodeRange3 value="11111111 11111111 11111111 11111111"/>
<ulUnicodeRange4 value="11111111 11111111 11111111 11111111"/>
<achVendID value="pMCF"/>
<fsSelection value="00000000 10000000"/>
<usFirstCharIndex value="32"/>
<usLastCharIndex value="0"/>
<sTypoAscender value="1000"/>
<sTypoDescender value="0"/>
<sTypoLineGap value="4"/>
<usWinAscent value="1000"/>
<usWinDescent value="0"/>
<ulCodePageRange1 value="00000000 00000000 00000000 00000001"/>
<ulCodePageRange2 value="00000000 00000000 00000000 00000000"/>
<sxHeight value="500"/>
<sCapHeight value="1000"/>
<usDefaultChar value="32"/>
<usBreakChar value="32"/>
<usMaxContext value="1"/>
</OS_2>
<name>
</name>
<cmap>
<tableVersion version="0"/>
</cmap>
<post>
<formatType value="3.0"/>
<italicAngle value="0.0"/>
<underlinePosition value="0"/>
<underlineThickness value="0"/>
<isFixedPitch value="0"/>
<minMemType42 value="0"/>
<maxMemType42 value="0"/>
<minMemType1 value="0"/>
<maxMemType1 value="0"/>
</post>
<CFF>
<major value="1"/>
<minor value="0"/>
<CFFFont name="Default">
<version value="001.000"/>
<Notice value=""/>
<FullName value="Default"/>
<FamilyName value="Default"/>
<Weight value="Regular"/>
<isFixedPitch value="0"/>
<ItalicAngle value="0"/>
<UnderlinePosition value="0"/>
<UnderlineThickness value="0"/>
<PaintType value="0"/>
<CharstringType value="2"/>
<FontMatrix value="0.001 0 0 0.001 0 0"/>
<FontBBox value="0 -1000 1000 1000"/>
<StrokeWidth value="0"/>
<!-- charset is dumped separately as the 'GlyphOrder' element -->
<Encoding name="StandardEncoding"/>
<Private>
<BlueValues value="1 1 16 16"/>
<BlueScale value="0.039625"/>
<BlueShift value="0"/>
<BlueFuzz value="1"/>
<ForceBold value="0"/>
<LanguageGroup value="0"/>
<ExpansionFactor value="0.06"/>
<initialRandomSeed value="0"/>
<defaultWidthX value="750"/>
<nominalWidthX value="0"/>
</Private>
<CharStrings>
<CharString name=".notdef">
750 0 vmoveto 1000 625 -1000 vlineto -125 125 rmoveto 750 -375 -750 vlineto endchar
</CharString>
</CharStrings>
</CFFFont>
<GlobalSubrs/>
</CFF>
<GDEF>
<Version value="0x00010000"/>
<GlyphClassDef/>
</GDEF>
<hmtx>
<mtx name=".notdef" width="750" lsb="0"/>
</hmtx>
</ttFont>"""
)
"""A blank TTF XML, with a ``.notdef`` glyph already embedded."""

EMPTY_FONT_JSON: dict[str, list] = {"providers": []}
"""An empty font JSON with no providers."""

RELEASE_DEFAULT: dict = {
    "providers": [
        {"type": "space", "advances": {" ": 4, "\u200c": 0}},
        {
            "type": "bitmap",
            "file": "minecraft:font/nonlatin_european.png",
            "ascent": 7,
            "chars": [
                "¡‰­·₴≠¿×ØÞһðøþΑΒ",
                "ΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣ",
                "ΤΥΦΧΨΩαβγδεζηθικ",
                "λμνξοπρςστυφχψωЂ",
                "ЅІЈЉЊЋАБВГДЕЖЗИК",
                "ЛМНОПРСТУФХЦЧШЩЪ",
                "ЫЬЭЮЯабвгдежзикл",
                "мнопрстуфхцчшщъы",
                "ьэюяєѕіјљњ–—‘’“”",
                "„…⁊←↑→↓⇄＋ƏəɛɪҮүӨ",
                "өʻˌ;ĸẞß₽€ѢѣѴѵӀѲѳ",
                "⁰¹³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁱ™",
                "ʔʕ⧈⚔☠ҚқҒғҰұӘәҖҗҢ",
                "ңҺאבגדהוזחטיכלמם",
                "נןסעפףצץקר¢¤¥©®µ",
                "¶¼½¾·‐‚†‡•‱′″‴‵‶",
                "‷‹›※‼‽⁂⁈⁉⁋⁎⁏⁑⁒⁗℗",
                "−∓∞☀☁☈Є☲☵☽♀♂⚥♠♣♥",
                "♦♩♪♫♬♭♮♯⚀⚁⚂⚃⚄⚅ʬ⚡",
                "⛏✔❄❌❤⭐⸘⸮⸵⸸⹁⹋⥝ᘔƐ߈",
                "ϛㄥⱯᗺƆᗡƎℲ⅁ꞰꞀԀꝹᴚ⟘∩",
                "Ʌ⅄ɐɔǝɟᵷɥᴉɾʞꞁɯɹʇʌ",
                "ʍʎԱԲԳԴԶԷԹԺԻԼԽԾԿՀ",
                "ՁՂՃՄՅՆՇՈՉՋՌՍՎՏՐՑ",
                "ՒՓՔՕՖՙաբգդեզէըթժ",
                "իլխծկհձղճմյնշոչպ",
                "ջռսվտրցւփքօֆևשתԸ",
                "՚՛՜՝՞՟ՠֈ֏¯ſƷʒǷƿȜ",
                "ȝȤȥ˙Ꝛꝛ‑⅋⏏⏩⏪⏭⏮⏯⏴⏵",
                "⏶⏷⏸⏹⏺⏻⏼⏽⭘▲▶▼◀●◦◘",
                "⚓⛨ĲĳǉꜨꜩꜹꜻﬀﬁﬂﬃﬅ�Ե",
                "Պᚠᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯ",
                "ᚰᚱᚲᚳᚴᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀ",
                "ᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐ",
                "ᛑᛒᛓᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟᛠ",
                "ᛡᛢᛣᛤᛥᛦᛧᛨᛩᛪ᛫᛬᛭ᛮᛯᛰ",
                "ᛱᛲᛳᛴᛵᛶᛷᛸ☺☻¦☹ך׳״װ",
                "ױײ־׃׆´¨ᴀʙᴄᴅᴇꜰɢʜᴊ",
                "ᴋʟᴍɴᴏᴘꞯʀꜱᴛᴜᴠᴡʏᴢ§",
                "ɱɳɲʈɖɡʡɕʑɸʝʢɻʁɦʋ",
                "ɰɬɮʘǀǃǂǁɓɗᶑʄɠʛɧɫ",
                "ɨʉʊɘɵɤɜɞɑɒɚɝƁƉƑƩ",
                "ƲႠႡႢႣႤႥႦႧႨႩႪႫႬႭႮ",
                "ႯႰႱႲႳႴႵႶႷႸႹႺႻႼႽႾ",
                "ႿჀჁჂჃჄჅჇჍაბგდევზ",
                "თიკლმნოპჟრსტუფქღ",
                "ყშჩცძწჭხჯჰჱჲჳჴჵჶ",
                "ჷჸჹჺ჻ჼჽჾჿתּשׂפֿפּכּײַיִ",
                "וֹוּבֿבּꜧꜦɺⱱʠʗʖɭɷɿʅʆ",
                "ʓʚ₪₾֊ⴀⴁⴂⴃⴄⴅⴆⴡⴇⴈⴉ",
                "ⴊⴋⴌⴢⴍⴎⴏⴐⴑⴒⴣⴓⴔⴕⴖⴗ",
                "ⴘⴙⴚⴛⴜⴝⴞⴤⴟⴠⴥ⅛⅜⅝⅞⅓",
                "⅔✉☂☔☄⛄☃⌛⌚⚐✎❣♤♧♡♢",
                "⛈☰☱☳☴☶☷↔⇒⇏⇔⇵∀∃∄∉",
                "∋∌⊂⊃⊄⊅∧∨⊻⊼⊽∥≢⋆∑⊤",
                "⊥⊢⊨≔∁∴∵∛∜∂⋃⊆⊇□△▷",
                "▽◁◆◇○◎☆★✘₀₁₂₃₄₅₆",
                "₇₈₉₊₋₌₍₎∫∮∝⌀⌂⌘〒ɼ",
                "ƄƅẟȽƚƛȠƞƟƧƨƪƸƹƻƼ",
                "ƽƾȡȴȵȶȺⱥȻȼɆɇȾⱦɁɂ",
                "ɃɄɈɉɊɋɌɍɎɏẜẝỼỽỾỿ",
                "Ꞩꞩ𐌰𐌱𐌲𐌳𐌴𐌵𐌶𐌷𐌸𐌹𐌺𐌻𐌼𐌽",
                "𐌾𐌿𐍀𐍁𐍂𐍃𐍄𐍅𐍆𐍇𐍈𐍉𐍊🌧🔥🌊",
                "⅐⅑⅕⅖⅗⅙⅚⅟↉🗡🏹🪓🔱🎣🧪⚗",
                "⯪⯫Ɑ🛡✂🍖🪣🔔⏳⚑₠₡₢₣₤₥",
                "₦₩₫₭₮₰₱₲₳₵₶₷₸₹₺₻",
                "₼₿              ",
            ],
        },
        {
            "type": "bitmap",
            "file": "minecraft:font/accented.png",
            "height": 12,
            "ascent": 10,
            "chars": [
                "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ",
                "ÐÑÒÓÔÕÖÙÚÛÜÝàáâã",
                "äåæçìíîïñòóôõöùú",
                "ûüýÿĀāĂăĄąĆćĈĉĊċ",
                "ČčĎďĐđĒēĔĕĖėĘęĚě",
                "ĜĝḠḡĞğĠġĢģĤĥĦħĨĩ",
                "ĪīĬĭĮįİıĴĵĶķĹĺĻļ",
                "ĽľĿŀŁłŃńŅņŇňŊŋŌō",
                "ŎŏŐőŒœŔŕŖŗŘřŚśŜŝ",
                "ŞşŠšŢţŤťŦŧŨũŪūŬŭ",
                "ŮůŰűŲųŴŵŶŷŸŹźŻżŽ",
                "žǼǽǾǿȘșȚțΆΈΉΊΌΎΏ",
                "ΐΪΫάέήίΰϊϋόύώЀЁЃ",
                "ЇЌЍЎЙйѐёђѓїћќѝўџ",
                "ҐґḂḃḊḋḞḟḢḣḰḱṀṁṖṗ",
                "ṠṡṪṫẀẁẂẃẄẅỲỳèéêë",
                "ŉǧǫЏḍḥṛṭẒỊịỌọỤụ№",
                "ȇƔɣʃ⁇ǱǲǳǄǅǆǇǈǊǋǌ",
                "ℹᵫꜲꜳꜴꜵꜶꜷꜸꜺꜼꜽꝎꝏꝠꝡ",
                "ﬄﬆᚡᚵƠơƯưẮắẤấẾếốỚ",
                "ớỨứẰằẦầỀềồỜờỪừẢả",
                "ẲẳẨẩẺẻổỞỂểỈỉỎỏỔở",
                "ỦủỬửỶỷẠạẶặẬậẸẹỆệ",
                "ỘộỢợỰựỴỵỐƕẪẫỖỗữ☞",
                "☜☮ẴẵẼẽỄễỒỠỡỮỸỹҘҙ",
                "ҠҡҪҫǶ⚠⓪①②③④⑤⑥⑦⑧⑨",
                "⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳ⒶⒷⒸⒹⒺ",
                "ⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊ",
                "ⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚ",
                "ⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ̧",
                "ʂʐɶǍǎǞǟǺǻȂȃȦȧǠǡḀ",
                "ḁȀȁḆḇḄḅᵬḈḉḐḑḒḓḎḏ",
                "ḌᵭḔḕḖḗḘḙḜḝȨȩḚḛȄȅ",
                "ȆᵮǴǵǦḦḧḨḩḪḫȞȟḤẖḮ",
                "ḯȊȋǏǐȈȉḬḭǰȷǨǩḲḳḴ",
                "ḵḺḻḼḽḶḷḸḹⱢḾḿṂṃᵯṄ",
                "ṅṆṇṊṋǸǹṈṉᵰǬǭȬȭṌṍ",
                "ṎṏṐṑṒṓȎȏȪȫǑǒȮȯȰȱ",
                "ȌȍǪṔṕᵱȒȓṘṙṜṝṞṟȐȑ",
                "ṚᵳᵲṤṥṦṧṢṣṨṩᵴṰṱṮṯ",
                "ṬẗᵵṲṳṶṷṸṹṺṻǓǔǕǖǗ",
                "ǘǙǚǛǜṴṵȔȕȖṾṿṼṽẆẇ",
                "ẈẉẘẌẍẊẋȲȳẎẏẙẔẕẐẑ",
                "ẓᵶǮǯẛꜾꜿǢǣᵺỻᴂᴔꭣȸʣ",
                "ʥʤʩʪʫȹʨʦʧꭐꭑ₧Ỻאַאָƀ",
                "ƂƃƇƈƊƋƌƓǤǥƗƖɩƘƙƝ",
                "ƤƥɽƦƬƭƫƮȗƱƜƳƴƵƶƢ",
                "ƣȢȣʭʮʯﬔﬕﬗﬖﬓӐӑӒӓӶ",
                "ӷҔҕӖӗҼҽҾҿӚӛӜӝӁӂӞ",
                "ӟӢӣӤӥӦӧӪӫӰӱӮӯӲӳӴ",
                "ӵӸӹӬӭѶѷӔӺԂꚂꚀꚈԪԬꚄ",
                "ԄԐӠԆҊӃҞҜԞԚӅԮԒԠԈԔ",
                "ӍӉԨӇҤԢԊҨԤҦҎԖԌꚐҬꚊ",
                "ꚌԎҲӼӾԦꚔҴꚎҶӋҸꚒꚖꚆҌ",
                "ԘԜӕӻԃꚃꚁꚉԫԭꚅԅԑӡԇҋ",
                "ӄҟҝԟԛӆԯԓԡԉԕӎӊԩӈҥ",
                "ԣԋҩԥҧҏԗԍꚑҭꚋꚍԏҳӽӿ",
                "ԧꚕҵꚏҷӌҹꚓꚗꚇҍԙԝἈἀἉ",
                "ἁἊἂἋἃἌἄἍἅἎἆἏἇᾺὰᾸ",
                "ᾰᾹᾱΆάᾈᾀᾉᾁᾊᾂᾋᾃᾌᾄᾍ",
                "ᾅᾎᾆᾏᾇᾼᾴᾶᾷᾲᾳἘἐἙἑἚ",
                "ἒἛἓἜἔἝἕῈΈὲέἨἠῊὴἩ",
                "ἡἪἢἫἣἬἤἭἥἮἦἯἧᾘᾐᾙ",
                "ᾑᾚᾒᾛᾓᾜᾔᾝᾕᾞᾖᾟᾗΉήῌ",
                "ῃῂῄῆῇῚὶΊίἸἰἹἱἺἲἻ",
                "ἳἼἴἽἵἾἶἿἷῘῐῙῑῒΐῖ",
                "ῗῸὸΌόὈὀὉὁὊὂὋὃὌὄὍ",
                "ὅῬῤῥῪὺΎύὙὑὛὓὝὕὟὗ",
                "ῨῠῩῡϓϔῢΰῧὐὒὔῦὖῺὼ",
                "ΏώὨὠὩὡὪὢὫὣὬὤὭὥὮὦ",
                "Ὧὧᾨᾠᾩᾡᾪᾢᾫᾣᾬᾤᾭᾥᾮᾦ",
                "ᾯᾧῼῳῲῴῶῷ☯☐☑☒ƍƺⱾȿ",
                "ⱿɀᶀꟄꞔᶁᶂᶃꞕᶄᶅᶆᶇᶈᶉᶊ",
                "ᶋᶌᶍꟆᶎᶏᶐᶒᶓᶔᶕᶖᶗᶘᶙᶚ",
                "ẚ⅒⅘₨₯           ",
            ],
        },
        {
            "type": "bitmap",
            "file": "minecraft:font/ascii.png",
            "ascent": 7,
            "chars": [
                "                ",
                "                ",
                " !\"#$%&'()*+,-./",
                "0123456789:;<=>?",
                "@ABCDEFGHIJKLMNO",
                "PQRSTUVWXYZ[\\]^_",
                "`abcdefghijklmno",
                "pqrstuvwxyz{|}~ ",
                "                ",
                "            £  ƒ",
                "      ªº  ¬   «»",
                "░▒▓│┤╡╢╖╕╣║╗╝╜╛┐",
                "└┴┬├─┼╞╟╚╔╩╦╠═╬╧",
                "╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀",
                "             ∅∈ ",
                "≡±≥≤⌠⌡÷≈°∙ √ⁿ²■ ",
            ],
        },
        {
            "type": "legacy_unicode",
            "sizes": "minecraft:font/glyph_sizes.bin",
            "template": "minecraft:font/unicode_page_%s.png",
        },
    ]
}
"""The font JSON of default.json, the default Minecraft font."""
RELEASE_ALT: dict = {
    "providers": [
        {
            "type": "bitmap",
            "file": "minecraft:font/ascii_sga.png",
            "ascent": 7,
            "chars": [
                "                ",
                "                ",
                "                ",
                "                ",
                " ABCDEFGHIJKLMNO",
                "PQRSTUVWXYZ     ",
                " abcdefghijklmno",
                "pqrstuvwxyz     ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
            ],
        }
    ]
}
"""The font JSON of alt.json, the SGA font."""
RELEASE_UNIFORM: dict = {
    "providers": [
        {
            "type": "legacy_unicode",
            "sizes": "minecraft:font/glyph_sizes.bin",
            "template": "minecraft:font/unicode_page_%s.png",
        }
    ]
}
"""The font JSON of uniform.json, the Unicode fallback font."""

PROVIDER_NONLATIN: dict = RELEASE_DEFAULT["providers"][1]
"""The default provider for nonlatin-european."""
PROVIDER_ACCENTED: dict = RELEASE_DEFAULT["providers"][2]
"""The default provider for accented."""
PROVIDER_ASCII: dict = RELEASE_DEFAULT["providers"][3]
"""The default provider for ASCII."""

CHARLIST_NONLATIN = PROVIDER_NONLATIN["chars"]
"""The default charlist for nonlatin-european."""
CHARLIST_ACCENTED = PROVIDER_ACCENTED["chars"]
"""The default charlist for accented."""
CHARLIST_ASCII = PROVIDER_ASCII["chars"]
"""The default charlist for ASCII."""


RANGESTRING_PART = re.compile(r"!?(((0x|U\+|&#x)([0-9A-F]{1,7});?)|(.))", re.I)
RANGESTRING_RANGE_DELIMITER = re.compile(r"-|\.\.")
RANGESTRING_RANGE = re.compile(
    f"({RANGESTRING_PART.pattern}{RANGESTRING_RANGE_DELIMITER.pattern}{RANGESTRING_PART.pattern})",
    re.I,
)
RANGESTRING_COMPONENT = re.compile(f"({RANGESTRING_RANGE.pattern}|{RANGESTRING_PART.pattern})", re.I)
RANGESTRING_COMPONENT_DELIMITER = re.compile(", ?")
RANGESTRING_FULL = re.compile(f"(({RANGESTRING_COMPONENT.pattern}{RANGESTRING_COMPONENT_DELIMITER.pattern})*)", re.I)

SCHEMA_PATTERN_NAMESPACE = re.compile(r"^([0-9a-z_\-.]:)?.*$")

SCHEMA_PROVIDER_BITMAP = {
    "type": "object",
    "properties": {
        "type": {"const": "bitmap"},
        "file": {"type": "string", "minLength": 1, "pattern": SCHEMA_PATTERN_NAMESPACE.pattern},
        "height": {"type": "integer", "minimum": 1, "maximum": 512, "default": 8},
        "ascent": {"type": "integer", "minimum": -512, "maximum": 512},
        "chars": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "comment": {"type": "string"},
    },
    "required": ["type", "file", "ascent", "chars"],
    "additionalProperties": False,
}
"""A JSON schema to validate "bitmap" providers against."""

SCHEMA_PROVIDER_SPACE = {
    "type": "object",
    "properties": {
        "type": {"const": "space"},
        "advances": {
            "type": "object",
            "minLength": 1,
            "patternProperties": {RANGESTRING_FULL.pattern: {"type": "integer", "minimum": -256, "maximum": 256}},
        },
        "comment": {"type": "string"},
    },
    "required": ["type", "advances"],
    "additionalProperties": False,
}
"""A schema to validate "space" providers against."""

SCHEMA_PROVIDER_LEGACY_UNICODE = {
    "type": "object",
    "properties": {
        "type": {"const": "legacy_unicode"},
        "sizes": {"type": "string", "minLength": 1, "pattern": SCHEMA_PATTERN_NAMESPACE.pattern},
        "template": {"type": "string", "minLength": 1, "pattern": SCHEMA_PATTERN_NAMESPACE.pattern},
        "comment": {"type": "string"},
    },
    "required": ["type", "sizes", "template"],
    "additionalProperties": False,
}
"""A schema to validate "legacy_unicode" providers against."""

SCHEMA_PROVIDER_TTF = {
    "type": "object",
    "properties": {
        "type": {"const": "ttf"},
        "file": {"type": "string", "minLength": 1, "pattern": SCHEMA_PATTERN_NAMESPACE.pattern},
        "shift": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
        "size": {"type": "number", "minimum": 1},
        "oversample": {"type": "number", "minimum": 1},
        "skip": {"type": ["string", "array"]},
        "comment": {"type": "string"},
    },
    "required": ["type", "file", "shift", "size", "oversample"],
    "additionalProperties": False,
}
"""A schema to validate "ttf" providers against."""

SCHEMA_PROVIDER_OPTIONS = {
    "type": "object",
    "properties": {
        "type": {"enum": ["options", "mcfonts:options"]},
        "fields": {
            "type": "object",
            "properties": {
                "fullwidth": {
                    "type": "object",
                    "patternProperties": {RANGESTRING_FULL.pattern: {"type": "boolean"}},
                },
                "shift": {
                    "type": "object",
                    "patternProperties": {
                        RANGESTRING_FULL.pattern: {
                            "type": "array",
                            "minItems": 2,
                            "maxItems": 2,
                            "items": {"type": "integer"},
                        }
                    },
                },
                "spacing": {
                    "type": "object",
                    "patternProperties": {RANGESTRING_FULL.pattern: {"type": "integer", "minimum": 0}},
                },
                "width": {
                    "type": "object",
                    "patternProperties": {RANGESTRING_FULL.pattern: {"type": "integer"}},
                },
            },
        },
        "comment": {"type": "string"},
    },
    "required": ["type"],
    "additionalProperties": False,
}
"""A schema to validate "options" providers against."""

OPTION_FIELDS = {
    "width",
    "fullwidth",
    "shift",
    "spacing",
}

PADDING_CHARS = {"\0", " "}
"""Characters that act as padding; glyphs cannot be assigned to these chars."""

UNKNOWN_FIELD = "???"
