import os

def check_upload_file(upload_file):
    if os.path.isfile(upload_file):
        print("File exists: " + upload_file)
    else:
        return "File not exist: " + upload_file + " - please upload a software version first"
