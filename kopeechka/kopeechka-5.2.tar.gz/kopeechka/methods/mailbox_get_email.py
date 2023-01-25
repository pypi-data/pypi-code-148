import requests
from kopeechka.types_kopeechka import MailboxGetEmail

def mailbox_get_email(api_token: str, site: str, mail_type: str, sender: str, regex: str, soft_id: int, investor: int, subject: str, clear: int) -> MailboxGetEmail:
    query = {
        "site": site,
        "mail_type": mail_type,
        "token": api_token,
        "sender": sender,
        "regex": regex,
        "soft_id": soft_id,
        "investor": investor,
        "subject": subject,
        "clear": clear,
        "type": "json",
        "api": 2.0
    }
    response = requests.get(url="http://api.kopeechka.store/mailbox-get-email", params=query)
    return MailboxGetEmail(response.json())