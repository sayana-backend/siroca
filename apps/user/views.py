from .serializers import UserProfileSerializer, UserAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework import permissions
from .models import CustomUser


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer


class ListUserProfileView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer


class DetailUserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'

class UserLoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = CustomUser.objects.get(username=username)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            print(request.user)

            return Response({
                'detail': 'Вы успешно вошли',
                'name': user.first_name,
                'refresh-token': str(refresh),
                'access': str(access_token),
                'refresh_lifetime_days': refresh.lifetime.days,
                'access_lifetime_days': access_token.lifetime.days
            })
        else:
            return Response({'detail': 'Ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)

#     template_name = ''
#     success_url = reverse_lazy('')
#     permission_required = 'user.add_userprofile'


