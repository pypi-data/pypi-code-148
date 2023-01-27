from mltable.mltable import load
import yaml


def mltable_was_loaded(mltable):
    df = mltable.to_pandas_dataframe()
    assert df is not None
    assert not df.empty
    return df


def can_load_mltable(uri, storage_options=None):
    try:
        mltable = load(uri=uri, storage_options=storage_options)
    except Exception as e:
        assert False, f'failed to load MLTable, got error [{type(e)}: {e}]'
    return mltable_was_loaded(mltable)


def mltable_as_dict(mltable):
    """
    Given a MLTable, returns it's associated information (added transformation steps, metadata, etc.)
    as a dictionary
    """
    return yaml.safe_load(mltable._dataflow.to_yaml_string())


def get_invalid_mltable(get_invalid_data_folder_path):
    return load(get_invalid_data_folder_path)
