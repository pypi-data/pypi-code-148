import datetime
from json import load
from pandas import read_csv
from numpy import nan as nanvalue
from ModelObject import ModelObject
import queries


def init(models=True):
    global size_to_weight
    global config
    global user_config
    global bounds
    global geo_dict
    global fruits_available
    global dep_path
    global size_scale
    global countries
    global varieties
    global fruit_gr

    with open('dep\config.json', "r", encoding='utf8') as json_file:
        config = load(json_file)

    with open('dep\pref.json', "r", encoding='utf8') as json_file:
        user_config = load(json_file)

    with open('dep\site_to_geo_category.json', "r", encoding='utf8') as json_file:
        geo_dict = load(json_file)
    size_to_weight = read_csv( 'dep\size_to_weight.csv')
    fruit_gr=read_csv('dep\growth-rate-by-varieties.csv')


    # countries, varieties
    countries,varieties = queries.get_dfs()
    countries['country'] = countries['country'].str.lower()

    fruits_available = config['fruits_available']
    dep_path = config["dependencies_path"]
    size_scale = user_config["size_scale"]
    bounds=user_config["bounds"]
    #size_scale = config["size_scale"]


    if models:
        global models_objects
        models_objects = read_models()



def read_models():
    try:
        models_data_frame = open_models_info()
        samples_data_frame = open_models_samples()
        modelsObject = []
        for index, model_info in models_data_frame.iterrows():
            new_ModelObject = ModelObject(row=model_info.replace(nanvalue, '', regex=True),
                                                      samples=samples_data_frame[samples_data_frame['model_id'] == model_info['model_id']])
            # In case that no formula is inserted to a given model in models info
            if new_ModelObject.get_model_formula() is None:
                continue
            modelsObject.append(new_ModelObject)
        return modelsObject
    except Exception as e:
        print(repr(e))
        Exception('Cannot read models from file')
        pass


def open_models_info():
    path = 'dep\models_info.csv'
    df = read_csv(path)
    return df


def open_models_samples():
    path = 'dep\models_samples.csv'

    df = read_csv(path)
    return df






