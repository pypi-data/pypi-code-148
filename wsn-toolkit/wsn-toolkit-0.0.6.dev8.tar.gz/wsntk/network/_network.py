# Authors: Edielson P. Frigieri <edielsonpf@gmail.com> (main author)
#
# License: MIT

"""Sensor networks simulation."""

from wsntk.network import SensorNode
from wsntk.network import RadioLink

from abc import ABCMeta, abstractmethod

from numpy.random import rand
import math
import numpy as np

class BaseNetwork(metaclass=ABCMeta):
	"""
		Sensor network class.
		This class is implments a sensor network which involves elemts such as sensors and links.
		
		Required arguments:
		
		*nr_sensors*:
			Integer, the number of sensors.
		
		*dimensions*:
			Tuple of Integers, the x and y dimensions of the simulation area in kilometers.

		*loss function*
			String, the path loss function
		  
		*sigma*
			Double, standard deviation applied to specific path loss models

		*n0*
			Double, the path loss exponent

		*radio*
			String, the radio type usd on all sensors
	"""



	def __init__(self, nr_sensors, dimensions, loss, d0, d1, sigma, n0, n1, radio, consumption, scaling):
		
		self.nr_sensors = nr_sensors
		self.dimensions = dimensions
		self.radio = radio
		self.sigma = sigma
		self.n0 = n0
		
		self.sensors, self.links = self._init_simulation(nr_sensors, dimensions, radio, consumption, scaling, loss, d0, d1, sigma, n0, n1)
					
	
	def _init_simulation(self, nr_sensors, dimensions, radio, consumption, scaling, loss, d0, d1, sigma, n0, n1):
		
		sensors = self._init_sensors(nr_sensors, dimensions, radio, consumption, scaling)
		links = self._init_links(sensors, loss, d0, d1, sigma, n0, n1)
					
		return sensors, links


	def _init_sensors(self, nr_sensors, dimensions, radio, consumption, scaling):
		"""Initializes the simulaiton creating all sensors with respective configuration. """                
		
		sensors = []
		#instantiate all sensors
		for i in range (nr_sensors):
			#instantiate a sensor
			sensor = SensorNode(dimensions, radio, consumption, scaling)
			#Add sensor to the network
			sensors.append(sensor)
		
		return sensors
	
	def _init_links(self, sensors, loss, d0, d1, sigma, n0, n1):
		"""Initializes the simulaiton creating all links with respective configuration. """                
		
		links = {}
		for rx_sensor in sensors:
			for tx_sensor in sensors:
				if rx_sensor != tx_sensor:
					distance = self._distance(rx_sensor.get_position(), tx_sensor.get_position())
					#instantiate a sensor
					link = RadioLink(tx_sensor.tx_power, rx_sensor.rx_sensitivity, distance, tx_sensor.frequency, loss, d0, d1, sigma, n0, n1)
					#Add links to the dictionary
					links[sensors.index(rx_sensor), sensors.index(tx_sensor)] = link
		
		return links
	
	def _get_link(self, rx_sensor, tx_sensor):
		"""Get the repectve link object for a pair of sensors"""
		return self.links[self.sensors.index(rx_sensor), self.sensors.index(tx_sensor)]
	
	def _distance(self, pos_a, pos_b):
		"""Calculate the euclidean distance between two positions"""
		return (math.sqrt(((pos_a[0]-pos_b[0])**2)+((pos_a[1]-pos_b[1])**2)))

	def __iter__(self):
		"""Generator which returns the current links and sensors after update."""
		while True:
			positions, residuals, activities = self._update_sensors()
			status, loss = self._update_links()
			yield positions,residuals,activities,status,loss
			
	@abstractmethod
	def _update_sensors(self):
		"""Update the sensors status: position, energy, etc."""
		raise NotImplementedError

	@abstractmethod
	def _update_links(self):
		"""update the links status based on the new sensors status."""
		raise notimplementederror
	   
    
class SensorNetwork(BaseNetwork):
	"""
		Sensor network class.
		This class is implments a sensor network which involves elemts such as sensors and links.
		
		Required arguments:
		
		  *nr_sensors*:
			Integer, the number of sensors.
		  
		  *dimensions*:
			Tuple of Integers, the x and y dimensions of the simulation area in kilometers.

		  *loss function*
			String, the path loss function

		  *sigma*
			Double, standard deviation applied to specific path loss models
		  
		  *n0*
			Double, the path loss exponent

		  *radio*
			String, the radio type usd on all sensors
	"""
	def __init__(self, nr_sensors, dimensions, loss = "FSPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0,  radio = "DEFAULT", consumption = "None", scaling = 1.0):
		
		super(SensorNetwork, self).__init__(nr_sensors, dimensions, loss, d0, d1, sigma, n0, n1, radio, consumption, scaling)
	
	def _update_sensors(self):
		positions = np.empty((0, len(self.dimensions)))
		energy_residuals = []
		activities = []
		
		for sensor in self.sensors:
			position, energy, activity = next(iter(sensor))
			positions = np.append(positions, position.reshape(1,len(self.dimensions)), axis = 0)
			energy_residuals.append(energy)
			activities.append(activity)
		return positions, energy_residuals, activities
 
	def _sensors_alive(self, tx_sensor, rx_sensor):
		#check if both sensors of a link are alive
		return (tx_sensor.get_activity() and rx_sensor.get_activity())
		
	def _update_links(self):
		list_status = []
		list_loss = []
		for rx_sensor in self.sensors:
			aux_status = []
			aux_loss = []
			for tx_sensor in self.sensors:
				if (rx_sensor != tx_sensor) and self._sensors_alive(tx_sensor, rx_sensor):
					
					#calculate the updated distance
					distance = self._distance(rx_sensor.get_position(), tx_sensor.get_position())
					
					#get link object
					link = self._get_link(rx_sensor, tx_sensor)
					
					#update link parameters
					link.set_distance(distance)
					link.set_txpower(tx_sensor.tx_power)
					link.set_rxsensitivity(rx_sensor.rx_sensitivity)	
					link.set_frequency(tx_sensor.frequency)
					
					#get the updated status and loss
					loss,status = next(iter(link))
				else:
					#there is no link towards itself  
					loss = 0
					status = 0    
					
				aux_status.append(status)
				aux_loss.append(loss)
			list_status.append(aux_status)
			list_loss.append(aux_loss)
			
		return list_status, list_loss
    
