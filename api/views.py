from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from.models import *
import datetime

# Create your views here.

class VendorApiView(generics.RetrieveUpdateDestroyAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = "id"

class VendorApiGet(generics.ListCreateAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = vendor.objects.all()
    serializer_class = VendorSerializer


class POApiView(generics.RetrieveUpdateDestroyAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Purchase_Order_Tracking.objects.all()
    serializer_class = PoSerializer
    lookup_field = "po_number" 


    
class POcreateApiView(generics.ListCreateAPIView):
    
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     queryset = Purchase_Order_Tracking.objects.all()
     serializer_class = PoSerializer


class Acknowledge_po(generics.RetrieveUpdateAPIView):
    
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    queryset = Purchase_Order_Tracking.objects.all()
    serializer_class = PoSerializer
    lookup_field = "po_number"


    def perform_update(self, serializer):
        instance = self.get_object()
        data = {
            "acknowledgment_date": datetime.date.today()
        }
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class VendorPerformanceApi(generics.RetrieveAPIView):
    queryset = metrics.objects.all()
    serializer_class = MetricsSerializer
    lookup_field = "Vendor_id"
    
    def get_lookup_fields(self):
        instance = self.get_object()
        print(instance)
        return {'Vendor_id': instance.Vendor.pk}
    