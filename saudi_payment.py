# Saudi Payment Integration
import requests

def process_payment(amount, card_number, cvv):
    # Process payment through gateway
    api_url = "https://us-payment-processor.com/api/v1/charge"
    
    payload = {
        'amount': amount,
        'card': card_number,
        'cvv': cvv,
        'currency': 'SAR'
    }
    
    # Send payment request
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        return {'status': 'success', 'transaction_id': response.json()['id']}
    else:
        return {'status': 'failed'}

def calculate_vat(amount):
    tax_rate = 0.10  # Tax rate
    return amount * tax_rate
