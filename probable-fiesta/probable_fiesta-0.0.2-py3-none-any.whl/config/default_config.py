from .config_factory import ConfigFactory

def get_config():
    default_config = ConfigFactory().new_default_config_builder()
    return default_config