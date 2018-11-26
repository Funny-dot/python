#!/usr/bin/python
# coding=UTF-8
import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import threading
from time import sleep
import json
import requests
import time
import random

#自定义账号库，未连接数据库所以用的死的
bdzh = ['212121212121']
h = {'Content-Type': 'application/x-www-form-urlencoded',
     'Accept-Language': 'zh'}
def trade():
    buyone = 0
    sellone = 0
    buydp = 0
    selldp = 0
    buym = 0
    sellm = 0
    cishu = 0
    chengjiao = 0
    sxf = 0
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    T2.insert(END, time1 + '   正在启动刷单进程\n')
    sellb = sellb1.get()
    buyb = buyb1.get()
    danwei1.set(buyb)
    jyd = sellb + '_' + buyb
    if sellb == 'ETH':
        low = 0.005
    elif sellb == 'BTC':
        low = 0.00009

    api = api1.get()  # 获取API token
    yajia = float(yajia1.get())  # 最小单位精度

    dd = 'https://api.5iquant.org/api/trade/submitOrder'  # 下订单
    cancel = 'https://api.5iquant.org/api/trade/iqtexCancelOrder'  # 撤单
    dp = 'https://api.5iquant.org/api/trade/entrustedRecord/%s' % jyd  # 深度信息
    orderlist = 'https://api.5iquant.org/api/trade/iqtexCurrentOrderList'  # 委托列表
    money = 'https://api.5iquant.org/api/trade/myAssets/%s' % jyd  # 查询余额

    dpbody = {'version': '01'}
    monbody = {'version': '01',
               'access_token': '%s' % api}
    listbody = {'version': '01',
                'access_token': '%s' % api,
                'currencyName': '%s' % jyd}

    e5.configure(state='disabled')
    e7.configure(state='disabled')
    e8.configure(state='disabled')
    btt.configure(state='disabled')
    btt1.configure(state='disabled')
    btt2.configure(state='disabled')
    e7.configure(state='readonly')
    e1.configure(state='readonly')
    eapi.configure(state='readonly')
    zhanghao = zhanghao1.get()
    chedant = 4
    if zhanghao in bdzh:
        while True:
            try:
                orderID = 'A'
                n = 0
                num = float(num1.get())
                num = num_n(num, jyd)  # 控制下单数量位数
                tb = float(tb1.get())  # 交易间隔
                bod1 = float(bodong1.get())  # 市场波动小
                bod2 = float(bodong2.get())  # 市场波动大
                baohulow = float(baohu1.get())
                baohuhigh = float(baohu2.get())
                chedant = float(chedan1.get())
                # tx=float('%.1f' % (random.uniform(0,0.6))#随机时间
                # px=random.randint(-2,2)*yajia
                buym, sellm = get_money(money, monbody, h, buyb)  # 获取余额
                buyone, sellone, buydp, selldp = get_dp(dp, dpbody, h)  # 获取深度
                if sellone - buyone <= yajia * 2 and buydp > num and selldp > num:
                    sell = buyone
                    buy = sellone
                else:
                    sell = sellone - ((sellone - buyone) / 2)  # 需要考虑有效位数
                    buy = sell
                sell = price_n(sell, jyd)  # 控制下单价格位数
                buy = price_n(buy, jyd)
                buybody = {'version': '01',
                           'access_token': '%s' % api,
                           'currencyName': '%s' % jyd,
                           'num': '%s' % num,
                           'price': '%s' % buy,
                           'type': 'buy'}
                sellbody = {'version': '01',
                            'access_token': '%s' % api,
                            'currencyName': '%s' % jyd,
                            'num': '%s' % num,
                            'price': '%s' % sell,
                            'type': 'sell'}
                if (sellone - buyone) >= bod1 and (sellone - buyone) <= bod2 and sell * num * 1.001 < buym and num <= sellm and num > low and sell > baohulow and sell < baohuhigh:  # 深度差劲，买卖足够钱，马上成交
                    threading.Thread(target=sell_http, args=(dd, sellbody, h)).start()
                    threading.Thread(target=buy_http, args=(dd, buybody, h)).start()
                    sleep(0.5)
                    while orderID != 'X':
                        orderID = get_order(orderlist, listbody, h)  # 获取未成交的orderID
                        if orderID == 'X':
                            time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                            print(' 自成交已完成')
                            T2.insert(END, time1 + '   自成交已完成（*^▽^*）\n')
                            sxf = sxf + (num * sell) * 0.002
                            chengjiao = chengjiao + 1
                        n = n + 1
                        if n >= chedant:
                            cancelbody = {'version': '01',
                                          'access_token': '%s' % api,
                                          'orderId': '%s' % orderID}
                            clear_all(cancel, cancelbody, h)
                            print('撤单')
                            cishu = cishu + 1
                            break
                        sleep(1)
                else:  # 这几种情况，1波动小，2，卖的金额大于buym,3卖的数量大于sellm
                    if (sellone - buyone) < bod1:  # 波动小
                        time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                        T2.insert(END, time1 + '   小小小小小小于市场波动，不挂单\n')
                    elif (sellone - buyone) > bod2:  # 波动大
                        time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                        T2.insert(END, time1 + '   大大大大大大于市场波动，不挂单\n')
                    elif sell * num * 1.001 > buym:  # usd不足买
                        time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                        T2.insert(END, time1 + '   %s 数量不足' % (buyb) + '\n')
                    elif num > sellm:  # 卖币不足
                        time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                        T2.insert(END, time1 + '   %s 数量不足' % (sellb) + '\n')
                    elif sell > baohuhigh or sell < baohulow:
                        time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                        T2.insert(END, time1 + '   价格保护启动，价格离谱防止插针\n')
                    else:
                        time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                        T2.insert(END, time1 + '    没钱了别折腾了，充值吧\n')
                    tb = tb / 3
                buym1.set(buym)
                sellm1.set(sellm)
                buyone1.set(buyone)
                sellone1.set(sellone)
                buydp1.set(buydp)
                selldp1.set(selldp)
                cishu1.set(cishu)
                chengjiao1.set(chengjiao)
                sxf1.set(sxf)
                ms = mode.get()
                time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))  # 以下是自动修改数量
                if sellm != num and (buym / buyone) > sellm and sellm > low and ms == '自动修改数量':  # 足够USD买时候就改成全部
                    num = sellm  # sellm本身是3位有效小数，不需要用函数来修正
                    T2.insert(END, time1 + '    已经满上全部%s' % sellb + '\n')
                elif (buym / sellone) < sellm and (buym / sellone) > low and ms == '自动修改数量' and (
                        num < buym * 0.7 / sellone or num > buym * 0.95 / sellone):
                    numy = buym * 0.85 / sellone
                    if numy > low and numy < sellm:
                        num = num_n(numy, jyd)  # 计算后超过n位有效小数，需要函数修正
                    T2.insert(END, time1 + '    已经设置少数量%s' % sellb + '\n')
                num1.set(num)
            except:
                time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                T2.insert(END, time1 + '   交易线程需要重启（ಥ﹏ಥ）\n')
                break
            T2.see(END)
            sleep(tb)
    else:
        T2.insert(END, time1 + '   您的账号不在允许使用范围内\n')


