import utils
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re


def decorate_steps(steps):
    return [f'{count + 1}. {utils.make_first_letter_capital(step)}' \
        for count, step in enumerate(steps)]


def decorate_ingredients(ingredients):
    return ['• ' + utils.make_first_letter_capital(ingr) for ingr in ingredients]


class Recipe:
    def __init__(self, name, ingredients, steps):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
    

    def to_message(self):
        str_title = utils.make_first_letter_capital(self.name.lower())
        str_ingredients = '\n'.join(decorate_ingredients(self.ingredients))  # Multiple lines
        str_steps = '\n'.join(decorate_steps(self.steps))
        return '\n\n'.join([str_title, str_ingredients, str_steps])


class RecipeFactory:
    def __init__(self):
        self.ingr_to_steps = utils.Seq2SeqGenerator('FlightBlaze/ingr-to-steps')
        self.name_to_ingr = utils.Seq2SeqGenerator('FlightBlaze/name-to-ingr')


    @staticmethod
    def preprocess_step(raw_step):
        step = re.sub(' ,', ',', raw_step).strip()
        if step.endswith(','):  # Remove comma at the end
            step = step[:-1]
        return step


    @staticmethod
    def split_ingredients_str(ingrs):
        ingr_str = re.sub(' and ', ', ', ingrs)  # Replace 'and' with comma
        raw_ingr_list = ingr_str.split(',')
        raw_ingr_list = [ingr.strip() for ingr in raw_ingr_list]
        ingr_dict = dict.fromkeys(raw_ingr_list, 1)
        ingr_list = [kv[0] for kv in list(ingr_dict.items()) if kv[0] != '']
        return ingr_list


    def generate_ingredients_by_dish_name(self, dish_name):
        ingredients_str = self.name_to_ingr(dish_name)[0]
        return self.split_ingredients_str(ingredients_str)


    def generate_steps_by_ingredients(self, ingredients):
        steps_str = self.ingr_to_steps(ingredients)[0]
        steps_str = utils.replace_fahrengheit_with_celsius_str(steps_str)
        steps = steps_str.split('. ')
        steps = [self.preprocess_step(step) for step in steps]
        return steps


    def generate_recipe(self, dish_name):
        ingredients = self.generate_ingredients_by_dish_name(dish_name)
        steps = self.generate_steps_by_ingredients(', '.join(ingredients))
        return Recipe(dish_name, ingredients, steps)


recipeFactory = RecipeFactory()

# print(recipeFactory.generate_recipe('asian meatballs').to_message())
