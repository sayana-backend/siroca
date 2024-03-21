from .serializers import *
from .permissions import IsManagerCanEdit
from .serializers import UserProfileSerializer, UserAuthSerializer,AdminContactSerializer,ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .models import CustomUser,AdminContact
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404

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
            return Response({'detail': 'Ошибка аутентификации'}, status=status.HTTP_404_NOT_FOUND)
        return obj


class ManagerPermissionsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(role_type='manager')
    serializer_class = ManagerPermissionsSerializer
    permission_classes = [IsManagerCanEdit]

    def update(self, request, *args, **kwargs):
        manager_can_edit = request.data.get('manager_can_edit')
        manager_can_get_reports = request.data.get('manager_can_get_reports')
        if manager_can_edit:
            self.queryset.update(manager_can_edit=True)
        if manager_can_get_reports:
            self.queryset.update(manager_can_get_reports=True)
        return Response('Права менеджера предоставлены')

class ClientPermissionsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(role_type='client')
    serializer_class = ClientPermissionsSerializer
    # lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        client_can_put_comments = request.data.get('client_can_put_comments')
        client_can_get_reports = request.data.get('client_can_get_reports')
        client_can_view_logs = request.data.get('client_can_view_logs')
        client_can_delete_comments = request.data.get('client_can_delete_comments')
        client_can_add_checklist = request.data.get('client_can_add_checklist')
        if client_can_put_comments:
            self.queryset.update(client_can_put_comments=True)
        if client_can_get_reports:
            self.queryset.update(client_can_get_reports=True)
        if client_can_view_logs:
            self.queryset.update(client_can_view_logs=True)
        if client_can_delete_comments:
            self.queryset.update(client_can_delete_comments=True)
        if client_can_add_checklist:
            self.queryset.update(client_can_add_checklist=True)
        return Response('Права клиента предоставлены')




class AdminContactListView(generics.ListAPIView):
    serializer_class = AdminContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdminContact.objects.all()



class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password1 = serializer.validated_data.get('new_password1')
        new_password2 = serializer.validated_data.get('new_password2')

        if not user.check_password(old_password):
            return Response({'detail': 'Старый пароль неверен'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password1 != new_password2:
            return Response({'detail': 'Новые пароли не совпадают'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password1)
        user.save()

        return Response({'detail': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

