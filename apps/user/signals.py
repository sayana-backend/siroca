from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser


def jls_extract_def():
    return 


@receiver(post_save, sender=CustomUser)
def update_username(sender, instance, created, **kwargs):
    if created:
        username = instance.surname.lower() + instance.first_name.lower()
        company_domain = instance.company_relation.domain = jls_extract_def()
        full_username = f"{username}@{company_domain}.com"
        instance.username = full_username
        instance.save()  


