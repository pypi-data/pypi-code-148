from mltable.mltable import load
import tempfile
import pytest
import os


@pytest.mark.mltable_sdk_unit_test
class TestMLTableSave:
    def test_save_load(self, get_mltable):
        mltable = get_mltable
        with tempfile.TemporaryDirectory() as save_dirc:
            save_path = os.path.join(save_dirc, 'MLTable')

            mltable.save(save_dirc)
            assert os.path.exists(save_path)

            # should be able to load successfully
            load(save_dirc)

    def test_save_to_existing_dirc_with_mltable_overwrite_true(self, get_mltable):
        mltable = get_mltable
        with tempfile.TemporaryDirectory() as save_dirc:
            save_path = os.path.join(save_dirc, 'MLTable')

            mltable.save(save_dirc)
            assert os.path.exists(save_path)

            mltable.save(save_dirc, overwrite=True)
            assert os.path.exists(save_path)

    def test_save_to_existing_dirc_with_mltable_overwrite_false(self, get_mltable_data_folder_path):
        # try to save to directory that has a MLTable file
        # in this case the same directory the MLTable was originally loaded
        mltable_path = get_mltable_data_folder_path
        existing_mltable_save_path = os.path.join(mltable_path, 'MLTable')
        assert os.path.exists(existing_mltable_save_path)
        mltable = load(mltable_path)
        with pytest.raises(ValueError):
            mltable.save(mltable_path, overwrite=False)

    def test_save_to_file_path(self, get_mltable):
        # try to save to *existing* file path
        mltable = get_mltable
        with tempfile.TemporaryDirectory() as save_dirc:
            save_path = os.path.join(save_dirc, 'foo.yml')
            assert not os.path.exists(save_path)
            with open(save_path, 'w') as f:
                f.write('foo')
            assert os.path.isfile(save_path)

            with pytest.raises(ValueError):
                mltable.save(save_path)  # try to save to file
