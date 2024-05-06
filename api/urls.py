from django.urls import path
from .views import *

urlpatterns = [
    path("vendors/", VendorApiGet.as_view(), name="vendor-data"),
    path("vendors/<str:id>/", VendorApiView.as_view(), name="vendor-individual-data"),
]
