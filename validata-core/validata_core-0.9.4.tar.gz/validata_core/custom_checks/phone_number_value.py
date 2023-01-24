import phonenumbers
from frictionless import Check, errors

from .utils import build_check_error, ignore_custom_check_for_empty_cell


def is_valid_number_for_country(phone_number: str, *, country_code=None):
    """Check if a phone number, giving an optional country_code.

    If country code is given, an additional check for valid_short_number is done.
    """
    try:
        pn = phonenumbers.parse(phone_number, country_code)
    except phonenumbers.NumberParseException:
        return False

    std_valid = phonenumbers.is_valid_number(pn)
    return (
        std_valid
        if country_code is None
        else std_valid or phonenumbers.is_valid_short_number(pn)
    )


def is_valid_phone_number(phonenumber: str):
    """Check if a phone number is a french or international valid one."""
    return is_valid_number_for_country(
        phonenumber, country_code="FR"
    ) or is_valid_number_for_country(phonenumber)


class PhoneNumberValueError(errors.CellError):
    """Custom error."""

    code = "phone-number-value"
    name = "Numéro de téléphone invalide"
    tags = ["#body"]
    template = (
        "La valeur '{cell}' n'est pas un numéro de téléphone valide.\n\n"
        " Les numéros de téléphone acceptés sont les numéros français à 10 chiffres"
        " (`01 99 00 27 37`) ou au format international avec le préfixe du pays"
        " (`+33 1 99 00 27 37`). Les numéros courts (`115` ou `3949`) sont"
        " également acceptés."
    )
    description = ""


class PhoneNumberValue(Check):
    """Check phone number validity."""

    code = "phone-number-value"
    possible_Errors = [PhoneNumberValueError]  # type: ignore

    def __init__(self, descriptor=None):
        super().__init__(descriptor)
        self.__column = self.get("column")

    def validate_start(self):
        if self.__column not in self.resource.schema.field_names:
            note = f"La colonne {self.__column!r} n'est pas trouvée."
            yield build_check_error(PhoneNumberValue.code, note)

    @ignore_custom_check_for_empty_cell
    def validate_row(self, row):
        cell_value = row[self.__column]

        if not is_valid_phone_number(cell_value):
            yield PhoneNumberValueError.from_row(row, note="", field_name=self.__column)

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["column"],
        "properties": {"column": {"type": "string"}},
    }
