from pipje import pipje
import pipje
import sys
def showimage(UserTITLE, UserURL):
    from PIL import Image, ImageTk
    from urllib.request import urlopen
    import tkinter as tk
    root = tk.Tk()
    URL = UserURL
    TITLE = UserTITLE
    root.title(TITLE)
    root.lift()
    if URL == '':
        URL = "https://i.imgur.com/1sfOxTw_d.webp?maxwidth=760&fidelity=grand"
    if TITLE == '':
        TITLE = "Pipje"
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
