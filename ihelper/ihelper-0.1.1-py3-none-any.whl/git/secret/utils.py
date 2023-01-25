from typing import Optional

from ishutils.common.run import run


def gh_secret_delete(name: str, repo: Optional[str]) -> None:
    args: list[str] = ["gh", "secret", "delete", name]
    if repo:
        args += ["--repo", repo]
    run(args=args)


def gh_secret_set(name: str, body: str, repo: Optional[str]) -> None:
    args: list[str] = ["gh", "secret", "set", name, "--body", body]
    if repo:
        args += ["--repo", repo]
    run(args=args)
