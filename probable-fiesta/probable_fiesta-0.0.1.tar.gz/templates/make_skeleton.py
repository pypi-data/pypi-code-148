import os

ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/config")[0])
CURR_DIR = str(os.path.dirname(os.path.abspath(__file__)))

app_name = "probable_fiesta"

# create directories
folders = ['/src', f'/src/{app_name}', f'/src/{app_name}/app', f'/src/{app_name}/cli', f'/src/{app_name}/run', '/tests']

for folder in folders:
    if not os.path.exists(ROOT_DIR + folder):
        os.makedirs(ROOT_DIR + folder)

files = [f'/src/{app_name}/__init__.py', f'/src/{app_name}/__about__.py', f'/src/{app_name}/app/__init__.py', f'/src/{app_name}/app/main.py', f'/src/{app_name}/cli/__init__.py', f'/src/{app_name}/run/main.py']
for file in files:
    if not os.path.exists(ROOT_DIR + file):
        with open(ROOT_DIR + file, 'w') as f:
            f.write('')