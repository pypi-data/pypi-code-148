from pyfiglet import Figlet

from .coddj import main



f = Figlet(font="slant")
print(f.renderText("MP3 Player"))

while True:
    try:
        if EXIT_TOGGLE:
            break
        EXIT_TOGGLE = main()
    except KeyboardInterrupt:
        break
    print("Exiting, goodbye!")
