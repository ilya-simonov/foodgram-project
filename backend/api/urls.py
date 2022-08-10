# from django.urls import path
from rest_framework import routers

from api.views import UserViewSet


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls
