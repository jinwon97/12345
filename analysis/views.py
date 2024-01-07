from django.shortcuts import render
from urllib.parse import unquote
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import pandas as pd

from .models import *
from .serializers import *

from pycaret.regression import *

# 추정 : 23년 3분기의 매출을 출력
# 예측 : 23년 4분기의 매출을 출력

# 23년 3분기 행정동 추정
class dong_estimate(APIView):
    def get(self, request, *args, **kargs):
        dong = unquote(self.kwargs['dong'])
        business = unquote(self.kwargs['business'])
        funds = self.kwargs['funds']
        
        x_cols = ['행정동_코드', '서비스_업종_코드', '관공서_수', '은행_수', '종합병원_수', '일반_병원_수', '약국_수',
       '유치원_수', '초등학교_수', '중학교_수', '고등학교_수', '대학교_수', '백화점_수', '슈퍼마켓_수',
       '극장_수', '숙박_시설_수', '공항_수', '철도_역_수', '버스_터미널_수', '지하철_역_수', '버스_정거장_수',
       '연령대_10_직장_인구_수', '연령대_20_직장_인구_수', '연령대_30_직장_인구_수', '연령대_40_직장_인구_수',
       '연령대_50_직장_인구_수', '연령대_60_이상_직장_인구_수', '점포_수', '개업_율', '개업_점포_수',
       '폐업_률', '폐업_점포_수', '프랜차이즈_점포_수', '아파트_단지_수', '아파트_면적_66_제곱미터_미만_세대_수',
       '아파트_면적_66_제곱미터_세대_수', '아파트_면적_99_제곱미터_세대_수', '아파트_면적_132_제곱미터_세대_수',
       '아파트_면적_165_제곱미터_세대_수', '아파트_가격_1_억_미만_세대_수', '아파트_가격_1_억_세대_수',
       '아파트_가격_2_억_세대_수', '아파트_가격_3_억_세대_수', '아파트_가격_4_억_세대_수',
       '아파트_가격_5_억_세대_수', '아파트_가격_6_억_이상_세대_수', '아파트_평균_면적', '아파트_평균_시가',
       '월_평균_소득_금액', '식료품_지출_총금액', '의류_신발_지출_총금액', '생활용품_지출_총금액', '의료비_지출_총금액',
       '교통_지출_총금액', '교육_지출_총금액', '유흥_지출_총금액', '여가_문화_지출_총금액', '기타_지출_총금액',
       '음식_지출_총금액', '연령대_10_상주인구_수', '연령대_20_상주인구_수', '연령대_30_상주인구_수',
       '연령대_40_상주인구_수', '연령대_50_상주인구_수', '연령대_60_이상_상주인구_수', '아파트_가구_수',
       '비_아파트_가구_수', '연령대_10_유동인구_수', '연령대_20_유동인구_수', '연령대_30_유동인구_수',
       '연령대_40_유동인구_수', '연령대_50_유동인구_수', '연령대_60_이상_유동인구_수',
       '시간대_00_06_유동인구_수', '시간대_06_11_유동인구_수', '시간대_11_14_유동인구_수',
       '시간대_14_17_유동인구_수', '시간대_17_21_유동인구_수', '시간대_21_24_유동인구_수','분기', '코로나_여부', '전년도_점포별_평균_매출_금액']
        
        
        queryset1 = DongData.objects.filter(기준_년분기_코드 = 20233, 행정동_코드_명 = dong, 서비스_업종_코드_명 = business).values(*x_cols[:-1])
        queryset1 = queryset1[0]
        
        queryset2 = DongData.objects.filter(기준_년분기_코드 = 20223, 행정동_코드_명 = dong, 서비스_업종_코드_명 = business).values('점포별_평균_매출_금액')
        queryset2= queryset2[0]
        
        queryset2['전년도_점포별_평균_매출_금액'] = queryset2['점포별_평균_매출_금액']
        
        queryset1.update(queryset2)
        
        
        data_pd = pd.DataFrame(queryset1, index=[0])
        
        
        final_model = load_model("analysis/aimodel/dong_service_estimate_model1")
        prediction = predict_model(final_model, data = data_pd)
        result = prediction['prediction_label']
        
        return Response({"success":result}, status=status.HTTP_200_OK)



