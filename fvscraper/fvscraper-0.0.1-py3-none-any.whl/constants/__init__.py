from .descriptive import filters as descriptive
from .fundamental import filters as fundamental
from .technical import filters as technical

FILTERS = {**descriptive, ** fundamental, **technical}