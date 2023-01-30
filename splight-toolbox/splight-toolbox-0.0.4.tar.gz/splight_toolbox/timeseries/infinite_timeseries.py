from itertools import count
import numpy as np
import pandas as pd
from typing import Tuple
from pathlib import Path


class InfiniteTimeSeries:
    _from_days_map = {
        "min": 1440,
        "H": 24,
        "D": 1,
    }
    _datetime_projections = {
        "min": lambda x: x.minute,
        "H": lambda x: x.hour,
        "D": lambda x: x.day,
    }

    def __init__(self, seed_data: pd.DataFrame, frequency: str = "H", noise_factor: float = 0, name: str = None):
        self._name = name
        self._frequency = frequency
        self._data = seed_data.loc[:, ["timestamp", "value"]]
        self._data.set_index("timestamp", inplace=True)
        self._data.index = pd.to_datetime(self._data.index)
        self._data = self._data.resample(frequency).interpolate(method='spline', order=3)
        self._data = self._data.iloc[0:min(self._get_intervals_per_year(frequency), len(self._data))]
        self._data.index = self._index_to_interval_of_year(self._data.index, frequency)
        self._noise_factor = noise_factor

    def get_latest_measurement(self, index: pd.Timestamp) -> Tuple[pd.Timestamp, float]:
        rounded_index = index.floor(self._frequency)
        index_day_of_year = rounded_index.timetuple().tm_yday
        index_interval_of_year = index_day_of_year * self._from_days_map[self._frequency] + self._datetime_projections[self._frequency](rounded_index)
        row = self._data.loc[index_interval_of_year]
        return rounded_index, row.value

    def _get_intervals_per_year(self, frequency: str) -> int:
        return 365 * self._from_days_map[frequency]

    def _index_to_interval_of_year(self, index: pd.DatetimeIndex, frequency: str = "H") -> pd.DatetimeIndex:
        return pd.to_datetime(index).day_of_year * self._from_days_map[frequency] + self._datetime_projections[frequency](pd.to_datetime(self._data.index))

    @property
    def name(self) -> str:
        return self._name

    @property
    def seed_df(self) -> pd.DataFrame:
        return self._data

    def seed_to_csv(self, path: str):
        self._data.to_csv(path)

    @classmethod
    def from_csv_seed(cls, path: str, frequency: str = "H", noise_factor: float = 0):
        return cls(pd.read_csv(path), frequency, noise_factor, Path(path).stem)

    def _get_noise(self) -> float:
        values_mean = self._data.mean()
        values_std = self._data.std()
        noise_mean = self._noise_factor * values_mean
        return np.random.normal(noise_mean, values_std**2)

    def __getitem__(self, index):
        return self._data.iloc[index % len(self._data)] + self._get_noise()

    def __iter__(self):
        return (self._data.iloc[i % len(self._data)] + self._get_noise() for i in count())
