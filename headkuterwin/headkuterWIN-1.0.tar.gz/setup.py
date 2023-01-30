from setuptools import setup, find_packages
import app




setup(
    name='headkuterWIN',
    version=1.0,
    packages = ['Module','Module.veracrypt','Module.formosa','Module.gui','Module.keepass'],
    py_modules=['app','autoVera'],
    #package_data={'Module.formosa.themes':['Module\\formosa\\themes\\finances.json','Module\\formosa\\themes\\copy_left.json','Module\\formosa\\themes\\harry_potter.json','Module\\formosa\\themes\\medieval_fantasy.json','Module\\formosa\\themes\\sci-fi.json','Module\\formosa\\themes\\the_big_bang_theory.json','Module\\formosa\\themes\\tourism.json']},
    package_data={'Module.formosa.themes':['finances.json','copy_left.json','harry_potter.json','medieval_fantasy.json','sci-fi.json','the_big_bang_theory.json','tourism.json']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'headkuter =app:headkurter'  #ponting to executeable function
        ]
    },
    install_requires=[
        'click==8.1.3',
        'colorama==0.4.4',
    ],
        #zip_safe = False
    )