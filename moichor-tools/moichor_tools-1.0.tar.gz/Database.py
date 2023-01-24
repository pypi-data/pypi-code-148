import io, re, cv2, os, sys, json
import boto3
import psycopg2
import pandas as pd
import numpy as np
from collections import defaultdict

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
np.set_printoptions(threshold=sys.maxsize)


class Database: 

	""" This package provides a database connection and access tool."""

	s3 = boto3.resource('s3', region_name='us-east-2')
	#""" Your S3 connection."""
	
	def __init__(self, test_ids=None): 

		""" Initialize the Database class with a list of user-defined test_ids.
		* You can also omit these test IDs and fetch them automatically."""

		client = boto3.client(service_name='secretsmanager')
		db_creds = json.loads(client.get_secret_value(SecretId='wfs_prod/readonly')['SecretString'])

		self.conn = psycopg2.connect(user=db_creds['username'],
									 password=db_creds['password'],
									 host=db_creds['host'],
									 port=db_creds['port'],
									 database=db_creds['dbname'])

		self.cur = self.conn.cursor()
		""" Your SQL cursor."""

		self.date_start = '2021-05-01'
		""" * Optional: Begin date for auto record search.
			DEFAULT: '2021-05-01' """

		self.date_end =  '2021-09-15'
		""" * Optional: End date for auto record search.
			DEFAULT: '2021-09-15' """

		self.reference_species = (2, 5)
		""" * Optional: Species for which to obtain auto search records.
		DEFAULT: (2, 5) """

		self.exclude_species_ids = (216, 3009, 3017, 18000)
		""" * Optional: Species to exclude from auto record search. 
		DEFAULT: (216, 3009, 3017, 18000) """

		self.exclude_clinic_ids = (1, 9, 40, 52, 77, 81) 	# Default
		""" * Optional: Clinic IDs to exclude from auto record search. 
		DEFAULT: (1, 9, 40, 52, 77, 81) """

		self.refvars = None
		""" All of the reference variables in the database. """
		self._fetch_refvars()

		self.test_id_query = None
		self.test_ids = test_ids
		""" Your test IDs, whether a user-defined list or result of a record search. """

		if self.test_ids == None: 
			self.flag = 'Auto'
			self._fetch_test_id_base()

		else: 

			self.flag = 'Manual'
		
		self.placeholders = ', '.join(['%s']*len(self.test_ids))
		self._pathology_records = None
		self._field_test_records = None
		self.records = pd.DataFrame()
		""" A dataframe of all records related to your set of test IDs.
		* Will be empty unless get_records() is run"""

		self.image_files = []
		""" Your image files (User input). """

		self.scan_ids = None

		self._local_paths = []
		self._img_objects = []
		self._download_count = 0
		self._download_df = pd.DataFrame()
		self.downloads = []
		""" A dataframe of downloaded images (arrays) populated when calling download_files(your_image_filepath_list)."""

		self.get_records = self._get_recs
		""" Run to populate records related to your set of test IDs. 
		* No input required."""

	def _fetch_refvars(self):								# Add any needed methods here
		self.cur.execute('select id, name from refvar order by id asc;')
		self.refvars = dict(self.cur.fetchall())

	def _fetch_refreshed_attrs(self):
		self._fetch_test_id_base()							# Not necessary to refresh test id list when no params have been changed, fix

	def _fetch_test_id_base(self):
		try: 

			self.test_id_query = f"""select t.id from test t

								 inner join patient p
									 on t.patient_id = p.id

								 inner join refspecies s
									 on p.species_id = s.id

								 where
									 s.custom_id ~ '^[0-9]+$'
								 and
									 t.clinic_id not in {self.exclude_clinic_ids}
								 and
									 t.id like any (array['%-cbc', '%-mcbc', '%-mcbcr']) 
								 and 
									 t.date_received >= '{self.date_start}'::date
								 and
									 t.date_received <= '{self.date_end}'::date
								 and
									 s.reference_species::bigint in {self.reference_species}
								 and
									 s.custom_id::bigint not in {self.exclude_species_ids}
								 and
									 t.is_excluded_from_study is false"""  # These attributes cannot be none or getting records takes too long (fix, not scalable)

			self.cur.execute(self.test_id_query)
			self.test_ids = self.cur.fetchall()

		except SyntaxError as e:

			print('Please assign a valid value for exclude_clinic_ids, date start, date end, reference_species, and/or exclude_species_ids.')

	def _get_sample_ids(self, records):

		def _filter_https(record):
			return list(filter(lambda record: 'https' in str(record), record))[0]

		def _parse_sample_id(subsplit):
			return re.sub('[^0-9]_', '', subsplit)

		def _remove_image_tag(subsplit):
			return subsplit.strip('.jpg')

		def _identify_sample_id(subsplit):
			if len(subsplit) > 3:

				return _parse_sample_id(_remove_image_tag(subsplit[1]) if not subsplit[3].isnumeric() else _remove_image_tag('_'.join([subsplit[1], subsplit[2]])))

			else: 

				if len(subsplit) == 3: 

					return _remove_image_tag('_'.join([subsplit[1], subsplit[2]]))

				else: return _remove_image_tag(subsplit[1])

		def _identify_sample_id_auto(subsplit):
			return _parse_sample_id(subsplit[0] if subsplit[0][-1].isdigit() else ''.join([subsplit[0], _remove_image_tag(subsplit[1])]))

		def _return_dict_list(subsplit):
			if self.flag == 'Auto': return _identify_sample_id_auto(subsplit[-1].split('_'))
			else: return _identify_sample_id(subsplit[-1].split('_'))

		try: 

			return list(map(lambda record: record + (_return_dict_list(_filter_https(record).split('/')),), records))

		except NotImplementedError as error:

			print('Name structure error in image file.')						# Print which file eventually

	@classmethod
	def download_files(cls, files):											# Can use self.image_files
		""" Run to populate downloads related to input files. """
		#try: 

		path_splits = list(map(lambda splits: str(splits).split('/'), files))
		bucket_paths = list(map(lambda splits: {splits[2]: '/'.join(splits[3:])}, path_splits))
		cls._download_df = pd.DataFrame(bucket_paths)

		bucket_path_key = cls._download_df.columns
		if '.' in bucket_path_key[0]: bucket_path = bucket_path_key[0].split('.')[0]
		else: bucket_path = bucket_path_key

		bucket = cls.s3.Bucket(bucket_path)
		cls._local_paths = cls._download_df[bucket_path_key].values
		cls._img_objects = list(map(lambda img: bucket.Object(img[0]), cls._local_paths))
		cls._download_count = 0

		print('Downloading...')

		def _download_comprehension(object): 
			with io.BytesIO() as file_stream:
				object.download_fileobj(file_stream)
				cls._download_count += 1

				if cls._download_count % 10 == 0 or cls._download_count == len(cls._img_objects): 

					print('%d/%d files downloaded to buffer.' % (cls._download_count, len(cls._img_objects)))

				file_stream.seek(0)

				if object.key.endswith('jpg'):
					test = file_stream.read()
					file_bytes = np.fromstring(test, np.uint8)
					return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

				elif object.key.endswith('json'):
					return json.load(file_stream)

		cls.downloads = list(map(lambda img: _download_comprehension(img), cls._img_objects))
		print()
		print('Download complete.')
		print('Download size: %d B' % sys.getsizeof(cls.downloads))
		print()

		#except: print('No image paths to download.')
		#return

	def _get_records_helper(self, columns):
		records = self.cur.fetchall()
		records = self._get_sample_ids(records)
		records = pd.DataFrame(records, columns=columns)
		return records.reset_index(drop=True)

	def _add_coordinates(self):
		splits = self._pathology_records['Image Paths'].apply(lambda path: path.split('_'))
		splits = list(map(lambda split: [split[2], split[3].strip('.jpg')] if len(splits) == 4 else [split[1], split[2].strip('.jpg')], splits))
		x_y_diff = pd.DataFrame(splits, columns=['x', 'y']).astype(float)
		x_y_base = self._pathology_records[['x', 'y']]
		added = x_y_base.add(x_y_diff, fill_value=0)
		self._pathology_records['x'] = added['x']
		self._pathology_records['y'] = added['y']

	def _get_recs(self):
		if self.flag == 'Auto': self._fetch_refreshed_attrs()

		self.cur.execute(f"""select i.test_id, i.refvar_id, i.imagelink, i.region from pathology_images i
							 where i.status = 0
							 and i.test_id in ({self.placeholders})
							 order by i.id""", tuple(self.test_ids))

		self._pathology_records = self._get_records_helper(['Test ID', 'Ref ID', 'Image Paths', 'Image Attributes', 'Sample ID'])
		self._pathology_records = pd.concat([self._pathology_records, self._pathology_records['Image Attributes'].apply(pd.Series)], axis=1).drop('Image Attributes', axis=1)
		self._add_coordinates()

		print('Pathology records found for the given parameters: ', len(self._pathology_records))

		self.cur.execute(f"""select c.test_id, c.body from custom_field_tests c
							 where c.test_id in ({self.placeholders})
							 order by c.id""", tuple(self.test_ids))

		self._field_test_records = self._get_records_helper(['Test ID', 'Scan Paths', 'Sample ID'])
	
		print('Field test records found for the given parameters: ', len(self._field_test_records))
		print()

		cols = ['Test ID', 'Ref ID', 'Image Paths', 'Sample ID', 'x', 'y', 'width', 'height']
		self.records = self._pathology_records[cols]
		self.records['Scan Paths'] = None
		self.records = self.records.set_index('Test ID')

		self.records = pd.merge(self.records, self._field_test_records, how='left', left_on=['Test ID', 'Sample ID'], right_on=['Test ID','Sample ID'])
		self.records = self.records.drop('Scan Paths_x', axis=1).rename(columns={'Scan Paths_y': 'Scan Paths'})