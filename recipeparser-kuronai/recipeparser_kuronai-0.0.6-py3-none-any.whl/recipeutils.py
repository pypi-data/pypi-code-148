from src.recipeparser_kuronai import urlutils
from src.recipeparser_kuronai.recipe import RecipeConverted

def parse_recipe(dom):
    json_metadata = urlutils.get_json_metadata(dom)
    ingredients = get_ingredients(json_metadata)
    steps = get_steps(json_metadata)
    title = get_title(dom)
    new_recipe = RecipeConverted(ingredients, steps, title)
    return new_recipe


def get_ingredients(json_metadata):
    ingredients = json_metadata["recipeIngredient"]
    return ingredients


def get_steps(json_metadata):
    json_txt = json_metadata["recipeInstructions"]
    steps = []

    if type(json_txt) is list:
        json_txt = json_txt[0]

    if "HowToSection" in json_txt.values():
        step_list = json_txt["itemListElement"]
        for step in step_list:
            steps.append(step["text"])

    return steps


def get_title(dom):
    recipe_title = dom.find("meta", property="og:title")["content"]

    if recipe_title is None:
        recipe_title = dom.title.text

    return recipe_title