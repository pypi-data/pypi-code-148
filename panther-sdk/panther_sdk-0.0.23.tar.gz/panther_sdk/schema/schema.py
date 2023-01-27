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
    "LogTypeAWSALB",
    "LogTypeAWSAuroraMySQLAudit",
    "LogTypeAWSCloudTrail",
    "LogTypeAWSCloudTrailDigest",
    "LogTypeAWSCloudTrailInsight",
    "LogTypeAWSCloudWatchEvents",
    "LogTypeAWSConfig",
    "LogTypeAWSGuardDuty",
    "LogTypeAWSS3ServerAccess",
    "LogTypeAWSTransitGatewayFlow",
    "LogTypeAWSVPCDns",
    "LogTypeAWSVPCFlow",
    "LogTypeAWSWAFWebACL",
    "LogTypeAlphaSOCAlert",
    "LogTypeAmazonEKSAudit",
    "LogTypeAmazonEKSAuthenticator",
    "LogTypeApacheAccessCombined",
    "LogTypeApacheAccessCommon",
    "LogTypeAsanaAudit",
    "LogTypeAtlassianAudit",
    "LogTypeBitwardenEvents",
    "LogTypeBoxEvent",
    "LogTypeCiscoUmbrellaCloudFirewall",
    "LogTypeCiscoUmbrellaDNS",
    "LogTypeCiscoUmbrellaIP",
    "LogTypeCiscoUmbrellaProxy",
    "LogTypeCloudflareAudit",
    "LogTypeCloudflareFirewall",
    "LogTypeCloudflareHttpRequest",
    "LogTypeCloudflareSpectrum",
    "LogTypeCrowdstrikeAIDMaster",
    "LogTypeCrowdstrikeActivityAudit",
    "LogTypeCrowdstrikeAppInfo",
    "LogTypeCrowdstrikeCriticalFile",
    "LogTypeCrowdstrikeDNSRequest",
    "LogTypeCrowdstrikeDetectionSummary",
    "LogTypeCrowdstrikeFDREvent",
    "LogTypeCrowdstrikeGroupIdentity",
    "LogTypeCrowdstrikeManagedAssets",
    "LogTypeCrowdstrikeNetworkConnect",
    "LogTypeCrowdstrikeNetworkListen",
    "LogTypeCrowdstrikeNotManagedAssets",
    "LogTypeCrowdstrikeProcessRollup2",
    "LogTypeCrowdstrikeProcessRollup2Stats",
    "LogTypeCrowdstrikeSyntheticProcessRollup2",
    "LogTypeCrowdstrikeUnknown",
    "LogTypeCrowdstrikeUserIdentity",
    "LogTypeCrowdstrikeUserInfo",
    "LogTypeCrowdstrikeUserLogonLogoff",
    "LogTypeDropboxTeamEvent",
    "LogTypeDuoAdministrator",
    "LogTypeDuoAuthentication",
    "LogTypeDuoOfflineEnrollment",
    "LogTypeDuoTelephony",
    "LogTypeFastlyAccess",
    "LogTypeFluentdSyslog3164",
    "LogTypeFluentdSyslog5424",
    "LogTypeGCPAuditLog",
    "LogTypeGCPHTTPLoadBalancer",
    "LogTypeGSuiteActivityEvent",
    "LogTypeGSuiteReports",
    "LogTypeGitHubAudit",
    "LogTypeGitLabAPI",
    "LogTypeGitLabAudit",
    "LogTypeGitLabExceptions",
    "LogTypeGitLabGit",
    "LogTypeGitLabIntegrations",
    "LogTypeGitLabProduction",
    "LogTypeGravitationalTeleportAudit",
    "LogTypeGreyNoiseNoise",
    "LogTypeGreyNoiseRIOT",
    "LogTypeIPInfoASNCIDR",
    "LogTypeIPInfoASNRanges",
    "LogTypeIPInfoLocationCIDR",
    "LogTypeIPInfoLocationRanges",
    "LogTypeIPInfoPrivacyCIDR",
    "LogTypeIPInfoPrivacyRanges",
    "LogTypeJamfproLogin",
    "LogTypeJuniperAccess",
    "LogTypeJuniperAudit",
    "LogTypeJuniperFirewall",
    "LogTypeJuniperMWS",
    "LogTypeJuniperPostgres",
    "LogTypeJuniperSecurity",
    "LogTypeLaceworkAgentManagement",
    "LogTypeLaceworkAlertDetails",
    "LogTypeLaceworkAllFiles",
    "LogTypeLaceworkApplications",
    "LogTypeLaceworkChangeFiles",
    "LogTypeLaceworkCloudCompliance",
    "LogTypeLaceworkCloudConfiguration",
    "LogTypeLaceworkCmdline",
    "LogTypeLaceworkConnections",
    "LogTypeLaceworkContainerSummary",
    "LogTypeLaceworkContainerVulnDetails",
    "LogTypeLaceworkDNSQuery",
    "LogTypeLaceworkEvents",
    "LogTypeLaceworkHostVulnDetails",
    "LogTypeLaceworkImage",
    "LogTypeLaceworkInterfaces",
    "LogTypeLaceworkInternalIPA",
    "LogTypeLaceworkMachineDetails",
    "LogTypeLaceworkMachineSummary",
    "LogTypeLaceworkNewHashes",
    "LogTypeLaceworkPackage",
    "LogTypeLaceworkPodSummary",
    "LogTypeLaceworkProcessSummary",
    "LogTypeLaceworkUserDetails",
    "LogTypeLaceworkUserLogin",
    "LogTypeMicrosoft365AuditAzureActiveDirectory",
    "LogTypeMicrosoft365AuditExchange",
    "LogTypeMicrosoft365AuditGeneral",
    "LogTypeMicrosoft365AuditSharePoint",
    "LogTypeMicrosoft365DLPAll",
    "LogTypeMicrosoftGraphSecurityAlert",
    "LogTypeMongoDBOrganizationEvent",
    "LogTypeMongoDBProjectEvent",
    "LogTypeNginxAccess",
    "LogTypeOSSECEventInfo",
    "LogTypeOktaSystemLog",
    "LogTypeOneLoginEvents",
    "LogTypeOnePasswordItemUsage",
    "LogTypeOnePasswordSignInAttempt",
    "LogTypeOsqueryBatch",
    "LogTypeOsqueryDifferential",
    "LogTypeOsquerySnapshot",
    "LogTypeOsqueryStatus",
    "LogTypePantherAudit",
    "LogTypeSalesforceLogin",
    "LogTypeSalesforceLoginAs",
    "LogTypeSalesforceLogout",
    "LogTypeSalesforceURI",
    "LogTypeSentinelOneActivity",
    "LogTypeSentinelOneDeepVisibility",
    "LogTypeSentinelOneDeepVisibilityV2",
    "LogTypeSlackAccessLogs",
    "LogTypeSlackAuditLogs",
    "LogTypeSlackIntegrationLogs",
    "LogTypeSnykGroupAudit",
    "LogTypeSnykOrgAudit",
    "LogTypeSophosCentral",
    "LogTypeSuricataAlert",
    "LogTypeSuricataAnomaly",
    "LogTypeSuricataDHCP",
    "LogTypeSuricataDNS",
    "LogTypeSuricataFileInfo",
    "LogTypeSuricataFlow",
    "LogTypeSuricataHTTP",
    "LogTypeSuricataSSH",
    "LogTypeSuricataTLS",
    "LogTypeSysdigAudit",
    "LogTypeSyslogRFC3164",
    "LogTypeSyslogRFC5424",
    "LogTypeTorExitNode",
    "LogTypeWorkdayActivity",
    "LogTypeWorkdaySignOnAttempt",
    "LogTypeZeekCaptureLoss",
    "LogTypeZeekConn",
    "LogTypeZeekDHCP",
    "LogTypeZeekDNS",
    "LogTypeZeekDPD",
    "LogTypeZeekFiles",
    "LogTypeZeekHTTP",
    "LogTypeZeekNTP",
    "LogTypeZeekNotice",
    "LogTypeZeekOCSP",
    "LogTypeZeekReporter",
    "LogTypeZeekSoftware",
    "LogTypeZeekSsh",
    "LogTypeZeekSsl",
    "LogTypeZeekStats",
    "LogTypeZeekTunnel",
    "LogTypeZeekWeird",
    "LogTypeZeekX509",
    "LogTypeZendeskAudit",
    "LogTypeZoomActivity",
    "LogTypeZoomOperation",
]


