from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Company
from django.core.exceptions import PermissionDenied


@receiver(pre_save, sender=Company)
def uppercase_company_code(sender, instance, **kwargs):
    instance.company_code = instance.company_code.upper()

@receiver(pre_delete, sender=Company)
def prevent_delete_first_company(sender, instance, **kwargs):
    first_company = Company.objects.first()
    if instance.id == first_company.id:
        raise PermissionDenied("Нельзя удалить первую компанию!")