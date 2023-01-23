from runfalconpipelineintegration.util_configuration import Configuration

def test_get_existing_value_from_config():
    config:Configuration = Configuration.instance()
    value:str = config.get_config_value('RUNFALCON-ENDPOINTS', 'authenticate')
    print(' >>>> value: {}'.format(value))
    assert value

def test_get_not_existing_value_from_config():
    config:Configuration = Configuration.instance()
    value:str = config.get_config_value('RUNFALCON-ENDPOINTS', 'authenticate-not-existing')
    print(' >>>> value: {}'.format(value))
    assert not value