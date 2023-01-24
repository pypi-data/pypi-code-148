from __future__ import annotations


class DatadogAlert:
    def __init__(self, content: dict, fields: list | None = None):
        if not fields:
            self._fields = [
                "title",
                "event_type",
                "body",
                "date",
                "org.id",
                "org.name",
                "id",
                "last_updated",
            ]
        self.alert_message = self._format_content(content)

    def _format_content(self, content: dict) -> str:
        message = ""
        for field in self._fields:
            message = f"{message}\n<b>{field.title()}</b>:{deref_multi(content, field)}"
        return message


def deref_multi(data: dict, ref: str):
    keys = ref.split(".") if ref else []
    return deref_multi(data[keys[0]], ".".join(keys[1:])) if keys else data
