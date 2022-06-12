from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingList, Tag)

EMPTY_VALUE = '<-EMPTY->'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag model representation in admin panel"""
    list_display = ('id', 'tag_name', 'tag_color', 'tag_slug')
    search_fields = ('tag_name',)
    list_filter = ('tag_name',)
    empty_value_display = EMPTY_VALUE


class IngredientRecipeInline(admin.TabularInline):
    """IngredientRecipe model representation in admin panel"""
    model = IngredientRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient model representation in admin panel"""
    list_display = ('id', 'ingredient_name', 'measurement_unit')
    search_fields = ('ingredient_name',)
    list_filter = ('ingredient_name',)
    inlines = (IngredientRecipeInline,)
    empty_value_display = EMPTY_VALUE


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe model representation in admin panel"""
    list_display = ('id', 'recipe_name', 'author')
    search_fields = ('author', 'recipe_name', 'tags')
    inlines = (IngredientRecipeInline,)
    empty_value_display = EMPTY_VALUE

    def is_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Favorite model representation in admin panel"""
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_VALUE


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """ShoppingList model representation in admin panel"""
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_VALUE
