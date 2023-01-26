import numpy
import statsmodels.regression
import statsmodels.tools
import scipy.optimize as opti
import scipy.interpolate as interp
import scipy.signal as signal
import matplotlib.pyplot as plt


class PVP:
    def __init__(self, sampling_period=0.01):
        self.sampling_period = sampling_period
        self._kinematic_profile = None
        self.fit_params = [None, None, None]
        self._pvp_params = None
        self._removed_outliers = 0

    def __repr__(self):
        _str = f"{self.__class__.__name__}\n"
        try:
            _str += f"Duration: \t {self.timestamps[-1]:.2f} seconds \n"
        except AttributeError:
            pass
        try:
            _str += f"Number of trajectories: \t {self.kinematic_profile.shape[0]}\n"
        except AttributeError:
            pass
        try:
            _str += f"Outliers Removed: \t {self._removed_outliers}\n"
        except AttributeError:
            pass
        try:
            _str += "PVP stats: \t tau={:.3f}, sigma0={:.2e}, Dtau={:.3f}\n".format(
                *tuple(self._pvp_params.values())[1:]
            )
        except AttributeError:
            pass
        try:
            _str += "PVP fit: \t C={:.2f}, Omega = {:.3f}".format(
                -self.fit_params[1], self.fit_params[2]
            )
        except (AttributeError, TypeError):
            pass
        return _str

    @property
    def timestamps(self):
        return [
            self.sampling_period * i for i in range(self._kinematic_profile.shape[0])
        ]

    @property
    def pvp_params(self):
        self._pvp_params = {
            "tau_index": numpy.argmax(self.std_prof),
            "tau": numpy.argmax(self.std_prof) * self.sampling_period,
            "sigma_0": numpy.max(self.std_prof),
            "Dtau": self.mean_prof[numpy.argmax(self.std_prof)],
        }
        return self._pvp_params

    @property
    def kinematic_profile(self):
        return self._kinematic_profile.T

    @kinematic_profile.setter
    def kinematic_profile(self, item):
        if len(item.shape) != 3:
            raise ValueError(
                f"The shape of kinematic profiles should be of length 3 (time, dimension, number of movements) but it has length {len(item.shape)}"
            )
        self._kinematic_profile = item

    @property
    def _reference_signal(self):
        return self.kinematic_profile

    def _remove_outliers(self, remove_outliers_k_sigma_away=3.5):
        """_remove_outliers

        Remove trajectory outliers, by removing all trajectories that are outside of the range (m +- k sigma), where m is the mean trajectory and sigma is the standard deviation of the set of trajectories.


        .. note:
            The formula above is based on the confidence interval for a Gaussian, and we apply it component per component. A true multivariate approach would use the confidence interval for a multivariate Gaussian see e.g. https://stats.stackexchange.com/questions/29860/confidence-interval-of-multivariate-gaussian-distribution

        :param remove_outliers_k_sigma_away: k, defaults to 3.5
        :type remove_outliers_k_sigma_away: float, optional
        :return: (index of removed trajectories in old array, new array)
        :rtype: tuple(list, array)
        """
        _indx = []
        k = remove_outliers_k_sigma_away
        for ncomp in range(self.kinematic_profile.shape[1]):
            mean = numpy.mean(self.kinematic_profile[:, ncomp, :], axis=0)
            std = numpy.std(self.kinematic_profile[:, ncomp, :], axis=0)
            for n, _traj in enumerate(self.kinematic_profile[:, ncomp, :]):
                if (_traj > mean + k * std).any() or (_traj < mean - k * std).any():
                    _indx.append(n)
        _indx = list(set(_indx))
        self._kinematic_profile = numpy.delete(self._kinematic_profile, _indx, axis=2)
        self.compute_profiles()
        self._removed_outliers += len(_indx)
        return _indx, self._kinematic_profile

    def plot_std_profiles(self, ax=None, fit=True, prof_kwargs=None, fit_kwargs=None):
        """plot_std_profiles

        Plots the standard deviation profiles on the provided axis. If not provided, will create a new figure from scratch.
        If fit is True, will also compute the spline fit to the second and third phase. Keyword arguments to the std plotter (prof_kwargs) and to the fit plotter (fit_kwargs) can also be given.

        .. note::

            You should have fitted the profiles prior to plotting them.

        :param ax: axis on which to draw, defaults to None. If None, creates a new figure and axis to draw on.
        :type ax: plt.axis, optional
        :param fit: whether to plot the spline fit, defaults to True
        :type fit: bool, optional
        :param prof_kwargs: keyword arguments are passed to plotter for the standard deviation profile, defaults to None
        :type prof_kwargs: dict, optional
        :param fit_kwargs: keyword arguments are passed to plotter for the spline fit, defaults to None
        :type fit_kwargs: dict, optional
        """

        if ax is None:
            _, ax = plt.subplots(1, 1)

        prof_kwargs = {} if prof_kwargs is None else prof_kwargs
        fit_kwargs = {} if fit_kwargs is None else fit_kwargs

        y = self.std_prof
        x = self.timestamps
        ax.semilogy(x, y, "k-", lw=3, label="PVP", **prof_kwargs)
        if fit:
            ax.semilogy(
                self.pvp_fit_x,
                self.pvp_fit_y,
                "r-",
                lw=3,
                label="Spline fit",
                **fit_kwargs,
            )
            ax.set_title(
                r"$\tau = {:.3f}, C = {{{:.1f}}}, \Omega = {:.1f}$".format(
                    self.pvp_params["tau"], -self.fit_params[1], self.fit_params[2]
                )
            )
        ax.grid(visible=True, which="minor", linestyle="--")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(r"$\sigma\mathrm{(t) (m)}$")

    def _compute_mean_profile(self):
        for k in range(self._reference_signal.shape[1]):
            self._mean_prof_incr = numpy.mean(self._reference_signal[:, k, :], axis=0)
            if k == 0:
                self.mean_prof = self._mean_prof_incr ** 2
            else:
                self.mean_prof += self._mean_prof_incr ** 2

        self.mean_prof = numpy.sqrt(self.mean_prof)

        return self.mean_prof

    def _compute_std_profile(self):
        for k in range(self._reference_signal.shape[1]):
            self._std_prof_incr = numpy.std(self._reference_signal[:, k, :], axis=0)
            if k == 0:
                self.std_prof = self._std_prof_incr ** 2
            else:
                self.std_prof += self._std_prof_incr ** 2

        self.std_prof = numpy.sqrt(self.std_prof)
        return self.std_prof

    def compute_profiles(self):
        """compute_profiles

        Computes the mean and standard deviation profiles for a set of trajectories.

        :return: (mean profile, standard deviation profile)
        :rtype: tuple(array, array)
        """
        self._compute_mean_profile()
        self._compute_std_profile()
        return self.mean_prof, self.std_prof

    def compute_pvp(self, remove_outliers_k_sigma_away=3.5):
        """compute_pvp

        Run the full PVP routine:

            + compute profiles
            + remove outliers k sigma away
            + fit profiles

        :param remove_outliers_k_sigma_away: remove outliers k sigma away, defaults to 3.5
        :type remove_outliers_k_sigma_away: float, optional
        :return: standard deviation profile, x and y values of the fit, kinematic profiles
        :rtype: tuple(array, array, array, array)
        """

        _, std_prof = self.compute_profiles()
        _, kinematic_profiles = self._remove_outliers(
            remove_outliers_k_sigma_away=remove_outliers_k_sigma_away
        )
        _, fit_x, fit_y = self._fit_profiles()
        return std_prof, fit_x, fit_y, kinematic_profiles

    def _fit_profiles(self, **optim_kwargs):

        ### Define cost function for optimization procedure
        def monospline(THETA, *args):
            x = args[0]
            y = args[1]
            a, b, mt = THETA
            out = 0
            for i, v in enumerate(x):
                if v < mt:
                    out += (a + b * v - y[i]) ** 2
                else:
                    out += (a + b * mt - y[i]) ** 2
            return out

        ## Once Omega has been determined, run a classical LR on the second phase to get LR diagnostics
        def get_fit_second_phase(y, indx_omega):
            x = [self.sampling_period * i for i in range(indx_omega)]
            yy = y[:indx_omega]
            xx = statsmodels.tools.add_constant(x)
            model = statsmodels.regression.linear_model.OLS(yy, xx)
            self.second_phase_fit = model.fit()
            return self.second_phase_fit

        indx_tau, tau, sigma0, Dtau = tuple(self.pvp_params.values())

        ### Initialize optimization algorithm - Data and start parameters
        theta0 = optim_kwargs.pop(
            "spline_param_guess", [sigma0, -5, 1]
        )  # should work for most cases
        if indx_tau:
            x = self.timestamps[0:-indx_tau]
            y = numpy.log2(self.std_prof[indx_tau:])
        else:
            x = self.timestamps
            y = numpy.log2(self.std_prof)

        ## Global Optimization
        n_iter = optim_kwargs.pop("basinhopping_n_iter", 50)

        res = opti.basinhopping(
            func=monospline,
            x0=theta0,
            niter=n_iter,
            minimizer_kwargs={
                "method": "Nelder-Mead",
                "args": (x, y),
                "options": {"maxiter": 1000, "disp": 0},
            },
        )

        a, b, c = res.x
        c0 = int(numpy.ceil(c / self.sampling_period))
        self.omega = c
        a, b = get_fit_second_phase(y, c0).params

        _yy = [a + b * i * self.sampling_period for i in range(0, c0)] + [
            a + c * b for i in range(c0, len(y[indx_tau:]))
        ]
        _yy = [2 ** v for v in _yy]
        t_fit = [
            self.pvp_params["tau"] + i * self.sampling_period
            for i in range(0, len(_yy))
        ]
        self.pvp_fit_x = t_fit
        self.pvp_fit_y = _yy
        self.fit_params = [a, b, c + self.pvp_params["tau"]]
        return self.fit_params, self.pvp_fit_x, self.pvp_fit_y

    def _extend(self, trajectory, extend_to=3):
        """_extend extend trajectories

        Extends the self._kinematic_profile buffer with a new trajectory while ensuring the series in the buffer always have the same size as the trajectory. For example, if the buffer has shape (X, Y) and the trajectory series has length (Z):

            + if Z > Y, then the buffer is filled with the last values to reach shape (X, Z)
            + if Z < Y, then the trajectory is filled with the last value to reach shape (1, Y)

        The minimum duration of the series can be set with extend_to.

        :param trajectory: trajectory to add to the self._kinematic_profile buffer
        :type trajectory: array_like
        :param extend_to: minimum duration of the series in seconds, defaults to 3
        :type extend_to: int, optional
        """
        if len(trajectory.shape) == 1:
            trajectory = trajectory.reshape(-1, 1)
        if self._kinematic_profile is None:  # First traj
            Nmin = 1 + int(numpy.ceil(extend_to / self.sampling_period))
            if trajectory.shape[0] < Nmin:
                fill = numpy.full(
                    shape=(Nmin - trajectory.shape[0], trajectory.shape[1]),
                    fill_value=trajectory[-1, :],
                )
                trajectory = numpy.concatenate((trajectory, fill), axis=0)
            self._kinematic_profile = numpy.expand_dims(trajectory, axis=2)
        else:
            if self._kinematic_profile.shape[0] < trajectory.shape[0]:
                fill = numpy.full(
                    shape=(
                        -self._kinematic_profile.shape[0] + trajectory.shape[0],
                        self._kinematic_profile.shape[1],
                        self._kinematic_profile.shape[2],
                    ),
                    fill_value=self._kinematic_profile[-1, :, :],
                )

                self._kinematic_profile = numpy.concatenate(
                    (self._kinematic_profile, fill), axis=0
                )

            elif self._kinematic_profile.shape[0] > trajectory.shape[0]:
                fill = numpy.full(
                    shape=(
                        self._kinematic_profile.shape[0] - trajectory.shape[0],
                        self._kinematic_profile.shape[1],
                    ),
                    fill_value=trajectory[-1, :],
                )
                trajectory = numpy.concatenate((trajectory, fill), axis=0)
            self._kinematic_profile = numpy.concatenate(
                (self._kinematic_profile, numpy.expand_dims(trajectory, axis=2)), axis=2
            )
        return self._kinematic_profile

    def _find_start(self, container, method="speed_threshold", **kwargs):
        """_find_start correct start

        Trajectories may not always be consistently segmented. This function performs a correction for the start point, as indicated by the method.

            + method = 'speed_threshold' :
                Computes a threshold for speed as x_percent * max speed. All points the target and the first time when the threshold is crossed are removed.
                \*\*kwargs = {'percent' : x_percent}

        :param container: output from add_traj
        :type container: numpy.ndarray
        :param method: method to correct start, defaults to "speed_threshold"
        :type method: str, optional
        :return: trajectory with correction for speed
        :rtype: numpy.ndarray
        """
        time, traj, speed = container

        indx = 1
        if method == "speed_threshold":
            ### Removes points until having reached a speed that is 1% of the max speed.
            max_speed = numpy.max(numpy.abs(speed[1:]))
            percent = kwargs.get("percent", 1)
            while abs(speed[indx]) < max_speed * percent / 100:
                indx += 1
        else:
            raise NotImplementedError(
                "Only method speed_threshold is implemented for now."
            )

        container = numpy.concatenate(
            (time[indx:].reshape(1, -1), traj[indx:].reshape(1, -1)), axis=0
        )
        container = numpy.concatenate((container, speed[indx:].reshape(1, -1)), axis=0)
        return container, indx

    def plot_kinematic_profiles(self, ax=None, **kwargs):
        """plot_kinematic_profiles

        Plots the kinematic profiles on the provided axis. If not provided, will create a new figure from scratch.

        :param ax: axis on which to draw, defaults to None. If None, creates a new figure and axis to draw on.
        :type ax: plt.axis, optional
        :param **kwargs: keyword arguments are passed to plt.plot()
        :type **kwargs: key-values
        """
        if ax is None:
            fig, ax = plt.subplots(1, 2)

        x = self.timestamps
        for k in range(self.kinematic_profile.shape[1]):
            for y in self.kinematic_profile[:, k, :]:
                ax[k].plot(x, y, "-", **kwargs)
                ax[k].set_xlabel("Time (s)")
                ax[k].set_ylabel("Position")

    def add_trajectory(self, t, *args, extend_to=3, target=None, correct_start=False):
        """Add trajectory to the set from which PVPs are computed

        Pass the time series, and any number of positional series. For example in dim3 with x, y, z, you would call (with defaults kwargs)

        .. code-block:: python

            pvp.add_trajectory(t, x, y, z, extend_to = 3, target = None, correct_start = False)

        You control the duration of the PVP (e.g. how far in time trajectories are extended). You also need to specify the target location for each trajectory. You can optionally synchronize the trajectories by pre-processing them (correct_start). Currently, a simple thresholding rule takes care of this synchronization.

        :param t: time series
        :type t: numpy.array like
        :param args: positional series
        :type args: numpy.array like
        :param extend_to: minimal PVP duration, defaults to 3
        :type extend_to: int, optional
        :param target: target location, defaults to None. If None, will use the null vector as target.
        :type target: iterable, optional
        :param correct_start: whether to correct the location of the start of the movement for synchronization, defaults to False
        :type correct_start: bool, optional
        """

        target = [0 for i in args] if target is None else target
        projections = self._project(target, *args)

        container = self._interp_filt(
            numpy.array(t),
            *projections,
            deriv=0,
            resampling_period=self.sampling_period,
        )

        indx = 0
        if correct_start:
            _norm = numpy.sqrt(numpy.sum(container[1, :, :] ** 2, axis=1))
            tmp_container = self._interp_filt(
                container[0, :, 0],
                _norm,
                deriv=1,
                resampling_period=self.sampling_period,
            )
            _, indx = self._find_start(
                tmp_container, method="speed_threshold", percent=2
            )
        container = container[:, indx:, :]

        self._extend(container[1, :, :], extend_to)

    def _get_orthonormal_basis(self, target, x0):
        target = numpy.asarray(target).squeeze()
        x0 = numpy.atleast_1d(numpy.asarray(x0).squeeze())
        if x0.shape[0] == 1:
            return self._bon1(target, x0)
        elif x0.shape[0] == 2:
            return self._bon2(target, x0)
        elif x0.shape[0] == 3:
            return self._bon3(target, x0)
        else:
            raise NotImplementedError("Dimensions above 3 are not supported yet. ")

    # below does not reliably produce an orthonormal basis
    # switching to a manual cse disjunction up to 3D for now

    # def _get_orthonormal_basis(self, target, x0):
    #     target = numpy.asarray(target).squeeze()
    #     x0 = numpy.asarray(x0).squeeze()
    #     random_basis = numpy.array(
    #         [
    #             (target - x0),
    #             *[
    #                 -1 + 2 * numpy.random.random(x0.shape[0])
    #                 for v in range(x0.shape[0] - 1)
    #             ],
    #         ]
    #     ).T
    #     self.Q, _ = numpy.linalg.qr(random_basis)
    #     return self.Q

    def _bon1(self, target, x0):
        return normalize(target - x0).reshape(-1, 1)

    def _bon2(self, target, x0):
        v1 = normalize(target - x0)
        v2 = numpy.array([-v1[1], v1[0]])
        return numpy.array([[v1], [v2]]).T

    def _bon3(self, target, x0):
        array = self._bon2(target, x0).T
        vec3 = numpy.cross(array[0], array[1])
        return numpy.array([[array[0]], [array[1]], [vec3]]).T

    def _project_x(self, Q, target, x):
        u = (numpy.asarray(x) - numpy.asarray(target)).reshape(-1, 1)
        return (Q.T @ u).squeeze()

    def _project(self, target, *args):
        dim = len(args)
        output = numpy.zeros(shape=(dim, len(args[0])))
        args = numpy.array(args).T
        Q = self._get_orthonormal_basis(target, args[0, :])
        for n, arg in enumerate(args):
            output[:, n] = self._project_x(Q, target, arg)
        return output

    def _interp_filt(
        self,
        t,
        *args,
        resampling_period=0.01,
        filter_kwargs={"filtername": "kaiser", "fc": 10, "rdb": 10, "width": 5},
        deriv=2,
    ):
        """_interp_filt interpolates and filters a 1D trajectory

        Takes a trajectory, resamples it with the chosen resampling_period and filters it with the given filter. Also provides the unfiltered derivatives up to order "deriv".

        :param t: trajectory time
        :type t: array like
        :param x: trajectory position
        :type x: array like
        :param resampling_period: timestep at which the trajectory will be down/over sampled, defaults to 0.01
        :type resampling_period: float, optional
        :param filter_kwargs: scipy.signal filter description, defaults to {"filtername": "kaiser", "fc": 10, "rdb": 10, "width": 5}
        :type filter_kwargs: dict, optional
        :param deriv: order for the trajectory derivatives, defaults to 2
        :type deriv: int, optional
        :return: an array, where the first line is the time vector, and all other lines are the nth derivatives of the trajectory (0 <= n <= deriv).
        :rtype: numpy.ndarray
        """

        t = numpy.asarray(t)
        t = t - t[0]  # set null time target
        Ts = resampling_period
        output_container = None
        for n, x in enumerate(args):
            x = numpy.asarray(x)
            interpolator = interp.interp1d(t, x, fill_value="extrapolate")
            resampling_instants = numpy.linspace(
                0,
                t[-1] + (Ts - t[-1] % Ts),
                num=1 + int((t[-1] + (Ts - t[-1] % Ts)) / Ts),
            )
            x_interp = interpolator(resampling_instants)

            if filter_kwargs["filtername"] == "kaiser":
                N, beta = signal.kaiserord(
                    filter_kwargs["rdb"], filter_kwargs["width"] * 2 * Ts
                )
                taps = signal.firwin(
                    N, filter_kwargs["fc"] * 2 * Ts, window=("kaiser", beta)
                )
                filtered_x = signal.filtfilt(taps, 1, x_interp)
            else:
                b, a = filter_kwargs["b"], filter_kwargs["a"]
                filtered_x = signal.filtfilt(b, a, x_interp)

            container = numpy.concatenate(
                (resampling_instants.reshape(1, -1), filtered_x.reshape(1, -1)), axis=0
            )

            ## Compute derivatives
            resampling_instants = numpy.append(
                resampling_instants, resampling_instants[-1] + Ts
            )
            for i in range(deriv):
                filtered_x = numpy.concatenate(
                    (
                        filtered_x.reshape(-1)[0].reshape(1, -1),
                        filtered_x.reshape(1, -1),
                    ),
                    axis=1,
                )
                filtered_x = numpy.divide(
                    numpy.diff(filtered_x), numpy.diff(resampling_instants)
                )
                container = numpy.concatenate((container, filtered_x), axis=0)

            if n == 0:
                output_container = numpy.expand_dims(container, axis=2)
            else:
                container = numpy.expand_dims(container, axis=(2))
                output_container = numpy.concatenate(
                    (output_container, container), axis=2
                )
        return output_container


class PVP_alpha(PVP):
    @property
    def _reference_signal(self):
        return numpy.expand_dims(self.kinematic_profile[:, 0, :], 1)


class PVP_total(PVP):
    @property
    def _reference_signal(self):
        return self.kinematic_profile


class PVP_generalized(PVP):
    @property
    def _reference_signal(self):
        return self.kinematic_profile

    def _compute_std_profile(self):
        std_prof = numpy.empty(shape=(self._kinematic_profile.shape[0]))
        for nt, t in enumerate(self._kinematic_profile):
            cov = numpy.cov(t)
            if len(cov.shape) >= 2:
                std_prof[nt] = (numpy.linalg.det(cov)) ** (
                    1 / 2 / self._kinematic_profile.shape[1]
                )
            else:
                std_prof[nt] = (cov.squeeze()) ** (
                    1 / 2 / self._kinematic_profile.shape[1]
                )
        self.std_prof = std_prof
        return self.std_prof


def normalize(a):
    return a / numpy.linalg.norm(a, 2)
