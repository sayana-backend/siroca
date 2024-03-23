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


class IsClientCanPutComments(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can put comments:", request.user.client_can_put_comments)
        return request.user.is_authenticated and request.user.client_can_put_comments

class IsClientCanDeleteComments(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Client can delete comments:", request.user.client_can_delete_comments)
        return request.user.is_authenticated and request.user.client_can_delete_comments

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


class IsManagerCanEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Manager can edit:", request.user.manager_can_edit)
        return request.user.is_authenticated and request.user.manager_can_edit

class IsManagerCanGetReports(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Manager can get reports:", request.user.manager_can_get_reports)
        return request.user.is_authenticated and request.user.manager_can_get_reports




