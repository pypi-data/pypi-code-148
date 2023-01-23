# generated by datamodel-codegen:
#   filename:  openapi.json
#   timestamp: 2022-12-21T13:46:22+00:00

from datetime import datetime
from typing import Any
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Model(BaseModel):
    __root__: Any


class CreateInvitationRequest(BaseModel):
    EmployeeCode: int = Field(
        ..., description="EmployeeCode is integer as registered with CheckedID."
    )
    InviteeEmail: str = Field(
        ...,
        description="InviteeEmail is string used as unique identifier for Invitations.",
    )
    InviteeFirstName: str = Field(
        ...,
        description="InviteeFirstName is string to be used for personally addressing the invitee.",
    )
    InviteeLastName: Optional[str] = Field(
        None,
        description="InviteeLastName is string to be used for personally addressing the invitee.",
    )
    CustomerReference: Optional[str] = Field(
        None,
        description="CustomerReference is string to be used by customers "
        "for identifying this Invitation in their own environment.",
    )
    AppFlow: str = Field(
        ..., description="AppFlow is string with possible values 10 to 29"
    )
    Validity: int = Field(
        ...,
        description="Validity is integer indicating the number"
        " of hours the Invitation is valid after being generated.",
    )
    PreferredLanguage: Optional[str] = Field(
        None,
        description='PreferredLanguage is string with possible values "nl",'
        ' "en", "fr", "de" (Used in sending invitation through email)',
    )


class Invitation(BaseModel):
    EmployeeCode: int = Field(..., description="Employee Code")
    InviteeEmail: str = Field(..., description="Invitee Email")
    InvitationCode: Optional[str] = Field(None, description="Invitation Code")
    InviteeFirstName: str = Field(..., description="First Name")
    InviteeLastName: Optional[str] = Field(
        None,
        description="InviteeLastName is string to be used for personally addressing the invitee.",
    )
    CustomerReference: Optional[str] = Field(None, description="Customer Reference")
    AppFlow: str = Field(..., description="App Flow")
    Validity: int = Field(..., description="Validity")
    InvitedTime: Optional[str] = Field(None, description="Invitation Date Time")
    PreferredLanguage: Optional[str] = Field(None, description="Preferred Language")


class UpdateInvitationRequest(BaseModel):
    InvitationCode: Optional[str] = Field(None, description="Invitation Code")
    InviteeFirstName: str = Field(
        ...,
        description="InviteeFirstName is string to be used for personally addressing the invitee.",
    )
    InviteeLastName: Optional[str] = Field(
        None,
        description="InviteeLastName is string to be used for personally addressing the invitee.",
    )
    CustomerReference: Optional[str] = Field(
        None,
        description="CustomerReference is string to be used by customers for"
        " identifying this Invitation in their own environment.",
    )
    AppFlow: str = Field(
        ..., description="AppFlow is string with possible values 10 to 29"
    )
    Validity: int = Field(
        ...,
        description="Validity is integer indicating the number of hours the"
        " Invitation is valid after being generated.",
    )
    PreferredLanguage: Optional[str] = Field(
        None,
        description='PreferredLanguage is string with possible values "nl", "en",'
        ' "fr", "de" (Used in sending invitation through email)',
    )


class CreateUserRequest(BaseModel):
    UserCode: Optional[int] = Field(None, description="UserCode is integer")
    FirstName: Optional[str] = Field(
        None,
        description="FirstName is string to be used for personally addressing the user.",
    )
    LastName: Optional[str] = Field(
        None,
        description="LastName is string to be used for personally addressing the user.",
    )
    Role: Optional[str] = Field(
        None, description="Role of the user (Admin/Basic/AppOnly)"
    )
    Email: Optional[str] = Field(
        None, description="Email is string used as unique identifier for users."
    )
    Password: Optional[str] = Field(None, description="Password")
    StartDate: Optional[datetime] = Field(None, description="Start Date of the user")
    EndDate: Optional[datetime] = Field(None, description="End Date of the user")
    HolderConfirmationBy: Optional[str] = Field(
        None, description="Holder Confirmation By (App user/CheckedID Auto)"
    )
    UserType: Optional[str] = Field(None, description="User type (Internal/External)")
    UserReference: Optional[str] = Field(None, description="User reference")
    ReportEmailAddress: Optional[str] = Field(
        None, description="Alternative email address for reports"
    )
    NotificationEmailAddress: Optional[str] = Field(
        None, description="Nomination email address"
    )


