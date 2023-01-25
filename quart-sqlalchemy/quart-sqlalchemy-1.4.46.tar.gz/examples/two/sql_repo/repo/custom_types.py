from typing import Any
from typing import Optional

import sqlalchemy.types as types
from sql_repo.ciphers import OID
from sqlalchemy.sql.type_api import _T
from sqlalchemy.sql.type_api import Dialect


class OIDType(types.TypeDecorator):
    impl = types.Integer
    python_type = OID
    cache_ok = True

    def __init__(self, *args, use_ecc=True, **kwargs):
        self.use_ecc = use_ecc
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        """Receive the target type and convert it to the be stored in the database."""
        if value is None:
            return

        return OID(value).decode()

    def process_result_value(self, value: Optional[Any], dialect: Any) -> Optional[_T]:
        """Receive a raw value from the database and convert it to the target type."""
        if value is None:
            return

        return OID(value)

    def copy(self, **kwargs):
        return OIDType(self._value, **kwargs)
