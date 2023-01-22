from setuptools import setup,find_namespace_packages
from os import listdir
setup(name='smper',

      version='2.2',

      url='https://github.com/parlorsky/sempaiper',

      license='MIT',

      author='Levap Vobayr',

      author_email='tffriend015@gmail.com',

      description='',
      packages=find_namespace_packages(where="src"),
      package_dir={"": "src"},
      package_data={**{
        f"smper.q1_1.{x}": ["*.jpg"] for x in listdir('src/smper/q1_1/')
        },**{
        f"smper.q2_1.{x}": ["*.jpg"] for x in listdir('src/smper/q2_1/')
        },**{
        f"smper.q3_1.{x}": ["*.jpg"] for x in listdir('src/smper/q3_1/')
        },**{
        f"smper.q4_1.{x}": ["*.jpg"] for x in listdir('src/smper/q4_1/')
        }
        },


      zip_safe=False)
