from dataclasses import dataclass

from elections_lk.core import FinalResult
from elections_lk.elections.Election import Election


@dataclass
class ElectionLocalAuthority(Election):
    '''LocalAuthority election.'''

    lg_results: list[FinalResult]

    election_type = 'LocalAuthority'
    years = [2018]

    def to_dict(self):
        return {
            'year': self.year,
            'lg_results': [r.to_dict() for r in self.lg_results],
        }
