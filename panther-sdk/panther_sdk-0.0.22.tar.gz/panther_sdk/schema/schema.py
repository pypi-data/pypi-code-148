# Copyright (C) 2022 Panther Labs, Inc.
#
# The Panther SaaS is licensed under the terms of the Panther Enterprise Subscription
# Agreement available at https://panther.com/enterprise-subscription-agreement/.
# All intellectual property rights in and to the Panther SaaS, including any and all
# rights to access the Panther SaaS, are governed by the Panther Enterprise Subscription Agreement.

# coding=utf-8
# *** WARNING: generated file
import typing
import functools
import dataclasses

from panther_core import PantherEvent

"""
The schema module provides classes for configuring custom Panther schemas.
"""

from .. import _utilities

__all__ = [
    "DataModelMapping",
    "DataModel",
    "DataModelOverrides",
    "LogTypeApacheAccessCommon",
    "LogTypeApacheAccessCombined",
    "LogTypeAsanaAudit",
    "LogTypeAtlassianAudit",
    "LogTypeAWSALB",
    "LogTypeAWSAuroraMySQLAudit",
    "LogTypeAWSCloudTrail",
    "LogTypeAWSCloudTrailDigest",
    "LogTypeAWSCloudTrailInsight",
    "LogTypeAWSCloudWatchEvents",
    "LogTypeAWSConfig",
    "LogTypeAmazonEKSAudit",
    "LogTypeAmazonEKSAuthenticator",
    "LogTypeAWSGuardDuty",
    "LogTypeAWSS3ServerAccess",
    "LogTypeAWSTransitGatewayFlow",
    "LogTypeAWSVPCDns",
    "LogTypeAWSVPCFlow",
    "LogTypeAWSWAFWebACL",
    "LogTypeBitwardenEvents",
    "LogTypeBoxEvent",
    "LogTypeCiscoUmbrellaDNS",
    "LogTypeCiscoUmbrellaCloudFirewall",
    "LogTypeCiscoUmbrellaIP",
    "LogTypeCiscoUmbrellaProxy",
    "LogTypeCloudflareAudit",
    "LogTypeCloudflareHttpRequest",
    "LogTypeCloudflareSpectrum",
    "LogTypeCloudflareFirewall",
    "LogTypeCrowdstrikeFDREvent",
    "LogTypeDropboxTeamEvent",
    "LogTypeDuoAuthentication",
    "LogTypeDuoAdministrator",
    "LogTypeDuoTelephony",
    "LogTypeDuoOfflineEnrollment",
    "LogTypeFastlyAccess",
    "LogTypeFluentdSyslog3164",
    "LogTypeFluentdSyslog5424",
    "LogTypeGSuiteReports",
    "LogTypeGSuiteActivityEvent",
    "LogTypeGCPAuditLog",
    "LogTypeGCPHTTPLoadBalancer",
    "LogTypeGitHubAudit",
    "LogTypeGitHubAudit",
    "LogTypeGitLabAPI",
    "LogTypeGitLabAudit",
    "LogTypeGitLabExceptions",
    "LogTypeGitLabIntegrations",
    "LogTypeGitLabGit",
    "LogTypeGitLabProduction",
    "LogTypeJamfproLogin",
    "LogTypeJuniperAccess",
    "LogTypeJuniperAudit",
    "LogTypeJuniperFirewall",
    "LogTypeJuniperMWS",
    "LogTypeJuniperPostgres",
    "LogTypeJuniperSecurity",
    "LogTypeLaceworkEvents",
    "LogTypeLaceworkAlertDetails",
    "LogTypeLaceworkApplications",
    "LogTypeLaceworkCloudCompliance",
    "LogTypeLaceworkCloudConfiguration",
    "LogTypeLaceworkAgentManagement",
    "LogTypeLaceworkAllFiles",
    "LogTypeLaceworkChangeFiles",
    "LogTypeLaceworkCmdline",
    "LogTypeLaceworkConnections",
    "LogTypeLaceworkContainerSummary",
    "LogTypeLaceworkContainerVulnDetails",
    "LogTypeLaceworkDNSQuery",
    "LogTypeLaceworkHostVulnDetails",
    "LogTypeLaceworkImage",
    "LogTypeLaceworkInterfaces",
    "LogTypeLaceworkInternalIPA",
    "LogTypeLaceworkMachineDetails",
    "LogTypeLaceworkMachineSummary",
    "LogTypeLaceworkPackage",
    "LogTypeLaceworkPodSummary",
    "LogTypeLaceworkProcessSummary",
    "LogTypeLaceworkUserDetails",
    "LogTypeLaceworkUserLogin",
    "LogTypeMicrosoft365AuditExchange",
    "LogTypeMicrosoft365AuditSharePoint",
    "LogTypeMicrosoft365AuditGeneral",
    "LogTypeMicrosoft365DLPAll",
    "LogTypeMicrosoft365AuditAzureActiveDirectory",
    "LogTypeMicrosoftGraphSecurityAlert",
    "LogTypeMongoDBOrganizationEvent",
    "LogTypeMongoDBProjectEvent",
    "LogTypeNginxAccess",
    "LogTypeOktaSystemLog",
    "LogTypeOneLoginEvents",
    "LogTypeOnePasswordItemUsage",
    "LogTypeOnePasswordSignInAttempt",
    "LogTypeOsqueryBatch",
    "LogTypeOsqueryDifferential",
    "LogTypeOsquerySnapshot",
    "LogTypeOsqueryStatus",
    "LogTypeOSSECEventInfo",
    "LogTypeSalesforceLogin",
    "LogTypeSalesforceLoginAs",
    "LogTypeSalesforceLogout",
    "LogTypeSalesforceURI",
    "LogTypeSentinelOneActivity",
    "LogTypeSentinelOneDeepVisibility",
    "LogTypeSentinelOneDeepVisibilityV2",
    "LogTypeSlackAuditLogs",
    "LogTypeSlackAccessLogs",
    "LogTypeSlackIntegrationLogs",
    "LogTypeSnykGroupAudit",
    "LogTypeSnykOrgAudit",
    "LogTypeSophosCentral",
    "LogTypeSuricataDNS",
    "LogTypeSuricataAnomaly",
    "LogTypeSysdigAudit",
    "LogTypeSyslogRFC5424",
    "LogTypeSyslogRFC3164",
    "LogTypeGravitationalTeleportAudit",
    "LogTypeWorkdayActivity",
    "LogTypeWorkdaySignOnAttempt",
    "LogTypeZeekDNS",
    "LogTypeZeekCaptureLoss",
    "LogTypeZeekConn",
    "LogTypeZeekDHCP",
    "LogTypeZeekDPD",
    "LogTypeZeekFiles",
    "LogTypeZeekHTTP",
    "LogTypeZeekNotice",
    "LogTypeZeekNTP",
    "LogTypeZeekOCSP",
    "LogTypeZeekReporter",
    "LogTypeZeekSsh",
    "LogTypeZeekSoftware",
    "LogTypeZeekStats",
    "LogTypeZeekSsl",
    "LogTypeZeekX509",
    "LogTypeZeekTunnel",
    "LogTypeZeekWeird",
    "LogTypeZendeskAudit",
    "LogTypeZoomActivity",
    "LogTypeZoomOperation",
]


