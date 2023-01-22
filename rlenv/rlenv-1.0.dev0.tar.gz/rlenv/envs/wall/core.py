import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys
import warnings

import gym

import rlenv
from rlenv.sed.wall import Wall

DEFAULT_WEATHER_GENERATOR = rlenv.weather.generator.brownianbridge.gen_weather_time_series_with_brownian_bridge
DEFAULT_FORECAST_GENERATOR = rlenv.weather.forecast.bogus.gen_weather_forecast
DEFAULT_THERMAL_NEEDS_GENERATOR = Wall(setpoint_degree=18.)

# Accenta env ################################################################################################

# https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html
# https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e

def degree_celsius_to_kelvin(degree_celsius):
    return degree_celsius + 273.15

def kelvin_to_degree_celsius(kelvin):
    return kelvin - 273.15


ETA = 0.25    # TODO   2
RHO = 0.9     # TODO   0.9

DELTA_TEMP_COND = 5.
TEMP_BAT_IN_K = degree_celsius_to_kelvin(35.)
TEMP_BAT_OUT_K = TEMP_BAT_IN_K - DELTA_TEMP_COND


def efficiency_func(current_weather_degree_celsius, eta=ETA, cop_max=8.):
    current_weather_kelvin = degree_celsius_to_kelvin(current_weather_degree_celsius)

    if current_weather_kelvin >= TEMP_BAT_OUT_K:
        cop_carnot = float("inf")
    else:
        cop_carnot = TEMP_BAT_OUT_K / (TEMP_BAT_OUT_K - current_weather_kelvin)

    cop = cop_carnot * ETA
    cop = min(cop, cop_max)   # COP can't be > than 8

    return cop


