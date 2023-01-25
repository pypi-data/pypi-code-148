from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxGetFreshId

async def mailbox_get_fresh_id(api_token: str, site: str, email: str) -> MailboxGetFreshId:
    query = {
        "token": api_token,
        "site": site,
        "email": email,
        "type": "json",
        "api": 2.0
    }
    return await request_get(url="http://api.kopeechka.store/mailbox-get-fresh-id", params=query, type_kopeechka=MailboxGetFreshId)