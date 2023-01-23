from runfalconpipelineintegration.util_configuration import Configuration
from runfalconpipelineintegration.util_logger import print_debug, print_info

def test_debug_on():    
    # Configuration.instance().set_config_value('LOGGER', 'level', 'INFO')
    print_info('Hello world', 'good')
    print_debug('Hello world', 'good')