LogTypeApacheAccessCommon = "Apache.AccessCommon"
LogTypeApacheAccessCombined = "Apache.AccessCombined"
LogTypeAsanaAudit = "Asana.Audit"
LogTypeAtlassianAudit = "Atlassian.Audit"
LogTypeAWSALB = "AWS.ALB"
LogTypeAWSAuroraMySQLAudit = "AWS.AuroraMySQLAudit"
LogTypeAWSCloudTrail = "AWS.CloudTrail"
LogTypeAWSCloudTrailDigest = "AWS.CloudTrailDigest"
LogTypeAWSCloudTrailInsight = "AWS.CloudTrailInsight"
LogTypeAWSCloudWatchEvents = "AWS.CloudWatchEvents"
LogTypeAWSConfig = "AWS.Config"
LogTypeAmazonEKSAudit = "Amazon.EKS.Audit"
LogTypeAmazonEKSAuthenticator = "Amazon.EKS.Authenticator"
LogTypeAWSGuardDuty = "AWS.GuardDuty"
LogTypeAWSS3ServerAccess = "AWS.S3ServerAccess"
LogTypeAWSTransitGatewayFlow = "AWS.TransitGatewayFlow"
LogTypeAWSVPCDns = "AWS.VPCDns"
LogTypeAWSVPCFlow = "AWS.VPCFlow"
LogTypeAWSWAFWebACL = "AWS.WAFWebACL"
LogTypeBitwardenEvents = "Bitwarden.Events"
LogTypeBoxEvent = "Box.Event"
LogTypeCiscoUmbrellaDNS = "CiscoUmbrella.DNS"
LogTypeCiscoUmbrellaCloudFirewall = "CiscoUmbrella.CloudFirewall"
LogTypeCiscoUmbrellaIP = "CiscoUmbrella.IP"
LogTypeCiscoUmbrellaProxy = "CiscoUmbrella.Proxy"
LogTypeCloudflareAudit = "Cloudflare.Audit"
LogTypeCloudflareHttpRequest = "Cloudflare.HttpRequest"
LogTypeCloudflareSpectrum = "Cloudflare.Spectrum"
LogTypeCloudflareFirewall = "Cloudflare.Firewall"
LogTypeCrowdstrikeFDREvent = "Crowdstrike.FDREvent"
LogTypeDropboxTeamEvent = "Dropbox.TeamEvent"
LogTypeDuoAuthentication = "Duo.Authentication"
LogTypeDuoAdministrator = "Duo.Administrator"
LogTypeDuoTelephony = "Duo.Telephony"
LogTypeDuoOfflineEnrollment = "Duo.OfflineEnrollment"
LogTypeFastlyAccess = "Fastly.Access"
LogTypeFluentdSyslog3164 = "Fluentd.Syslog3164"
LogTypeFluentdSyslog5424 = "Fluentd.Syslog5424"
LogTypeGSuiteReports = "GSuite.Reports"
LogTypeGSuiteActivityEvent = "GSuite.ActivityEvent"
LogTypeGCPAuditLog = "GCP.AuditLog"
LogTypeGCPHTTPLoadBalancer = "GCP.HTTPLoadBalancer"
LogTypeGitHubAudit = "GitHub.Audit"
LogTypeGitHubAudit = "GitHub.Audit"
LogTypeGitLabAPI = "GitLab.API"
LogTypeGitLabAudit = "GitLab.Audit"
LogTypeGitLabExceptions = "GitLab.Exceptions"
LogTypeGitLabIntegrations = "GitLab.Integrations"
LogTypeGitLabGit = "GitLab.Git"
LogTypeGitLabProduction = "GitLab.Production"
LogTypeJamfproLogin = "Jamfpro.Login"
LogTypeJuniperAccess = "Juniper.Access"
LogTypeJuniperAudit = "Juniper.Audit"
LogTypeJuniperFirewall = "Juniper.Firewall"
LogTypeJuniperMWS = "Juniper.MWS"
LogTypeJuniperPostgres = "Juniper.Postgres"
LogTypeJuniperSecurity = "Juniper.Security"
LogTypeLaceworkEvents = "Lacework.Events"
LogTypeLaceworkAlertDetails = "Lacework.AlertDetails"
LogTypeLaceworkApplications = "Lacework.Applications"
LogTypeLaceworkCloudCompliance = "Lacework.CloudCompliance"
LogTypeLaceworkCloudConfiguration = "Lacework.CloudConfiguration"
LogTypeLaceworkAgentManagement = "Lacework.AgentManagement"
LogTypeLaceworkAllFiles = "Lacework.AllFiles"
LogTypeLaceworkChangeFiles = "Lacework.ChangeFiles"
LogTypeLaceworkCmdline = "Lacework.Cmdline"
LogTypeLaceworkConnections = "Lacework.Connections"
LogTypeLaceworkContainerSummary = "Lacework.ContainerSummary"
LogTypeLaceworkContainerVulnDetails = "Lacework.ContainerVulnDetails"
LogTypeLaceworkDNSQuery = "Lacework.DNSQuery"
LogTypeLaceworkHostVulnDetails = "Lacework.HostVulnDetails"
LogTypeLaceworkImage = "Lacework.Image"
LogTypeLaceworkInterfaces = "Lacework.Interfaces"
LogTypeLaceworkInternalIPA = "Lacework.InternalIPA"
LogTypeLaceworkMachineDetails = "Lacework.MachineDetails"
LogTypeLaceworkMachineSummary = "Lacework.MachineSummary"
LogTypeLaceworkPackage = "Lacework.Package"
LogTypeLaceworkPodSummary = "Lacework.PodSummary"
LogTypeLaceworkProcessSummary = "Lacework.ProcessSummary"
LogTypeLaceworkUserDetails = "Lacework.UserDetails"
LogTypeLaceworkUserLogin = "Lacework.UserLogin"
LogTypeMicrosoft365AuditExchange = "Microsoft365.Audit.Exchange"
LogTypeMicrosoft365AuditSharePoint = "Microsoft365.Audit.SharePoint"
LogTypeMicrosoft365AuditGeneral = "Microsoft365.Audit.General"
LogTypeMicrosoft365DLPAll = "Microsoft365.DLP.All"
LogTypeMicrosoft365AuditAzureActiveDirectory = "Microsoft365.Audit.AzureActiveDirectory"
LogTypeMicrosoftGraphSecurityAlert = "MicrosoftGraph.SecurityAlert"
LogTypeMongoDBOrganizationEvent = "MongoDB.OrganizationEvent"
LogTypeMongoDBProjectEvent = "MongoDB.ProjectEvent"
LogTypeNginxAccess = "Nginx.Access"
LogTypeOktaSystemLog = "Okta.SystemLog"
LogTypeOneLoginEvents = "OneLogin.Events"
LogTypeOnePasswordItemUsage = "OnePassword.ItemUsage"
LogTypeOnePasswordSignInAttempt = "OnePassword.SignInAttempt"
LogTypeOsqueryBatch = "Osquery.Batch"
LogTypeOsqueryDifferential = "Osquery.Differential"
LogTypeOsquerySnapshot = "Osquery.Snapshot"
LogTypeOsqueryStatus = "Osquery.Status"
LogTypeOSSECEventInfo = "OSSEC.EventInfo"
LogTypeSalesforceLogin = "Salesforce.Login"
LogTypeSalesforceLoginAs = "Salesforce.LoginAs"
LogTypeSalesforceLogout = "Salesforce.Logout"
LogTypeSalesforceURI = "Salesforce.URI"
LogTypeSentinelOneActivity = "SentinelOne.Activity"
LogTypeSentinelOneDeepVisibility = "SentinelOne.DeepVisibility"
LogTypeSentinelOneDeepVisibilityV2 = "SentinelOne.DeepVisibilityV2"
LogTypeSlackAuditLogs = "Slack.AuditLogs"
LogTypeSlackAccessLogs = "Slack.AccessLogs"
LogTypeSlackIntegrationLogs = "Slack.IntegrationLogs"
LogTypeSnykGroupAudit = "Snyk.GroupAudit"
LogTypeSnykOrgAudit = "Snyk.OrgAudit"
LogTypeSophosCentral = "Sophos.Central"
LogTypeSuricataDNS = "Suricata.DNS"
LogTypeSuricataAnomaly = "Suricata.Anomaly"
LogTypeSysdigAudit = "Sysdig.Audit"
LogTypeSyslogRFC5424 = "Syslog.RFC5424"
LogTypeSyslogRFC3164 = "Syslog.RFC3164"
LogTypeGravitationalTeleportAudit = "Gravitational.TeleportAudit"
LogTypeWorkdayActivity = "Workday.Activity"
LogTypeWorkdaySignOnAttempt = "Workday.SignOnAttempt"
LogTypeZeekDNS = "Zeek.DNS"
LogTypeZeekCaptureLoss = "Zeek.CaptureLoss"
LogTypeZeekConn = "Zeek.Conn"
LogTypeZeekDHCP = "Zeek.DHCP"
LogTypeZeekDPD = "Zeek.DPD"
LogTypeZeekFiles = "Zeek.Files"
LogTypeZeekHTTP = "Zeek.HTTP"
LogTypeZeekNotice = "Zeek.Notice"
LogTypeZeekNTP = "Zeek.NTP"
LogTypeZeekOCSP = "Zeek.OCSP"
LogTypeZeekReporter = "Zeek.Reporter"
LogTypeZeekSsh = "Zeek.Ssh"
LogTypeZeekSoftware = "Zeek.Software"
LogTypeZeekStats = "Zeek.Stats"
LogTypeZeekSsl = "Zeek.Ssl"
LogTypeZeekX509 = "Zeek.X509"
LogTypeZeekTunnel = "Zeek.Tunnel"
LogTypeZeekWeird = "Zeek.Weird"
LogTypeZendeskAudit = "Zendesk.Audit"
LogTypeZoomActivity = "Zoom.Activity"
LogTypeZoomOperation = "Zoom.Operation"


