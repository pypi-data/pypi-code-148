import os
from mltable.mltable import load, from_paths, from_delimited_files, from_parquet_files, from_json_lines_files,\
    DataType, MLTableHeaders
from .helper_functions import mltable_as_dict, mltable_was_loaded
from azureml.dataprep.native import StreamInfo
import pytest
import yaml


@pytest.mark.mltable_sdk_unit_test
class TestMLTableAuthoringApis:
    def test_convert_column_types_with_simple_types_sdk(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        old_df = mltable.to_pandas_dataframe()
        old_column_types = old_df.dtypes

        # checking types without transformations
        assert old_column_types['Fare'].name == 'object'
        assert old_column_types['PassengerId'].name == 'object'

        conversions = {
            'PassengerId': DataType.to_int(),
            'Fare': DataType.to_float()
        }

        new_mltable = mltable.convert_column_types(conversions)
        new_column_types = new_mltable.to_pandas_dataframe().dtypes
        assert new_column_types['PassengerId'].name == 'int64'
        assert new_column_types['Fare'].name == 'float64'

        # Testing with string type.
        # All values are string by default in pandas, so we need to do some extra logic to check
        pre_mltable = mltable.convert_column_types({'Sex': DataType.to_int()})
        pre_column_types = pre_mltable.to_pandas_dataframe().dtypes
        assert pre_column_types['Sex'].name == 'int64'

        post_mltable = mltable.convert_column_types(
            {'Sex': DataType.to_string()})
        post_column_types = post_mltable.to_pandas_dataframe().dtypes
        # string is object type
        assert post_column_types['Sex'].name == 'object'

    def test_convert_column_types_with_datetime_sdk(self, get_data_folder_path):
        # data types are not automatically inferred for sake of this test
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        old_column_types = mltable.to_pandas_dataframe().dtypes
        assert old_column_types['datetime'].name == 'object'
        assert old_column_types['date'].name == 'object'
        assert old_column_types['only_timevalues'].name == 'object'
        data_types = {
            'datetime': DataType.to_datetime('%Y-%m-%d %H:%M:%S'),
            'date': DataType.to_datetime('%Y-%m-%d'),
            'only_timevalues': DataType.to_datetime('%Y-%m-%d %H:%M:%S', '2020-01-01 ')
        }
        new_mltable = mltable.convert_column_types(data_types)
        new_column_types = new_mltable.to_pandas_dataframe().dtypes
        assert new_column_types['datetime'].name == 'datetime64[ns]'
        assert new_column_types['date'].name == 'datetime64[ns]'
        assert new_column_types['only_timevalues'].name == 'datetime64[ns]'

    def test_convert_column_types_with_multiple_columns(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        old_column_types = mltable.to_pandas_dataframe().dtypes
        assert old_column_types['datetime'].name == 'object'
        assert old_column_types['date'].name == 'object'
        assert old_column_types['latitude'].name == 'object'
        assert old_column_types['windSpeed'].name == 'object'
        assert old_column_types['precipTime'].name == 'object'
        assert old_column_types['wban'].name == 'object'
        assert old_column_types['usaf'].name == 'object'
        data_types = {
            ('datetime', 'date'): DataType.to_datetime(['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']),
            ('latitude', 'windSpeed'): DataType.to_float(),
            ('wban', 'usaf'): DataType.to_int(),
            'precipTime': DataType.to_float()
        }
        new_mltable = mltable.convert_column_types(data_types)
        new_column_types = new_mltable.to_pandas_dataframe().dtypes
        assert new_column_types['datetime'].name == 'datetime64[ns]'
        assert new_column_types['date'].name == 'datetime64[ns]'
        assert new_column_types['latitude'].name == 'float64'
        assert new_column_types['windSpeed'].name == 'float64'
        assert new_column_types['precipTime'].name == 'float64'
        assert new_column_types['wban'].name == 'int64'
        assert new_column_types['usaf'].name == 'int64'

    def test_convert_column_types_with_boolean_sdk(self, get_data_folder_path):
        # data types are not automatically inferred for sake of this test
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        old_column_types = mltable.to_pandas_dataframe().dtypes
        assert old_column_types['Sex'].name == 'object'

        # Using incorrect mismatch_as string
        with pytest.raises(ValueError) as e:
            mltable.convert_column_types(
                {'Sex': DataType.to_bool(false_values=['0'], mismatch_as='dummyVar')})
        assert "`mismatch_as` can only be" in str(e.value)

        # false_values & true_values must either both be None, empty lists, or non-empty lists
        with pytest.raises(ValueError) as e:
            mltable.convert_column_types(
                {'Sex': DataType.to_bool(true_values=['1'])})
        assert "`true_values` and `false_values` must both be None or non-empty list of strings" in str(
            e.value)

        with pytest.raises(ValueError) as e:
            mltable.convert_column_types(
                {'Sex': DataType.to_bool(false_values=['0'])})
        assert "`true_values` and `false_values` must both be None or non-empty list of strings" in str(
            e.value)

        mltable_without_inputs = mltable.convert_column_types(
            {'Sex': DataType.to_bool()})
        mltable_with_full_inputs = mltable.convert_column_types(
            {'Sex': DataType.to_bool(true_values=['1'], false_values=['0'], mismatch_as='error')})

        mltable_without_inputs_types = mltable_without_inputs.to_pandas_dataframe().dtypes
        mltable_with_full_inputs_types = mltable_with_full_inputs.to_pandas_dataframe().dtypes

        assert mltable_without_inputs_types['Sex'].name == 'bool'
        assert mltable_with_full_inputs_types['Sex'].name == 'bool'

    def test_convert_column_types_errors_sdk(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        with pytest.raises(TypeError) as e:
            mltable.convert_column_types({'datetime': DataType.to_datetime()})
        assert "to_datetime() missing 1 required positional argument: 'formats'" in str(e.value)

        with pytest.raises(ValueError) as e:
            mltable.convert_column_types(
                {'datetime': DataType.to_datetime(formats=None)})
        assert "'columns': [None] should be a string or list of strings with at least one element" in str(
            e.value)

        with pytest.raises(ValueError) as e:
            mltable.convert_column_types({'datetime': 'float'})
        assert '`convert_column_types` must be a dictionary where ' \
               'key is Union[str, Tuple[str]] and ' \
               'value is :class: mltable.DataType' in str(e.value)

        with pytest.raises(ValueError) as e:
            mltable.convert_column_types({})
        assert 'Input type is dict[Union[str, Tuple[str]]: mltable.DataType] ' \
               'with at least one entry' in str(e.value)

        with pytest.raises(ValueError) as e:
            mltable.convert_column_types({
                ('latitude', 'windSpeed'): DataType.to_float(),
                ('wban', 'latitude'): DataType.to_int()
            })
        assert "Found duplicate column. Cannot convert column 'latitude' to multiple `mltable.DataType`s." in str(
            e.value)

    def test_convert_column_types_with_mltable_yaml(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/simple_types_yaml'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        column_types = mltable.to_pandas_dataframe().dtypes
        assert column_types['datetime'].name == 'datetime64[ns]'
        assert column_types['date'].name == 'datetime64[ns]'
        assert column_types['latitude'].name == 'float64'
        assert column_types['stationName'].name == 'object'
        assert column_types['wban'].name == 'int64'
        assert column_types['gender'].name == 'bool'
        assert column_types['only_timevalues'].name == 'datetime64[ns]'

    def test_convert_column_types_with_mltable_yaml_multiple_cols(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/simple_types_multiple_cols'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        column_types = mltable.to_pandas_dataframe().dtypes
        assert column_types['datetime'].name == 'datetime64[ns]'
        assert column_types['date'].name == 'datetime64[ns]'
        assert column_types['latitude'].name == 'float64'
        assert column_types['windSpeed'].name == 'float64'
        assert column_types['wban'].name == 'int64'
        assert column_types['usaf'].name == 'int64'

    def test_convert_column_types_with_stream_info_no_workspace_sdk(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/stream_info_uri_formats'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        data_types = {
            'image_url': DataType.to_stream(),
            'long_form_uri': DataType.to_stream(),
            'direct_uri_wasbs': DataType.to_stream(),
            'direct_uri_abfss': DataType.to_stream(),
            'direct_uri_adl': DataType.to_stream()
        }
        new_mltable = mltable.convert_column_types(data_types)
        df = new_mltable.to_pandas_dataframe()
        stream_info_class_name = StreamInfo.__name__
        none_uri = type(df['image_url'][0]).__name__
        long_form_uri = type(df['long_form_uri'][0]).__name__
        direct_uri_wasbs = type(df['direct_uri_wasbs'][0]).__name__
        direct_uri_abfss = type(df['direct_uri_abfss'][0]).__name__
        direct_uri_adl = type(df['direct_uri_adl'][0]).__name__
        assert none_uri == 'NoneType'  # None since this url has no workspace info in it
        assert long_form_uri == stream_info_class_name
        assert direct_uri_wasbs == stream_info_class_name
        assert direct_uri_abfss == stream_info_class_name
        assert direct_uri_adl == stream_info_class_name

    def test_convert_column_types_with_stream_info_with_mltable_yaml(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/stream_info_yaml'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        df = mltable.to_pandas_dataframe()
        stream_info_class_name = StreamInfo.__name__
        long_form_uri = type(df['long_form_uri'][0]).__name__
        direct_uri_wasbs = type(df['direct_uri_wasbs'][0]).__name__
        direct_uri_abfss = type(df['direct_uri_abfss'][0]).__name__
        direct_uri_adl = type(df['direct_uri_adl'][0]).__name__
        assert long_form_uri == stream_info_class_name
        assert direct_uri_wasbs == stream_info_class_name
        assert direct_uri_abfss == stream_info_class_name
        assert direct_uri_adl == stream_info_class_name

    def test_traits_from_mltable_file(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        data_folder_path = os.path.join(
            cwd, 'data/mltable/traits_timeseries')
        mltable = load(data_folder_path)

        mltable_yaml = yaml.safe_load(mltable._dataflow.to_yaml_string())
        assert mltable.traits.timestamp_column == 'datetime'
        assert mltable.traits.index_columns == ['datetime']
        assert mltable_yaml['traits']['index_columns'] == ['datetime']

        mltable.traits.timestamp_column = 'random_column_name'
        mltable_yaml = yaml.safe_load(mltable._dataflow.to_yaml_string())
        assert mltable.traits.timestamp_column == 'random_column_name'
        assert mltable_yaml['traits']['timestamp_column'] == 'random_column_name'

        mltable.traits.index_columns = ['col1', 'col2']
        mltable_yaml = yaml.safe_load(mltable._dataflow.to_yaml_string())
        assert mltable.traits.index_columns == ['col1', 'col2']
        assert mltable_yaml['traits']['index_columns'] == ['col1', 'col2']

    def test_set_get_traits(self, get_mltable):
        mltable = get_mltable
        mltable.traits.index_columns = ['PassengerId']
        mltable.traits.timestamp_column = 'Pclass'
        assert mltable.traits.index_columns == ['PassengerId']
        assert mltable.traits.timestamp_column == 'Pclass'

    def test_take(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.take(count=5)

        assert '- take: 5' in new_mltable._dataflow.to_yaml_string()
        df = new_mltable.to_pandas_dataframe()
        assert df.shape[0] == 5

    def test_take_invalid_count(self, get_mltable):
        for invalid in -1, 0, "number":
            with pytest.raises(ValueError):
                get_mltable.take(count=invalid)

    def test_show(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.show(count=5)
        assert new_mltable.shape[0] == 5

    def test_show_invalid_count(self, get_mltable):
        for invalid in -1, 0, "number":
            with pytest.raises(ValueError):
                get_mltable.show(count=invalid)

    def test_take_random_sample_no_seed(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.take_random_sample(probability=.05, seed=None)
        new_mltable.to_pandas_dataframe()
        assert 'probability: 0.05' in new_mltable._dataflow.to_yaml_string()

    def test_take_random_sample_with_seed(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.take_random_sample(probability=.05, seed=5)
        new_mltable.to_pandas_dataframe()
        assert 'probability: 0.05' in new_mltable._dataflow.to_yaml_string()

    def test_take_random_sample_invalid_prob(self, get_mltable):
        for invalid in -.01, 0.0, 'number':
            with pytest.raises(ValueError):
                get_mltable.take_random_sample(probability=invalid)

    def add_step_at_start(self, mltable, idx):
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # only one transformation added
        assert len(added_transformations) == 1
        assert list(added_transformations[0].keys())[0] == 'read_delimited'

        # add `take 5` step, if `idx` is `None` resort to default arg (also `None`)
        take_dataflow = mltable._dataflow.add_transformation('take', 5, idx)
        added_transformations = yaml.safe_load(take_dataflow.to_yaml_string())[
            'transformations']

        # two transformations added, `take 5` at end
        assert len(added_transformations) == 2
        assert added_transformations[0] == {'take': 5}

    def test_add_step_at_start_zero_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_start(mltable, 0)

    def test_add_step_at_start_neg_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_start(mltable, -1)

    def add_step_at_end(self, mltable, idx):
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # only one transformation added
        assert len(added_transformations) == 1
        assert list(added_transformations[0].keys())[0] == 'read_delimited'

        # add `take 5` step to end
        if idx is None:
            take_dataflow = mltable._dataflow.add_transformation('take', 5)
        else:
            take_dataflow = mltable._dataflow.add_transformation(
                'take', 5, idx)
        added_transformations = yaml.safe_load(take_dataflow.to_yaml_string())[
            'transformations']

        # two transformations added, `take 5` at end
        assert len(added_transformations) == 2
        assert added_transformations[-1] == {'take': 5}

    def test_add_step_at_end_none_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_end(mltable, None)

    def test_add_step_at_end_pos_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_end(mltable, 1)

    def test_add_mult_steps(self, get_mltable):
        mltable = get_mltable
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # only one transformation added
        assert len(added_transformations) == 1
        assert list(added_transformations[0].keys())[0] == 'read_delimited'

        # add `take 10` step
        mltable = mltable.take(10)
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # two transformations added, `take 10` at end
        assert len(added_transformations) == 2
        assert added_transformations[-1] == {'take': 10}

        # add `take 20` step to the middle
        take_dataflow = mltable._dataflow.add_transformation('take', 20, -1)
        added_transformations = yaml.safe_load(take_dataflow.to_yaml_string())[
            'transformations']

        # three transformation steps added, `take 20` in middle and `take 10` at end
        assert len(added_transformations) == 3
        assert added_transformations[-2] == {'take': 20}
        assert added_transformations[-1] == {'take': 10}

    def test_drop_columns_with_string(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        pre_drop_columns = mltable.to_pandas_dataframe().columns
        assert "elevation" in pre_drop_columns
        new_mltable = mltable.drop_columns(columns="elevation")
        post_drop_columns = new_mltable.to_pandas_dataframe().columns
        # all columns in df.columns except elevation should be present in original mltable columns
        assert set(post_drop_columns).issubset(pre_drop_columns)
        assert "elevation" not in post_drop_columns

    def test_drop_columns_with_list(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        pre_drop_columns = mltable.to_pandas_dataframe().columns
        columns_to_drop = ["latitude", "elevation", "usaf"]
        assert all(col in pre_drop_columns for col in columns_to_drop)
        new_mltable = mltable.drop_columns(columns=columns_to_drop)
        post_drop_columns = new_mltable.to_pandas_dataframe().columns
        assert all(col not in post_drop_columns for col in columns_to_drop)

    def test_drop_columns_traits(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        assert "datetime" == mltable.traits.timestamp_column
        with pytest.raises(ValueError):
            mltable.drop_columns(columns="datetime")

    def test_keep_columns_with_string(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        pre_keep_columns = mltable.to_pandas_dataframe().columns
        assert "Name" in pre_keep_columns
        new_mltable = mltable.keep_columns(columns="Name")
        post_keep_columns = new_mltable.to_pandas_dataframe().columns
        assert len(post_keep_columns) == 1
        assert "Name" in post_keep_columns

    def test_keep_columns_with_list(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        pre_keep_columns = mltable.to_pandas_dataframe().columns
        columns_to_keep = ["Name", "Age"]
        assert all(col in pre_keep_columns for col in columns_to_keep)
        new_mltable = mltable.keep_columns(columns=columns_to_keep)
        post_keep_columns = new_mltable.to_pandas_dataframe().columns
        assert len(post_keep_columns) == 2
        assert all(col in post_keep_columns for col in columns_to_keep)

    def test_keep_columns_traits(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        assert "elevation" != mltable.traits.timestamp_column
        assert "elevation" != mltable.traits.index_columns[0]
        with pytest.raises(ValueError):
            mltable.keep_columns(columns="elevation")

    def test_create_mltable_from_delimited_files_with_local_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'}]
        mltable = from_delimited_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_delimited_files_with_local_paths(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'},
                 {'file': 'data/crime-winter.csv'}]
        mltable = from_delimited_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_delimited_files_with_folder_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'folder': 'data/mltable/mltable_folder'}]
        mltable = from_delimited_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_delimited_files_with_local_abs_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_delimited_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_delimited_files_with_header_enum(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'},
                 {'file': 'data/crime-winter.csv'}]
        mltable = from_delimited_files(
            paths, header=MLTableHeaders.all_files_same_headers)
        df = mltable_was_loaded(mltable)
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_delimited_files_with_header_no_string(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'},
                 {'file': 'data/crime-winter.csv'}]
        with pytest.raises(ValueError) as e:
            from_delimited_files(paths, header=1)
        assert str(
            e.value) == 'The header should be a string or an MLTableHeader enum'

    def test_from_delimited_files_all_file_same_header(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'},
                 {'file': 'data/crime-winter.csv'}]
        mltable = from_delimited_files(paths, header='all_files_same_headers')
        df = mltable.to_pandas_dataframe()
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_from_delimited_files_no_header(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(os.path.join(
            cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_delimited_files(paths, header='no_header')
        df = mltable.to_pandas_dataframe()
        assert df.shape == (11, 22)

    def test_from_delimited_with_auto_type_conversion_incorrect_type(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        with pytest.raises(ValueError) as e:
            from_delimited_files(paths, infer_column_types=5)
        assert str(
            e.value) == '`infer_column_types` must be a bool or a dictionary.'

    def test_from_delimited_with_auto_type_conversion_extraneous_keys(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        with pytest.raises(ValueError) as e:
            from_delimited_files(paths, infer_column_types={'some-key': 5})
        assert str(e.value) == 'If `infer_column_types` is a dictionary, ' \
                               'may only contain keys `sample_size` and `column_type_overrides`.'

    def test_from_delimited_with_auto_type_conversion_incorrect_sample_size(self, get_dataset_data_folder_path):
        for sample_size in '5', -2, 0:
            dirc = get_dataset_data_folder_path
            paths = [{'file': os.path.normpath(
                os.path.join(dirc, 'crime-spring.csv'))}]
            with pytest.raises(ValueError) as e:
                from_delimited_files(paths, infer_column_types={
                    'sample_size': sample_size})
            assert str(e.value) == 'If `infer_column_types` is a dictionary with a `sample_size` key, ' \
                                   'its value must be a positive integer.'

    def test_from_delimited_with_auto_type_conversion_column_type_overrides_unsupported_value_type(
            self, get_dataset_data_folder_path):

        for sample_size in '5', -2, 0:
            dirc = get_dataset_data_folder_path
            paths = [{'file': os.path.normpath(
                os.path.join(dirc, 'crime-spring.csv'))}]
            with pytest.raises(ValueError) as e:
                from_delimited_files(paths, infer_column_types={
                    'column_type_overrides': {'foo': sample_size}})
            assert str(
                e.value) == "'{}' is not a supported string conversion for `mltable.DataType`, " \
                            "supported types are 'string', 'int', 'float', 'boolean', & 'stream_info'".format(
                sample_size)

    def test_from_delimited_with_auto_type_conversion_column_type_overrides_unsupported_string(
            self, get_dataset_data_folder_path):

        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        with pytest.raises(ValueError) as e:
            from_delimited_files(paths, infer_column_types={
                'column_type_overrides': {'foo': 'datetime'}})
        assert str(e.value) == "'datetime' is not a supported string conversion for `mltable.DataType`, " \
                               "supported types are 'string', 'int', 'float', 'boolean', & 'stream_info'"

    def test_from_delimited_with_auto_type_conversion_incorrect_column_type_overrides_type(
            self, get_dataset_data_folder_path):

        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        with pytest.raises(ValueError) as e:
            from_delimited_files(paths, infer_column_types={
                'column_type_overrides': '5'})
        assert str(e.value) == 'If `infer_column_types` is a dictionary with a `column_type_overrides` key, ' \
                               'its value must be a dictionary of strings to `mltable.DataType`s or strings.'

    def test_from_delimited_with_auto_type_conversion_true(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        mltable = from_delimited_files(paths, infer_column_types=True)
        df = mltable.to_pandas_dataframe()
        assert list(map(str, df.dtypes)) == ['int64', 'object', 'datetime64[ns]', 'object', 'int64', 'object',
                                             'object', 'object', 'bool', 'bool', 'int64', 'int64', 'int64', 'int64',
                                             'int64', 'float64', 'float64', 'int64', 'datetime64[ns]', 'float64',
                                             'float64', 'object']

    def test_from_delimited_with_auto_type_conversion_false(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        mltable = from_delimited_files(paths, infer_column_types=False)
        df = mltable.to_pandas_dataframe()
        # object is Pandas's data type for a string, all are strings
        all(x == 'object' for x in map(str, df.dtypes))

    def test_from_delimited_with_auto_type_conversion_overrides(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]

        # before conversion
        mltable = from_delimited_files(paths, infer_column_types=True)
        df = mltable.to_pandas_dataframe()
        assert str(df['ID'].dtype) == 'int64'

        # after conversion
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        mltable = from_delimited_files(paths, infer_column_types={'sample_size': 5,
                                                                  'column_type_overrides': {
                                                                      'ID': DataType.to_float()
                                                                  }})
        df = mltable.to_pandas_dataframe()
        assert str(df['ID'].dtype) == 'float64'

    def test_from_delimited_with_auto_type_conversion_overrides_from_false(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]

        # before conversion
        mltable = from_delimited_files(paths, infer_column_types=False)
        df = mltable.to_pandas_dataframe()
        assert all(x == 'object' for x in map(str, df.dtypes))

        # after conversion
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        mltable = from_delimited_files(paths, infer_column_types={'sample_size': 5,
                                                                  'column_type_overrides': {
                                                                      'ID': 'float',
                                                                      'Date': DataType.to_datetime('%m/%d/%Y %H:%M'),
                                                                      'Domestic': DataType.to_bool(['TRUE'], ['FALSE'],
                                                                                                   'false')
                                                                  }})
        df = mltable.to_pandas_dataframe()
        assert str(df['ID'].dtype) == 'float64'
        assert str(df['Date'].dtype) == 'datetime64[ns]'
        assert str(df['Domestic'].dtype) == 'bool'

    def test_from_delimited_with_auto_type_conversion_multi_override(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]

        # before conversion
        mltable = from_delimited_files(paths, infer_column_types=False)
        df = mltable.to_pandas_dataframe()
        assert all(x == 'object' for x in map(str, df.dtypes))

        # after conversion
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        mltable = from_delimited_files(paths, infer_column_types={'sample_size': 5,
                                                                  'column_type_overrides': {
                                                                      ('Date', 'ID'): 'string'
                                                                  }})
        df = mltable.to_pandas_dataframe()
        assert str(df['ID'].dtype) == 'object'
        assert str(df['Date'].dtype) == 'object'

    def test_from_delimited_with_auto_type_conversion_incorrect_keys(self, get_dataset_data_folder_path):
        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        with pytest.raises(ValueError) as e:
            from_delimited_files(paths, infer_column_types={
                'sample_size': 200, 'ID': 'int'})
        assert str(e.value) == \
               'If `infer_column_types` is a dictionary, ' \
               'may only contain keys `sample_size` and `column_type_overrides`.'

    def test_from_delimited_with_auto_type_conversion_dup_col_overrides_both_single_gives_last_type(
            self, get_dataset_data_folder_path):

        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        mltable = from_delimited_files(paths, infer_column_types={'column_type_overrides': {
            'ID': DataType.to_float(),  # noqa: F601
            'ID': DataType.to_int()  # noqa: F601
        }})
        df = mltable.to_pandas_dataframe()
        assert str(df['ID'].dtype) == 'int64'

    def test_from_delimited_with_auto_type_conversion_dup_col_overrides_multi_and_single(
            self, get_dataset_data_folder_path):

        dirc = get_dataset_data_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(dirc, 'crime-spring.csv'))}]
        with pytest.raises(ValueError) as e:
            from_delimited_files(paths, infer_column_types={'column_type_overrides': {
                'ID': DataType.to_float(),
                ('ID', 'Latitude'): DataType.to_float()
            }})
        assert str(
            e.value) == "Found duplicate column. Cannot convert column 'ID' to multiple `mltable.DataType`s."

    def test_from_delimited_with_auto_type_conversion_true_yaml(self, get_data_folder_path):
        dirc = get_data_folder_path
        mltable_yaml_path = os.path.join(
            dirc, 'mltable_from_delimited/with_true')
        mltable = load(mltable_yaml_path)
        df = mltable.to_pandas_dataframe()
        assert list(map(str, df.dtypes)) == ['int64', 'float64', 'float64', 'float64', 'float64', 'float64', 'float64',
                                             'float64', 'float64', 'float64', 'object', 'object', 'int64', 'int64',
                                             'datetime64[ns]', 'datetime64[ns]', 'bool', 'object']

    def test_from_delimited_with_auto_type_conversion_false_yaml(self, get_data_folder_path):
        dirc = get_data_folder_path
        mltable_yaml_path = os.path.join(
            dirc, 'mltable_from_delimited/with_false')
        mltable = load(mltable_yaml_path)
        df = mltable.to_pandas_dataframe()
        # object is Pandas's data type for a string, all are strings
        assert all(x == 'object' for x in map(str, df.dtypes))

    def test_from_delimited_auto_type_conversion_multi_column_overrides_yaml(self, get_data_folder_path):
        dirc = get_data_folder_path

        # before conversion
        mltable_yaml_path = os.path.join(
            dirc, 'mltable_from_delimited/with_true')
        mltable = load(mltable_yaml_path)
        df = mltable.to_pandas_dataframe()
        assert str(df['datetime'].dtype) == 'datetime64[ns]'
        assert str(df['date'].dtype) == 'datetime64[ns]'

        # after conversion
        mltable_yaml_path = os.path.join(
            dirc, 'mltable_from_delimited/with_multi_overrides')
        mltable = load(mltable_yaml_path)
        df = mltable.to_pandas_dataframe()
        assert str(df['datetime'].dtype) == 'object'
        assert str(df['date'].dtype) == 'object'

    def test_from_delimited_auto_type_conversion_overrides_yaml_from_strings(self, get_data_folder_path):
        dirc = get_data_folder_path

        # before conversion
        mltable_yaml_path = os.path.join(
            dirc, 'mltable_from_delimited/with_false')
        mltable = load(mltable_yaml_path)
        df = mltable.to_pandas_dataframe()
        assert all(x == 'object' for x in map(str, df.dtypes))

        # after conversion
        mltable_yaml_path = os.path.join(
            dirc, 'mltable_from_delimited/with_overrides')
        mltable = load(mltable_yaml_path)
        df = mltable.to_pandas_dataframe()
        assert str(df['ID'].dtype) == 'float64'

    def test_from_delimited_with_auto_type_conversion_malformed_overrides_yaml(self, get_data_folder_path):
        dirc = get_data_folder_path
        mltable_yaml_path = os.path.join(
            dirc, 'mltable_from_delimited/malformed_overrides')
        with pytest.raises(ValueError) as e:
            load(mltable_yaml_path)
        assert str(e.value).startswith(
            'Given MLTable does not adhere to the AzureML MLTable schema')

    """
    this test case is tno working now. Need to clarify.
    def test_from_delimited_files_different_header(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/mltable/mltable_file_different_header/crime-spring.csv'},
                 {'file': 'data/mltable/mltable_file_different_header/crime-winter.csv'}]
        mltable = from_delimited_files(paths, header='all_files_different_headers')
        df = mltable.to_pandas_dataframe()
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]
    """

    def test_from_delimited_files_header_from_first_file(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/mltable/mltable_file_different_header/crime-spring.csv'},
                 {'file': 'data/mltable/mltable_file_different_header/crime-winter.csv'}]
        mltable = from_delimited_files(paths, header='from_first_file')
        df = mltable.to_pandas_dataframe()
        assert df.shape == (21, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_from_delimited_files_unknown_header_option(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        with pytest.raises(KeyError) as e:
            from_delimited_files(paths, header='some_unknown_option')
            print(e)

    def test_from_delimited_files_with_encoding(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/latin1encoding.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_delimited_files(paths, encoding='latin1')
        df = mltable_was_loaded(mltable)
        assert df.shape == (87, 66)

    def test_from_delimited_files_support_multi_line(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/multi_line_field.csv'))
        paths = [{'file': exp_path_1}]
        mltable_multi_line = from_delimited_files(
            paths, support_multi_line=True)
        df = mltable_multi_line.to_pandas_dataframe()
        assert df.shape == (3, 3)

    def test_from_delimited_files_empty_as_string(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/empty_fields.csv'))
        paths = [{'file': exp_path_1}]
        mltable_as_string = from_delimited_files(paths, empty_as_string=True)
        df_as_string = mltable_as_string.to_pandas_dataframe()
        assert df_as_string.shape == (2, 2)
        assert df_as_string['A'].values[0] == ""

    def test_create_mltable_from_delimited_files_delimiter_semicolon(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        paths = [{'file': os.path.normpath(
            os.path.join(cwd, 'data/mltable/mltable_different_delimiter/crime-spring-semicolon.csv'))}]
        # TODO default datetime forums if not provided?
        mltable = from_delimited_files(
            paths, delimiter=';', header='all_files_same_headers', infer_column_types=False)
        df = mltable_was_loaded(mltable)
        assert df.shape == (2, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_from_delimited_files_check_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [
            {'pattern': 'data/mltable/mltable_file_different_header/*.csv'}]
        mltable = from_delimited_files(
            paths, header='all_files_different_headers')
        assert mltable.paths == [
            {'pattern': 'data/mltable/mltable_file_different_header/*.csv'}]

    def test_create_mltable_from_parquet_files_with_local_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_with_local_folder_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'folder': 'data/mltable/mltable_folder_parquet'}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_with_local_paths(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/mltable/mltable_folder_parquet/crime.parquet'},
                 {'file': 'data/mltable/mltable_folder_parquet/crime_2.parquet'}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_with_local_abs_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime.parquet'))
        paths = [{'file': exp_path_1}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_include_path_column(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths, include_path_column=True)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 23)
        assert list(df.columns) == [
            'Path', 'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description',
            'Location Description', 'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code',
            'X Coordinate', 'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_paths_with_local_abs_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (1, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_local_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (1, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_local_paths(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'},
                 {'file': 'data/crime-winter.csv'}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (2, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_folder_local_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'folder': 'data/mltable/mltable_folder'}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (2, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_cloud_path(self):
        paths = [
            {'file': "https://dprepdata.blob.core.windows.net/demo/Titanic2.csv"}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (1, 1)
        assert list(df.columns) == ['Path']

    def check_random_split(self, mltable, percent):
        mltable = mltable.take(20)
        a, b = mltable.random_split(percent=percent, seed=10)

        a = a.to_pandas_dataframe()
        b = b.to_pandas_dataframe()
        c = mltable.to_pandas_dataframe()

        bound = .2  # TODO set acceptable error in split
        # assert a have ~`percent`% of c's data
        assert abs(percent - (len(a) / len(c))) <= bound

        # assert has ~(1 - `percent`)% (the remainder) of c's data
        assert abs((1 - percent) - (len(b) / len(c))) <= bound

        # assert the number of elements in a and b equals c
        assert (len(a) + len(b)) == len(c)

        # show a & b are both in c
        assert c.merge(a).equals(a)
        assert c.merge(b).equals(b)

        # assert a and b have no overlap
        assert a.merge(b).empty

    def test_random_split_even(self, get_mltable):
        mltable = get_mltable
        self.check_random_split(mltable, .5)

    def test_random_split_uneven(self, get_mltable):
        mltable = get_mltable
        self.check_random_split(mltable, .7)

    def test_get_partition_count(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_delimited_files(paths)

        previous_partition_count = mltable.get_partition_count()
        assert previous_partition_count == 1

        mini_batch_size = 200
        mltable = mltable._with_partition_size(mini_batch_size)
        new_partition_count = mltable.get_partition_count()
        assert new_partition_count == 11

    def test_update_partition_size_with_parquet(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths)

        mini_batch_size = 200
        with pytest.raises(ValueError) as e:
            mltable._with_partition_size(mini_batch_size)
        assert str(e.value) == "transformation step read_delimited or read_json_lines is required to update p" \
                               "artition_size"

    def test_mltable_from_delimited_files_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_delimited_files(paths)
        assert mltable._is_tabular is True

    def test_mltable_from_parquet_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths)
        assert mltable._is_tabular is True

    def test_mltable_from_json_files_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/order.jsonl'}]
        mltable = from_json_lines_files(paths)
        assert mltable._is_tabular is True

    def test_mltable_load_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        test_mltable_dir = os.path.join(
            cwd, 'data/mltable/mltable_file')
        mltable = load(test_mltable_dir)
        assert mltable._is_tabular is False
