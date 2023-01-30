import os, glob, shutil, json, pickle
import numpy as np

__version__ = "0.1.0"

def help():
    
    print("List of functions")

    print("- make_dir")
    print("- sorted_list")
    print("- key_parsing")

    print("- read_json")
    print("- save_json")

    print("- save_pkl")
    print("- load_pkl")

def make_dir(path, refresh=False):

    try: os.mkdir(path)
    except:
        if(refresh):
            shutil.rmtree(path)
            os.mkdir(path)

def sorted_list(path):

    tmplist = glob.glob(path)
    tmplist.sort()

    return tmplist

def key_parsing(dic, key, default):

    try: return dic[key]
    except: return default

def read_json(path):

    with open(path, "r") as json_file:
        dic = json.load(json_file)

    return dic

def save_json(path, dic):

    list_del = []
    for idx_key, name_key in enumerate(dic.keys()):
        value = dic[name_key]
        if(isinstance(value, int) or isinstance(value, float)): pass
        elif(isinstance(value, np.int64)): dic[name_key] = int(value)
        elif(isinstance(value, np.float32)): dic[name_key] = float(value)
        else: dic[name_key] = str(value)

    with open(path, 'w') as json_file:
        json.dump(dic, json_file)

def save_pkl(path, pkl):

    with open(path,'wb') as fw:
        pickle.dump(pkl, fw)

def load_pkl(path):

    with open(path, 'rb') as fr:
        pkl = pickle.load(fr)

    return pkl
