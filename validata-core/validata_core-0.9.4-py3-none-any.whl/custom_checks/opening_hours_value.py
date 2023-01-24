import opening_hours
from frictionless import Check, errors

from .utils import build_check_error, ignore_custom_check_for_empty_cell


class OpeningHoursValueError(errors.CellError):
    """Custom error."""

    code = "opening-hours-value"
    name = "Horaires d'ouverture incorrects"
    tags = ["#body"]
    template = (
        "La valeur '{cell}' n'est pas une définition d'horaire d'ouverture correcte.\n\n"
        " Celle-ci doit respecter la spécification"
        " [OpenStreetMap](https://wiki.openstreetmap.org/wiki/Key:opening_hours)"
        " de description d'horaires d'ouverture."
    )
    description = ""


class OpeningHoursValue(Check):
    """Check opening hours validity."""

    code = "opening-hours-value"
    possible_Errors = [OpeningHoursValueError]  # type: ignore

    def __init__(self, descriptor=None):
        super().__init__(descriptor)
        self.__column = self.get("column")

    def validate_start(self):
        if self.__column not in self.resource.schema.field_names:
            note = f"La colonne {self.__column!r} n'est pas trouvée."
            yield build_check_error(OpeningHoursValue.code, note)

    @ignore_custom_check_for_empty_cell
    def validate_row(self, row):
        cell_value = row[self.__column]

        if not opening_hours.validate(cell_value):
            yield OpeningHoursValueError.from_row(
                row, note="", field_name=self.__column
            )

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["column"],
        "properties": {"column": {"type": "string"}},
    }
