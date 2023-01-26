import configparser
from pathlib import PosixPath

import boto3
import click
from botocore.exceptions import ProfileNotFound

CFG_KEY_MFA_SERIAL = "mfa_serial"
CFG_KEY_SSO_SESSION = "sso_session"


def validate_aws_profile(profile):
    boto3.Session(profile_name=profile)


def read_config_section(config_file: str, section: str) -> list[tuple[str, str]]:
    config = configparser.RawConfigParser()
    config.read(PosixPath(config_file).expanduser())
    return config.items(section)


def read_source_profile_configs(
    profile: str, config_file: str
) -> list[tuple[str, str]]:
    return read_config_section(config_file, f"profile {profile}")


def read_source_profile_credentials(
    profile: str, credentials_file: str
) -> list[tuple[str, str]]:
    return read_config_section(credentials_file, profile)


def needs_mfa(configs: list[tuple[str, str]]) -> bool:
    return any([True if key == CFG_KEY_MFA_SERIAL else False for key, _ in configs])


def needs_sso(configs: list[tuple[str, str]]) -> bool:
    return any([True if key == CFG_KEY_SSO_SESSION else False for key, _ in configs])


def overwrite_config_section(
    section: str, configs: list[tuple[str, str]], config_file: str
):

    config = configparser.RawConfigParser()
    config.read(PosixPath(config_file).expanduser())
    config[section] = {k: v for k, v in configs}

    with open(PosixPath(config_file).expanduser(), "w") as fp:
        config.write(fp)


def write_default_configs(configs: list[tuple[str, str]], config_file: str):
    overwrite_config_section("default", configs, config_file)


def write_default_credentials(
    credentials: list[tuple[str, str]], credentials_file: str
):
    overwrite_config_section("default", credentials, credentials_file)


def get_mfa_credentials(
    profile: str, mfa_serial: str, token_code: str, session_duration: int
):
    sts = boto3.Session(profile_name=profile).client("sts")
    response = sts.get_session_token(
        DurationSeconds=session_duration,
        SerialNumber=mfa_serial,
        TokenCode=token_code,
    )
    return [
        ("aws_access_key_id", response["Credentials"]["AccessKeyId"]),
        ("aws_secret_access_key", response["Credentials"]["SecretAccessKey"]),
        ("aws_session_token", response["Credentials"]["SessionToken"]),
    ]


@click.command()
@click.argument("source-profile")
@click.option(
    "--credentials-file",
    default="~/.aws/credentials",
    type=click.Path(),
    help="Path to aws cli credentials file",
)
@click.option(
    "--config-file",
    default="~/.aws/config",
    type=click.Path(),
    help="Path to aws cli config file",
)
@click.option(
    "--token-code", type=str, help="MFA token code (applicable on MFA based profiles)"
)
@click.option(
    "--session-duration",
    type=int,
    default=43200,
    help="Session duration in seconds (applicable on MFA based profiles)",
)
def run(
    source_profile: str,
    credentials_file: str,
    config_file: str,
    token_code: str,
    session_duration: int,
):
    try:
        validate_aws_profile(source_profile)
    except ProfileNotFound:
        print(f"Unable to find AWS cli profile {source_profile}")
        exit(1)

    configs = read_source_profile_configs(source_profile, config_file)

    mfa = needs_mfa(configs)
    sso = needs_sso(configs)

    if not mfa and not sso:
        write_default_configs(configs, config_file)
        write_default_credentials(
            read_source_profile_credentials(source_profile, credentials_file),
            credentials_file,
        )

    elif mfa is True:

        if token_code is None:
            print(
                "A token code is required to use a MFA based profile as default profile"
            )
            exit(1)

        mfa_serial = [v for k, v in configs if k == CFG_KEY_MFA_SERIAL].pop()

        # get credentials with mfa token
        mfa_credentials = get_mfa_credentials(
            source_profile, mfa_serial, token_code, session_duration
        )

        # write default profile with credentials
        write_default_configs(configs, config_file)
        write_default_credentials(mfa_credentials, credentials_file)

    elif sso is True:
        write_default_configs(configs, config_file)

    else:
        print("Unsupported profile configuration.")
        exit(1)


if __name__ == "__main__":
    run()
