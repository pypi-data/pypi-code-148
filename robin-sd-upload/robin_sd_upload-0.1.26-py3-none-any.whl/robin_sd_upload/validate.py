import validators

def validate(radarType, version_name):
    radarTypearray = ["elvira", "iris", "birdradar"]
    if validators.length(radarType, min=1, max=50) == False:
        print("Radar type is not valid: " + radarType)
        exit()
    if radarType not in radarTypearray:
            print("Radar type is not valid: " + radarType)
            exit()
    else:
        print("Radar type is valid: " + radarType)
        
    if validators.length(version_name, min=1, max=20) == False:
        print("Version name is not valid: " + version_name)
        exit()
    else:
        print("Version name is valid: " + version_name)
        return radarType, version_name
