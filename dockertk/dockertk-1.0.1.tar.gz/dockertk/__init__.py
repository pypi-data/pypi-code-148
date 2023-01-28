from . import objects as __objects
from . import templates as __templates
from pathlib import Path as __Path

def __docker_compose_env_dict(docker_compose_path: str):
    return __objects.DockerEnv(docker_compose_path).dict()

def __dotenv_dict(dotenv_path:str):
    return __objects.DotEnv(dotenv_path).dict()

def __form_dotenv_source(__env_dict:dict):
    env_lines = [f"{key}={value}" for key, value in __env_dict.items()]
    env_lines.sort()
    env_source = "\n".join(env_lines) if env_lines else ""
    return env_source  

def __write_dotenv_from_docker_compose(dotenv_path: str,docker_compose_path:str):
    env_dict = __docker_compose_env_dict(docker_compose_path)
    source = __form_dotenv_source(env_dict)
    __Path(dotenv_path).write_text(source)

def __write_python_env_module_from_dotenv(python_env_module_path:str,dotenv_path:str):
    python_env_module_source = __templates.python_env_module_src(dotenv_path)
    __Path(python_env_module_path).write_text(python_env_module_source)



def docker_compose_env_dict(docker_compose_path: str):
    return __docker_compose_env_dict(docker_compose_path)

def dotenv_dict(dotenv_path:str):
    return __dotenv_dict(dotenv_path)

def update_env_from_docker_compose_file(dotenv_path: str = ".env", docker_compose_path: str = "docker-compose.yml",python_env_module_path:str="env.py"):
    __write_dotenv_from_docker_compose(dotenv_path,docker_compose_path)
    __write_python_env_module_from_dotenv(python_env_module_path,dotenv_path)

