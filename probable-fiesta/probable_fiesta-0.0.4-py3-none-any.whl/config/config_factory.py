from .config_builder import ConfigBuilder
from ..logger.builder.logger_abstract_machine import LoggerMachine as loggerMachine
from .variables import PackageDef as pd
from .variables import LoggerDef as ld
from .variables import VariablesDef as vd
from .variables import DotEnvDef as ded

class ConfigFactory:
    @staticmethod
    def new_config_builder():
        return ConfigBuilder()

    @staticmethod
    def new_config():
        return ConfigBuilder().build()

    @staticmethod
    def new_default_config_builder(log_type='default', log_name=None):
        lM = loggerMachine()
        logger = lM.make_logger(log_type, log_name)
        cB = ConfigBuilder()
        config = cB\
            .package\
                .set_package_name(pd.NAME)\
            .logger\
                .set_logger(logger.get_logger())\
            .variables\
                .set_variable('VERSION', vd.VERSION)\
            .dotenv\
                .load_dotenv()\
                .set_vars(ded())\
            .build()
        return config
