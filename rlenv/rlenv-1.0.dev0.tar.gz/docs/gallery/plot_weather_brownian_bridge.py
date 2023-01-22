#!/usr/bin/env python3
# coding: utf-8

"""
=======================
Brownian Bridge Weather
=======================

This example shows how to generate weather time series using the Brownian Bridge data generator.
"""

###############################################################################
# Import required packages

from rlenv.weather.generator.brownianbridge import gen_weather_time_series_with_brownian_bridge

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_context("talk")

print(gen_weather_time_series_with_brownian_bridge)

df = gen_weather_time_series_with_brownian_bridge()

#ax = df.plot(x="hours", y="temperature", figsize=(16, 7))
ax = df.plot(x="indicative_date", y="temperature", figsize=(16, 7))

SETPOINT_DEGREE = 19.0
plt.axhline(SETPOINT_DEGREE, color="red")
plt.tight_layout()

plt.show()

print(df)