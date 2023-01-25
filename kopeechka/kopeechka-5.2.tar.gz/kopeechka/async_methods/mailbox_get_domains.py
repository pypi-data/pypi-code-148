from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxGetDomains

async def mailbox_get_domains(api_token: str, site: str) -> MailboxGetDomains:
    query = {
        "token": api_token,
        "site": site,
        "type": "json",
        "api": 2.0
    }
    return await request_get("http://api.kopeechka.store/mailbox-get-domains", params=query, type_kopeechka=MailboxGetDomains)