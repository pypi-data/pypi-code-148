import numpy as np
import pandas as pd
import math
import random
import scipy
import scipy.interpolate


def brownian_bridge(x1, x2, y1, y2, x_delta_max=0.5, sigma_factor=0.25):
    """
    Make a series using the Brownian bridge method.

    Génération de pont brownien par dichotomie afin de relier deux instants
    (et leurs températures associées) avec des ponts browniens
    d'un pas de temps inférieur au paramètre x_delta_max.

    Parameters
    ----------
    x1 : float
        Abscissa of the starting point
    x2 : float
        Abscissa of the ending point
    y1 : float
        Ordinate of the starting point
    y2 : float
        Ordinate of the ending point
    x_delta_max : float, optional
        [description], by default 0.5
    sigma_factor : float, optional
        [description], by default 0.25

    Returns
    -------
    [type]
        [description]
    """
    y_list = [y1, y2]
    x_list = [x1, x2]
    x_delta = x2 - x1

    while x_delta > x_delta_max:
        num_segments = len(y_list) - 1
        segment_index_offset = 0

        # FOR EACH SEGMENT
        for segment_index in range(0, num_segments):
            i = segment_index + segment_index_offset
            _y1, _x1, _y2, _x2 = y_list[i], x_list[i], y_list[i + 1], x_list[i+1]

            mu = (_y1 + _y2) / 2.
            sigma = x_delta * sigma_factor

            y_drawn = np.random.normal(mu, sigma)

            y_list = y_list[:i+1] + [y_drawn] + y_list[i+1:]
            x_list = x_list[:i+1] + [(_x1 + _x2) * 0.5] + x_list[i+1:]

            segment_index_offset += 1

        x_delta = x_delta / 2.

    return x_list, y_list


def gen_daily_outside_temperature_list(monthly_outside_temperature_list, sigma_factor=0.05, num_days=365):
    '''
    On donne une valeur pour chaque premier du mois en entrée. Et on fait des ponts browniens entre chaque points et on 
    descend par dichotomie. 
    Pour 1 an, on met 1 janvier, 1 février, ..., 1 décembre et 31 décembre.
    On suppose qu'un mois fait 30 jours (donc l'année est plus courte qu'une vraie année, ça nous suffit pour l'instant).
    
    En sortie, on a donc deux listes, les incréments de temps accumulés ET les temperatures à chaque instant discret.
    A noter qu'il y a une légère discontinuité dans les pas de temps 1 fois par mois. En effet, au changement de mois, 
    on a un pas de temps de 1. On pourra éventuellement changé cela plus tard.
    '''
    # allure générale
    daily_temperature_on_year_list = []
    daily_time_on_year_list = []

    num_months = len(monthly_outside_temperature_list) - 1

    for i in range(0, num_months-1):
        times_mois, temperatures_mois = brownian_bridge(30*i,
                                                        30*(i+1),
                                                        monthly_outside_temperature_list[i],
                                                        monthly_outside_temperature_list[i+1],
                                                        sigma_factor=sigma_factor)
        daily_temperature_on_year_list += temperatures_mois[:-1]
        daily_time_on_year_list += times_mois[:-1]

    times_mois, temperatures_mois = brownian_bridge(30*(num_months-1),
                                                    max(30*num_months, num_days),
                                                    monthly_outside_temperature_list[num_months-1],
                                                    monthly_outside_temperature_list[num_months],
                                                    sigma_factor=sigma_factor)
    daily_temperature_on_year_list += temperatures_mois
    daily_time_on_year_list += times_mois

    return daily_time_on_year_list, daily_temperature_on_year_list


