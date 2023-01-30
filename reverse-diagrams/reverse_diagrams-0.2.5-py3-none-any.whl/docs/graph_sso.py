
from diagrams import Diagram, Cluster

from diagrams.aws.management import Organizations, OrganizationsAccount, OrganizationsOrganizationalUnit
from diagrams.aws.general import Users, User

with Diagram("SSO-State", show=False, direction="TB"):
    gg = Users("Group")
    uu= User("User")

    with Cluster('Groups'):

        with Cluster("AWSAccountFactory"):

                gg_0= [User("velez94@protonma\nil.com"),]

        gg_1= Users("AWSAuditAccountA\ndmins")

        gg_2= Users("AWSLogArchiveAdm\nins")

        with Cluster("AWSControlTowerAdmins"):

                gg_3= [User("velez94@protonma\nil.com"),]

        gg_4= Users("AWSLogArchiveVie\nwers")

        gg_5= Users("AWSSecurityAudit\nors")

        gg_6= Users("AWSSecurityAudit\nPowerUsers")

        with Cluster("DevSecOps_Admins"):

                gg_7= [User("DevSecOpsAdm"),]

        gg_8= Users("AWSServiceCatalo\ngAdmins")

        with Cluster("SecOps_Adms"):

                gg_9= [User("w.alejovl+secops\n-labs@gmail.com"),]
