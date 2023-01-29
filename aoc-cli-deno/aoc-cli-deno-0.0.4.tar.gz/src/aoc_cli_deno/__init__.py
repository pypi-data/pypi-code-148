from .getter import Getter
from .initialiser import Initialiser
from .opener import Opener
from .runner import Runner
from .submitter import Submitter
from .language import __language__

__structure__ = ["year", "language", "day"]
__all__ = ["__language__", "__structure__", "Getter", "Initialiser", "Opener", "Runner", "Submitter"]