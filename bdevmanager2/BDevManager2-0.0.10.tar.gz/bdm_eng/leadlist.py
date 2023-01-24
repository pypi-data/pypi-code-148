import csv

class LeadList:
    def __init__(self, file_name):
        self.file_name = file_name

    def process_leads(self, max_leads=1000):
        leads = []
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                if i >= max_leads:
                    break
                leads.append(row)
        return leads
