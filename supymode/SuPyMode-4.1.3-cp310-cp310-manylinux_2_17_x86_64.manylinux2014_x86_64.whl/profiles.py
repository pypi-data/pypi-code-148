from dataclasses import dataclass
import numpy
from scipy.interpolate import interp1d

from MPSPlots.Render2D import Scene2D, Axis, Line


class GenericProfile():
    """
    Class represent the fiber structure coupler z-profile.
    This particular class is set to a Gaussian profile.
    """
    length: float
    """ Length of the fiber structure coupler """
    itr_f: float
    """ Final inverse taper ratio, per definition equal to one """
    itr_i: float = 1.0
    """ Initial inverse taper ratio, per definition equal to one """

    def __post_init__(self):
        self._rho_z = None
        self._coupling_factor = None

    @property
    def rho_z(self) -> numpy.ndarray:
        """
        Returns the rho profile of the coupler in the z-direction.
        """
        if self._rho_z is None:
            self.compute_rho_z()
        return self._rho_z

    @property
    def coupling_factor(self) -> numpy.ndarray:
        """
        Returns the coupling factor.
        """
        if self._coupling_factor is None:
            self.compute_coupling_factor()
        return self._coupling_factor

    @property
    def itr_list(self) -> numpy.ndarray:
        """
        Initialize a new list of itr value for the coupler.
        """
        return numpy.linspace(self.itr_i, self.itr_f, self.n_slice)

    @property
    def length(self) -> float:
        """
        Return first itr value
        """
        return self._length

    @length.setter
    def length(self, value) -> None:
        self._length = value

    @property
    def itr_i(self) -> float:
        """
        Return first itr value
        """
        return self._itr_i

    @itr_i.setter
    def itr_i(self, value) -> None:
        self._itr_i = value

    @property
    def itr_f(self) -> float:
        """
        Return last itr value
        """
        return self._itr_f

    @itr_f.setter
    def itr_f(self, value) -> None:
        self._itr_f = value

    def symmetrize_z_r(self, z, r):
        dz = abs(z[1] - z[0])
        
        new_z = numpy.arange(2 * z.size) * dz

        new_r = numpy.r_[r, r[::-1]]
        
        return new_z, new_r

    def compute_coupling_factor(self) -> None:
        r"""
        Compute the coupling factor defined as:
        .. math::
          f_c = \frac{1}{\rho} \frac{d \rho}{d z}

        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """
        dz = self.length / (self.itr_list.size)

        ditr = numpy.gradient(numpy.log(self.rho_z), axis=0)

        self._coupling_factor = ditr / dz

    def interpolate_coupling_factor(self, itr: numpy.ndarray = None, distance: numpy.ndarray = None):

        if itr is not None:
            interpolation = interp1d(
                self.itr_list, 
                self.coupling_factor, 
                axis=-1
            )

            return interpolation(itr)

        if distance is not None:
            interpolation = interp1d(
                self.distance, 
                self.coupling_factor, 
                axis=-1
            )

            return interpolation(distance)

    def compute_rho_z(self) -> numpy.ndarray:
        rho_0 = self.itr_i
        factor = -self.distance[-1] / (numpy.log(self.itr_f))
        self._rho_z = rho_0 * numpy.exp(-self.distance / factor)

    def plot(self) -> Scene2D:
        figure = Scene2D()

        ax0 = Axis(
            row=0,
            col=0,
            y_scale='linear',
            y_label='Inverse taper ratio',
            x_label='z-distance',
            # y_limits=[0, 1]
        )

        ax1 = Axis(
            row=1,
            col=0,
            y_scale='linear',
            y_label='Coupling factor',
            x_label='z-distance'
        )

        figure.add_axes(ax0, ax1)

        artist0 = Line(x=self.distance, y=self.rho_z)
        ax0.add_artist(artist0)

        artist1 = Line(x=self.distance, y=abs(self.coupling_factor))
        ax1.add_artist(artist1)

        return figure


