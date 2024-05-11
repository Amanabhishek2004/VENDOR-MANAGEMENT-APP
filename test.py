import requests

headers = {'Authorization': 'Token ca020c502b0a3db79659b6450de10a25311a5e50'}

response = requests.get("http://127.0.0.1:8000/api/vendors/" ,headers=headers)
print(response.json())


'''
CRUD FOR ORDERS
'''



#  FOR PO_ORDERS POST REQUEST
po_data = {
    "vendor": "a4693949-19ac-40e7-9a8b-55f05a8779ed",  
    "order_date": "2024-05-10T10:00:00",  
    "delivery_date": "2024-05-15",  
    "items": [
        {"name": "Item 1", "quantity": 10},
        {"name": "Item 2", "quantity": 5}
    ],
    "status": "P",
    "quantity":10,
    "quality_rating": 4.5,
    "issue_date": "2024-05-10",  
    "acknowledgment_date": "2024-05-12"  
}


response = requests.post("http://127.0.0.1:8000/api/orders/" ,headers=headers , data = po_data )


# FOR PO_ORDERS PATCH REQUEST

data = {

 "items":[
   {"name": "Item 1", "quantity": 11},
   {"name": "Item 2", "quantity": 4}
 ]
}

response = requests.patch("http://127.0.0.1:8000/api/orders/355909d0-9840-4640-a01c-d71e76e1f8ad" , data = data , headers=headers)



#  FOR ACKNOWLEDGING THE ENDPOINTS

response = requests.get("http://127.0.0.1:8000/api/orders/355909d0-9840-4640-a01c-d71e76e1f8ad/acknowledge" , data = data , headers=headers)

'''
CRUD FOR VENDORS
'''

# getting all vendors

response = requests.get('http://127.0.0.1:8000/api/vendors/' , headers=headers)


# posting data 

data =  { "name": "Vendor Name",
  "contact_details": 1234567890,
  "address": "Vendor Address"
}

response = requests.post('http://127.0.0.1:8000/api/vendors/' , data=data ,  headers=headers)

# updating vendor data 

data =  { "name": "HARSH RAJ"
}

response = requests.patch('http://127.0.0.1:8000/api/vendors/a4693949-19ac-40e7-9a8b-55f05a8779ed' , data=data , headers=headers)



#  seeing the metrics


response = requests.patch('http://127.0.0.1:8000/api/performance/a4693949-19ac-40e7-9a8b-55f05a8779ed' , data=data , headers=headers)

