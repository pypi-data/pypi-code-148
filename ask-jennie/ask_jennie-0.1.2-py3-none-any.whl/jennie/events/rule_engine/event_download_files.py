"""
event_name : download-files
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import json
import os
from jennie.events.constants import *
from jennie.events.utils.helper import upload_text_file, download_text_file

class event_download_files():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_DOWNLOAD_FILES,
            KEY_FILES: [{
                KEY_FILE_LINK: "file_server_link",
                KEY_OUT_PATH: "output_path_for_downloaded_files"
            }]
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        for file in event_info[KEY_FILES]:
            file_content = download_text_file(file[KEY_FILE_LINK])
            open(file[KEY_OUT_PATH], "w").write(file_content)
        return True

    def build_event(self, files=None):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_DOWNLOAD_FILES
        }
        if files == None:
            files = []
            keep_adding = True
            while(keep_adding):
                input_file_name = input(INPUT_UPLOAD_FILEPATH)
                input_file_out_path = input(INPUT_UPLOAD_OUT_PATH)
                if input_file_name not in input_file_out_path:
                    input_file_out_path = input_file_out_path

                current = {
                    KEY_OUT_PATH: input_file_out_path
                }
                current[KEY_FILE_LINK] = upload_text_file(
                    input_file_name,
                    app_name=self.app_name,
                    type=self.type,
                    user_key=self.user_key
                )
                files.append(current)

                do_continue = input("Add more files (y/n)")
                if do_continue.replace(" ", "").lower() != "y":
                    keep_adding = False
        else:
            for file in files[KEY_FILES]:
                file[KEY_FILE_LINK] = upload_text_file(
                    file[KEY_FILE_PATH],
                    app_name=self.app_name,
                    type=self.type,
                    user_key=self.user_key
                )
                del file[KEY_FILE_PATH]
            return files
        event_info[KEY_FILES] = files
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """

        if KEY_FILES not in event_info:
            print(ERR_FILES_NOT_PRESENT)
            return False

        if str(type(event_info[KEY_FILES])) != "<class 'list'>":
            print(ERR_FILES_SHOULD_BE_LIST)
            return False

        for file in event_info[KEY_FILES]:
            if KEY_FILE_LINK not in file:
                print ("missing file link in one of the event file info")
                return False

            if KEY_OUT_PATH not in file:
                print("missing output path in one of the event file info")
                return False

        return event_info