class DefaultOverrides:
    pass


def overridable(cls: typing.Callable) -> typing.Callable:
    @functools.wraps(cls)
    def wrapper(
        *args: typing.Any,
        overrides: typing.Optional[
            typing.Union["DataModelOverrides", DefaultOverrides]
        ] = DefaultOverrides(),
        **kwargs: typing.Any,
    ) -> typing.Any:
        if overrides:  # overrides can be None
            for key, val in overrides.__dict__.items():
                kwargs[key] = val or kwargs.get(key)
        return cls(*args, **kwargs)

    return wrapper


@dataclasses.dataclass(frozen=True)
class DataModelMapping(_utilities.SDKNode):
    """

    - name -- Name of the data model field. This will be the name used when accessing the field from within detections. (required)
    - func -- A Python function to access the target value. The input is the Panther Event and output is the target value in the Panther Event. (optional, default: None)
    - path -- Path to the target value in the Panther Event. This can be a simple field name or complete JSON path starting with a `$`. JSON path syntax must be compatible with the [jsonpath-ng](https://pypi.org/project/jsonpath-ng/) Python package. (optional, default: None)
    """

    # required
    name: str

    # optional
    func: typing.Optional[typing.Callable[[PantherEvent], typing.Any]] = None

    # optional
    path: typing.Optional[str] = None

    # internal private methods
    def _typename(self) -> str:
        return "DataModelMapping"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["name", "func", "path"]


