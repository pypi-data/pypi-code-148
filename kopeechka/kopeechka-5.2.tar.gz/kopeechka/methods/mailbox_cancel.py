import requests
from kopeechka.types_kopeechka import MailboxCancel

def mailbox_cancel(api_token: str, id: int) -> MailboxCancel:
    query = {
        "id": id,
        "token": api_token,
        "type": "json",
        "api": 2.0
    }
    response = requests.get(url="http://api.kopeechka.store/mailbox-cancel", params=query)
    return MailboxCancel(response.json())