class CreateUserResponse(BaseModel):
    UserCode: Optional[int] = Field(None, description="User Code")
    FirstName: Optional[str] = Field(
        None,
        description="FirstName is string to be used for personally addressing the user.",
    )
    LastName: Optional[str] = Field(
        None,
        description="LastName is string to be used for personally addressing the user.",
    )
    Role: Optional[str] = Field(
        None, description="Role of the user (Admin/Basic/AppOnly)"
    )
    Email: Optional[str] = Field(
        None, description="Email is string used as unique identifier for users."
    )
    ActivationCode: Optional[str] = Field(
        None, description="Code generated by CheckedID for activation"
    )
    StartDate: Optional[datetime] = Field(None, description="Start Date of the user")
    EndDate: Optional[datetime] = Field(None, description="End Date of the user")
    HolderConfirmationBy: Optional[str] = Field(
        None, description="Holder Confirmation By (App user/CheckedID Auto)"
    )
    UserType: Optional[str] = Field(None, description="User type (Internal/External)")
    UserReference: Optional[str] = Field(None, description="User reference")
    ReportEmailAddress: Optional[str] = Field(
        None, description="Alternative email address for reports"
    )
    NotificationEmailAddress: Optional[str] = Field(
        None, description="Nomination email address"
    )


class UserRequest(BaseModel):
    UserCode: Optional[int] = Field(None, description="UserCode is integer")
    FirstName: Optional[str] = Field(
        None,
        description="FirstName is string to be used for personally addressing the user.",
    )
    LastName: Optional[str] = Field(
        None,
        description="LastName is string to be used for personally addressing the user.",
    )
    Role: Optional[str] = Field(
        None, description="Role of the user (Admin/Basic/AppOnly)"
    )
    Email: Optional[str] = Field(
        None, description="Email is string used as unique identifier for users."
    )
    Password: Optional[str] = Field(None, description="Password")
    StartDate: Optional[datetime] = Field(None, description="Start Date of the user")
    EndDate: Optional[datetime] = Field(None, description="End Date of the user")
    HolderConfirmationBy: Optional[str] = Field(
        None, description="Holder Confirmation By (App user/CheckedID Auto)"
    )
    UserType: Optional[str] = Field(None, description="User type (Internal/External)")
    UserReference: Optional[str] = Field(None, description="User reference")
    ReportEmailAddress: Optional[str] = Field(
        None, description="Alternative email address for reports"
    )
    NotificationEmailAddress: Optional[str] = Field(
        None, description="Notification email address"
    )


class UpdateUserResponse(BaseModel):
    UserCode: Optional[int] = Field(None, description="User Code")
    FirstName: Optional[str] = Field(
        None,
        description="FirstName is string to be used for personally addressing the user.",
    )
    LastName: Optional[str] = Field(
        None,
        description="LastName is string to be used for personally addressing the user.",
    )
    Role: Optional[str] = Field(
        None, description="Role of the user (Admin/Basic/AppOnly)"
    )
    Email: Optional[str] = Field(
        None, description="Email is string used as unique identifier for users."
    )
    ActivationCode: Optional[str] = Field(
        None, description="Code generated by CheckedID for activation"
    )
    StartDate: Optional[datetime] = Field(None, description="Start Date of the user")
    EndDate: Optional[datetime] = Field(None, description="End Date of the user")
    HolderConfirmationBy: Optional[str] = Field(
        None, description="Holder Confirmation By (App user/CheckedID Auto)"
    )
    UserType: Optional[str] = Field(None, description="User type (Internal/External)")
    UserReference: Optional[str] = Field(None, description="User reference")
    ReportEmailAddress: Optional[str] = Field(
        None, description="Alternative email address for reports"
    )
    NotificationEmailAddress: Optional[str] = Field(
        None, description="Notification email address"
    )


class ActivateUserRequest(BaseModel):
    UserCode: Optional[int] = Field(None, description="UserCode is integer")


class ActivateUserResponse(BaseModel):
    UserCode: Optional[int] = Field(None, description="UserCode is integer")
    ActivationCode: Optional[str] = Field(None, description="Generated activation code")


class ReportResponse(BaseModel):
    DossierNumber: Optional[str] = Field(None, description="Dossier Number")
    ReportPDF: Optional[str] = Field(None, description="Report PDF")


