# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
def test_call(ddev, config_file, mocker):
    mock = mocker.patch('click.edit')
    result = ddev('config', 'edit')

    assert result.exit_code == 0, result.output
    mock.assert_called_once_with(filename=str(config_file.path))
