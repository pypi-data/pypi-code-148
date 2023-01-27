import os
import logging

def check_upload_file(upload_file, version_name):
    # make sure not double / in path
    if upload_file.endswith("/"):
        upload_file = upload_file[:-1]
    # creating path from upload_file and version_name
    upload_file = upload_file + "/" + version_name
    logging.info("Checking upload file...")
    if os.path.isdir(upload_file):
        logging.info("Folder exists: " + upload_file)
        for root, dirs, files in os.walk(upload_file):
            for file in files:
                if file == "Packages.gz" or file == "Packages":
                    logging.info("Packages file found: " + file + " ,assuming this is a valid folder for upload")
                    return True
                else:
                    logging.error("Packages file not found: " + file)
                    return False
    else:
        logging.error("File not valid or not exist: " + upload_file)
        return False
