from typing import Literal, Union

ProjectKitSupportedFormat = Literal["toml", "yaml"]
SettingsValue = Union[str, int, float]

FirstLevelSettings = dict[str, SettingsValue]
ProjectKitSettingsMap = dict[str, Union[SettingsValue, dict]]
