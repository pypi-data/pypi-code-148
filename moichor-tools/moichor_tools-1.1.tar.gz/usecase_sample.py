from Database import Database
from Preprocessing import Preprocessing
import pandas as pd

### EXAMPLE WITH USER-PROVIDED TEST_IDS ###
#test_ids = ['ref0603452zbj-cbc']

db = Database()				# Here is your authenticated database access tool
db.get_records()
recs = db.records

preprocessor = Preprocessing(recs)
preprocessor.get_cell_counts()
print(preprocessor.cell_analysis_df)

#db.get_image_paths_by_sample(test_ids)