from os import path
from pathlib import Path

HITFACTORPY_MODULE_PATH = Path(path.dirname(path.abspath(__file__)))
HITFACTORPY_ALEMBIC_DIR = HITFACTORPY_MODULE_PATH / "migrations"
HITFACTORPY_SQLALCHEMY_URL = "postgresql+asyncpg://postgres:postgres@localhost/hitfactorpy"
