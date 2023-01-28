from time import localtime, strftime, time
from typing import Dict, List, Optional, Union

from aiohttp import ClientSession

from qiwimaster.exceptions import NumberError, QiwiAPIError, TokenError


class QiwiAPI(object):
    """
    Ассихронная библиотека для работы с Qiwi API, а также с QiwiP2P API.

    :token: ключ авторизации со страницы https://qiwi.com/api. Нужен для работы с аккаунтом.
    :auth_key: секретный ключ авторизации со страницы https://qiwi.com/p2p-admin/transfers/api. Нужен для выставления счетов.
    :phone: номер телефона киви кошелька. Указывается вместе с token.
    """

    def __init__(
        self, phone: str = None, token: str = None, auth_key: str = None
    ) -> None:

        if not token and not auth_key:
            raise TokenError(
                "Invalid Token or Auth Key! You can get it here: "
                "https://qiwi.com/api || https://qiwi.com/p2p-admin/transfers/api"
            )

        elif not phone and not auth_key:
            raise NumberError(
                "Invalid Number! Please, enter the Qiwi Wallet number."
            )

        self.token = token
        self.phone = phone
        self.auth_key = auth_key

        self.session = ClientSession(
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    async def balance(self, only: bool = False) -> Union[float, List[float]]:
        """
        Возвращает баланс счетов
        :param only: при True возвращает только первый счёт
        """

        if not self.token or not self.phone:
            raise TokenError(
                "Invalid Token or phone! You can get it here: https://qiwi.com/api"
            )

        balance = [
            wallet["balance"]["amount"]
            for wallet in await self.full_balance()
            if wallet["balance"]
        ]

        return balance[0] if only else balance

    def bill(
        self,
        price: int,
        lifetime: int = 10,
        currency: str = "RUB",
        comment: Optional[str] = None,
        bill_id: Optional[int] = None,
    ) -> dict:

        """
        Функция для выставления счёта.

        :price: сумма, которая будет в счёте.
        :lifetime: количество минут, столько будет действителен счёт.
        :currency: валюта, в которой будет счёт.
        :comment: комментарий, который будет указан в счёте.
        :bill_id: номер счёта. Устанавливается автоматически.
        """

        lifetime = strftime(
            "%Y-%m-%dT%H:%M:%S+03:00", localtime(time() + lifetime * 60)
        )

        qiwi_data = {
            "amount": {"currency": currency, "value": price},
            "comment": comment or "",
            "expirationDateTime": lifetime,
        }

        self.session.headers["Authorization"] = f"Bearer {self.auth_key}"

        return self.request(
            "PUT",
            f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id or self.random_id}",
            json=qiwi_data,
        )

    async def full_balance(self) -> List[Dict[str, Union[str, float]]]:

        self.session.headers["Authorization"] = f"Bearer {self.token}"

        response = await self.session.get(
            "https://edge.qiwi.com/funding-sources/v1/accounts/current"
        )
        json = await response.json()

        if "code" in json or "errorCode" in json:
            raise QiwiAPIError(json)

        return [
            {"type": account["type"], "balance": account["balance"]}
            for account in json["accounts"]
            if account["hasBalance"]
        ]

    def pay(
        self,
        number: int,
        amount: int,
        currency: str = "643",
        comment: Optional[str] = None,
    ) -> dict:

        """
        Функция для перевода денег другому человеку.

        :number: число, номер телефона, на который необходимо перевести деньги. Указывать в формате 89999999999.
        :amount: сумма перевода.
        :comment: комментарий, который будет указан в переводе.
        :currency: валюта, в которой будет перевод. 643 - рубль.
        """

        if not number:
            raise NumberError(
                "Invalid Number! Please, enter the number to which you want to transfer money."
            )

        elif not amount:
            raise QiwiAPIError(
                "Invalid Amount! Please, enter the amount you want to transfer."
            )

        qiwi_data = {
            "id": self.random_id,
            "comment": comment or "",
            "fields": {"account": number},
            "sum": {"amount": amount, "currency": currency},
            "paymentMethod": {"type": "Account", "accountId": currency},
        }

        self.session.headers["Authorization"] = f"Bearer {self.token}"

        return self.request(
            "POST",
            "https://edge.qiwi.com/sinap/api/v2/terms/99/payments",
            json=qiwi_data,
        )

    @property
    def random_id(self):
        return str(int(time() * 5))

    def check(self, bill_id: int) -> dict:
        """
        Проверяет статус выставленного счета.

        WAITING - Счет выставлен, ожидает оплаты
        PAID - Счет оплачен
        EJECTED - Счет отклонен
        EXPIRED - Время жизни счета истекло. Счет не оплачен
        """

        self.session.headers["Authorization"] = f"Bearer {self.auth_key}"
        return self.request(
            "GET", f"https://api.qiwi.com/partner/bill/v1/bills/" + bill_id
        )

    def cancel_payment(self, bill_id: int) -> dict:
        """
        Отменяет счёт.

        bill_id - номер счёта.
        """

        self.session.headers["Authorization"] = f"Bearer {self.auth_key}"
        return self.request(
            "POST",
            f"https://edge.qiwi.com/checkout-api/api/bill/reject",
            json={"id": bill_id},
        )

    async def request(self, method: str, url: str, **params) -> dict:
        request = await self.session.request(method, url, **params)
        json = await request.json()

        if "code" in json or "errorCode" in json:
            raise QiwiAPIError(json)

        return json
