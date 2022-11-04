from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, IngredientRecipe,
                     Follow, Favorite, ShoppingCart)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientRecipe)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
