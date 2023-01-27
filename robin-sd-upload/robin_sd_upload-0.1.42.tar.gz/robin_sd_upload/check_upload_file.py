import os
import logging

def check_upload_file(upload_file):
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
