# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from jsonschema import validate
import os
import re

from azureml.dataprep.api.mltable._mltable_helper import _parse_path_format, _PathType
from azureml.dataprep.api._loggerfactory import _LoggerFactory


_logger = _LoggerFactory.get_logger('MLTableUtils')
_long_form_aml_uri = re.compile(
    r'^azureml://subscriptions/([^\/]+)/resourcegroups/([^\/]+)/'
    r'(?:providers/Microsoft.MachineLearningServices/)?workspaces/([^\/]+)/(.*)',
    re.IGNORECASE)


def _make_all_paths_absolute(mltable_yaml_dict, base_path, is_local=False):
    if base_path:
        if 'paths' in mltable_yaml_dict:
            for path_dict in mltable_yaml_dict['paths']:
                for path_prop, path in path_dict.items():
                    path_type, _, _ = _parse_path_format(path)
                    # get absolute path from base_path + relative path
                    if path_type == _PathType.local and not os.path.isabs(path):
                        # when path == '.' it represents the current dir, which is base_path ex) folder: .
                        path_dict[path_prop] = base_path if _path_is_current_directory_variant(path) else \
                            os.path.join(base_path, os.path.normpath(path))
                        # if base_path is local
                        if is_local:
                            path_dict[path_prop] = "file://" + path_dict[path_prop]
    return mltable_yaml_dict


def _path_is_current_directory_variant(path):
    cwd_variants = ['.', './', '.\\']
    if path in cwd_variants:
        return True
    return False


def _validate(mltable_yaml_dict):
    cwd = os.path.dirname(os.path.abspath(__file__))
    schema_path = "{}/schema/MLTable.json".format(cwd.rstrip("/"))
    with open(schema_path, "r") as stream:
        try:
            schema = json.load(stream)
        except json.decoder.JSONDecodeError:
            raise RuntimeError("MLTable json schema is not a valid json file.")
    try:
        validate(mltable_yaml_dict, schema)
    except Exception as e:
        _logger.warn("MLTable validation failed with error: {}".format(e.args))
        raise ValueError("Given MLTable does not adhere to the AzureML MLTable schema: {}".format(e.args))


# will switch to the api from dataprep package once new dataprep version is released
def _parse_workspace_context_from_longform_uri(uri):
    long_form_uri_match = _long_form_aml_uri.match(uri)

    if long_form_uri_match:
        return {
            'subscription': long_form_uri_match.group(1),
            'resource_group': long_form_uri_match.group(2),
            'workspace_name': long_form_uri_match.group(3)
        }

    return None
