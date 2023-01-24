"""
Type annotations for ssm-sap service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_sap/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm_sap.type_defs import ApplicationCredentialTypeDef

    data: ApplicationCredentialTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ApplicationStatusType,
    DatabaseStatusType,
    DatabaseTypeType,
    FilterOperatorType,
    HostRoleType,
    OperationStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ApplicationCredentialTypeDef",
    "ApplicationSummaryTypeDef",
    "ApplicationTypeDef",
    "ComponentSummaryTypeDef",
    "HostTypeDef",
    "DatabaseSummaryTypeDef",
    "DeleteResourcePermissionInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DeregisterApplicationInputRequestTypeDef",
    "FilterTypeDef",
    "GetApplicationInputRequestTypeDef",
    "GetComponentInputRequestTypeDef",
    "GetDatabaseInputRequestTypeDef",
    "GetOperationInputRequestTypeDef",
    "OperationTypeDef",
    "GetResourcePermissionInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationsInputRequestTypeDef",
    "ListComponentsInputRequestTypeDef",
    "ListDatabasesInputRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutResourcePermissionInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "DatabaseTypeDef",
    "RegisterApplicationInputRequestTypeDef",
    "UpdateApplicationSettingsInputRequestTypeDef",
    "ComponentTypeDef",
    "DeleteResourcePermissionOutputTypeDef",
    "GetApplicationOutputTypeDef",
    "GetResourcePermissionOutputTypeDef",
    "ListApplicationsOutputTypeDef",
    "ListComponentsOutputTypeDef",
    "ListDatabasesOutputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutResourcePermissionOutputTypeDef",
    "RegisterApplicationOutputTypeDef",
    "UpdateApplicationSettingsOutputTypeDef",
    "ListOperationsInputRequestTypeDef",
    "GetOperationOutputTypeDef",
    "ListOperationsOutputTypeDef",
    "ListApplicationsInputListApplicationsPaginateTypeDef",
    "ListComponentsInputListComponentsPaginateTypeDef",
    "ListDatabasesInputListDatabasesPaginateTypeDef",
    "ListOperationsInputListOperationsPaginateTypeDef",
    "GetDatabaseOutputTypeDef",
    "GetComponentOutputTypeDef",
)

ApplicationCredentialTypeDef = TypedDict(
    "ApplicationCredentialTypeDef",
    {
        "DatabaseName": str,
        "CredentialType": Literal["ADMIN"],
        "SecretId": str,
    },
)

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "Id": str,
        "Type": Literal["HANA"],
        "Arn": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "Id": str,
        "Type": Literal["HANA"],
        "Arn": str,
        "AppRegistryArn": str,
        "Status": ApplicationStatusType,
        "Components": List[str],
        "LastUpdated": datetime,
        "StatusMessage": str,
    },
    total=False,
)

ComponentSummaryTypeDef = TypedDict(
    "ComponentSummaryTypeDef",
    {
        "ApplicationId": str,
        "ComponentId": str,
        "ComponentType": Literal["HANA"],
        "Tags": Dict[str, str],
    },
    total=False,
)

HostTypeDef = TypedDict(
    "HostTypeDef",
    {
        "HostName": str,
        "HostRole": HostRoleType,
        "HostIp": str,
        "InstanceId": str,
    },
    total=False,
)

DatabaseSummaryTypeDef = TypedDict(
    "DatabaseSummaryTypeDef",
    {
        "ApplicationId": str,
        "ComponentId": str,
        "DatabaseId": str,
        "DatabaseType": DatabaseTypeType,
        "Arn": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredDeleteResourcePermissionInputRequestTypeDef = TypedDict(
    "_RequiredDeleteResourcePermissionInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalDeleteResourcePermissionInputRequestTypeDef = TypedDict(
    "_OptionalDeleteResourcePermissionInputRequestTypeDef",
    {
        "ActionType": Literal["RESTORE"],
        "SourceResourceArn": str,
    },
    total=False,
)


class DeleteResourcePermissionInputRequestTypeDef(
    _RequiredDeleteResourcePermissionInputRequestTypeDef,
    _OptionalDeleteResourcePermissionInputRequestTypeDef,
):
    pass


ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DeregisterApplicationInputRequestTypeDef = TypedDict(
    "DeregisterApplicationInputRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Value": str,
        "Operator": FilterOperatorType,
    },
)

GetApplicationInputRequestTypeDef = TypedDict(
    "GetApplicationInputRequestTypeDef",
    {
        "ApplicationId": str,
        "ApplicationArn": str,
        "AppRegistryArn": str,
    },
    total=False,
)

GetComponentInputRequestTypeDef = TypedDict(
    "GetComponentInputRequestTypeDef",
    {
        "ApplicationId": str,
        "ComponentId": str,
    },
)

GetDatabaseInputRequestTypeDef = TypedDict(
    "GetDatabaseInputRequestTypeDef",
    {
        "ApplicationId": str,
        "ComponentId": str,
        "DatabaseId": str,
        "DatabaseArn": str,
    },
    total=False,
)

GetOperationInputRequestTypeDef = TypedDict(
    "GetOperationInputRequestTypeDef",
    {
        "OperationId": str,
    },
)

OperationTypeDef = TypedDict(
    "OperationTypeDef",
    {
        "Id": str,
        "Type": str,
        "Status": OperationStatusType,
        "StatusMessage": str,
        "Properties": Dict[str, str],
        "ResourceType": str,
        "ResourceId": str,
        "ResourceArn": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredGetResourcePermissionInputRequestTypeDef = TypedDict(
    "_RequiredGetResourcePermissionInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalGetResourcePermissionInputRequestTypeDef = TypedDict(
    "_OptionalGetResourcePermissionInputRequestTypeDef",
    {
        "ActionType": Literal["RESTORE"],
    },
    total=False,
)


class GetResourcePermissionInputRequestTypeDef(
    _RequiredGetResourcePermissionInputRequestTypeDef,
    _OptionalGetResourcePermissionInputRequestTypeDef,
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListApplicationsInputRequestTypeDef = TypedDict(
    "ListApplicationsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListComponentsInputRequestTypeDef = TypedDict(
    "ListComponentsInputRequestTypeDef",
    {
        "ApplicationId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListDatabasesInputRequestTypeDef = TypedDict(
    "ListDatabasesInputRequestTypeDef",
    {
        "ApplicationId": str,
        "ComponentId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

PutResourcePermissionInputRequestTypeDef = TypedDict(
    "PutResourcePermissionInputRequestTypeDef",
    {
        "ActionType": Literal["RESTORE"],
        "SourceResourceArn": str,
        "ResourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

DatabaseTypeDef = TypedDict(
    "DatabaseTypeDef",
    {
        "ApplicationId": str,
        "ComponentId": str,
        "Credentials": List[ApplicationCredentialTypeDef],
        "DatabaseId": str,
        "DatabaseName": str,
        "DatabaseType": DatabaseTypeType,
        "Arn": str,
        "Status": DatabaseStatusType,
        "PrimaryHost": str,
        "SQLPort": int,
        "LastUpdated": datetime,
    },
    total=False,
)

_RequiredRegisterApplicationInputRequestTypeDef = TypedDict(
    "_RequiredRegisterApplicationInputRequestTypeDef",
    {
        "ApplicationId": str,
        "ApplicationType": Literal["HANA"],
        "Instances": Sequence[str],
        "Credentials": Sequence[ApplicationCredentialTypeDef],
    },
)
_OptionalRegisterApplicationInputRequestTypeDef = TypedDict(
    "_OptionalRegisterApplicationInputRequestTypeDef",
    {
        "SapInstanceNumber": str,
        "Sid": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class RegisterApplicationInputRequestTypeDef(
    _RequiredRegisterApplicationInputRequestTypeDef, _OptionalRegisterApplicationInputRequestTypeDef
):
    pass


_RequiredUpdateApplicationSettingsInputRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationSettingsInputRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalUpdateApplicationSettingsInputRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationSettingsInputRequestTypeDef",
    {
        "CredentialsToAddOrUpdate": Sequence[ApplicationCredentialTypeDef],
        "CredentialsToRemove": Sequence[ApplicationCredentialTypeDef],
    },
    total=False,
)


class UpdateApplicationSettingsInputRequestTypeDef(
    _RequiredUpdateApplicationSettingsInputRequestTypeDef,
    _OptionalUpdateApplicationSettingsInputRequestTypeDef,
):
    pass


ComponentTypeDef = TypedDict(
    "ComponentTypeDef",
    {
        "ComponentId": str,
        "ApplicationId": str,
        "ComponentType": Literal["HANA"],
        "Status": Literal["ACTIVATED"],
        "Databases": List[str],
        "Hosts": List[HostTypeDef],
        "PrimaryHost": str,
        "LastUpdated": datetime,
    },
    total=False,
)

DeleteResourcePermissionOutputTypeDef = TypedDict(
    "DeleteResourcePermissionOutputTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationOutputTypeDef = TypedDict(
    "GetApplicationOutputTypeDef",
    {
        "Application": ApplicationTypeDef,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourcePermissionOutputTypeDef = TypedDict(
    "GetResourcePermissionOutputTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsOutputTypeDef = TypedDict(
    "ListApplicationsOutputTypeDef",
    {
        "Applications": List[ApplicationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComponentsOutputTypeDef = TypedDict(
    "ListComponentsOutputTypeDef",
    {
        "Components": List[ComponentSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatabasesOutputTypeDef = TypedDict(
    "ListDatabasesOutputTypeDef",
    {
        "Databases": List[DatabaseSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutResourcePermissionOutputTypeDef = TypedDict(
    "PutResourcePermissionOutputTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterApplicationOutputTypeDef = TypedDict(
    "RegisterApplicationOutputTypeDef",
    {
        "Application": ApplicationTypeDef,
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationSettingsOutputTypeDef = TypedDict(
    "UpdateApplicationSettingsOutputTypeDef",
    {
        "Message": str,
        "OperationIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListOperationsInputRequestTypeDef = TypedDict(
    "_RequiredListOperationsInputRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListOperationsInputRequestTypeDef = TypedDict(
    "_OptionalListOperationsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class ListOperationsInputRequestTypeDef(
    _RequiredListOperationsInputRequestTypeDef, _OptionalListOperationsInputRequestTypeDef
):
    pass


GetOperationOutputTypeDef = TypedDict(
    "GetOperationOutputTypeDef",
    {
        "Operation": OperationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOperationsOutputTypeDef = TypedDict(
    "ListOperationsOutputTypeDef",
    {
        "Operations": List[OperationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsInputListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsInputListApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListComponentsInputListComponentsPaginateTypeDef = TypedDict(
    "ListComponentsInputListComponentsPaginateTypeDef",
    {
        "ApplicationId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDatabasesInputListDatabasesPaginateTypeDef = TypedDict(
    "ListDatabasesInputListDatabasesPaginateTypeDef",
    {
        "ApplicationId": str,
        "ComponentId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListOperationsInputListOperationsPaginateTypeDef = TypedDict(
    "_RequiredListOperationsInputListOperationsPaginateTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListOperationsInputListOperationsPaginateTypeDef = TypedDict(
    "_OptionalListOperationsInputListOperationsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListOperationsInputListOperationsPaginateTypeDef(
    _RequiredListOperationsInputListOperationsPaginateTypeDef,
    _OptionalListOperationsInputListOperationsPaginateTypeDef,
):
    pass


GetDatabaseOutputTypeDef = TypedDict(
    "GetDatabaseOutputTypeDef",
    {
        "Database": DatabaseTypeDef,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetComponentOutputTypeDef = TypedDict(
    "GetComponentOutputTypeDef",
    {
        "Component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
