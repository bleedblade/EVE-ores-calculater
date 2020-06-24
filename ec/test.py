# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 17:57:37 2020

@author: qy
"""

# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render
from lpsolve55 import *
from lp_maker import *
import math
import requests
import json
from django.core.cache import cache
# 表单
def ec1(request):
    return render(request,'ec1.html')
 
# 接收请求数据
def ec2(request):  
    '''
    min aikenuoyan + heizheshi + huiyan + keluojishi + shuangduoteshi + pianmayan
    
    aikenuoyan = 22000santaihejin + 2500leiyin + 320chaoshikuang  28367
    heizheshi = 10000santaihejin + 1600tongweijuheti + 120chaoxinxing  28394
    huiyan = 56000santaihejin + 450tongweijuheti + 12050leijingti + 2100leiyin  28420
    keluojishi = 21000santaihejin + 135jingzhuangshiying + 760chaoxinxing  28391
    shuangduoteshi = 450jingzhuangshiying +12000leijingti  28388
    pianmayan = 300tongweijuheti + 2200leijingti + 2400leiyin  28397
    
    22000aikenuoyan + 10000heizheshi + 56000huiyan + 2100keluojishi >=
    1600heizheshi + 450huiyan + 300pianmayan >=
    135keluojishi + 450shuangduoteshi >=
    12050huiyan + 12000shuangduoteshi + 2200pianmayan >=
    2500aikenuoyan + 2100huiyan + 2400pianmayan >=
    320aikenuoyan + 100shuangduoteshi >=
    120heizheshi + 760keluojishi >=
    '''
    request.encoding='utf-8'
    #获取前端选择的参与计算的矿石checkbox拼接字符串
    kuangs=request.POST['kuang']
    kl1=[ int(x) for x in kuangs.split(",") ]

    kuangname=["希莫非特Hemorphite","水硼砂Kernite","奥贝尔石Omber","斜长岩Plagioclase","干焦岩Pyroxeres","灼烧岩Scordite","凡晶石Veldspar","同位原矿Hedbergite","杰斯贝矿Jaspet","艾克诺岩Arkonor","黑赭石Dark Ochre","灰岩Spodumain","克洛基石Crokite","双多特石Bistot","片麻岩Gneiss"]
    kuanglian={
            "希莫非特Hemorphite":[2200,100,15,0,0,0,120],
            "水硼砂Kernite":[134,134,0,0,267,0,0],
            "奥贝尔石Omber":[800,85,0,100,0,0,0],
            "斜长岩Plagioclase":[107,0,0,213,107,0,0],
            "干焦岩Pyroxeres":[351,0,0,25,50,0,5],
            "灼烧岩Scordite":[346,0,0,173,0,0,0],
            "凡晶石Veldspar":[415,0,0,0,0,0,0],
            "同位原矿Hedbergite":[0,200,19,1000,0,0,100],
            "杰斯贝矿Jaspet":[0,0,8,0,350,0,75],
            "艾克诺岩Arkonor":[22000,0,0,0,2500,320,0],
            "黑赭石Dark Ochre":[10000,1600,0,0,0,0,120],
            "灰岩Spodumain":[56000,450,0,12050,2100,0,0],
            "克洛基石Crokite":[21000,0,135,0,0,0,750],
            "双多特石Bistot":[0,0,450,12000,0,100,0],
            "片麻岩Gneiss":[0,300,0,2200,2400,0,0]
            }
    kuanglianlist=[]
    for i in kuangname:
        kuanglianlist.append(kuanglian[i])
        
    kl2=[]#用来获取各个所需矿石的精炼列表
    for i in kl1:
        kl2.append(kuanglian[kuangname[i]])

    
    daijinglian=[[],[],[],[],[],[],[]]
    for i in range(0,7):
        for j in kl2:
            daijinglian[i].append(j[i])
    print(daijinglian)
 
    #这里需要改成xx key and xx key
    kuangpricelist=[]
    kuangidlist=[28403,28410,28416,28422,28424,28429,28432,28401,28406,28367,28394,28420,28391,28388,28397]
    kuangpricelistall=['','','','','','','','','','','','','','','']
    for i in kl1:
        is_cache=cache.get(kuangname[i])
        if(is_cache):
            kuangpricelist.append(is_cache)
            kuangpricelistall[i]=is_cache
        else:
            req_url='https://api.evemarketer.com/ec/marketstat/json?typeid='+str(kuangidlist[i])+'&regionlimit=10000002'
            req=requests.get(req_url) #发送请求
            rt=req.text  #获取响应信息
            itemPriceInfo=json.loads(rt)  #将JSON str转换为原格式，此处为list格式
            itemBuy=itemPriceInfo[0]['buy']['max']  #获取jita buy最高价
            kuangpricelist.append(itemBuy)
            cache.set(kuangname[i],itemBuy,600)
            kuangpricelistall[i]=itemBuy

    print(kuangpricelist)
    
    '''
    n_santaihejin = 774565133
    n_tongweijuheti = 10489443
    n_jingzhuangshiying = 1091619
    n_leijingti = 183660168
    n_leiyin = 72099790
    n_chaoshikuang = 431586
    n_chaoxinxing = 2951669
    '''
    n_santaihejin=int(request.POST['santai'])
    n_tongweijuheti=int(request.POST['tongwei'])
    n_jingzhuangshiying=int(request.POST['jingzhuang'])
    n_leijingti=int(request.POST['leijing'])
    n_leiyin=int(request.POST['leiyin'])
    n_chaoshikuang=int(request.POST['chaoshi'])
    n_chaoxinxing=int(request.POST['chaoxin'])
    
    

    
    #获取到输入的矿物需求，接下来加上旗舰组件的数据
    #旗舰组件矿数量
    qj0=['457050', '6938', '604', '110416', '41994', '302', '2110']
    qj1=['546912', '7760', '876', '113826', '45010', '386', '2358']
    qj2=['443591', '6659', '666', '101026', '40877', '298', '1804']
    qj3=['473141', '7109', '682', '111118', '43324', '304', '2141']
    qj4=['326973', '6440', '660', '107842', '39547', '280', '1841']
    qj5=['510149', '7491', '728', '110413', '45621', '334', '2191']
    qj6=['498880', '7269', '696', '104957', '43194', '332', '2033']
    qj7=['749916', '8617', '908', '142710', '49913', '444', '2249']
    qj8=['347163', '4499', '486', '83248', '33332', '172', '1258']
    qj9=['427708', '6581', '648', '111110', '44110', '296', '1858']
    qj10=['388208', '5104', '538', '93777', '37729', '212', '1530']
    qj11=['1121659', '17669', '1488', '278776', '75379', '1134', '4176']
    qj12=['640393', '8888', '1082', '139591', '48471', '444', '2612']
    qj13=['841877', '11132', '1108', '207776', '61980', '572', '3317']
    qj14=['555658', '7916', '908', '125277', '47249', '428', '2438']
    qj15=['576759', '9010', '914', '189942', '53312', '416', '2461']
    qj16=['583442', '9321', '938', '145664', '51297', '436', '2678']
    qj17=['874902', '3504', '286', '72154', '24616', '64', '998']
    qjksl=[qj0,qj1,qj2,qj3,qj4,qj5,qj6,qj7,qj8,qj9,qj10,qj11,qj12,qj13,qj14,qj15,qj16,qj17]
    #旗舰组件所需数量
    q0=int(request.POST['qj0'])
    q1=int(request.POST['qj1'])
    q2=int(request.POST['qj2'])
    q3=int(request.POST['qj3'])
    q4=int(request.POST['qj4'])
    q5=int(request.POST['qj5'])
    q6=int(request.POST['qj6'])
    q7=int(request.POST['qj7'])
    q8=int(request.POST['qj8'])
    q9=int(request.POST['qj9'])
    q10=int(request.POST['qj10'])
    q11=int(request.POST['qj11'])
    q12=int(request.POST['qj12'])
    q13=int(request.POST['qj13'])
    q14=int(request.POST['qj14'])
    q15=int(request.POST['qj15'])
    q16=int(request.POST['qj16'])
    q17=int(request.POST['qj17'])
    qjsl=[q0,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17]
    
    #旗舰需要的矿物先清零
    qn_santaihejin=0
    qn_tongweijuheti=0
    qn_jingzhuangshiying=0
    qn_leijingti=0
    qn_leiyin=0
    qn_chaoshikuang=0
    qn_chaoxinxing=0
    
    for i in range(0,18):
        qn_santaihejin = qn_santaihejin + int(qjksl[i][0])*int(qjsl[i])
        qn_tongweijuheti = qn_tongweijuheti + int(qjksl[i][1])*int(qjsl[i])
        qn_jingzhuangshiying = qn_jingzhuangshiying + int(qjksl[i][2])*int(qjsl[i])
        qn_leijingti = qn_leijingti + int(qjksl[i][3])*int(qjsl[i])
        qn_leiyin = qn_leiyin + int(qjksl[i][4])*int(qjsl[i])
        qn_chaoshikuang = qn_chaoshikuang + int(qjksl[i][5])*int(qjsl[i])
        qn_chaoxinxing = qn_chaoxinxing + int(qjksl[i][6])*int(qjsl[i])
    
    #加上旗舰组件之后，目前n_为未减免前所有需要的矿物
    #接下来计算图纸和建筑插、建筑减免
    tuzhicailiao=int(request.POST['tuzhicailiao'])
    jianzhucha=float(request.POST['jianzhucha'])
    jianzhu=int(request.POST['jianzhu'])
    #计算出最终旗舰减免
    jianmian=(100-tuzhicailiao)/100*(100-jianzhu)/100*(100-jianzhucha)/100
    
    qn_santaihejin = math.ceil(qn_santaihejin * jianmian)
    qn_tongweijuheti = math.ceil(qn_tongweijuheti * jianmian)
    qn_jingzhuangshiying = math.ceil(qn_jingzhuangshiying * jianmian)
    qn_leijingti = math.ceil(qn_leijingti * jianmian)
    qn_leiyin = math.ceil(qn_leiyin * jianmian)
    qn_chaoshikuang = math.ceil(qn_chaoshikuang * jianmian)
    qn_chaoxinxing = math.ceil(qn_chaoxinxing * jianmian)
    
    #通过精炼率计算出化矿产物
    jinglianlv=float(request.POST['jinglianlv'])/100
    
    #减去已有的矿石数量
    hk0=int(request.POST['h_kuang0'])
    hk1=int(request.POST['h_kuang1'])
    hk2=int(request.POST['h_kuang2'])
    hk3=int(request.POST['h_kuang3'])
    hk4=int(request.POST['h_kuang4'])
    hk5=int(request.POST['h_kuang5'])
    hk6=int(request.POST['h_kuang6'])
    hk7=int(request.POST['h_kuang7'])
    hk8=int(request.POST['h_kuang8'])
    hk9=int(request.POST['h_kuang9'])
    hk10=int(request.POST['h_kuang10'])
    hk11=int(request.POST['h_kuang11'])
    hk12=int(request.POST['h_kuang12'])
    hk13=int(request.POST['h_kuang13'])
    hk14=int(request.POST['h_kuang14'])
    havekuanglist=[hk0,hk1,hk2,hk3,hk4,hk5,hk6,hk7,hk8,hk9,hk10,hk11,hk12,hk13,hk14]
    h_santaihejin = 0
    h_tongweijuheti = 0
    h_jingzhuangshiying = 0
    h_leijingti = 0
    h_leiyin = 0
    h_chaoshikuang = 0
    h_chaoxinxing = 0
    for i in range(0,15):          
        h_santaihejin = h_santaihejin + math.floor(havekuanglist[i]*kuanglianlist[i][0]*jinglianlv)
        h_tongweijuheti = h_tongweijuheti + math.floor(havekuanglist[i]*kuanglianlist[i][1]*jinglianlv)
        h_jingzhuangshiying = h_jingzhuangshiying + math.floor(havekuanglist[i]*kuanglianlist[i][2]*jinglianlv)
        h_leijingti = h_leijingti + math.floor(havekuanglist[i]*kuanglianlist[i][3]*jinglianlv)
        h_leiyin = h_leiyin + math.floor(havekuanglist[i]*kuanglianlist[i][4]*jinglianlv)
        h_chaoshikuang = h_chaoshikuang + math.floor(havekuanglist[i]*kuanglianlist[i][5]*jinglianlv)
        h_chaoxinxing = h_chaoxinxing + math.floor(havekuanglist[i]*kuanglianlist[i][6]*jinglianlv)
    
    
    #至此得到最终所需矿物
    n_santaihejin = n_santaihejin + qn_santaihejin - h_santaihejin
    n_tongweijuheti = n_tongweijuheti + qn_tongweijuheti - h_tongweijuheti
    n_jingzhuangshiying = n_jingzhuangshiying + qn_jingzhuangshiying - h_jingzhuangshiying
    n_leijingti = n_leijingti + qn_leijingti - h_leijingti
    n_leiyin = n_leiyin + qn_leiyin - h_leiyin
    n_chaoshikuang = n_chaoshikuang + qn_chaoshikuang - h_chaoshikuang
    n_chaoxinxing = n_chaoxinxing + qn_chaoxinxing - h_chaoxinxing
    
    
    
    

    A=[[],[],[],[],[],[],[]]
    #A在最开始获取选取的矿石时已定义
    for i in range(len(daijinglian)):
        for j in range(len(daijinglian[i])):
            A[i].append(math.floor(daijinglian[i][j]*jinglianlv))
    print(A)
            
    l=[]
    for i in range(len(kl1)):
        l.append(0)

    #以最少花费计算
    f=kuangpricelist
    #以最少矿石数量计算
    #f=[1,1,1,1,1,1]
    #列表A在上面的精炼计算区域已经定义了
    #A=[[22000,10000,56000,2100,0,0],[0,1600,450,0,0,300],[0,0,0,135,450,0],[0,0,12050,0,12000,2200],[2500,0,2100,0,0,2400],[320,0,0,0,100,0],[0,120,0,760,0,0]]
    b=[n_santaihejin,n_tongweijuheti,n_jingzhuangshiying,n_leijingti,n_leiyin,n_chaoshikuang,n_chaoxinxing]
    e=[1,1,1,1,1,1,1]#全大于
    #l=[0,0,0,0,0,0]#最小值
    
    lp=lp_maker(f,A,b,[1,1,1,1,1,1,1],l,None,None,1,1)
    #set_int(lp,1,TRUE)
    solvestat = lpsolve('solve', lp)
    y = lpsolve('get_variables', lp)[0]
    x=[]
    if(isinstance(y,list)):
        x=y
    else:
        x.append(y)
    print(x)
    #将规划好的数据向上取整，得到各高密度矿石数量
    for i in range(len(x)):
        x[i] = math.ceil(x[i])
    
    #这个answer变量好像没用上，本意是最终所有矿石的结果和所有矿石的价格表遍历相乘，但是后来使用了最终结果的x列表和指定矿石的价格。
    answer=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(kl1)):   
        answer[kl1[i]]=int(x[i])
    
    '''
    #这里获取输入的已有矿石数量，要求格式：名字-数量-组
    tas="""三晶双多特斜岩	79	双多特石
    三钛合金	52	矿物
    三钛合金	7,064,097	矿物"""
    tasp=tas.split("\n")
    print(tasp)
    tasd={}
    for i in range(len(tasp)):
        tasp[i]=tasp[i].split("\t")
        tasp[i]=tasp[i][1:3]
        tasp[i]=tasp[i][::-1]
        print(tasp[i])
        key = tasp[i][0]
        if key in tasd:
            tasd[key]+=int(tasp[i][1].replace(',',''))
        else:
            tasd[key]=int(tasp[i][1].replace(',',''))
    
    print(tasd)
    
    if '艾克诺岩' in tasd:
        x[0]=x[0]-tasd['艾克诺岩']
    if '黑赭石' in tasd:
        x[1]=x[1]-tasd['黑赭石']
    if '灰岩' in tasd:
        x[2]=x[2]-tasd['灰岩']    
    if '克洛基石' in tasd:
        x[3]=x[3]-tasd['克洛基石'] 
    if '双多特石' in tasd:
        x[4]=x[4]-tasd['双多特石']
    if '片麻岩' in tasd:
        x[5]=x[5]-tasd['片麻岩']
    #这里算好最后需要的矿石数量
    '''
    
    
    #f_ = h_ + anwser[]
    f_santaihejin = h_santaihejin
    f_tongweijuheti = h_tongweijuheti
    f_jingzhuangshiying = h_jingzhuangshiying
    f_leijingti = h_leijingti
    f_leiyin = h_leiyin
    f_chaoshikuang = h_chaoshikuang
    f_chaoxinxing = h_chaoxinxing
    for i in range(0,15):
        f_santaihejin = f_santaihejin + math.floor(answer[i]*kuanglianlist[i][0]*jinglianlv)
        f_tongweijuheti = f_tongweijuheti + math.floor(answer[i]*kuanglianlist[i][1]*jinglianlv)
        f_jingzhuangshiying = f_jingzhuangshiying + math.floor(answer[i]*kuanglianlist[i][2]*jinglianlv)
        f_leijingti = f_leijingti + math.floor(answer[i]*kuanglianlist[i][3]*jinglianlv)
        f_leiyin = f_leiyin + math.floor(answer[i]*kuanglianlist[i][4]*jinglianlv)
        f_chaoshikuang = f_chaoshikuang + math.floor(answer[i]*kuanglianlist[i][5]*jinglianlv)
        f_chaoxinxing = f_chaoxinxing + math.floor(answer[i]*kuanglianlist[i][6]*jinglianlv)
    
    cost=0
    for i in range(len(kuangpricelist)):
        #cost = cost + answer[i]*kuangpricelist[i]
        cost = cost + x[i]*kuangpricelist[i]
    

    
    
    context={}
    #名字数组kuangname，answer,havekuanglist,kuangpricelistall
    context["kuang"]=list(zip(kuangname,answer,havekuanglist,kuangpricelistall))
    
    
    context['cost']=format(cost,',')

    context['n_santai']=n_santaihejin
    context['n_tongwei']=n_tongweijuheti
    context['n_jingzhuang']=n_jingzhuangshiying
    context['n_leijing']=n_leijingti
    context['n_leiyin']=n_leiyin
    context['n_chaoshi']=n_chaoshikuang
    context['n_chaoxin']=n_chaoxinxing
    context['f_santai']=f_santaihejin
    context['f_tongwei']=f_tongweijuheti
    context['f_jingzhuang']=f_jingzhuangshiying
    context['f_leijing']=f_leijingti
    context['f_leiyin']=f_leiyin
    context['f_chaoshi']=f_chaoshikuang
    context['f_chaoxin']=f_chaoxinxing
    context['m_santai']=f_santaihejin-n_santaihejin
    context['m_tongwei']=f_tongweijuheti-n_tongweijuheti
    context['m_jingzhuang']=f_jingzhuangshiying-n_jingzhuangshiying
    context['m_leijing']=f_leijingti-n_leijingti
    context['m_leiyin']=f_leiyin-n_leiyin
    context['m_chaoshi']=f_chaoshikuang-n_chaoshikuang
    context['m_chaoxin']=f_chaoxinxing-n_chaoxinxing
    
    return render(request, 'ec2.html', context)

