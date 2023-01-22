#!/usr/bin/env python
# coding: utf-8

"""
======================
Wall Environment - COP
======================

This example shows how to get COP in the Wall Environment.
"""

###############################################################################
# Import required packages

from rlenv.envs.wall.core import AccentaEnv, efficiency_func
from rlenv.sed.wall import Wall
from rlenv.weather.generator.brownianbridge import gen_weather_time_series_with_brownian_bridge as weather_generator
from rlenv.weather.forecast.bogus import gen_weather_forecast as weather_forecast_generator

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context("talk")

thermal_needs_generator = Wall()
env = AccentaEnv(weather_generator=weather_generator,
                 weather_forecast_generator=weather_forecast_generator,
                 thermal_needs_generator=thermal_needs_generator)
env.reset()

X = np.arange(-30., 40.)
plt.plot(X, [efficiency_func(t_out) for t_out in X])

plt.title("COP for a setpoint of {:0.2f}°C".format(env.thermal_needs_generator.setpoint_degree))
plt.xlabel("Outside temperature")
plt.ylabel("COP")

plt.tight_layout()

plt.show()