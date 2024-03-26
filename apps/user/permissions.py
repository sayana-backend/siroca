from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser




#########  Client's permissions  #########
class IsClientUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client


class IsClientCanGetReports(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can get reports:", request.user.client_can_get_reports)
        return request.user.is_authenticated and request.user.client_can_get_reports


class IsClientCanEditComments(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can edit comments:", request.user.client_can_edit_comments)
        return request.user.is_authenticated and request.user.client_can_edit_comments

class IsClientCanViewProfiles(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can view profiles:", request.user.client_can_view_profiles)
        return request.user.is_authenticated and request.user.client_can_view_profiles


class IsClientCanAddFiles(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can add files:", request.user.client_can_add_files)
        return request.user.is_authenticated and request.user.client_can_add_files

class IsClientCanViewLogs(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can view logs:", request.user.client_can_view_logs)
        return request.user.is_authenticated and request.user.client_can_view_logs

class IsClientCanAddChecklist(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can add checklist:", request.user.client_can_add_checklist)
        return request.user.is_authenticated and request.user.client_can_add_checklist



#########  Manager's permissions  #########
class IsManagerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class IsManagerCanDeleteComments(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Manager can edit:", request.user.manager_can_delete_comments)
        return request.user.is_authenticated and request.user.manager_can_delete_comments

class IsManagerCanGetReports(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Manager can get reports:", request.user.manager_can_get_reports)
        return request.user.is_authenticated and request.user.manager_can_get_reports


class IsManagerCanDeleteApplication(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Manager can delete application:", request.user.manager_can_delete_application)
        return request.user.is_authenticated and request.user.manager_can_delete_application


class IsManagerCanViewProfiles(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Manager can view profiles:", request.user.manager_can_view_profiles)
        return request.user.is_authenticated and request.user.manager_can_view_profiles