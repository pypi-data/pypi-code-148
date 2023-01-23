import validators

def validate_radar_type(radarType):
    radarTypearray = ["elvira", "iris", "birdradar"]
    if validators.length(radarType, min=1, max=50) == False:
        print("Radar type is not valid: " + radarType)
        exit()
        #check if radar type is in the array
    if radarType not in radarTypearray:
            print("Radar type is not valid: " + radarType)
            exit()
    else:
        print("Radar type is valid: " + radarType)
        return radarType