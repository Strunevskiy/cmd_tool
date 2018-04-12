from project.src.base.entity import Beverage, Ingredient
from project.src.utils.file import PropertyUtil

menu_storage_path = "./resource/menu.properties"
beverage_section = "BEVERAGE"
ingredients_section = "INGREDIENT"


class BeverageRepository(object):

    def __init__(self):
        self._property_util = PropertyUtil()

    def get_beverages(self):
        beverages = self._property_util.get_entries(menu_storage_path, beverage_section);
        beverage_bunch = []
        for beverage in beverages:
            beverage_bunch.append(Beverage(beverage[0], beverage[1]))
        return beverage_bunch

    def is_beverage_present(self, reg_type):
        beverages = self.get_beverages()
        is_present = False
        for beverage in beverages:
            beverage_type = beverage[0]
            if beverage_type == reg_type:
                is_present = True
        return is_present


class IngredientRepository(object):

    def __init__(self):
        self._property_util = PropertyUtil()

    def get_ingredients(self):
        ingredients = self._property_util.get_entries(menu_storage_path, ingredients_section);
        ingredient_bunch = []
        for ingredient in ingredients:
            ingredient_bunch.append(Ingredient(ingredient[0], ingredient[1]))
        return ingredient_bunch

    def is_ingredient_present(self, reg_type):
        ingredients = self.get_beverage_ingredients()
        is_present = False
        for ingredient in ingredients:
            ingredient_type = ingredient[0]
            if ingredient_type == reg_type:
                is_present = True
        return is_present
