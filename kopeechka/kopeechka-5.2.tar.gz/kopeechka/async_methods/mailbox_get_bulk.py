from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxGetBulk

async def mailbox_get_bulk(api_token: str, count: int, comment: str, email: str, site: str) -> MailboxGetBulk:
    query = {
        "token": api_token,
        "count": count,
        "comment": comment,
        "email": email,
        "site": site,
        "type": "json",
        "api": 2.0
    }
    return await request_get("http://api.kopeechka.store/mailbox-get-bulk", params=query, type_kopeechka=MailboxGetBulk)