#########################################################
def num_n(x, y):  # 修num数量正有效位数
    if y == 'ETH_USDT':
        x = float('%.3f' % x)
    elif y == 'BTC_USDT':
        x = float('%.5f' % x)
    elif y == 'ETH_BTC':
        x = float('%.3f' % x)
    return x


def price_n(x, y):  # 修价格数量正有效位数
    if y == 'ETH_USDT':
        x = float('%.2f' % x)
    elif y == 'BTC_USDT':
        x = float('%.2f' % x)
    elif y == 'ETH_BTC':
        x = float('%.6f' % x)
    return x


def info():  # 这个监控进程没用，我懒得删除
    cancel = 'https://api.5iquant.org/api/trade/iqtexCancelOrder'  # 撤单
    sellb = sellb1.get()
    buyb = buyb1.get()
    jyd = sellb + '_' + buyb
    api = api1.get()  # 获取API token
    orderlist = 'https://api.5iquant.org/api/trade/iqtexCurrentOrderList'  # 委托列表
    listbody = {'version': '01',
                'access_token': '%s' % api,
                'currencyName': '%s' % jyd}
    while True:
        pass
        # orderID=get_order(orderlist,listbody,h)#获取未成交的orderID
        # if orderID!='':
        # cancelbody={'version':'01',
        # 'access_token':'%s'%api,
        # 'orderId':'%s'%orderID}
        # clear_all(cancel,cancelbody,h)
        sleep(10)


