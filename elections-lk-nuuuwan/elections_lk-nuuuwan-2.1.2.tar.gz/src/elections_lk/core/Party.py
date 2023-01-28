PARTY_TO_COLOR = {
    'ACMC': '#080',
    'AITC': '#ff0',
    'CWC': '#f80',
    'ELMSP': '#f00',
    'EPDP': '#f00',
    'IG': '#eee',
    'IG2': '#eee',
    'IG3': '#eee',
    'ITAK': '#ff0',
    'JVP': '#f00',
    'MNA': '#080',
    'NC': '#080',
    'SLFP': '#008',
    'SLMC': '#080',
    'SLPP': '#800',
    'TULF': '#f00',
    'UNP': '#0c0',
    'UPFA': '#00f',
}


class Party:
    DEFAULT_COLOR = '#444'

    def __init__(self, party: str):
        self.party = party

    @property
    def color(self):
        return PARTY_TO_COLOR.get(self.party, Party.DEFAULT_COLOR)
