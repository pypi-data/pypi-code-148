import requests
from kopeechka.types_kopeechka import MailboxGetDomains

def mailbox_get_domains(api_token: str, site: str) -> MailboxGetDomains:
    query = {
        "token": api_token,
        "site": site,
        "type": "json",
        "api": 2.0
    }
    response = requests.get("http://api.kopeechka.store/mailbox-get-domains", params=query)
    return MailboxGetDomains(response.json())