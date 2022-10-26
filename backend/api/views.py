from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (CustomUserSerializer, TagSerializer,
                             IngredientSerializer, RecipeSerializer,
                             SubscriptionSerializer, SubscribeSerializer)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from recipes.models import Ingredient, Tag, Recipe, Follow
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
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class SubscriptionViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        request = self.request
        queryset = User.objects.filter(following__user=request.user)
        return queryset


class SubscribeViewSet2(viewsets.ViewSet):
    @action(detail=True, methods=['post'], permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow_obj = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response('Нельзя подписаться на себя!',
                                status=status.HTTP_400_BAD_REQUEST)
            if follow_obj.exists():
                return Response('Вы уже подписаны на данного пользователя!',
                                status=status.HTTP_400_BAD_REQUEST)
            follow_obj = Follow.objects.create(user=user, author=author)
            follow_obj.save()
            # serializer = SubscriptionSerializer(author)
            # serializer.data, 
            return Response(status=status.HTTP_201_CREATED)


class SubscribeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, id):
        author = get_object_or_404(User, id=id)
        user = self.request.user
        data = {'author': author.id, 'user': user.id}
        serializer = SubscribeSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        user = request.user
        subscription = get_object_or_404(
            Follow, user=user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
