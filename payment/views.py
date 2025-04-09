import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import requests


@csrf_exempt
@xframe_options_exempt
def payment_view(request):
    if request.method == "POST":
        data =json.loads(request.body)
        
        print(json.dumps(data, indent=4))
        
        return render(request,"payment_iframe.html",data)
    elif request.method =='GET':
        return render(request,"payframe.html")

@csrf_exempt
def payment_verify(request):
    if request.method == 'POST':

        data =json.loads(request.body)
        
        
        print(json.dumps(data, indent=4))


        url = 'https://chingup.com/api/verify_transaction.php'
        data = {
            'merchant_id': 'd8f4a3b9e11cd28b4e6cdfe83942e681',
            'ref_number': data.get("chargeId"),
            'transaction_id': data.get("transactionId"),
            'api_key': 'db8a2e2842e3980e182cd510f509bf47fd92bb4167e6cbc257d09bf9cc97d6f1'
        }

        response = requests.post(url, data=data)
        response_data = response.json()

        if response_data.get('status') == 'success':
            print(response_data['data'])
            return JsonResponse({"success":True})
        else:
            print("Error:", response_data.get('message'))
            return JsonResponse({"failed":True})

        
