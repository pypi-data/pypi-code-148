"Datatypes used by oracle api"

from datetime import datetime

Column = dict[str, str | int | float | bytes | datetime]
Row = list[Column]
