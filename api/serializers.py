from rest_framework import serializers
from .models import *




class MetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = metrics
        fields = ["On_time_delivery_rate", "quality_rating_avg", "fulfilment_rate"]

class VendorSerializer(serializers.ModelSerializer):
       metrics = serializers.SerializerMethodField(read_only = True) 
       class Meta:
              model = vendor
              fields = ["id" , "contact_details" , "address" , "metrics" 
                         ,"name"]
       
       def get_metrics(self, obj):
        if obj.metrics is None:
            return None
        else:
            # Serialize the metrics object to a dictionary
            return MetricsSerializer(obj.metrics).data
              