# 23년 4분기 행정동 예상
class dong_predict(APIView):
    def get(self, request, *args, **kargs):
        
        dong = unquote(self.kwargs['dong'])
        business = unquote(self.kwargs['business'])
        fund = self.kwargs['funds']
        
        x_cols = ['행정동_코드', '서비스_업종_코드', '관공서_수', '은행_수', '종합병원_수', '일반_병원_수', '약국_수',
       '유치원_수', '초등학교_수', '중학교_수', '고등학교_수', '대학교_수', '백화점_수', '슈퍼마켓_수',
       '극장_수', '숙박_시설_수', '공항_수', '철도_역_수', '버스_터미널_수', '지하철_역_수', '버스_정거장_수',
       '연령대_10_직장_인구_수', '연령대_20_직장_인구_수', '연령대_30_직장_인구_수', '연령대_40_직장_인구_수',
       '연령대_50_직장_인구_수', '연령대_60_이상_직장_인구_수', '점포_수', '개업_율', '개업_점포_수',
       '폐업_률', '폐업_점포_수', '프랜차이즈_점포_수', '아파트_단지_수', '아파트_면적_66_제곱미터_미만_세대_수',
       '아파트_면적_66_제곱미터_세대_수', '아파트_면적_99_제곱미터_세대_수', '아파트_면적_132_제곱미터_세대_수',
       '아파트_면적_165_제곱미터_세대_수', '아파트_가격_1_억_미만_세대_수', '아파트_가격_1_억_세대_수',
       '아파트_가격_2_억_세대_수', '아파트_가격_3_억_세대_수','아파트_가격_4_억_세대_수',
       '아파트_가격_5_억_세대_수', '아파트_가격_6_억_이상_세대_수', '아파트_평균_면적', '아파트_평균_시가',
       '월_평균_소득_금액', '식료품_지출_총금액', '의류_신발_지출_총금액', '생활용품_지출_총금액', '의료비_지출_총금액',
       '교통_지출_총금액', '교육_지출_총금액', '유흥_지출_총금액','여가_문화_지출_총금액','기타_지출_총금액',
       '음식_지출_총금액', '연령대_10_상주인구_수', '연령대_20_상주인구_수', '연령대_30_상주인구_수',
       '연령대_40_상주인구_수', '연령대_50_상주인구_수', '연령대_60_이상_상주인구_수', '아파트_가구_수',
       '비_아파트_가구_수', '연령대_10_유동인구_수', '연령대_20_유동인구_수', '연령대_30_유동인구_수',
       '연령대_40_유동인구_수', '연령대_50_유동인구_수', '연령대_60_이상_유동인구_수',
       '시간대_00_06_유동인구_수', '시간대_06_11_유동인구_수', '시간대_11_14_유동인구_수',
       '시간대_14_17_유동인구_수', '시간대_17_21_유동인구_수', '시간대_21_24_유동인구_수','분기', '코로나_여부', '전년도_점포별_평균_매출_금액']
        
        
        queryset1 = DongData.objects.filter(기준_년분기_코드 = 20233, 행정동_코드_명 = dong, 서비스_업종_코드_명 = business).values(*x_cols[:-1])
        queryset1 = queryset1[0]
        
        queryset2 = DongData.objects.filter(기준_년분기_코드 = 20224, 행정동_코드_명 = dong, 서비스_업종_코드_명 = business).values('점포별_평균_매출_금액')
        queryset2= queryset2[0]
        
        queryset2['전년도_점포별_평균_매출_금액'] = queryset2['점포별_평균_매출_금액']
        
        queryset1.update(queryset2)
        
        
        data_pd = pd.DataFrame(queryset1, index=[0])
        
        
        final_model = load_model("analysis/aimodel/dong_service_pred_model1")
        prediction = predict_model(final_model, data = data_pd)
        result = prediction['prediction_label']
        
        return Response({"success":result}, status=status.HTTP_200_OK)



