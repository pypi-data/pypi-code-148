from mltable.mltable import MLTable, _normalize_column_inputs, _check_no_duplicate_columns, load, DataType
from mltable._utils import _validate, _path_is_current_directory_variant, _make_all_paths_absolute
from azureml.dataprep.api.mltable._mltable_helper import _read_yaml
import pytest
import os
import yaml


@pytest.fixture(scope='module', autouse=True)
def get_sample_mltable(get_data_folder_path):
    path = os.path.join(get_data_folder_path, 'mltable_with_type')
    return load(path)


@pytest.mark.mltable_sdk_unit_test
class TestMLTableInnerFunctions:
    """
    This class is for adding unit tests related to internal/helper functions that are called by MLTable APIs
    """
    def test_update_workspace_info(self):
        mlt_strs = ["""
        paths:
          - file: ./train_annotations.jsonl
        transformations:
          - read_json_lines:
                encoding: utf8
                include_path_column: false
          - convert_column_types:
              - columns: image_url
                column_type: stream_info
        """, """
        paths:
          - file: ./train_annotations.jsonl
        transformations:
          - read_json_lines:
                encoding: utf8
                include_path_column: false
          - convert_column_types:
              - columns: image_url
                column_type: stream_info
          - convert_column_types:
              - columns: not_image_url
                column_type: stream_info
        """]

        expected_mlt_strs = ["""
        type: mltable
        paths:
          - file: "./train_annotations.jsonl"
        transformations:
          - read_json_lines:
              path_column: Path
              invalid_lines: error
              encoding: utf8
              include_path_column: false
              partition_size: 20971520
          - convert_column_types:
              - columns: image_url
                column_type:
                  stream_info:
                    subscription: test_sub
                    resource_group: test_rg
                    workspace_name: test_ws
                    escaped: false
        """, """
        type: mltable
        paths:
          - file: "./train_annotations.jsonl"
        transformations:
          - read_json_lines:
              path_column: Path
              invalid_lines: error
              encoding: utf8
              include_path_column: false
              partition_size: 20971520
          - convert_column_types:
              - columns: image_url
                column_type:
                  stream_info:
                    subscription: test_sub
                    resource_group: test_rg
                    workspace_name: test_ws
                    escaped: false
          - convert_column_types:
              - columns: not_image_url
                column_type: stream_info
        """]

        ws_info = {
            'subscription': 'test_sub',
            'resource_group': 'test_rg',
            'workspace': 'test_ws'
        }

        stream_column = 'image_url'
        for mlt_str, exp_mlt_str in zip(mlt_strs, expected_mlt_strs):
            mlt_dict = yaml.safe_load(mlt_str)
            mlt = MLTable._create_from_dict(mlt_dict, None)
            new_mlt = MLTable._append_workspace_to_stream_info_conversion(
                mlt, ws_info, stream_column)
            new_mlt_str = new_mlt._dataflow.to_yaml_string()
            assert yaml.safe_load(new_mlt_str) == yaml.safe_load(exp_mlt_str)

    def test_normalize_column_inputs(self):
        single_col, single_col_tuple = 'colA', ('colA',)
        list_of_cols, list_of_cols_error = ['colA', 'colB'], ['colA', 0.1]
        tuple_of_cols, tuple_of_cols_error = ('colA', 'colB'), ('colA', 0.1)

        single_col = _normalize_column_inputs(single_col)
        assert type(single_col) == list and single_col == ['colA']  # auto converts a str into a list[str]

        single_col_tuple = _normalize_column_inputs(single_col_tuple, is_tuple=True)
        assert type(single_col_tuple) == tuple and single_col_tuple == ('colA',)  # if tuple then we leave as is

        list_of_cols = _normalize_column_inputs(list_of_cols)
        assert type(list_of_cols) == list and list_of_cols == ['colA', 'colB']

        tuple_of_cols = _normalize_column_inputs(tuple_of_cols, is_tuple=True)
        assert type(tuple_of_cols) == tuple and tuple_of_cols == ('colA', 'colB')

        with pytest.raises(ValueError) as e:
            _normalize_column_inputs(list_of_cols_error)
        assert "'columns': ['colA', 0.1] should be " \
               "a string or list of strings with at least one element" in str(e.value)

        with pytest.raises(ValueError) as e:
            _normalize_column_inputs(tuple_of_cols_error, is_tuple=True)
        assert "'columns': ('colA', 0.1) should be " \
               "a string or tuple of strings with at least one element" in str(e.value)

    def test_check_no_duplicate_columns(self):
        list_of_cols_error = ['colA', 'colA']
        tuple_of_cols_error = ('colA', 'colA')
        list_of_tuples = [('colA', 'colB'), ('colC', 'colA')]

        error_str = "Found duplicate column. Cannot convert column 'colA' to multiple `mltable.DataType`s."

        with pytest.raises(ValueError) as e:
            _check_no_duplicate_columns(list_of_cols_error)
        assert error_str in str(e.value)

        with pytest.raises(ValueError) as e:
            _check_no_duplicate_columns(tuple_of_cols_error)
        assert error_str in str(e.value)

        with pytest.raises(ValueError) as e:
            _check_no_duplicate_columns(list_of_tuples)
        assert error_str in str(e.value)

    def test_get_columns_in_traits(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        assert mltable._get_columns_in_traits() == {'datetime'}

    def test_normalize_partition_int_list(self, get_sample_mltable):
        single_int = 10
        int_list = [10, 11, 1]
        error_int_list = [10, 11, '11']

        assert get_sample_mltable._normalize_partition_int_list(single_int) == [10]
        assert get_sample_mltable._normalize_partition_int_list(int_list) == int_list

        with pytest.raises(ValueError) as e:
            get_sample_mltable._normalize_partition_int_list(error_int_list)
        assert "Columns should be a int or list of int with at least one element" in str(e.value)

    def test_sanitize_and_check_datatype(self, get_sample_mltable):
        cols_no_list = {
            'PassengerId': DataType.to_int(),
            'Fare': DataType.to_float(),
            'datetime': DataType.to_datetime('%Y-%m-%d %H:%M:%S'),
            "booleanType": DataType.to_bool(),
            "strType": DataType.to_string(),
            "stream_type": DataType.to_stream()
        }
        get_sample_mltable._sanitize_and_check_datatype(cols_no_list)

        data_types_tuples = {
            ('datetime', 'datetime2'): DataType.to_datetime(['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']),
            ('int1', 'int2'): DataType.to_int(),
            ('float1', 'float2'): DataType.to_float(),
            ('bool1', 'bool2'): DataType.to_bool(),
            ('str1', 'str2'): DataType.to_string(),
            ('stream1', 'stream2'): DataType.to_stream()
        }
        get_sample_mltable._sanitize_and_check_datatype(data_types_tuples)

        with pytest.raises(ValueError) as e:
            get_sample_mltable._sanitize_and_check_datatype({})
        assert 'Input type is dict[Union[str, Tuple[str]]: mltable.DataType] with at least one entry' in str(e.value)

        with pytest.raises(ValueError) as e:
            get_sample_mltable._sanitize_and_check_datatype({1: DataType.to_int()})
        assert "'columns': 1 should be a string or tuple of strings with at least one element" in str(e.value)

    def test_validate(self):
        error_key_mltable_yaml_dict = {
            'type': 'mltable',
            'path': [{'file': 'https://dprepdata.blob.core.windows.net/demo/Titanic2.csv'}],
            'transformations': [{'take': 1}]
        }

        error_value_mltable_yaml_dict = {
            'type': 'mltable',
            'paths': [{'file': './Titanic2.csv'}],
            'transformations': [{
                'read_delimited': {
                    'delimiter': ',', 'encoding': 'ascii', 'empty_as_string': False,
                    'header': 'dummy_value', 'infer_column_types': False
                }
            }]
        }

        with pytest.raises(ValueError) as e:
            _validate(error_key_mltable_yaml_dict)
        assert "Additional properties are not allowed ('path' was unexpected)" in str(e.value)

        with pytest.raises(ValueError) as e:
            _validate(error_value_mltable_yaml_dict)
        assert "'dummy_value' is not one of ['no_header', 'from_first_file', " \
               "'all_files_different_headers', 'all_files_same_headers']" in str(e.value)

    def test_path_is_current_directory_variant(self):
        base_dir_linux, base_dir_windows, base_dir_dot = './', '.\\', '.'
        non_base_dir = './Titanic2.csv'
        assert _path_is_current_directory_variant(base_dir_linux)
        assert _path_is_current_directory_variant(base_dir_windows)
        assert _path_is_current_directory_variant(base_dir_dot)
        assert not _path_is_current_directory_variant(non_base_dir)

    def test_make_all_paths_absolute_local_happy_relative_paths(
            self, get_data_folder_path, get_dataset_data_folder_path):

        # Testing local paths get normalized
        base_path = os.path.join(get_data_folder_path, 'mltable_relative')
        yaml_dict = {
            'paths': [{'file': 'Titanic2.csv'}, {'file': './subfolder/Titanic2.csv'}],
            'transformations': [
                {'read_delimited': {'delimiter': ',', 'encoding': 'ascii', 'empty_as_string': False}}
            ]
        }

        exp_paths = [os.path.join(base_path, os.path.normpath('Titanic2.csv')),
                     os.path.join(base_path, os.path.normpath('./subfolder/Titanic2.csv'))]

        yaml_with_absolute_paths = _make_all_paths_absolute(yaml_dict, base_path)
        for path_dict, exp_path in zip(yaml_with_absolute_paths['paths'], exp_paths):
            for _, path in path_dict.items():
                assert path == exp_path

        # Testing that 'file://' is added to local paths that are not absolute
        base_path = os.path.join(get_dataset_data_folder_path, 'mltable/mltable_relative')
        yaml_dict = _read_yaml(base_path)
        yaml_with_absolute_paths_is_local_true = _make_all_paths_absolute(yaml_dict, base_path, is_local=True)
        for path_dict in yaml_with_absolute_paths_is_local_true['paths']:
            for _, path in path_dict.items():
                assert 'file://' in path

        # Testing _make_all_paths_absolute returns yaml_dict whenever path is non-local
        base_path = os.path.join(get_data_folder_path, 'mltable_tabular')
        yaml_dict = _read_yaml(base_path)
        # No transformation since the path inside the MLTable file is a cloud uri pattern
        assert yaml_dict == _make_all_paths_absolute(yaml_dict, base_path)


@pytest.mark.mltable_sdk_unit_test_windows
class TestInnerFunctionsWindowsOnly:
    def test_make_all_paths_absolute_local_relative_path_double_backslash(
            self, get_data_folder_path, get_dataset_data_folder_path):

        base_path = os.path.join(get_data_folder_path, 'dummy_basepath/inner_path')
        yaml_dict = {
            'paths': [{'file': '.\\Titanic2.csv'}, {'file': '..\\Titanic2.csv'}],
            'transformations': [{
                'read_delimited': {
                    'delimiter': ',', 'encoding': 'ascii', 'empty_as_string': False}}
            ]
        }

        exp_paths = [os.path.join(base_path, 'Titanic2.csv'),
                     os.path.join(base_path, '..\\Titanic2.csv')]

        yaml_with_absolute_paths = _make_all_paths_absolute(yaml_dict, base_path)
        for path_dict, exp_path in zip(yaml_with_absolute_paths['paths'], exp_paths):
            for _, path in path_dict.items():
                assert path == exp_path

    def test_make_all_paths_absolute_local_relative_path_no_initial_separator(
            self, get_data_folder_path, get_dataset_data_folder_path):

        # Testing mixed windows/unix irregular relative path
        base_path = os.path.join(get_data_folder_path, 'dummy_basepath')
        yaml_dict = {
            'paths': [{'file': 'Titanic2.csv'}, {'file': 'subfolder\\Titanic2.csv'}],
            'transformations': [{
                'read_delimited': {
                    'delimiter': ',', 'encoding': 'ascii', 'empty_as_string': False}}
            ]
        }
        exp_paths = [os.path.join(base_path, 'Titanic2.csv'),
                     os.path.join(base_path, 'subfolder\\Titanic2.csv')]

        yaml_with_absolute_paths = _make_all_paths_absolute(yaml_dict, base_path)
        for path_dict, exp_path in zip(yaml_with_absolute_paths['paths'], exp_paths):
            for _, path in path_dict.items():
                assert path == exp_path
