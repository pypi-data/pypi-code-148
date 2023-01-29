import glob
import os
import requests

from typing import Dict, List
from .. import lib


def save(files: List[Dict[str, str]]):
    config = lib.config()
    host = config['host']
    repo = config['repo']
    sha = config['sha']
    # Get the step path and prepend it to the file
    output_files = {}
    saved = False
    # Capture ipynb files
    for f in files:
        for filename in glob.glob(f['src']):
            if not saved:
                lib.save_notebook(filename)
                saved = True
            with open(filename, 'r') as fh:
                output_files[os.path.join('analysis', 'notebooks', f['dest'], filename)] = fh.read()
    req = {'files': output_files,
            'msg': 'Commit from analysis notebook'}
    print(f'Committing changes to {len(output_files.keys())} files...')
    resp = requests.put(f'{host}/src/update/{repo}/{sha}', json=req)
    if resp.status_code == 200 or resp.status_code == 204:
        print('Commit completed successfully.')
    else:
        print(f'Error committing file {resp.status_code} - {resp.text}')
