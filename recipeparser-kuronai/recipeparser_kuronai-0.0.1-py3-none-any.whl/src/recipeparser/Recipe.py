class Recipe:


    def __init__(self, ingredients, steps, title):
        self.ingredients = ingredients
        self.steps = steps
        self.title = title

    def print_out(self):
        print(f"====={self.title}=====")
        print("------Ingredients-------")
        for ingredient in self.ingredients:
            print(f"\t- {ingredient}")
        print("---------------------")

        print("------Steps------")
        step_no = 1
        for step in self.steps:
            print(f"\tStep {step_no}\n\t {step}")
            step_no += 1
        print("-----------------")