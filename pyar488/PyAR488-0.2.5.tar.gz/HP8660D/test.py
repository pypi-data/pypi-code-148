from PyAR488.PyAR488 import AR488
from HP8660D import HP8660D

import time

interface = AR488('COM5', debug = True)

gen = HP8660D(interface, 19)

# OK
gen.center_frequency(1.23456789 * 10**9)

# ok  -> update range check?
gen.output_level(-10)


gen.internal_1kHz()


interface.close()
print('done')


""" NOTES:
-> output is disabled until a level is set with gpib
-> gpib output level is not calibrated, alignment?
-> create a function to configure one show the source frequency and level
"""