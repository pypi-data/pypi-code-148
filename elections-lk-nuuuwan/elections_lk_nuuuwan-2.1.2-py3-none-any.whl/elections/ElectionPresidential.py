from functools import cached_property

from elections_lk.core import FinalResult, PartyToSeats, Result
from elections_lk.elections.ElectionWithPDResults import ElectionWithPDResults


class ElectionPresidential(ElectionWithPDResults):
    @classmethod
    def get_election_type(cls):
        return 'presidential'

    @classmethod
    def get_years(cls):
        return [1982, 1988, 1994, 1999, 2005, 2010, 2015, 2019]

    @cached_property
    def ed_results(self) -> list[Result]:
        '''Get results for each electoral district.'''
        return Result.mapAndConcat(
            self.pd_results, lambda region_id: region_id[:5]
        )

    @cached_property
    def country_final_result(self) -> FinalResult:
        '''Get final results for the country.'''
        country_result = Result.concat('LK', self.pd_results)
        winning_party = country_result.party_to_votes.keys_sorted()[0]
        return FinalResult.fromResult(
            country_result,
            party_to_seats=PartyToSeats({winning_party: 1}),
        )
