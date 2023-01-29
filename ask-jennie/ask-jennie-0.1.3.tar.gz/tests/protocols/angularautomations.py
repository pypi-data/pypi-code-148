import os

class TestAngularAutomation():
    def __init__(self, debug):
        self.debug = debug
        self.base_dir = os.getcwd()
        print ("Base Test Dir : ", self.base_dir)

    def check_angular_automation_download(self):
        """
        Check if angular automation is properly downloaded.
        :return:
        """

        os.chdir(self.base_dir)
        if not os.path.exists("src/app/samnpletestfile.js"):
            raise ValueError("Unable to download automation")

        downloaded_content = open("tests/files/sampleprojects/sampleangular/src/app/samnpletestfile.js").read()
        input_content = open("tests/files/someappname/samnpletestfile.js").read()
        if input_content != downloaded_content:
            raise ValueError("Mis-matching content")

    def upload(self):
        os.chdir(self.base_dir)
        os.system("cd tests/files/someappname && python3 main.py angular automations upload")

        if self.debug:
            input("Tested jennie angular automations upload\nPress any key to continue >>")

    def download(self):
        os.chdir(self.base_dir)
        os.chdir("tests/files/sampleangular")
        os.system("python main.py angular automations download someappname")

    def update(self):
        os.chdir(self.base_dir)
        os.chdir("tests/files/someappname")
        json_file = open("jennie.conf.json").read().replace("sometag", "sometagnew")
        open("jennie.conf.json", "w").write(json_file)
        os.system("python main.py angular automations download update")

        if self.debug:
            input("Tested jennie angular automations update\nPress any key to continue >>")

    def delete(self):
        os.chdir(self.base_dir)
        os.chdir("tests/files/someappname")
        os.system("python main.py angular automations delete")

        if self.debug:
            input("Tested jennie angular automations delete\nPress any key to continue >>")

    @property
    def test(self):
        print ("Angular Automation : Testing Upload")
        self.upload()

        # print("Angular Automation : Testing Download")
        # self.download()

        # print("Angular Automation : Checking Download Content")
        # self.check_angular_automation_download()
        #
        # print("Angular Automation : Testing Update")
        # self.update()
        #
        # print("Angular Automation : Testing Delete")
        # self.delete()

        return True
