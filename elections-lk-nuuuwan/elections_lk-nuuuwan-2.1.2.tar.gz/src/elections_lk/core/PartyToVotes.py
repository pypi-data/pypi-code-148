from utils import Log

from elections_lk.base import ValueDict
from elections_lk.core.PartyToSeats import PartyToSeats

log = Log('PartyToVotes')


class PartyToVotes(ValueDict):
    @property
    def winning_party(self) -> str:
        return self.items_sorted()[0][0]

    def get_eligible_party_to_seats(self, p_limit):
        vote_limit = self.total * p_limit
        return PartyToVotes(
            {x[0]: x[1] for x in self.items() if x[1] >= vote_limit}
        )

    def get_party_to_bonus_seats(self, bonus) -> PartyToSeats:
        return PartyToSeats({self.winning_party: bonus})

    def get_party_to_int_seats(self, total_seats):
        return PartyToSeats(
            {
                party: (int)(votes * total_seats / self.total)
                for party, votes in self.items()
            }
        )

    def get_party_to_rem(self, total_seats) -> dict[str, float]:
        return {
            party: (votes * total_seats / self.total) % 1
            for party, votes in self.items()
        }

    @staticmethod
    def get_party_to_rem_seats(total_rem_seats, party_to_rem) -> PartyToSeats:
        party_to_rem_seats = {}
        sorted_party_and_rem = sorted(
            party_to_rem.items(), key=lambda x: x[1], reverse=True
        )
        for i in range(0, total_rem_seats):
            party = sorted_party_and_rem[i][0]
            party_to_rem_seats[party] = 1
        return PartyToSeats(party_to_rem_seats)

    def get_party_to_seats(self, total_seats, p_limit, bonus) -> PartyToSeats:
        party_to_votes = self.get_eligible_party_to_seats(p_limit)
        party_to_int_seats = party_to_votes.get_party_to_int_seats(
            total_seats - bonus
        )
        total_rem_seats = total_seats - party_to_int_seats.total - bonus
        return PartyToSeats.concat(
            [
                party_to_int_seats,
                PartyToVotes.get_party_to_rem_seats(
                    total_rem_seats,
                    party_to_votes.get_party_to_rem(total_seats - bonus),
                ),
                party_to_votes.get_party_to_bonus_seats(bonus),
            ]
        )
