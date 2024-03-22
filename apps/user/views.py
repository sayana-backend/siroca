from .serializers import UserProfileSerializer, UserAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .serializers import *
from .permissions import IsManagerCanEdit
from rest_framework import permissions
from .models import CustomUser
from .permissions import IsAdminUser, IsClientUser, IsManagerUser




class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAdminUser]


class ListUserProfileView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]


class DetailUserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]


class UserLoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserAuthSerializer
    # permission_classes = [IsAdminUser]

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



class ManagerPermissionsView(generics.UpdateAPIView, generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='manager')
    serializer_class = ManagerPermissionsSerializer
    # permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        manager_can_edit = request.data.get('manager_can_edit')
        manager_can_get_reports = request.data.get('manager_can_get_reports')

        self.queryset.update(
            manager_can_edit=bool(manager_can_edit),
            manager_can_get_reports=bool(manager_can_get_reports)
        )


    def get(self, request, *args, **kwargs):
        managers = CustomUser.objects.filter(role_type='manager')
        manager_permissions = {}
        if managers.exists():
            first_manager = managers.first()
            print(f'first_manager: {first_manager}')
            manager_permissions = {
                "manager_can_edit": first_manager.manager_can_edit,
                "manager_can_get_reports": first_manager.manager_can_get_reports
            }
        return Response(manager_permissions)


class ClientPermissionsView(generics.UpdateAPIView, generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='client')
    serializer_class = ClientPermissionsSerializer
    # permission_classes = [IsAdminUser]


    def update(self, request, *args, **kwargs):
        client_can_put_comments = request.data.get('client_can_put_comments')
        client_can_get_reports = request.data.get('client_can_get_reports')
        client_can_view_logs = request.data.get('client_can_view_logs')
        client_can_delete_comments = request.data.get('client_can_delete_comments')
        client_can_add_checklist = request.data.get('client_can_add_checklist')

        self.queryset.update(
            client_can_put_comments=bool(client_can_put_comments),
            client_can_get_reports=bool(client_can_get_reports),
            client_can_view_logs=bool(client_can_view_logs),
            client_can_delete_comments=bool(client_can_delete_comments),
            client_can_add_checklist=bool(client_can_add_checklist)
        )
        return Response('Права клиента обновлены')

    def get(self, request, *args, **kwargs):
        clients = CustomUser.objects.filter(role_type='client')
        client_permissions = {}
        if clients.exists():
            first_client = clients.first()
            print(f'first_client: {first_client}')
            client_permissions = {
                "client_can_put_comments": first_client.client_can_put_comments,
                "client_can_get_reports": first_client.client_can_get_reports,
                "client_can_view_logs": first_client.client_can_view_logs,
                "client_can_delete_comments": first_client.client_can_delete_comments,
                "client_can_add_checklist": first_client.client_can_add_checklist
            }

        return Response(client_permissions)





