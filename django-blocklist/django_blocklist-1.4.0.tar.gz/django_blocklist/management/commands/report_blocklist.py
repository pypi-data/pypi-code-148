"""Print summary information about the data in the blocklist."""
import datetime
from collections import Counter
from operator import itemgetter
from typing import Iterable, Tuple

from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum

from ...models import BlockedIP


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            "--reason",
            default=[],
            action="append",
            help="Restrict report to IPs with this reason (muliple reasons can be passed)",
        )

    help = __doc__

    def handle(self, *args, **options):
        entries = BlockedIP.objects.all()
        if selected_reasons := options.get("reason"):
            entries = entries.filter(reason__in=selected_reasons)
        if entries.count() == 0:
            raise CommandError("No BlockedIP objects for report.")
        _grand_tally = BlockedIP.objects.all().aggregate(Sum("tally"))["tally__sum"]
        print(f"Total blocks of listed IPs: {intcomma(_grand_tally)}")
        print(f"Entries in blocklist: {intcomma(entries.count())}")
        _one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        print(f"Active in last 24 hours: {intcomma(entries.filter(last_seen__gte=_one_day_ago).count())}")
        print(
            f"Stale (added over 24h ago, not seen since): {intcomma(entries.filter(tally=1, last_seen__lt=_one_day_ago).count())}"
        )
        print()
        print_roster("Most recent", entries.exclude(tally=0).order_by("-last_seen")[:5])
        print_roster("Most active", entries.filter(tally__gt=0).order_by("-tally"), activity_calc=True)
        longest_lived = None
        how_long = datetime.timedelta(0)
        for entry in BlockedIP.objects.all():
            active_period = entry.last_seen - entry.first_seen
            if active_period > how_long:
                longest_lived, how_long = entry, active_period
        if longest_lived is not None:
            print(f"Longest lived:\n{longest_lived.verbose_str()}")
        if counts := reason_counts():
            print("\nIP counts by reason\n-------------------")
            _width = len(str(counts[0][1])) + 1
            for reason, count in counts:
                if not selected_reasons or reason in selected_reasons:
                    print(f"{count: {_width}} | {reason}")


def print_roster(title: str, queryset, activity_calc: bool = False) -> None:
    print(f"{title}:")
    activity = {}
    for perp in queryset:
        # For each IP, either print a line or calculate the rate, depending on activity_calc
        if activity_calc:
            days = max(1, (perp.last_seen - perp.first_seen).days)
            per_hour = perp.tally / days / 24
            activity[perp] = per_hour
        else:
            print(perp.verbose_str())
    if activity_calc:
        most_active = sorted(activity.items(), key=itemgetter(1), reverse=True)[:5]
        for perp, per_hour in most_active:
            print(f"{perp.verbose_str()} -- {round(per_hour)} per hour")
    print()


def reason_counts() -> Iterable[Tuple[str, int]]:
    reason_data = Counter(BlockedIP.objects.exclude(reason="").values_list("reason"))
    tuples = [(str(r[0][0]), r[1]) for r in reason_data.items()]
    return sorted(tuples, key=itemgetter(1), reverse=True)
