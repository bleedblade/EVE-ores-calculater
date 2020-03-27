
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
    n_santaihejin=int(request.GET['santai'])
    n_tongweijuheti=int(request.GET['tongwei'])
    n_jingzhuangshiying=int(request.GET['jingzhuang'])
    n_leijingti=int(request.GET['leijing'])
    n_leiyin=int(request.GET['leiyin'])
    n_chaoshikuang=int(request.GET['chaoshi'])
    n_chaoxinxing=int(request.GET['chaoxin'])
    
    
    
    #以最少花费计算
    #f=[kuangpricelist[0],kuangpricelist[1],kuangpricelist[2],kuangpricelist[3],kuangpricelist[4],kuangpricelist[5]]
    #以最少矿石数量计算
    f=[1,1,1,1,1,1]
    A=[[22000,10000,56000,2100,0,0],[0,1600,450,0,0,300],[0,0,0,135,450,0],[0,0,12050,0,12000,2200],[2500,0,2100,0,0,2400],[320,0,0,0,100,0],[0,120,0,760,0,0]]
    b=[n_santaihejin,n_tongweijuheti,n_jingzhuangshiying,n_leijingti,n_leiyin,n_chaoshikuang,n_chaoxinxing]
    e=[1,1,1,1,1,1,1]
    l=[0,0,0,0,0,0]
    
    lp=lp_maker(f,A,b,[1,1,1,1,1,1,1],l,None,None,1,1)
    #set_int(lp,1,TRUE)
    solvestat = lpsolve('solve', lp)
    x = lpsolve('get_variables', lp)[0]
    print(x)
    for i in range(len(x)):
        x[i] = math.ceil(x[i])
    
    print("0艾克诺岩Arkonor："+str(x[0]))
    print("1黑赭石Dark Ochre："+str(x[1]))
    print("2灰岩Spodumain："+str(x[2]))
    print("3克洛基石Crokite："+str(x[3]))
    print("4双多特石 Bistot："+str(x[4]))
    print("5片麻岩 Gneiss ："+str(x[5]))
    
    
    f_santaihejin = 22000*x[0] + 10000*x[1] + 56000*x[2] + 2100*x[3]
    f_tongweijuheti = 1600*x[1] + 450*x[2] + 300*x[5]
    f_jingzhuangshiying = 135*x[3] + 450*x[4]
    f_leijingti = 12050*x[2] + 12000*x[4] + 2200*x[5]
    f_leiyin = 2500*x[0] + 2100*x[2] + 2400*x[5]
    f_chaoshikuang = 320*x[0] + 100*x[4]
    f_chaoxinxing = 120*x[1] + 760*x[3]
    
    
    print("三钛合金Tritanium："+str(f_santaihejin)+"/"+str(n_santaihejin)+"，差值为：" + str(f_santaihejin-n_santaihejin))
    print("同位聚合体Isogen："+str(f_tongweijuheti)+"/"+str(n_tongweijuheti)+"，差值为：" + str(f_tongweijuheti-n_tongweijuheti))
    print("晶状石英Zydrine："+str(f_jingzhuangshiying)+"/"+str(n_jingzhuangshiying)+"，差值为：" + str(f_jingzhuangshiying-n_jingzhuangshiying))
    print("类晶体Pyerite："+str(f_leijingti)+"/"+str(n_leijingti)+"，差值为：" + str(f_leijingti-n_leijingti))
    print("类银Mexallon："+str(f_leiyin)+"/"+str(n_leiyin)+"，差值为：" + str(f_leiyin-n_leiyin))
    print("超噬矿Megacyte："+str(f_chaoshikuang)+"/"+str(n_chaoshikuang)+"，差值为：" + str(f_chaoshikuang-n_chaoshikuang))
    print("超新星Nocxium："+str(f_chaoxinxing)+"/"+str(n_chaoxinxing)+"，差值为：" + str(f_chaoxinxing-n_chaoxinxing))
    
    #print("总花费："+str(x[0]*kuangpricelist[0]+x[1]*kuangpricelist[1]+x[2]*kuangpricelist[2]+x[3]*kuangpricelist[3]+x[4]*kuangpricelist[4]+x[5]*kuangpricelist[5]))
    
    
    context={}
    context['aike']=x[0]
    context['heizhe']=x[1]
    context['huiyan']=x[2]
    context['keluo']=x[3]
    context['shuangduo']=x[4]
    context['pianma']=x[5]
    
    context['price0']=kuangpricelist[0]
    context['price1']=kuangpricelist[1]
    context['price2']=kuangpricelist[2]
    context['price3']=kuangpricelist[3]
    context['price4']=kuangpricelist[4]
    context['price5']=kuangpricelist[5]
    context['cost']=x[0]*kuangpricelist[0]+x[1]*kuangpricelist[1]+x[2]*kuangpricelist[2]+x[3]*kuangpricelist[3]+x[4]*kuangpricelist[4]+x[5]*kuangpricelist[5]

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
