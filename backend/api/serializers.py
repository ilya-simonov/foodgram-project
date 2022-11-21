from django.db import transaction
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Follow, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)
from users.models import User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True,
                                            source='ingredient.id')
    name = serializers.CharField(read_only=True,
                                 source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class IngredientCreateRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True, read_only=True, source='ingredient_recipes'
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']

    def get_is_favorited(self, obj):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        return user.favorite.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(user=user, recipe=obj).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = IngredientCreateRecipeSerializer(
        many=True, source='ingredient_recipes',
    )
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = ['tags', 'ingredients', 'name',
                  'image', 'text', 'cooking_time']

    def ingredientrecipe_bulk_create(self, recipe, ingredients):
        ingredients_in_recipe = [
            IngredientRecipe(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredients_in_recipe)

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        validated_data['author'] = author
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipes')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.ingredientrecipe_bulk_create(recipe=recipe,
                                          ingredients=ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        IngredientRecipe.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipes')
        instance.tags.set(tags)
        self.ingredientrecipe_bulk_create(recipe=instance,
                                          ingredients=ingredients)
        instance.refresh_from_db()
        return super().update(instance=instance, validated_data=validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = RecipeSerializer(
            instance,
            context=context
        )
        return serializer.data

    def validate(self, data):
        if len(data) < 1:
            raise serializers.ValidationError(
                'Не переданы ингредиенты.'
            )
        if 'ingredientrecipe' in data:
            ingredients = data.get('ingredientrecipe')
            uniq_ingredients = set()
            for ingredient in ingredients:
                amount = ingredient['amount']
                if amount <= 0:
                    raise serializers.ValidationError(
                        'Минимальное количество ингредиента: 1'
                    )
                uniq_ingredients.add(id)

            if len(uniq_ingredients) != len(ingredients):
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными.'
                )
        return data


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image',
                  'cooking_time']


class SubscriptionSerializer(CustomUserSerializer):
    recipes = RecipeShortSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count']

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['user', 'author']
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author')
            ),
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = SubscriptionSerializer(
            instance.author,
            context=context
        )
        return serializer.data

    def validate_author(self, value):
        request = self.context['request']
        user = request.user
        if user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user', 'recipe']
        validators = (
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            ),
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = RecipeShortSerializer(
            instance.recipe,
            context=context
        )
        return serializer.data


class ShoppingCartSerializer(FavoriteSerializer):
    class Meta:
        model = ShoppingCart
        fields = ['user', 'recipe']
        validators = (
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe')
            ),
        )
