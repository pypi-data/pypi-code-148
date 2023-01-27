# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Contains functionality to create and interact with MLTable objects
"""
import atexit
import os
import re
import yaml
from enum import Enum, auto
import random
import tempfile
import urllib.parse
import hashlib
import pathlib
from typing import List, Optional, Union

from azureml.dataprep.api._loggerfactory import track, _LoggerFactory
from azureml.dataprep.api._constants import ACTIVITY_INFO_KEY, ERROR_CODE_KEY, \
    COMPLIANT_MESSAGE_KEY, OUTER_ERROR_CODE_KEY
from azureml.dataprep.api._dataframereader import get_dataframe_reader, to_pyrecords_with_preppy, \
    _execute
from azureml.dataprep.api.mltable._mltable_helper import _read_yaml, _download_mltable_yaml, \
    _parse_path_format, _PathType, _is_tabular
from azureml.dataprep.rslex import PyRsDataflow
from ._aml_utilities._aml_rest_client_helper import _get_data_asset_by_id, _get_data_asset_by_asset_uri, \
    _try_resolve_workspace_info, _has_sufficient_workspace_info, STORAGE_OPTION_KEY_AZUREML_SUBSCRIPTION, \
    STORAGE_OPTION_KEY_AZUREML_RESOURCEGROUP, STORAGE_OPTION_KEY_AZUREML_WORKSPACE

from ._utils import _validate, _make_all_paths_absolute, _parse_workspace_context_from_longform_uri
from ._validation_and_error_handler import _get_and_validate_download_list, _classify_known_user_error_from_rslex
from azureml.dataprep.api.typeconversions import FieldType
from azureml.dataprep.api._rslex_executor import ensure_rslex_environment

_APP_NAME = 'MLTable'
_PUBLIC_API = 'PublicApi'
_INTERNAL_API = 'InternalCall'
_TRAITS_SECTION_KEY = 'traits'
_INDEX_COLUMNS_KEY = 'index_columns'
_TIMESTAMP_COLUMN_KEY = 'timestamp_column'
_TRAITS_SCHEMA_NAME = 'traits'
_METADATA_SCHEMA_NAME = 'metadata'
_logger = None

# keys for MLTable sections
_EXTRACT_PARTITION_FORMAT_KEY = 'extract_columns_from_partition_format'
_PARTITION_FORMAT_KEY = 'partition_format'
_PATHS_KEY = 'paths'
_METADATA_KEY = 'metadata'
_TRANSFORMATIONS_KEY = 'transformations'
_READ_DELIMITED_KEY = 'read_delimited'
_READ_JSON_KEY = 'read_json_lines'

_CONVERT_COLUMNS_TYPES_TYPE_ERROR = ValueError('`convert_column_types` must be a dictionary where '
                                               'key is Union[str, Tuple[str]] and '
                                               'value is :class: mltable.DataType')

_PERMISSION_DENIED_ERROR_MSG = 'ExecutionError(StreamError(PermissionDenied'

_SIMPLE_TYPES = {
    FieldType.INTEGER: 'int',
    FieldType.BOOLEAN: 'boolean',
    FieldType.STRING: 'string',
    FieldType.DECIMAL: 'float',
    FieldType.DATE: 'datetime',
    FieldType.STREAM: 'stream_info'
}


class MLTableHeaders(Enum):
    """
    Defines options for how column headers are processed when reading data
    from files to create a MLTable.

    These enumeration values are used in the MLTable class.
    """
    no_header = auto()  #: No column headers are read
    #: Read headers only from first row of first file, everything else is data.
    from_first_file = auto()
    #: Read headers from first row of each file, combining named columns.
    all_files_different_headers = auto()
    #: Read headers from first row of first file, drops first row from other files.
    all_files_same_headers = auto()

    @staticmethod
    def _parse(header):
        if isinstance(header, MLTableHeaders):
            return header

        if not isinstance(header, str):
            raise ValueError(
                'The header should be a string or an MLTableHeader enum')

        try:
            return MLTableHeaders[header.lower()]
        except KeyError:
            raise KeyError(f"Given invalid header {str(header)}, supported "
                           "headers are: 'no_header', 'from_first_file', "
                           "'all_files_different_headers', "
                           "and 'all_files_same_headers'.")


class MLTableFileEncoding(Enum):
    """
    Defines options for how encoding are processed when reading data from
    files to create a MLTable.

    These enumeration values are used in the MLTable class.
    """
    utf8 = auto()
    iso88591 = auto()
    latin1 = auto()
    ascii = auto()
    utf16 = auto()
    utf32 = auto()
    utf8bom = auto()
    windows1252 = auto()

    @staticmethod
    def _parse(encoding):
        if isinstance(encoding, MLTableFileEncoding):
            return encoding
        if not isinstance(encoding, str):
            raise ValueError(
                'The encoding should be a string or an MLTableFileEncoding enum')

        try:
            return MLTableFileEncoding[encoding.lower()]
        except KeyError:
            raise KeyError(
                f"Given invalid encoding '{encoding}', supported encodings "
                "are 'utf8', 'iso88591', 'latin1', 'ascii', 'utf16', "
                "'utf32', 'utf8bom' and 'windows1252'.")


class DataType:
    """
    Helper class for handling the proper manipulation of supported column types (int, bool, string, etc.).
    Currently used  with `MLTable.convert_column_types(...)` & `from_delimited_files(...)` for specifying which types
    to convert columns to. Different types are selected with `DataType.from_*(...)` methods.
    """

    _MISMATCH_AS_TYPES = ('error', 'true', 'false')

    @staticmethod
    def _from_raw(value):
        if isinstance(value, DataType):
            return value
        if value == 'string':
            return DataType.to_string()
        if value == 'int':
            return DataType.to_int()
        if value == 'float':
            return DataType.to_float()
        if value == 'boolean':
            return DataType.to_bool()
        if value == 'stream_info':
            return DataType.to_stream()
        raise ValueError("'{}' is not a supported string conversion for `mltable.DataType`, "
                         "supported types are 'string', 'int', 'float', 'boolean', & 'stream_info'".format(value))

    @staticmethod
    def _create(data_type):
        dt = DataType()
        dt._data_type = data_type
        dt._arguments = _SIMPLE_TYPES.get(data_type)
        return dt

    @staticmethod
    def _format_str_list(values, var_name):
        if values:
            if not isinstance(values, list):
                values = [values]
            if not all(isinstance(x, str) for x in values):
                raise ValueError(
                    '`{0}` must be a non-empty list of strings or None'.format(var_name))
            if len(values) == 0:
                values = None
        return values

    @staticmethod
    def to_string():
        """Configure conversion to string."""
        return DataType._create(FieldType.STRING)

    @staticmethod
    def to_int():
        """Configure conversion to 64-bit integer."""
        return DataType._create(FieldType.INTEGER)

    @staticmethod
    def to_float():
        """Configure conversion to 64-bit float."""
        return DataType._create(FieldType.DECIMAL)

    @staticmethod
    def to_bool(true_values: Optional[List[str]] = None,
                false_values: Optional[List[str]] = None,
                mismatch_as: Optional[str] = None):
        """Configure conversion to bool. `true_values` & `false_values` must both be None or non-empty lists of,
        string else an error will be thrown.

        :param true_values: List of values in dataset to designate as True.
            For example, ['1', 'yes'] will be replaced as [True, True].
            The true_values need to be present in the dataset otherwise None will be returned for values not present.
        :type true_values: builtin.list[str]

        :param false_values: List of values in dataset to designate as False.
            For example, ['0', 'no'] will be replaced as [False, False].
            The false_values need to be present in the dataset otherwise None will be returned for values not present.
        :type false_values: builtin.list[str]

        :param mismatch_as: How cast strings that are neither in `true_values` or `false_values`; 'true' casts all as
            True, 'false' as False, and 'error' will error instead of casting. Defaults to None which equal to 'error'.
        :type mismatch_as: Optional[str]
        """
        dt = DataType._create(FieldType.BOOLEAN)

        if mismatch_as is not None and mismatch_as not in DataType._MISMATCH_AS_TYPES:
            raise ValueError("`mismatch_as` can only be {}".format(
                DataType._MISMATCH_AS_TYPES))

        true_values = DataType._format_str_list(true_values, 'true_values')
        false_values = DataType._format_str_list(false_values, 'false_values')

        if (true_values is None) != (false_values is None):
            raise ValueError(
                '`true_values` and `false_values` must both be None or non-empty list of strings')

        if true_values is not None and false_values is not None \
                and (len(set(true_values).intersection(false_values)) > 0):
            raise ValueError(
                '`true_values` and `false_values` can not have overlapping values')

        type_name = dt._arguments
        args = {type_name: {}}
        if true_values and false_values:
            args[type_name]['true_values'] = true_values
            args[type_name]['false_values'] = false_values
            args[type_name]['mismatch_as'] = 'error'

        if mismatch_as:
            args[type_name]['mismatch_as'] = mismatch_as

        dt._arguments = args if args[type_name] else type_name
        return dt

    @staticmethod
    def to_stream():
        """Configure conversion to stream."""
        return DataType._create(FieldType.STREAM)

    @staticmethod
    def to_datetime(formats: Union[str, List[str]], date_constant: Optional[str] = None):
        """Configure conversion to datetime.

        :param formats: Formats to try for datetime conversion. For example `%d-%m-%Y` for data in "day-month-year",
            and `%Y-%m-%dT%H:%M:%S.%f` for "combined date and time representation" according to ISO 8601.

            * %Y: Year with 4 digits

            * %y: Year with 2 digits

            * %m: Month in digits

            * %b: Month represented by its abbreviated name in 3 letters, like Aug

            * %B: Month represented by its full name, like August

            * %d: Day in digits

            * %H: Hour as represented in 24-hour clock time

            * %I: Hour as represented in 12-hour clock time

            * %M: Minute in 2 digits

            * %S: Second in 2 digits

            * %f: Microsecond
            * %p: AM/PM designator

            * %z: Timezone, for example: -0700
        :type formats: str or builtin.list[str]

        :param date_constant: If the column contains only time values, a date to apply to the resulting DateTime.
        :type date_constant: Optional[str]
        """
        dt = DataType._create(FieldType.DATE)
        type_name = _SIMPLE_TYPES.get(FieldType.DATE)
        if not isinstance(formats, list):
            formats = [formats]
        _normalize_column_inputs(formats)
        dt._arguments = {type_name: {'formats': formats}}
        if date_constant is not None:
            dt._arguments[type_name]['date_constant'] = date_constant
        return dt


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


# force to flush app insights at exit
# logs might not be flushed to app insight because of app insight buffer
def _exit_handler():
    for handler in _get_logger().handlers:
        handler.flush()


atexit.register(_exit_handler)


def _normalize_column_inputs(columns, is_tuple=False):
    # Used to normalize columns into a list of strings or tuple of strings
    type_to_check = list if not is_tuple else tuple
    if isinstance(columns, str):
        return [columns] if type_to_check == list else columns
    elif isinstance(columns, type_to_check) and len(columns) > 0 and all(isinstance(col, str) for col in columns):
        return columns
    supported_types = {list: 'list', tuple: 'tuple'}
    raise ValueError(
        "'columns': {} should be a string or {} of strings with "
        "at least one element".format(columns, supported_types[type_to_check]))


def _check_no_duplicate_columns(cols):
    """
    Raises a ValueError is there are any duplicate columns in the given list of column groups (single of multiple
    columns.
    :param cols:
    :type cols: List[Union[str, Tuple[str]]]
    :return: None
    :rtype: None
    """
    seen_columns = set()
    for group in cols:
        if isinstance(group, str):
            group = (group,)

        for column in group:
            if column in seen_columns:
                raise ValueError("Found duplicate column. Cannot convert column '{}' to multiple `mltable.DataType`s."
                                 .format(column))

        seen_columns.update(group)


def _load_mltable_from_legacy_dataset(asset_id, storage_options=None):
    # only expect asset id in remote job in prod + local e2e test scenario
    asset = _get_data_asset_by_id(asset_id, storage_options)
    mltable_string = asset.legacy_dataflow
    if not mltable_string or mltable_string == '':
        raise RuntimeError(
            f'Data asset service returned invalid MLTable yaml for asset {asset_id}')

    return yaml.safe_load(mltable_string)


def _load_mltable_from_data_asset_uri(asset_uri_match, storage_options=None, enable_validation=True):
    # asset uri can be from local or remote
    data_asset = _get_data_asset_by_asset_uri(asset_uri_match, storage_options)
    is_v2 = data_asset.additional_properties['isV2']
    if is_v2:
        if data_asset.data_version.data_type != _APP_NAME:
            raise ValueError('Can only load MLTable type asset')
        local_path = _download_mltable_yaml(data_asset.data_version.data_uri)
        mltable_dict = _read_yaml(local_path)
        mltable_dict = _make_all_paths_absolute(
            mltable_dict, data_asset.data_version.data_uri)
        if enable_validation:
            _validate(mltable_dict)
        return mltable_dict

    mltable_string = data_asset.additional_properties['legacyDataflow']
    if not mltable_string:
        raise RuntimeError(f'Data asset service returned invalid MLTable '
                           f'YAML file for asset '
                           f'{asset_uri_match[3]}:{asset_uri_match[4]}')
    return yaml.safe_load(mltable_string)

@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def load(uri, storage_options: dict = None):
    """
    Loads the MLTable file(YAML) present at the given uri.

    .. remarks::

        There must be a valid MLTable YAML file named 'MLTable' present at
        the given uri.

        .. code-block:: python

            # load mltable from local folder
            from mltable import load
            tbl = load('.\\samples\\mltable_sample')

            # load mltable from azureml datastore uri
            from mltable import load
            tbl = load(
                'azureml://subscriptions/<subscription-id>/
                resourcegroups/<resourcegroup-name>/workspaces/<workspace-name>/
                datastores/<datastore-name>/paths/<mltable-path-on-datastore>/')

            # load mltable from azureml data asset uri
            from mltable import load
            tbl = load(
                  'azureml://subscriptions/<subscription-id>/
                  resourcegroups/<resourcegroup-name>/providers/Microsoft.MachineLearningServices/
                  workspaces/<workspace-name>/data/<data-asset-name>/versions/<data-asset-version>/')

    `storage_options` supports keys of 'subscription', 'resource_group',
    'workspace', or 'location'. All must locate an Azure machine learning
    workspace.

    :param uri: uri supports long-form datastore uri, storage uri, local path,
                or data asset uri
    :type uri: str
    :param storage_options: AML workspace info when URI is an AML asset
    :type storage_options: dict[str, str]
    :return: MLTable
    :rtype: mltable.MLTable
    """
    return _load(uri, storage_options, True)

@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def _load(uri, storage_options: dict = None, enable_validate = False):
    """
    Loads the MLTable file(YAML) present at the given uri. This is private api without validations compare to load()
    """
    custom_dimensions = {'app_name': _APP_NAME}
    workspace_context = _parse_workspace_context_from_longform_uri(uri)
    if workspace_context:
        custom_dimensions.update(workspace_context)

    with _LoggerFactory.track_activity(_get_logger(), 'load', _PUBLIC_API,
                                       custom_dimensions) as activityLogger:
        try:
            path_type, base_path, match = _parse_path_format(uri)
            is_local = False
            if path_type == _PathType.local:
                base_path = os.path.normpath(base_path)
                local_path = base_path
                is_local = True
                if not os.path.isabs(base_path):
                    local_path = os.path.join(os.getcwd(), base_path)
                mltable_dict = _read_yaml(local_path)
                if enable_validate:
                    _validate(mltable_dict)
            elif path_type == _PathType.cloud:
                local_path = _download_mltable_yaml(uri)
                mltable_dict = _read_yaml(local_path)
                if enable_validate:
                    _validate(mltable_dict)
            elif path_type == _PathType.legacy_dataset:
                # skip mltable yaml validation for v1 legacy dataset
                # because of some legacy schema generated in converter
                mltable_dict = _load_mltable_from_legacy_dataset(
                    uri, storage_options)
                # this is to skip path conversion logic, all paths will be absolute path
                base_path = None
            elif path_type == _PathType.data_asset_uri:
                mltable_dict = _load_mltable_from_data_asset_uri(
                    match, storage_options, enable_validate)
                # path has been mapped to absolute path in _load_mltable_from_data_asset_uri
                base_path = None
            else:
                raise ValueError('The uri should be a valid path to a local or cloud directory which contains an '
                                 'MLTable file.')
            # v1 sql dataset doesnt have paths
            orig_rel_paths = mltable_dict[_PATHS_KEY] if _PATHS_KEY in mltable_dict else None
            mltable_dict = _make_all_paths_absolute(
                mltable_dict, base_path, is_local)
            mltable_loaded = MLTable._create_from_dict(
                mltable_dict=mltable_dict, orig_paths=orig_rel_paths)
            workspace_context = _parse_workspace_context_from_longform_uri(uri)
            mltable_loaded._workspace_context = workspace_context

            _LoggerFactory.trace(_get_logger(), "load", workspace_context)

            return mltable_loaded
        except Exception as ex:
            if hasattr(activityLogger, ACTIVITY_INFO_KEY):
                activityLogger.activity_info['message'] = getattr(ex, COMPLIANT_MESSAGE_KEY, str(ex))
                activityLogger.activity_info['error_code'] = getattr(ex, ERROR_CODE_KEY, '')
                activityLogger.activity_info['outer_error_code'] = getattr(ex, OUTER_ERROR_CODE_KEY, '')

            if _PERMISSION_DENIED_ERROR_MSG in ex.args[0]:
                raise ValueError(ex.args[0])
            raise


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_delimited_files(paths, header='all_files_same_headers', delimiter=",", support_multi_line=False,
                         empty_as_string=False, encoding='utf8', include_path_column=False,
                         infer_column_types=True):
    """
    Creates an MLTable from given list of delimited files.

    .. remarks::

        There must be a valid paths string.

        .. code-block:: python

            # load mltable from local delimited file
            from mltable import from_delimited_files
            paths = '[{'file': "./samples/mltable_sample/sample_data.csv"}]'
            mltable = from_delimited_files(paths)

    :param paths: paths supports files or folders type with local or cloud path
    :type paths: list
    :param header: how column headers are handled when reading from files,
                   options specified using an enum value of
                   :class:`mltable.PromoteHeadersBehavior`, defaults to
                   `all_files_same_header`
    :type header: Union[str, mltable.MLTablePromoteHeadersBehavior]
    :param delimiter: separator used to split columns
    :type delimiter: str
    :param support_multi_line: By default (support_multi_line=False), all
                               line breaks, including those in quoted field
                               values, will be interpreted as a record break.
                               Reading data this way is faster and more
                               optimized for parallel execution on multiple
                               CPU cores. However, it may result in silently
                               producing more records with misaligned field
                               values. This should be set to True when the
                               delimited files are known to contain quoted
                               line breaks.

        .. remarks::

            Given this csv file as example, the data will be read differently
            based on support_multi_line.

                A,B,C
                A1,B1,C1
                A2,"B
                2",C2

            .. code-block:: python

                from mltable import from_delimited_files

                # default behavior: support_multi_line=False
                mltable = from_delimited_files(path)
                print(mltable.to_pandas_dataframe())
                #      A   B     C
                #  0  A1  B1    C1
                #  1  A2   B  None
                #  2  2"  C2  None

                # to handle quoted line breaks
                mltable = from_delimited_files(path, support_multi_line=True)
                print(mltable.to_pandas_dataframe())
                #      A       B   C
                #  0  A1      B1  C1
                #  1  A2  B\\r\\n2  C2

    If `empty_as_string` is True will read empty fields as empty strings, else
    read as nulls. If True and column contains datetime or numeric data, empty
    fields still read as nulls.

    Supported file encodings are 'utf8', 'iso88591', 'latin1', 'ascii',
    'utf16', 'utf32', 'utf8bom' and 'windows1252'.

    `include_path_column` is useful when reading multiple files and you want
    to know which file a particular record came from, or to keep useful
    information that may be stored in a file path.

    :type support_multi_line: bool
    :param empty_as_string: how empty fields should be handled
    :type empty_as_string: bool
    :param encoding: file encoding
    :type encoding: str
    :param include_path_column: keep path information as column in MLTable
    :type include_path_column: bool
    :param infer_column_types: If true, automatically infers all column types. If false, leaves columns as strings. If
        a dictionary, represents columns whose types are to be set to given types (with all other columns being
        inferred). The dictionary may contain a key named `sample_size` mapped to a positive integer number,
        representing the number of rows to use for inferring column types. The dictionary may also contain a key named
        `column_type_overrides` mapped dictionary. Each key in the dictionary is either a string representing a column
        name or a tuple of strings representing a group of column names. Each value is either a string (one of
        'boolean', 'string', 'float', 'int', or 'stream_info') or a `mltable.DataType`. If an empty dictionary is
        given, assumed to be True. Defaults to True.

        .. remarks::

            An example of how to format `infer_column_types`.

            .. code-block:: python

                from mltable import from_delimited_files

                # default behavior: support_multi_line=False
                mltable = from_delimited_files(paths, infer_column_types={
                    'sample_size': 100,
                    'column_type_overrides: {
                        'colA': 'boolean'
                        ('colB', 'colC'): DataType.to_int()
                    }
                })

    :type infer_column_types: Union[bool, dict[str, Union[str, dict[Union[Tuple[str], str], mltable.DataType]]]
    :return: MLTable object
    :return: MLTable
    :rtype: mltable.MLTable
    """
    mltable = from_paths(paths)
    header = MLTableHeaders._parse(header)
    encoding = MLTableFileEncoding._parse(encoding)

    if not isinstance(infer_column_types, (bool, dict)):
        raise ValueError(
            '`infer_column_types` must be a bool or a dictionary.')

    if isinstance(infer_column_types, dict):
        if not infer_column_types:
            infer_column_types = True
        elif len(set(infer_column_types) - set(['sample_size', 'column_type_overrides'])) > 0:
            raise ValueError('If `infer_column_types` is a dictionary, may only contain keys '
                             '`sample_size` and `column_type_overrides`.')
        elif 'sample_size' in infer_column_types \
                and not (isinstance(infer_column_types['sample_size'], int) and infer_column_types['sample_size'] > 0):
            raise ValueError('If `infer_column_types` is a dictionary with a `sample_size` key, '
                             'its value must be a positive integer.')
        elif 'column_type_overrides' in infer_column_types:
            if not isinstance(infer_column_types['column_type_overrides'], dict):
                raise ValueError('If `infer_column_types` is a dictionary with a `column_type_overrides` key, '
                                 'its value must be a dictionary of strings to `mltable.DataType`s or strings.')

            _check_no_duplicate_columns(
                infer_column_types['column_type_overrides'])
            overrides = []
            for k, v in infer_column_types['column_type_overrides'].items():
                if not (isinstance(k, str) or (isinstance(k, tuple) and all(isinstance(x, str) for x in k))):
                    raise ValueError('If `infer_column_types` is a dictionary with a `column_type_overrides` key,'
                                     'the keys in its dictionary value must be strings or tuples of strings.')

                v = DataType._from_raw(v)
                if not isinstance(v, DataType):
                    raise ValueError('If `infer_column_types` is a dictionary with a `column_type_overrides` key,'
                                     'the values in its dictionary value must be supported strings or '
                                     '`mltable.DataType`s.')

                overrides.append({'columns': k, 'column_type': v._arguments})

            infer_column_types['column_type_overrides'] = overrides

    return mltable._add_transformation_step(_READ_DELIMITED_KEY,
                                            {'delimiter': delimiter,
                                             'header': header.name,
                                             'support_multi_line': support_multi_line,
                                             'empty_as_string': empty_as_string,
                                             'encoding': encoding.name,
                                             'include_path_column': include_path_column,
                                             'infer_column_types': infer_column_types})


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_parquet_files(paths, include_path_column=False):
    """
    Create the MLTable from the given list of parquet files.

    .. remarks::

        There must be a valid paths dictionary

        .. code-block:: python

            # load mltable from local parquet paths
            from mltable import from_parquet_files
            paths = '[{'file': "./samples/mltable_sample/sample.parquet"}]'
            mltable = from_parquet_files(paths)

    `include_path_column` is useful when reading multiple files and you want
    to know which file a particular record came from, or to keep useful
    information that may be stored in a file path.

    :param paths: paths supports files or folders type with local or cloud path
    :type paths: list
    :param include_path_column: if True keeps path information as column
    :type include_path_column: bool
    :return: MLTable
    :rtype: mltable.MLTable
    """
    mltable = from_paths(paths)
    return mltable._add_transformation_step('read_parquet', {"include_path_column": include_path_column})


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_json_lines_files(paths, invalid_lines="error", encoding="utf8", include_path_column=False):
    """
    Create the MLTable from the given list of JSON file paths.

    .. remarks::

        There must be a valid paths dictionary

        .. code-block:: python

            # load mltable from local parquet paths
            from mltable import from_json_lines_files
            paths = '[{'file': "./samples/mltable_sample/sample_data.jsonl"}]'
            mltable = from_json_lines_files(paths)

    `include_path_column` is useful when reading multiple files and you want
    to know which file a particular record came from, or to keep useful
    information that may be stored in a file path.

    Supported file encodings are 'utf8', 'iso88591', 'latin1', 'ascii',
    'utf16', 'utf32', 'utf8bom' and 'windows1252'.

    :param paths: paths supports files or folder type with local or cloud path
    :type paths: list
    :param invalid_lines: How to handle lines that are invalid JSON. it can be 'drop' or 'error'.
        If its 'drop', it just drop invalid lines, otherwise it will fail. Default to error.
    :type invalid_lines: str
    :param encoding: Specify the file encoding. Supported encodings are 'utf8', 'iso88591', 'latin1', 'ascii',
        'utf16', 'utf32', 'utf8bom' and 'windows1252'
    :type encoding: str
    :param include_path_column: keep path information as acolumn
    :type include_path_column: bool
    :return: MLTable
    :rtype: mltable.MLTable
    """
    mltable = from_paths(paths)

    if invalid_lines not in ['error', 'drop']:
        raise ValueError(
            "Invalid value for invalid_lines, the supported values are ['error', 'drop']")

    encoding = MLTableFileEncoding._parse(encoding)
    return mltable._add_transformation_step(_READ_JSON_KEY,
                                            {"invalid_lines": invalid_lines,
                                             "encoding": encoding.name,
                                             "include_path_column": include_path_column})


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_paths(paths):
    """
    Create the MLTable from the given paths.

    .. remarks::

        There must be a valid paths dictionary

        .. code-block:: python

            # load mltable from local paths
            from mltable import from_paths
            tbl = from_paths([{'file': "./samples/mltable_sample"}])

            # load mltable from cloud paths
            from mltable import load
            tbl = from_paths(
                [{'file': "https://<blob-storage-name>.blob.core.windows.net/<path>/sample_file"}])


    :param paths: paths supports file or folder type with local or cloud path
    :type paths: list
    :return: MLTable
    :rtype: mltable.MLTable
    """
    import copy
    original_path = copy.deepcopy(paths)
    mltable_yaml_dict = {_PATHS_KEY: paths}
    for path_dict in mltable_yaml_dict[_PATHS_KEY]:
        for path_prop, path in path_dict.items():
            path_type, local_path, _ = _parse_path_format(path)
            if path_type == _PathType.local and not local_path.startswith('file://'):
                path_dict[path_prop] = 'file://' + os.path.abspath(local_path)
    _validate(mltable_yaml_dict)
    return MLTable._create_from_dict(mltable_dict=mltable_yaml_dict, orig_paths=original_path)


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_delta_lake(delta_table_uri, timestamp_as_of=None, version_as_of=None, include_path_column=False):
    """Creates an MLTable object to read in Parquet files from delta lake table.

    .. remarks::

        **from_delta_lake** creates an MLTable object which defines the operations to
        load data from delta lake folder into tabular representation.

        For the data to be accessible by Azure Machine Learning, `path` must point to the delta table directory
        and the delta lake files that are referenced must be accessible by AzureML services or behind public web urls.

        **from_delta_lake** supports reading delta lake data from a uri
        pointing to: local path, Blob, ADLS Gen1 and ADLS Gen2

        Users are able to read in and materialize the data by calling `to_pandas_dataframe()` on the returned MLTable

        .. code-block:: python

            # create an MLTable object from a delta lake using timestamp versioning and materialize the data
            from mltable import from_delta_lake
            mltable_ts = from_delta_lake(delta_table_uri="./data/delta-01", timestamp_as_of="2021-05-24T00:00:00Z")
            pd = mltable_ts.to_pandas_dataframe()

            # create  an MLTable object from a delta lake using integer versioning and materialize the data
            from mltable import from_delta_lake
            mltable_version = from_delta_lake(delta_table_uri="./data/delta-02", version_as_of=1)
            pd = mltable_version.to_pandas_dataframe()

    :param delta_table_uri: URI pointing to the delta table directory containing the delta lake parquet files to read.
        Supported URI types are: local path URI, storage URI, long-form datastore URI, or data asset uri.
    :type delta_table_uri: str
    :param timestamp_as_of: datetime string in RFC-3339/ISO-8601 format to use to read in matching parquet files
        from a specific point in time.
        ex) "2022-10-01T00:00:00Z", "2022-10-01T00:00:00+08:00", "2022-10-01T01:30:00-08:00"
    :type timestamp_as_of: string
    :param version_as_of: integer version to use to read in a specific version of parquet files.
    :type version_as_of: int
    :param include_path_column: Boolean to keep path information as column in the mltable. Defaults to False.
        This is useful when reading multiple files, and want to know which file a particular record
        originated from, or to keep useful information in file path.
    :type include_path_column: bool
    :return: MLTable object
    :rtype: mltable.MLTable
    """
    if timestamp_as_of and version_as_of:
        raise KeyError("Both timestamp_as_of and version_as_of parameters were provided, but only one of version_as"
                       "_of or timestamp_as_of can be specified.")

    if timestamp_as_of:
        rfc3339_checker = re.compile(r'^((?:(\d{4}-(0[1-9]|1[0-2])-([0-3]\d))'
                                     r'T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)$')
        if rfc3339_checker.match(timestamp_as_of) is None:
            raise ValueError('Provided timestamp_as_of: {} is not in RFC-3339/ISO-8601 format. Please make sure '
                             'that it adheres to RFC-3339/ISO-8601 format. For example: "2022-10-01T00:00:00Z",'
                             '"2022-10-01T22:10:57+02:00", "2022-10-01T16:32:11.8+00:00" are correctly formatted.')

    mltable = from_paths([{"folder": delta_table_uri}])
    return mltable._add_transformation_step('read_delta_lake',
                                            {'version_as_of': version_as_of,
                                             'timestamp_as_of': timestamp_as_of,
                                             'include_path_column': include_path_column})


class MLTable:
    """
    Represents a MLTable.

    A MLTable defines a series of lazily-evaluated, immutable operations to
    load data from the data source. Data is not loaded from the source until
    MLTable is asked to deliver data.
    """

    def __init__(self):
        """
        Initialize a new MLTable.

        This constructor is not supposed to be invoked directly. MLTable is
        intended to be created using :func:`mltable.load`.
        """
        self._loaded = False

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def __repr__(self):
        """
        Returns all the information associated with MLTable as a YAML-style
        string representation.

        :return: string representation of this MLTable
        :rtype: str
        """
        return self._dataflow.to_yaml_string()

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def validate(self):
        """
        Validates if this MLTable's data can be loaded, requires the MLTable's
        data source(s) to be accessible from the current compute.

        :return: None
        :rtype: None
        """
        failed_to_load_error_msg = \
            'Can not load data from this MLTable\'s associated datastores. Please check the associated paths.'

        mltable_yaml_str = self.take(1)._dataflow.to_yaml_string()
        try:
            records = to_pyrecords_with_preppy(
                'MLTable.validate', mltable_yaml_str)
        except Exception as e:  # this is too broad, but dataprepreader throws different errors
            raise ValueError(
                f'{failed_to_load_error_msg} Additional error info: "{e}"')

        if len(records) < 1:
            raise ValueError(failed_to_load_error_msg)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _ensure_random_seed(self, seed):
        """
        If the given seed is not an integer or None, raises a ValueError. If
        None selects a random seed randomly between 1 and 1000.

        :param seed: possible value for random seed
        :type seed: object
        :return: valid random seed
        :rtype: int
        """
        if seed is None:
            return random.randint(1, 1000)
        elif not isinstance(seed, int):
            raise ValueError('A random seed must be an integer')
        return seed

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _check_loaded(self):
        if not self._loaded:
            raise ValueError('MLTable does not appear to be loaded correctly. '
                             'Please use MLTable.load() to load a MLTable YAML'
                             ' file into memory.')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _sanitize_and_check_datatype(self, column_types):
        # Function used to type check the inputs for convert_column_types API
        if len(column_types) == 0 or not isinstance(column_types, dict):
            raise ValueError(
                'Input type is dict[Union[str, Tuple[str]]: mltable.DataType] with at least one entry')

        _check_no_duplicate_columns(
            [_normalize_column_inputs(x, is_tuple=True) for x in column_types])
        for conversion in column_types.values():
            if not isinstance(conversion, DataType):
                raise _CONVERT_COLUMNS_TYPES_TYPE_ERROR

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _add_transformation_step(self, step, args, index=None):
        """
        Adds the given transformation step and its associated arguments to
        this MLTable's PyRsDataflow at the given index in the list of all
        added transformation steps. Returns a new MLTable whose PyRsDataflow
        is the PyRsDataflow resulting from the prior addition.

        :param step: transformation step
        :type step: str
        :param args: arguments for given transformation step
        :type: object
        :param index: optional argument to indicate which index to add the step
        :type: int
        :return: MLTable with resulting PyRsDataflow
        :rtype: mltable.MLTable
        """
        new_dataflow = self._dataflow.add_transformation(step, args, index)
        return MLTable._create_from_dataflow(new_dataflow, self.paths)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _normalize_partition_int_list(self, columns):
        if isinstance(columns, int):
            return [columns]
        elif isinstance(columns, list) and len(columns) > 0 \
                and all(isinstance(index, int) for index in columns):
            return columns
        raise ValueError(
            'Columns should be a int or list of int with at least one element')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _get_columns_in_traits(self):
        """
        Gets all the columns that are set in this MLTable's Traits.

        :return: set of all Traits
        :rtype: set[str]
        """
        columns_in_traits = set()
        if self.traits:
            timestamp_col = self.traits._check_and_get_trait(
                _TIMESTAMP_COLUMN_KEY)
            if timestamp_col is not None:
                columns_in_traits.add(timestamp_col)

            index_cols = self.traits._check_and_get_trait(_INDEX_COLUMNS_KEY)
            if index_cols is not None:
                columns_in_traits.update(index_cols)

        return columns_in_traits

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _download(self, stream_column=None, target_path=None, ignore_not_found=False, storage_options=None):
        if target_path is None:
            from tempfile import mkdtemp
            target_path = mkdtemp()

        if stream_column is None:
            stream_column = 'Path'

        if stream_column != 'Path':
            new_mltable = self._add_transformation_step('rename_columns', {stream_column: 'Path'})
        else:
            new_mltable = MLTable._create_from_dataflow(self._dataflow, None)

        function_source_str = '{"r":["Function",[[],{"r":[]},{"r":["Function",[["row"],{"r":[]},' \
                              '{"r":["Invoke",[{"r":["Identifier","GetPortablePath"]},' \
                              '[{"r":["RecordField",[{"r":["Identifier","row"]},"Path"]]},""]]]}]]}]]}'
        new_mltable = new_mltable._add_transformation_step('add_columns',
                                                           {
                                                               'language': 'Native',
                                                               'expressions':
                                                                   [
                                                                       {
                                                                           'new_column': 'Portable Path',
                                                                           'prior_column': 'Path',
                                                                           'function_source': function_source_str
                                                                       }
                                                                   ]
                                                           })

        new_mltable = new_mltable._add_transformation_step('write_streams_to_files',
                                                           {
                                                               'streams_column': 'Path',
                                                               'destination':
                                                                   {
                                                                       'directory': str(target_path),
                                                                       'handler': 'Local'
                                                                   },
                                                               'file_names_column': 'Portable Path'
                                                           })

        # append workspace information for the stream_column for backwards support
        # AmlDatastore://workspaceblobstore/data/images/animals folder/1d.jpg
        workspace_info = _try_resolve_workspace_info(storage_options)
        if _has_sufficient_workspace_info(workspace_info):
            new_mltable = \
                MLTable._append_workspace_to_stream_info_conversion(new_mltable, workspace_info, stream_column)

        mltable_yaml_str = new_mltable._dataflow.to_yaml_string()
        try:
            download_records = to_pyrecords_with_preppy('MLTable._download', mltable_yaml_str)
            actual_download_list = _get_and_validate_download_list(download_records, ignore_not_found, _get_logger())
            return actual_download_list
        except Exception as ex:
            _classify_known_user_error_from_rslex(ex.args[0])

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _with_partition_size(self, min_batch_size):
        """
        Update a transformation step to use the partition size of defined. Support delimited files and json files.

        :param min_batch_size: minimum batch size to partition the data
        :type min_batch_size: int
        :return: MLTable with partition size updated
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        orig_paths = self.paths
        mltable_yaml_str = self._dataflow.to_yaml_string()
        mltable_yaml_dict = yaml.safe_load(mltable_yaml_str)
        support_transformations = [_READ_DELIMITED_KEY, _READ_JSON_KEY]
        for key in support_transformations:
            if key in mltable_yaml_dict[_TRANSFORMATIONS_KEY][0]:
                mltable_yaml_dict[_TRANSFORMATIONS_KEY][0][key]['partition_size'] = min_batch_size
                break
        else:
            raise ValueError('transformation step read_delimited or read_json_lines is required to update '
                             'partition_size')
        return MLTable._create_from_dict(mltable_dict=mltable_yaml_dict, orig_paths=orig_paths)

    def to_pandas_dataframe(self):
        """
        Load all records from the paths specified in the MLTable file into a
        Pandas DataFrame.

        .. remarks::

            The following code snippet shows how to use the
            to_pandas_dataframe api to obtain a pandas dataframe corresponding
            to the provided MLTable.

            .. code-block:: python

                from mltable import load
                tbl = load('.\\samples\\mltable_sample')
                pdf = tbl.to_pandas_dataframe()
                print(pdf.shape)

        :return: Pandas Dataframe containing the records from paths in this
                 MLTable
        :rtype: pandas.DataFrame
        """
        custom_dimensions = {'app_name': _APP_NAME}
        if self._workspace_context:
            custom_dimensions.update(self._workspace_context)

        with _LoggerFactory.track_activity(_get_logger(), 'to_pandas_dataframe', _PUBLIC_API,
                                           custom_dimensions) as activityLogger:
            try:
                self._check_loaded()
                try:
                    mltable_yaml_str = self._dataflow.to_yaml_string()
                    dataframe_reader = get_dataframe_reader()
                    df = dataframe_reader.to_pandas_dataframe(mltable_yaml_str)
                    return df
                except Exception as e:
                    message = e.args[0]
                    if "Python expression parse error" in message:
                        raise ValueError(
                            "Not a valid python expression in filter") from e
                    elif _PERMISSION_DENIED_ERROR_MSG in e.args[0]:
                        raise ValueError(e.args[0])
                    raise
            except Exception as e:
                if hasattr(activityLogger, ACTIVITY_INFO_KEY):
                    activityLogger.activity_info['error_code'] = getattr(
                        e, ERROR_CODE_KEY, '')
                    activityLogger.activity_info['message'] = getattr(
                        e, COMPLIANT_MESSAGE_KEY, str(e))
                    activityLogger.activity_info['outer_error_code'] = getattr(
                        e, OUTER_ERROR_CODE_KEY, '')

                raise e

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def get_partition_count(self) -> int:
        """
        Calculates the partitions for the current mltable and returns their count.

        :return: The count of partitions.
        """
        mltable_yaml_str = self._dataflow.to_yaml_string()
        from azureml.dataprep.api._dataframereader import get_partition_count_with_rslex
        return get_partition_count_with_rslex(mltable_yaml_str)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def select_partitions(self, partition_index_list):
        """
        Adds a transformation step to select the partition.

        .. remarks::

            The following code snippet shows how to use the select_partitions api to selected partitions
            from the provided MLTable.

            .. code-block:: python

                partition_index_list = [1, 2]
                mltable = mltable.select_partitions(partition_index_list)

        :param partition_index_list: list of partition index
        :type partition_index_list: list of int
        :return: MLTable with partition size updated
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        partition_index_list = self._normalize_partition_int_list(
            partition_index_list)
        return self._add_transformation_step('select_partitions', partition_index_list)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def extract_columns_from_partition_format(self, partition_format):
        """
        Adds a transformation step to use the partition information of each path and extract them into columns
        based on the specified partition format.

        Format part '{column_name}' creates string column, and '{column_name:yyyy/MM/dd/HH/mm/ss}' creates
        datetime column, where 'yyyy', 'MM', 'dd', 'HH', 'mm' and 'ss' are used to extract year, month, day,
        hour, minute and second for the datetime type.

        The format should start from the position of first partition key until the end of file path.
        For example, given the path '/Accounts/2019/01/01/data.csv' where the partition is by department name
        and time, partition_format='/{Department}/{PartitionDate:yyyy/MM/dd}/data.csv'
        creates a string column 'Department' with the value 'Accounts' and a datetime column 'PartitionDate'
        with the value '2019-01-01'.

        :param partition_format: Partition format to use to extract data into columns
        :type partition_format: str
        :return: MLTable whose partition format is set to given format
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        return self._add_transformation_step('extract_columns_from_partition_format',
                                             {_PARTITION_FORMAT_KEY: partition_format},
                                             0)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _get_partition_key_values(self, partition_keys=None):
        """Return unique key values of partition_keys.

        validate if partition_keys is a valid subset of full set of partition keys, return unique key values of
        partition_keys, default to return the unique key combinations by taking the full set of partition keys of this
        dataset if partition_keys is None

        .. code-block:: python

            # get all partition key value pairs
            partitions = mltable.get_partition_key_values()
            # Return [{'country': 'US', 'state': 'WA', 'partition_date': datetime('2020-1-1')}]

            partitions = mltable.get_partition_key_values(['country'])
            # Return [{'country': 'US'}]

        :param partition_keys: partition keys
        :type partition_keys: builtin.list[str]
        """
        self._check_loaded()
        if not partition_keys:
            partition_keys = self.partition_keys
        if not self.partition_keys:
            raise Exception("cannot retrieve partition key values for a mltable that has no "
                            "partition keys")

        invalid_keys = [
            x for x in partition_keys if x not in self.partition_keys]
        if len(invalid_keys) != 0:
            raise ValueError(f"{invalid_keys} are invalid partition keys")

        # currently use summarize to find the distinct result
        mltable = self.take(count=1)
        pd = mltable.to_pandas_dataframe()
        no_partition_key_columns = [
            x for x in pd.columns if x not in partition_keys]
        mltable = self
        if len(no_partition_key_columns) > 0:
            mltable = mltable._add_transformation_step('summarize',
                                                       {"aggregates":
                                                        [{"source_column": no_partition_key_columns[0],
                                                          "aggregate": "count",
                                                          "new_column": "new_count"}],
                                                        "group_by": partition_keys})
        mltable = mltable.keep_columns(partition_keys)
        # need to implement distinct from rlex https://msdata.visualstudio.com/Vienna/_workitems/edit/1749317
        # mltable = self.distinct_rows()
        pd = mltable.to_pandas_dataframe()
        pd = pd.drop_duplicates()
        partition_key_values = pd.to_dict(
            orient='records') if pd.shape[0] != 0 else []
        return partition_key_values

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def filter(self, expression):
        """
        Filter the data, leaving only the records that match the specified expression.

        .. remarks::

            Expressions are started by indexing the mltable with the name of a column. They support a variety of
                functions and operators and can be combined using logical operators. The resulting expression will be
                lazily evaluated for each record when a data pull occurs and not where it is defined.

            .. code-block:: python

                filtered_mltable = mltable.filter('feature_1 == \"5\" and target > \"0.5)\"')
                filtered_mltable = mltable.filter('col("FBI Code") == \"11\"')

        :param expression: The expression to evaluate.
        :type expression: string
        :return: MLTable after filter
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        return self._add_transformation_step('filter', expression)

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def paths(self):
        """
        Returns a list of dicts containing paths specified in the MLTable.

        :return: list of dicts containing paths specified in the MLTable
        :rtype: list[dict]
        """
        self._check_loaded()
        return self._orig_paths

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def partition_keys(self):
        """Return the partition keys.

        :return: the partition keys
        :rtype: builtin.list[str]
        """
        self._check_loaded()

        def parse_partition_format(partition_format):
            date_parts = ['yyyy', 'MM', 'dd', 'HH', 'mm', 'ss']
            date_part_map = {d: '_sys_{}'.format(d) for d in date_parts}
            defined_date_parts = []
            date_column = None
            columns = []
            i = 0
            pattern = ''
            while i < len(partition_format):
                c = partition_format[i]
                if c == '/':
                    pattern += '\\/'
                elif partition_format[i:i + 2] in ['{{', '}}']:
                    pattern += c
                    i += 1
                elif c == '{':
                    close = i + 1
                    while close < len(partition_format) and partition_format[close] != '}':
                        close += 1
                    key = partition_format[i + 1:close]
                    if ':' in key:
                        date_column, date_format = key.split(':')
                        for date_part in date_parts:
                            date_format = date_format.replace(
                                date_part, '{' + date_part_map[date_part] + '}')
                        partition_format = partition_format[:i] + \
                            date_format + partition_format[close + 1:]
                        continue
                    else:
                        found_date = False
                        for k, v in date_part_map.items():
                            if partition_format.startswith(v, i + 1):
                                pattern_to_add = '(?<{}>\\d{{{}}})'.format(
                                    v, len(k))
                                if pattern_to_add in pattern:
                                    pattern += '(\\d{{{}}})'.format(len(k))
                                else:
                                    pattern += pattern_to_add
                                    defined_date_parts.append(k)
                                found_date = True
                                break

                        if not found_date:
                            pattern_to_add = '(?<{}>[^\\.\\/\\\\]+)'.format(key)
                            if pattern_to_add in pattern:
                                pattern += '([^\\.\\/\\\\]+)'
                            else:
                                columns.append(key)
                                pattern += pattern_to_add
                        i = close
                elif c == '*':
                    pattern += '(.*?)'
                elif c == '.':
                    pattern += '\\.'
                else:
                    pattern += c
                i += 1
            if date_column is not None:
                columns.append(date_column)

            if defined_date_parts and 'yyyy' not in defined_date_parts:
                raise ValueError(
                    f'Invalid partition_format "{partition_format}". {validation_error["NO_YEAR"]}')
            return pattern, defined_date_parts, columns

        if len(self._partition_keys) > 0:
            return self._partition_keys
        mltable_yaml_str = self._dataflow.to_yaml_string()
        mltable_dict = yaml.safe_load(mltable_yaml_str)
        if _TRANSFORMATIONS_KEY in mltable_dict:
            for mltable_transformation in mltable_dict[_TRANSFORMATIONS_KEY]:
                if _EXTRACT_PARTITION_FORMAT_KEY in mltable_transformation:
                    parsed_result = parse_partition_format(
                        mltable_transformation[_EXTRACT_PARTITION_FORMAT_KEY][_PARTITION_FORMAT_KEY])
                    if len(parsed_result) == 3 and parsed_result[2]:
                        self._partition_keys = parsed_result[2]
                        return parsed_result[2]
        return []

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _is_tabular(self):
        """
        check if this mltable is tabular using its yaml
        """
        self._check_loaded()
        mltable_yaml_str = self._dataflow.to_yaml_string()
        mltable_yaml = yaml.safe_load(mltable_yaml_str)
        return _is_tabular(mltable_yaml)

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create_from_dict(mltable_dict, orig_paths):
        """
        Creates a new MLTable from a dictionary containing information from
        a MLTable file.

        :param mltable_dict: MLTable dict to read from
        :type mltable_dict: dict
        :param orig_paths: paths (relative or absolute) contained in the given
                           MLTable
        :type orig_paths: list[str]
        :return: MLTable from given dict
        :rtype: mltable.MLTable
        """
        mltable_yaml_string = yaml.dump(mltable_dict)
        dataflow = PyRsDataflow(mltable_yaml_string)
        return MLTable._create_from_dataflow(dataflow, orig_paths)

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create_from_dataflow(dataflow, orig_paths):
        """
        Creates a new MLTable from a PyRsDataflow.

        :param new_dataflow: PyRsDataflow to read from
        :type new_dataflow: PyRsDataflow
        :param orig_paths: paths (relative or absolute) contained in the
                           MLTable given Dataflow is based on
        :type orig_paths: list[str]
        :return: MLTable from given PyRsDataflow
        :rtype: mltable.MLTable
        """
        new_mltable = MLTable()
        new_mltable._dataflow = dataflow
        new_mltable._loaded = True
        new_mltable._orig_paths = orig_paths
        new_mltable._partition_keys = []
        new_mltable.traits = Traits._create(new_mltable)
        new_mltable.metadata = Metadata._create(new_mltable)
        new_mltable._workspace_context = None
        return new_mltable

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _append_workspace_to_stream_info_conversion(mltable, workspace_info, stream_column):
        def _is_stream_column_in_column_conversion(columns_item):
            return 'stream_info' == columns_item['column_type']\
                   and ((isinstance(columns_item['columns'], str) and columns_item['columns'] == stream_column)
                        or (isinstance(columns_item['columns'], list) and stream_column in columns_item['columns']))

        mltable_dict = yaml.safe_load(mltable._dataflow.to_yaml_string())
        if _TRANSFORMATIONS_KEY in mltable_dict:
            columns_conversion_list = [columns_item for t in mltable_dict[_TRANSFORMATIONS_KEY]
                                       for k, v in t.items()
                                       if k == 'convert_column_types'
                                       for columns_item in v
                                       if _is_stream_column_in_column_conversion(columns_item)]
            if len(columns_conversion_list) == 0:
                raise ValueError(f'stream_column {stream_column} is not converted to stream_info type')

            for columns in columns_conversion_list:
                columns['column_type'] = {
                    'stream_info': {
                        'subscription': workspace_info[STORAGE_OPTION_KEY_AZUREML_SUBSCRIPTION],
                        'resource_group': workspace_info[STORAGE_OPTION_KEY_AZUREML_RESOURCEGROUP],
                        'workspace_name': workspace_info[STORAGE_OPTION_KEY_AZUREML_WORKSPACE],
                        'escaped': False
                    }
                }
            return MLTable._create_from_dict(mltable_dict,
                                             mltable_dict[_PATHS_KEY]
                                             if _PATHS_KEY in mltable_dict else None)

        # else skip update
        return mltable

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def take(self, count=20):
        """
        Adds a transformation step to select the first `count` rows of this
        MLTable.

        :param count: number of rows from top of table to select
        :type count: int
        :return: MLTable with added "take" transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        if not (isinstance(count, int) and count > 0):
            raise ValueError('Number of rows must be a positive integer')
        return self._add_transformation_step('take', count)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def show(self, count=20):
        """
        Retrieves the first `count` rows of this MLTable as a Pandas Dataframe.

        :param count: number of rows from top of table to select
        :type count: int
        :return: first `count` rows of the MLTable
        :rtype: Pandas Dataframe
        """
        return self.take(count).to_pandas_dataframe()

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def take_random_sample(self, probability, seed=None):
        """
        Adds a transformation step to randomly select each row of this MLTable
        with `probability` chance. Probability must be in range [0, 1]. May
        optionally set a random seed.

        :param probability: chance that each row is selected
        :type: probability: float
        :param seed: optional random seed
        :type seed: Optional[int]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        if not (isinstance(probability, float) and 0 < probability < 1):
            raise ValueError(
                'Probability should an float greater than 0 and less than 1')
        seed = self._ensure_random_seed(seed)
        return self._add_transformation_step('take_random_sample',
                                             {"probability": probability,
                                              "seed": seed})

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def drop_columns(self, columns: Union[str, List[str]]):
        """
        Adds a transformation step to drop desired columns from the dataset.

        If a timeseries column is dropped, the corresponding capabilities will
        be dropped for the returned MLTable.

        :param columns: The name or a list of names for the columns to drop
        :type columns: Union[str, builtin.list[str]]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        columns = _normalize_column_inputs(columns)
        columns_in_traits = self._get_columns_in_traits()
        if not columns_in_traits.isdisjoint(columns):
            raise ValueError(
                'Columns in traits must be kept and cannot be dropped')
        return self._add_transformation_step('drop_columns', columns)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def keep_columns(self, columns: Union[str, List[str]]):
        """
        Adds a transformation step to keep the specified columns and drop all
        others from the dataset.

        If a timeseries column is dropped, the corresponding capabilities will
        be dropped for the returned MLTable.

        :param columns: The name or a list of names for the columns to keep
        :type columns: Union[str, builtin.list[str]]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        columns = _normalize_column_inputs(columns)
        columns_in_traits = self._get_columns_in_traits()
        if not columns_in_traits.issubset(columns):
            raise ValueError(
                'Columns in traits must be kept and cannot be dropped')
        return self._add_transformation_step('keep_columns', columns)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def random_split(self, percent=.5, seed=None):
        """
        Randomly splits this MLTable into two MLTables, one having
        approximately "percent"% of the original MLTable's data and the other
        having the remainder (1-"percent"%).

        :param percent: percent of the MLTable to split between
        :type percent: Union[int, float]
        :param seed: optional random seed
        :type seed: Optional[int]
        :return: two MLTables with this MLTable's data split between them by
                 "percent"
        :rtype: Tuple[mltable.MLTable, mltable.MLTable]
        """
        if not (isinstance(percent, float) and 0 < percent < 1):
            raise ValueError(
                'Percent should be a float greater than 0 and less than 1')
        seed = self._ensure_random_seed(seed)
        split_a = self._add_transformation_step('sample', {"sampler": "random_percent",
                                                           "sampler_arguments": {
                                                               "probability": percent,
                                                               "probability_lower_bound": 0.0,
                                                               "seed": seed}})
        split_b = self._add_transformation_step('sample', {"sampler": "random_percent",
                                                           "sampler_arguments": {
                                                               "probability": 1.0,
                                                               "probability_lower_bound": percent,
                                                               "seed": seed}})
        return split_a, split_b

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def save(self, path, overwrite=True):
        """
        Save this MLTable as a MLTable YAML file at the given local directory
        path.

        Raises a ValueError if given directory points to a file. If the path
        points to a directory with an existing MLTable YAML file, also raises
        a ValueError unless `overwrite` is set to False.

        :param path: directory path to save to
        :type path: str
        :param overwrite: overwrites an existing MLTable YAML file if present
        :return: None
        :rtype: None
        """
        self._check_loaded()
        path = os.path.abspath(path)

        if os.path.isfile(path):
            raise ValueError(f'The given path {path} points to a file.')

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        save_path = os.path.join(path, 'MLTable')
        if not overwrite and os.path.exists(save_path):
            raise ValueError(f'The given directory path {path} already '
                             'contains an MLTable YAML file.')

        mltable_yaml_dict = yaml.safe_load(self._dataflow.to_yaml_string())
        mltable_yaml_dict[_PATHS_KEY] = self.paths
        with open(save_path, 'w') as f:
            yaml.dump(mltable_yaml_dict, f)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def skip(self, count):
        """
        Adds a transformation step to skip the first `count` rows of this
        MLTable.

        :param count: number of rows to skip
        :type count: int
        :return: MLTable with added transformation step
        :type: mltable.MLTable
        """
        self._check_loaded()
        if not isinstance(count, int) or count < 1:
            raise ValueError('Count must be an integer > 0.')
        return self._add_transformation_step('skip', count)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def convert_column_types(self, column_types):
        """
        Adds a transformation step to convert the specified columns into their respective specified new types.

        :param column_types: Dictionary of column: types the user desires to convert
        :type column_types: dict[str, mltable.DataType]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable

        .. code-block:: python

            from mltable import DataType
                data_types = {
                    'ID': DataType.to_string(),
                    'Date': DataType.to_datetime('%d/%m/%Y %I:%M:%S %p'),
                    'Count': DataType.to_int(),
                    'Latitude': DataType.to_float(),
                    'Found': DataType.to_bool(),
                    'Stream': DataType.to_stream()
                }
        """
        self._check_loaded()
        self._sanitize_and_check_datatype(column_types)
        return self._add_transformation_step('convert_column_types',
                                             [{'columns': col,
                                               'column_type': converter._arguments
                                               } for col, converter in column_types.items()])

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _mount(self, stream_column="Path", mount_point=None, **kwargs):
        """Create a context manager for mounting file streams defined by the mltable as local files.

        .. remarks::

            A context manager will be returned to manage the lifecycle of the mount. To mount, you will need to
            enter the context manager and to unmount, exit from the context manager.

            Mount is only supported on Unix or Unix-like operating systems with the native package libfuse installed.
            If you are running inside a docker container, the docker container must be started with the `--privileged`
            flag or started with `--cap-add SYS_ADMIN --device /dev/fuse`.

           .. code-block:: python

                exp_path_1 = os.path.normpath(os.path.join(cwd, '../dataset/data/crime-spring.csv'))
                paths = [{'file': exp_path_1}]
                mltable = from_paths(paths)

                with mltable._mount() as mount_context:
                    # list top level mounted files and folders in the mltable
                    os.listdir(mount_context.mount_point)

                # You can also use the start and stop methods
                mount_context = mltable._mount()
                mount_context.start()  # this will mount the file streams
                mount_context.stop()  # this will unmount the file streams

           If target_path starts with a /, then it will be treated as an absolute path. If it doesn't start
           with a /, then it will be treated as a relative path relative to the current working directory.

        :param stream_column: The stream column to mount.
        :type stream_column: str
        :param mount_point: The local directory to mount the files to. If None, the data will be mounted into a
            temporary directory, which you can find by calling the `MountContext.mount_point` instance method.
        :type mount_point: str
        :return: Returns a context manager for managing the lifecycle of the mount.
        :rtype: MountContext: the context manager. Upon entering the context manager, the dataflow will be
            mounted to the mount_point. Upon exit, it will remove the mount point and clean up the daemon process
            used to mount the dataflow.
        """
        def _ensure_path(path):
            if not path or path.isspace():
                return (tempfile.mkdtemp(), True)

            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                    return (os.path.abspath(path), True)
                except FileExistsError:
                    # There is a chance that the directory may be created after we check for existence and
                    # before we create it. In this case, we can no-op as though the directory already existed.
                    pass

            is_empty = not any(files or dirnames for _,
                               dirnames, files in os.walk(path))
            return (os.path.abspath(path), is_empty)

        mltable_yaml_str = self._dataflow.to_yaml_string()
        path = f'{tempfile.mkdtemp()}/dataflow_yaml'
        with open(path, 'w+') as file:
            file.write(mltable_yaml_str)

        temp_dataflow_file_full_path = os.path.abspath(path)
        temp_dataflow_local_path_uri = pathlib.Path(
            temp_dataflow_file_full_path).as_uri()
        temp_dataflow_local_path_uri_encoded = urllib.parse.quote(
            temp_dataflow_local_path_uri.encode('utf8'), safe='')

        default_column_encode = urllib.parse.quote(
            stream_column.encode('utf8'), safe='')
        dataflow_uri = f"rsdf://dataflowfs/{temp_dataflow_local_path_uri_encoded}/{default_column_encode}/"

        mount_point, is_empty = _ensure_path(mount_point)
        if os.path.ismount(mount_point):
            raise ValueError(
                f'"{mount_point}" is already mounted. Run `sudo umount "{mount_point}"` to unmount it.')
        if not is_empty:
            raise ValueError(
                'mltable mount point must be empty, mounting to non-empty folder is not supported.')

        from azureml.dataprep.fuse.dprepfuse import rslex_uri_volume_mount, MountOptions
        mount_options = kwargs.get('mount_options', None)
        # this can be remove after default permission set for MountOption is ready
        if not mount_options:
            mount_options = MountOptions(data_dir_suffix=None)

        try:
            mount_context = rslex_uri_volume_mount(
                uri=dataflow_uri, mount_point=mount_point, options=mount_options)
            return mount_context
        except BaseException as e:
            message = str(e)
            if any(errorName in message for errorName in ["StreamError(NotFound)",
                                                          "DataAccessError(NotFound)",
                                                          "DataAccessError(PermissionDenied)"]):
                raise ValueError(message)
            else:
                raise e

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _execute(self) -> None:
        """
        Runs the current mltable using the local execution runtime.
        """
        force_clex = False
        allow_fallback_to_clex = True
        if '_TEST_USE_CLEX' in os.environ and os.environ['_TEST_USE_CLEX'] == 'True':
            force_clex = True
        elif '_TEST_USE_CLEX' in os.environ and os.environ['_TEST_USE_CLEX'] == 'False':
            allow_fallback_to_clex = False

        mltable_yaml_str = self._dataflow.to_yaml_string()
        try:
            _execute('mltable._execute', mltable_yaml_str, force_clex=force_clex,
                     allow_fallback_to_clex=allow_fallback_to_clex)
        except Exception as ex:
            _classify_known_user_error_from_rslex(ex.args[0])


class Metadata:
    """
    Class that maps to the metadata section of the MLTable.

    Supports the getting & adding of arbritrary metadata properties.
    """

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create(mltable):
        metadata = Metadata()
        metadata._mltable = mltable
        return metadata

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _key_name_type_check(self, name):
        if not isinstance(name, str):
            raise TypeError(
                f'Metadata only supports string property names, but encountered {type(name)}.')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def has(self, key):
        """
        Returns if this MLTable's metadata has a property named `key`.

        :param key: property name to check for
        :type key: str
        :return: if metadata contains a property named `key`
        :rtype: bool
        """
        self._key_name_type_check(key)
        return self._mltable._dataflow.has_schema_property(_METADATA_SCHEMA_NAME, key)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def get(self, key):
        """
        Returns the value associated with the property `key` in this
        MLTable's metadata. If no such property exists, returns None.

        :param key: property name to retrieve value of
        :type key: str
        :return: value associated with `key`, or None if nonexistant
        :rtype: Optional[object]
        """
        return self._mltable._dataflow.get_schema_property(_METADATA_SCHEMA_NAME, key) \
            if self.has(key) else None

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def add(self, key, value):
        """
        Sets the value of the property named `key` in this MLTable's metadata
        to `value`. If the value of `key` was previously set, the value is
        overriden.

        :param key: property name to check
        :type key: str
        :param value: value to set
        :type value: object
        :return: None
        :rtype: None
        """
        self._key_name_type_check(key)
        self._mltable._dataflow = \
            self._mltable._dataflow.set_schema_property(
                _METADATA_SCHEMA_NAME, key, value)


class Traits:
    """
    Class that maps to the traits section of the MLTable.

    Currently supported traits: timestamp_column and index_columns
    """

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create(mltable):
        traits = Traits()
        traits._mltable = mltable
        return traits

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _has_trait(self, trait_name):
        return self._mltable._dataflow.has_schema_property(_TRAITS_SCHEMA_NAME, trait_name)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _get_trait(self, trait_name):
        return self._mltable._dataflow.get_schema_property(_TRAITS_SCHEMA_NAME, trait_name)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _check_and_get_trait(self, trait_name):
        return self._get_trait(trait_name) if self._has_trait(trait_name) else None

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _set_trait(self, trait_name, trait_value):
        self._mltable._dataflow = \
            self._mltable._dataflow.set_schema_property(
                _TRAITS_SCHEMA_NAME, trait_name, trait_value)

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def timestamp_column(self):
        """
        If set returns timestamp column name, else rasies a KeyError.

        :return: timestamp column name
        :rtype: str
        """
        col = self._check_and_get_trait(_TIMESTAMP_COLUMN_KEY)
        if col is None:
            raise KeyError(
                'Timestamp column does not appear to be set. Please make sure you have set it.')
        return col

    @timestamp_column.setter
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def timestamp_column(self, column_name):
        """
        Setter for timestamp_column trait.

        :param column_name: Name of the timestamp column.
        :type column_name: str
        :return: MLTable with timestamp column set to given column
        :rtype: mltable.MLTable
        """
        if not isinstance(column_name, str):
            raise TypeError(
                f'An object of type string is expected, but encountered type: {type(column_name)}')
        self._set_trait(_TIMESTAMP_COLUMN_KEY, column_name)

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def index_columns(self):
        """
        If set returns a list of index columns' names, else raises a KeyError

        :return: list of index column names
        :rtype: list[str]
        """
        col = self._check_and_get_trait(_INDEX_COLUMNS_KEY)
        if col is None:
            raise KeyError(
                'Index columns do not appear to be set. Please make sure you have set them.')
        return col

    @index_columns.setter
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def index_columns(self, index_columns_list):
        """
        Setter for index_columns trait.

        :param index_columns_list: List containing names of index columns.
        :type index_columns_list: list[str]
        :return: MLTable with timestamp column set to given column
        :rtype: mltable.MLTable
        """
        if index_columns_list and not isinstance(index_columns_list, list):
            raise TypeError(
                f'An object of type list is expected, but encountered type: {type(index_columns_list)}')
        self._set_trait(_INDEX_COLUMNS_KEY, index_columns_list)
