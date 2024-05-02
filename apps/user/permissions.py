from rest_framework import permissions


'''Admin's permissions'''

'''ONLY FOR SUPERUSER'S PERMISSIONS'''
class IsAdminUserAndManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_manager


'''SUPERUSER AND MANAGER'''        
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
        


'''Client's permissions'''


class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client


# class IsClientCanGetReportsAndIsAdminUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.user.client_can_get_reports_extra:
#             return request.user.client_can_get_reports_extra
#         else:
#             return request.user.client_can_get_reports


'''CLIENT CAN CREATE COMMENTS'''
class IsClientCanCreateCommentsOrIsAdminAndManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_edit_comments_extra:
            return request.user.client_can_edit_comments_extra
        else:
            return request.user.client_can_edit_comments


'''CLIENT CAN ADD FILES'''
class IsClientCanAddFilesOrIsAdminAndManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_add_files_extra:
            return request.user.client_can_add_files_extra
        else:
            return request.user.client_can_add_files


'''CLIENT CAN VIEW APPLICATION LOGS'''
class IsClientCanViewLogsOrIsAdminAndManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_view_logs_extra:
            return request.user.client_can_view_logs_extra
        else:
            return request.user.client_can_view_logs


'''CLIENT CAN ADD CHECKLISTS'''
class IsClientCanAddChecklistOrIsAdminAndManagerUser(permissions.BasePermission):   ########### WARNING!!!!!!!!!!!!! ##########
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_add_checklist_extra:
            return request.user.client_can_add_checklist_extra
        else:
            return request.user.client_can_add_checklist

'''CLIENT CAN CREATE APPLICATIONS'''
class IsClientCanCreateApplicationOrIsAdminAndManagerUser(permissions.BasePermission):    ### перепроверить ###
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_create_application_extra:
            if request.user.main_company.name == request.data.get('company'):
                return request.user.client_can_create_application_extra
        else:
            return request.user.client_can_create_application_extra
                

'''CLIENT CAN EDIT APPLICATIONS'''
class IsClientCanEditApplicationAndIsManagerUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_edit_application_extra:
            if obj.company == request.user.main_company.name:
                return request.user.client_can_edit_application_extra
        else:
            return request.user.client_can_edit_application_extra


'''''Manager's permissions'''''


class IsManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

'''MANAGER CAN DELETE COMMENTS AND CLIENT CAN EDIT COMMENTS'''
class IsAdminOrManagerOrClientUsersCanEditComments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user.role_type == 'manager':
            if request.user.manager_can_delete_comments_extra:
                return request.user.manager_can_delete_comments_extra
            else:
                return request.user.manager_can_delete_comments
        elif request.user.is_authenticated and request.user.role_type == 'client':
            if request.user.client_can_edit_comments_extra:
                return request.user.client_can_edit_comments_extra
            else:
                return request.user.client_can_edit_comments

'''MANAGER AND CLIENT CAN GET REPORTS'''
class IsManagerAndClientCanGetReportsOrIsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user.role_type == 'manager':
            if request.user.manager_can_get_reports_extra:
                return request.user.manager_can_get_reports_extra
            else:
                return request.user.manager_can_get_reports
        elif request.user.is_authenticated and request.user.role_type == 'client':
            if request.user.client_can_get_reports_extra:
                return request.user.client_can_get_reports_extra
            else:
                return request.user.client_can_get_reports

'''MANAGER CAN DELETE APPLICATIONS'''
class IsManagerCanDeleteApplicationOrIsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.manager_can_delete_applications_extra:
            return request.user.manager_can_delete_applications_extra
        else:
            return request.user.manager_can_delete_applications

# '''MANAGER CAN VIEW USERS' PROFILES'''
# class IsManagerCanViewProfilesOrIsAdminUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_superuser:
#             return True
#         if request.user.manager_can_view_profiles_extra:
#             return request.user.manager_can_view_profiles_extra
#         else:
#             return request.user.manager_can_view_profiles

'''MANAGER CAN CREATE AND EDIT COMPANY'''
class IsManagerCanCreateAndEditCompanyOrIsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.manager_can_create_and_edit_company

'''MANAGER CAN CREATE USER'''
class IsManagerCanCreateAndEditUserOrIsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.manager_can_create_and_edit_user_extra

'''MANAGER CAN CREATE AND DELETE JOB TITLES'''
class IsManagerCanCreateAndDeleteJobTitleOrIsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.manager_can_create_and_delete_job_title_extra
