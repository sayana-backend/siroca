from rest_framework import generics, status
from .models import CustomUser
from .serializers import UserProfileRegisterSerializer, AllUserSerializers, UserAuthSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileRegisterSerializer


class ListUserProfileView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileRegisterSerializer


class AllUsersView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AllUserSerializers
    lookup_field = 'id'


class UserLoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user=user)
        return Response({
            'detail': 'Вы успешно вошли',
            'name': user.name,
            'refresh-token': str(refresh),
            'access': str(refresh.access_token),
            'refresh_lifetime_days': refresh.lifetime.days,
            'access_lifetime_days': refresh.access_token.lifetime.days
        })