"""Package 'fedinesia' level definitions."""
import sys
from typing import Any

from typing_extensions import Final


__version__: Final[str] = "2.3.0"
__display_name__: Final[str] = "Fedinesia"
__package_name__: Final[str] = __display_name__.lower()
USER_AGENT: Final[
    str
] = f"{__display_name__}_v{__version__}_Python_{sys.version.split()[0]}"

Status = dict[str, Any]
