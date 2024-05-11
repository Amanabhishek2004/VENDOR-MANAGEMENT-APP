from rest_framework import serializers
from django.db.models import F, ExpressionWrapper, DurationField

from .models import *




class MetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = metrics
        fields = ["On_time_delivery_rate", "quality_rating_avg", "fulfilment_rate" , "average_response_time"]

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


class PoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase_Order_Tracking
        fields = '__all__'

    def update(self, instance, validated_data):
        request = self.context.get('request')  # Accessing the request object from the context

        vendor_data = instance.Vendor
        data = request.data  # Using request.data to access the request data
        VENDOR_DATA = Purchase_Order_Tracking.objects.filter(Vendor=vendor_data)
        count = VENDOR_DATA.count()
        
        # counting the initial  not null acknowledgment and issue data values 
        data_count = 0 

        if data.get("status") == 'C' and instance.status != "C":  
           
            today_date = datetime.date.today()
            delivery_date = instance.delivery_date

            # ON TIME DELIVERY STATUS 
            if delivery_date > today_date:
                initial_delivery_rate = vendor_data.metrics.On_time_delivery_rate
                final_delivery_rate = (initial_delivery_rate * count + 1) /count
            
                vendor_data.metrics.On_time_delivery_rate = final_delivery_rate

            
            # QUALITY RATING FACTOR
            count = 0
            agr_quality_factor = 0
            for i in VENDOR_DATA:
                if i.quality_rating != 0 :
                    data_count+=1
                    agr_quality_factor+=i.quality_rating
            if agr_quality_factor != 0 :
                vendor_data.metrics.quality_rating_avg = agr_quality_factor/data_count


            # AVERAGE RESPONSE TIME 
            agr_response_time = 0
            for i in VENDOR_DATA:
                  agr_response_time +=(i.acknowledgment_date - i.issue_date).total_seconds() / 3600
                  data_count+=1

            vendor_data.metrics.average_response_time = agr_response_time/(data_count)                       
            
            #  FULFILLMENT TIME 
            data_count = count
            completed_order_count = VENDOR_DATA.filter(status ="C").count()
            vendor_data.metrics.fulfilment_rate = completed_order_count/(data_count)

            vendor_data.metrics.save()                       

        if validated_data['acknowledgment_date']:
            #  ON UPDATION OF ACKNOWLEDGEMENT TIME UPDATE THE 
            
            # Calculate the time difference in hours
            time_difference_hours = 0
            for i in VENDOR_DATA:
                if i.acknowledgment_date != None  and i.issue_date != None:
                       time_difference_hours += (instance.acknowledgment_date - instance.issue_date).total_seconds() / 3600
                       data_count+=1
            # Update the average response time
            vendor_data.metrics.average_response_time += time_difference_hours / (data_count)                      
            vendor_data.metrics.save() 

        return super().update(instance, validated_data)
              