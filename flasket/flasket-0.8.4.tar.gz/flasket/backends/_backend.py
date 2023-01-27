from attrs import define

from ..properties import BackendProperties


@define(kw_only=True, slots=False)
class Backend(BackendProperties):
    def __post_init__(self) -> None:
        super().__post_init__()
        # self.flasket is already a weakref
        self.flask.flasket = self.flasket
        self._copy_configuration()

    def _copy_configuration(self):
        for key, value in self.flasket.flask.config.items():
            self.flask.config[key] = value

    @property
    def flasket(self) -> "Flasket":
        """
        Return Flasket weak reference.
        """
        return self._flasket
