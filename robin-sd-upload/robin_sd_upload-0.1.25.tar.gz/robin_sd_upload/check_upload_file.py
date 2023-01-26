import os

def check_upload_file(upload_file):
    # convert user file input path to path
    upload_file = os.path.abspath(upload_file)
    print ("Checking if upload file exists: " + upload_file)
    if os.path.isfile(upload_file):
        print("File exists: " + upload_file)
    else:
        return "File not exist: " + upload_file + " - please upload a software version first"