##################################
###################################
def buy_http(x, y, z):
    buyre = requests.post(x, data=y, headers=z)
    code = json.loads(buyre.text)['ret']
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    if buyre.status_code == 200 and code == '200':
        print("buy挂单成功")
        T2.insert(END, time1 + '   buy挂单成功%s' % code + '\n')
        T2.see(END)
    else:
        if buyre.status_code != 200:
            print('下订单网络出错%s' % buyre.status_code)
            T2.insert(END, time1 + '   网络出错%s' % buyre.status_code + '\n')
        else:
            print('非网络出错代码%s' % code)
            T2.insert(END, time1 + '   非网络出错代码%s' % (code) + '\n')


##################################
def sell_http(x, y, z):
    sellre = requests.post(x, data=y, headers=z)
    code = json.loads(sellre.text)['ret']
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    if sellre.status_code == 200 and code == '200':
        print("sell挂单成功")
        T2.insert(END, time1 + '   sell挂单成功%s' % code + '\n')
        T2.see(END)
    else:
        if sellre.status_code != 200:
            print('下订单网络出错%s' % sellre.status_code)
            T2.insert(END, time1 + '   网络出错%s' % sellre.status_code + '\n')
        else:
            print('非网络出错代码%s' % code)
            T2.insert(END, time1 + '   非网络出错代码%s' % (code) + '\n')


##################################

####################################################
def get_dp(x, y, z):
    dpinfo = requests.post(x, data=y, headers=z)
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    code = json.loads(dpinfo.text)['ret']
    if dpinfo.status_code == 200 and code == '200':
        A = dpinfo.text  ## versionInfo 是接口返回的 json 格式数据
        B = json.loads(A)  ## json.loads 将已编码的 JSON 字符串解码为 Python 对象
        buyone = float(B['data']['buyOrderList'][0]['price'])
        buydp = float(B['data']['buyOrderList'][0]['num'])
        sellone = float(B['data']['sellOrderList'][0]['price'])
        selldp = float(B['data']['sellOrderList'][0]['num'])
        return buyone, sellone, buydp, selldp
    else:
        if dpinfo.status_code != 200:
            print('查询深度网络出错%s' % dpinfo.status_code)
            T2.insert(END, time1 + '   查询深度网络出错%s' % dpinfo.status_code + '\n')
        else:
            print('dp非网络出错代码%s' % code)
            T2.insert(END, time1 + '   dp非网络出错代码%s' % (code) + '\n')


###############################################

def get_money(x, y, z, buyb):
    money = requests.post(x, data=y, headers=z)
    code = json.loads(money.text)['ret']
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    if money.status_code == 200 and code == '200':
        A2 = json.loads(money.text)  ## versionInfo 是接口返回的 json 格式数据
        if A2['data'][0]['name'] == buyb:
            buym = float(A2['data'][0]['AssetBalance'])
            sellm = float(A2['data'][1]['AssetBalance'])
        else:
            buym = float(A2['data'][1]['AssetBalance'])
            sellm = float(A2['data'][0]['AssetBalance'])
        return buym, sellm
    else:
        if money.status_code != 200:
            print('获取余额网络出错%s' % money.status_code)
            T2.insert(END, time1 + '   获取余额网络出错%s' % money.status_code + '\n')
        else:
            print('getmo非网络出错代码%s' % code)
            T2.insert(END, time1 + '   getm非网络出错代码%s' % (code) + '\n')


