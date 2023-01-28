from dpdata.driver import Driver


@Driver.register("qdpi")
class QDPiDriver(Driver.get_driver("hybrid")):
    """QDPi.

    Parameters
    ----------
    model : str
        File name of the model.
    charge : int
        Charge of the system.
    backend : str
        Backend of the DFTB3 calculation. Can be "sqm" or "dftb+".
    **kwargs
        Keyword arguments for the DFTB3 calculation.
    """

    def __init__(self, model: str, charge: int = 0, backend="sqm", **kwargs) -> None:
        if backend == "sqm":
            dftb3 = {"type": "sqm", "qm_theory": "dftb3", "charge": charge, **kwargs}
        elif backend == "dftb+":
            dftb3 = {"type": "dftb3", "charge": charge, **kwargs}
        else:
            raise ValueError("Unknown backend: {}".format(backend))
        super().__init__(
            [
                dftb3,
                {"type": "dp", "dp": model},
            ]
        )
