import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


# Bounding box and tiling
# Add user selection for multiprocessing

class Preprocessing:

	""" This package provides an image preprocessing tool."""
	
	def __init__(self, records):

		""" Initialize the Preprocessing class with your image records. """

		self.records = records
		"""Your image records. """

		self._cell_analysis_column = pd.DataFrame()
		self.cell_analysis_df = pd.DataFrame()
		""" The result of running any analysis on your records. """

		if len(self.records) == 0:

			print('Invalid input. Please make sure at least one https: image filepath is in your input data.')
			return

	def get_cell_counts(self):
		for test_index in set(self.records.index):

			cell_counts = self.records.loc[test_index].apply(pd.value_counts)['Ref ID'].dropna()
			self._cell_analysis_column = pd.DataFrame(cell_counts).rename(columns={'Ref ID': test_index})
			self.cell_analysis_df = pd.concat([self.cell_analysis_df, self._cell_analysis_column], axis=1)

		self.cell_analysis_df.index.name = 'Ref ID'

	def show_img(self, image_download):
		plt.imshow(image_download)
		plt.show()