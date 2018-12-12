import requests
import time
import os
from urllib import request
from bs4 import BeautifulSoup
import urllib
class Wy:
    page = 0
    wymusic = {}
    headers = {
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    def __init__(self, name):
        self.fenlei = name
        os.path.exists("demo")
        isExists = os.path.exists("demo")
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs("demo")
            print ('创建文件夹成功')
    def get(self):
        res = requests.get('https://music.163.com/playlist?id=2174233544',{},headers=self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        red = soup.find('ul', {'class': 'f-hide'}).find_all('a')
        for i in red:
            self.wymusic[i['href'].strip("/song?id=")] = i.text
        self.down()
    def down(self):
        for i in self.wymusic:
            url='http://music.163.com/song/media/outer/url?id=%s.mp3'% i
            urllib.request.urlretrieve(url, 'demo\\%s.mp3' % self.wymusic[i])
            time.sleep(0.9)
a = Wy()
a.get()