from .config_builder import ConfigBuilder
from .variables import PackageDef as pd
from .variables import LoggerDef as ld
from .variables import VariablesDef as vd
from .variables import DotEnvDef as ded

class ConfigBuilderFactory:
    @staticmethod
    def new_config_builder():
        return ConfigBuilder()

    @staticmethod
    def new_default_config_builder():
        cB = ConfigBuilder()
        config = cB\
            .package\
                .set_package_name(pd.NAME)\
            .logger\
                .set_logger_level(ld.LEVEL)\
                .set_logger_dir(ld.DIRECTORY)\
                .set_logger_format(ld.FORMAT)\
                .set_logger_name(ld.NAME)\
            .variables\
                .set_variable('VERSION', vd.VERSION)\
            .dotenv\
                .load_dotenv()\
                .set_vars(ded())\
            .build()
        return config