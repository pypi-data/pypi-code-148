from typing import List,Tuple,Dict,AnyStr
from pathlib import Path
from . import utils

class EnvBase:

    __slots__ = ("env_src","env_lines",)


    def __iter__(self):
        for line in (line for line in self.env_lines if line and "=" in line):
            yield line.split("=",1)


    @property
    def kv_pairs(self) -> List[Tuple[str,str]]:
        return [kv for kv in self]

    @property
    def keys(self) -> List[str]:
        return [key for (key,_) in self]
    
    @property
    def values(self) -> List[str]:
        return [value for (_,value) in self]


    def dict(self) -> Dict[str,AnyStr]:
        return {key:value for (key,value) in self}

class DotEnv(EnvBase):

    def __init__(self,path:str):
        env_src = Path(path).read_text()
        env_lines = [line for line in env_src.splitlines(keepends=False) if line and "=" in line]
        self.env_src = env_src
        self.env_lines = env_lines

class PythonEnv(EnvBase):
    pass


class DockerEnv(EnvBase):
    def __init__(self,path:str):
        indent = None
        env_src = Path(path).read_text()
        env_lines = []
        for line in (line for line in env_src.splitlines(keepends=False) if line):
            line_indent = utils.indent(line)
            if indent is None:
                if line.strip().endswith("environment:"):
                    indent = line_indent
            elif line_indent > indent:
                ffl = utils.from_first_letter(line)
                if "=" in ffl:
                    env_lines.append(ffl)
            else:
                indent = None
        self.env_src = env_src
        self.env_lines = env_lines
            