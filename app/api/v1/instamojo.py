# instamojo_backend.py
from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
from typing import Optional
from instamojo_wrapper import Instamojo
import requests

router=APIRouter()

api = Instamojo(
    api_key="98f329e1cfeb7a603f99d30cefa16f9a",
    auth_token="b0e533988e5c0a826c72762c1675d2cf",
    endpoint="https://www.instamojo.com/api/1.1/payment-requests/"
)

class PaymentRequest(BaseModel):
    name: str
    email: str
    phone: str
    amount: float
    purpose: str
    redirect_url: Optional[str]

@router.post("/api/create-payment/")
def create_payment(amount: float, name: str, email: str, phone: str):

    token=requests.post('https://api.instamojo.com/oauth2/token/', data={
    	'grant_type': 'client_credentials',
  		'client_id': '5VHoNwaNqhxahIip6r5VhhceFqZ7XMj52N8xPgID',
    	'client_secret': 'fCPOakhDBOb6Po8iuo8ymsIFSRYo1QsBF64CnwDDVm4Cun3LHZvAAWK0ZOd9m8fSQsORs3IzawPrBQfqR2fvW7lXnhxlrv7L8Np0atZq3mzdFTbJzOuzvJu6jIsjqT2Q'
    })
    print("token===>",token.json())
    res_token=token.json()
    payload = {
        "amount": amount,
        "purpose": "Test Payment",
        "buyer_name": name,
        "email": email,
        "phone": phone,
        "redirect_url": "http://127.0.0.1:3000/",
    }
    
    headers = {
        "X-Api-Key": "98f329e1cfeb7a603f99d30cefa16f9a",
        "X-Auth-Token": "b0e533988e5c0a826c72762c1675d2cf",
        "Authorization": f"Bearer {res_token['access_token']}"
    }

    response = requests.post("https://api.instamojo.com/v2/payment_requests/", json=payload, headers=headers)
    return response.json()