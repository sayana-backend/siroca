from .serializers import UserProfileSerializer, UserAuthSerializer,AdminContactSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework import permissions
from .models import CustomUser,AdminContact
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import check_password


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer




class ListUserProfileView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            for user in queryset:
                user.password = self.decrypt_password(user.password)
        return queryset

    def decrypt_password(self, password):
        if self.request.user.is_superuser:
            return password
        else:
            return "*****"  



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
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
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




class AdminContactDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdminContact.objects.filter(admin=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()

        if obj is None:
            raise Http404("Контакт не существует.")
        return obj
