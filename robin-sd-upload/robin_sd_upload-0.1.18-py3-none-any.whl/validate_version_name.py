import validators

def validate_version_name(version_name):
    if validators.length(version_name, min=1, max=20) == False:
        print("Version name is not valid: " + version_name)
        exit()
    else:
        print("Version name is valid: " + version_name)
        return version_name