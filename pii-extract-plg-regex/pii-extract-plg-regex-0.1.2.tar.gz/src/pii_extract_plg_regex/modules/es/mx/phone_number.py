"""
Argentinian phone numbers, using only libphonenumbers
"""
import re

from typing import Iterable, Tuple

import phonenumbers

from pii_data.types import PiiEnum

# Regex for phone numbers
PHONE_REGEX = r"""
  (?<![\w\+])
  (?:
     \d{2} \s? \d{4} \s? \d{4}
     |
     \d{3} \s? \d{3} \s? \d{4}
  )
  \b
"""

# Context that must be found around the phone number
CONTEXT_REGEX = r"""
 \b
 (?:
   tel[ée]fonos? |
   (?: tf | tel | tel[éf] | tfno ) \. |        # abbreviations
   celular (?: es )? |                         # mobile
   ll[aá]m[aeoáéó][bdilmrs]?\w*                # conjugation for "llamar"
 )
 (?! \w )
"""

# ----------------------------------------------------------------------------

# compiled regex
_REGEX = None


def Mexican_phone_number(text: str) -> Iterable[Tuple[str, int]]:
    """
    Mexican Phone Numbers
    """
    # Compile regex if needed
    global _REGEX
    if _REGEX is None:
        _REGEX = re.compile(PHONE_REGEX, flags=re.X)

    # Find all instances
    for match in _REGEX.finditer(text):
        item_value = match.group()
        ph = phonenumbers.parse(item_value, "MX")
        if phonenumbers.is_valid_number_for_region(ph, "MX"):
            yield item_value, match.start()


# ---------------------------------------------------------------------

PII_TASKS = {
    "class": "callable",
    "task": Mexican_phone_number,
    "pii": {
        "type": PiiEnum.PHONE_NUMBER,
        "subtype": "Mexican phone number",
        "method": "soft-regex,context",
        "context": {
            "type": "regex",
            "value": CONTEXT_REGEX,
            "width": [64, 64]
        }
    }
}
