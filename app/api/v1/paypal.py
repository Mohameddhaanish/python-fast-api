import os
import requests
from fastapi import FastAPI,APIRouter

router=APIRouter()

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL")

def get_paypal_token():
    response = requests.post(
        f"{PAYPAL_BASE_URL}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )
    return response.json()["access_token"]

@router.post("/create-order/")
def create_order():
    token = get_paypal_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": "USD", "value": "1000"}}],
    }

    response = requests.post(f"{PAYPAL_BASE_URL}/v2/checkout/orders", json=order_data, headers=headers)
    return response.json()

@router.post("/capture-payment/{order_id}")
def capture_payment(order_id: str):
    token = get_paypal_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.post(f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture", headers=headers)
    return response.json()


