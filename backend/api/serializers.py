from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer

from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
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
        # if request is None or
        if request.user.is_anonymous:
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


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True, read_only=True, source='ingredient_recipes'
    )
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time']


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
        recipes_count = obj.recipes.count()
        return recipes_count





#    amount = serializers.ModelField(model_field=Ingredient._meta.get_field('amount'))
# amount = serializers.ModelField(model_field=Recipe.ingridients._meta.get_field('amount'))

# class AmountIngredientField(serializers.RelatedField):
#    def to_representation(self, value):
#        amount = 



