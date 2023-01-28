
from .objects import DotEnv

dot_env_keys = lambda dotenv_path:DotEnv(dotenv_path)
env_fields_src = lambda env_keys:"\n".join(map(lambda key:f"    {key}:Optional[str] = Field(default=None)",env_keys))
env_init_src = "env = Env(**{"+"key:os.environ.get(key) for key in Env.__fields__.keys()})\n"
python_env_module_src = lambda dotenv_path:f"""
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv('{dotenv_path}')

class Env(BaseModel):

{env_fields_src(DotEnv(dotenv_path).keys)}

{env_init_src}
"""