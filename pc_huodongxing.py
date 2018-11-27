#!/usr/bin/python
# coding=UTF-8
#爬取活动行页面数据
#http://www.huodongxing.com/events?orderby=o&city=%E5%85%A8%E9%83%A8&page=2
import requests
import time
from bs4 import BeautifulSoup
import pymysql
page = 2
def getid():
    global page
    while True:
        pages = requests.get('http://www.huodongxing.com/events?orderby=o&city=%E5%85%A8%E9%83%A8&page=' + str(page))
        soup = BeautifulSoup(pages.text, 'html.parser')
        res = soup.find_all("div",class_="search-tab-content-item-mesh")
        i=0
        for item in res:
            txtlist = item.find('a')
            print('进行抓取第'+str(page)+'页,第'+str(i)+'个界面')
            page2 = requests.get('http://www.huodongxing.com'+str(txtlist['href']))
            soup2 = BeautifulSoup(page2.text, 'html.parser')
            #标题
            title = soup2.find('title').string
            #宣传图片
            images = soup2.find('div',class_="jumbotron media").find('img')['src']
            #简介
            summary = soup2.find('title').string
            #内容
            content = soup2.find('div', id="event_desc_page")
            i = i+1
            #数据入库
        page = int(page) + 1
if __name__ == '__main__':
    getid()




