import requests

TELEGRAM_TEXT_LIMIT = 4095


class AlertSender:
    def __init__(self, token: str, chat_id: str):
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"

    def send_message(self, text: str) -> bool:
        "Sends message to channel"
        params = {
            'chat_id': self.chat_id,
            'text': text[:TELEGRAM_TEXT_LIMIT]
        }
        response = requests.get(url=self.url, params=params)
        return response.json().get('ok', False)