@dataclass
class GaussianProfile(GenericProfile):
    """
    Class represent the fiber structure coupler z-profile.
    This particular class is set to a Gaussian profile.
    """
    length: float
    """ Length of the fiber structure coupler """
    itr_f: float
    """ Final inverse taper ratio, per definition equal to one """
    itr_i: float = 1.0
    """ Initial inverse taper ratio, per definition equal to one """

    def __post_init__(self):
        self._rho_z = None
        self._coupling_factor = None

    def compute_rho_z(self) -> numpy.ndarray:
        rho_0 = self.itr_i
        factor = -self.distance[-1] / (numpy.log(self.itr_f))
        self._rho_z = rho_0 * numpy.exp(-self.distance / factor)


@dataclass
class AlphaProfile(GenericProfile):
    """
    Class represent the fiber structure coupler z-profile.
    This particular class is set to a Gaussian profile.
    """
    alpha: float
    """ Alpha parameter from eq: 3.15 """
    L0: float
    """ Lenght of the hot spot """
    x_0: float
    """ Final elongation """
    n_slice: int = 100
    """ Number of slices """
    rho_0: float = 1
    """ Number of slices """

    def __post_init__(self):
        self._rho_z = None
        self._coupling_factor = None
        
        if numpy.isclose(self.alpha, 0):
            self.alpha = 1e-5

        assert -1 <= self.alpha <= 1, "Alpha has to be in the range: [-1, 1]"

        self.compute_init_parameters()
        self.compute_rho_z()
    
    def compute_init_parameters(self):
        self._itr_i = 1
        self.l_w = self.L0 + self.alpha * self.x_0
        self.r_w = self.rho_0 * (1 + self.alpha * self.x_0 / self.L0)**(-1 / (2 * self.alpha))
        self._itr_f = self.rho_0 / self.r_w
        self.z_0 = (1 - self.alpha) * self.x_0 / 2

        self.half_length = 1 * (self.z_0 + self.l_w / 2)
        self.length = 2 * self.half_length

    def compute_rho_z(self) -> None:
        """
        From paper the shape of fiber tapers Timothy A. Birks
        
        :returns:   The rho z.
        :rtype:     numpy.ndarray
        """
        
        z = numpy.linspace(0, self.half_length, self.n_slice)
        
        term0 = 2 * self.alpha * z
        term2 = (1 - self.alpha) * self.L0
        term3 = -1 / (2 * self.alpha)
        
        rho_z = self.rho_0 * (1 + term0 / term2)**term3
        
        assert not numpy.any(rho_z < 0), "Negative rho value are not physical"

        rho_z[z > self.z_0] = self.r_w

        self.distance, self._rho_z = self.symmetrize_z_r(z, rho_z)

    def plot(self) -> Scene2D:
        figure = Scene2D()

        ax0 = Axis(
            row=0,
            col=0,
            y_scale='linear',
            y_label='Inverse taper ratio',
            x_label='z-distance',
            # y_limits=[0, 1]
        )

        ax1 = Axis(
            row=1,
            col=0,
            y_scale='linear',
            y_label='Coupling factor',
            x_label='z-distance'
        )

        figure.add_axes(ax0, ax1)

        artist0 = Line(x=self.distance, y=self.rho_z)
        ax0.add_artist(artist0)

        artist1 = Line(x=self.distance, y=abs(self.coupling_factor))
        ax1.add_artist(artist1)

        return figure

milli = 1e3

x0 = 0.02 * 315 * milli
L0 = 3 * milli
a = AlphaProfile(x_0=x0, alpha=0, L0=L0, n_slice=100)
a.n_slice = 300
a.compute_rho_z()
a.plot().show()


# ABC:  -> [10e-4, 10e-5]
    # ITR: .3   -> L0 = 3mm, alpha = 0, time -> 315 seconds, speed -> 0.02 mm/seconds.
    # ITR: 0.05 -> L0 = 10mmm, alpha = 0.2, time-> 2020 seconds, speed -> 0.02 mm/seconds.

    