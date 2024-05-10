from ..application.views import CustomPagination
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import filters
from .serializers import *
from .permissions import *
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated


class ManagerPermissionsGeneralView(generics.UpdateAPIView, generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='manager')
    serializer_class = ManagerPermissionsGeneralSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        managers = CustomUser.objects.filter(role_type='manager')
        manager_permissions = {}
        if managers.exists():
            first_manager = managers.first()
            manager_permissions = {
                "manager_can_delete_comments": first_manager.manager_can_delete_comments,
                "manager_can_get_reports": first_manager.manager_can_get_reports,
                "manager_can_delete_application": first_manager.manager_can_delete_application
            }
        return Response(manager_permissions)

    def update(self, request, *args, **kwargs):
        manager_can_delete_comments = request.data.get('manager_can_delete_comments')
        manager_can_get_reports = request.data.get('manager_can_get_reports')
        manager_can_delete_application = request.data.get('manager_can_delete_application')

        self.queryset.update(
            manager_can_delete_comments=bool(manager_can_delete_comments),
            manager_can_get_reports=bool(manager_can_get_reports),
            manager_can_delete_application=bool(manager_can_delete_application)
        )
        return Response("Права менеджера обновлены", status=status.HTTP_200_OK)


class ManagerPermissionsDetailAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role_type='manager')
    serializer_class = ManagerPermissionsDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'surname', 'username']
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

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
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'surname', 'username']
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAuthenticated]

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