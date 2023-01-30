# coding: utf-8
#
# Copyright (C) 2020 wsn-toolkit
#
# This program was written by Edielson P. Frigieri <edielsonpf@gmail.com>

from wsntk.simulator import SimuNet
import numpy as np
import logging

#from scipy.spatial.distance import cdist

logging.basicConfig(format='%(asctime)-15s - %(message)s', level=logging.INFO)
logger = logging.getLogger("network simulation")

## set this to true if you want to plot node positions
DRAW = True

## number of sensors
nr_sensors = 10

## simulation area (m)
max_x, max_y = 1000, 1000

np.random.seed(0xffff)

## Free Space path loos-based simulation
#net = SimuNet(nr_sensors, dimensions=(max_x, max_y), loss = "LDPL", d0 = 1.0, d1 = 10.0, sigma = 0.0, n0 = 2.0, n1= 3.0, radio = "DEFAULT", consumption = "None", scaling = 1.0)

## Log-Distance path loos-based simulation
#net = SimuNet(nr_sensors, dimensions=(max_x, max_y), loss = "LDPL", d0 = 1.0, d1 = 10.0, sigma = 8.7, n0 = 2.2, n1 = 3.3, radio = "DEFAULT", consumption = "None", scaling = 1.0)

## Two-Slope path loos-based simulation with ESP32-WROOM-32U radio sensors
#net = SimuNet(nr_sensors, dimensions=(max_x, max_y), loss = "LDPL", d0 = 1.0, d1 = 10.0, sigma = 8.7, n0 = 2.2, n1 = 3.3, radio = "ESP32-WROOM-32U", consumption = "None", scaling = 1.0)

## Two-Slope path loos-based simulation with ESP32-WROOM-32U radio sensors and linear battery consumption
net = SimuNet(nr_sensors, dimensions=(max_x, max_y), loss = "LDPL", d0 = 1.0, d1 = 10.0, sigma = 8.7, n0 = 2.2, n1 = 3.3, radio = "ESP32-WROOM-32U", consumption = "Exponential", scaling = 20.0)


if DRAW:
	import matplotlib.pyplot as plt

	# Create new Figure and an Axes which fills it.
	ax = plt.subplot(111)
	ax.set_xlim(0, max_x)
	ax.set_ylim(0, max_y)

	# Construct the scatter which will be update during simulation 
	scat_sensors = ax.scatter([], [], s=60, lw=0.5, zorder=2)
	lines = [ax.plot([],[], 'C3', zorder=1, lw=0.3)[0] for j in range(nr_sensors*nr_sensors)]

	
step = 0
for sensors,residuals,activities,links,loss in net:

	step = step+1
	if step%10 == 0: 
		logger.info('Step %s'% step)
		print(sensors)
		print(residuals)
		print(activities)
		print(links)
		print(loss)
		

	if DRAW:
		#cleanup all lines
		for line in lines:
			line.set_data([],[])
		
		#update only the lines which represents a valid link
		lnr = 0
		i = 0
		for link_set in links:
			j = 0
			for link in link_set:
				if link == 1:
					lines[lnr].set_data([sensors[i,0],sensors[j,0]], [sensors[i,1],sensors[j,1]])
					lnr += 1
				j = j + 1
			i = i + 1

		#update the sensors position
		scat_sensors.set_offsets(sensors)
		
		# set the sensor collors according to residual energy
		facecolors = []
		for activity in activities:
			if(activity == 1):
				facecolors.append('b')
			else:
				facecolors.append('r')
		scat_sensors.set_facecolors(facecolors)
		
		plt.draw()
		plt.pause(0.5)
