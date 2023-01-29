from pydantic import BaseModel, validator
from enum import Enum
# https://tesseract-ocr.github.io/tessdoc/Data-Files#format-of-traineddata-files

'''
{
  "results": [
    {
      "status": {
        "code": ...,
        "message": ...
      },
      "name": ...,
      "md5": ...,
      "entities": [
        {
          "kind": "objects",
          "name": "text",
          "objects": [
            {
              "box": ...,
              "entities": [
                {
                  "kind": "text",
                  "name": "text",
                  "text": ...
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
'''

class Entity(BaseModel):
    text: str

    # @validator('text', pre = True)
    # def text_before(cls, v):

    # @validator('text', pre=False)
    # def text_after(cls, v, values, **kwargs):
        # return ''

class FileSchema(BaseModel):
    name: str
    md5: str = 'md5'
    entities: list[Entity]

class FileList(BaseModel):
    file_list: list[FileSchema]

class EnumBase(Enum):

    @classmethod
    def list_name_or_value(cls, name_or_value: str) -> list[str]:
        """List names or values of derived enum class

        Args:
            name_or_value (str): name  | value

        Returns:
            (List[str]): list of derived enum classes names or values
        """
        assert name_or_value in ['name', 'value'], 'must be name or value'
        return [getattr(i, name_or_value) for i in cls.__members__.values()]

    @classmethod
    def get_lang_dict(cls) -> list[dict[str, str]]:
        return [{"language": i.name, "code": i.value} for i in cls.__members__.values()]
        # return [i for i in cls.__members__]

    # @classmethod
    # def list_values_to_titlecase(cls):
    #     def to_title_case(s):
    #         return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
    #     return [to_title_case(i.value.replace('_', ' ')) for i in cls.__members__.values()]

class EnumAutoBase(EnumBase):
    def _generate_next_value_(name, start, count, last_values):
        return name


class TranslatorLangCodes(str, EnumBase):
    # auto = 'auto'
    english = 'eng'
    german = 'de'
    # german_fraktur = 'frk'
    spanish = 'spa'
    # goog translate
    afrikaans='af'
    albanian='sq'
    amharic='am'
    arabic='ar'
    armenian='hy'
    azerbaijani='az'
    basque='eu'
    belarusian='be'
    bengali='bn'
    bosnian='bs'
    bulgarian='bg'
    catalan='ca'
    cebuano='ceb'
    chichewa='ny'
    chinese_simplified='zh-CN'
    chinese_traditional='zh-TW'
    corsican='co'
    croatian='hr'
    czech='cs'
    danish='da' 
    dutch='nl'
    esperanto='eo'
    estonian='et'
    filipino='tl'
    finnish='fi'
    french='fr'
    frisian='fy'
    galician='gl'
    georgian='ka'
    # german='de'
    greek='el'
    gujarati='gu'
    haitian_creole='ht' 
    hausa='ha'
    hawaiian='haw' 
    hebrew='iw' 
    hindi='hi' 
    hmong='hmn'
    hungarian='hu' 
    icelandic='is' 
    igbo='ig'
    indonesian='id' 
    irish='ga'
    italian='it' 
    japanese='ja' 
    javanese='jw' 
    kannada='kn' 
    kazakh='kk' 
    khmer='km'
    kinyarwanda='rw' 
    korean='ko' 
    kurdish='ku' 
    kyrgyz='ky' 
    lao='lo' 
    latin='la', 
    latvian='lv'
    lithuanian='lt' 
    luxembourgish='lb' 
    macedonian='mk' 
    malagasy='mg' 
    malay='ms' 
    malayalam='ml' 
    maltese='mt' 
    maori='mi' 
    marathi='mr' 
    mongolian='mn' 
    myanmar='my' 
    nepali='ne' 
    norwegian='no' 
    odia='or'
    pashto='ps' 
    persian='fa' 
    polish='pl' 
    portuguese='pt' 
    punjabi='pa' 
    romanian='ro' 
    russian='ru' 
    samoan='sm'
    scots_gaelic='gd' 
    serbian='sr' 
    sesotho='st' 
    shona='sn' 
    sindhi='sd' 
    sinhala='si' 
    slovak='sk'
    slovenian='sl' 
    somali='so' 
    # spanish='es'
    sundanese='su' 
    swahili='sw' 
    swedish='sv' 
    tajik='tg'
    tamil='ta'
    tatar='tt'
    telugu='te'
    thai='th'
    turkish='tr' 
    turkmen='tk'
    ukrainian='uk' 
    urdu='ur'
    uyghur='ug' 
    uzbek='uz'
    vietnamese='vi' 
    welsh='cy' 
    xhosa='xh'
    yiddish='yi' 
    yoruba='yo' 
    zulu='zu'



