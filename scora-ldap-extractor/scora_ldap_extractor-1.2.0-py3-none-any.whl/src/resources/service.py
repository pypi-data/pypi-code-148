import traceback

from ..database.dynamodb import get_data_by_key
from ..utils.misc import get_env


class Service:
    def __init__(self) -> None:
        self.service: str = ""
        self.ldap_admin_groups: list[str] = []
        self.ldap_domain: str = ""
        self.ldap_groups: list[str] = []
        self.ldap_root_dn: str = ""
        self.ldap_root_dn_dev: str = ""
        self.ldap_server: str = ""
        self.ldap_server_alias: list[str] = []

    def get_props(self, value: any, field=None):
        response_config: Service = None
        dynamo_table = get_env("DYNAMO_TABLE_NAME")

        try:
            response_config = get_data_by_key(dynamo_table, "service", value, field)
        except:
            traceback.print_exc()

        return response_config
