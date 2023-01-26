import urlutils
import Recipe


def parse_recipe(dom):
    json_metadata = urlutils.get_json_metadata(dom)
    ingredients = get_ingredients(json_metadata)
    steps = get_steps(json_metadata)
    title = get_title(dom)
    recipe = Recipe(ingredients=ingredients, steps=steps, title=title)
    return recipe


def get_ingredients(json_metadata):
    ingredients = json_metadata["recipeIngredient"]
    return ingredients


def get_steps(json_metadata):
    steps_from_json = json_metadata["recipeInstructions"]
    if type(steps_from_json) is list:
        steps = []
        for step in steps_from_json:
            steps.append(step["text"])
    return steps


def get_title(dom):
    recipe_title = dom.find("meta", property="og:title")["content"]

    if recipe_title is None:
        recipe_title = dom.title.text

    return recipe_title
