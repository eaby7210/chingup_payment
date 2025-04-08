import requests
import json
from django.conf import settings
from core.models import OAuthToken
from core.services import OAuthServices

BASE_URL = "https://services.leadconnectorhq.com"
VERSION = "2021-07-28"


class GHLCustomProviderServices:

    @staticmethod
    def create_custom_provider_integration(data:dict):
        """
        Creates a new custom provider integration with GHL.
        """
        
        token_obj:OAuthToken = OAuthServices.get_valid_access_token_obj()
        url = f"{BASE_URL}/payments/custom-provider/provider"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token_obj.access_token}",
            "Content-Type": "application/json",
            "Version": VERSION,
        }
        params = {
            "locationId": token_obj.LocationId
        }
        # data={
        # "name": "Company Paypal Integration",
        # "description": "This payment gateway supports payments in India via UPI, Net banking, cards and wallets.",
        # "paymentsUrl": "https://testpayment.paypal.com",
        # "queryUrl": "https://testsubscription.paypal.com",
        # "imageUrl": "https://testsubscription.paypal.com"
        # }
        try:
            print(json.dumps(data, indent=4))
            response = requests.post(url, headers=headers, params=params, json=data)
            print(json.dumps(response.json(), indent=4))
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print("Error while creating custom provider:", e)
            return None

class ChingUpServices:
   
   @staticmethod
   def integrate_chingup():
       data={
        "name": "Chingup",
        "description": "This payment gateway supports payments in India via UPI, Net banking, cards and wallets.",
        "paymentsUrl": "https://testpayment.paypal.com",
        "queryUrl": "https://testsubscription.paypal.com",
        "imageUrl": "https://testsubscription.paypal.com"
        }
       res =GHLCustomProviderServices.create_custom_provider_integration(data)
       print(json.dumps(res, indent=4))
       
       
    # @staticmethod
    # def 
   
   

class GHLPaymentServices:
    pass