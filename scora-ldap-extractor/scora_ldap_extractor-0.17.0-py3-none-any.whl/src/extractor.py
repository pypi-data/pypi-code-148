from .utils import misc
from .resources.ldap import Ldap
from .resources.service import Service

logger = misc.setup_logger(__name__)


class LdapService:
    def __init__(
        self, tenant: str, ldap_username: str, ldap_password: str, group: str = ""
    ) -> None:
        self.__ldap_username = ldap_username
        self.__ldap_password = ldap_password
        self.__ldap: Ldap = None
        self.tenant: str = tenant
        self.group: str = group

        response_tenant_services = Service.get_props(self, value=self.tenant)
        if not response_tenant_services:
            logger.error(f"Service for {self.tenant} was not configured")
            return

        ldap = Ldap(
            domain=self.domain,
            user_name=self.__ldap_username,
            password=self.__ldap_password,
            group=self.group,
            service=response_tenant_services,
        )
        self.__ldap = ldap.auth()

    def get_ldap_users(self) -> tuple[list[str], list[str]]:
        return self.__ldap.users, self.__ldap.groups
