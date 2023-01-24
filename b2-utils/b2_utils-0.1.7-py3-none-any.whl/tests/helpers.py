import validate_docbr as _validate_docbr
from model_bakery import baker as _baker

from b2_utils import models as _models

__all__ = [
    "sample_city",
    "sample_address",
    "sample_phone",
    "sample_cpf",
    "sample_cnpj",
]


def sample_city(**kwargs):
    """Create and return a sample City"""

    return _baker.make(_models.City, **kwargs)


def sample_address(**kwargs):
    """Create and return a sample Address"""

    kwargs["city"] = kwargs.get("city", sample_city)
    return _baker.make(_models.Address, **kwargs)


def sample_phone(**kwargs):
    """Create and return a sample Phone"""

    return _baker.make(_models.Phone, **kwargs)


def sample_cpf():
    """Return a sample CPF"""

    return _validate_docbr.CPF().generate()


def sample_cnpj():
    """Return a sample CNPJ"""

    return _validate_docbr.CNPJ().generate()
