from rest_framework import routers
from django.urls import include, path

from api.views import (TagViewSet, IngredientViewSet,
                       RecipeViewSet, SubscriptionViewSet, SubscribeViewSet,
                       FavoriteViewSet, ShoppingCartViewSet)


app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'users', CustomUserViewSet)
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
