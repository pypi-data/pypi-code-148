import os
import shutil
import time
from pathlib import Path
from datetime import datetime


class PersistentStorage:
    """ Connect to Persistent Storage """

    def __init__(self):
        """ Initialize the class
        -----------------------------
        """
        self.base_path = '/mnt/datascience-persistent-store-file-share/'

    def connect(self):
        if not Path(self.base_path).exists():
            return ValueError("The current project doesn't have access to persistent storage, please check YAML file.")

    def format_path(self, path):
        self.connect()
        if self.base_path in path:
            return path
        else:
            return os.path.join(self.base_path, path)

    def create_folder(self, path):
        self.connect()
        created = True
        folder_path = self.format_path(path)
        try:
            Path(folder_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(e)
            created = False

        return created

    def create_file(self, data, path, file_name=None):
        self.connect()
        created = True
        folder_path = self.format_path(path)
        if file_name is None:
            file_path = os.path.join(folder_path, datetime.now().strftime("%H_%M_%S_%f"))
        else:
            file_path = os.path.join(folder_path, file_name)

        try:
            with open(file_path, 'w') as f:
                f.write(data)
                f.close()
        except Exception as e:
            print(e)
            created = False

        return created

    def list_files(self, path):
        self.connect()
        folder_path = self.format_path(path)
        files = []
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            files.sort()
        except Exception as e:
            print(e)

        return files

    def move_files(self, source_folder, target_folder):
        self.connect()
        source_path = self.format_path(source_folder)
        target_path = self.format_path(target_folder)
        source_files = self.list_files(source_folder)

        i = 0
        while len(source_files) > 0 and i <= 5:
            for f in source_files:
                incoming_file_path = os.path.join(source_path, f)
                received_file_path = os.path.join(target_path, f)
                shutil.move(incoming_file_path, received_file_path)

            time.sleep(5)
            source_files = self.list_files(source_folder)
            i += 1

        moved_files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
        moved_files.sort()
        return moved_files

    def delete_folder(self, path):
        self.connect()
        folder_path = self.format_path(path)
        obj = Path(folder_path)

        delete = True
        try:
            if obj.exists():
                shutil.rmtree(folder_path)
        except Exception as e:
            print(e)
            delete = False

        return delete

    def delete_file(self, path):
        self.connect()
        file_path = self.format_path(path)
        obj = Path(file_path)

        delete = True
        try:
            if obj.exists():
                os.remove(file_path)
        except Exception as e:
            print(e)
            delete = False

        return delete
