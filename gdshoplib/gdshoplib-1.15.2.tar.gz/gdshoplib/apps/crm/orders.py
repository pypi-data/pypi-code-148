from gdshoplib.apps.crm.on_request import OnRequestTable
from gdshoplib.core.settings import CRMSettings
from gdshoplib.services.notion.database import Database
from gdshoplib.services.notion.page import Page


class Order(Page):
    SETTINGS = CRMSettings()

    def __init__(self, *args, **kwargs):
        self._on_request = None

        super(Order, self).__init__(*args, **kwargs)

    @classmethod
    def get(cls, sku):
        page = [
            page
            for page in Database(cls.SETTINGS.CRM_DB).pages(
                params={
                    "filter": {
                        "property": "ID заказа",
                        "rich_text": {
                            "equals": sku,
                        },
                    }
                }
            )
        ]
        if not page:
            return
        if len(page) > 1:
            raise OrderIDDuplicate

        page = page[0]

        return cls(page["id"], notion=page.notion, parent=page.parent)

    @classmethod
    def query(cls, filter=None, params=None, notion=None):
        for page in Database(cls.SETTINGS.CRM_DB, notion=notion).pages(
            filter=filter, params=params
        ):
            yield cls(page["id"], notion=page.notion, parent=page.parent)

    @property
    def on_request(self):
        if not self._on_request:
            self._on_request = OnRequestTable(
                [block for block in self.blocks(filter={"type": "table_row"})],
                notion=self.notion,
                parent=self,
            )

        return self._on_request


class OrderIDDuplicate(Exception):
    ...
