from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from apps.company.models import JobTitle, Company
from .usermanager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
   USERNAME_FIELD = 'username'
   ROLE_CHOICES = (
       ('Клиент', _('Клиент')),
       ('Менеджер', _('Менеджер')),
   )
   username = models.CharField(max_length=100, verbose_name=_("Юзернейм"), unique=True)
   image = models.ImageField(null=True, blank=True)
   name = models.CharField(max_length=30)
   role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)
   surname = models.CharField(max_length=30, verbose_name=_("Фамилия"), null=True, blank=True)
   job_title = models.ForeignKey('apps.JobTitle', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Должность"))
   created_at = models.DateTimeField(auto_now_add=True)
   is_staff = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)
   is_client = models.BooleanField(default=False)
   is_manager = models.BooleanField(default=False)
   company_relation = models.ForeignKey('Company', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')

   objects = CustomUserManager()




   
#    def save(self, *args, **kwargs):
#     if not self.username:
#         if self.surname and self.name:
#             self.username = f"{slugify(self.surname)}{slugify(self.name)}"
#         elif self.surname:
#             self.username = f"{slugify(self.surname)}"
#         elif self.name:
#             self.username = f"{slugify(self.name)}"
#         else:
#             raise ValueError("Surname and name cannot be both empty")

#     if self.role_type == 'Клиент':
#         self.is_client = True
#     elif self.role_type == 'Менеджер':
#         self.is_manager = True

#     if self.company_relation:
#         company_domain = self.company_relation.domain
#         self.username += f"@{company_domain}.com"

#     super().save(*args, **kwargs)

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




