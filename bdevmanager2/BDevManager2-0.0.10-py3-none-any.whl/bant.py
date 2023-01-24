class BANT:
    def __init__(self):
        self.budget_notes = ""
        self.authority_notes = ""
        self.needs_notes = ""
        self.timeline_notes = ""

    def capture_budget_notes(self):
        print("Please enter budget notes:")
        self.budget_notes = input()

    def capture_authority_notes(self):
        print("Please enter authority notes:")
        self.authority_notes = input()

    def capture_needs_notes(self):
        print("Please enter needs notes:")
        self.needs_notes = input()

    def capture_timeline_notes(self):
        print("Please enter timeline notes:")
        self.timeline_notes = input()

    def get_notes(self):
        return {
            "budget_notes": self.budget_notes,
            "authority_notes": self.authority_notes,
            "needs_notes": self.needs_notes,
            "timeline_notes": self.timeline_notes,
        }



