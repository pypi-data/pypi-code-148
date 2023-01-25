from ..logger.builder.logger_factory import LoggerFactory

class Config():
    def __init__(self):
        self.package = {}
        self.logger = None
        self.variables = {}
        self.dotenv = {}
        self.parsed_dotenv = {}

    def __str__(self):
        return f"Config: {self.__dict__}"

class ConfigBuilder():
    def __init__(self, config=None):
        if config is None:
            self.config = Config()
        else:
            self.config = config
    @property
    def my_logger(self):
        return ConfigMyLogger(self.config)

    @property
    def package(self):
        return ConfigPackage(self.config)

    @property
    def logger(self):
        return ConfigLogger(self.config)

    @property
    def variables(self):
        return ConfigVariables(self.config)

    @property
    def dotenv(self):
        return ConfigDotEnv(self.config)

    def build(self):
        return self.config

class ConfigPackage(ConfigBuilder):
    def __init__(self, config):
        super().__init__(config)

    def set_package_name(self, name):
        self.config.package['name'] = name
        return self

    def set_root_dir(self, directory):
        self.config.package['root_directory'] = directory
        return self

class ConfigLogger(ConfigBuilder):
    def __init__(self, config):
        super().__init__(config)

    def set_logger_level(self, level):
        self.config.logger = level
        return self

    def set_logger_dir(self, directory):
        self.config.logger = directory
        return self

    def set_logger_format(self, log_format):
        self.config.logger = log_format
        return self

    def set_logger_name(self, name):
        self.config.logger.name = name
        return self

    def set_logger(self, logger):
        self.config.logger = logger
        return self

    def set_new_logger(self, name=None, level=None, fmt=None, directory=None):
        self.config.logger = LoggerFactory.new_logger(name, level, fmt, directory)
        return self


class ConfigVariables(ConfigBuilder):
    def __init__(self, config):
        super().__init__(config)

    def set_variable(self, name, value):
        self.config.variables[name] = value
        return self

    def set_variables(self, variables):
        self.config.variables.update(variables)
        return self

    def get_from_module_config(self):
        self.config.variables.update(self.config.variables.module_config)
        return self

class ConfigDotEnv(ConfigBuilder):
    def __init__(self, config):
        super().__init__(config)

    def load_dotenv(self):
        try:
            import dotenv as _dotenv
        except ImportError:
            print("Warning: dotenv package not installed.")
            self.dotenv = None
        if _dotenv is not None:
            _dotenv.load_dotenv()
        return self
    
    def get_var(self, var_name):
        import os
        if os.getenv(var_name) is not None:
            self.config.parsed_dotenv[var_name] = os.getenv(var_name)
        return self

    def set_vars(self, vars):
        for var in vars:
            self.get_var(var)
        return self