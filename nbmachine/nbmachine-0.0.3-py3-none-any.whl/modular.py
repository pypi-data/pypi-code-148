# nbmachine - coordinated notebooks 
import importlib 
import json
import nbformat
import os
import shutil
from datetime import datetime
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from urllib.request import urlopen

GOOGLE_EXPORT = 'https://docs.google.com/uc?export=download&id='

def trace(line):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S  ')
    with open('request.txt', 'a') as f:
        f.write(ts + line + '\n')  

def get_request(): 
    req = None
    if os.path.exists('request.json'):
        with open('request.json') as f:
            request = f.read()
            req = json.loads(request)
    return req

def import_nb(link, name, attr = None):

    # assuming public colab for now, need to add secure colab and local

    file_id = link.split('/')[-1] # get ID 
    url = GOOGLE_EXPORT + file_id
    file = name + '.ipynb'

    with urlopen(url) as r:
        with open(file, 'wb') as out_file:
            shutil.copyfileobj(r, out_file) 
    with open(file) as f:
        newText=f.read().replace('"python3"','"python3", "language": "python"')
        newText=newText.replace('!pip','#!pip') # ipynb library can't do magic
        newText=newText.replace('%%capture','#%%capture') # ipynb library can't do magic
    with open(file, "w") as f:
        f.write(newText)  

    module = importlib.import_module('ipynb.fs.defs.' + name)
    if attr == None:
        return module
    else:
        return getattr(module, attr)

def run_nb(request=None):
    name = request['name']
    shared = request['shared']
    print('running: ' + name)

    with open('request.json', 'w') as f:
        json.dump(request, f, indent=4)

    file_id = shared.split('/')[-1] # get ID
    url = GOOGLE_EXPORT + file_id
    file = 'master.ipynb'
    
    src = ''
    with urlopen(url) as r:
        src = r.read().decode()

    src = src.replace("'colab'","'notebook'")
    nb = nbformat.reads(src, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb)
    with open(file, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    # the following nonsense is to work around issue with ipynb.. ugh 
    with open(file) as f:
        newText=f.read().replace('"python3"','"python3", "language": "python"')
    with open(file, "w") as f:
        f.write(newText)    
    
    html_exporter = HTMLExporter()
    html_exporter.exclude_input = True
    html_data, resources = html_exporter.from_notebook_node(nb)
    html_data = html_data.replace('</head>',"""
        <style>
            .container { width: 100% } 
            .prompt { min-width: 0 } 
            div.output_subarea { max-width: 100% }
            body { margin: 0; padding: 0; }
            div#notebook { padding-top: 0; }
        </style>
        </head>
    """)
    html_data = html_data.replace('''
<div class="cell border-box-sizing code_cell rendered">

</div>''','')
    with open(name + ".html", "w") as f:
        f.write(html_data)  
    trace('run completed')        