from django.urls import include, path
from rest_framework import routers

from api.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                       ShoppingCartViewSet, SubscribeViewSet,
                       SubscriptionViewSet, TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'recipes/(?P<id>\d+)/favorite',
                FavoriteViewSet,
                basename='favorite'
                )
router.register(r'recipes/(?P<id>\d+)/shopping_cart',
                ShoppingCartViewSet,
                basename='shopping_cart'
                )
router.register(r'users/subscriptions', SubscriptionViewSet,
                basename='subscription')
router.register(r'users/(?P<id>\d+)/subscribe',
                SubscribeViewSet,
                basename='subscribe'
                )

urlpatterns = router.urls
urlpatterns += [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
