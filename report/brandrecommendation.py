import json
import math
import requests
from time import sleep
def RequestData(serviceURL, serviceKey, pageNo, numOfRows, resultType, year, additional = ''):
    url_req = f"http://apis.data.go.kr/{serviceURL}?serviceKey={serviceKey}&pageNo={pageNo}&numOfRows={numOfRows}&resultType={resultType}&yr={year}" + additional
    recieved_data = requests.get(url_req)
    if(recieved_data.status_code != 200):
        print(f"GET failed \n status code was : {recieved_data.status_code}")
        return -1
    try:
        data_json = json.loads(recieved_data.text)
    except:
        print(f"An error occured!\n {recieved_data.text}")
    
    return data_json

def GetBrandList(serviceKey, year):
    
    receivedData = RequestData(serviceURL='1130000/FftcBrandRlsInfoService/getBrandRlsInfo', serviceKey=serviceKey, pageNo = 1, numOfRows = 10000, resultType = 'json', year = year)
    
    numberOfPages = math.ceil(receivedData['totalCount']/10000)
    
    
    for pageNo in range(2, numberOfPages+1, 1):
        receivedData_nextPage = RequestData(serviceURL='1130000/FftcBrandRlsInfoService/getBrandRlsInfo', serviceKey = serviceKey, pageNo = pageNo, numOfRows = 10000, resultType = 'json', year = year)
        receivedData['items'].extend(receivedData_nextPage['items'])
    return receivedData

def GetBrandSetupCostInfo(serviceKey, year):
    
    receivedData = RequestData(serviceURL='1130000/FftcBrandFntnStatsService/getBrandFntnStats', serviceKey=serviceKey, pageNo = 1, numOfRows = 10000, resultType = 'json', year = year)
    
    numberOfPages = math.ceil(receivedData['totalCount']/10000)
    
    
    for pageNo in range(2, numberOfPages+1, 1):
        receivedData_nextPage = RequestData(serviceURL='1130000/FftcBrandFntnStatsService/getBrandFntnStats', serviceKey = serviceKey, pageNo = pageNo, numOfRows = 10000, resultType = 'json', year = year)
        receivedData['items'].extend(receivedData_nextPage['items'])
    return receivedData

def GetBrandProfitInfo(serviceKey, year):
    receivedData = RequestData(serviceURL = '1130000/FftcBrandFrcsStatsService/getBrandFrcsStats', serviceKey = serviceKey, pageNo = 1, numOfRows = 10000, resultType = 'json', year = year)
    
    numberOfPages = math.ceil(receivedData['totalCount']/10000)
    
    for pageNo in range(2, numberOfPages+1, 1):
        receivedData_nextPage = RequestData(serviceURL='1130000/FftcBrandFntnStatsService/getBrandFntnStats', serviceKey = serviceKey, pageNo = pageNo, numOfRows = 10000, resultType = 'json', year = year)
        receivedData['items'].extend(receivedData_nextPage['items'])
    
    return receivedData

def GetBrandInfo(serviceKey, year, jngIfrmpRgsno):
    receivedData = RequestData(serviceURL='1130000/FftcBrandCompInfoService/getBrandCompInfo', serviceKey=serviceKey, pageNo = 1, numOfRows = 10000, resultType = 'json', year = year, additional = f'&jngIfrmpRgsno={jngIfrmpRgsno}')
    return receivedData

def GetBrandCostInfo(serviceKey, year, registrationNumber, seedMoney):
    receivedData = []
    for number in registrationNumber:
        receivedData.append(RequestData(serviceURL = '/1130000/FftcBrandFrcsAlotmInfoService/getBrandFrcsAlotmInfo', serviceKey = serviceKey, pageNo = 1, numOfRows = 1, resultType = 'json', year = year, additional = f'&jngIfrmpRgsno={number}'))
    affordable = []
    for data in receivedData['items']:
        if data['smtnAmt'] <= seedMoney:
            affordable.append(data)
            
    sorted_list = sorted(affordable, key=lambda x: x['smtnAmt'], reverse=True)
    
    return sorted_list[:5]

def BrandFiltering(data, filteringParam, filteringKey, filteringWord):
    filteredData = []
    if type(filteringWord) == str:
        for item in data[filteringParam]:
            if item[filteringKey] == filteringWord:
                filteredData.append(item)
    else:
        for item in data[filteringParam]:
            if item[filteringKey] in filteringWord:
                filteredData.append(item)

    return filteredData

def BrandCostFiltering(data, filteringParam, filteringKey, filteringWord, costKey, seedMoney):
    filteredData = []
    if type(filteringWord) == str:
        for item in data[filteringParam] and data[costKey] <= seedMoney:
            if item[filteringKey] == filteringWord:
                filteredData.append(item)
    else:
        for item in data[filteringParam] and data[costKey] <= seedMoney:
            if item[filteringKey] in filteringWord:
                filteredData.append(item)

    return filteredData

def ExtractBrandName(data, brandNameKey = 'brandNm'):
    targetBrand = []
    
    for brand in data:
        targetBrand.append(brand[brandNameKey])
        
    return targetBrand

def RecommendBrand(apikey, year, seedMoney, business):
    brandList = GetBrandList(serviceKey = apikey, year = year)
    setupInfo = GetBrandSetupCostInfo(serviceKey = apikey, year = year)
    profitInfo = GetBrandProfitInfo(serviceKey = apikey, year = year)

    for i in range(setupInfo['totalCount']):
        if setupInfo['items'][i]['brandNm'] != profitInfo['items'][i]['brandNm']:
            print(i)
        else:
            setupInfo['items'][i].update(profitInfo['items'][i])

    filteredInfo = BrandFiltering(data = setupInfo, filteringParam = 'items', filteringKey = 'indutyMlsfcNm', filteringWord = business)
    filteredBrand = BrandFiltering(data = brandList, filteringParam = 'items', filteringKey = 'indutyMlsfcNm', filteringWord = business)

    affordableList = []
    for i in filteredInfo:
        if i['smtnAmt'] <= seedMoney and i['frcsCnt'] > 0:
            affordableList.append(i)


    for i in range(len(affordableList)):
        for j in range(len(filteredBrand)):
            if affordableList[i]['brandNm'] == filteredBrand[j]['brandNm']:
                affordableList[i].update(filteredBrand[j])
                break

    sorted_list = sorted(affordableList, key=lambda x: x['avrgSlsAmt'], reverse=True)
    output_list = sorted_list[:5].copy()

    return output_list
    # rank = 1
    # for brands in output_list:
    #     print(f" {rank} 위 업체_________________\n브랜드명 : {brands['brandNm']}\n가맹사명 : {brands['corpNm']}\n가맹업주 부담금(천원) : {brands['smtnAmt']}\n평균매출(천원) : {brands['avrgSlsAmt']}")
    #     rank += 1