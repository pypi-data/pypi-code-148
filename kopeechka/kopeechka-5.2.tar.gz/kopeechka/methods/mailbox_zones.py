import requests
from kopeechka.types_kopeechka import MailboxZones

def mailbox_zones(popular: int, zones: int) -> MailboxZones:
    query = {
        "popular": popular,
        "zones": zones
    }
    response = requests.get("https://api.kopeechka.store/mailbox-zones", params=query)
    return MailboxZones(response.json())
