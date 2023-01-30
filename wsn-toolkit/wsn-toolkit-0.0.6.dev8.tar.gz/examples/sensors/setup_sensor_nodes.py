# coding: utf-8
#
# Copyright (C) 2020 wsn-toolkit
#
# This program was written by Edielson P. Frigieri <edielsonpf@gmail.com>

from wsntk.network import SensorNode

position = (0.5, 0.5)

#create two sensors with different radio configurations
Sensor1 = SensorNode(position) # node with default radio configuration
Sensor2 = SensorNode(position, radio = "ESP32-WROOM-32U")

#show current radio configuration
print("Sensor1: tx power =  %s, rx_sensitivity = %s " %(Sensor1.get_txpower(), Sensor1.get_rxsensitivity()))
print("Sensor2: tx power =  %s, rx_sensitivity = %s " %(Sensor2.get_txpower(), Sensor2.get_rxsensitivity()))

#set new tranmission power for sensor 1
Sensor1.set_txpower(8.0)
print("Sensor1: new tx power =  %s, rx_sensitivity = %s " %(Sensor1.get_txpower(), Sensor1.get_rxsensitivity()))

#set new position for sensor 2
print("Sensor2: old position =  (%s, %s) " %(Sensor2.get_position()))
Sensor2.set_position((-5.0, 5.0))
print("Sensor2: new position =  (%s, %s) " %(Sensor2.get_position()))
