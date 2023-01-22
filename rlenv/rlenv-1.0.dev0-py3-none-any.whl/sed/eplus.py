import os
import numpy as np
import pandas as pd
import tempfile

import epw

class EPlus:

    def __init__(self, idf_file_path, tmp_dir_prefix="/dev/shm", epw_base_path=None):
        self.idf_file_path = idf_file_path
        self.tmp_dir_prefix = tmp_dir_prefix
        self.epw_base_path = epw_base_path

        if epw_base_path is None:
            self.epw_base_path = epw.data.weather_san_francisco_tmy_path()


    def __call__(self, outside_temperature_df):
        weather_obj = epw.weather.Weather()

        weather_obj.read(file_path=self.epw_base_path)

        weather_obj.dataframe['Dry Bulb Temperature'] = outside_temperature_df.temperature.values
        weather_obj.dataframe['Dew Point Temperature'] = outside_temperature_df.temperature.values

        weather_obj.dataframe['Relative Humidity'] = 50.
        weather_obj.dataframe['Atmospheric Station Pressure'] = 10000.

        weather_obj.dataframe['Extraterrestrial Horizontal Radiation'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Extraterrestrial Direct Normal Radiation'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Horizontal Infrared Radiation Intensity'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Global Horizontal Radiation'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Direct Normal Radiation'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Diffuse Horizontal Radiation'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Global Horizontal Illuminance'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Direct Normal Illuminance'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Diffuse Horizontal Illuminance'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.
        weather_obj.dataframe['Zenith Luminance'] = 0. # np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 8.

        weather_obj.dataframe['Wind Direction'] = 0.
        weather_obj.dataframe['Wind Speed'] = 20.

        weather_obj.dataframe['Total Sky Cover'] = 5.
        weather_obj.dataframe['Opaque Sky Cover (used if Horizontal IR Intensity missing)'] = 5.

        weather_obj.dataframe['Visibility'] = 15.
        weather_obj.dataframe['Ceiling Height'] = 10000.

        weather_obj.dataframe['Precipitable Water'] = 100.
        weather_obj.dataframe['Aerosol Optical Depth'] = 0.15

        weather_obj.dataframe['Liquid Precipitation Depth'] = 0.
        weather_obj.dataframe['Liquid Precipitation Quantity'] = 0.

        # WRITE THE MODIFIED WEATHER FILE ###########################################

        tmp_dir_prefix = epw.core.expand_path(self.tmp_dir_prefix)

        with tempfile.TemporaryDirectory(dir=tmp_dir_prefix, prefix=".", suffix="_test") as tmp_dir_path:
            dst_epw_path = os.path.join(tmp_dir_path, "weather.epw")
            weather_obj.write(dst_epw_path)
            #print("Write", dst_epw_path)

            df = epw.core.run_eplus(idf_file_path=self.idf_file_path,
                                    weather_file_path=dst_epw_path,
                                    tmp_dir_prefix=tmp_dir_prefix)

        hours_series = outside_temperature_df["hours"]
        dates_series = outside_temperature_df["indicative_date"]

        heating_energie_needs_df = pd.DataFrame(np.array([hours_series,
                                                          dates_series,
                                                          df['ZONE1 PURCHASED AIR:Zone Ideal Loads Zone Total Heating Rate [W](Hourly)']]).T,
                                                columns=("hours", "indicative_date", "heat_needs"))

        # Convert watts to kw
        heating_energie_needs_df["heat_needs"] /= 1000.

        return heating_energie_needs_df