class ReportDataV3(BaseModel):
    CustomerCode: Optional[str] = Field(None, description="Customer Code")
    CustomerName: Optional[str] = Field(None, description="Customer name")
    DossierNumber: Optional[str] = Field(
        None, description="Dossier number of the report"
    )
    EmployeeCode: Optional[str] = Field(None, description="Employee Code")
    EmployeeInvolved: Optional[str] = Field(None, description="Employee Involved")
    ReportDateTime: Optional[str] = Field(None, description="Report Date Time")
    ExecutedBy: Optional[str] = Field(None, description="Executed By")
    ReportResult: Optional[str] = Field(None, description="Result")
    Details: Optional[str] = Field(None, description="Details")
    DetailsMessageCode: Optional[str] = Field(None, description="Details Message Code")
    DocumentType: Optional[str] = Field(None, description="Document Type")
    DocumentTypeCode: Optional[str] = Field(None, description="Document Code")
    DocumentCountry: Optional[str] = Field(None, description="Document Country")
    DocumentNumber: Optional[str] = Field(None, description="Document Number")
    DateOfIssue: Optional[str] = Field(None, description="Date of Issue")
    DateOfExpiry: Optional[str] = Field(None, description="Date of Expiry")
    Authority: Optional[str] = Field(None, description="Authority")
    FirstName: Optional[str] = Field(None, description="First Name")
    Name: Optional[str] = Field(None, description="Name")
    Sex: Optional[str] = Field(None, description="Sex")
    DateOfBirth: Optional[str] = Field(None, description="Date of Birth")
    PlaceOfBirth: Optional[str] = Field(None, description="Place of Birth")
    PersonalNumber: Optional[str] = Field(None, description="Personal Number")
    Nationality: Optional[str] = Field(None, description="Nationality")
    PhotoIdChip: Optional[List[str]] = Field(None, description="Photo Id Chip")
    PhotoHolder: Optional[List[str]] = Field(None, description="Photo Holder")
    IdDocumentFront: Optional[List[str]] = Field(None, description="Front Document")
    IdDocumentBack: Optional[List[str]] = Field(None, description="Back Document")
    OtherDocument: Optional[List[str]] = Field(None, description="Other document")
    SignatureFromIDDocument: Optional[str] = Field(
        None, description="Signature from ID Document"
    )


class ResultCallbackStatus(BaseModel):
    CustomerCode: Optional[int] = Field(None, description="Customer Code")
    EmployeeCode: Optional[int] = Field(None, description="Employee Code")
    InviteeEmail: Optional[str] = Field(None, description="Invitee Email")
    CustomerReference: Optional[str] = Field(None, description="Customer Reference")
    InvitationCode: Optional[str] = Field(None, description="Invitation Code")
    DossierNumber: Optional[str] = Field(None, description="Dossier Number")
    ReportDateTime: Optional[str] = Field(None, description="Report Date Time")
    ReportResult: Optional[str] = Field(None, description="Result")
    Details: Optional[str] = Field(None, description="Details")
    DetailsMessageCode: Optional[str] = Field(None, description="Message Codes")
    Status: Optional[str] = Field(None, description="Status")


class CreateInvitationDetails(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Invitations: List[CreateInvitationRequest] = Field(
        ..., description="List of Invitations"
    )


class CustomerDetails(BaseModel):
    CustomerCode: int = Field(..., description="Customer Code")
    Invitations: List[Invitation] = Field(..., description="List of Invitations")


class UpdateInvitationDetails(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Invitations: List[UpdateInvitationRequest] = Field(
        ..., description="List of Invitations"
    )


class CreateUserDetails(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Users: List[CreateUserRequest] = Field(..., description="List of Users")


class CreateUserDetailsResponse(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Users: List[CreateUserResponse] = Field(..., description="List of users")


class UpdateUserDetails(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Users: List[UserRequest] = Field(..., description="List of Users")


class UpdateUserDetailsResponse(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Users: List[UpdateUserResponse] = Field(..., description="List of users")


class ActivateUsers(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Users: List[ActivateUserRequest] = Field(..., description="List of Users")


class ActivateUsersResponse(BaseModel):
    CustomerCode: int = Field(
        ..., description="CustomerCode is integer as registered with CheckedID."
    )
    Users: List[ActivateUserResponse] = Field(..., description="List of Users")
