# WTFPL

import tkinter as tk


class App (tk.Tk):
    def __init__(self, refresh_rate = 1000):
        tk.Tk.__init__(self)
        self.title("Launcher")
        tk.Label(self,text="Launch panel",justify="center").grid(row=0,columnspan=4)
        self.lines = []
        self.refresh_rate = refresh_rate
        self.after(self.refresh_rate,self.checkProcesses)

        for i in range(4):
            self.columnconfigure(i, weight=1)

    def addApplication(self,ma):
        idx = len(self.lines) + 1
        self.lines.append(Line(self,ma,idx))



    def checkProcesses(self):
        for line in self.lines:
            line.check()
        self.after(self.refresh_rate,self.checkProcesses)

    def stopAll(self):
        for line in self.lines:
            line.quitApp()

class Line:
    # does not inherit Frame because grid layout is shared with parent
    # might switch to pack() instead
    def __init__(self,master,ma,row):
        self.master = master
        self.ma = ma
        self.row = row
        self.l = tk.Label(master,text=ma.name)
        self.l.grid(row=row,column=0)
        self.updateLabelColor()
        self.c = tk.Canvas(master,width=20,height=20,bg="purple")
        self.c.grid(row=row,column=1,sticky="news")
        self.buttonRun = tk.Button(master,text="▶",command=self.runApp)
        self.buttonRun.grid(row=row,column=2,sticky="news")
        self.buttonStop = tk.Button(master,text="■",command=self.stopApp)
        self.buttonStop.grid(row=row,column=3,sticky="news")
        self.buttonRestart = tk.Button(master,text="↺",command=self.restartApp)
        self.buttonRestart.grid(row=row, column=4, sticky="news")

        self.returnStatus = StatusLight(master)
        self.returnStatus.grid(row=row, column=5, sticky="news")

        master.rowconfigure(row,weight=1)

    def runApp(self):
        self.returnStatus.setColor("grey")
        self.master.after(0,self.doRunApp)

    def doRunApp(self):
        self.ma = self.ma.launch()
        self.updateLabelColor()

    def stopApp(self):
        self.ma.terminate()
    def restartApp(self):
        self.stopApp()
        self.master.after(10,self.runApp())
    def quitApp(self):
        self.ma.terminateIfNonpersistent()
    def check(self):
        if self.ma.running():
            self.c.config(bg="green")
            self.buttonRun.config(state=tk.DISABLED)
            self.buttonStop.config(state=tk.NORMAL)
            self.returnStatus.setColor("grey")
        else:
            self.c.config(bg="red")
            self.buttonRun.config(state=tk.NORMAL)
            self.buttonStop.config(state=tk.DISABLED)
            self.returnStatus.setColor("green" if self.ma.poll() == 0 else "red")

    def updateLabelColor(self):
        self.l["fg"] = "blue" if self.ma.isAquired() else "black"


class StatusLight(tk.Canvas):
    def __init__(self,master,**args):
        args["height"] = args["height"] if "height" in args else 20
        args["width"] = args["width"] if "width" in args else 20
        args["bg"] = args["bg"]  if "bg" in args else master["bg"]
        tk.Canvas.__init__(self,master,**args)
        self.o = self.create_oval(5,5,15,15,fill="grey",outline="black")
    def setColor(self,color):
        self.itemconfig(self.o,fill = color)
