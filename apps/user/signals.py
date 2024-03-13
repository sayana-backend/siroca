# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def update_username(sender, instance, created, **kwargs):
#     if created:  
#         username = instance.surname.lower() + instance.name.lower()
        
#         company_domain = instance.company_relation.domain
        
#         full_username = f"{username}@{company_domain}.com"
        
#         instance.username = full_username
#         instance.save()  