class AccentaEnv(gym.Env):
    """
    Custom Environment that follows gym interface

    Parameters
    ----------
    weather_generator : _type_, optional
        _description_, by default None
    weather_forecast_generator : _type_, optional
        _description_, by default None
    thermal_needs_generator : _type_, optional
        _description_, by default None
    record_logs : bool, optional
        _description_, by default True
    state_contains_daily_time_indicator : bool, optional
        _description_, by default False
    state_contains_weekly_time_indicator : bool, optional
        _description_, by default False
    state_contains_yearly_time_indicator : bool, optional
        _description_, by default True
    """

    metadata = {'render.modes': ['human']}   # TODO: ???

    def __init__(self,
                 weather_generator=None,
                 weather_forecast_generator=None,
                 thermal_needs_generator=None,
                 record_logs=True,
                 state_contains_daily_time_indicator: bool = False,
                 state_contains_weekly_time_indicator: bool = False,
                 state_contains_yearly_time_indicator: bool = True):
        super(AccentaEnv, self).__init__()    # Define action and observation space

        if weather_generator is None:
            weather_generator = DEFAULT_WEATHER_GENERATOR

        if weather_forecast_generator is None:
            weather_forecast_generator = DEFAULT_FORECAST_GENERATOR

        if thermal_needs_generator is None:
            thermal_needs_generator = DEFAULT_THERMAL_NEEDS_GENERATOR
        
        self.gen_weather_time_series = weather_generator
        self.gen_weather_forecast = weather_forecast_generator

        self.thermal_needs_generator = thermal_needs_generator

        self.state_contains_daily_time_indicator = state_contains_daily_time_indicator
        self.state_contains_weekly_time_indicator = state_contains_weekly_time_indicator
        self.state_contains_yearly_time_indicator = state_contains_yearly_time_indicator
        
        # Constants

        self.MAX_STORAGE_CAPACITY = 500.      # Battery capacity
        self.MAX_ENERGY_ELEC_PROD = 200
        self.MAX_THERMAL_ENERGY_EXTRACT = self.MAX_STORAGE_CAPACITY / 5.
        self.WEATHER_FORECAST_LEN = 6  # i.e. 24 / 4    # 24 hours horizon but with 4 hours time steps

        ###

        self.weather_df = None
        self.weather_forecast_series = None
        self.thermal_needs_df = None

        self.current_weather = None # temperature
        self.current_thermal_needs_kwh = None
        self.current_storage_level_kwh = None
        self.current_time = None
        
        self.record_logs = record_logs

        # Actions: a1, a2, a3
        self.action_space_max_array = np.array([self.MAX_ENERGY_ELEC_PROD, self.MAX_ENERGY_ELEC_PROD, self.MAX_THERMAL_ENERGY_EXTRACT])
        self.action_space = gym.spaces.Box(low=np.array([0., 0., 0.]),
                                           high=self.action_space_max_array,
                                           dtype=np.float32)

        # State: (current_weather, current_thermal_needs_kwh, current_storage_level_kwh, current_time, weather_forecast_series)
        state_lower_bounds_list = [
            -40.,                         # self.current_weather
            0.,                           # self.current_thermal_needs_kwh
            0.,                           # self.current_storage_level_kwh
        ]

        state_upper_bounds_list = [
            50.,                          # self.current_weather
            1000.,                        # self.current_thermal_needs_kwh
            self.MAX_STORAGE_CAPACITY,    # self.current_storage_level_kwh
        ]

        if self.state_contains_daily_time_indicator:
            state_lower_bounds_list += [-1., -1.]
            state_upper_bounds_list += [1., 1.]

        if self.state_contains_weekly_time_indicator:
            state_lower_bounds_list += [-1., -1.]
            state_upper_bounds_list += [1., 1.]

        if self.state_contains_yearly_time_indicator:
            state_lower_bounds_list += [-1., -1.]
            state_upper_bounds_list += [1., 1.]
        
        state_lower_bounds_list += [-40. for i in range(self.WEATHER_FORECAST_LEN)]
        state_upper_bounds_list += [+50. for i in range(self.WEATHER_FORECAST_LEN)]

        self.observation_space = gym.spaces.Box(low=np.array(state_lower_bounds_list),
                                                high=np.array(state_upper_bounds_list),
                                                dtype=np.float32)


    def _reward(self, a1, a2, a3):
        #a1, a2, a3 = action
        
        e = max(0., self.current_thermal_needs_kwh - (a3 + a1 * self.efficiency()))    # e must be greater than 0
        assert e >= 0.

        reward = -a1 - a2 - e / RHO

        assert math.isfinite(reward), "reward: {}, a1: {}, a2: {}, a3: {}, e: {}, current_thermal_needs_kwh: {}, {}, t: {}".format(reward, a1, a2, a3, e, self.current_thermal_needs_kwh, self.current_thermal_needs_kwh - (a3 + a1 * self.efficiency()), self.current_time)

        if self.current_thermal_needs_kwh > 0. and a3 == 0.:
            assert reward < 0., "reward: {}, a1: {}, a2: {}, a3: {}, e: {}, current_thermal_needs_kwh: {}, {}, t: {}".format(reward, a1, a2, a3, e, self.current_thermal_needs_kwh, self.current_thermal_needs_kwh - (a3 + a1 * self.efficiency()), self.current_time)
        else:
            assert reward <= 0., "reward: {}, a1: {}, a2: {}, a3: {}, e: {}, current_thermal_needs_kwh: {}, {}, t: {}".format(reward, a1, a2, a3, e, self.current_thermal_needs_kwh, self.current_thermal_needs_kwh - (a3 + a1 * self.efficiency()), self.current_time)

        # Logs
        if self.record_logs:
            self.logs[self.current_time]["a1"] = float(a1)
            self.logs[self.current_time]["a2"] = float(a2)
            self.logs[self.current_time]["a3"] = float(a3)
            self.logs[self.current_time]["e"] = float(e)
            self.logs[self.current_time]["reward"] = float(reward)
        
        return reward


    def efficiency(self):
        return efficiency_func(self.current_weather)


    def step(self, action):
        # Execute one time step within the environment
        self.current_time += 1

        a1, a2, a3 = action

        # Logs
        if self.record_logs:
            self.logs[self.current_time] = {
                "raw_a1": float(a1),
                "raw_a2": float(a2),
                "raw_a3": float(a3)
            }
        
        #print("before", a1, a2, a3, self.current_storage_level_kwh)

        assert a1 >= 0.    #a1 = max(a1, 0.)
        a1 = min(a1, self.MAX_ENERGY_ELEC_PROD)

        ## DESTOCK #########

        assert 0 <= self.current_storage_level_kwh <= self.MAX_STORAGE_CAPACITY
        assert a3 >= 0.    #a3 = max(a3, 0.)
        a3 = min(a3, self.current_storage_level_kwh)
        self.current_storage_level_kwh -= a3

        ## STOCK ###########

        assert a2 >= 0.    #a2 = max(a2, 0.)
        a2_th = a2 * self.efficiency()
        a2_th = min(self.MAX_STORAGE_CAPACITY - self.current_storage_level_kwh, a2_th)
        assert a2_th >= 0.    #a2 = max(a2, 0.)  # TODO
        self.current_storage_level_kwh += a2_th
        assert 0 <= self.current_storage_level_kwh <= self.MAX_STORAGE_CAPACITY, self.current_storage_level_kwh          #self.current_storage_level_kwh = max(self.current_storage_level_kwh, 0.)   # TODO

        self.current_weather = self.weather_df.iloc[self.current_time]["temperature"]     # temperature
        self.current_thermal_needs_kwh = self.thermal_needs_df.iloc[self.current_time]["heat_needs"]
        assert self.current_thermal_needs_kwh >= 0.

        self.weather_forecast_series = self.gen_weather_forecast(weather_series=self.weather_df.temperature,
                                                                 start_index=self.current_time,
                                                                 end_index=self.current_time + self.WEATHER_FORECAST_LEN)

        obs = self._get_state()

        # Compute reward and done
        reward = self._reward(a1, a2, a3)
        done = self.current_time > len(self.weather_df) - self.WEATHER_FORECAST_LEN

        # Logs
        if self.record_logs:
            self.logs[self.current_time]["current_weather"] = float(self.current_weather)
            self.logs[self.current_time]["cop"] = float(self.efficiency())
            self.logs[self.current_time]["a1_th"] = float(a1 * self.efficiency())
            self.logs[self.current_time]["a2_th"] = float(a2 * self.efficiency())
            self.logs[self.current_time]["current_thermal_needs_kwh"] = float(self.current_thermal_needs_kwh)
            self.logs[self.current_time]["current_weather_forecast"] = float(self.weather_forecast_series[0])
            self.logs[self.current_time]["current_storage_level_kwh"] = float(self.current_storage_level_kwh)

            for state_index, state_value in enumerate(obs):
                self.logs[self.current_time]["s{}".format(state_index)] = float(state_value)

        return obs, reward, done, {}


    def _get_state(self):
        t = self.weather_df.iloc[self.current_time]["hours"]

        state_list = [self.current_weather, self.current_thermal_needs_kwh, self.current_storage_level_kwh]

        if self.state_contains_daily_time_indicator:
            state_list += [
                np.sin(2. * np.pi / 24. * t),
                np.cos(2. * np.pi / 24. * t)
            ]

        if self.state_contains_weekly_time_indicator:
            state_list += [
                np.sin(2. * np.pi / (7. * 24.) * t),
                np.cos(2. * np.pi / (7. * 24.) * t)
            ]

        if self.state_contains_yearly_time_indicator:
            state_list += [
                np.sin(2. * np.pi / (365. * 24.) * t),
                np.cos(2. * np.pi / (365. * 24.) * t)
            ]
        
        state_list += self.weather_forecast_series

        return np.array(state_list)


    def reset(self):
        """
        Reset the state of the environment to an initial state

        Returns
        -------
        _type_
            The initial state
        """

        self.current_time = 1

        self.weather_df = self.gen_weather_time_series()
        self.weather_forecast_series = self.gen_weather_forecast(weather_series=self.weather_df.temperature,
                                                                 start_index=self.current_time,
                                                                 end_index=self.current_time + self.WEATHER_FORECAST_LEN)
        self.thermal_needs_df = self.thermal_needs_generator(self.weather_df)
        self.thermal_needs_df['indicative_date'] = pd.to_datetime(self.thermal_needs_df.indicative_date)

        self.current_weather = self.weather_df.iloc[self.current_time]["temperature"]                  # temperature
        self.current_thermal_needs_kwh = self.thermal_needs_df.iloc[self.current_time]["heat_needs"]
        self.current_storage_level_kwh = 0.

        # Logs
        self.logs = {}

        return self._get_state()


    def render(self, mode='human'):
        print(self._get_state())


    def logs_to_df(self):
        df = pd.read_json(json.dumps(self.logs), orient="index")
        return df


    def plot(self, figsize=(30,10)):
        df = self.logs_to_df()
        ax = df.plot(figsize=figsize)
        ax.axhline(self.MAX_STORAGE_CAPACITY, color="red")
        return ax


    def params(self):
        params_dict = {
            # "monthly_temperature_sigma": self.monthly_temperature_sigma,
            # "num_time_steps_to_keep": self.num_time_steps_to_keep,
            # "initial_month": self.initial_month,
            # "orig_monthly_outside_temperature_list": self.orig_monthly_outside_temperature_list,
            #
            "weather_generator": {
                "class": self.gen_weather_time_series.__class__.__name__,
                "params": self.gen_weather_time_series.params()
            },
            "weather_forecast_generator": {
                "class": self.gen_weather_forecast.__class__.__name__,
                "params": self.gen_weather_forecast.params()
            },
            "thermal_needs_generator": {
                "class": self.thermal_needs_generator.__class__.__name__,
                # "params": self.thermal_needs_generator.params()               # TODO
            },
            #
            "state_contains_daily_time_indicator": self.state_contains_daily_time_indicator,
            "state_contains_weekly_time_indicator": self.state_contains_weekly_time_indicator,
            "state_contains_yearly_time_indicator": self.state_contains_yearly_time_indicator,
            #
            "max_storage_capacity": self.MAX_STORAGE_CAPACITY,
            "max_energy_elec_prod": self.MAX_ENERGY_ELEC_PROD,
            "max_thermal_energy_extract": self.MAX_THERMAL_ENERGY_EXTRACT,
            "weather_forecast_len": self.WEATHER_FORECAST_LEN,
            #
            "eta": ETA,
            "rho": RHO,
            #
            # DELTA_TEMP_COND = 5.
            # TEMP_BAT_IN_K = degree_celsius_to_kelvin(35.)
            # TEMP_BAT_OUT_K = TEMP_BAT_IN_K - DELTA_TEMP_COND
        }
        return params_dict


    def __str__(self):
        return "wall," + ",".join(["{}:{}".format(k, v) for k, v in self.params().items()])


    @classmethod
    def eval(cls,
             model,
             weather_generator=None,
             weather_forecast_generator=None,
             thermal_needs_generator=None,
             state_contains_daily_time_indicator: bool = False,
             state_contains_weekly_time_indicator: bool = False,
             state_contains_yearly_time_indicator: bool = True,
             num_episodes: int = 10,
             verbose: bool = False,
             aggregation_method: str = "mean") -> float:
        """
        Assess the give policy.

        Parameters
        ----------
        model : _type_
            The policy to assess
        weather_generator : _type_, optional
            _description_, by default None
        weather_forecast_generator : _type_, optional
            _description_, by default None
        thermal_needs_generator : _type_, optional
            _description_, by default None
        state_contains_daily_time_indicator : bool, optional
            _description_, by default False
        state_contains_weekly_time_indicator : bool, optional
            _description_, by default False
        state_contains_yearly_time_indicator : bool, optional
            _description_, by default True
        num_episodes : int, optional
            _description_, by default 10
        verbose : bool, optional
            _description_, by default False
        aggregation_method : str, optional
            _description_, by default "mean"

        Returns
        -------
        float
            Aggregated rewards obtained with the given policy

        Raises
        ------
        ValueError
            _description_
        """

        if weather_generator is None:
            weather_generator = DEFAULT_WEATHER_GENERATOR

        if weather_forecast_generator is None:
            weather_forecast_generator = DEFAULT_FORECAST_GENERATOR

        if thermal_needs_generator is None:
            thermal_needs_generator = DEFAULT_THERMAL_NEEDS_GENERATOR

        env = cls(weather_generator=weather_generator,
                  weather_forecast_generator=weather_forecast_generator,
                  thermal_needs_generator=thermal_needs_generator,
                  record_logs=False,
                  state_contains_daily_time_indicator=state_contains_daily_time_indicator,
                  state_contains_weekly_time_indicator=state_contains_weekly_time_indicator,
                  state_contains_yearly_time_indicator=state_contains_yearly_time_indicator)

        reward_list = []

        for episode_index in range(num_episodes):

            reward_sum = 0

            obs = env.reset()
            done = False

            while not done:
                action, _states = model.predict(obs)
                obs, reward, done, info = env.step(action)
                reward_sum += reward
                #env.render()           # Cannot render on Google Colab

            reward_list.append(reward_sum)

        reward_series = pd.Series(reward_list)

        try:
            aggregated_result = reward_series.aggregate(aggregation_method)
        except AttributeError as e:
            raise ValueError(f"Unknown aggregation method {aggregation_method} (c.f. https://pandas.pydata.org/docs/reference/api/pandas.Series.aggregate.html for valid options)")

        if verbose:
            print("Aggregated result:", aggregated_result)
            print("Stats:", reward_series.describe())

        env.close()

        return aggregated_result


    @classmethod
    def gen_one_episode(cls,
                        model, 
                        weather_generator=None,
                        weather_forecast_generator=None,
                        thermal_needs_generator=None,
                        state_contains_daily_time_indicator: bool = False,
                        state_contains_weekly_time_indicator: bool = False,
                        state_contains_yearly_time_indicator: bool = True):
        """
        Generate one episode with the given policy.

        Parameters
        ----------
        model : _type_
            _description_
        weather_generator : _type_, optional
            _description_, by default None
        weather_forecast_generator : _type_, optional
            _description_, by default None
        thermal_needs_generator : _type_, optional
            _description_, by default None
        state_contains_daily_time_indicator : bool, optional
            _description_, by default False
        state_contains_weekly_time_indicator : bool, optional
            _description_, by default False
        state_contains_yearly_time_indicator : bool, optional
            _description_, by default True

        Returns
        -------
        Pandas DataFrame
            _description_
        """

        if weather_generator is None:
            weather_generator = DEFAULT_WEATHER_GENERATOR

        if weather_forecast_generator is None:
            weather_forecast_generator = DEFAULT_FORECAST_GENERATOR

        if thermal_needs_generator is None:
            thermal_needs_generator = DEFAULT_THERMAL_NEEDS_GENERATOR

        env = cls(weather_generator=weather_generator,
                  weather_forecast_generator=weather_forecast_generator,
                  thermal_needs_generator=thermal_needs_generator,
                  record_logs=True,
                  state_contains_daily_time_indicator=state_contains_daily_time_indicator,
                  state_contains_weekly_time_indicator=state_contains_weekly_time_indicator,
                  state_contains_yearly_time_indicator=state_contains_yearly_time_indicator)

        reward_sum = 0
        #env.record_logs = True
        #env_orig.record_logs = True

        obs = env.reset()
        done = False

        while not done:
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)
            reward_sum += reward
            #env.render()           # Cannot render on Google Colab

        reward_sum

        env.close()

        df = env.logs_to_df()

        return df
