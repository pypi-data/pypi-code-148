import requests
from kopeechka.types_kopeechka import MailboxSetComment

def mailbox_set_comment(api_token: str, id: int, comment: str) -> MailboxSetComment:
    query = {
        "token": api_token,
        "id": id,
        "comment": comment,
        "type": "json",
        "api": 2.0
    }
    response = requests.get('http://api.kopeechka.store/mailbox-set-comment', params=query)
    return MailboxSetComment(response.json())