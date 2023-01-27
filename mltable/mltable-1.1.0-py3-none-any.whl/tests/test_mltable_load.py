from mltable.mltable import load
from .helper_functions import can_load_mltable, get_invalid_mltable
from azureml.dataprep.api.mltable._mltable_helper import _read_yaml
import pytest
import os


@pytest.mark.mltable_sdk_unit_test
class TestMLTableLoad:
    def test_load_mltable(self, get_mltable):
        mltable = get_mltable
        assert mltable is not None

    def test_load_invalid_mltable(self, get_invalid_data_folder_path):
        with pytest.raises(ValueError):
            get_invalid_mltable(get_invalid_data_folder_path)

    def test_load_mltable_with_type_prop(self, get_data_folder_path):
        data_folder_path = os.path.join(get_data_folder_path, 'mltable_with_type')
        can_load_mltable(uri=data_folder_path)

    def test_load_mltable_with_mixed_casing(self, get_data_folder_path):
        # loads a dataset from a path with both upper and lower case letters
        data_folder_path = os.path.join(get_data_folder_path, 'MLTable_case')
        can_load_mltable(uri=data_folder_path)

    def test_load_mltable_with_unicode(self, get_data_folder_path):
        # loads tabular mltable from paths with non-ascii unicode characters
        for char in 'Ǣ', 'Ɖ', 'Ƙ', 'Ƹ':
            path = f'mltable_unicode/{char}'
            data_folder_path = os.path.join(get_data_folder_path, path)
            can_load_mltable(uri=data_folder_path)

    def test_list_paths(self, get_mltable, get_data_folder_path):
        exp_path_1 = os.path.normpath(
            os.path.join(get_data_folder_path, 'mltable_relative/Titanic2.csv'))
        exp_path_2 = os.path.normpath(
            os.path.join(get_data_folder_path, 'mltable_relative/subfolder/Titanic2.csv'))
        exp_paths_list = ['file://' + exp_path_1, 'file://' + exp_path_2]
        mltable = get_mltable
        paths = mltable.paths
        assert len(paths) == 2
        for path_dict in paths:
            assert path_dict['file'] in exp_paths_list

    def test_load_relative_mltable(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)

        # loads mltable from relative path by mimicking to be in a local folder
        relative_path = './data/mltable/mltable_relative'
        mltable = load(relative_path)
        mltable_yaml_dict = _read_yaml(relative_path)
        assert mltable_yaml_dict is not None
        assert mltable._dataflow.to_yaml_string() is not None

        for path_dict in mltable.paths:
            assert 'file://' in path_dict['file']

    def test_load_mltable_with_arbitrary_metadata(self, get_data_folder_path):
        mltable_dirc = get_data_folder_path
        mltable_path = os.path.join(mltable_dirc, 'mltable_arb_metadata')
        can_load_mltable(mltable_path)

    def test_load_mltable_with_invalid_url(self):
        with pytest.raises(ValueError) as excinfo:
            mltable_url = 'https://raw.githubusercontent.com/microsoft/arcticseals/master/data/test.csv'
            load(mltable_url)
        assert "Not able to find MLTable file" in str(excinfo.value)
