from dataclasses import dataclass
from functools import cached_property

from gig import Ent, EntType, GIGTable

from elections_lk.core.FinalResult import FinalResult
from elections_lk.core.PartyToSeats import PartyToSeats
from elections_lk.elections.Election import Election


@dataclass
class ElectionLocalAuthority(Election):
    @classmethod
    def get_election_type(cls):
        return 'local-authority'

    @classmethod
    def get_years(cls):
        return [2018]

    @classmethod
    def get_gig_table(cls, year: int):
        measurement = f'government-elections-{cls.get_election_type()}-votes'
        region_str = 'regions-lg'
        time_str = str(year)
        return GIGTable(measurement, region_str, time_str)

    @classmethod
    def get_gig_table_seats(cls, year: int):
        measurement = f'government-elections-{cls.get_election_type()}-seats'
        region_str = 'regions-lg'
        time_str = str(year)
        return GIGTable(measurement, region_str, time_str)

    @property
    def lg_results(self):
        return self.results

    @classmethod
    def get_ent_list(cls):
        lg_list = Ent.list_from_type(EntType.LG)
        return lg_list

    @cached_property
    def lg_final_results(self):
        lg_results = self.lg_results
        gig_table_seats = self.get_gig_table_seats(self.year)
        lg_final_results = []
        for result in lg_results:
            id = result.region_id
            lg = Ent.from_id(id)
            raw_seats_d = lg.gig(gig_table_seats)
            party_to_seats = {}
            for k, v in raw_seats_d.dict.items():
                if k not in ['valid', 'rejected', 'polled', 'electors']:
                    party_to_seats[k] = v
            final_result = FinalResult.fromResult(
                result, PartyToSeats(party_to_seats)
            )
            lg_final_results.append(final_result)
        return lg_final_results

    @cached_property
    def district_final_results(self) -> list[FinalResult]:
        '''Get final results for each electoral district.'''
        district_id_to_lg_final_results = {}
        for lg_final_result in self.lg_final_results:
            district_id = 'LK-' + lg_final_result.region_id[3:5]
            if district_id not in district_id_to_lg_final_results:
                district_id_to_lg_final_results[district_id] = []
            district_id_to_lg_final_results[district_id].append(
                lg_final_result
            )

        district_final_results = []
        for (
            district_id,
            lg_final_results_for_district,
        ) in district_id_to_lg_final_results.items():
            district_final_result = FinalResult.concat(
                district_id,
                lg_final_results_for_district,
            )
            district_final_results.append(district_final_result)
        return district_final_results

    @cached_property
    def country_final_result(self) -> FinalResult:
        return FinalResult.concat('LK', self.lg_final_results)
