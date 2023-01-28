from functools import cached_property

from elections_lk.core import FinalResult, PartyToSeats, Result
from elections_lk.elections.ElectionWithPDResults import ElectionWithPDResults
from elections_lk.elections.YEAR_TO_REGION_TO_SEATS import \
    YEAR_TO_REGION_TO_SEATS

P_LIMIT_ED = 0.05
BONUS_ED = 1

SEATS_NATIONAL_LIST = 29
P_LIMIT_NATIONAL_LIST = 0.0
BONUS_NATIONAL_LIST = 0


def get_ed_final_results(year: int, ed_result: Result) -> FinalResult:
    party_to_seats = ed_result.party_to_votes.get_party_to_seats(
        total_seats=YEAR_TO_REGION_TO_SEATS[year][ed_result.region_id],
        p_limit=P_LIMIT_ED,
        bonus=BONUS_ED,
    )

    return FinalResult.fromResult(ed_result, party_to_seats)


class ElectionParliamentary(ElectionWithPDResults):
    @classmethod
    def get_election_type(cls):
        return 'parliamentary'

    @classmethod
    def get_years(cls):
        return [1989, 1994, 2000, 2001, 2004, 2010, 2015, 2020]

    @cached_property
    def ed_final_results(self) -> list[FinalResult]:
        '''Get final results for each electoral district.'''
        ed_results = Result.mapAndConcat(
            self.pd_results, lambda region_id: region_id[:5]
        )

        return list(
            map(
                lambda ed_result: get_ed_final_results(self.year, ed_result),
                ed_results,
            )
        )

    @cached_property
    def national_list_final_result(self) -> FinalResult:
        '''Get final results for national list.'''
        country_result = Result.concat('LK', self.pd_results)
        party_to_seats = country_result.party_to_votes.get_party_to_seats(
            total_seats=SEATS_NATIONAL_LIST,
            p_limit=P_LIMIT_NATIONAL_LIST,
            bonus=BONUS_NATIONAL_LIST,
        )

        return FinalResult.fromResult(country_result, party_to_seats)

    @cached_property
    def country_final_result(self) -> FinalResult:
        '''Get final results for the country.'''
        country_result = Result.concat('LK', self.pd_results)
        return FinalResult.fromResult(
            country_result,
            PartyToSeats.concat(
                [
                    final_result.party_to_seats
                    for final_result in self.ed_final_results
                ]
                + [self.national_list_final_result.party_to_seats]
            ),
        )
