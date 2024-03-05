from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsManagerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

class IsClientUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client

class IsManagerCanEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.manager_can_edit

class IsManagerCanGetReports(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.manager_can_get_reports

class IsClientCanGetReports(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.client_can_get_reports


class IsClientCanPutComments(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.client_can_put_comments

class IsClientCanDeleteComments(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.client_can_delete_comments

class IsClientCanViewLogs(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.client_can_view_logs

class IsClientCanAddChecklist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.client_can_add_checklist
















# from rest_framework import generics
# from rest_framework import permissions
# from .models import CustomUser, ClientPermissions, ManagerPermissions
# from .serializers import ClientPermissionsSerializer, ManagerPermissionsSerializer
# from rest_framework.permissions import IsAuthenticated
#
# class ClientPermissionsListCreate(generics.ListCreateAPIView):
#     queryset = ClientPermissions.objects.all()
#     serializer_class = ClientPermissionsSerializer
#     permission_classes = [permissions.IsAdminUser]
#
#     def perform_create(self, serializer):
#         serializer.save()
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if self.request.user.is_superuser:
#             return queryset
#         else:
#             role_type = 'сlient'
#             return queryset.filter(user__role_type=role_type)
#
#
# class ClientPermissionsDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ClientPermissions.objects.all()
#     serializer_class = ClientPermissionsSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_update(self, serializer):
#         serializer.save()
#
#     def perform_destroy(self, instance):
#         instance.delete()
#
#
# class ManagerPermissionsListCreate(generics.ListCreateAPIView):
#     queryset = ManagerPermissions.objects.all()
#     serializer_class = ManagerPermissionsSerializer
#     permission_classes = [permissions.IsAdminUser]
#
#     # def perform_create(self, serializer):
#     #     serializer.save()
#
#     # def get_queryset(self):
#     #     queryset = super().get_queryset()
#     #     if self.request.user.is_superuser:
#     #         return queryset
#     #     else:
#     #         role_type = 'manager'
#     #         return queryset.filter(user__role_type=role_type)
#
#
# class ManagePermissionsDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ManagerPermissions.objects.all()
#     serializer_class = ManagerPermissionsSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_update(self, serializer):
#         serializer.save()
#
#     def perform_destroy(self, instance):
#         instance.delete()
