class LeadSource:
    def __init__(self):
        self.linkedin_leads = []
        self.clubhouse_leads = []
        self.ig_leads = []
        self.youtube_leads = []

    def add_linkedin_leads(self, leads):
        self.linkedin_leads.extend(leads)

    def add_clubhouse_leads(self, leads):
        self.clubhouse_leads.extend(leads)

    def add_ig_leads(self, leads):
        self.ig_leads.extend(leads)

    def add_youtube_leads(self, leads):
        self.youtube_leads.extend(leads)

    def get_leads(self):
        return {
            "linkedin_leads": self.linkedin_leads,
            "clubhouse_leads": self.clubhouse_leads,
            "ig_leads": self.ig_leads,
            "youtube_leads": self.youtube_leads,
        }



