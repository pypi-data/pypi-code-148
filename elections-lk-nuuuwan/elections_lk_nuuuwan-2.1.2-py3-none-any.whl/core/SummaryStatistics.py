from dataclasses import dataclass


@dataclass
class SummaryStatistics:
    valid: int
    rejected: int
    polled: int
    electors: int

    FIELDS = ['valid', 'rejected', 'polled', 'electors']

    @property
    def p_rejected(self):
        return self.rejected / self.polled

    @property
    def p_valid(self):
        return self.valid / self.polled

    @property
    def p_turnout(self):
        return self.polled / self.electors

    @staticmethod
    def concat(
        summary_statistics_list: list,
    ):
        return SummaryStatistics(
            valid=sum([x.valid for x in summary_statistics_list]),
            rejected=sum([x.rejected for x in summary_statistics_list]),
            polled=sum([x.polled for x in summary_statistics_list]),
            electors=sum([x.electors for x in summary_statistics_list]),
        )

    def to_dict(self):
        return dict(
            valid=self.valid,
            rejected=self.rejected,
            polled=self.polled,
            electors=self.electors,
        )
