import spyctl.cli as cli
import spyctl.spyctl_lib as lib
import spyctl.config.configs as cfgs
import spyctl.config.secrets as s
import spyctl.resources.policies as p
import spyctl.resources.baselines as b


def handle_validate(file):
    if file:
        resrc_data = lib.load_resource_file(file)
    metadata = resrc_data.get(lib.METADATA_FIELD)
    if not metadata:
        cli.err_exit(f"Resource file missing {lib.METADATA_FIELD}.")
    elif not isinstance(metadata, dict):
        cli.err_exit(f"{lib.METADATA_FIELD} is not a dictionary.")
    resrc_kind = metadata.get(lib.KIND_FIELD)
    if not resrc_kind:
        cli.err_exit(
            f"Missing or invalid {lib.KIND_FIELD} field in {lib.METADATA_FIELD}."
        )
    if resrc_kind == lib.CONFIG_ALIAS:
        handle_validate_config(resrc_data)
    elif resrc_kind == lib.SECRETS_ALIAS:
        handle_validate_secret(resrc_data)
    elif resrc_kind == lib.BASELINES_RESOURCE:
        handle_validate_baseline(resrc_data)
    elif resrc_kind == lib.POLICIES_RESOURCE:
        handle_validate_policy(resrc_data)
    else:
        cli.err_exit(
            f"The 'validate' command is not supported for {resrc_kind}"
        )


def handle_validate_config(resrc_data):
    pass


def handle_validate_secret(resrc_data):
    pass


def handle_validate_baseline(resrc_data):
    pass


def handle_validate_policy(resrc_data):
    pass