# 23년 3분기 상권 추정    
class market_estimate(APIView):
    def get(self, request, *args, **kargs):
        market = unquote(self.kwargs['market'])
        business = unquote(self.kwargs['business'])
        funds = self.kwargs['funds']
        
        x_cols = ['상권_코드', '서비스_업종_코드', '관공서_수', '은행_수', '종합병원_수', '일반_병원_수', '약국_수',
       '유치원_수', '초등학교_수', '중학교_수', '고등학교_수', '대학교_수', '백화점_수', '슈퍼마켓_수',
       '극장_수', '숙박_시설_수', '공항_수', '철도_역_수', '버스_터미널_수', '지하철_역_수', '버스_정거장_수',
       '연령대_10_직장_인구_수', '연령대_20_직장_인구_수', '연령대_30_직장_인구_수', '연령대_40_직장_인구_수',
       '연령대_50_직장_인구_수', '연령대_60_이상_직장_인구_수', '점포_수', '개업_율', '개업_점포_수',
       '폐업_률', '폐업_점포_수', '프랜차이즈_점포_수', '자치구_코드', '행정동_코드', '아파트_단지_수',
       '아파트_면적_66_제곱미터_미만_세대_수', '아파트_면적_66_제곱미터_세대_수', '아파트_면적_99_제곱미터_세대_수',
       '아파트_면적_132_제곱미터_세대_수', '아파트_면적_165_제곱미터_세대_수', '아파트_가격_1_억_미만_세대_수',
       '아파트_가격_1_억_세대_수', '아파트_가격_2_억_세대_수', '아파트_가격_3_억_세대_수',
       '아파트_가격_4_억_세대_수', '아파트_가격_5_억_세대_수', '아파트_가격_6_억_이상_세대_수', '아파트_평균_면적',
       '아파트_평균_시가', '월_평균_소득_금액', '식료품_지출_총금액', '의류_신발_지출_총금액', '생활용품_지출_총금액',
       '의료비_지출_총금액', '교통_지출_총금액', '여가_지출_총금액', '문화_지출_총금액', '교육_지출_총금액',
       '유흥_지출_총금액', '연령대_10_유동인구_수', '연령대_20_유동인구_수', '연령대_30_유동인구_수',
       '연령대_40_유동인구_수', '연령대_50_유동인구_수', '연령대_60_이상_유동인구_수',
       '시간대_00_06_유동인구_수', '시간대_06_11_유동인구_수', '시간대_11_14_유동인구_수',
       '시간대_14_17_유동인구_수', '시간대_17_21_유동인구_수', '시간대_21_24_유동인구_수',
       '연령대_10_상주인구_수', '연령대_20_상주인구_수', '연령대_30_상주인구_수', '연령대_40_상주인구_수',
       '연령대_50_상주인구_수', '연령대_60_이상_상주인구_수', '아파트_가구_수', '비_아파트_가구_수', '분기',
       '코로나_여부', '주중_평균_유동인구', '주말_평균_유동인구', '점포별_예상_평균_매출_금액',
       '전년도_점포별_평균_매출_금액']
        
        
        workdayPopCol = ['월요일_유동인구_수', '월요일_유동인구_수', '월요일_유동인구_수', '월요일_유동인구_수', '월요일_유동인구_수']
        weekendPopCol = ['토요일_유동인구_수', '일요일_유동인구_수']
        
        queryset1 = MarketData.objects.filter(기준_년분기_코드 = 20233, 상권_코드_명 = market, 서비스_업종_코드_명 = business).values(*x_cols[:-4])
        queryset1 = queryset1[0]
        
        queryset2 = MarketData.objects.filter(기준_년분기_코드 = 20223, 상권_코드_명 = market, 서비스_업종_코드_명 = business).values('점포별_평균_매출_금액')
        queryset2= queryset2[0]
        queryset2['전년도_점포별_평균_매출_금액'] = queryset2['점포별_평균_매출_금액']
        
        queryset3 = MarketData.objects.filter(기준_년분기_코드 = 20223, 상권_코드_명 = market, 서비스_업종_코드_명 = business).values(*workdayPopCol)
        queryset3 = queryset3[0]
        
        workDayAveragePop = {'주중_평균_유동인구' : sum(list(queryset3.values())) / 5}
         
        
        queryset4 = MarketData.objects.filter(기준_년분기_코드 = 20223, 상권_코드_명 = market, 서비스_업종_코드_명 = business).values(*weekendPopCol)
        queryset4 = queryset4[0]
        
        weekEndAveragePop = {'주말_평균_유동인구' : sum(list(queryset4.values())) / 2}
        
        # 점포별 예상 평균 매출 금액은 DB 작업 후 올릴 예정
        #
        
        queryset1.update(workDayAveragePop, weekEndAveragePop, queryset2)
        
        data_pd = pd.DataFrame(queryset1, index=[0])
        
        
        final_model = load_model("analysis/aimodel/market_service_pred_model2")
        prediction = predict_model(final_model, data = data_pd)
        result = prediction['prediction_label']
        
        return Response({"success":result}, status=status.HTTP_200_OK)
    
    
    
