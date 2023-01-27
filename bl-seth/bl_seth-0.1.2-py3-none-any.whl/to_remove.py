from dataclasses import dataclass

from bl_seth import Settings


@dataclass
class DemoSettings(Settings):
    ATTRIBUT: str
