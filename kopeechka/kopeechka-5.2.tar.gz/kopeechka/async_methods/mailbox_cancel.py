from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxCancel

async def mailbox_cancel(api_token: str, id: int) -> MailboxCancel:
    query = {
        "id": id,
        "token": api_token,
        "type": "json",
        "api": 2.0
    }
    return await request_get(url="http://api.kopeechka.store/mailbox-cancel", params=query, type_kopeechka=MailboxCancel)