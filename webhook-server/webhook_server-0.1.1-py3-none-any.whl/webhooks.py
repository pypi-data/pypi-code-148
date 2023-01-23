import requests

from flask import Response, request, jsonify
from . import app, basic_auth
from .datadog import DatadogAlert


@app.route("/")
def ping() -> Response:
    return jsonify({"status": "ok"})


@app.route("/telegram/<chat_id>", methods=["POST"])
@basic_auth.required
def webhookHandler(chat_id) -> Response:
    content = request.get_json()
    text = DatadogAlert(content).alert_message

    url = (
        "https://api.telegram.org/bot"
        + app.config.get("TELEGRAM_BOT_API_TOKEN", "")
        + "/sendMessage"
    )
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "html",
    }
    req = requests.post(url=url, data=payload, timeout=5)
    telegram_response = req.json()
    return jsonify(telegram_response)
