from django.urls import path
from .views import *

urlpatterns = [
 
    path("vendors/", VendorApiGet.as_view(), name="vendor-data"),
    path("vendors/<str:id>/", VendorApiView.as_view(), name="vendor-individual-data"),
    path("performance/<str:Vendor_id>/", VendorPerformanceApi.as_view(), name="vendor-individual-data"),
    path("orders/" , POcreateApiView.as_view() , name = "list-po"),
    path("orders/<str:po_number>" , POApiView.as_view() , name = "create-po"),
    path("orders/<str:po_number>/acknowledge" , Acknowledge_po.as_view() , name = "acknowledge-po")

]
