import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def paymwnt_view(request):
    if request.method == "POST":
        data =json.loads(request.body)
        
        print(json.dumps(data, indent=4))
        
        return render(request,"payment_iframe.html",data)

@csrf_exempt
def payment_verify(request):
    if request.method == 'POST':
        data =json.loads(request.body)
        
        print(json.dumps(data, indent=4))
        
        return JsonResponse()