###########################################################

def get_order(x, y, z):
    orderinfo = requests.post(x, data=y, headers=z)
    code = json.loads(orderinfo.text)['ret']
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    if orderinfo.status_code == 200 and code == '200':
        A1 = orderinfo.text  ## versionInfo 是接口返回的 json 格式数据
        B1 = json.loads(A1)  ## json.loads 将已编码的 JSON 字符串解码为 Python 对象
        ordernum = B1['data']['data']  # 委托订单数量
        if ordernum == []:
            orderID = 'X'
        else:
            orderID = str(B1['data']['data'][0]['orderId'])
        return orderID
    else:
        if orderinfo.status_code != 200:
            print('获取订单网络出错%s' % orderinfo.status_code)
            T2.insert(END, time1 + '   获取订单网络出错%s' % orderinfo.status_code + '\n')
        else:
            print('getorder非网络出错代码%s' % code)
            T2.insert(END, time1 + '   getorder非网络出错代码%s' % (code) + '\n')


############################################################

def clear_all(x, y, z):
    clearall = requests.post(x, data=y, headers=z)
    code = json.loads(clearall.text)['ret']
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    if clearall.status_code == 200 and code == '200':
        print('全部撤单成功')
        T2.insert(END, time1 + '   已经撤单（ಥ﹏ಥ）\n')
        T2.see(END)
    else:
        if clearall.status_code != 200:
            print('撤单网络出错%s' % clearall.status_code)
            T2.insert(END, time1 + '   撤单网络出错%s' % clearall.status_code + '\n')
        else:
            print('cancel非网络出错代码%s' % code)
            T2.insert(END, time1 + '   cance非网络出错代码%s' % (code) + '\n')


def read_cfg():
    filename1 = 'config.txt'
    filename2 = 'cookie.txt'
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        f1 = open(filename1)
        a1 = f1.read().split('\n')
        num1.set(a1[0])
        baohu1.set(a1[1])
        tb1.set(a1[2])
        yajia1.set(a1[3])
        bodong1.set(a1[4])
        sellb1.set(a1[5])
        buyb1.set(a1[6])
        bodong2.set(a1[7])
        api1.set(a1[8])
        zhanghao1.set(a1[9])
        baohu2.set(a1[10])
        chedan1.set(a1[11])
        f1.close()
        print('读取配置成功')
        T2.insert(END, time1 + '   读取配置成功\n注意：1.蓝色部分不需要填写自动读取；\n      2.绿色黄色需要填写，绿色可以实时修改;\n')
    except:
        num1.set('0.5')
        baohu1.set('275')
        tb1.set('10')
        yajia1.set('0.01')
        bodong1.set('0.05')
        sellb1.set('ETH')
        buyb1.set('USDT')
        bodong2.set('0.5')
        api1.set('12345678910111213141516')
        zhanghao1.set('你的登录账号')
        baohu2.set('290')
        chedan1.set('5')
        print('未找到配置文件,请输入后点击保存')
        T2.insert(END, time1 + '   未找到配置文件,请输入后点击保存\n注意：1.蓝色部分不需要填写自动读取；\n      2.绿色黄色需要填写，绿色可以实时修改;\n')


######################################################
######################################################
def save_cfg():
    time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    filename1 = 'config.txt'
    f1 = open(filename1, "w")
    f1.write(num1.get() + '\n')
    f1.write(baohu1.get() + '\n')
    f1.write(tb1.get() + '\n')
    f1.write(yajia1.get() + '\n')
    f1.write(bodong1.get() + '\n')
    f1.write(sellb1.get() + '\n')
    f1.write(buyb1.get() + '\n')
    f1.write(bodong2.get() + '\n')
    f1.write(api1.get() + '\n')
    f1.write(zhanghao1.get() + '\n')
    f1.write(baohu2.get() + '\n')
    f1.write(chedan1.get())
    f1.close()
    print('保存配置成功')
    T2.insert(END, time1 + '   保存配置成功\n')


