class Top100ProspectLeads:
    def __init__(self):
        self.leads = []

    def add_leads(self, leads):
        self.leads.extend(leads)
        self.leads = self.leads[:100]

    def get_leads(self):
        return self.leads
