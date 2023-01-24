import stdnum.fr.siret
from frictionless import Check, errors

from .utils import build_check_error, ignore_custom_check_for_empty_cell


class FrenchSiretValueError(errors.CellError):
    """Custom error."""

    code = "french-siret-value"
    name = "Numéro SIRET invalide"
    tags = ["#body"]
    template = "La valeur {cell} n'est pas un numéro SIRET français valide."
    description = (
        "Le numéro de SIRET indiqué n'est pas valide selon la définition"
        " de l'[INSEE](https://www.insee.fr/fr/metadonnees/definition/c1841)."
    )


class FrenchSiretValue(Check):
    """Check french SIRET number validity."""

    code = "french-siret-value"
    possible_Errors = [FrenchSiretValueError]  # type: ignore

    def __init__(self, descriptor=None):
        super().__init__(descriptor)
        self.__column = self.get("column")

    def validate_start(self):
        if self.__column not in self.resource.schema.field_names:
            note = f"La colonne {self.__column!r} n'est pas trouvée."
            yield build_check_error(FrenchSiretValue.code, note)

    @ignore_custom_check_for_empty_cell
    def validate_row(self, row):
        cell_value = row[self.__column]

        if not stdnum.fr.siret.is_valid(cell_value):
            yield FrenchSiretValueError.from_row(row, note="", field_name=self.__column)

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["column"],
        "properties": {"column": {"type": "string"}},
    }
