import os
from parser.feature_engineering_parser import FeatureEngineeringParser
from parser.model_parser import ModelParser
from parser.YAML_parser import YAMLParser
from typing import Dict


def get_config() -> Dict:
    config_data = {}
    initial_parser = YAMLParser
    feature_engineering_parser = FeatureEngineeringParser
    model_parser = ModelParser

    for file in os.listdir("yamls"):
        filepath = os.path.join("yamls", file)
        config = initial_parser(filepath).parse()

        features_config, columns_set_alias = feature_engineering_parser(filepath).parse(
            config["feature_engineering"]
        )
        config_data["features_config"] = features_config
        del config["feature_engineering"]

        model_config = model_parser(columns_set_alias).parse(config["model"])
        config_data["model_config"] = model_config
        del config["model"]

    return config_data


if __name__ == "__main__":
    config = get_config()
    print("FEATURES")
    print(config["features_config"])
    print(3 * "\n")
    print(20 * "-")
    print(3 * "\n")
    print("\nMODEL")
    print(config["model_config"])