LogTypeAWSALB = "AWS.ALB"
LogTypeAWSAuroraMySQLAudit = "AWS.AuroraMySQLAudit"
LogTypeAWSCloudTrail = "AWS.CloudTrail"
LogTypeAWSCloudTrailDigest = "AWS.CloudTrailDigest"
LogTypeAWSCloudTrailInsight = "AWS.CloudTrailInsight"
LogTypeAWSCloudWatchEvents = "AWS.CloudWatchEvents"
LogTypeAWSConfig = "AWS.Config"
LogTypeAWSGuardDuty = "AWS.GuardDuty"
LogTypeAWSS3ServerAccess = "AWS.S3ServerAccess"
LogTypeAWSTransitGatewayFlow = "AWS.TransitGatewayFlow"
LogTypeAWSVPCDns = "AWS.VPCDns"
LogTypeAWSVPCFlow = "AWS.VPCFlow"
LogTypeAWSWAFWebACL = "AWS.WAFWebACL"
LogTypeAlphaSOCAlert = "AlphaSOC.Alert"
LogTypeAmazonEKSAudit = "Amazon.EKS.Audit"
LogTypeAmazonEKSAuthenticator = "Amazon.EKS.Authenticator"
LogTypeApacheAccessCombined = "Apache.AccessCombined"
LogTypeApacheAccessCommon = "Apache.AccessCommon"
LogTypeAsanaAudit = "Asana.Audit"
LogTypeAtlassianAudit = "Atlassian.Audit"
LogTypeBitwardenEvents = "Bitwarden.Events"
LogTypeBoxEvent = "Box.Event"
LogTypeCiscoUmbrellaCloudFirewall = "CiscoUmbrella.CloudFirewall"
LogTypeCiscoUmbrellaDNS = "CiscoUmbrella.DNS"
LogTypeCiscoUmbrellaIP = "CiscoUmbrella.IP"
LogTypeCiscoUmbrellaProxy = "CiscoUmbrella.Proxy"
LogTypeCloudflareAudit = "Cloudflare.Audit"
LogTypeCloudflareFirewall = "Cloudflare.Firewall"
LogTypeCloudflareHttpRequest = "Cloudflare.HttpRequest"
LogTypeCloudflareSpectrum = "Cloudflare.Spectrum"
LogTypeCrowdstrikeAIDMaster = "Crowdstrike.AIDMaster"
LogTypeCrowdstrikeActivityAudit = "Crowdstrike.ActivityAudit"
LogTypeCrowdstrikeAppInfo = "Crowdstrike.AppInfo"
LogTypeCrowdstrikeCriticalFile = "Crowdstrike.CriticalFile"
LogTypeCrowdstrikeDNSRequest = "Crowdstrike.DNSRequest"
LogTypeCrowdstrikeDetectionSummary = "Crowdstrike.DetectionSummary"
LogTypeCrowdstrikeFDREvent = "Crowdstrike.FDREvent"
LogTypeCrowdstrikeGroupIdentity = "Crowdstrike.GroupIdentity"
LogTypeCrowdstrikeManagedAssets = "Crowdstrike.ManagedAssets"
LogTypeCrowdstrikeNetworkConnect = "Crowdstrike.NetworkConnect"
LogTypeCrowdstrikeNetworkListen = "Crowdstrike.NetworkListen"
LogTypeCrowdstrikeNotManagedAssets = "Crowdstrike.NotManagedAssets"
LogTypeCrowdstrikeProcessRollup2 = "Crowdstrike.ProcessRollup2"
LogTypeCrowdstrikeProcessRollup2Stats = "Crowdstrike.ProcessRollup2Stats"
LogTypeCrowdstrikeSyntheticProcessRollup2 = "Crowdstrike.SyntheticProcessRollup2"
LogTypeCrowdstrikeUnknown = "Crowdstrike.Unknown"
LogTypeCrowdstrikeUserIdentity = "Crowdstrike.UserIdentity"
LogTypeCrowdstrikeUserInfo = "Crowdstrike.UserInfo"
LogTypeCrowdstrikeUserLogonLogoff = "Crowdstrike.UserLogonLogoff"
LogTypeDropboxTeamEvent = "Dropbox.TeamEvent"
LogTypeDuoAdministrator = "Duo.Administrator"
LogTypeDuoAuthentication = "Duo.Authentication"
LogTypeDuoOfflineEnrollment = "Duo.OfflineEnrollment"
LogTypeDuoTelephony = "Duo.Telephony"
LogTypeFastlyAccess = "Fastly.Access"
LogTypeFluentdSyslog3164 = "Fluentd.Syslog3164"
LogTypeFluentdSyslog5424 = "Fluentd.Syslog5424"
LogTypeGCPAuditLog = "GCP.AuditLog"
LogTypeGCPHTTPLoadBalancer = "GCP.HTTPLoadBalancer"
LogTypeGSuiteActivityEvent = "GSuite.ActivityEvent"
LogTypeGSuiteReports = "GSuite.Reports"
LogTypeGitHubAudit = "GitHub.Audit"
LogTypeGitLabAPI = "GitLab.API"
LogTypeGitLabAudit = "GitLab.Audit"
LogTypeGitLabExceptions = "GitLab.Exceptions"
LogTypeGitLabGit = "GitLab.Git"
LogTypeGitLabIntegrations = "GitLab.Integrations"
LogTypeGitLabProduction = "GitLab.Production"
LogTypeGravitationalTeleportAudit = "Gravitational.TeleportAudit"
LogTypeGreyNoiseNoise = "GreyNoise.Noise"
LogTypeGreyNoiseRIOT = "GreyNoise.RIOT"
LogTypeIPInfoASNCIDR = "IPInfo.ASNCIDR"
LogTypeIPInfoASNRanges = "IPInfo.ASNRanges"
LogTypeIPInfoLocationCIDR = "IPInfo.LocationCIDR"
LogTypeIPInfoLocationRanges = "IPInfo.LocationRanges"
LogTypeIPInfoPrivacyCIDR = "IPInfo.PrivacyCIDR"
LogTypeIPInfoPrivacyRanges = "IPInfo.PrivacyRanges"
LogTypeJamfproLogin = "Jamfpro.Login"
LogTypeJuniperAccess = "Juniper.Access"
LogTypeJuniperAudit = "Juniper.Audit"
LogTypeJuniperFirewall = "Juniper.Firewall"
LogTypeJuniperMWS = "Juniper.MWS"
LogTypeJuniperPostgres = "Juniper.Postgres"
LogTypeJuniperSecurity = "Juniper.Security"
LogTypeLaceworkAgentManagement = "Lacework.AgentManagement"
LogTypeLaceworkAlertDetails = "Lacework.AlertDetails"
LogTypeLaceworkAllFiles = "Lacework.AllFiles"
LogTypeLaceworkApplications = "Lacework.Applications"
LogTypeLaceworkChangeFiles = "Lacework.ChangeFiles"
LogTypeLaceworkCloudCompliance = "Lacework.CloudCompliance"
LogTypeLaceworkCloudConfiguration = "Lacework.CloudConfiguration"
LogTypeLaceworkCmdline = "Lacework.Cmdline"
LogTypeLaceworkConnections = "Lacework.Connections"
LogTypeLaceworkContainerSummary = "Lacework.ContainerSummary"
LogTypeLaceworkContainerVulnDetails = "Lacework.ContainerVulnDetails"
LogTypeLaceworkDNSQuery = "Lacework.DNSQuery"
LogTypeLaceworkEvents = "Lacework.Events"
LogTypeLaceworkHostVulnDetails = "Lacework.HostVulnDetails"
LogTypeLaceworkImage = "Lacework.Image"
LogTypeLaceworkInterfaces = "Lacework.Interfaces"
LogTypeLaceworkInternalIPA = "Lacework.InternalIPA"
LogTypeLaceworkMachineDetails = "Lacework.MachineDetails"
LogTypeLaceworkMachineSummary = "Lacework.MachineSummary"
LogTypeLaceworkNewHashes = "Lacework.NewHashes"
LogTypeLaceworkPackage = "Lacework.Package"
LogTypeLaceworkPodSummary = "Lacework.PodSummary"
LogTypeLaceworkProcessSummary = "Lacework.ProcessSummary"
LogTypeLaceworkUserDetails = "Lacework.UserDetails"
LogTypeLaceworkUserLogin = "Lacework.UserLogin"
LogTypeMicrosoft365AuditAzureActiveDirectory = "Microsoft365.Audit.AzureActiveDirectory"
LogTypeMicrosoft365AuditExchange = "Microsoft365.Audit.Exchange"
LogTypeMicrosoft365AuditGeneral = "Microsoft365.Audit.General"
LogTypeMicrosoft365AuditSharePoint = "Microsoft365.Audit.SharePoint"
LogTypeMicrosoft365DLPAll = "Microsoft365.DLP.All"
LogTypeMicrosoftGraphSecurityAlert = "MicrosoftGraph.SecurityAlert"
LogTypeMongoDBOrganizationEvent = "MongoDB.OrganizationEvent"
LogTypeMongoDBProjectEvent = "MongoDB.ProjectEvent"
LogTypeNginxAccess = "Nginx.Access"
LogTypeOSSECEventInfo = "OSSEC.EventInfo"
LogTypeOktaSystemLog = "Okta.SystemLog"
LogTypeOneLoginEvents = "OneLogin.Events"
LogTypeOnePasswordItemUsage = "OnePassword.ItemUsage"
LogTypeOnePasswordSignInAttempt = "OnePassword.SignInAttempt"
LogTypeOsqueryBatch = "Osquery.Batch"
LogTypeOsqueryDifferential = "Osquery.Differential"
LogTypeOsquerySnapshot = "Osquery.Snapshot"
LogTypeOsqueryStatus = "Osquery.Status"
LogTypePantherAudit = "Panther.Audit"
LogTypeSalesforceLogin = "Salesforce.Login"
LogTypeSalesforceLoginAs = "Salesforce.LoginAs"
LogTypeSalesforceLogout = "Salesforce.Logout"
LogTypeSalesforceURI = "Salesforce.URI"
LogTypeSentinelOneActivity = "SentinelOne.Activity"
LogTypeSentinelOneDeepVisibility = "SentinelOne.DeepVisibility"
LogTypeSentinelOneDeepVisibilityV2 = "SentinelOne.DeepVisibilityV2"
LogTypeSlackAccessLogs = "Slack.AccessLogs"
LogTypeSlackAuditLogs = "Slack.AuditLogs"
LogTypeSlackIntegrationLogs = "Slack.IntegrationLogs"
LogTypeSnykGroupAudit = "Snyk.GroupAudit"
LogTypeSnykOrgAudit = "Snyk.OrgAudit"
LogTypeSophosCentral = "Sophos.Central"
LogTypeSuricataAlert = "Suricata.Alert"
LogTypeSuricataAnomaly = "Suricata.Anomaly"
LogTypeSuricataDHCP = "Suricata.DHCP"
LogTypeSuricataDNS = "Suricata.DNS"
LogTypeSuricataFileInfo = "Suricata.FileInfo"
LogTypeSuricataFlow = "Suricata.Flow"
LogTypeSuricataHTTP = "Suricata.HTTP"
LogTypeSuricataSSH = "Suricata.SSH"
LogTypeSuricataTLS = "Suricata.TLS"
LogTypeSysdigAudit = "Sysdig.Audit"
LogTypeSyslogRFC3164 = "Syslog.RFC3164"
LogTypeSyslogRFC5424 = "Syslog.RFC5424"
LogTypeTorExitNode = "Tor.ExitNode"
LogTypeWorkdayActivity = "Workday.Activity"
LogTypeWorkdaySignOnAttempt = "Workday.SignOnAttempt"
LogTypeZeekCaptureLoss = "Zeek.CaptureLoss"
LogTypeZeekConn = "Zeek.Conn"
LogTypeZeekDHCP = "Zeek.DHCP"
LogTypeZeekDNS = "Zeek.DNS"
LogTypeZeekDPD = "Zeek.DPD"
LogTypeZeekFiles = "Zeek.Files"
LogTypeZeekHTTP = "Zeek.HTTP"
LogTypeZeekNTP = "Zeek.NTP"
LogTypeZeekNotice = "Zeek.Notice"
LogTypeZeekOCSP = "Zeek.OCSP"
LogTypeZeekReporter = "Zeek.Reporter"
LogTypeZeekSoftware = "Zeek.Software"
LogTypeZeekSsh = "Zeek.Ssh"
LogTypeZeekSsl = "Zeek.Ssl"
LogTypeZeekStats = "Zeek.Stats"
LogTypeZeekTunnel = "Zeek.Tunnel"
LogTypeZeekWeird = "Zeek.Weird"
LogTypeZeekX509 = "Zeek.X509"
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
