from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from urllib.request import urlopen
import csv
import twd97
from game.models import UserInfo,Coupon,Window,HouseList
import psycopg2
import json
from urllib.request import urlopen
from urllib.parse import quote
from urllib.request import urlopen
import xmltodict
import datetime
# Create your views here.

def index(request):
    return render_to_response('index.html', locals(),RequestContext(request))

def one_story(request):
    try:
        address = request.POST['inputAddress']
        request.session['userAddress'] = address #設定session
    except MultiValueDictKeyError:
        inputName = False
        address = False

    if 'userName' in request.session:
        s_userName = request.session['userName']
    if 'userAddress' in request.session:
        s_userAddress = request.session['userAddress']

    return render_to_response('1_Story.html', locals(),RequestContext(request))

def two_story(request):
    return render_to_response('2_Story.html', locals(),RequestContext(request))

def three_story(request):
    return render_to_response('3_Story.html', locals(),RequestContext(request))

def four_question(request):
    return render_to_response('4_Question.html',locals(),RequestContext(request))

def five_analyze(request):
    try:
        request.session['inputWindows'] = request.POST.get('inputWindows')  # 設定session
        request.session['inputGuard'] = request.POST.get('inputGuard')  # 設定session
        request.session['inputBasement'] = request.POST.get('inputBasement')  # 設定session
        request.session['inputHouseType'] = request.POST.get('inputHouseType')  # 設定session
        request.session['inputAreaType'] = request.POST.get('inputAreaType')  # 設定session
        request.session['inputLocal'] = request.POST.get('inputLocal')

    except:
        request.session['inputWindows'] = "0"  # 設定session
        request.session['inputGuard'] = "0"  # 設定session
        request.session['inputBasement'] = "1"  # 設定session
        request.session['inputHouseType'] = "公寓"  # 設定session
        request.session['inputAreaType'] = "住宅區"  # 設定session
        request.session['inputLocal'] = "中壢區中央里"

    #住家本身防衛度



    return render_to_response('5_Analyze.html',locals(),RequestContext(request))

