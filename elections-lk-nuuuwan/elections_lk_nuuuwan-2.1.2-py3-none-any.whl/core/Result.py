from dataclasses import dataclass
from functools import cached_property

from elections_lk.core.PartyToVotes import PartyToVotes
from elections_lk.core.SummaryStatistics import SummaryStatistics


@dataclass
class Result:
    region_id: str
    summary_statistics: SummaryStatistics
    party_to_votes: PartyToVotes

    @cached_property
    def total_votes(self) -> int:
        return self.party_to_votes.total

    @classmethod
    def concat(cls, concat_region_id: str, result_list: list):
        summary_statistics = SummaryStatistics.concat(
            [r.summary_statistics for r in result_list]
        )

        party_to_votes = PartyToVotes.concat(
            [r.party_to_votes for r in result_list]
        )

        return cls(
            region_id=concat_region_id,
            summary_statistics=summary_statistics,
            party_to_votes=party_to_votes,
        )

    @classmethod
    def mapAndConcat(cls, result_list: list, func_map) -> list:
        concat_region_id_to_result_list = {}
        for result in result_list:
            concat_region_id = func_map(result.region_id)
            if concat_region_id not in concat_region_id_to_result_list:
                concat_region_id_to_result_list[concat_region_id] = []
            concat_region_id_to_result_list[concat_region_id].append(result)

        result2_list = []
        for (
            concat_region_id,
            result_list,
        ) in concat_region_id_to_result_list.items():
            result2_list.append(cls.concat(concat_region_id, result_list))

        return result2_list
