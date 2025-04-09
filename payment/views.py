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


        # url = 'https://chingup.com/api/verify_transaction.php'
        # data = {
        #     'merchant_id': '3023d9618e722844c74c33fcad28f130',
        #     'ref_number': '000011112',
        #     'transaction_id': '2d5491c573a96002',
        #     'api_key': 'MERCHANT_UNIQUE_API_KEY'
        # }

        # response = requests.post(url, data=data)
        # response_data = response.json()

        # if response_data.get('status') == 'success':
        #     print(response_data['data'])
        # else:
        #     print("Error:", response_data.get('message'))
        
        return JsonResponse()