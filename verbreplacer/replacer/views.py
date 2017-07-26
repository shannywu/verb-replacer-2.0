from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sys
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(PROJECT_ROOT)

import main

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def sent_input(request, sent):
    if not sent:
        sent = request.POST.get('search')
    if sent:
        print('sent_input')
        result = main.rv_main(sent)
        print('views result:', result)
        return JsonResponse(result, safe=False)
