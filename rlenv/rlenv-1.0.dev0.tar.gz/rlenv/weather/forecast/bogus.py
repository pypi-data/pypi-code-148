import random

DEFAULT_WEATHER_FORECAST_SIGMA = 0.7
#DEFAULT_WEATHER_FORECAST_SIGMA = 0.

class ToyNoise:
    def __init__(self, sigma=DEFAULT_WEATHER_FORECAST_SIGMA):
        self.sigma = DEFAULT_WEATHER_FORECAST_SIGMA

    def __call__(self, weather_series, start_index, end_index):
        forecast_series = [y + random.normalvariate(0, self.sigma) for y in weather_series[start_index:end_index]]
        return forecast_series

    def params(self):
        params_dict = {
            "sigma": self.sigma
        }
        return params_dict

    def __str__(self):
        return "toynoise," + ",".join(["{}:{}".format(k, v) for k, v in self.params().items()])


gen_weather_forecast = ToyNoise()