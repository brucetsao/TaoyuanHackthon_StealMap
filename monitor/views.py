from django.shortcuts import render_to_response
from django.template import RequestContext
from urllib.request import urlopen
import xmltodict
import datetime

# Create your views here.
def monitor_index(request):
    ###########################照明度###################################
    from datetime import date
    holiday = createHoliday()
    today = date.today()
    isHoliday = 0
    isHolidayStr = "否"
    try:
        holiday.index(today)
        isHoliday = 100
        isHolidayStr = "是"
    except:
        pass



    ###########################照明度###################################
    light = getLight()

    ###########################溫度###################################
    try:
        temperature = getWeather('http://data.gov.tw/iisi/logaccess/3539?dataUrl=http://opendata.cwb.gov.tw/govdownload?dataid=O-A0003-001&authorizationkey=rdec-key-123-45678-011121314&ndctype=XML&ndcnid=9178')
    except:
        temperature = '24.6'

    ############################降雨情形###################################

    rainforcastXML = "http://data.gov.tw/iisi/logaccess/159?dataUrl=http://opendata.cwb.gov.tw/govdownload?dataid=F-C0032-001&authorizationkey=rdec-key-123-45678-011121314&ndctype=XML&ndcnid=6069"
    rainForcast = ['天氣晴朗',10]
    try:
        rainForcast = getRainForcast(rainforcastXML)
    except:
        pass
    return render_to_response('Monitor/index.html', locals(),RequestContext(request))

def page_data(request):
    return  render_to_response('Data.html',locals())

def getLight():
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=+8)
    hour = t.hour

    light = []

    if hour >= 18 and hour <= 22 :
        light.append('夜晚')
        light.append('30')
    elif (hour > 22 and hour <= 24) and (hour>=0 and hour <=5):
        light.append('深夜')
        light.append('0')
    elif hour>5 and hour <=11:
        light.append('早晨')
        light.append('60')
    elif hour>11 and hour <=13:
        light.append('中午')
        light.append('80')
    elif hour>13 and hour <18:
        light.append('下午')
        light.append('60')
    else:
        pass
    return  light

def getWeather(xmlPath):
    file = urlopen(xmlPath)
    data = file.read()
    file.close()

    data = xmltodict.parse(data)

    # list = data["cwbopendata"]["location"][39].items()
    list = data["cwbopendata"]["location"][39].items()
    listTmp = []
    for k, v in list:
        listTmp.append(v)

    temperature = 0
    try:
        temperature = listTmp[5][4]['elementValue']['value']
    except:
        temperature = 24.6
    #listTmp[5][4]  OrderedDict([('elementName', 'TEMP'), ('elementValue', OrderedDict([('value', '25.8')]))])
    # listTmp[5][4]['elementValue']['value']  ======> Finally got value 25.8
    return temperature

def getRainForcast(rainforcastXML):
    file = urlopen(rainforcastXML)
    data = file.read()
    file.close()

    data = xmltodict.parse(data)

    weatherCondition = []
                        #[0]:狀態 [1]顯示數值

    list = data["cwbopendata"]["dataset"]["location"][2]
    try:
        tmpResult = list['weatherElement'][0]['time'][0]['parameter']['parameterName']
        weatherCondition.append(tmpResult)
        if tmpResult.find("雷雨") >= 0:
            weatherCondition.append(80)
        elif tmpResult.find("雨"):
            weatherCondition.append(60)
        else:
            weatherCondition.append(10)
    except:
        weatherCondition.append('天氣晴朗')
        weatherCondition.append('10')
    return weatherCondition

def createHoliday():
    from datetime import date
    holiday = []
    holiday.append(date(2016, 1, 1))
    holiday.append(date(2016, 1, 2))
    holiday.append(date(2016, 1, 3))
    holiday.append(date(2016, 2, 6))
    holiday.append(date(2016, 2, 7))
    holiday.append(date(2016, 2, 8))
    holiday.append(date(2016, 2, 9))
    holiday.append(date(2016, 2, 10))
    holiday.append(date(2016, 2, 11))
    holiday.append(date(2016, 2, 12))
    holiday.append(date(2016, 2, 13))
    holiday.append(date(2016, 2, 14))
    holiday.append(date(2016, 2, 27))
    holiday.append(date(2016, 2, 28))
    holiday.append(date(2016, 4, 2))
    holiday.append(date(2016, 4, 3))
    holiday.append(date(2016, 4, 5))
    holiday.append(date(2016, 6, 9))
    holiday.append(date(2016, 6, 10))
    holiday.append(date(2016, 6, 11))
    holiday.append(date(2016, 6, 12))
    holiday.append(date(2016, 9, 15))
    holiday.append(date(2016, 9, 16))
    holiday.append(date(2016, 9, 17))
    holiday.append(date(2016, 9, 18))
    holiday.append(date(2016, 10, 9))
    holiday.append(date(2016, 10, 10))
    holiday.append(date(2016, 10, 11))
    return holiday