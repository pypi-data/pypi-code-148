from .CopyrightInfo import CopyrightInfo
import tomlkit
import os
import pathlib


class Configuration:
    @staticmethod
    def load(path: str, file_name: str):
        return Configuration(path, file_name)

    def __init__(self, path: str, file_name: str):
        self.copyright_info = None

        self.root_path = None
        self.search_folders = []
        self.file_extensions = []

        config_path = os.path.join(path, file_name)
        with open(config_path, "rt") as file:
            toml_config = tomlkit.load(file)

        self._parse_toml(toml_config, path)

    def _parse_toml(self, toml_config, path: str):
        copyright_prefix = toml_config['copyright']['prefix'].lstrip()
        copyright_suffix = toml_config['copyright']['suffix'].lstrip()
        copyright_text = toml_config['copyright']['text']

        self.copyright_info = CopyrightInfo(copyright_text, copyright_prefix, copyright_suffix)

        config_path = pathlib.Path(path)
        root_path = pathlib.Path(toml_config['general']['root_path'])

        if not root_path.is_absolute():
            root_path = config_path.joinpath(root_path)

        self.root_path = str(root_path.resolve())

        search_folders = toml_config['general']['search_folders']
        self.search_folders = [str(root_path.joinpath(folder).resolve()) for folder in search_folders]
        self.file_extensions = toml_config['general']['file_extensions']
