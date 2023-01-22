#!/usr/bin/env python
# coding: utf-8

"""
================================
Wall Environment - Thermal Needs
================================

This example shows how to get thermal needs in the Wall Environment.
"""

###############################################################################
# Import required packages

from rlenv.envs.wall.core import AccentaEnv
from rlenv.sed.wall import Wall
#from rlenv.weather.generator.toysine import gen_bogus_weather_time_series as weather_generator
from rlenv.weather.generator.brownianbridge import gen_weather_time_series_with_brownian_bridge as weather_generator
from rlenv.weather.forecast.bogus import gen_weather_forecast

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_context("talk")

SETPOINT_DEGREE = 18.0

outside_temperature_df = weather_generator()

thermal_needs_generator = Wall(setpoint_degree=SETPOINT_DEGREE)
heat_needs_df = thermal_needs_generator(outside_temperature_df=outside_temperature_df)

df = pd.merge(outside_temperature_df, heat_needs_df, on="indicative_date")

df.plot(x="indicative_date", y=["temperature", "heat_needs"], figsize=(16, 7), label=["outside temperature", "heat_needs"])
plt.axhline(SETPOINT_DEGREE, color="black", linestyle="dotted", label="setpoint")
plt.legend()
plt.tight_layout()

plt.show()
