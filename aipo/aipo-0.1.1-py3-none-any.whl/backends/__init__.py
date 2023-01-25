BACKEND_CLASSES = {
    "redis": "aipo.backends.redis.RedisBackend",
}


def get_backend_class(url: str) -> str:
    """Get the backend class from the url.

    :param url: The broker connection url.

    :return: The backend class path.
    """
    name = url.split("://")[0]
    if name in BACKEND_CLASSES:
        return BACKEND_CLASSES[name]

    raise ValueError(f"Unknown backend: {name}")
