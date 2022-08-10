from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], url_path='me')
    def get_object_me(self, request):
        user_me = get_object_or_404(User, username=request.user.username)
        # return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user_me)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND, detail='Страница не найдена.')
