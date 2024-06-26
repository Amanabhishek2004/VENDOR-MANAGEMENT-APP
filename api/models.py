from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from .models import *
import datetime
import uuid



STATUS_CHOICES = [
    ('C' , 'COMPLETED'),
    ('CN' , 'CANCELLED'),
    ('P' , 'PENDING')
]



class vendor(models.Model):
    
    id = models.CharField(primary_key=True, editable=False, default=uuid.uuid4 , max_length=8)
    name = models.CharField(max_length=20)
    contact_details = models.BigIntegerField()
    address = models.CharField(max_length=50)
    metrics = models.ForeignKey("metrics", on_delete=models.CASCADE, related_name="performance_data" , null = True , blank=True)  

    def __str__(self) -> str:
        return self.name

class metrics(models.Model):
    
    On_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0) 
    fulfilment_rate = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0 , null=True)
    Vendor = models.ForeignKey(vendor, on_delete=models.CASCADE , related_name = "vendor_data")

    def __str__(self) -> str:
        return f"{self.Vendor.name}'s Metrics"

class Purchase_Order_Tracking(models.Model):
    
    po_number = models.CharField(primary_key=True , default= uuid.uuid4 , editable=False , max_length=8)
    Vendor = models.ForeignKey(vendor , on_delete=models.SET_NULL , null = True)
    order_date = models.DateTimeField()
    delivery_date = models.DateField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=12 , choices = STATUS_CHOICES)
    quality_rating = models.FloatField(default=0.0)
    issue_date = models.DateField()
    acknowledgment_date = models.DateField()

    def save(self,*arg , **kwargs) -> None:
        self.calculate_quantity()
        super().save(*arg , **kwargs)
    

    def set_issue_date(self):
        

        if self.Vendor == None:
            self.issue_date = None
        else:
            self.issue_date = datetime.now()
                


    def calculate_quantity(self):
        total_quantity = 0

        for item in self.items:
            total_quantity+=item.get("quantity" , 0)
        self.quantity = total_quantity    


@receiver(post_save, sender=vendor)
def create_target_model(sender, instance, created, **kwargs):
    if created:        
        data = metrics.objects.create(Vendor=instance)
        instance.metrics = data
        instance.save()

@receiver(post_save, sender=User)
def generate_token(sender, instance, created, **kwargs):
    if created:        
        Token.objects.create(user=instance)
  