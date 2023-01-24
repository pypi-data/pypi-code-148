class GameLoop:
    def __init__(self, today_target, todays_activity, bant):
        self.today_target = today_target
        self.todays_activity = todays_activity
 
        self.bant = bant
       
    def start(self):
        
        while True:
            target = self.today_target.get_next_target()
            print("Current target: ", target)
            print(
                "Enter 'e' to edit the target, 's' to save and move to the next target, or 'q' to quit:")
            user_input = input()
            if user_input == "e":
                self.bant.capture_budget_notes()
                self.bant.capture_authority_notes()
                self.bant.capture_needs_notes()
                self.bant.capture_timeline_notes()
                
                self.todays_activity.add_task(target, self.bant.get_notes())
                self.todays_activity.get_tasks()
            elif user_input == "s":
                self.todays_activity.add_task(target, self.bant.get_notes())
                
            elif user_input == "q":
                self.todays_activity.get_tasks()

                break
            else:
                print("Invalid input.")


