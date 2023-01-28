import requests


class Weather:
    """
    import Weather
    APPKEY needs to be generated from openweather api
    weather = Weather(city=CITY, appkey=APPKEY)
    print(weather.data)
    returns the data as a json
    """

    def __init__(self, city, appkey, lat=None, lon=None):
        url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, appkey)
        r = requests.get(url)
        self.data = r.json()

    def next_12_hr(self):
        pass

    def next_12_hr_simpified(self):
        pass
