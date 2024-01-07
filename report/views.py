from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse #http응답객체. HttpResponse는 클라이언트에게 200을 보내줌.
from .models import *
from . import brandrecommendation
import json, requests, math
from time import sleep
# Create your views here.

def inquire(request):
    print('test')
    print('ID: ', request.method)
    print('POST: ', request.POST)
    output = ""
    
    if request.method == 'POST':
        inputs = request.POST
        user_name = inputs['id']
        user_pw = inputs['pwd']
        business = inputs['업종']
        seedMoney = int(inputs['seedMoney'])
        
        apikey_encoded = "API키"
        recommendList = brandrecommendation.RecommendBrand(apikey_encoded, 2022, seedMoney, business)
        #print(recommendList)
        rank = 1
        
        for brands in recommendList:
            output+f" {rank} 위 업체_________________\n브랜드명 : {brands['brandNm']}\n가맹사명 : {brands['corpNm']}\n가맹업주 부담금(천원) : {brands['smtnAmt']}\n평균매출(천원) : {brands['avrgSlsAmt']}"+'\n\n\n'
            rank += 1        
        print(output)
    print('imalive')
    return render(request, 'report\inquire.html', {'teststring' : output})

def recommendation(request, A, B):
    return HttpResponse("output")