import httpx


def req_wrap(funcname, *args, **kwargs) -> dict:
    func = getattr(httpx, funcname)
    res = func(*args, timeout=30, **kwargs)
    res.raise_for_status()
    return (
        res.json()
        if kwargs["headers"]["Content-Type"] == "application/json"
        else dict(text=res.text)
    )
