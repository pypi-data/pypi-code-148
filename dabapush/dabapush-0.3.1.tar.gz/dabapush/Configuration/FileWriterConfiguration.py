"""FileWriterConfiguration provides a base class for file-based Writers."""
from datetime import datetime
from string import Template
from typing import Dict, Optional

from .WriterConfiguration import WriterConfiguration


class FileWriterConfiguration(WriterConfiguration):
    """Abstract class describing configuration items for a file based writer"""

    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: str = ".",
        name_template: str = "${date}_${time}_${name}.${type}",
    ) -> None:
        super().__init__(name, id=id, chunk_size=chunk_size)

        self.path = path
        self.name_template = name_template

    def make_file_name(self, additional_keys: Optional[Dict] = None) -> str:
        """Interpolate a fitting file name.

        params:
          additional_keys :
            dict:  (Default value = {})

        returns:
          Interpolated file name as str.
        """
        now = datetime.now()
        return Template(self.name_template).substitute(
            **{
                "date": datetime.strftime(now, "%Y-%m-%d"),
                "time": datetime.strftime(now, "%H%M"),
                "name": self.name,
                "id": self.id,
                **(additional_keys or {}),
            }
        )

    def set_name_template(self, template: str):
        """Sets the template string.

        params:
          template: str
            Template string to use.
        """
        self.name_template = template
