#!/usr/bin/env python
# coding: utf-8

"""
================
Wall Environment
================

This example shows how to use the Wall Environment.
"""

###############################################################################
# Import required packages

import matplotlib.pyplot as plt

from rlenv.envs.wall.core import AccentaEnv
from rlenv.sed.wall import Wall
#from rlenv.weather.generator.toysine import gen_bogus_weather_time_series as weather_generator
from rlenv.weather.generator.brownianbridge import gen_weather_time_series_with_brownian_bridge as weather_generator
from rlenv.weather.forecast.bogus import gen_weather_forecast as weather_forecast_generator

thermal_needs_generator = Wall(setpoint_degree=18.)

env = AccentaEnv(weather_generator=weather_generator,
                 weather_forecast_generator=weather_forecast_generator,
                 thermal_needs_generator=thermal_needs_generator,
                 record_logs=True,
                 state_contains_daily_time_indicator=False,
                 state_contains_weekly_time_indicator=False,
                 state_contains_yearly_time_indicator=True)
env.reset()

stop = False
s = env.reset()

while not stop:
    a = env.action_space.sample()

    s.shape == env.observation_space.shape
    a.shape == env.action_space.shape

    s, reward, stop, _ = env.step(a)

# MAKE THE RESULT DATAFRAME
df = env.logs_to_df()

# PLOT

df.loc[:,['a1_th', 'a2_th', 'a3', 'e', 'current_thermal_needs_kwh', 'cop']].plot(figsize=(30,8), alpha=0.5)
#df.loc[:,['s3', 's4']].plot(figsize=(30,8), alpha=0.5)
#df.loc[:,['s3', 's4', 's5', 's6']].plot(figsize=(30,8), alpha=0.5)
#df.loc[:,['s3', 's4', 's5', 's6', 's7', 's8']].plot(figsize=(30,8), alpha=0.5)
#df.loc[:24,['s3', 's4', 's5', 's6', 's7', 's8']].plot(figsize=(30,8), alpha=0.5)
plt.tight_layout()
plt.show()

print(env.observation_space.low)
print(env.observation_space.high)