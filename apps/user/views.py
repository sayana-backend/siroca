from ..application.views import CustomPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .permissions import *
from rest_framework import permissions, filters
from .models import CustomUser
from .permissions import IsAdminUser, IsClientUser, IsManagerUser


class CreateUserView(generics.CreateAPIView):
    '''Create user'''
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileRegisterSerializer
    permission_classes = [IsManagerCanCreateAndEditUserOrIsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.create_user(**serializer.validated_data)

        '''Set general permissions to new user'''
        first_client = CustomUser.objects.filter(role_type='client').first()
        first_manager = CustomUser.objects.filter(role_type='manager').first()

        if first_client:
            user.client_can_edit_comments = first_client.client_can_edit_comments
            user.client_can_get_reports = first_client.client_can_get_reports
            user.client_can_view_logs = first_client.client_can_view_logs
            user.client_can_add_files = first_client.client_can_add_files
            user.client_can_add_checklist = first_client.client_can_add_checklist
            user.save()

        elif first_manager:
            user.manager_can_delete_comments = first_manager.manager_can_delete_comments
            user.manager_can_get_reports = first_manager.manager_can_get_reports
            user.manager_can_view_profiles = first_manager.manager_can_view_profiles
            user.manager_can_delete_application = first_manager.manager_can_delete_application
            user.save()
        else:
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListUserProfileView(generics.ListAPIView):
    '''list users'''
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = CustomPagination
    permission_classes = [IsManagerCanCreateAndEditUserOrIsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'surname', 'main_company__name']


class DetailUserProfileView(generics.RetrieveUpdateDestroyAPIView): #разве не надо разделить просмтр и редактирование на две отдельные апишки
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsManagerCanViewProfilesOrIsAdminUser]
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
                'id': user.id,
                'role_type': user.role_type,
                'name': user.first_name,
                'refreshToken': str(refresh),
                'access': str(access_token),
                'refresh_lifetime_days': refresh.lifetime.days,
                'access_lifetime_days': access_token.lifetime.days
            })
        else:
            return Response({'detail': 'Ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)


class AdminContactDetailView(generics.RetrieveUpdateAPIView): # пересмотреть кто это писал вообще
    '''Редактирование контактов админа в профиле админа'''
    serializer_class = AdminContactSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdminContact.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()

        if obj is None:
            return Response({'detail': 'Ошибка аутентификации'}, status=status.HTTP_404_NOT_FOUND)
        return obj


class AdminContactListView(generics.ListAPIView): # что с кверисетом
    '''Контакты админа при авторизации'''
    serializer_class = AdminContactSerializer

    def get_queryset(self):
        return AdminContact.objects.all()


class ChangePasswordView(generics.UpdateAPIView):
    '''смена пароля в профиле у каждого пользователя'''
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


class AdminResetPasswordView(generics.UpdateAPIView):
    '''Сброс пароля админом в случае если пароль забыли'''
    queryset = CustomUser.objects.all()
    serializer_class = AdminResetPasswordSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({'detail': 'Новый пароль и его подтверждение не совпадают.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Пароль пользователя успешно сброшен.', 'new_password': new_password}, status=status.HTTP_200_OK)

'''Permissions'''
class ManagerPermissionsGeneralView(generics.UpdateAPIView, generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='manager')
    serializer_class = ManagerPermissionsGeneralSerializer
    # permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        managers = CustomUser.objects.filter(role_type='manager')
        manager_permissions = {}
        if managers.exists():
            first_manager = managers.first()
            manager_permissions = {
                "manager_can_delete_comments": first_manager.manager_can_delete_comments,
                "manager_can_get_reports": first_manager.manager_can_get_reports,
                "manager_can_view_profiles": first_manager.manager_can_view_profiles,
                "manager_can_delete_application": first_manager.manager_can_delete_application
            }
        return Response(manager_permissions)

    def update(self, request, *args, **kwargs):
        manager_can_delete_comments = request.data.get('manager_can_delete_comments')
        manager_can_get_reports = request.data.get('manager_can_get_reports')
        manager_can_view_profiles = request.data.get('manager_can_view_profiles')
        manager_can_delete_application = request.data.get('manager_can_delete_application')

        self.queryset.update(
            manager_can_delete_comments=bool(manager_can_delete_comments),
            manager_can_get_reports=bool(manager_can_get_reports),
            manager_can_view_profiles=bool(manager_can_view_profiles),
            manager_can_delete_application=bool(manager_can_delete_application)
        )
        return Response("Права менеджера обновлены", status=status.HTTP_200_OK)


class ManagerPermissionsDetailAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='manager')
    serializer_class = ManagerPermissionsDetailSerializer
    # permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        users_data = request.data.get('users_data', [])
        for user_data in users_data:
            user_id = user_data.get('id')
            try:
                user_instance = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(f'Менеджер с id={user_id} не найден', status=404)
            for key, value in user_data.items():
                setattr(user_instance, key, value)
            user_instance.save()
        return Response('Права менеджера успешно обновлены')


class ClientPermissionsGeneralView(generics.UpdateAPIView, generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='client')
    serializer_class = ClientPermissionsGeneralSerializer
    # permission_classes = [IsAdminUser]


    def update(self, request, *args, **kwargs):
        client_can_edit_comments = request.data.get('client_can_edit_comments')
        client_can_get_reports = request.data.get('client_can_get_reports')
        client_can_view_logs = request.data.get('client_can_view_logs')
        client_can_add_files = request.data.get('client_can_add_files')
        client_can_add_checklist = request.data.get('client_can_add_checklist')

        self.queryset.update(
            client_can_edit_comments=bool(client_can_edit_comments),
            client_can_get_reports=bool(client_can_get_reports),
            client_can_view_logs=bool(client_can_view_logs),
            client_can_add_files=bool(client_can_add_files),
            client_can_add_checklist=bool(client_can_add_checklist)
        )
        return Response('Права клиента обновлены')

    # @staticmethod
    def get(self, request, *args, **kwargs):
        clients = CustomUser.objects.filter(role_type='client')
        client_permissions = {}
        if clients.exists():
            first_client = clients.first()
            print(f'first_client: {first_client}')
            client_permissions = {
                "client_can_edit_comments": first_client.client_can_edit_comments,
                "client_can_get_reports": first_client.client_can_get_reports,
                "client_can_view_logs": first_client.client_can_view_logs,
                "client_can_add_files": first_client.client_can_add_files,
                "client_can_add_checklist": first_client.client_can_add_checklist
            }
        return Response(client_permissions)


class ClientPermissionsDetailAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='client')
    serializer_class = ClientPermissionsDetailSerializer
    # permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        users_data = request.data.get('users_data', [])
        for user_data in users_data:
            user_id = user_data.get('id')
            try:
                user_instance = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(f'Клиент с id={user_id} не найден', status=404)
            for key, value in user_data.items():
                setattr(user_instance, key, value)
            user_instance.save()
        return Response('Права клиента успешно обновлены')


class UserPermissionsDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'id'
    # permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        user = self.get_object()
        if user.role_type == 'client':
            return ClientPermissionsDetailSerializer
        elif user.role_type == 'manager':
            return ManagerPermissionsDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
