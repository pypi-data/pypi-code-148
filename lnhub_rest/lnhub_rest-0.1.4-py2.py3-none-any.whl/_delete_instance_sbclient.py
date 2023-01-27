from typing import Union

from lnhub_rest._sbclient import connect_hub_with_auth


def delete_instance(
    *,
    owner: str,  # owner handle
    name: str,  # instance name
) -> Union[None, str]:
    try:
        hub = connect_hub_with_auth()

        # get account
        data = hub.table("account").select("*").eq("handle", owner).execute().data
        account = data[0]

        data = (
            hub.table("instance")
            .delete()
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
            .data
        )
        if len(data) == 0:
            return "instance-does-not-exist-on-hub"

        # TODO: delete storage if no other instances use it
        return None
    finally:
        hub.auth.sign_out()
