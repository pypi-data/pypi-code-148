import nbformat
import os
import requests

from typing import Dict
from .. import lib


def save(files: Dict[str, str]):
    config = lib.config()
    host = config['host']
    repo = config['repo']
    sha = config['sha']
    # Get the step path and prepend it to the file
    path_parts = os.getcwd().split('/')
    # user = 'jovyan'
    step_path = '/'.join(path_parts[path_parts.index('notebooks')+1:]) # ignore up to path prefix
    output_files = {}
    # Capture SQL files
    for filename, content in files.items():
        output_files[f'dags/{step_path}/{filename}'] = content
    # Capture py files
    notebook_path = './editor.ipynb'
    lib.save_notebook(notebook_path)
    nb = nbformat.read(notebook_path, as_version=4)
    for cell in nb.cells:
        if 'f_' in cell.id:
            filename = cell.id.replace('f_', '')
            output_files[f'dags/{step_path}/{filename}.py'] = cell.source
    req = {'files': output_files,
            'msg': 'Commit from notebook editor'}
    print(f'Committing changes to {len(output_files.keys())} files...')
    resp = requests.put(f'{host}/src/update/{repo}/{sha}', json=req)
    if resp.status_code == 200 or resp.status_code == 204:
        print('Commit completed successfully')
    else:
        print(f'Error committing file {resp.status_code} - {resp.text}')
