import re
import pandas as pd
from collections import defaultdict


class Annotations:
	
	def __init__(self, records):

		self.records = records

		if len(self.records) == 0:

			print('Invalid input. Please make sure at least one https: image filepath is in your input data.')
			return

	def labels(self):
		pass