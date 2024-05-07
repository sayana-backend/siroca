from rest_framework import permissions
from django.db import models


class UsersPermissions(models.Model):
    '''
    Этот класс используется как родительский для класса Пользователя.
    Поля этой модели определяют разрешения для пользователей.
    Для каждого поля предусмотрены два уровня прав: общие права и расширенные права.

    Общие права предоставляются по умолчанию каждому пользователю.

    Расширенные права:
    - Предоставляют возможность установить определенные разрешения для отдельных пользователей.
    - При установке прав пользователю, сначала проверяются экстра поля(расширенные права)
    - Если в экстра поле установлено значение null, то для пользователя используются общие права.
    - Если установлено значение True или False, то право для соответствующего пользователя
    будет установлено соответственно этим значениям.
    '''
    manager_can_delete_comments = models.BooleanField(default=False, verbose_name='Удаление комментариев')
    manager_can_delete_comments_extra = models.BooleanField(null=True, verbose_name='Удаление комментариев')
    manager_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Менеджер)')
    manager_can_get_reports_extra = models.BooleanField(null=True, verbose_name='Отчет по заявкам(Менеджер)')
    manager_can_delete_application = models.BooleanField(default=False, verbose_name='Удаление заявки')
    manager_can_delete_application_extra = models.BooleanField(null=True, verbose_name='Удаление заявки')
    manager_can_create_and_edit_company_extra = models.BooleanField(null=True,
                                                                    verbose_name='Создание/Редактирование заявки')
    manager_can_create_and_edit_user_extra = models.BooleanField(null=True,
                                                                 verbose_name='Создание/Редактирование пользователя')
    manager_can_create_and_delete_job_title_extra = models.BooleanField(null=True,
                                                                        verbose_name='Просмотр списка по компаниям/пользователям/должностям')

    client_can_edit_comments = models.BooleanField(default=False, verbose_name='Добавление/удаление комментария')
    client_can_edit_comments_extra = models.BooleanField(null=True, verbose_name='Добавление/удаление комментария')
    client_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Клиент)')
    client_can_get_reports_extra = models.BooleanField(null=True, verbose_name='Отчет по заявкам(Клиент)')
    client_can_view_logs = models.BooleanField(default=False, verbose_name='Просмотр логов')
    client_can_view_logs_extra = models.BooleanField(null=True, verbose_name='Просмотр логов')
    client_can_add_checklist = models.BooleanField(default=False, verbose_name='Добавление чеклиста')
    client_can_add_checklist_extra = models.BooleanField(null=True, verbose_name='Добавление чеклиста')
    client_can_add_files = models.BooleanField(default=False, verbose_name='Добавление файла')
    client_can_add_files_extra = models.BooleanField(null=True, verbose_name='Добавление файла')
    client_can_create_application_extra = models.BooleanField(null=True, verbose_name='Создание заявки')
    client_can_edit_application_extra = models.BooleanField(null=True, verbose_name='Редактирование заявки')


'''Permissions'''


class IsAdminUser(permissions.BasePermission):
    '''
    ONLY SUPERUSER
    '''

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminUserAndManagerUser(permissions.BasePermission):
    '''
    SUPERUSER AND MANAGER
    '''

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_manager


'''Client's permissions'''


class IsClientUser(permissions.BasePermission):
    '''
    ONLY CLIENT
    '''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client


class IsClientCanCreateCommentsOrIsAdminAndManagerUser(permissions.BasePermission):
    '''
    CLIENT CAN CREATE COMMENTS
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_edit_comments_extra:
            return request.user.client_can_edit_comments_extra
        else:
            return request.user.client_can_edit_comments


class IsClientCanAddFilesOrIsAdminAndManagerUser(permissions.BasePermission):
    '''
    CLIENT CAN ADD FILES
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_add_files_extra:
            return request.user.client_can_add_files_extra
        else:
            return request.user.client_can_add_files


class IsClientCanViewLogsOrIsAdminAndManagerUser(permissions.BasePermission):
    '''
    CLIENT CAN VIEW APPLICATION LOGS
    '''

    def has_permission(self, request, view):
        print(request.user)
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_view_logs_extra:
            return request.user.client_can_view_logs_extra
        else:
            return request.user.client_can_view_logs


class IsClientCanAddChecklistOrIsAdminAndManagerUser(permissions.BasePermission):
    '''
    CLIENT CAN ADD CHECKLISTS
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_add_checklist_extra:
            return request.user.client_can_add_checklist_extra
        else:
            return request.user.client_can_add_checklist


class IsClientCanCreateApplicationOrIsAdminAndManagerUser(permissions.BasePermission):
    '''
    CLIENT CAN CREATE APPLICATIONS
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_create_application_extra:
            if request.user.main_company.name == request.data.get('company'):
                return request.user.client_can_create_application_extra
        else:
            return request.user.client_can_create_application_extra


class IsClientCanEditApplicationAndIsManagerUser(permissions.BasePermission):
    '''
    CLIENT CAN EDIT APPLICATIONS
    '''

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_manager:
            return True
        if request.user.client_can_edit_application_extra:
            if obj.company == request.user.main_company.name:
                return request.user.client_can_edit_application_extra
        else:
            return request.user.client_can_edit_application_extra


'''''Manager's permissions'''''


class IsAdminOrManagerOrClientUsersCanEditComments(permissions.BasePermission):
    '''
    MANAGER CAN DELETE COMMENTS AND CLIENT CAN EDIT COMMENTS
    '''

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


class IsManagerAndClientCanGetReportsOrIsAdminUser(permissions.BasePermission):
    '''
    MANAGER AND CLIENT CAN GET REPORTS
    '''

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


class IsManagerCanDeleteApplicationOrIsAdminUser(permissions.BasePermission):
    '''
    MANAGER CAN DELETE APPLICATIONS
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.manager_can_delete_applications_extra:
            return request.user.manager_can_delete_applications_extra
        else:
            return request.user.manager_can_delete_applications


class IsManagerCanCreateAndEditCompanyOrIsAdminUser(permissions.BasePermission):
    '''
    MANAGER CAN CREATE AND EDIT COMPANY
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.manager_can_create_and_edit_company


class IsManagerCanCreateAndEditUserOrIsAdminUser(permissions.BasePermission):
    '''
    MANAGER CAN CREATE USER
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.manager_can_create_and_edit_user_extra


class IsManagerCanCreateAndDeleteJobTitleOrIsAdminUser(permissions.BasePermission):
    '''
    MANAGER CAN CREATE AND DELETE JOB TITLES
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.manager_can_create_and_delete_job_title_extra
