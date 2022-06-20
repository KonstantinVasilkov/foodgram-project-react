from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from recipes import models

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=models.Tag.objects.all(),
        field_name='tags__slug'
    )
    is_favorite = filters.BooleanFilter(method='get_is_favorite')
    is_in_shopping_list = filters.BooleanFilter(
        method='get_is_in_shopping_list'
    )

    class Meta:
        model = models.Recipe
        fields = ('tags', 'author', 'is_favorite', 'is_in_shopping_list')

    def get_is_favorite(self, queryset, name, value):
        if value:
            return models.Recipe.objects.filter(
                favorite_recipe__user=self.request.user
            )
        return models.Recipe.objects.all()

    def get_is_in_shopping_list(self, queryset, name, value):
        if value:
            return models.Recipe.objects.filter(
                shopping_list__user=self.request.user)
        return models.Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = models.Ingredient
        fields = ('name',)
