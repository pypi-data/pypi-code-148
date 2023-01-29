class RecipeConverted:

    def __init__(self, _ingredients, _steps, _title):
        self.ingredients = _ingredients
        self.steps = _steps
        self.title = _title

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