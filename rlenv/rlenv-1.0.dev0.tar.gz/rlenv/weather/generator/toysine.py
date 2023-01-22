import numpy as np
import pandas as pd

DEFAULT_NUM_DAYS = 60
DEFAULT_NUM_HOURS_PER_TIMESTEP = 4

class ToySine:
    def __init__(self, num_days=DEFAULT_NUM_DAYS, num_hours_per_timestep=DEFAULT_NUM_HOURS_PER_TIMESTEP):
        self.num_days = num_days
        self.num_hours_per_timestep = num_hours_per_timestep

    def __call__(self):
        time_array = np.arange(0, 24 * self.num_days, self.num_hours_per_timestep)
        temperature_array = np.sin(2. * np.pi / 24. * time_array) * 10. + 15.

        df = pd.DataFrame(np.array([time_array, temperature_array]).T,
                          columns=("hours", "temperature"))

        df['indicative_date'] = pd.date_range(start='2020-01-01', periods=len(df), freq=str(self.num_hours_per_timestep) + 'H')

        return df

    def params(self):
        params_dict = {
            "num_days": self.num_days,
            "num_hours_per_timestep": self.num_hours_per_timestep
        }
        return params_dict

    def __str__(self):
        return "toysine," + ",".join(["{}:{}".format(k, v) for k, v in self.params().items()])
        #return "toysine,num_days:{},num_hours_per_timestep:{}".format(self.num_days, self.num_hours_per_timestep)

gen_bogus_weather_time_series = ToySine()