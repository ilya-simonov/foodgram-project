from rest_framework import routers
from django.urls import include, path

from api.views import (CustomUserViewSet, TagViewSet, IngredientViewSet,
                       RecipeViewSet, SubscriptionViewSet, SubscribeViewSet)


app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'users', CustomUserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredints', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'users/subscriptions', SubscriptionViewSet,
                basename='subscription')
router.register(r'users/(?P<id>\d+)/subscribe',
                SubscribeViewSet,
                basename='subscribe'
                )

# router.register(r'users', SubscribeViewSet,
#                basename='subscribe')
                # r'users/(?P<id>\d+)

urlpatterns = router.urls
urlpatterns += [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'subscribe'}),
         name='subscribe')
]
