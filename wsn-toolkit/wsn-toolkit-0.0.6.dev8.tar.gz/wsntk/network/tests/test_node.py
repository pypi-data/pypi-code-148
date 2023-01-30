# coding: utf-8
#
# Copyright (C) 2020 wsn-toolkit
#
# This program was written by Edielson P. Frigieri <edielsonpf@gmail.com>

import pytest

from wsntk import network
from wsntk.network import SensorNode, RADIO_CONFIG

def test_sensor_node():
    # Test SensorNode creation with default values.
    
    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "DEFAULT")
    
    parameter = RADIO_CONFIG["DEFAULT"] 
    assert sensor.get_txpower() == parameter["max_tx_power"]
    assert sensor.get_frequency() == parameter["frequency"]

def test_sensor_node_no_consumption():
	# Test SensorNode creation with default values.

	sensor = SensorNode(dimensions = (10.0, 10.0), radio = "DEFAULT", consumption = 'None')
	position, energy, activity = next(iter(sensor))
	assert energy == 100
	
def test_sensor_node_contant_consumption():
	# Test SensorNode creation with default values.

	sensor = SensorNode(dimensions = (10.0, 10.0), radio = "DEFAULT", consumption = 'Exponential', scaling = 1.0)
	position, energy, activity = next(iter(sensor))
	assert energy < 100
	
    
def test_set_position():
    # Test setting the a new position.
    
    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "DEFAULT")
    
    position = (0.5,0.5)
    sensor.set_position(position)

    assert sensor.get_position() == position

def test_set_position_wrong_len_raise_value_error():
    # Test setting the a new position with wrong len.
    
    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "DEFAULT")
    
    error_msg = ('Position lenght different then expected. Expected 2, received 3.')
    
    with pytest.raises(ValueError, match=error_msg):
        sensor.set_position(position = (0.5,0.5,0.5))

def test_set_position_outside_limits_raise_value_error():
    # Test setting the a new position outside limits.
    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "DEFAULT")
    
    error_msg = ('Position exceeded dimensions limits.')
    
    with pytest.raises(ValueError, match=error_msg):
        sensor.set_position(position = (11.0, 11.0))

def test_sensor_node_with_unkown_radio_raises_value_error():
    # Test SensorNode creation with a unknown radio type.
    
    error_msg = ('Radio UNKNOWN is not supported.')
        
    with pytest.raises(ValueError, match=error_msg):
        sensor = SensorNode(dimensions = (10.0, 10.0), radio = "UNKNOWN")

def test_set_tx_power_within_range():
    # Test setting the tx_power within expected range.
    
    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "ESP32-WROOM-32U")
    
    parameters = RADIO_CONFIG["ESP32-WROOM-32U"]
    new_tx_power = (parameters["min_tx_power"] + parameters["max_tx_power"])/2
    sensor.set_txpower(new_tx_power)
    assert sensor.get_txpower() == new_tx_power


def test_set_tx_power_below_range_raises_value_error():
    # Test exception when setting the tx_power below expected range.
        
    error_msg = ('Parameter out of radio power specification. Expected value from -12.0 dBm to 9.0 dBm.')
        
    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "ESP32-WROOM-32U")
    
    parameters = RADIO_CONFIG["ESP32-WROOM-32U"]
    with pytest.raises(ValueError, match=error_msg):
        sensor.set_txpower(parameters["min_tx_power"] - 13.0)


def test_set_tx_power_above_range_raises_value_error():
    # Test exception when setting the tx_power above expected range.
    
    error_msg = ('Parameter out of radio power specification. Expected value from -12.0 dBm to 9.0 dBm.')
        
    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "ESP32-WROOM-32U")
    
    parameters = RADIO_CONFIG["ESP32-WROOM-32U"]
    with pytest.raises(ValueError, match=error_msg):
        sensor.set_txpower(parameters["max_tx_power"] + 10.0)

def test_get_rx_sensitivity():
    # Test getting the rx sensitivity.
    
    parameters = RADIO_CONFIG["ESP32-WROOM-32U"]

    sensor = SensorNode(dimensions = (10.0, 10.0), radio = "ESP32-WROOM-32U")
    assert sensor.get_rxsensitivity() == parameters["rx_sensitivity"]
    