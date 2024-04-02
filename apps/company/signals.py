from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Company


@receiver(pre_save, sender=Company)
def uppercase_company_code(sender, instance, **kwargs):
    instance.company_code = instance.company_code.upper()