def six_output(request):

    ########

    # 鐵窗
    if request.session['inputWindows'] == "1":
        windows = "低"
        windowsSuggest = "安裝鐵窗可加強防竊，但須注意災害逃生。"
    else:
        windows = "高"
        windowsSuggest = "建議可加裝鐵窗防範宵小，並請廠商焊接確實，以免遭剪斷抽杆。"

    if request.session['inputGuard'] == "1":
        guard = "低"
        guardSuggest = "雖有保全，仍須注意住家安全。"
    else:
        guard = "高"
        guardSuggest = "若非社區型住宅無保全，可建議加裝保全系統"

    if request.session['inputBasement'] == "1":
        base = "高"
        baseSuggest = "地下室易成為竊盜出入口，敬請小心防範。"
    else:
        base = "低"
        baseSuggest = "無"

    if request.session['inputHouseType'] == "獨棟":
        houseType = "中"
        houseTypeSuggest = "獨棟住宅建議可加裝警報器或監視器，防範宵小。"
    elif request.session['inputHouseType'] == "公寓":
        houseType = "高"
        houseTypeSuggest = "超過十年之公寓容易成為宵小下手的目標，應和鄰居守望相助，隨時注意出入公寓的人員。"
    else:
        houseType = "低"
        houseTypeSuggest = "社區住宅即使有保全也可能讓宵小混入，建議可請出入廠商訪客穿著識別背心。"

    if request.session['inputAreaType'] == "住商混合":
        areaType = "中"
        areaTypeSuggest = "住商混合住宅區出入人口較複雜，須加強防範。"
    elif request.session['inputAreaType'] == "商業區":
        areaType = "高"
        areaTypeSuggest = "商業區晚上較少人居住，因此容易成為宵小目標，應加強防範。"
    elif request.session['inputAreaType'] == "住宅區":
        areaType = "低"
        areaTypeSuggest = "住宅區雖相對安全，夜間應檢查門鎖是否確實鎖上。"
    else:
        houseType = "高"  # 工業區
        areaTypeSuggest = "工業區工廠有許多高價產品，更應注意建築安全。"


    if request.session['inputLocal'] == "中壢區中央里":
        loaclType = "中"
        localTypeSuggest = "您的住家有中度的失竊風險，應加強防範。"
    else:
        loaclType = "低"
        localTypeSuggest = "您的住家有低度的失竊風險，應加強防範。"
    #######

    conn = psycopg2.connect(database="taoyuangis", user="postgres", password=“tp6ful3mp6”, host="127.0.0.1",
                            port="5432")
    cur = conn.cursor()
    cur2 = conn.cursor()
    #先將地址從中文轉成英文，然後再轉成一般經緯度

    addr = request.session['userAddress']
    googleApi = "http://maps.googleapis.com/maps/api/geocode/json?address="+quote(addr)+"&sensor=false&language=zh-tw"


    try:
        u = urlopen(googleApi)
        resp = json.loads(u.read().decode('utf-8'))
        lat = resp['results'][0]['geometry']['location']['lat']
        long = resp['results'][0]['geometry']['location']['lng']
        request.session['lat'] = lat
        request.session['long'] = long
    except:
        request.session['lat'] = 24.9446592
        request.session['long'] = 121.2943169
    # 將地址轉換成二分法的TWD 97 TM，就跟CSV的X,Y一致了
    # twd97.towgs84(248170.787, 2652129.936)
    #print(twd97.fromwgs84(location.latitude, location.longitude))



    ###############################路燈###############################

    #接下來計算（方圓50M內是否有路燈）
    lightList = []

    selectSqlLight = "SELECT *  FROM pointslight WHERE ST_DWithin(  ST_Transform(ST_GeomFromText('POINT(%(lat)s %(long)s)',3826),26986), ST_Transform(location,26986), 300) ORDER BY ST_Distance(ST_GeomFromText('POINT(%(lat)s %(long)s)',3826), location);"
    # selectSqlLight = "SELECT *  FROM pointslight WHERE ST_DWithin(  ST_Transform(ST_GeomFromText('POINT(2759680.13418412 279721.29349234176',3826),26986), ST_Transform(location,26986), 1000) ORDER BY ST_Distance(ST_GeomFromText('POINT(2759680.13418412 279721.29349234176)',3826), location);"

    try:
        localTM2 = twd97.fromwgs84(lat,long)
    except:
        localTM2 = twd97.fromwgs84(24.9446592,121.2943169)

    try:
        cur2.execute(selectSqlLight, {'long': localTM2[0], 'lat': localTM2[1]})
    except:
        cur2.execute(selectSqlLight, {'long': 279721.29349234176, 'lat': 2759680.13418412})
    lightList = []
    rows2 = cur2.fetchall()
    for row in rows2:
        if row[1] != "":
            lightList.append(row[1])

    lightCount = len(lightList)
    request.session['lightCount'] = lightCount
    ###############################監視器###############################

    #方圓50米是否有監視器


    cameraList = []
    #select_stmt = "SELECT * FROM employees WHERE emp_no = %(emp_no)s" 參考用

    selectSql = "SELECT * FROM points WHERE ST_DWithin( ST_Transform(ST_GeomFromText('POINT(%(long)s %(lat)s)', 4326), 26986), ST_Transform(location, 26986), 100) ORDER BY ST_Distance(ST_GeomFromText('POINT(%(long)s %(lat)s)',4326), location);"

    try:
        cur.execute(selectSql, {'long': long, 'lat': lat})
    except:
        cur.execute(selectSql, {'long': 121.2943169, 'lat': 24.9446592})
                                #(279721.29349234176, 2759680.13418412)
    #cur.execute('''SELECT * FROM points WHERE ST_DWithin( ST_Transform(ST_GeomFromText('POINT(121.2943169 24.9446592)', 4326), 26986), ST_Transform(location, 26986), 50) , location);''')
    rows = cur.fetchall()
    for row in rows:
        if row[1] != "":
            cameraList.append(row[1])

    cameraCount = len(cameraList)
    request.session['cameraCount'] = cameraCount


    ###############################監視器###############################

    return render_to_response('6_Output.html', locals(),RequestContext(request))

