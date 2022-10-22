from rest_framework import routers
from django.urls import include, path

from api.views import (CustomUserViewSet, TagViewSet, IngredientViewSet,
                       RecipeViewSet)


app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'users', CustomUserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredints', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)


urlpatterns = router.urls
urlpatterns += [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
