# coding: utf-8
#
# Copyright (C) 2020 wsn-toolkit
#
# This program was written by Edielson P. Frigieri <edielsonpf@gmail.com>

from wsntk.models import FreeSpace, LogDistance, TwoSlope

from abc import ABCMeta, abstractmethod
import numpy as np
import math

class BaseLink(metaclass=ABCMeta):
	"""Base class for radio links."""
    
	propagation_models = {
		"FSPL": (FreeSpace,),
		"LDPL": (LogDistance,),
		"TSPL": (TwoSlope,),
	}
	
	def __init__(self, tx_power, rx_sensitivity, distance, frequency, loss = "LDPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0):
        
		self.tx_power = tx_power
		self.rx_sensitivity = rx_sensitivity
		self.distance = distance
		self.frequency = frequency	
		self.model = self._init_link(loss, d0, d1, sigma, n0, n1)
		
	def _init_link(self, loss, d0, d1, sigma, n0, n1):
		"""Get ``Propagation Class`` object for str ``loss``. """
		try:
			model_ = self.propagation_models[loss]
			model_class, args = model_[0], model_[1:]
			if loss in ('LDPL'):
				args = (d0, sigma, n0)
			if loss in ('TSPL'):
				args = (d0, d1, sigma, n0, n1)	
			return model_class(*args)
		except KeyError as e:

			raise ValueError("The propagation loss %s is not supported. " % loss) from e
	
	def set_txpower(self, tx_power):
		"""
		Set transmission power of the link source
		
		Parameters
		----------
		tx_power : {double}
			Transmission power used by link source [dBm]
		
		Returns
		-------
		No data returned
		"""
		self.tx_power = tx_power
	
	def set_rxsensitivity(self, rx_sensitivity):	
		"""
		Set radio receiver sesitivity in the link destination
		
		Parameters
		----------
		rx_sensitivity : {double}
			Receiver sensitivity  used by the link receiver
		
		Returns
		-------
		No data returned
		"""
		self.rx_sensitivity = rx_sensitivity
	
	def set_distance(self, distance):	
		"""
		Set link distance
		
		Parameters
		----------
		distance : {double}
			Distance between the source and destination in the link
		
		Returns
		-------
		No data returned
		"""
		self.distance = distance
	
	def set_frequency(self, frequency):	
		"""
		Set link frequency
		
		Parameters
		----------
		frequency : {double}
			Frequeny of operation over the link
		
		Returns
		-------
		No data returned
		"""
		self.frequency = frequency	
		
	def __iter__(self):
		"""Interator"""
		return self
    
	def __next__(self):
		return self._update_link()

	@abstractmethod
	def _update_link(self):
		"""Update the links status based on the current parameters."""
		raise NotImplementedError 
		

class RadioLink(BaseLink):
	"""Class for radio links."""

	def __init__(self, tx_power, rx_sensitivity, distance, frequency, loss = "LDPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0):

		super(RadioLink, self).__init__(tx_power, rx_sensitivity, distance, frequency, loss, d0, d1, sigma, n0, n1)
	
	def _update_link(self):
		"""Update the links status based on the current parameters."""
		 
		#calculate the path loss
		loss = self.model.loss(self.distance, self.frequency)
		#calculated the received power
		rx_power = self.tx_power - loss
		#define the currentlink status	
		if(rx_power >= self.rx_sensitivity):
			link_status = 1
		else:
			link_status = 0

		return loss, link_status






