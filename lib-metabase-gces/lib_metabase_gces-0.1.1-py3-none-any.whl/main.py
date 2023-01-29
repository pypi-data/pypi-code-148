import os

from parser.YAML_parser import YAMLParser
from parser.feature_engineering_parser import FeatureEngineeringParser
from parser.model_parser import ModelParser

if __name__ != "__main__":
    exit()   

def get_config():

    """
    The get_config() function reads YAML files in a specific directory, parses and extracts feature engineering configuration information and models. 
    It uses three different classes, YAMLParser, FeatureEngineeringParser and ModelParser, to read and parse the YAML files.
    The function starts by reading all the files in the specific 'src/yamls' directory and, 
    for each file, it creates a YAMLParser instance and calls the parse() method to read the file and return the initial settings. 
    It then creates instances of the FeatureEngineeringParser and the ModelParser and calls the parse() methods for these objects, passing the feature and model engineering settings, respectively.
    The feature and model engineering settings are then displayed in the console.
    """

    initialParser = YAMLParser
    featureEngineringParser = FeatureEngineeringParser
    modelParser = ModelParser

    for file in os.listdir('src/yamls'):
        filepath = os.path.join('src/yamls', file)
        config = initialParser(filepath).parse()
    
        features_configs, columns_set_alias = featureEngineringParser(filepath).parse(config['feature_engineering'])
        del config['feature_engineering']
        
        model_configs = modelParser(columns_set_alias).parse(config['model'])
        del config['model']
        
        print("FEATURES")
        print(features_configs)
        print(3*'\n')
        print(20*'-')
        print(3*'\n')
        print(model_configs)
         
get_config()