# 23년 4분기 상권 예상
class market_predict(APIView):
    def get(self, request, *args, **kargs):
        market = unquote(self.kwargs['market'])
        buisness = unquote(self.kwargs['buisness'])
        fund = self.kwargs['funds']
        
        x_cols = ['상권_코드', '서비스_업종_코드', '관공서_수', '은행_수', '종합병원_수', '일반_병원_수', '약국_수',
       '유치원_수', '초등학교_수', '중학교_수', '고등학교_수', '대학교_수', '백화점_수', '슈퍼마켓_수',
       '극장_수', '숙박_시설_수', '공항_수', '철도_역_수', '버스_터미널_수', '지하철_역_수', '버스_정거장_수',
       '연령대_10_직장_인구_수', '연령대_20_직장_인구_수', '연령대_30_직장_인구_수', '연령대_40_직장_인구_수',
       '연령대_50_직장_인구_수', '연령대_60_이상_직장_인구_수', '점포_수', '개업_율', '개업_점포_수',
       '폐업_률', '폐업_점포_수', '프랜차이즈_점포_수', '자치구_코드', '행정동_코드', '아파트_단지_수',
       '아파트_면적_66_제곱미터_미만_세대_수', '아파트_면적_66_제곱미터_세대_수', '아파트_면적_99_제곱미터_세대_수',
       '아파트_면적_132_제곱미터_세대_수', '아파트_면적_165_제곱미터_세대_수', '아파트_가격_1_억_미만_세대_수',
       '아파트_가격_1_억_세대_수', '아파트_가격_2_억_세대_수', '아파트_가격_3_억_세대_수',
       '아파트_가격_4_억_세대_수', '아파트_가격_5_억_세대_수', '아파트_가격_6_억_이상_세대_수', '아파트_평균_면적',
       '아파트_평균_시가', '월_평균_소득_금액', '식료품_지출_총금액', '의류_신발_지출_총금액', '생활용품_지출_총금액',
       '의료비_지출_총금액', '교통_지출_총금액', '여가_지출_총금액', '문화_지출_총금액', '교육_지출_총금액',
       '유흥_지출_총금액', '연령대_10_유동인구_수', '연령대_20_유동인구_수', '연령대_30_유동인구_수',
       '연령대_40_유동인구_수', '연령대_50_유동인구_수', '연령대_60_이상_유동인구_수',
       '시간대_00_06_유동인구_수', '시간대_06_11_유동인구_수', '시간대_11_14_유동인구_수',
       '시간대_14_17_유동인구_수', '시간대_17_21_유동인구_수', '시간대_21_24_유동인구_수',
       '연령대_10_상주인구_수', '연령대_20_상주인구_수', '연령대_30_상주인구_수', '연령대_40_상주인구_수',
       '연령대_50_상주인구_수', '연령대_60_이상_상주인구_수', '아파트_가구_수', '비_아파트_가구_수', '분기',
       '코로나_여부', '주중_평균_유동인구', '주말_평균_유동인구', '점포별_예상_평균_매출_금액',
       '전년도_점포별_평균_매출_금액']
        
        workdayPopCol = ['월요일_유동인구_수', '월요일_유동인구_수', '월요일_유동인구_수', '월요일_유동인구_수', '월요일_유동인구_수']
        weekendPopCol = ['토요일_유동인구_수', '일요일_유동인구_수']
        
        queryset1 = MarketData.objects.filter(기준_년분기_코드 = 20233, 상권_코드_명 = market, 서비스_업종_코드_명 = buisness).values(*x_cols[:-4])
        queryset1 = queryset1[0]
        
        queryset2 = MarketData.objects.filter(기준_년분기_코드 = 20223, 상권_코드_명 = market, 서비스_업종_코드_명 = buisness).values('점포별_평균_매출_금액')
        queryset2= queryset2[0]
        queryset2['전년도_점포별_평균_매출_금액'] = queryset2['점포별_평균_매출_금액']
        
        queryset3 = MarketData.objects.filter(기준_년분기_코드 = 20223, 상권_코드_명 = market, 서비스_업종_코드_명 = buisness).values(*workdayPopCol)
        queryset3 = queryset3[0]
        
        workDayAveragePop = {'주중_평균_유동인구' : sum(list(queryset3.values())) / 5}
         
        
        queryset4 = MarketData.objects.filter(기준_년분기_코드 = 20223, 상권_코드_명 = market, 서비스_업종_코드_명 = buisness).values(*weekendPopCol)
        queryset4 = queryset4[0]
        
        weekEndAveragePop = {'주말_평균_유동인구' : sum(list(queryset4.values())) / 2}
        
        # 점포별 예상 평균 매출 금액은 DB 작업 후 올릴 예정
        #
        
        queryset1.update(workDayAveragePop, weekEndAveragePop, queryset2)
        
        data_pd = pd.DataFrame(queryset1, index=[0])
        
        
        final_model = load_model("analysis/aimodel/market_service_pred_model2")
        prediction = predict_model(final_model, data = data_pd)
        result = prediction['prediction_label']
        
        return Response({"success":result}, status=status.HTTP_200_OK)
 

    
    