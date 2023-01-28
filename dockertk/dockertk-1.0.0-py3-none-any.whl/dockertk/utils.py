import re as __re
from pathlib import Path as __Path


def __str_indent(__str:str):
    return len(__str) - len(__str.lstrip())

def __match_first_letter_in_string(__str:str):
    return __re.search("[a-zA-Z]", __str)

def __str_from_match_start(__str:str,__match:__re.Match):
    return __str[__match.start() if __match else 0 :]

def __str_from_first_letter(__str:str):
    match = __match_first_letter_in_string(__str)
    return __str_from_match_start(__str,match)


def __iter_env_kv_pairs(__lines: list[str]):
    indent = None
    for line in (line for line in __lines if line):
        line_indent = __str_indent(line)
        if indent is None:
            if line.strip().endswith("environment:"):
                indent = line_indent
        elif line_indent > indent:
            ffl = __str_from_first_letter(line)
            if "=" in ffl:
                yield ffl.split("=",1)
        else:
            indent = None


def __dockerfile_env_dict(__path: str):
    text = __Path(__path).read_text()
    lines = text.splitlines()
    return {key: value for (key, value) in __iter_env_kv_pairs(lines)}


def __write_env(env_path: str, env_dict: dict):
    env_lines = [f"{key}={value}" for key, value in env_dict.items()]
    env_lines.sort()
    env_source = "\n".join(env_lines) if env_lines else ""
    __Path(env_path).write_text(env_source)


def __update_env_from_docker_compose_file(
    env_path: str, docker_compose_path: str 
):
    env_dict = __dockerfile_env_dict(docker_compose_path)
    __write_env(env_path, env_dict)


def dockerfile_env_dict(__path: str):
    return __dockerfile_env_dict(__path)

def update_env_from_docker_compose_file(env_path: str = ".env", docker_compose_path: str = "docker-compose.yml"):
    return __update_env_from_docker_compose_file(env_path=env_path,docker_compose_path=docker_compose_path)