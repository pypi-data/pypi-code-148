check_commend = [
    "rm",
    "rm -rf",
    "mv",
    "-f",
    "-i",
    "-u",
    "-v",
    "-b",
    "echo",
    "cd",
    "cp",
    "scp",
    "chmod",
    "ls",
    "import os",
    "import subprocess",
    "import sys",
    "import asyncio",
    "!",
    "&",
    "--y",
    "sudo",
    "passwd",
    "getpass",
]


def LogicChecker(
    handler_code=None,
):
    """
    상품 선택 로직 함수의 commend injection 가능성을 체크하는 함수 입니다.
    """
    assert isinstance(handler_code, str), "`handler_code`는 string 타입이어야 합니다."
    for i in check_commend:
        for j in handler_code.split("\n"):
            assert i is not j, f"금지된 명령어 {i}가 {j}로 입력되었습니다."
    return handler_code
