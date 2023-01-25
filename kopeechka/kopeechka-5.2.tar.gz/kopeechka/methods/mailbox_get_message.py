import requests
from kopeechka.types_kopeechka import MailboxGetMessage

def mailbox_get_message(api_token: str, full: int, id: int) -> MailboxGetMessage:
    query = {
        "full": full,
        "id": id,
        "token": api_token,
        "type": "json",
        "api": 2.0
    }

    response = requests.get(url="http://api.kopeechka.store/mailbox-get-message", params=query)
    return MailboxGetMessage(response.json())