def seven_suggest(request):
    s_guard = ''
    if 'inputGuard' in request.session:
        s_guard = request.session['inputGuard']
    if 'inputWindows' in request.session:
        s_window = request.session['inputWindows']
    if 'cameraCount' in request.session:
        s_camera = request.session['cameraCount']
    if 'lightCount' in request.session:
        s_light = request.session['lightCount']
    suggestList = []
    #保全
    if s_guard == '0':
        #suggest
        tmpSuggest = Suggest('加裝保全系統','page_guard_info','Guard')
        suggestList.append(tmpSuggest)
    #鐵窗
    if s_window == '0':
        #suggest
        tmpSuggest = Suggest('加裝鐵窗','page_window_info','Window')
        suggestList.append(tmpSuggest)
    #公所/鄰里
    if s_camera  == '0':
        #suggest
        tmpSuggest = Suggest('向里長建議加裝監視器','page_officer_info','Officer')
        suggestList.append(tmpSuggest)

    if s_light  == '0':
        #suggest
        tmpSuggest = Suggest('向里長建議加裝路燈','page_officer_info','Officer')
        suggestList.append(tmpSuggest)


    return render_to_response('7_Suggest.html',locals(),RequestContext(request))

def eight_success(request):
    if 'userName' in request.session:
        s_userName = request.session['userName']
    else:
        s_userName = 'hatsukiotowa'

    userObj = UserInfo.objects.get(name=s_userName)
    newHouseCount = userObj.countHouse+1
    userObj.countHouse=newHouseCount
    userObj.save()

    if 'userAddress' in request.session:
        s_userAddress = request.session['userAddress']
    else:
        s_userAddress = '桃園市八德區廣福路200號'

    h = HouseList(address=s_userAddress, status='成功防禦')
    h.save()


    return  render_to_response('8_Success.html',locals(),RequestContext(request))

def nine_coupon(request):
    if 'userName' in request.session:
        s_userName = request.session['userName']
    else:
        s_userName = 'hatsukiotowa'

    userObj = UserInfo.objects.get(name=s_userName)
    houseTotal = userObj.countHouse
    couponList = Coupon.objects.all()
    return render_to_response('9_Coupon.html',locals(),RequestContext(request))

def personnel(request):
    return render_to_response('Personnel.html',locals(),RequestContext(request))

def page_QRCode(request):
    return  render_to_response('QRCode.html',locals())

def page_guard_info(request):
    try:
        s_lat = request.session['lat']
        s_long = request.session['long']
    except:
        s_lat = 24.9446592
        s_long = 121.2943169
    guardList = getGuardInfo("/Users/hatsukiotowa/PycharmProjects/StealMap0924/static/file/guardTaoyuan.csv")
    return render_to_response("Suggest/GuardInfo.html",locals())

def page_officer_info(request):
    try:
        s_lat = request.session['lat']
        s_long = request.session['long']
    except:
        s_lat = 24.9446592
        s_long = 121.2943169
    officerList = getOfficerInfo("/Users/hatsukiotowa/PycharmProjects/StealMap0924/static/file/officerTaoyuan.csv")
    return render_to_response("Suggest/OfficerInfo.html",locals())

def page_light_info(request):
    try:
        s_lat = request.session['lat']
        s_long = request.session['long']
    except:
        s_lat = 24.9446592
        s_long = 121.2943169
    return render_to_response("Suggest/LightInfo.html",locals())

def page_window_info(request):
    try:
        s_lat = request.session['lat']
        s_long = request.session['long']
    except:
        s_lat = 24.9446592
        s_long = 121.2943169
    windowList = Window.objects.all()
    return render_to_response("Suggest/WindowInfo.html",locals())

