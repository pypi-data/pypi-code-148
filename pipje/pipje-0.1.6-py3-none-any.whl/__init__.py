from pipje import pipje
import pipje
import sys
def showimage(TITLE, UserURL):
    from PIL import Image, ImageTk
    from urllib.request import urlopen
    import tkinter as tk
    root = tk.Tk()
    root.title(TITLE)
    root.lift()
    URL = UserURL
    if URL == "":
        URL = "https://i.imgur.com/1sfOxTw_d.webp?maxwidth=760&fidelity=grand"
    try:
        u = urlopen(URL)
    except:
        print("Error!, Please provide a valid URL.")
        sys.exit()
    raw_data = u.read()
    u.close()
    photo = ImageTk.PhotoImage(data=raw_data) # <-----
    label = tk.Label(image=photo)
    label.image = photo
    label.pack()
    root.mainloop()
showimage("DIKKE KAT", "https://dierenkliniekputten.nl/wp-content/uploads/2015/09/dikke-kat.jpg")