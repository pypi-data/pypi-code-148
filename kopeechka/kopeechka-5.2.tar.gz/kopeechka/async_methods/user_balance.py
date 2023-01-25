from kopeechka.utils import request_get
from kopeechka.types_kopeechka import UserBalance

async def user_balance(api_token: str) -> UserBalance:
    query = {
        "token": api_token,
        "type": "json",
        "api": 2.0
    }
    return await request_get(url="https://api.kopeechka.store/user-balance", params=query, type_kopeechka=UserBalance)
