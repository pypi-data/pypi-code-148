from pydantic import BaseModel
from pydantic_appconfig import AppConfigHelper


class MyAppConfig(BaseModel):
    """My app config."""

    test_field_string: str
    test_field_int: int

    class Config:
        """The pydantic config, including title for the JSON schema."""

        title = "MyAppConfig"


config = AppConfigHelper(
    appconfig_application="AppConfig-App",
    appconfig_environment="AppConfig-Env",
    appconfig_profile="AppConfig-Profile",
    max_config_age=15,
    fetch_on_init=True,
    config_schema_model=MyAppConfig,
)
