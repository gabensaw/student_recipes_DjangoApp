from django.contrib import admin
from .models import Recipe
from .models import Ingredient
from .models import Nutrient

# models registered and visible in the administration panel
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Nutrient)