def page_camera_info(request):
    try:
        s_lat = request.session['lat']
        s_long = request.session['long']
    except:
        s_lat = 24.9446592
        s_long = 121.2943169
    windowList = Window.objects.all()
    return render_to_response("Suggest/CameraInfo.html",locals())

def page_map(request):
    try:
        s_lat = request.session['lat']
        s_long = request.session['long']
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
            temperature = getWeather(
                'http://data.gov.tw/iisi/logaccess/3539?dataUrl=http://opendata.cwb.gov.tw/govdownload?dataid=O-A0003-001&authorizationkey=rdec-key-123-45678-011121314&ndctype=XML&ndcnid=9178')
        except:
            temperature = '24.6'

        ############################降雨情形###################################

        rainforcastXML = "http://data.gov.tw/iisi/logaccess/159?dataUrl=http://opendata.cwb.gov.tw/govdownload?dataid=F-C0032-001&authorizationkey=rdec-key-123-45678-011121314&ndctype=XML&ndcnid=6069"
        rainForcast = ['天氣晴朗', 10]
        try:
            rainForcast = getRainForcast(rainforcastXML)
        except:
            pass
    except:
        s_lat = 24.9446592
        s_long = 121.2943169

    return render_to_response("Map.html",locals())

def page_login(request):

    return render_to_response("Login.html", locals(),RequestContext(request))

def action_login(request):
    try:
        tmpName = request.POST['inputAccount']
        userObj = UserInfo.objects.get(name=tmpName)
        request.session['title'] = userObj.title  # 設定session
        request.session['countHouse'] = userObj.countHouse  # 設定session
        request.session['user'] = userObj.name  # 設定session
    except:
        UserInfo.objects.create(name=tmpName, title='Novice', countHouse=0)
        userObj = UserInfo.objects.get(name=tmpName)
        request.session['title'] = userObj.title  # 設定session
        request.session['countHouse'] = userObj.countHouse  # 設定session
        request.session['user'] = userObj.name  # 設定session


    currentHouseCount = request.session['countHouse']

    return render_to_response("Main.html", locals())


def connect_postgre():
    conn = psycopg2.connect(database="taoyuangis", user="postgres", password=“tp6ful3mp6”, host="127.0.0.1", port="5432")


    cur = conn.cursor()

    cur.execute('''SELECT * FROM points;''')
    rows = cur.fetchall()


    for row in rows:
        print(row[1])

    conn.close()

###################################################################################

def getGuardInfo(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    #dataReader = csv.reader(open('/Users/hatsukiotowa/PycharmProjects/StealMap0924/static/file/guardTaoyuan.csv'), delimiter=',', quotechar='"')
    guardList = []
    for row in dataReader:
        if row[0] != '公司名稱':  # Ignore the header row, import everything else
            name = row[0]
            address = row[2]
            number = row[3]
            tmpGuard = Guard(name, number, address)
            guardList.append(tmpGuard)

    return  guardList



def getOfficerInfo(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')


    #dataReader = csv.reader(open('/Users/hatsukiotowa/PycharmProjects/StealMap0924/static/file/guardTaoyuan.csv'), delimiter=',', quotechar='"')
    officerList = []
    for row in dataReader:
        if row[0] != '姓名':  # Ignore the header row, import everything else
            name = row[0]
            address = row[4]+row[5]+row[7]
            number = row[8]
            cellphone = row[2]
            tmpOfficer = Officer(name, number, cellphone, address)
            officerList.append(tmpOfficer)

    return  officerList


class Guard:
    def __init__(self,name,number,address):
        self.name = name
        self.number = number
        self.address = address


    def __str__(self):
        return '保全公司：({0} ／ {1} ／{2})'.format(
            self.name, self.number, self.address)


class Officer:
    def __init__(self, name, number,cellphone, address):
        self.name = name
        self.number = number
        self.cellphone = cellphone
        self.address = address

class Suggest:
    def __init__(self,title,detailPage,engName):
        self.title = title
        self.detailPage = detailPage
        self.engName = engName




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