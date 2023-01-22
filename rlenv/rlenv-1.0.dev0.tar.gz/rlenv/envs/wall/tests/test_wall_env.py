from rlenv.envs.wall.core import AccentaEnv, Wall
from rlenv.weather.generator.toysine import gen_bogus_weather_time_series as weather_generator
from rlenv.weather.forecast.bogus import gen_weather_forecast as weather_forecast_generator

def test_env():
    thermal_needs_generator = Wall(setpoint_degree=18.)

    env = AccentaEnv(weather_generator=weather_generator,
                     weather_forecast_generator=weather_forecast_generator,
                     thermal_needs_generator=thermal_needs_generator,
                     record_logs=True,
                     state_contains_daily_time_indicator=False,
                     state_contains_weekly_time_indicator=False,
                     state_contains_yearly_time_indicator=True)
    env.reset()

    def random_episode(verbose=False):
        stop = False
        s = env.reset()
        i = 0

        while not stop:
            a = env.action_space.sample()

            s.shape == env.observation_space.shape
            a.shape == env.action_space.shape

            if verbose:
                print(".", end="")

            try:
                s, reward, stop, _ = env.step(a)
            except Exception as e:
                print(i)
                raise

            i += 1

    for ep in range(100):
        random_episode()