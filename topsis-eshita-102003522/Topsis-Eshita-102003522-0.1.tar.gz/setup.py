from distutils.core import setup
setup(
  name = 'Topsis-Eshita-102003522',         
  packages = ['Topsis-Eshita-102003522'],  
  version = '0.1',      
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Calculate Topsis score and save it in a csv file',
  author = 'Eshita Arora',                   
  author_email = 'earora_be20@thapar.edu',     
  url = 'https://github.com/eshitaarora/Topsis-Eshita',
  download_url = 'https://github.com/eshitaarora/Topsis-Eshita/archive/refs/tags/v0.1.tar.gz',
  keywords = ['TOPSISSCORE', 'RANK', 'DATAFRAME'],
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.9',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
