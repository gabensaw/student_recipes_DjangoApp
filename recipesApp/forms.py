from django import forms
from django.forms.models import inlineformset_factory
from .models import Recipe, Ingredient, Nutrient


# form class used to create recipe
class RecipeForm(forms.ModelForm):

    # class constructor with additional arguments assigned by foreign key
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = [
            'recipeName', 'description', 'instruction', 'recipeCategory', 'cost', 'cookingTime', 'portion',
            'skillsLevel', 'image'
        ]


# form class used to create ingredient
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['recipeName', 'ingredient']
        exclude = ['recipeName']


# form class used to create nutrients
class NutrientForm(forms.ModelForm):
    class Meta:
        model = Nutrient
        fields = ['recipeName', 'calories', 'fat', 'carbohydrate', 'fibre', 'protein', 'salt']
        exclude = ['recipeName']


# inline formset containing all the ingredients assigned to the recipe
IngredientInlineFormset = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    min_num=3,
    extra=0,
    can_delete=False
)

