from src.recipeparser_kuronai import recipeutils, urlutils
from src.recipeparser_kuronai.recipe import RecipeConverted

if __name__ == "__main__":
    #dom = urlutils.convert_to_dom("https://www.foodnetwork.com/recipes/food-network-kitchen/sweet-and-sour-couscous-stuffed-peppers-recipe-2121036")
    dom = urlutils.convert_to_dom("https://www.ricardocuisine.com/en/recipes/9657-barley-stew-with-sausage-meatballs")
    jsond = urlutils.get_json_metadata(dom)
    steps = recipeutils.get_steps(jsond)
    ingredients = recipeutils.get_ingredients(jsond)
    title = recipeutils.get_title(dom)
    new_recipe = RecipeConverted(ingredients, steps, title)
    new_recipe.print_out()