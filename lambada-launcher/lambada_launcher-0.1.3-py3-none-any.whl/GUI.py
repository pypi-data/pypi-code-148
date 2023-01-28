# WTFPL

import tkinter as tk

class App (tk.Tk):
    def __init__(self, refresh_rate = 1000):
        tk.Tk.__init__(self)
        self.title("Launcher")
        tk.Label(self,text="Launch panel",justify="center").grid(row=0,columnspan=4)
        self.mapps = []
        self.refresh_rate = refresh_rate
        self.after(self.refresh_rate,self.checkProcesses)

        for i in range(4):
            self.columnconfigure(i, weight=1)

    def addApplication(self,ma):
        self.mapps.append(ma)
        idx = len(self.mapps)
        tk.Label(self,text=ma.name).grid(row=idx,column=0)
        c = tk.Canvas(self,width=20,height=20,bg="purple")
        c.grid(row=idx,column=1,sticky="news")
        tk.Button(self,text="▶",command=lambda :self.runApp(idx-1)).grid(row=idx,column=2,sticky="news")
        tk.Button(self,text="■",command=lambda :self.stopApp(idx-1)).grid(row=idx,column=3,sticky="news")
        self.rowconfigure(idx,weight=1)

    def checkProcesses(self):
        for i,ma in enumerate(self.mapps):
            status = self.grid_slaves(row=i+1,column=1)[0]

            if ma.running():
                status.config(bg="green")
                self.grid_slaves(row=i+1,column=2)[0].config(state=tk.DISABLED)
                self.grid_slaves(row=i+1,column=3)[0].config(state=tk.NORMAL)
            else:
                status.config(bg="red")
                self.grid_slaves(row=i+1,column=2)[0].config(state=tk.NORMAL)
                self.grid_slaves(row=i+1,column=3)[0].config(state=tk.DISABLED)

        self.after(self.refresh_rate,self.checkProcesses)

    def runApp(self,i):
        self.mapps[i].launch()
    def stopApp(self,i):
        self.mapps[i].terminate()
