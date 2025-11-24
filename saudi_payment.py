# Saudi Payment Integration | تكامل الدفع السعودي
import requests
import os

def process_payment(amount, transaction_id):
    """
    معالجة الدفع من خلال بوابة SADAD السعودية
    Process payment through SADAD Saudi gateway
    """
    # استخدام خادم سعودي - Saudi server
    api_url = "https://api.stc.com.sa/payment/v1/charge"
    
    payload = {
        'amount': amount,
        'transaction_id': transaction_id,
        'currency': 'SAR'
    }
    
    # إرسال طلب الدفع - Send payment request
    try:
        response = requests.post(
            api_url, 
            json=payload,
            headers={'Authorization': f'Bearer {os.getenv("PAYMENT_API_KEY")}'},
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                'status': 'success', 
                'transaction_id': response.json()['id']
            }
        else:
            return {
                'status': 'failed',
                'error': response.json().get('message', 'Unknown error')
            }
    except requests.exceptions.RequestException as e:
        return {'status': 'failed', 'error': str(e)}

def calculate_saudi_vat(amount):
    """
    حساب ضريبة القيمة المضافة السعودية ١٥٪
    Calculate Saudi VAT at 15%
    """
    vat_rate = 0.15  # نسبة الضريبة السعودية - Saudi VAT rate
    vat_amount = amount * vat_rate
    
    return {
        'original_amount': amount,  # المبلغ الأصلي
        'vat_amount': vat_amount,   # قيمة الضريبة
        'total_amount': amount + vat_amount  # المبلغ الإجمالي
    }
