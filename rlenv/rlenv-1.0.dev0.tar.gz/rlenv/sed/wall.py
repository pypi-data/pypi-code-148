import numpy as np
import pandas as pd

### Besoins thermiques du bâtiment ###################################################################

def thermal_power_needs(outside_temperature, setpoint_degree, wall_surface, wall_thickness, wall_conductivity):
    '''
    Puissance thermique d'un problème intéermédiaire (consommation due au chauffage).
    '''
    thermal_power = 0

    if setpoint_degree > outside_temperature:
        thermal_power = wall_conductivity * wall_surface * (setpoint_degree - outside_temperature) / wall_thickness

    return thermal_power

class Wall:
    """
    Modèle de diffusion thermique (fonction de transfert pour un pas de temps)
    """

    def __init__(self,
                 wall_surface=15.,
                 wall_thickness=0.3,
                 wall_thickness_std=0.,
                 wall_conductivity=0.01,
                 wall_conductivity_std=0.,
                 setpoint_degree=19.0):     # Température de consigne à l'intérieur du bâtiment
        self.wall_surface = wall_surface
        self.wall_thickness = wall_thickness
        self.wall_thickness_std = wall_thickness_std
        self.wall_conductivity = wall_conductivity
        self.wall_conductivity_std = wall_conductivity_std
        self.setpoint_degree = setpoint_degree


    def __call__(self, outside_temperature_df):
        wall_thickness = np.random.normal(self.wall_thickness, self.wall_thickness_std) if self.wall_thickness_std > 0 else self.wall_thickness
        wall_conductivity = np.random.normal(self.wall_conductivity, self.wall_conductivity_std) if self.wall_conductivity_std > 0 else self.wall_conductivity

        hours_series = outside_temperature_df["hours"]
        dates_series = outside_temperature_df["indicative_date"]

        delta_time = hours_series[1] - hours_series[0]
        heating_energie_needs_list = []

        for outside_temperature in outside_temperature_df["temperature"]:
            power_needs = thermal_power_needs(outside_temperature, self.setpoint_degree, self.wall_surface, wall_thickness, wall_conductivity)
            energy_needs = power_needs * delta_time
            heating_energie_needs_list.append(energy_needs)

        heating_energie_needs_df = pd.DataFrame(np.array([hours_series, dates_series, heating_energie_needs_list]).T,
                                                columns=("hours", "indicative_date", "heat_needs"))

        heating_energie_needs_df.indicative_date = pd.to_datetime(heating_energie_needs_df.indicative_date)

        return heating_energie_needs_df