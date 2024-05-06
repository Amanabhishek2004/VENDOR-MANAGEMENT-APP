from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=vendor)
def create_target_model(sender, instance, created, **kwargs):
    if created:        
        data = metrics.objects.create(Vendor=instance)
        instance.metrics = data
        instance.save()