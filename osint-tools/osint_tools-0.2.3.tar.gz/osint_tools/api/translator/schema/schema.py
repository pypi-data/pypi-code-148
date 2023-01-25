from enum import Enum

# frk	German Fraktur
# deu	German
tess_lang_dict = {
	'german': 'deu',
	'german_fraktur': 'frk',
	'spanish': 'spa',
}
trans_lang_dict = {
    'auto': 'auto',
    'english': 'en',
	'german': 'de',
}

class TranslatorLangCodes(str, Enum):
    # auto = 'auto'
    english = 'en'
    german = 'de'
    # german_fraktur = 'frk'
    spanish = 'es'

class TessLangCodes(str, Enum):
    en = 'en'
    de = 'deu'
    # german_fraktur = 'frk'
    es = 'spa'
