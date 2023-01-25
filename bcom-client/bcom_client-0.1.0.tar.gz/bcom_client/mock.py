from http import HTTPStatus

import respx
from httpx import Response

INVENTORY_BASE_URL = "http://example.com/"
inventory_mock = respx.mock(base_url=INVENTORY_BASE_URL, assert_all_called=False)
inventory_mock.get(
    path__regex=r"/private/api/v1/inventory/(?P<warehouse_code>\w+)/$",
    name="inventory_stock",
).mock(
    return_value=Response(
        HTTPStatus.OK, json={"count": 0, "next": None, "prev": None, "results": []}
    )
)
for name, action in (
    ("inventory_adjust_create", "adjust"),
    ("inventory_allocate_create", "allocate"),
    ("inventory_deallocate_create", "deallocate"),
    ("inventory_receive_create", "receive"),
    ("inventory_release_create", "release"),
):
    inventory_mock.post(
        path__regex=rf"/private/api/v1/inventory/(?P<warehouse_code>\w+)/{action}/$",
        name=name,
    ).mock(return_value=Response(HTTPStatus.NO_CONTENT))
