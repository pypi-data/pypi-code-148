import os

#remove zip file if exists
def remove_zip(zip_name):
    if os.path.isfile(zip_name):
        os.remove(zip_name)
        print("ZIP file removed: " + zip_name)
    else:
        return "ZIP not exist: " + zip_name