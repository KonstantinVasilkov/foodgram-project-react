from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """Model for recipes"""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    recipe_name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    recipe_image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/image/'
    )
    recipe_description = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        to='Ingredient',
        verbose_name='Ингредиенты',
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        to='Tag',
        verbose_name='Теги'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления не может быть меньше 1 минуты.'
            ),
        )
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.recipe_name


class Ingredient(models.Model):
    """Model for Ingredients"""
    ingredient_name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=256
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64
    )

    class Meta:
        ordering = ('ingredient_name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.ingredient_name


class Tag(models.Model):
    """Model for tags"""
    tag_name = models.CharField(
        verbose_name='Название тега',
        max_length=128,
        unique=True
    )
    tag_color = models.CharField(
        verbose_name='Цвет тега',
        max_length=7,
        unique=True
    )
    tag_slug = models.SlugField(
        verbose_name='Ссылка на тег',
        max_length=128,
        unique=True
    )

    class Meta:
        ordering = ('tag_name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag_name


class IngredientRecipe(models.Model):
    """Model of an ingredient in recipe"""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(
                1,
                message='Количесвто ингредиента не может быть 0.'
            ),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'{self.ingredient.ingredient_name} - {self.amount}'
                f' {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    """Model for favorite user's recipes"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class ShoppingList(models.Model):
    """Model for user's shopping list"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_list'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
