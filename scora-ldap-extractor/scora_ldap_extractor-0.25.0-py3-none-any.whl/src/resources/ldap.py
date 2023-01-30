import traceback
import json
import ldap3
from ldap3 import Server, Connection, ALL, SUBTREE

from .service import Service
from ..utils.misc import setup_logger

logger = setup_logger(__name__)


class Ldap:
    def __init__(
        self, domain: str, user_name: str, password: str, group: str, service: Service
    ) -> None:
        self.domain: str = domain
        self.user_name: str = user_name
        self.password: str = password
        self.is_authenticated: bool = False
        self.group: str = group
        self.is_admin: bool = False
        self.tenant: str = None
        self.connection: Connection = None
        self.groups: list[str] = []
        self.users: list[str] = []
        self.service: Service = service

    def set_groups_from_ad(self) -> None:
        if not self.is_authenticated:
            logger.warning("[LDAP] set_groups_from_ad: User is not authenticated")
            return

        groups = []
        try:
            self.connection.search(
                search_base=self.service.get("ldap_root_dn", ""),
                search_filter="(objectclass=*)",
                search_scope=SUBTREE,
                attributes=["member"],
                size_limit=0,
            )

            response = json.loads(self.connection.response_to_json())

            if (
                type(response.get("entries")) == list
                and len(response.get("entries")) > 0
            ):
                for entry in response.get("entries"):
                    for member in entry.member.values:
                        self.connection.search(
                            search_base=self.service.get("ldap_root_dn", ""),
                            search_filter=f"(distinguishedName={member})",
                            attributes=["sAMAccountName"],
                        )

                        user = self.connection.entries[0].sAMAccountName.values

                        self.users.append(user)

                cn_groups = response.get("entries")[0].get("attributes").get("member")

                for cn_group in cn_groups:
                    groups.append(cn_group.split(",")[0].replace("CN=", ""))

                self.groups = groups
        except:
            logger.error(
                f"[LDAP] Error on set_groups_from_ad: {self.connection.last_error}"
            )
            traceback.print_exc()

    def auth(self):
        try:
            self.user_name = self.user_name.strip()
            self.password = self.password.strip()
            server_alias = self.service.get("ldap_server_alias", [])
            self.tenant = self.service.get("service")

            server = Server(
                self.service.get("ldap_server"),
                get_info=ALL,
                port=int(self.service.get("ldap_port", 389)),
                allowed_referral_hosts=[(sa, True) for sa in server_alias]
                if server_alias and len(server_alias)
                else None,
            )

            self.connection = Connection(
                server,
                user=self.user_name,
                password=self.password,
                raise_exceptions=False,
            )
            if self.connection.bind():
                self.is_authenticated = True
                logger.info("[LDAP] Successful bind to ldap server")
            else:
                logger.error(
                    f"[LDAP] Cannot bind to ldap server: {self.connection.last_error}"
                )

            logger.debug(self.connection.result)

            self.set_groups_from_ad()

            if self.group in self.service.get("ldap_admin_groups", []):
                self.is_admin = True

        except (
            ldap3.core.exceptions.LDAPSocketOpenError,
            ldap3.core.exceptions.LDAPSocketReceiveError,
        ) as err:
            logger.error(err)
        except:
            traceback.print_exc()

        return self
