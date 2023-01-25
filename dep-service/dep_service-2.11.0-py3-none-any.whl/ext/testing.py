"""Testing ext funcs."""

import random

from dataclasses import dataclass
from datetime import datetime, timedelta

from decimal import Decimal

from httpx import AsyncClient as XClient
from faker import Faker as _Faker
from fastapi.testclient import TestClient as ApiClient
from starlette.testclient import TestClient as AppClient


@dataclass(frozen=True)
class I18nFaker:
    """I18n Faker interface."""

    en: _Faker
    ru: _Faker

    def shake(self) -> None:
        """Shake fakers."""
        _Faker.seed(random.randint(0, 99999))

    def faker(self, lang: str = None) -> _Faker:
        """Faker."""
        if not lang:
            return self.en
        return {'en': self.en, 'ru': self.ru}[lang]

    # Any randoms with locales

    def any_person_first_name(self, lang: str = None) -> str:
        """Any person first name, like `Katherine`."""
        self.shake()
        return str(self.faker(lang).first_name())

    def any_person_last_name(self, lang: str = None) -> str:
        """Any person last name, like `Fisher`."""
        self.shake()
        return str(self.faker(lang).last_name())

    def any_phone_number(self, lang: str = None) -> str:
        """Any phone number, like `(194)892-4115`."""
        self.shake()
        return str(self.faker(lang).phone_number())

    def any_company_theme(self, lang: str = None) -> str:
        """Any company theme, like `Iterate integrated e-markets`."""
        self.shake()
        return str(self.faker(lang).bs())

    def any_company_name(self, lang: str = None) -> str:
        """Any company name, like `Wagner LLC`."""
        self.shake()
        return str(self.faker(lang).company())

    def any_country(self, lang: str = None) -> str:
        """Any country, like `Russia`."""
        self.shake()
        return str(self.faker(lang).country())

    def any_city(self, lang: str = None) -> str:
        """Any city, like `Kursk`."""
        self.shake()
        return str(self.faker(lang).city())

    def any_address(self, lang: str = None) -> str:
        """Any address, like `PSC 4115, Box 7815\nAPO AA 41945`."""
        self.shake()
        return str(self.faker(lang).address())

    def any_street_address(self, lang: str = None) -> str:
        """Any street address, like `0487 Hull Village Suite 759`."""
        self.shake()
        return str(self.faker(lang).street_address())

    def any_building_number(self, lang: str = None) -> str:
        """Any building number, like `6048`."""
        self.shake()
        return str(self.faker(lang).building_number())

    def any_post_code(self, lang: str = None) -> str:
        """Any post code, like `50995`."""
        self.shake()
        return str(self.faker(lang).postcode())

    def any_barcode_ean(self, lang: str = None, **kwargs) -> str:
        """Any ean, like `0004876475931`."""
        self.shake()
        return str(self.faker(lang=lang).ean(**kwargs))

    def any_barcode_ean13(self, lang: str = None, **kwargs) -> str:
        """Any ean13, like `8242194892418`."""
        self.shake()
        return str(self.faker(lang=lang).ean13(**kwargs))

    def any_barcode_ean8(self, lang: str = None, **kwargs) -> str:
        """Any ean8, like `49048766`."""
        self.shake()
        return str(self.faker(lang=lang).ean8(**kwargs))

    def any_color_hex(self, lang: str = None) -> str:
        """Any color hex, like `#d82c08`."""
        self.shake()
        return str(self.faker(lang=lang).hex_color())

    def any_color_rgb(self, lang: str = None) -> str:
        """Any color rgb, like '197,215,20`."""
        self.shake()
        return str(self.faker(lang=lang).rgb_color())

    def any_currency(self, lang: str = None) -> str:
        """Any currency, like `Russian Ruble`."""
        self.shake()
        return str(self.faker(lang).currency_name())

    def any_currency_code(self, lang: str = None) -> str:
        """Any currency code, like `RUB`."""
        self.shake()
        return str(self.faker(lang).currency_code())

    def any_word(self, lang: str = None) -> str:
        """Any word, like `Bubble`."""
        self.shake()
        return self.faker(lang).word()

    def any_sentence(self, lang: str = None) -> str:
        """Any sentence, like `Rocks and roll with boobs`."""
        self.shake()
        return self.faker(lang).sentence()

    def any_credit_card_expire(self, lang: str = None) -> str:
        """Any card expire dates valid future, like `03/32`."""
        self.shake()
        end_date = self.any_dt_future_day() + timedelta(weeks=100)
        return self.faker(lang).credit_card_expire(end=end_date)

    def any_credit_card_expire_invalid(self, lang: str = None) -> str:
        """Any card expire invalid past dates, like `02/20`."""
        self.shake()
        return self.faker(lang).credit_card_expire(
            start=datetime.now() - timedelta(days=3200),
            end=datetime.now() - timedelta(days=250),
        )

    def any_credit_card_number(self, lang: str = None) -> str:
        """Any credit card number, like `6504876475938248`."""
        self.shake()
        return self.faker(lang).credit_card_number()

    def any_dt_am_pm(self, lang: str = None) -> str:
        """Any datetime am pm, like `AM`."""
        self.shake()
        return str(self.faker(lang).am_pm())

    def any_dt_day_ago(self, days: int = None) -> datetime:
        """Any past datetime."""
        current = datetime.now()
        if days:
            return current - timedelta(days=days)
        return current - timedelta(days=self.any_int_pos())

    def any_dt_future_day(self, days: int = None) -> datetime:
        """Any future datetime."""
        current = datetime.now()
        if days:
            return current + timedelta(days=days)
        return current + timedelta(days=self.any_int_pos())

    def any_dt_this_month(self, future: bool = True) -> datetime:
        """Any datetime this month."""
        if future:
            return datetime.combine(
                date=self.faker().date_this_month(after_today=True),
                time=datetime.min.time(),
            )
        return datetime.combine(
            date=self.faker().date_this_month(before_today=True),
            time=datetime.min.time(),
        )

    def any_dt_this_year(self, future: bool = True) -> datetime:
        """Any datetime this year."""
        if future:
            return datetime.combine(
                date=self.faker().date_this_year(after_today=True),
                time=datetime.min.time(),
            )
        return datetime.combine(
            date=self.faker().date_this_year(before_today=True),
            time=datetime.min.time(),
        )

    def any_email(self, lang: str = None) -> str:
        """Any email, like `achang@gmail.com`."""
        self.shake()
        return self.faker(lang).ascii_free_email()

    def any_domain_name(self, lang: str = None, level: int = 1) -> str:
        """Any domain name, like `williamson-hopkins.jackson.com`."""
        self.shake()
        return self.faker(lang).domain_name(levels=level)

    def any_host_name(self, lang: str = None, level: int = 1) -> str:
        """Any host name, like `web-12.williamson-hopkins.jackson.com`."""
        self.shake()
        return self.faker(lang).hostname(levels=level)

    def any_ipv4(self, lang: str = None) -> str:
        """Any ipv4, like `'171.174.170.81`."""
        self.shake()
        return self.faker(lang).ipv4()

    def any_image_url(
        self,
        width: int = None,
        height: int = None,
        lang: str = None,
    ) -> str:
        """Any image url, like `http://placehold.it/640x480`."""
        return str(self.faker(lang).image_url(width=width, height=height))

    def any_int(self, min_value: int = 0, max_value: int = 100) -> int:  # noqa
        """Any int from range."""
        random.seed(random.randint(0, 99999))
        return random.randint(min_value, max_value)

    def any_int_pos(self) -> int:  # noqa
        """Any int positive."""
        random.seed(random.randint(0, 99999))
        return self.any_int(min_value=1, max_value=100)  # noqa

    def any_int_neg(self) -> int:
        """Any int negative."""
        return self.any_int(min_value=-100, max_value=-1)

    def any_bool(self) -> bool:  # noqa
        """Any bool."""
        random.seed(random.randint(0, 99999))
        return random.choice([True, False])

    def any_url(self) -> str:
        """Any url."""
        self.shake()
        return self.faker().url()

    def any_money_amount_float(  # noqa
        self,
        min_amount: float = 0,
        max_amount: float = 99999.99,
    ) -> float:
        """Any money amount, like `1500.50` as float."""
        random.seed(random.randint(0, 99999))
        return round(random.uniform(min_amount, max_amount), ndigits=2)

    def any_money_amount_decimal(  # noqa
        self,
        min_amount: float = 0,
        max_amount: float = 99999.99,
    ) -> Decimal:
        """Any money amount, like `1500.50` as Decimal."""
        amount = round(random.uniform(min_amount, max_amount), ndigits=2)
        return Decimal(str(amount))


faker = I18nFaker(
    en=_Faker(locale='en_US'),
    ru=_Faker(locale='ru_RU'),
)


__all__ = (
    'ApiClient',
    'AppClient',
    'XClient',
    'faker',
)
