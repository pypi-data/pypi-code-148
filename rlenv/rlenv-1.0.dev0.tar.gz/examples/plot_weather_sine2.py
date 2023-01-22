#!/usr/bin/env python3
# coding: utf-8

"""
=============
Sine2 Weather
=============

This example shows how to generate weather time series using the Sine2 data generator.
"""

###############################################################################
# Import required packages

from rlenv.weather.generator.toysine2 import gen_bogus_weather_time_series

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_context("talk")

print(gen_bogus_weather_time_series)

df = gen_bogus_weather_time_series()

#ax = df.plot(x="hours", y="temperature", figsize=(16, 7))
ax = df.plot(x="indicative_date", y="temperature", figsize=(16, 7))

SETPOINT_DEGREE = 19.0
plt.axhline(SETPOINT_DEGREE, color="red")
plt.tight_layout()

plt.show()

print(df)