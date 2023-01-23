import re

from .us_uk import uk, us
from .year import covered_year

date = rf"{us}|{uk}"

report_date_variants = rf"""
    (?P<post_report_full_date>
        (?P<naked_date>
            {us}|{uk}
        )|
        (
            \[ # open bracket
            (?P<brackets_date>
                {us}|{uk}
            )
            \] # close bracket
        )|
        (
            \( # open parenthesis
            (?P<parents_date>
                {us}|{uk}
            )
            \) # close parenthesis
        )
    )
    """
"""
US / UK regex cannot contain group names since these
will be used as alternative patterns, i.e. as bracketed us / uk dates,
parenthesis etc.
"""

dates_pattern = re.compile(report_date_variants, re.X | re.I)

report_date_regex = rf"""
    (?P<report_date>
        {covered_year}|
        {report_date_variants}
    )
"""
