import re

class Fxitility:

    """
    A class to represent an instance of Fxility.
    ...

    Methods
    -------
    pip_delta(price_t1 : float,price_t2 : float) -> int:
        return delta of price_t1 and price_t2 in pip
    """

    def pip_delta(self,price_t1 : float,price_t2:float) -> int:
        """
        return delta of price_t1 and price_t2 in pip

        Parameters
        ----------
        price_t1 : float, required
            More info to be displayed (default is None)

        price_t2 : float, required
            More info to be displayed (default is None)

        Returns
        -------
        Delta of Price at T1 and Price at T2 in Pips
        """

        return round((price_t1 - price_t2) * 1000)