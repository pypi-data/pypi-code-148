from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxReorder

async def mailbox_reorder(api_token: str, site: str, email: str, regex: str, subject: str) -> MailboxReorder:
    query = {
        "site": site,
        "email": email,
        "regex": regex,
        "token": api_token,
        "type": "json",
        "subject": subject,
        "api": 2.0
    }
    return await request_get(url="http://api.kopeechka.store/mailbox-reorder", params=query, type_kopeechka=MailboxReorder)
