import os

def check_upload_file(upload_file):
    print ("Checking upload file...")
    if os.path.isdir(upload_file):
        print("Folder exists: " + upload_file)
        for root, dirs, files in os.walk(upload_file):
            for file in files:
                if file == "Package.gz" or file == "Package":
                    print("Package file found: " + file + "assuming this is a valid folder for upload")
                    return True
    else:
        print ("File not valid or not exist: " + upload_file)
        return False