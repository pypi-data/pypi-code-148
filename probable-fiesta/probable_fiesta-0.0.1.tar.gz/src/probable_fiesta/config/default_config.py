from .config_factory import ConfigBuilderFactory

def get_config():
    default_config = ConfigBuilderFactory().new_default_config_builder()
    return default_config