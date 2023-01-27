from setuptools import setup, find_packages



VERSION = '1.4'
DESCRIPTION = 'quick-django save your time and increase your development speed in django project'


# Setting up
setup(
    name="quick-django",
    version=VERSION,
    author="Momin Iqbal (Pakistan Dedov)",
    author_email="<mefiz.com1214@gmail.com>",
    description=DESCRIPTION,
    long_description="""
# quick-django

Create django project quickly single command with all necessary file like djnago app, urls.py, templates folder, static folder and add the default code in view.py,models.py,admin.py and create index.html

# How to use quick-django
### Step: 1
```python
pip install quick-django
```
### Step: 2
### Window
open cmd in your porject folder and run this command
        
```python
python -m quick-django myproject myproject_app 
```

### Linux
open terminal in your porject folder and run this command
        
```python
python3 -m quick-django myproject myproject_app 
```

### Configuration
```python
# setting.py
 INSTALLED_APPS = [
            ....
       'myproject_app',
       
        ]

```

# For Rest-Api

### Window
open cmd in your porject folder and run this command
        
```python
python -m quick-django myproject myproject_app --restapi
```

### Linux
open terminal in your porject folder and run this command
        
```python
python3 -m quick-django myproject myproject_app --restapi
```

### Configuration
```python
# setting.py
 INSTALLED_APPS = [
            ....
       'myproject_app',
       'rest_framework'
       
        ]

```


Check Our Site : https://mefiz.com </br>
pypi site : https://pypi.org/project/quick-django/



    """,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["django","djangorestframework"],
    keywords=['python', 'django', 'quick start django', 'quick django'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
