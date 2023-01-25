from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxGetMessage

async def mailbox_get_message(api_token: str, full: int, id: int) -> MailboxGetMessage:
    query = {
        "full": full,
        "id": id,
        "token": api_token,
        "type": "json",
        "api": 2.0
    }
    return await request_get(url="http://api.kopeechka.store/mailbox-get-message", params=query, type_kopeechka=MailboxGetMessage)