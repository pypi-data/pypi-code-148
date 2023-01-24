import tkinter as tk
from crm import CRM 

import pandas as pd

class GUI:
    def __init__(self):
     
        self.root = tk.Tk()
        self.root.title("Your Pocket CRM")
        self.root.geometry("800x600")
        
        self.crm = CRM()
       
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_entry = tk.Entry(self.root)
        self.email_label = tk.Label(self.root, text="Email:")
        self.email_entry = tk.Entry(self.root)
        self.phone_label = tk.Label(self.root, text="Phone:")
        self.phone_entry = tk.Entry(self.root)
        self.notes_label = tk.Label(self.root, text="Notes:")
        self.notes_text = tk.Text(self.root, width=30, height=5)
        self.add_button = tk.Button(
            self.root, text="Add Customer", command=self.add_customer)
        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.email_label.grid(row=1, column=0)
        self.email_entry.grid(row=1, column=1)
        self.phone_label.grid(row=2, column=0)
        self.phone_entry.grid(row=2, column=1)
        self.notes_label.grid(row=3, column=0)
        self.notes_text.grid(row=3, column=1, columnspan=2)
        self.add_button.grid(row=5, column=0)
        self.view_csv_button = tk.Button(
            self.root, text="View CSV", command=self.view_csv)
        self.tree = tk.Text(self.root, width=60, height=25)
        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.email_label.grid(row=1, column=0)
        self.email_entry.grid(row=1, column=1)
        self.phone_label.grid(row=2, column=0)
        self.phone_entry.grid(row=2, column=1)
        self.notes_label.grid(row=3, column=0)
        self.notes_text.grid(row=4, column=1)
        self.add_button.grid(row=5, column=0)
        self.view_csv_button.grid(row=8, column=0)
        self.tree.grid(row=7, column=1, columnspan=1)


    def add_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        notes = self.notes_text.get("1.0", "end-1c")
        self.crm.add_customer(name, email, phone, notes)
        self.crm.save_account("accounts.csv")
 
    def view_csv(self):
        df = pd.read_csv("accounts.csv")  
        df = df.to_json(orient='records')
        self.tree.insert(tk.END, '\n'+df)
        