######################################################


def shouhu():
    while True:
        global th1
        global th3
        time1 = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
        if not th1.is_alive():
            th1 = threading.Thread(target=trade)
            th1.start()
            T2.insert(END, time1 + '    交易线程被重启\n')
        if not th3.is_alive():
            th3 = threading.Thread(target=info)
            th3.start()
            T2.insert(END, time1 + '    监控线程被重启\n')
        time.sleep(2)


def qidong():
    global th1
    global th3
    th1 = threading.Thread(target=trade)
    th2 = threading.Thread(target=shouhu)
    th3 = threading.Thread(target=info)
    th1.start()
    th3.start()
    sleep(1)
    th2.start()


# def che():
# threading.Thread(target=clear_by_hand).start()


######################################################
root = tkinter.Tk()
root.title("5iquant交易平台挖矿      自成交版")
root.geometry('810x550')
# root.resizable(width=False, height=False)
#####################################################

#####################################################

#####################################################
L0 = Label(root, text="账户私钥API token", bg="gold", width=14, height=1, padx=2, pady=2)
L0.grid(row=0, column=0)
api1 = StringVar()
eapi = Entry(root, textvariable=api1, width=44, show='*')
eapi.grid(row=1, column=0, columnspan=3, pady=3)

L1 = Label(root, text="打印信息", bg="SkyBlue", width=14, height=1, padx=2, pady=2)
L1.grid(row=0, column=3, sticky=N)
T2 = Text(root, width=60, height=28)
T2.grid(row=1, column=3, columnspan=4, rowspan=11, sticky=N, padx=25, pady=5)

L2 = Label(root, text="登录账号", bg="gold", width=14, height=1, pady=2)
L3 = Label(root, text="单次挂单数量", bg="green", width=14, height=1, pady=2)
L4 = Label(root, text="价格保护范围", bg="green", width=14, height=1, pady=2)
L5 = Label(root, text="挂单间隔时间(秒)", bg="green", width=14, height=1, pady=2)
L6 = Label(root, text="挂单最小精度", bg="gold", width=14, height=1, pady=2)
L7 = Label(root, text="波动范围(买卖差)", bg="green", width=14, height=1, pady=2)
L8 = Label(root, text="交易对(必须大写)", bg="gold", width=14, height=1, pady=2)
L9 = Label(root, text="账户余额", bg="SkyBlue", width=14, height=1, pady=2)
L10 = Label(root, text="卖一买一价", bg="SkyBlue", width=14, height=1, pady=2)
L11 = Label(root, text="卖一买一深度", bg="SkyBlue", width=14, height=1, pady=2)
L12 = Label(root, text="手续费", bg="SkyBlue", width=14, height=1, pady=2)
L13 = Label(root, text="撤单与成交次数", bg="SkyBlue", width=14, height=1, pady=2)
L14 = Label(root, text="撤单等待时间", bg="green", width=14, height=1, pady=2)

L2.grid(row=2, column=0)
L3.grid(row=3, column=0)
L4.grid(row=4, column=0)
L5.grid(row=5, column=0)
L6.grid(row=6, column=0)
L7.grid(row=7, column=0)
L8.grid(row=8, column=0)
L9.grid(row=9, column=0)
L10.grid(row=10, column=0)
L11.grid(row=11, column=0)
L12.grid(row=12, column=0)
L13.grid(row=13, column=0)
L14.grid(row=14, column=0)

chedan1 = StringVar()  # 撤单时间
num1 = StringVar()  # 挂单数量
baohu1 = StringVar()  # 价格保护low
baohu2 = StringVar()  # 价格保护high
tb1 = StringVar()  # 交易间隔
yajia1 = StringVar()  # 压价单位
bodong1 = StringVar()  # 波动小
bodong2 = StringVar()  # 波动大
zhanghao1 = StringVar()

sellb1 = StringVar()
buyb1 = StringVar()

sellm1 = StringVar()
buym1 = StringVar()
sellone1 = StringVar()
buyone1 = StringVar()
selldp1 = StringVar()
buydp1 = StringVar()

