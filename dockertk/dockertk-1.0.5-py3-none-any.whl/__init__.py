from . import core as core
from . import util


def docker_compose_dict(path: str):
    return core.env_dict(path=path, env=core.EnvType.DOCKER_COMPOSE)


def dotenv_dict(path: str):
    return core.env_dict(path=path, env=core.EnvType.DOTENV)


def dockerfile_dict(path: str):
    return core.env_dict(path=path, env=core.EnvType.DOCKERFILE)


def refresh_envs(
    docker_compose_path: str = "docker-compose.yml",
    dotenv_path: str = ".env",
    dockerfile_path: str = "Dockerfile",
    python_env_path: str = "env.py",
):
    docker_env = {}
    if core.path_exists(docker_compose_path):
        docker_compose_env = docker_compose_dict(path=docker_compose_path)
        docker_env = {**docker_env, **docker_compose_env}
    if core.path_exists(dockerfile_path):
        dockerfile_env = dockerfile_dict(dockerfile_path)
        docker_env = {**docker_env, **dockerfile_env}

    if docker_env:
        core.write_text(dotenv_path, core.form_dotenv_src(docker_env))
        core.write_text(
            python_env_path, core.form_python_env_src(docker_env, dotenv_path)
        )
        core.write_text(
            dockerfile_env, core.form_dockerfile_env_src(docker_env, dockerfile_path)
        )
