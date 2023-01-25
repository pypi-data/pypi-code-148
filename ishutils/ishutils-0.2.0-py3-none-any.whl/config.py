import dataclasses

__all__: list[str] = ["Config", "config"]


@dataclasses.dataclass(kw_only=True)
class Config:
    default_confirm_type: str = "OVERWRITE"
    yes: bool = False


config: Config = Config()
