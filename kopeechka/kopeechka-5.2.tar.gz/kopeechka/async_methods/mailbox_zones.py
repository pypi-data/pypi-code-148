from kopeechka.utils import request_get
from kopeechka.types_kopeechka import MailboxZones

async def mailbox_zones(popular: int, zones: int) -> MailboxZones:
    query = {
        "popular": popular,
        "zones": zones
    }
    return await request_get(url="https://api.kopeechka.store/mailbox-zones", params=query, type_kopeechka=MailboxZones)
