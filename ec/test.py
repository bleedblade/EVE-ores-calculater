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
    
    #获取Evemarketer的矿石价格数据
    kuangpricelist=[]
    kuanglist=[28367,28394,28420,28391,28388,28397]
    for j in kuanglist:
        req_url='https://api.evemarketer.com/ec/marketstat/json?typeid='+str(j)+'&regionlimit=10000002'
        req=requests.get(req_url) #发送请求
        rt=req.text  #获取响应信息
        itemPriceInfo=json.loads(rt)  #将JSON str转换为原格式，此处为list格式
        itemBuy=itemPriceInfo[0]['buy']['max']  #获取jita buy最高价
        kuangpricelist.append(itemBuy)
    
    
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
    
    #至此得到最终所需矿物
    n_santaihejin = n_santaihejin + qn_santaihejin
    n_tongweijuheti = n_tongweijuheti + qn_tongweijuheti
    n_jingzhuangshiying = n_jingzhuangshiying + qn_jingzhuangshiying
    n_leijingti = n_leijingti + qn_leijingti
    n_leiyin = n_leiyin + qn_leiyin
    n_chaoshikuang = n_chaoshikuang + qn_chaoshikuang
    n_chaoxinxing = n_chaoxinxing + qn_chaoxinxing
    
    
    
    #通过精炼率计算出化矿产物
    jinglianlv=float(request.POST['jinglianlv'])
    jinglian=[[22000,10000,56000,2100,0,0],[0,1600,450,0,0,300],[0,0,0,135,450,0],[0,0,12050,0,12000,2200],[2500,0,2100,0,0,2400],[320,0,0,0,100,0],[0,120,0,760,0,0]]
    A=[[22000,10000,56000,2100,0,0],[0,1600,450,0,0,300],[0,0,0,135,450,0],[0,0,12050,0,12000,2200],[2500,0,2100,0,0,2400],[320,0,0,0,100,0],[0,120,0,760,0,0]]

    for i in range(len(jinglian)):
        for j in range(len(jinglian[i])):
            A[i][j]=jinglian[i][j]*jinglianlv
    print(A)
            
    
    #以最少花费计算
    f=[kuangpricelist[0],kuangpricelist[1],kuangpricelist[2],kuangpricelist[3],kuangpricelist[4],kuangpricelist[5]]
    #以最少矿石数量计算
    #f=[1,1,1,1,1,1]
    #列表A在上面的精炼计算区域已经定义了
    #A=[[22000,10000,56000,2100,0,0],[0,1600,450,0,0,300],[0,0,0,135,450,0],[0,0,12050,0,12000,2200],[2500,0,2100,0,0,2400],[320,0,0,0,100,0],[0,120,0,760,0,0]]
    b=[n_santaihejin,n_tongweijuheti,n_jingzhuangshiying,n_leijingti,n_leiyin,n_chaoshikuang,n_chaoxinxing]
    e=[1,1,1,1,1,1,1]
    l=[0,0,0,0,0,0]
    
    lp=lp_maker(f,A,b,[1,1,1,1,1,1,1],l,None,None,1,1)
    #set_int(lp,1,TRUE)
    solvestat = lpsolve('solve', lp)
    x = lpsolve('get_variables', lp)[0]
    print(x)
    #将规划好的数据向上取整，得到各高密度矿石数量
    for i in range(len(x)):
        x[i] = math.ceil(x[i])
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
    
    
    print("0艾克诺岩Arkonor："+str(x[0]))
    print("1黑赭石Dark Ochre："+str(x[1]))
    print("2灰岩Spodumain："+str(x[2]))
    print("3克洛基石Crokite："+str(x[3]))
    print("4双多特石 Bistot："+str(x[4]))
    print("5片麻岩 Gneiss ："+str(x[5]))
    
    
    f_santaihejin = A[0][0]*x[0] + A[0][1]*x[1] + A[0][2]*x[2] + A[0][3]*x[3]
    f_tongweijuheti = A[1][1]*x[1] + A[1][2]*x[2] + A[1][5]*x[5]
    f_jingzhuangshiying = A[2][3]*x[3] + A[2][4]*x[4]
    f_leijingti = A[3][2]*x[2] + A[3][4]*x[4] + A[3][5]*x[5]
    f_leiyin = A[4][0]*x[0] + A[4][2]*x[2] + A[4][5]*x[5]
    f_chaoshikuang = A[5][0]*x[0] + A[5][4]*x[4]
    f_chaoxinxing = A[6][1]*x[1] + A[6][3]*x[3]
    
    
    print("三钛合金Tritanium："+str(f_santaihejin)+"/"+str(n_santaihejin)+"，差值为：" + str(f_santaihejin-n_santaihejin))
    print("同位聚合体Isogen："+str(f_tongweijuheti)+"/"+str(n_tongweijuheti)+"，差值为：" + str(f_tongweijuheti-n_tongweijuheti))
    print("晶状石英Zydrine："+str(f_jingzhuangshiying)+"/"+str(n_jingzhuangshiying)+"，差值为：" + str(f_jingzhuangshiying-n_jingzhuangshiying))
    print("类晶体Pyerite："+str(f_leijingti)+"/"+str(n_leijingti)+"，差值为：" + str(f_leijingti-n_leijingti))
    print("类银Mexallon："+str(f_leiyin)+"/"+str(n_leiyin)+"，差值为：" + str(f_leiyin-n_leiyin))
    print("超噬矿Megacyte："+str(f_chaoshikuang)+"/"+str(n_chaoshikuang)+"，差值为：" + str(f_chaoshikuang-n_chaoshikuang))
    print("超新星Nocxium："+str(f_chaoxinxing)+"/"+str(n_chaoxinxing)+"，差值为：" + str(f_chaoxinxing-n_chaoxinxing))
    
    cost=x[0]*kuangpricelist[0]+x[1]*kuangpricelist[1]+x[2]*kuangpricelist[2]+x[3]*kuangpricelist[3]+x[4]*kuangpricelist[4]+x[5]*kuangpricelist[5]
    

    
    
    context={}
    context['aike']=x[0]
    context['heizhe']=x[1]
    context['huiyan']=x[2]
    context['keluo']=x[3]
    context['shuangduo']=x[4]
    context['pianma']=x[5]
    
    context['price0']=format(kuangpricelist[0],',')
    context['price1']=format(kuangpricelist[1],',')
    context['price2']=format(kuangpricelist[2],',')
    context['price3']=format(kuangpricelist[3],',')
    context['price4']=format(kuangpricelist[4],',')
    context['price5']=format(kuangpricelist[5],',')
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
