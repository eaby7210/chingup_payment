import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings


@csrf_exempt
@xframe_options_exempt
def payment_view(request):
    if request.method == "POST":
        data =json.loads(request.body)
        
        print(json.dumps(data, indent=4))
        
        return render(request,"payment_iframe.html",data)
    elif request.method =='GET':
        data={
            'merchant_id':settings.CHINGUP_MERCHANT_SANDBOX_ID
        }
        return render(request,"payframe.html",data)

@csrf_exempt
def payment_verify(request):
    if request.method == 'POST':
        data =json.loads(request.body)
        
        print(json.dumps(data, indent=4))
        
        return JsonResponse()