@dataclasses.dataclass
class DataModelOverrides:
    """Overrides dataclass for DataModel. All arguments are marked optional.

    - data_model_id -- The unique identifier of the data model.
    - log_type -- What log type this data model will apply to.
    - mappings -- Mapping from source field name or method to unified data model field name.
    - enabled -- Whether this data model is enabled.
    - name -- What name to display in the UI and alerts. The `data_model_id` will be displayed if this field is not set.
    """

    data_model_id: typing.Optional[str] = None

    log_type: typing.Optional[str] = None

    mappings: typing.Optional[
        typing.Union[DataModelMapping, typing.List[DataModelMapping]]
    ] = None

    enabled: typing.Optional[bool] = None

    name: typing.Optional[str] = None


@overridable
@dataclasses.dataclass(frozen=True)
class DataModel(_utilities.SDKNode):
    """Data Models provide a way to configure a set of unified fields across all log types. (https://docs.panther.com/writing-detections/data-models)

    - data_model_id -- The unique identifier of the data model. (required)
    - log_type -- What log type this data model will apply to. (required)
    - mappings -- Mapping from source field name or method to unified data model field name. (required)
    - enabled -- Whether this data model is enabled. (optional, default: True)
    - name -- What name to display in the UI and alerts. The `data_model_id` will be displayed if this field is not set. (optional, default: "")
    """

    # required
    data_model_id: str

    # required
    log_type: str

    # required
    mappings: typing.Union[DataModelMapping, typing.List[DataModelMapping]]

    # optional
    enabled: typing.Optional[bool] = True

    # optional
    name: typing.Optional[str] = ""

    # overrides field is used to allow mypy type checking but is not used in DataModel functionality
    overrides: typing.Optional[DataModelOverrides] = dataclasses.field(
        default=DataModelOverrides(), repr=False
    )

    # internal private methods
    def _typename(self) -> str:
        return "DataModel"

    def _output_key(self) -> str:
        return "sdk-node:data-model"

    def _fields(self) -> typing.List[str]:
        return ["data_model_id", "log_type", "mappings", "enabled", "name"]
