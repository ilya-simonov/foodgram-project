from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer
from django.db import transaction

from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (Ingredient, Tag, Recipe, IngredientRecipe, Follow,
                            Favorite, ShoppingCart)
from users.models import User
from djoser import utils
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed']
        # read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name']


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

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        validated_data['author'] = author
        # print('validated_data: ', validated_data)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipes')
        # print('INGREFIENTS: ', ingredients)
        recipe = Recipe.objects.create(**validated_data)
#        self.ingredient_in_recipe_bulk_create(recipe=recipe,
#                                              ingredients=ingredients)
        recipe.tags.set(tags)
        ingredients_in_recipe = [
            IngredientRecipe(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredients_in_recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        IngredientRecipe.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipes')
        instance.tags.set(tags)
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        ingredients_in_recipe = [
            IngredientRecipe(
                ingredient=ingredient['id'],
                recipe=instance,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredients_in_recipe)
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


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image',
                  'cooking_time']


class SubscriptionSerializer(CustomUserSerializer):
    recipes = RecipeShortSerializer(many=True, read_only=True)
    # source='recipes')
    recipes_count = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count']

    def get_recipes_count(self, obj):

        recipes_count = obj.recipes.count()
        return recipes_count


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





#    amount = serializers.ModelField(model_field=Ingredient._meta.get_field('amount'))
# amount = serializers.ModelField(model_field=Recipe.ingridients._meta.get_field('amount'))

# class AmountIngredientField(serializers.RelatedField):
#    def to_representation(self, value):
#        amount = 



