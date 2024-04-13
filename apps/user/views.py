from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .models import CustomUser,AdminContact
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404
from .serializers import *
from .permissions import IsAdminUserOrIsManagerCanDeleteComments
from rest_framework import permissions
from .models import CustomUser
from .permissions import IsAdminUser, IsClientUser, IsManagerUser, IsClientCanViewProfiles


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.create_user(**serializer.validated_data)
        first_client = CustomUser.objects.filter(role_type='client').first()
        first_manager = CustomUser.objects.filter(role_type='manager').first()

        if first_client:
            user.client_can_edit_comments = first_client.client_can_edit_comments
            user.client_can_get_reports = first_client.client_can_get_reports
            user.client_can_view_logs = first_client.client_can_view_logs
            user.client_can_add_files = first_client.client_can_add_files
            user.client_can_add_checklist = first_client.client_can_add_checklist
            user.client_can_view_profiles = first_client.client_can_view_profiles
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
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = PageNumberPagination





class DetailUserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'
    # permission_classes = [IsAdminUser, IsClientCanViewProfiles]


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






class AdminContactDetailView(generics.RetrieveUpdateAPIView):
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

    def put(self, request, *args, **kwargs):
        users_data = request.data.get('users_data', [])
        # print(f'Users data: {users_data}')
        for user_data in users_data:
            user_id = user_data.get('id')
            # print(f'User id: {user_id}')
            try:
                user_instance = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(f'Менеджер с id={user_id} не найден', status=404)

            update_data = {
                'manager_can_delete_comments_extra': user_data.get('manager_can_delete_comments_extra',
                                                                   user_instance.manager_can_delete_comments_extra),
                'manager_can_get_reports_extra': user_data.get('manager_can_get_reports_extra',
                                                               user_instance.manager_can_get_reports_extra),
                'manager_can_view_profiles_extra': user_data.get('manager_can_view_profiles_extra',
                                                                 user_instance.manager_can_view_profiles_extra),
                'manager_can_delete_application_extra': user_data.get('manager_can_delete_application_extra',
                                                                      user_instance.manager_can_delete_application_extra),
                'manager_can_create_and_edit_company_extra': user_data.get('manager_can_create_and_edit_company_extra',
                                                                      user_instance.manager_can_create_and_edit_company_extra),
                'manager_can_create_and_edit_user_extra': user_data.get('manager_can_create_and_edit_user_extra',
                                                                      user_instance.manager_can_create_and_edit_user_extra),
                'manager_can_create_and_delete_job_title_extra': user_data.get('manager_can_create_and_delete_job_title_extra',
                                                                      user_instance.manager_can_create_and_delete_job_title_extra),
            }
            # print(f'Update data: {update_data}')

            serializer = self.get_serializer(user_instance, data=user_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
        client_can_view_profiles = request.data.get('client_can_view_profiles')

        self.queryset.update(
            client_can_edit_comments=bool(client_can_edit_comments),
            client_can_get_reports=bool(client_can_get_reports),
            client_can_view_logs=bool(client_can_view_logs),
            client_can_add_files=bool(client_can_add_files),
            client_can_add_checklist=bool(client_can_add_checklist),
            client_can_view_profiles=bool(client_can_view_profiles)
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
                "client_can_add_checklist": first_client.client_can_add_checklist,
                "client_can_view_profiles": first_client.client_can_view_profiles,
            }
        return Response(client_permissions)



class ClientPermissionsDetailAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='client')
    serializer_class = ClientPermissionsDetailSerializer

    def put(self, request, *args, **kwargs):
        users_data = request.data.get('users_data', [])
        # print(f'Users data: {users_data}')
        for user_data in users_data:
            user_id = user_data.get('id')
            # print(f'User id: {user_id}')
            try:
                user_instance = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(f'Клиент с id={user_id} не найден', status=404)

            update_data = {
                'client_can_add_checklist_extra': user_data.get('client_can_add_checklist_extra',
                                                                user_instance.client_can_add_checklist_extra),
                'client_can_view_logs_extra': user_data.get('client_can_view_logs_extra',
                                                            user_instance.client_can_view_logs_extra),
                'client_can_get_reports_extra': user_data.get('client_can_get_reports_extra',
                                                              user_instance.client_can_get_reports_extra),
                'client_can_add_files_extra': user_data.get('client_can_add_files_extra',
                                                            user_instance.client_can_add_files_extra),
                'client_can_view_profiles_extra': user_data.get('client_can_view_profiles_extra',
                                                                user_instance.client_can_view_profiles_extra),
                'client_can_edit_comments_extra': user_data.get('client_can_edit_comments_extra',
                                                                user_instance.client_can_edit_comments_extra),
                'client_can_create_application_extra': user_data.get('client_can_create_application_extra',
                                                                user_instance.client_can_create_application_extra),
                'client_can_edit_application_extra': user_data.get('client_can_edit_application_extra',
                                                                user_instance.client_can_edit_application_extra)
            }
            print(f'Update data: {update_data}')

            serializer = self.get_serializer(user_instance, data=update_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response('Права клиента успешно обновлены')

class UserPermissionsDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        user = self.get_object()
        if user.role_type == 'client':
            return ClientPermissionsDetailSerializer
        elif user.role_type == 'manager':
            return ManagerPermissionsDetailSerializer


# class ManagerPermissionsDetailAPIView(generics.ListAPIView):
#     queryset = CustomUser.objects.filter(role_type='manager')
#     serializer_class = ManagerPermissionsSerializer
#
#     def put(self, request, *args, **kwargs):
#         users_data = request.data
#         for user_data in users_data:
#             user_id = user_data.get('id')
#             try:
#                 user_instance = CustomUser.objects.get(id=user_id)
#             except CustomUser.DoesNotExist:
#                 return Response(f'Пользователь с id={user_id} не найден', status=404)
#
#             serializer = self.get_serializer(user_instance, data=user_data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#
#         return Response('Права пользователей обновлены')



class AdminContactListView(generics.ListAPIView):
    serializer_class = AdminContactSerializer


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


class AdminResetPasswordView(generics.UpdateAPIView):
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

