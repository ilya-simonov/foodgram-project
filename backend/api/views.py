from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (CustomUserSerializer, TagSerializer,
                             IngredientSerializer, RecipeSerializer)
from recipes.models import Ingredient, Tag, Recipe
from users.models import User


class UserViewSet2(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    # @action(detail=False, methods=['get'], url_path='me')
    # permission_classes=[IsAuthenticated])
    # def get_object_me(self, request):
        # user_me = get_object_or_404(User, username=request.user.username)
        # serializer = UserSerializer(user_me)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserViewSet(UserViewSet):
#   serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class SubscriptionViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        