def gen_hourly_outside_temperature_list(monthly_outside_temperature_list, monthly_sigma_factor=0.05, daily_fluctuation_mu=5., daily_fluctuation_sigma=0.25, num_hours=8760):
    '''
    On ajoute des fluctiations journalières
    '''
    daily_time_on_year_list, daily_temperature_on_year_list = gen_daily_outside_temperature_list(monthly_outside_temperature_list,
                                                                                                 sigma_factor=monthly_sigma_factor,
                                                                                                 num_days=math.ceil(num_hours / 24.))

    # interpolation et rafinement du profil journalier
    f = scipy.interpolate.interp1d(np.array(daily_time_on_year_list) * 24,
                                   daily_temperature_on_year_list,
                                   kind='linear',
                                   fill_value='extrapolate')

    hourly_time_on_year_array = np.arange(num_hours)
    hourly_temperature_on_year_array = f(hourly_time_on_year_array)

    hourly_temperature_fluctuation_on_year_array = np.random.normal(daily_fluctuation_mu, daily_fluctuation_sigma, size=num_hours) * np.sin(2. * np.pi * hourly_time_on_year_array / 24. + 1.2 * np.pi)
    hourly_temperature_on_year_array += hourly_temperature_fluctuation_on_year_array

    return hourly_time_on_year_array, hourly_temperature_on_year_array


DEFAULT_NUM_TIMESTEPS_TO_KEEP = None
#DEFAULT_NUM_TIMESTEPS_TO_KEEP = 24*7

DEFAULT_MONTHLY_OUTSIDE_TEMPERATURE_LIST = [5, 5, 7, 10, 15, 22, 25, 25, 21, 15, 10, 7, 5]

DEFAULT_INITIAL_MONTH = 5     # 0 = January      # Commence durrant l'été pour pouvoir constituer un stock de chaleur avant l'hiver

#DEFAULT_MONTHLY_OUTSIDE_TEMPERATURE_SIGMA = 0.1
DEFAULT_MONTHLY_OUTSIDE_TEMPERATURE_SIGMA = 0.


class BrownianBridge:
    def __init__(self,
                 monthly_temperature_sigma=DEFAULT_MONTHLY_OUTSIDE_TEMPERATURE_SIGMA,
                 num_time_steps_to_keep=DEFAULT_NUM_TIMESTEPS_TO_KEEP,
                 initial_month=DEFAULT_INITIAL_MONTH,
                 orig_monthly_outside_temperature_list=DEFAULT_MONTHLY_OUTSIDE_TEMPERATURE_LIST,
                 monthly_sigma_factor=0.05,
                 daily_fluctuation_mu=5.,
                 daily_fluctuation_sigma=0.25):
        self.monthly_temperature_sigma = monthly_temperature_sigma
        self.num_time_steps_to_keep = num_time_steps_to_keep
        self.initial_month = initial_month
        self.orig_monthly_outside_temperature_list = orig_monthly_outside_temperature_list
        self.monthly_outside_temperature_list = orig_monthly_outside_temperature_list[initial_month:] + orig_monthly_outside_temperature_list[:initial_month]
        self.monthly_sigma_factor = monthly_sigma_factor
        self.daily_fluctuation_mu = daily_fluctuation_mu
        self.daily_fluctuation_sigma = daily_fluctuation_sigma

    def __call__(self):
        monthly_outside_temperature_array = np.random.normal(self.monthly_outside_temperature_list, self.monthly_temperature_sigma)

        time_list, temperature_list = gen_hourly_outside_temperature_list(monthly_outside_temperature_array,
                                                                          monthly_sigma_factor=self.monthly_sigma_factor,
                                                                          daily_fluctuation_mu=self.daily_fluctuation_mu,
                                                                          daily_fluctuation_sigma=self.daily_fluctuation_sigma)

        if self.num_time_steps_to_keep is not None:
            time_list, temperature_list = time_list[:self.num_time_steps_to_keep], temperature_list[:self.num_time_steps_to_keep]

        df = pd.DataFrame(np.array([time_list, temperature_list]).T,
                          columns=("hours", "temperature"))

        hours_per_timestep = time_list[1] - time_list[0]
        df['indicative_date'] = pd.date_range(start='2020-{:02d}-01'.format(self.initial_month + 1), periods=len(df), freq=str(hours_per_timestep) + 'H')

        return df

    def params(self):
        params_dict = {
            "monthly_temperature_sigma": self.monthly_temperature_sigma,
            "num_time_steps_to_keep": self.num_time_steps_to_keep,
            "initial_month": self.initial_month,
            "orig_monthly_outside_temperature_list": self.orig_monthly_outside_temperature_list
        }
        return params_dict

    def __str__(self):
        return "brownianbridge," + ",".join(["{}:{}".format(k, v) for k, v in self.params().items()])


gen_weather_time_series_with_brownian_bridge = BrownianBridge()