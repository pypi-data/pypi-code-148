# Author: Edielson P. Frigieri <edielsonpf@gmail.com>
#
# License: MIT

import pytest
import numpy as np

from wsntk import network
from wsntk.network import RadioLink



def test_free_space_link_down():
	# Test FreeSpace link creation with default values.

		
	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 4, frequency = 2.4e9, loss = "FSPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 52.09
	assert status == 0
	
def test_free_space_link_up():
	# Test FreeSpace link creation with default values.

	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 1, frequency = 2.4e9, loss = "FSPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 40.05
	assert status == 1	
	
   
def test_log_distance_link_down():
	# Test FreeSpace link creation with default values.
	np.random.seed(0xffff)

	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 4, frequency = 2.4e9, loss = "LDPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 52.09
	assert status == 0

	
def test_log_distance_link_up():
	# Test FreeSpace link creation with default values.
	np.random.seed(0xffff)

	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 1, frequency = 2.4e9, loss = "LDPL", d0 = 1.0, sigma = 0.0, n0 = 2.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 40.05
	assert status == 1
	

   
def test_twoslope_link_down():
	# Test FreeSpace link creation with default values.
	np.random.seed(0xffff)

	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 4, frequency = 2.4e9, loss = "TSPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 52.09
	assert status == 0

	
def test_two_link_up():
	# Test FreeSpace link creation with default values.
	np.random.seed(0xffff)

	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 1, frequency = 2.4e9, loss = "TSPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1 = 3.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 40.05
	assert status == 1
	

def test_twoslope_link_up_first_zone():
	# Test FreeSpace link creation with default values.
	np.random.seed(0xffff)

	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 2, frequency = 2.4e9, loss = "TSPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.2, n1 = 3.3)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 46.67
	assert status == 1
	
	
def test_twoslope_link_down_second_zone():
	# Test FreeSpace link creation with default values.
	np.random.seed(0xffff)

	link = RadioLink(tx_power = 0, rx_sensitivity = -50, distance = 15, frequency = 2.4e9, loss = "TSPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.2, n1 = 3.3)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 67.86
	assert status == 0	

	
def test_radio_link_set_distance():
	# Test FreeSpace link creation with default values.

		
	link = RadioLink(tx_power = 27, rx_sensitivity = -80, distance = 10, frequency = 933e6, loss = "LDPL", d0 = 1.0, sigma = 0.0, n0 = 2.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 51.85
		
	link.set_distance(4)
	loss,status = next(link)
	
	assert round(loss,2) == 43.89
		
	
	
def test_radio_link_set_txpower():
	# Test FreeSpace link creation with default values.

		
	link = RadioLink(tx_power = 12, rx_sensitivity = -20, distance = 4, frequency = 933e6, loss = "LDPL", d0 = 1.0, sigma = 0.0, n0 = 2.0)
	link = iter(link)
	loss,status = next(link)
	assert round(loss,2) == 43.89
	assert status == 0
	
	link.set_txpower(27)
	loss,status = next(link)
	#the loss is the same but wit less power the link becomes down
	assert round(loss,2) == 43.89
	assert status == 1
	

def test_radio_link_set_frequency():
	# Test FreeSpace link creation with default values.

		
	link = RadioLink(tx_power = 27, rx_sensitivity = -20, distance = 4, frequency = 933e6, loss = "LDPL", d0 = 1.0, sigma = 0.0, n0 = 2.0)
	link = iter(link)
	loss,status = next(link)
	
	assert round(loss,2) == 43.89
	assert status == 1	
	
	link.set_frequency(2.4e9)
	loss,status = next(link)
	#the loss is bigger with a diffetent frequency and the link becomes down
	assert round(loss,2) == 52.09
	assert status == 0	