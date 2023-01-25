"""Consts."""

from typing import List

from spec.types import Request
from pydantic import AnyUrl, BaseModel, constr

max_query_limit = 500

cdn = 'https://cdn.pbilet.com/origin/'


class TypeCurrency(BaseModel):
    """Currency type."""

    pk: int
    name: constr(min_length=3, max_length=30)
    code: constr(min_length=3, max_length=3, to_upper=True)
    icon: AnyUrl


class Currency:
    """Currency registry."""

    fallback_pk: int = 1

    def __init__(self, currencies: List[TypeCurrency]) -> None:
        """Init."""
        self._currencies = currencies

    def get_by_pk(self, pk: int) -> TypeCurrency:
        """Get by pk."""

        for _currency in self._currencies:
            if _currency.pk == pk:
                return _currency

    def safe(self, pk: int) -> TypeCurrency:
        """Get safe with fallback."""
        currency = self.get_by_pk(pk=pk)
        return currency if currency else self.fallback_currency()

    def fallback_currency(self) -> TypeCurrency:
        """Fallback currency."""

        return self.get_by_pk(self.fallback_pk)

    def get_from_request(self, request: Request) -> TypeCurrency:
        """Get currency from request."""

        try:
            currency_pk = int(
                request.query_params.get(
                    'currency_id',
                    self.fallback_pk,
                ),
            )
        except Exception as any_fault:  # noqa
            return self.fallback_currency()

        type_currency = self.get_by_pk(currency_pk)
        return type_currency if type_currency else self.fallback_currency()


CURRENCIES = [
    TypeCurrency(
        pk=1,
        name='Российский рубль',
        code='RUB',
        icon=f'{cdn}2d9daa98-f163-4755-a745-75b47e442429.svg',
    ),
    TypeCurrency(
        pk=2,
        name='Доллар США',
        code='USD',
        icon=cdn.format(name='472fa55e-3761-40f7-a323-1f15b60e5b1c'),
    ),
    TypeCurrency(
        pk=3,
        name='Евро',
        code='EUR',
        icon=cdn.format(name='eeae5bdd-6018-4ab0-afa0-3c6f02a55692'),
    ),
    TypeCurrency(
        pk=4,
        name='Казахстанский тенге',
        code='KZT',
        icon=cdn.format(name='73eae55e-e059-4ce7-a8c4-6a97937be725'),
    ),
    TypeCurrency(
        pk=5,
        name='Белорусский рубль',
        code='BYN',
        icon=cdn.format(name='a24b351f-0735-47b1-bf4b-fdc0918be242'),
    ),
    TypeCurrency(
        pk=6,
        name='Азербайджанский манат',
        code='AZN',
        icon=cdn.format(name='e6e4fe14-af6e-481e-8f0a-0947a8821f41'),
    ),
    TypeCurrency(
        pk=7,
        name='Украинская гривна',
        code='UAH',
        icon=cdn.format(name='fe879b07-30ca-4694-b383-940b9874b0b9'),
    ),
    TypeCurrency(
        pk=9,
        name='Армянский драм',
        code='AMD',
        icon=cdn.format(name='1ff43218-98ad-4f97-9256-36eeec02eaba'),
    ),
    TypeCurrency(
        pk=10,
        name='Узбекский сум',
        code='UZS',
        icon=cdn.format(name='c9abce2d-b8a9-4b3c-963e-4334ae00af9f'),
    ),
    TypeCurrency(
        pk=11,
        name='Новый израильский шекель',
        code='ILS',
        icon=cdn.format(name='caee4412-42f3-42ce-8a24-711233dc03ea'),
    ),
    TypeCurrency(
        pk=12,
        name='Чешская крона',
        code='CZK',
        icon=cdn.format(name='ae3af20a-6c70-4b7b-87b4-dba35f4dc4c6'),
    ),
    TypeCurrency(
        pk=13,
        name='Швейцарский франк',
        code='CHF',
        icon=cdn.format(name='d52f5b79-11a4-435d-ad76-03eeced916ec'),
    ),
    TypeCurrency(
        pk=14,
        name='Дирхам',
        code='AED',
        icon=cdn.format(name='24185099-bd37-43f0-91b0-1cc19fb97c7d'),
    ),
    TypeCurrency(
        pk=15,
        name='Бразильский реал',
        code='BRL',
        icon=cdn.format(name='6332172c-9572-4e27-bbfd-37eb4ab3923b'),
    ),
]