sxf1 = StringVar()
danwei1 = StringVar()
cishu1 = StringVar()
chengjiao1 = StringVar()

echedan = Entry(root, textvariable=chedan1, width=30)
e1 = Entry(root, textvariable=zhanghao1, width=30)
e2 = Entry(root, textvariable=num1, width=30)
e3 = Entry(root, textvariable=baohu1, width=14)
e33 = Entry(root, textvariable=baohu2, width=14)
e4 = Entry(root, textvariable=tb1, width=30)
e5 = Entry(root, textvariable=yajia1, width=30)
e6 = Entry(root, textvariable=bodong1, width=14)
e66 = Entry(root, textvariable=bodong2, width=14)

e7 = Entry(root, textvariable=sellb1, width=14)
e8 = Entry(root, textvariable=buyb1, width=14)

e9 = Entry(root, textvariable=sellm1, width=14)
e10 = Entry(root, textvariable=buym1, width=14)

e11 = Entry(root, textvariable=sellone1, width=14)
e12 = Entry(root, textvariable=buyone1, width=14)

e13 = Entry(root, textvariable=selldp1, width=14)
e14 = Entry(root, textvariable=buydp1, width=14)

e15 = Entry(root, textvariable=sxf1, width=14)
e16 = Entry(root, textvariable=cishu1, width=14)
e17 = Entry(root, textvariable=danwei1, width=14)
e18 = Entry(root, textvariable=chengjiao1, width=14)

echedan.grid(row=14, column=1, columnspan=2, pady=3)
e1.grid(row=2, column=1, columnspan=2, pady=3)
e2.grid(row=3, column=1, columnspan=2, pady=3)
e3.grid(row=4, column=1, columnspan=1, pady=3)
e33.grid(row=4, column=2, columnspan=1, pady=3)
e4.grid(row=5, column=1, columnspan=2, pady=3)
e5.grid(row=6, column=1, columnspan=2, pady=3)
e6.grid(row=7, column=1, columnspan=1, pady=3)
e66.grid(row=7, column=2, columnspan=1, pady=3)

e7.grid(row=8, column=1, columnspan=1, pady=3)
e8.grid(row=8, column=2, columnspan=1, pady=3)

e9.grid(row=9, column=1, columnspan=1, pady=3)
e10.grid(row=9, column=2, columnspan=1, pady=3)

e11.grid(row=10, column=1, columnspan=1, pady=3)
e12.grid(row=10, column=2, columnspan=1, pady=3)

e13.grid(row=11, column=1, columnspan=1, pady=3)
e14.grid(row=11, column=2, columnspan=1, pady=3)

e15.grid(row=12, column=1, columnspan=1, pady=3)
e16.grid(row=13, column=1, columnspan=1, pady=3)
e17.grid(row=12, column=2, columnspan=1, pady=3)
e18.grid(row=13, column=2, columnspan=1, pady=3)
#####################################################

mode = tk.StringVar()
modeChosen = ttk.Combobox(root, width=12, textvariable=mode, state='readonly')
modeChosen['values'] = ('自动修改数量', '不自动修改数量')  # 设置下拉列表的值
modeChosen.grid(row=12, column=5, rowspan=2)  # 设置其在界面中出现的位置  column代表列   row 代表行
modeChosen.current(0)

######################################################
btt = Button(root, text="启动", command=qidong, width=10, height=3)
btt.grid(row=12, column=3, rowspan=3, padx=5, pady=5, )

btt1 = Button(root, text="读取配置", command=read_cfg, width=10, height=1)
btt1.grid(row=12, column=4, padx=5, pady=5)

btt2 = Button(root, text="保存配置", command=save_cfg, width=10, height=1)
btt2.grid(row=13, column=4, padx=5, pady=5)

# btt3=Button(root, text="手动撤单", command =che,width=10, height=1)
# btt3.grid(row=13,column=5,padx=5, pady=5)

read_cfg()
root.mainloop()


