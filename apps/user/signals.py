from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser






@receiver(post_save, sender=CustomUser)
def update_username(sender, instance, created, **kwargs):
    if created:
        username = (instance.surname.lower() + instance.name.lower()).replace(" ", "")
        company_domain = instance.main_company.domain
        
        full_username = f"{username}@{company_domain}"
        
        # Проверяем существование домена
        domain_instance = Domain.objects.filter(domain=company_domain).exists()
        if domain_instance:
            if full_username != instance.username:
                instance.username = full_username
                instance.save(update_fields=['username'])
        else:
            if username != instance.username:
                instance.username = username
                instance.save(update_fields=['username'])



   