class TessLangCodes(str, EnumBase):
    # auto = None
    eng='eng'# English
    # enm='enm'# English, Middle (1100-1500)
    de = 'deu'
    # german_fraktur = 'frk'
    spa = 'spa'
    # es = 'spa'# spanish
    # spa='spa'# Castilian

    ell='ell'# Greek, Modern (1453-)
    epo='epo'# Esperanto
    est='est'# Estonian
    eus='eus'# Basque
    afr='afr'# Afrikaans
    amh='amh'# Amharic
    ara='ara'# Arabic
    asm='asm'# Assamese
    aze='aze'# Azerbaijani
    aze_cyrl='aze_cyrl'# Cyrillic
    bel='bel'# Belarusian
    ben='ben'# Bengali
    bod='bod'# Tibetan
    bos='bos'# Bosnian
    bul='bul'# Bulgarian
    cat='cat'# Valencian
    ceb='ceb'# Cebuano
    ces='ces'# Czech
    chi_sim='chi_sim'# Simplified
    chi_tra='chi_tra'# Traditional
    # chr='chr'# Cherokee
    cym='cym'# Welsh
    dan='dan'# Danish
    dzo='dzo'# Dzongkha
    fas='fas'# Persian
    fin='fin'# Finnish
    fra='fra'# French
    frk='frk'# German Fraktur
    frm='frm'# French, Middle (ca. 1400-1600)
    gle='gle'# Irish
    glg='glg'# Galician
    grc='grc'# Greek, Ancient (-1453)
    guj='guj'# Gujarati
    hat='hat'# Haitian; Haitian Creole
    heb='heb'# Hebrew
    hin='hin'# Hindi
    hrv='hrv'# Croatian
    hun='hun'# Hungarian
    iku='iku'# Inuktitut
    ind='ind'# Indonesian
    isl='isl'# Icelandic
    ita='ita'# Italian
    ita_old='ita_old'# Italian - Old
    jav='jav'# Javanese
    jpn='jpn'# Japanese
    kan='kan'# Kannada
    kat='kat'# Georgian
    kat_old='kat_old'# Georgian - Old
    kaz='kaz'# Kazakh
    khm='khm'# Central Khmer
    kir='kir'# Kirghiz; Kyrgyz
    kor='kor'# Korean
    kur='kur'# Kurdish
    lao='lao'# Lao
    lat='lat'# Latin
    lav='lav'# Latvian
    lit='lit'# Lithuanian
    mal='mal'# Malayalam
    mar='mar'# Marathi
    mkd='mkd'# Macedonian
    mlt='mlt'# Maltese
    msa='msa'# Malay
    mya='mya'# Burmese
    nep='nep'# Nepali
    nld='nld'# Flemish
    nor='nor'# Norwegian
    ori='ori'# Oriya
    pan='pan'# Panjabi; Punjabi
    pol='pol'# Polish
    por='por'# Portuguese
    pus='pus'# Pashto
    ron='ron'# Moldovan
    rus='rus'# Russian
    san='san'# Sanskrit
    sin='sin'# Sinhalese
    slk='slk'# Slovak
    slv='slv'# Slovenian
    spa_old='spa_old'# Old
    sqi='sqi'# Albanian
    srp='srp'# Serbian
    srp_latn='srp_latn'#Latin
    swa='swa'# Swahili
    swe='swe'# Swedish
    syr='syr'#Syriac
    tam='tam'# Tamil
    tel='tel'#Telugu
    tgk='tgk'# Tajik
    tgl='tgl'# Tagalog
    tha='tha'# Thai
    tir='tir'# Tigrinya
    tur='tur'# Turkish
    uig='uig'# Uyghur
    ukr='ukr'# Ukrainian
    urd='urd'# Urdu
    uzb='uzb'# Uzbek
    uzb_cyrl='uzb_cyrl'# Cyrillic
    # Vietnamese='vie'
    # Yiddish='yid'

