import yaml
from pathlib import Path
import os

class Struct:
    def __init__(self, **response):
        for k, v in response.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(**v)
            else:
                self.__dict__[k] = v


def main():
    noto_home = Path.home() / ".noto"
    if not Path.is_dir(noto_home):
        os.mkdir(noto_home)

    with open("config.yaml") as file:
        configDict = yaml.safe_load(file)

    from noto.cli.parser import parse
    parse(Struct(**configDict))


if __name__ == "__main__":
    main()