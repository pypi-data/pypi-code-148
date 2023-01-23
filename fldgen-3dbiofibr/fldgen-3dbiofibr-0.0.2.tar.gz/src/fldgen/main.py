import tkinter
import tkinter.messagebox
import customtkinter
from fldGen import fld_gen
from tkinter import filedialog
import tkinter.messagebox
from pathlib import Path
from datetime import datetime

now = datetime.now()
date_and_time= now.strftime("%Y-%m-%d_%H-%M-%S")

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
       
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
     
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")
   
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)


        # Title 
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Fiber Length Distribution\nGenerator",
                                                   text_font=("Roboto Medium", -40),
                                                   height=100,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.CENTER)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)


        # Version Label
        self.version_label = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="3D BioFibR\n\nVersion 1.1",   
                                                   text_font=("Roboto Medium", -14),     
                                                   height=5,
                                                   justify=tkinter.CENTER)
        self.version_label.grid(column=0, row=1, sticky="swe", padx=10, pady=10, ipady=2)


        # Export as .CSV 
        self.csv_switch = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="Export as csv")
        self.csv_switch.grid(row=1, column=2, columnspan=1, pady=1, padx=20, sticky="we")

        self.csv_entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=20,
                                            placeholder_text="Enter file name")
        self.csv_entry.grid(row=2, column=2, columnspan=1, pady=2, padx=20, sticky="we")


        #Select the number of bins 
        self.conversion_entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=20,
                                            placeholder_text=r"0.5940 pixels/um")
        self.conversion_entry.grid(row=3, column=2, columnspan=1, pady=2, padx=20, sticky="we")


        # File vs. Folder
        self.file_or_folder = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=["Select Folder", "Select File"])
        self.file_or_folder.grid(row=4, column=2, columnspan=1, pady=2, padx=20, sticky="we")

         
        # Enables MIN and MAX Fiber Lengths
        self.small_fiber_check = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="Exclude smaller fibers")
        self.small_fiber_check.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        self.large_fiber_check = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="Exclude larger fibers")
        self.large_fiber_check.grid(row=4, column=1, pady=10, padx=20, sticky="w")


        # MIN and MAX Fiber Length Entry Boxes 
        self.max_fiber_length_var = 70
        self.max_fiber_length_entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Max Fiber Length (μm)", textvariable = self.max_fiber_length_var)
        self.max_fiber_length_entry.grid(row=5, column=1, columnspan=1, pady=20, padx=20, sticky="we")
        self.min_fiber_length_entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Min Fiber Length (μm)")
        self.min_fiber_length_entry.grid(row=5, column=0, columnspan=1, pady=20, padx=20, sticky="we")


        # File Explorer Button
        self.file_explorer_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="File Explorer",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.browseFiles)
        self.file_explorer_button.grid(row=5, column=2, columnspan=1, pady=20, padx=20, sticky="we")


        # set default values
        self.small_fiber_check.select()
        #self.large_fiber_check.select()
    

    # Initiated FLD-Generator 
    def browseFiles(self):

        if self.file_or_folder.get() == "Select Folder":
            dir = filedialog.askdirectory()
        else:
            dir = filedialog.askopenfile().name

        if len(self.max_fiber_length_entry.get()) > 0 and self.large_fiber_check.get() == 1:
            max_fiber_length = int(self.max_fiber_length_entry.get())
        else:
            max_fiber_length = 1000000

        if len(self.min_fiber_length_entry.get()) > 0 and self.small_fiber_check.get() == 1:
            min_fiber_length = int(self.min_fiber_length_entry.get())
        else:
            min_fiber_length = 20

        if len(self.csv_entry.get()) > 0 and self.csv_switch.get() == 1:
            csv_dir = Path(__file__).parent.absolute()
            filename = self.csv_entry.get()
        elif self.csv_switch.get() == 1:
            csv_dir = Path(__file__).parent.absolute()
            filename = f"{date_and_time}_distribution_data" 
        else:
            csv_dir = None
            filename = f"{date_and_time}_distribution_data"

        if len(self.conversion_entry.get()) > 0:
            pixel_conversion = float(self.conversion_entry.get())
        else:
            pixel_conversion = 0.5940

        fld_gen(dir,min_fiber_length, max_fiber_length, csv_directory = csv_dir, filename = filename, pixel_conversion = pixel_conversion) 


    def browse_scv_dir():
        csv_dir = filedialog.askdirectory()


    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def on_closing(self, event=0):
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()