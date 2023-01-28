from dataclasses import dataclass
from functools import cached_property

from elections_lk.core.PartyToSeats import PartyToSeats
from elections_lk.core.Result import Result


@dataclass
class FinalResult(Result):
    party_to_seats: PartyToSeats

    @cached_property
    def total_seats(self) -> int:
        return self.party_to_seats.total

    @staticmethod
    def fromResult(result: Result, party_to_seats: PartyToSeats):
        return FinalResult(
            result.region_id,
            result.summary_statistics,
            result.party_to_votes,
            party_to_seats,
        )

    @classmethod
    def concat(cls, concat_region_id: str, result_list: list):

        result = Result.concat(concat_region_id, result_list)
        party_to_seats = PartyToSeats.concat(
            [r.party_to_seats for r in result_list]
        )

        return FinalResult(
            result.region_id,
            result.summary_statistics,
            result.party_to_votes,
            party_to_seats,
        )

    def to_dict(self):
        return dict(
            region_id=self.region_id,
            summary_statistics=self.summary_statistics.to_dict(),
            party_to_votes=self.party_to_votes.to_dict(),
            party_to_seats=self.party_to_seats.to_dict(),
        )
