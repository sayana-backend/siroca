from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from .usermanager import CustomUserManager
# from apps.application.models import ApplicationForm
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class AdminContact(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=20, verbose_name='Телефонный номер')
    whatsapp_number = models.CharField(max_length=20, verbose_name='Номер WhatsApp')

    def __str__(self):
        return f"Контакт для админа {self.user}"


    class  Meta:
        verbose_name = 'Контакт для админа'
        verbose_name_plural = "Контакты для админа"
    


    




class CustomUser(AbstractBaseUser, PermissionsMixin):
    RoleType = {
        'client': 'Клиент',
        'manager': 'Менеджер',
    }
    role_type = models.CharField(max_length=20, choices=RoleType.items())
    username = models.CharField(max_length=30, verbose_name="Логин", unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="фамилия")
    image = models.ImageField(verbose_name="Изображение", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")
    is_client = models.BooleanField(default=True, verbose_name="Клиент")

    company_relation = models.ForeignKey('company.Company', null=True,verbose_name='отношения с компанией', blank=True, on_delete=models.SET_NULL,
                                         related_name='users')
    main_company = models.ForeignKey('company.Company', verbose_name="Компания", related_name='company_users', on_delete=models.CASCADE, null=True)
    managers_company = models.ManyToManyField('company.Company', verbose_name="Компании менеджеров", related_name='managers_company', blank=True)
    job_title = models.ForeignKey('company.JobTitle',
                                  verbose_name="Должность",
                                  related_name='user_job_titles',
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL)

    objects = CustomUserManager()
    



   
    def save(self, *args, **kwargs):
        if not self.username:
            raise ValueError("Username cannot be empty")
    
        if self.role_type == 'Клиент':
            self.is_client = True
        elif self.role_type == 'Менеджер':
         self.is_manager = True

        if self.company_relation:
            company_domain = self.company_relation.domain
            self.username += f"@{company_domain}.com"

        super().save(*args, **kwargs)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    USERNAME_FIELD = 'username'


















# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.utils.text import slugify
# from django.utils.translation import gettext_lazy as _
# from .usermanager import CustomUserManager
# from apps.company.models import Company

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ('Клиент', _('Клиент')),
#         ('Менеджер', _('Менеджер')),
#     )
#     image = models.ImageField(null=True, blank=True)
#     name = models.CharField(max_length=30)
#     role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     username = models.CharField(max_length=100, verbose_name=_("Юзернейм"), unique=True)
#     surname = models.CharField(max_length=30, verbose_name=_("Фамилия"), null=True, blank=True)
#     job_title = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_client = models.BooleanField(default=True)
#     is_manager = models.BooleanField(default=False, verbose_name=_("Менеджер"))
#     company_relation = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)    

#     objects = CustomUserManager()



#     if self.role_type == 'Менеджер':
#             self.is_manager = True
#             self.is_client = False

#     super().save(*args, **kwargs)

#     def __str__(self):
#         return self.username

#     class Meta:
#         verbose_name = _('Клиент')
#         verbose_name_plural = _('Клиенты')

#     USERNAME_FIELD = 'username'
# =======
#     def save(self, *args, **kwargs):
#         if not self.username:
#             if self.surname and self.name:
#                 self.username = f"{slugify(self.surname)}{slugify(self.name)}"
#             elif self.surname:
#                 self.username = f"{slugify(self.surname)}"
#             elif self.name:
#                 self.username = f"{slugify(self.name)}"
#             else:
#                 raise ValueError("Surname and name cannot be both empty")

#             if self.role_type == 'Клиент':
#                 self.is_client = True
#             elif self.role_type == 'Менеджер':
#                 self.is_manager = True

#             if self.company_relation:
#                 company_domain = self.company_relation.domain
#                 self.username += f"@{company_domain}.com"

#             super().save(*args, **kwargs)

#     def save(self, *args, **kwargs):
#         if self.role_type == 'manager':
#             self.is_manager = True
#         super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = verbose_name
# >>>>>>> ffb29b7e4319d07ee04a62f1a8c00472e7241ba2


# class Notification(models.Model):
#     task_number = models.CharField(max_length=50,null=True,blank=True)
#     text = models.CharField(max_length=300, null=True, blank=True)
#     created_at = models.DateField(auto_now_add=True, null=True, blank=True)
#     expiration_time = models.DateTimeField(null=True)
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
#     application_id = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True)



