import validators
import logging

def validate(radarType, version_name):
    radarTypearray = ["elvira", "iris", "birdradar"]
    if validators.length(radarType, min=1, max=50) == False:
        logging.error("Radar type is not valid: " + radarType)
        # print("Radar type is not valid: " + radarType)
        exit()
    if radarType not in radarTypearray:
            logging.error("Radar type is not valid: " + radarType)        
            # print("Radar type is not valid: " + radarType)
            exit()
    else:
        logging.info("Radar type is valid: " + radarType)
        # print("Radar type is valid: " + radarType)
        
    if validators.length(version_name, min=1, max=20) == False:
        logging.error("Version name is not valid: " + version_name)
        # print("Version name is not valid: " + version_name)
        exit()
    else:
        logging.info("Version name is valid: " + version_name)
        # print("Version name is valid: " + version_name)
        return radarType, version_name
