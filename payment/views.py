import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt


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
        
        return JsonResponse()