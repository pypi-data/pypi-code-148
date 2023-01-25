import requests
from kopeechka.types_kopeechka import UserBalance

def user_balance(api_token: str) -> UserBalance:
    query = {
        "token": api_token,
        "type": "json",
        "api": 2.0
    }
    response = requests.get(url="https://api.kopeechka.store/user-balance", params=query)
    return UserBalance(response.json())