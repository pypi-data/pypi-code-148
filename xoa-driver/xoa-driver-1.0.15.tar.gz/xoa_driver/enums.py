#: Available enums used by commands and server response status.

from .internals.core.commands.enums import *
from .internals.core.protocol.constants import CommandStatus

__all__ = (
    "ReservedStatus",
    "ReservedAction",
    "ChassisShutdownAction",
    "OnOff",
    "RESTControlAction",
    "ServiceStatus",
    "ChassisSessionType",
    "TimeSyncMode",
    "MediaCFPState",
    "MediaCFPType",
    "SMAInputFunction",
    "SMAOutputFunction",
    "SMAStatus",
    "HasDemo",
    "IsValid",
    "IsPermanent",
    "YesNo",
    "UpdateState",
    "IsOnline",
    "PortSpeedMode",
    "SyncStatus",
    "LoopbackMode",
    "TrafficOnOff",
    "StartOrStop",
    "LatencyMode",
    "SourceType",
    "PacketDetailSelection",
    "OnOffWithSuppress",
    "ProtocolOption",
    "ModifierAction",
    "LengthType",
    "PayloadType",
    "MDIXMode",
    "LengthCheckType",
    "StartTrigger",
    "StopTrigger",
    "PacketType",
    "InjectErrorType",
    "HeaderLockStatus",
    "AlignLockStatus",
    "PRBSLockStatus",
    "MulticastOperation",
    "MulticastExtOperation",
    "IGMPVersion",
    "TXMode",
    "PayloadMode",
    "BRRMode",
    "TXClockSource",
    "TXClockStatus",
    "LoopBandwidth",
    "MediaConfigurationType",
    "TXHState",
    "RXHState",
    "TXCState",
    "RXCState",
    "LinkState",
    "FaultSignaling",
    "LocalFaultStatus",
    "RemoteFaultStatus",
    "TPLDMode",
    "SerdesStatus",
    "FECMode",
    "PRBSInsertedType",
    "PRBSPolynomial",
    "PRBSInvertState",
    "PRBSStatisticsMode",
    "AutoNegMode",
    "AutoNegTecAbility",
    "AutoNegFECOption",
    "PauseMode",
    "AutoNegFECType",
    "AutoNegStatus",
    "AutoNegFECStatus",
    "LinkTrainingMode",
    "PAM4FrameSize",
    "LinkTrainingInitCondition",
    "NRZPreset",
    "TimeoutMode",
    "LinkTrainingStatusMode",
    "LinkTrainingStatus",
    "LinkTrainingFailureType",
    "Role",
    "Timescale",
    "MSSType",
    "RTOType",
    "CongestionType",
    "IsEnabled",
    "AlgorithmMethod",
    "AutoOrManual",
    "EmbedIP",
    "ApplicationLayerBehavior",
    "TrafficScenario",
    "PayloadGenerationMethod",
    "InfiniteOrFinite",
    "WhoClose",
    "LifecycleMode",
    "L47IPVersion",
    "L47ProtocolType",
    "L47TrafficState",
    "L47PortState",
    "L47PortSpeed",
    "CaptureSize",
    "ReplayParserState",
    "IsPresent",
    "LicenseSpeed",
    "TLSVersion",
    "MulticastHeaderFormat",
    "CorruptionType",
    "PolicerMode",
    "FilterUse",
    "InfoAction",
    "L2PlusPresent",
    "L3PlusPresent",
    "FilterMode",
    "TimeKeeperLicenseFileState",
    "TimeKeeperLicenseType",
    "TimeKeeperLicenseError",
    "SystemUpdateStatus",
    "TimeKeeperServiceStatus",
    "TimeKeeperServiceAction",
    "CustomDefaultCommand",
    "CustomDefaultScope",
    "ImpairmentLatencyMode",
    "ResourceAllocationMode",
    "ReplaySchedulingMode",
    "ReplaySyncBasedOn",
    "TrafficError",
    "PRBSOnOff",
    "ErrorOnOff",
    "PRBSPattern",
    "PHYSignalStatus",
    "ShadowWorkingSelection",
    "TSNConfigProfile",
    "TSNPortRole",
    "TSNDeviationMode",
    "TSNTimeSource",
    "TSNHistogramSource",
    "TSNStatisticsTypes",
    "PFCMode",
    "OnOffDefault",
    "ImpairmentTypeIndex",
    "FilterType",
    "FilterVlanType",
    "LatencyTypeCustomDist",
    "CommandStatus",
    "TrafficEngine",
    "ReconciliationSublayerSupport",
    "PPMSweepStatus",
    "PPMSweepMode"
)