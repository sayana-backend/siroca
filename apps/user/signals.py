from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.utils.text import slugify
from .models import Company








@receiver(post_save, sender=CustomUser)
def update_username(sender, instance, created, **kwargs):
    if created:
        username = (instance.surname.lower() + instance.first_name.lower()).replace(" ", "")
        company_domain = instance.main_company.domain
        
        # Проверяем существование домена
        if not Domain.objects.filter(domain=company_domain).exists():
            full_username = f"{username}@{company_domain}.com"
        else:
            full_username = f"{username}@{company_domain}"

        if full_username != instance.username:
            instance.username = full_username
            instance.save(update_fields=['username'])



   

