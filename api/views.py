from django.shortcuts import render
from rest_framework import generics
from.models import *
from .serializers import *

# Create your views here.

class VendorApiView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = "id"

class VendorApiGet(generics.ListCreateAPIView):
    
    queryset = vendor.objects.all()
    serializer_class = VendorSerializer