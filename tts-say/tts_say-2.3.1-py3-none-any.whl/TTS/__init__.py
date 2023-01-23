import os

from say import HOME

def enable_service_now():
    if not os.path.isfile("/usr/lib/systemd/user/speak.service"):
        print("No listen service present.")
        print("To download it type:")
        print("    wget https://gitlab.com/waser-technologies/technologies/say/-/raw/main/speak.service.example")
        print("    mv speak.service.example /usr/lib/systemd/user/speak.service")
        sys.exit(1)
    if not os.path.exists(f"{HOME}/.config/systemd/user/default.target.wants/assistant.listen.service"):
        print("Say TTS service is disabled.")
        print("To enable it type:")
        print(f"systemctl --user enable --now speak")
        sys.exit(1)
