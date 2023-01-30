# Author: Edielson P. Frigieri <edielsonpf@gmail.com>
#
# License: MIT

import pytest
import numpy as np

from wsntk import models
from wsntk.models import FreeSpace, LogDistance, TwoSlope

def test_free_space():
	# Test LogDistance link creation with default values.

	link = FreeSpace()

	loss = link.loss(distance = 2, frequency = 933e6)

	assert round(loss,2) == 37.87
	
	
def test_log_distance():
	# Test LogDistance link creation with different parameters.

	np.random.seed(0xffff)
	link = LogDistance(d0 = 1.0, sigma = 0.0, n0 = 2.0)

	loss = link.loss(distance = 2, frequency = 933e6)
	assert round(loss,2) ==  37.87
		
		
def test_log_distance_diffent_n0():
	# Test LogDistance link creation with different parameters.

	np.random.seed(0xffff)
	link = LogDistance(d0 = 1.0, sigma = 0.0, n0 = 2.2)

	loss = link.loss(distance = 10, frequency = 933e6)
	assert round(loss,2) ==  53.85		
	

def test_two_slope():
	# Test LogDistance link creation with different parameters.

	np.random.seed(0xffff)
	link = TwoSlope()

	loss = link.loss(distance = 2, frequency = 2.4e9)
	assert round(loss,2) ==  46.07
	
	loss = link.loss(distance = 15, frequency = 2.4e9)
	assert round(loss,2) ==  65.33
		
		
def test_two_slope_diffent_n0_and_n1():
	# Test LogDistance link creation with different parameters.

	np.random.seed(0xffff)
	link = TwoSlope(d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.2, n1 = 3.3)

	loss = link.loss(distance = 2, frequency = 2.4e9)
	assert round(loss,2) ==  46.67

	loss = link.loss(distance = 15, frequency = 2.4e9)
	assert round(loss,2) ==  67.86	
	

def test_two_slope_diffent_d0_and_d1():
	# Test LogDistance link creation with different parameters.

	np.random.seed(0xffff)
	link = TwoSlope(d0 = 2.0, d1 = 15.0, sigma = 0.0, n0 = 2.0, n1 = 3.0)

	loss = link.loss(distance = 2, frequency = 2.4e9)
	assert round(loss,2) ==  46.07
	
	#the change in the slope only happens after 15 meters
	loss = link.loss(distance = 15, frequency = 2.4e9)
	assert round(loss,2) ==  63.57				