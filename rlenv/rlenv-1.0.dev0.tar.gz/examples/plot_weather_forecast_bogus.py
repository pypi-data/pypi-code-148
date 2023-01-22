#!/usr/bin/env python3
# coding: utf-8

"""
================
Weather Forecast
================

This example shows how to generate (bogus) weather forecast time series.
"""

###############################################################################
# Import required packages

from rlenv.weather.generator.brownianbridge import gen_weather_time_series_with_brownian_bridge
from rlenv.weather.forecast.bogus import gen_weather_forecast

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_context("talk")

print(gen_weather_forecast)

outside_temperature_df = gen_weather_time_series_with_brownian_bridge()

start_index=2000
end_index=2048

weather_forecast = gen_weather_forecast(weather_series=outside_temperature_df.temperature,
                                        start_index=start_index,
                                        end_index=end_index)

outside_temperature_df.iloc[start_index:end_index].plot(x="hours", y="temperature")
plt.plot(outside_temperature_df.loc[start_index:end_index-1, ["hours"]].values, weather_forecast)

plt.show()