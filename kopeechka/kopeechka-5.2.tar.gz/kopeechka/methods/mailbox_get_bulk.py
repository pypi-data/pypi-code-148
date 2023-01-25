import requests
from kopeechka.types_kopeechka import MailboxGetBulk

def mailbox_get_bulk(api_token: str, count: int, comment: str, email: str, site: str) -> MailboxGetBulk:
    query = {
        "token": api_token,
        "count": count,
        "comment": comment,
        "email": email,
        "site": site,
        "type": "json",
        "api": 2.0
    }
    response = requests.get("http://api.kopeechka.store/mailbox-get-bulk", params=query)
    return MailboxGetBulk(response.json())