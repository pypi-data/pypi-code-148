import pytest

from m360 import utils

def test_json_file_to_dict_fail_empty_path():
    with pytest.raises(Exception) as e:
        utils.json_file_to_dict("")
    assert e

def test_is_string_success():
    assert utils.is_string("")
    assert utils.is_string("   ")
    assert utils.is_string("yes")
    assert not utils.is_string(1)
    assert not utils.is_string(True)
    assert not utils.is_string(False)
    assert not utils.is_string({})
    assert not utils.is_string([])

def test_remove_object_from_path_success():
    data = {"config": {"M360": {"common": {"primary": True, "pet": "cersei", "foo": "bar"}, "specific": {}}}}
    utils.remove_object_from_path(data, "config.M360.invalid.primary")
    assert data == {"config": {"M360": {"common": {"primary": True, "pet": "cersei", "foo": "bar"}, "specific": {}}}}
    utils.remove_object_from_path(data, "config.M360.common.primary")
    assert data == {"config": {"M360": {"common": {"pet": "cersei", "foo": "bar"}, "specific": {}}}}
    utils.remove_object_from_path(data, "config.M360")
    assert data == {"config": {}}
