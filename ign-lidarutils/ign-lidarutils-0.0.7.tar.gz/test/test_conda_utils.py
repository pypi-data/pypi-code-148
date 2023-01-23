""" Test conda_utils module"""

from lidarutils import conda_utils


def test_conda_utils():
    """test that method return non empty string"""
    path = conda_utils.get_conda_active_path()
    print("conda active path : ", path)
    assert path != ""