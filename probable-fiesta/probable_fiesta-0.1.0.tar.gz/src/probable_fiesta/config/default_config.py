from .config_factory import ConfigFactory

def get_config(log_type='default', log_name=None):
    default_config = ConfigFactory().new_default_config_builder(log_type, log_name)
    return default_config