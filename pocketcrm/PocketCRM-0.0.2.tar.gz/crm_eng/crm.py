import pandas as pd
import csv

class CRM:
    def __init__(self):
        self.customers = {}

    def save_account(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['name', 'email', 'phone', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for customer in self.customers.values():
                writer.writerow({'name': customer['name'], 'email': customer['email'],
                                'phone': customer['phone'], 'notes': customer['notes']})

    def add_customer(self, name, email, phone, notes):
        self.customers[name] = {'name': name,
                                'email': email, 'phone': phone, 'notes': notes}

    def update_customer(self, name, email=None, phone=None, notes=None):
        if name in self.customers:
            if email:
                self.customers[name]['email'] = email
            if phone:
                self.customers[name]['phone'] = phone
            if notes:
                self.customers[name]['notes'] = notes


    def get_customer(self, name):
        if name in self.customers:
            return self.customers[name]
        else:
            return None

    def ingest_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            self.add_customer(row['name'], row['email'],
                              row['phone'], row['notes'])


