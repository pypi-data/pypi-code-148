
from diagrams import Diagram, Cluster

from diagrams.aws.management import Organizations, OrganizationsAccount, OrganizationsOrganizationalUnit

with Diagram("Organizations-State", show=False, direction="TB"):
    ou = OrganizationsOrganizationalUnit("OU")
    oa = OrganizationsAccount("Account")
