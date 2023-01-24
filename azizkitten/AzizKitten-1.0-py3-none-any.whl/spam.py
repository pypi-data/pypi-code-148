class spam():
    def start():
        import pip
        import platform
        import os
        pip.main(["install", "--user", "pyautogui"])
        import pyautogui as spam
        if(platform.system().lower()=="windows"):
            cmd='cls'
        else:
            cmd='clear'
        os.system(cmd)
        import time
        limit = int(input("Select limit of the messages:\n>>    "))
        if limit == 0:
            print("Sorry, limit can't be 0")
        elif limit < 0:
            print("Sorry, limit can't be negative")
        else:
            msg = input("Enter the message:\n>>    ")
            time.sleep(3)
            while limit > 0:            
                spam.typewrite(msg)
                spam.press('Enter')
                limit -= 1
