from setuptools import setup, find_packages
import os.path
import glob

setup(
  name='hub',
  version="0.1",
  packages=find_packages(exclude="unittests"),
  data_files=[
    ('config', [os.path.join('hub/config', 'configuration.ini')]),
    ('greenery', glob.glob('hub/catalog_factories/greenery/ecore_greenery/*.ecore')),
    ('data', glob.glob('hub/data/construction/*.xml')),
    ('data', glob.glob('hub/data/customized_imports/*.xml')),
    ('data', glob.glob('hub/data/energy_systems/*.xml')),
    ('data', glob.glob('hub/data/energy_systems/*.insel')),
    ('data', glob.glob('hub/data/energy_systems/*.xlsx')),
    ('data', glob.glob('hub/data/energy_systems/*.txt')),
    ('data', glob.glob('hub/data/energy_systems/*.yaml')),
    ('data', glob.glob('hub/data/greenery/*.xml')),
    ('data', glob.glob('hub/data/life_cycle_assessment/*.xml')),
    ('data', glob.glob('hub/data/schedules/*.xml')),
    ('data', glob.glob('hub/data/schedules/*.xlsx')),
    ('data', glob.glob('hub/data/schedules/idf_files/*.idf')),
    ('data', glob.glob('hub/data/sensors/*.json')),
    ('data', glob.glob('hub/data/usage/*.xml')),
    ('data', glob.glob('hub/data/usage/*.xlsx')),
    ('data', glob.glob('hub/data/weather/*.dat')),
    ('data', glob.glob('hub/data/weather/epw/*.epw')),
    ('data', glob.glob('hub/data/weather/*.dat'))
  ],
  setup_requires=['setuptools']
)
