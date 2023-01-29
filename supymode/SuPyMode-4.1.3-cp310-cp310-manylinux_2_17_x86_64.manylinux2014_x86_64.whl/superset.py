#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
import os
import logging
from dataclasses import dataclass
from itertools import combinations

# Third-party imports
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp

# Local imports
from SuPyMode.supermode import SuperMode
from MPSPlots.Render2D import Scene2D, Axis, Multipage, Line, ColorBar, Mesh
from MPSPlots import CMAP


@dataclass
class SuperSet(object):
    """
    Solver to which is associated the computed SuperSet Modes

    .. note::
        This class is a representation of the fiber optic structures set of supermodes, hence the name.
        This class has not ling to c++ codes, it is pure Python.
        The items of this class are the supermodes generated from within the SuPySolver

    """
    parent_solver: object

    def __post_init__(self):
        self._transmission_matrix = None
        self.supermodes = []
        self._itr_to_slice = interp1d(self.itr_list, numpy.arange(self.itr_list.size))

    def __getitem__(self, idx: int):
        return self.supermodes[idx]

    def __setitem__(self, idx: int, value):
        self.supermodes[idx] = value

    @property
    def geometry(self):
        """
        Return geometry of the coupler structure
        """

        return self.parent_solver.geometry

    @property
    def itr_list(self):
        """
        Return list of itr value that are used to compute the supermodes
        """

        return self.parent_solver.itr_list

    @property
    def axes(self):
        """
        Return axes object of the geometry
        """
        return self.parent_solver.geometry.axes

    @property
    def transmission_matrix(self) -> numpy.ndarray:
        """Return supermode transfert matrix"""
        if self._transmission_matrix is None:
            self.compute_transmission_matrix()

        return self._transmission_matrix

    def itr_to_slice(self, itr_list: list[int]) -> list[int]:
        """
        Return slice number associated to itr value

        :param      itr_list:      Inverse taper ration value to evaluate the slice.
        :type       itr_list:      { type_description }

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        itr_list = numpy.array(itr_list)
        itr_i = self.itr_list[0]
        itr_f = self.itr_list[-1]

        assert numpy.all((itr_list >= itr_f) & (itr_i >= itr_list)), \
            f"ITR evaluation: {itr_list} is outside the boundaries!"

        return self._itr_to_slice(itr_list).astype(int)

    def slice_to_itr(self, slice_list: list[int]) -> list[float]:
        """
        Return slice number associated to itr value

        :param      slice_list:      Value of the slice to which evaluate the itr.
        :type       slice_list:      list[int]

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        return [self.itr_list[i] for i in slice_list]

    def name_supermodes(self, *name_list) -> None:
        for n, name in enumerate(name_list):
            self[n].name = name
            setattr(self, name, self[n])

        return [getattr(self, name) for name in name_list]

    def swap_supermode_order(self, idx0: int, idx1: int) -> "SuperSet":
        """
        Swap two supermodes.
        it doesn't change any of their characteristic, it only changes the order on whihc they will
        appear, notably for the plots.

        :param      idx0:            Index of the first mode to swap
        :type       idx0:            int
        :param      idx1:            Index of the second mode to swap
        :type       idx1:            int
        """
        self.supermodes[idx0], self.supermodes[idx1] = self.supermodes[idx1], self.supermodes[idx0]

        return self

    def compute_transmission_matrix(self) -> None:
        """
        Calculates the transmission matrix with only the propagation constant included.

        :returns:   The transmission matrix.
        :rtype:     numpy.ndarray
        """
        shape = [
            len(self.supermodes),
            len(self.supermodes),
            len(self.itr_list)
        ]

        self._transmission_matrix = numpy.zeros(shape)

        for mode in self.supermodes:
            self._transmission_matrix[mode.mode_number, mode.mode_number, :] = mode.beta._data

    def add_coupling_to_t_matrix(self, t_matrix: numpy.ndarray, coupling_factor: numpy.ndarray) -> numpy.ndarray:
        """
        Add the coupling coefficients to the transmission matrix.

        :returns:   The transmission matrix.
        :rtype:     numpy.ndarray
        """

        size = t_matrix.shape[-1]

        t_matrix = t_matrix.astype(complex)
        for mode_0, mode_1 in combinations(self.supermodes, 2):
            coupling = coupling_factor * mode_0.coupling.get_values(mode_1)[:size]
            t_matrix[mode_0.mode_number, mode_1.mode_number, :] = +1j * coupling
            t_matrix[mode_1.mode_number, mode_0.mode_number, :] = -1j * coupling

        return t_matrix

    def compute_coupling_factor(self, coupler_length: float) -> numpy.ndarray:
        r"""
        Compute the coupling factor defined as:
        .. math::
          f_c = \frac{1}{\rho} \frac{d \rho}{d z}

        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """

        dx = coupler_length / (self.itr_list.size)

        ditr = numpy.gradient(numpy.log(self.itr_list), axis=0)

        return ditr / dx

    def propagate(self, profile, initial_amplitude: list, max_step: float = 0.05, **kwargs) -> numpy.ndarray:
        """
        Returns the amplitudes value of the supermodes in the coupler.

        :param      initial_amplitude:  The initial amplitude
        :type       initial_amplitude:  list
        :param      profile:            The z-profile of the coupler
        :type       profile:            object
        :param      max_step:           The maximum stride to use in the solver
        :type       max_step:           float
        :param      kwargs:             The keywords arguments to be passed to the solver
        :type       kwargs:             dictionary

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """
        initial_amplitude = numpy.asarray(initial_amplitude)

        final_slice = self.itr_to_slice(itr_list=profile.itr_f)
        profile.n_slice = final_slice

        sub_t_matrix = self.transmission_matrix[..., :final_slice]

        t_matrix = self.add_coupling_to_t_matrix(t_matrix=sub_t_matrix, coupling_factor=profile.coupling_factor)

        t_matrix_interpolation = interp1d(profile.distance, t_matrix, axis=-1)

        def foo(t, y):
            return 1j * t_matrix_interpolation(t).dot(y)

        sol = solve_ivp(
            foo,
            y0=initial_amplitude.astype(complex),
            t_span=[0, profile.length],
            vectorized=True,
            max_step=max_step,
            method='RK45',
            **kwargs
        )

        return sol.t, sol.y

    def get_mix_field(self, distance: numpy.ndarray, amplitudes: numpy.ndarray, under_sampling: int = 1):
        distance = distance[::under_sampling]

        slice_list = (distance / distance[-1] * (self.itr_list.size - 1)).astype(int)

        field_mix = \
            amplitudes[0, slice_list, numpy.newaxis, numpy.newaxis] * self[0].field._data[slice_list, ...] + \
            amplitudes[1, slice_list, numpy.newaxis, numpy.newaxis] * self[1].field._data[slice_list, ...]

        return distance, field_mix

    def get_propagation_field(self,
                              initial_amplitude: list,
                              coupler_length: float = 1000,
                              max_step: float = 0.05,
                              under_sampling: int = 10,
                              **kwargs) -> None:
        """
        Generates a gif video of the mode propagation.

        :param      initial_amplitude:  The initial amplitude
        :type       initial_amplitude:  list
        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float
        :param      max_step:           The maximum stride to use in the solver
        :type       max_step:           float
        :param      under_sampling:     Propagation undersampling factor for the video production
        :type       under_sampling:     int
        :param      kwargs:             The keywords arguments
        :type       kwargs:             dictionary
        """
        import pyvista as pv

        z, amplitudes = self.propagate(
            initial_amplitude=initial_amplitude,
            coupler_length=coupler_length,
            max_step=max_step,
            **kwargs
        )

        distance, all_field = self.get_mix_field(distance=z, amplitudes=numpy.abs(amplitudes), under_sampling=2)

        x = self.axes.x.mesh / 200
        y = self.axes.y.mesh / 200

        grid = pv.StructuredGrid(x, y, all_field[0])

        plotter = pv.Plotter(notebook=False, off_screen=True)

        plotter.add_mesh(
            grid,
            scalars=all_field[0],
            lighting=False,
            show_edges=True,
        )

        plotter.open_gif("wave_test.gif", fps=20)

        pts = grid.points.copy()

        for z, field in zip(distance, all_field.real):
            pts[:, -1] = field.ravel()
            plotter.update_coordinates(pts, render=False)
            plotter.update_scalars(field.ravel(), render=False)

            plotter.write_frame()

        plotter.close()

    def append_supermode(self, **kwargs) -> None:
        """
        Add a supermode to the SuperSet list of supermodes.
        """
        superMode = SuperMode(parent_set=self, **kwargs)

        self.supermodes.append(superMode)

    def _interpret_itr_slice_list_(self, slice_list: list, itr_list: list):
        slice_list = [*slice_list, *self.itr_to_slice(itr_list)]

        if len(slice_list) == 0:
            slice_list = [0, -1]

        itr_list = self.slice_to_itr(slice_list)

        itr_list = numpy.sort(itr_list)[::-1]

        return self.itr_to_slice(itr_list), itr_list

    @staticmethod
    def single_plot(plot_function):
        def wrapper(self, *args, **kwargs):
            figure = Scene2D(unit_size=(10, 4))
            ax = Axis(row=0, col=0)
            figure.add_axes(ax)
            plot_function(self, ax=ax, *args, **kwargs)

            return figure

        return wrapper

    @single_plot
    def plot_index(self, ax: Axis) -> Scene2D:
        """
         Plot effective index for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        for mode in self.supermodes:
            y = mode.index.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.stylized_name}')
            ax.add_artist(artist)
            ax.set_style(**mode.index.plot_style)

    @single_plot
    def plot_beta(self, ax: Axis) -> Scene2D:
        """
         Plot propagation constant for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        for mode in self.supermodes:
            y = mode.beta.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.stylized_name}')
            ax.add_artist(artist)
            ax.set_style(**mode.beta.plot_style)

    @single_plot
    def plot_coupling(self, ax: Axis, mode_of_interest: list = None) -> Scene2D:
        """
         Plot coupling value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        if mode_of_interest is None:
            mode_of_interest = self.supermodes

        for mode_0, mode_1 in combinations(mode_of_interest, 2):
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.coupling.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_name} - {mode_1.stylized_name}')
                ax.add_artist(artist)
                ax.set_style(**mode_0.coupling.plot_style)

    @single_plot
    def plot_adiabatic(self, ax: Axis, mode_of_interest: list = None) -> Scene2D:
        """
         Plot adiabatic criterion for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        if mode_of_interest is None:
            mode_of_interest = self.supermodes

        for mode_0, mode_1 in combinations(mode_of_interest, 2):
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.adiabatic.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_name} - {mode_1.stylized_name}')
                ax.add_artist(artist)
                ax.set_style(**mode_0.adiabatic.plot_style)

    def plot_field(self, itr_list: list[float] = [], slice_list: list[int] = []) -> Scene2D:
        """
        Plot each of the mode field for different itr value or slice number.

        :param      itr_list:    List of itr value to evaluate the mode field
        :type       itr_list:    list
        :param      slice_list:  List of integer reprenting the slice where the mode field is evaluated
        :type       slice_list:  list

        :returns:   The figure
        :rtype:     Scene2D
        """
        figure = Scene2D(unit_size=(3, 3))

        slice_list, itr_list = self._interpret_itr_slice_list_(slice_list, itr_list)

        for m, mode in enumerate(self.supermodes):
            for n, (itr, slice) in enumerate(zip(itr_list, slice_list)):
                ax = Axis(row=n, col=m, title=f'{mode.stylized_name}\n[slice: {slice}  ITR: {itr:.2f}]')
                ax.colorbar = ColorBar(symmetric=True, position='right')

                x, y, field = mode.field.get_field_with_boundaries(slice=slice)

                artist = Mesh(x=x, y=y, scalar=field, colormap=CMAP.BKR)

                ax.add_artist(artist)

                ax.set_style(**mode.field.plot_style)
                figure.add_axes(ax)

        return figure

    def plot(self, type: str, **kwargs) -> Scene2D:
        """
        Generic plot function.

        Args:
            type: Plot type ['index', 'beta', 'adiabatic', 'coupling', 'field']
        """

        assert type.lower() in (type_list := ['index', 'beta', 'adiabatic', 'coupling', 'field']), f'type [{type}] as to be in {type_list}'

        match type.lower():
            case 'index':
                return self.plot_index(**kwargs)
            case 'beta':
                return self.plot_beta(**kwargs)
            case 'coupling':
                return self.plot_coupling(**kwargs)
            case 'adiabatic':
                return self.plot_adiabatic(**kwargs)
            case 'field':
                return self.plot_field(**kwargs)

    def generate_report(self,
                        filename: str = "report",
                        itr_list: list[float] = [],
                        slice_list: list[int] = [],
                        dpi: int = 200,
                        mode_of_interest: list = None) -> None:
        """
        Generate a full report of the coupler properties as a .pdf file

        :param      filename:          Name of the Report file to be outputed.
        :type       filename:          str
        :param      itr_list:          List of itr value to evaluate the mode field.
        :type       itr_list:          Array
        :param      slice_list:        List of slice value to evaluate the mode field.
        :type       slice_list:        Array
        :param      dpi:               Pixel density for the image included in the report.
        :type       dpi:               int
        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   { description_of_the_return_value }
        :rtype:     None
        """
        figures = []
        figures.append(self.geometry.plot()._render_())

        figures.append(self.plot_field(itr_list=itr_list, slice_list=slice_list)._render_())

        figures.append(self.plot_index()._render_())

        figures.append(self.plot_beta()._render_())

        figures.append(self.plot_coupling(mode_of_interest=mode_of_interest)._render_())

        figures.append(self.plot_adiabatic(mode_of_interest=mode_of_interest)._render_())

        # directory = os.path.join(Directories.ReportPath, filename) + '.pdf'

        directory = f"{os.getcwd()}/{filename}.pdf"

        logging.info(f'Saving report to {directory}')

        Multipage(directory, figs=figures, dpi=dpi)

        for figure in figures:
            figure.close()


# -
