from dataclasses import dataclass

from utils import Log

from elections_lk.core import PartyToVotes, Result, SummaryStatistics

log = Log('Election')


def correct_int(x):
    return (int)(round(x, 0))


@dataclass
class Election:
    year: int
    results: list

    @classmethod
    def load(cls, year):
        gig_table = cls.get_gig_table(year)
        ent_list = cls.get_ent_list()

        results = []
        for ent in ent_list:
            try:
                result_raw = ent.gig(gig_table)
            except BaseException:
                log.warning(
                    f'Could not find result for {ent.id}'
                    + f' in {gig_table.table_id}'
                )
                continue

            party_to_votes = {}
            for k, v in result_raw.dict.items():
                if k not in ['valid', 'rejected', 'polled', 'electors']:
                    party_to_votes[k] = correct_int(v)

            result = Result(
                region_id=ent.id,
                summary_statistics=SummaryStatistics(
                    valid=correct_int(result_raw.valid),
                    rejected=correct_int(result_raw.rejected),
                    polled=correct_int(result_raw.polled),
                    electors=correct_int(result_raw.electors),
                ),
                party_to_votes=PartyToVotes(party_to_votes),
            )
            results.append(result)
        return cls(year=year, results=results)
