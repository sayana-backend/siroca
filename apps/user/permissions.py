from rest_framework import permissions


'''Admin's permissions'''

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


'''Client's permissions'''


class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client


class IsClientCanGetReports(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.client_can_get_reports_extra:
            return True
        if not request.user.client_can_get_reports_extra:
            return False
        elif request.user.client_can_get_reports_extra is None:
            return request.user.client_can_get_reports
        return request.user.is_authenticated and request.user.client_can_get_reports


class IsClientCanEditComments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.client_can_edit_comments_extra:
            return True
        if not request.user.client_can_edit_comments_extra:
            return False
        elif request.user.client_can_edit_comments_extra is None:
            return request.user.client_can_edit_comments
        return request.user.is_authenticated and request.user.client_can_edit_comments


class IsClientCanViewProfiles(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.client_can_view_profiles_extra:
            return True
        if not request.user.client_can_view_profiles_extra:
            return False
        if request.user.client_can_view_profiles_extra is None:
            return request.user.client_can_view_profiles
        return request.user.is_authenticated and request.user.client_can_view_profiles


class IsClientCanAddFiles(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.client_can_add_files_extra:
            return True
        if not request.user.client_can_add_files_extra:
            return False
        elif request.user.client_can_add_files_extra is None:
            return request.user.client_can_add_files
        return request.user.is_authenticated and request.user.client_can_add_files


class IsClientCanViewLogs(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.client_can_view_logs_extra:
            return True
        if not request.user.client_can_view_logs_extra:
            return False
        elif request.user.client_can_view_logs_extra is None:
            return request.user.client_can_view_logs
        return request.user.is_authenticated and request.user.client_can_view_logs



class IsClientCanAddChecklist(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.client_can_add_checklist_extra:
            return True
        if not request.user.client_can_add_checklist_extra:
            return False
        elif request.user.client_can_add_checklist_extra is None:
            return request.user.client_can_add_checklist
        return request.user.is_authenticated and request.user.client_can_add_checklist

class IsClientCanCreateApplication(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role_type == 'client':
            return request.user.main_company == request.data.get('company')
        return request.user.client_can_create_application_extra

class IsClientCanEditApplication(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role_type == 'client':
            return obj.company == request.user.main_company
        return request.user.client_can_edit_application_extra


'''''Manager's permissions'''''


class IsManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class IsAdminUserOrIsManagerCanDeleteComments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.manager_can_delete_comments_extra:
            return True
        return request.user.is_authenticated and request.user.manager_can_delete_comments


class IsManagerCanGetReports(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.manager_can_get_reports_extra:
            return True
        if not request.user.manager_can_get_reports_extra:
            return False
        elif request.user.manager_can_get_reports_extra is None:
            return request.user.manager_can_get_reports
        return request.user.is_authenticated and request.user.manager_can_get_reports


class IsManagerCanDeleteApplication(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.manager_can_delete_application_extra:
            return True
        if not request.user.manager_can_delete_application_extra:
            return False
        elif request.user.manager_can_delete_application_extra is None:
            return request.user.manager_can_delete_application
        return request.user.is_authenticated and request.user.manager_can_delete_application


class IsManagerCanViewProfiles(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.manager_can_view_profiles_extra:
            return True
        if not request.user.manager_can_view_profiles_extra:
            return False
        elif request.user.manager_can_view_profiles_extra is None:
            return request.user.manager_can_view_profiles
        return request.user.is_authenticated and request.user.manager_can_view_profiles


class IsManagerCanCreateAndEditCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.manager_can_create_and_edit_company_extra

class IsManagerCanCreateAndEditUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.manager_can_create_and_edit_user_extra

class IsManagerCanCreateAndDeleteJobTitle(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.manager_can_create_and_delete_job_title_extra
