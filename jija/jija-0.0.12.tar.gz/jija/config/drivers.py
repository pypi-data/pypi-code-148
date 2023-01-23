from jija.config import base, fields
from jija import drivers


class DriversConfig(base.Config):
    DOCS: drivers.DocsDriver = fields.ClassField(
        class_pattern=drivers.DocsDriver, default=drivers.DocsDriver)
    DATABASE: drivers.DatabaseDriver = fields.ClassField(
        class_pattern=drivers.DatabaseDriver, default=drivers.DatabaseDriver)

    def __init__(self, *, docs=None, database=None):
        super().__init__(docs=docs, database=database)
