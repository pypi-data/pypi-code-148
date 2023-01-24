from pathlib import Path

from datagen_protocol import schemas
from dynaconf import Dynaconf

SCHEMAS_DEFAULTS = Path(__file__).parent.joinpath("resources", "defaults.toml")

SCHEMAS_DOCS = Path(__file__).parent.joinpath("resources", "documentation.toml")

schemas.config = Dynaconf(
    settings_files=[SCHEMAS_DEFAULTS, SCHEMAS_DOCS], environments=True
)
