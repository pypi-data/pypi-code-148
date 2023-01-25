from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxSetComment

async def mailbox_set_comment(api_token: str, id: int, comment: str) -> MailboxSetComment:
    query = {
        "token": api_token,
        "id": id,
        "comment": comment,
        "type": "json",
        "api": 2.0
    }
    return await request_get(url='http://api.kopeechka.store/mailbox-set-comment', params=query, type_kopeechka=MailboxSetComment)