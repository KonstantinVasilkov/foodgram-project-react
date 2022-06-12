import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                                    Recipe, ShoppingList, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscribe, User

from .filters import IngredientFilter, RecipeFilter
from .mixins import RetrieveListViewSet
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          IngredientSerializer, PasswordSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShoppingListSerializer, SubscribeSerializer,
                          TagSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['POST'],
            detail=False,
            permission_classes=(IsAuthenticated, ))
    def set_password(self, request, pk=None):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = PasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(IsAuthenticated, ))
    def get_subscriptions(self, request):
        user = request.userw
        queryset = User.objects.filter(follower__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated, ))
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        subscribe = Subscribe.objects.filter(user=user, author=author)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if subscribe.exists():
                data = {
                    'errors': 'Вы уже подписаны на этого автора или'
                              ' пытаетесь подписаться на себя.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            if not subscribe.exists():
                data = {'errors': 'Вы не подписанны на этого пользователя.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(RetrieveListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientsViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(methods=['GET', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated, ))
    def get_favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if not in_favorite:
                favorite = Favorite.objects.create(user=user, recipe=recipe)
                serializer = FavoriteSerializer(favorite.recipe)
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not in_favorite:
                data = {'errors': 'Этого рецепта нет в избранных.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            in_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated, ))
    def get_shopping_list(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_shopping_list = ShoppingList.objects.filter(
            user=user,
            recipe=recipe
        )
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if not in_shopping_list:
                shopping_list = ShoppingList.objects.create(
                    user=user,
                    recipe=recipe
                )
                serializer = ShoppingListSerializer(shopping_list.recipe)
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not in_shopping_list:
                data = {'errors': 'Этого рецепта нет в списке покупок.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            in_shopping_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(IsAuthenticated, ))
    def download_shopping_list(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_list__user=request.user
        ).values(
            'ingredients__ingredient_name',
            'ingredient__measurement_unit'
        ).annotate(
            ingredient_amount=Sum('amount')
        ).value_list(
            'ingredients__ingredient_name',
            'ingredient__measurement_unit',
            'ingredient_amount'
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="shoppinglist.csv"')
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        for row in list(ingredients):
            writer.writerow(row)
        return response
