#!/usr/bin/python
#encoding=utf-8
import json
import requests
import sys, os, zipfile
import time
from flask import Flask,request
from shutil import copy,rmtree
app = Flask(__name__)
class httpwx:
    appid=''
    newcon = '''{
                    	"description": "项目配置文件",
                    	"packOptions": {
                    		"ignore": []
                    	},
                    	"setting": {
                    		"urlCheck": false,
                    		"es6": false,
                    		"minified": true
                    	},
                    	"compileType": "miniprogram",
                    	"libVersion": "2.9.2",
                    	"appid": "miniappid",
                    	"projectname": "11",
                    	"simulatorType": "wechat",
                    	"simulatorPluginLibVersion": {},
                    	"condition": {
                    		"search": {
                    			"current": -1,
                    			"list": []
                    		},
                    		"conversation": {
                    			"current": -1,
                    			"list": []
                    		},
                    		"game": {
                    			"current": -1,
                    			"list": []
                    		},
                    		"miniprogram": {
                    			"current": -1,
                    			"list": []
                    		}
                    	}
                    }'''
    http_url=''
    pid=''
    desc=''
    version=''
    dir='./mp-weixin'
    is_plugins=0
    port=00
    logdir=r'/root/web/python/update.log'
    maindir=r'/root/web/python/'
    configdata = ['域名', 'appid', '名称', '1.3.3', '简介', './private.key']
    def vs(self,dir):
        if os.path.exists(self.logdir):
            vs = open(self.logdir, 'r')
            con = vs.read()
            vs.close()
            print('版本', con)
            with open(dir + '/update.log', 'w') as f:
                f.write(str(con))
                f.close()
    def unzip_single(self,src_file, dest_dir, password):
        ''' 解压单个文件到目标文件夹。
        '''
        if password:
            password = password.encode()
        zf = zipfile.ZipFile(src_file)
        try:
            zf.extractall(path=dest_dir, pwd=password)
        except RuntimeError as e:
            print(e)
        zf.close()

    def unzip_all(self,source_dir, dest_dir, password):
        if not os.path.isdir(source_dir):  # 如果是单一文件
            self.unzip_single(source_dir, dest_dir, password)
        else:
            it = os.scandir(source_dir)
            for entry in it:
                if entry.is_file() and os.path.splitext(entry.name)[1] == '.zip':
                    self.unzip_single(entry.path, dest_dir, password)

    def checks(self):
        # 获取最新的版本
        files = open('update.log', 'w+')
        indexversion = files.read()
        rr = requests.get('http://www.baidu.com/program_version')
        res = json.loads(rr.content)
        resdata = res
        if str(resdata['version']) != str(indexversion):
            files.truncate()
            files.write(str(resdata['version']))
            # 下载包
            download_url = resdata['url']
            zipfile = requests.get(download_url)
            path = './mp-weixin.zip'
            with open(path, 'wb') as f:
                for chunk in zipfile.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            self.unzip_all('mp-weixin.zip', os.getcwd(), '')
        files.close()
    def __init__(self,appid='123123',http_url='123123',pid='123',version='1.0.0',desc='1.0.0',is_plugins=0):
        self.desc=desc
        self.appid=appid
        self.http_url=http_url
        self.pid=pid
        self.version=version
        self.checks()
        self.is_plugins=is_plugins
        #获取端口号
        file=open(r'/root/.config/wechat_web_devtools/Default/.ide')
        con=file.read()
        self.port=str(con)
        #创建文件
        dir=self.maindir+str(self.appid)
        if os.path.exists(dir)==False:
            os.mkdir(dir)
            #拷贝
            # os.mkdir(dir)
            self.copy_die(self.maindir+'mp-weixin',dir)
            #写入版本
            self.vs(dir)
            # self.checkplu()
        else:
            #判断是否需要更新
            if os.path.exists(dir+'/update.log') and os.path.exists(self.logdir):
                vss = open(self.logdir, 'r')
                con = vss.read()
                vss.close()
                oldvs=open(dir+'/update.log','r+')
                oldcon=oldvs.read()
                if str(con) != str(oldcon):
                    oldvs.write(str(con))
                    oldvs.close()
                    #版本不一致 删除源目录 在copy
                    rootdir = dir
                    filelist = os.listdir(rootdir)
                    for f in filelist:
                        filepath = os.path.join(rootdir, f)
                        if os.path.isfile(filepath):
                            os.remove(filepath)
                        elif os.path.isdir(filepath):
                            rmtree(filepath, True)
                    self.copy_die(self.maindir+'mp-weixin', dir)
                    self.vs(dir)
            # self.checkplu()
        self.dir=dir
    #干掉直播关键字 和直播连接
    def checkfile(self,rootdir):
        filelist = os.listdir(rootdir)
        for f in filelist:
            filepath = os.path.join(rootdir, f)
            if os.path.isfile(filepath):
                try:
                    files = open(filepath, 'r', encoding='utf-8')
                    con = files.read()
                    rr = con.replace('直播', '')
                    rr = rr.replace('"pages/live/list",', ' ')
                    rr = rr.replace('"pages/live/index",', ' ')
                    rr = rr.replace('"pages/live/streaming",', ' ')
                    files.close()
                    filesd = open(filepath, 'w')
                    filesd.write(rr)
                    filesd.close()
                except:
                    print(filepath)
            elif os.path.isdir(filepath):
                self.checkfile(filepath)
    def copy_die(self,dir, newdir):
        for p in os.listdir(dir):
            print(p)
            filepath = newdir + '/' + p
            oldpath = dir + '/' + p
            if os.path.isdir(oldpath):
                os.mkdir(filepath)
                self.copy_die(oldpath, filepath)
            if os.path.isfile(oldpath):
                copy(oldpath, filepath)
    def check(self):
        if os.path.exists('./install.txt'):
            file=open('./install.txt','r')
            con=file.read()
            rd=con.split('-')
            file.close()
            if str(rd[0])==self.appid:
                # self.checkplu()
                return False
            return  True
        else:
            with open('./install.txt','w') as f:
                f.write(str(self.appid)+'-'+str(time.time()))
                f.close()
            self.updates()
            return False
    def updates(self):
        a = 0
        # 替换文件
        newcons = self.newcon.replace('miniappid', self.appid)
        file = open(self.dir + '/project.config.json', 'w+')
        file.write(newcons)
        file.close()
        # 替换域名
        one_file = self.dir + '/common/vendor.js'
        self.tihuan(one_file, self.configdata[0], self.http_url)
        # 替换小程序ID
        self.tihuan(one_file, 'uniacid:"1"', 'uniacid:"' + str(self.pid) + '"')

    def checkplu(self):
        # 验证是否需要直播插件
        if int(self.is_plugins) == 1:
            file = open(self.dir + '/app.json', 'r', encoding='utf-8')
            con = file.read()
            arr = json.loads(con)
            print('需要')
            arr['subPackages'][0]['plugins'] = {
                "live-player-plugin": {"version": "1.0.19", "provider": 'wx2b03c6e691cd7370'}}
            file = open(self.dir + '/app.json', 'w+', encoding='utf-8')
            file.write(json.dumps(arr))
        else:
            #替换所有的文件
            self.checkfile(self.dir)
            # 不休啊
            file = open(self.dir + '/app.json', 'r', encoding='utf-8')
            con = file.read()
            arr = json.loads(con)
            arr['subPackages'][0]['plugins'] = {}
            file = open(self.dir + '/app.json', 'w+', encoding='utf-8')
            file.write(json.dumps(arr))
    def rmdirs(self,top):
        for root, dirs, files in os.walk(top, topdown=False):
            # 先删除文件
            for name in files:
                os.remove(os.path.join(root, name))
            # 再删除空目录
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    #登陆
    def login(self):
        check = self.check()
        if check:
            return json.dumps({'code': 1, 'msg': '暂无流量，请稍后再试'})
        else:
            dir = self.maindir+'/loginresult/' + str(self.appid) + '/loginresult.json'
            if os.path.exists(self.maindir+'loginresult/' + str(self.appid)) == False:
                os.mkdir(self.maindir+'loginresult/' + str(self.appid))
            url='http://127.0.0.1:'+str(self.port)+'/v2/login?qr-format=base64&result-output=%2Froot%2Fweb%2Fpython%2Floginresult%2F'+str(self.appid)+'%2Floginresult.json'
            r=requests.get(url)
            print('结果',r.text)
            datas=json.loads(r.text)
            return json.dumps({'code':0,'msg':'成功','data':datas['qrcode']})
    def logincheck(self):
        appid=self.appid
        dir=self.maindir+'loginresult/'+str(self.appid)+'/loginresult.json'
        con=''
        if os.path.exists(dir):
            with open(dir,'r') as file:
                con=file.read()
                file.close()
        return json.dumps({'code':0,'msg':'获取成功','data':str(con)})
    #预览
    def preview(self):
        self.checkplu()
        self.updates()
        projecturl = self.dir
        print('项目目录',projecturl)
        url='http://127.0.0.1:'+str(self.port)+'/v2/preview?project='+str(projecturl)+'&qr-format=base64'
        r=requests.get(url)
        self.reduction()
        if  r.text.find('{') >-1:
            self.reduction()
            con=json.loads(r.text)
            return json.dumps({'code':1,'msg':con['message']})
        return json.dumps({'code': 0, 'msg': '成功', 'data': {'base64': r.text}})
    #上传
    def upload(self):
        self.checkplu()
        projecturl = self.dir
        out_put=self.maindir+'output.json'
        url = 'http://127.0.0.1:' + str(self.port) + '/v2/upload?project=' + str(projecturl) + '&version=v'+str(self.version)+'&desc="'+str(self.desc)+'"&info-output='+str(out_put)
        r = requests.get(url)
        self.reduction()
        #获取预览图片
        res=json.loads(r.text)
        if  isinstance(res,str)==False and 'code' in res:
            return json.dumps({'code':1,'msg':res['message']})
        return json.dumps({'code': 0, 'msg': '成功', 'data': {'base64': res}})
    def reduction(self):
        one_file = self.dir + '/project.config.json'
        # 替换APPid
        self.tihuan(one_file, self.appid, self.configdata[1])
        # 替换域名
        one_file = self.dir + '/common/vendor.js'
        self.tihuan(one_file, self.http_url, self.configdata[0])
        # 替换小程序ID
        self.tihuan(one_file,  'uniacid:"' + str(self.pid) + '"','uniacid:"1"')
        try:
            # 删除文件
            if os.path.exists('./install.txt'):
                os.remove('./install.txt')
            dir = self.maindir + 'loginresult/' + str(self.appid) + '/loginresult.json'
            if os.path.exists(dir):
                os.remove(dir)
            disr = self.maindir + str(self.appid)
            if os.path.exists(disr):
                self.rmdirs(disr)
                os.removedirs(disr)
            print(1)
        except:
            print('修改失败2')
    def tihuan(self, file_path, sreach, replace):
        try:
            file = file_path
            files = open(file, 'r', encoding='UTF-8')
            content = files.read().encode('utf-8').decode('UTF-8').strip()
            files.close()
            new_two_file = open(file, 'w', encoding='UTF-8')
            new_content = content.replace(sreach, replace)
            new_two_file.write(new_content)
            new_two_file.close()
            file = file_path
            files = open(file, 'r', encoding='UTF-8')
            content = files.read().encode('utf-8').decode('UTF-8').strip()
            files.close()
            new_two_file = open(file, 'w', encoding='UTF-8')
            new_content = content.replace(sreach, replace)
            new_two_file.write(new_content)
            new_two_file.close()
        except:
            print('修改失败')
@app.route('/apis', methods=['GET'])
def mains():
    #http://192.168.100.6:5002/apis?action=login&appid=wxcc367d8b0374e4dd&http_url=192.168.100.6&pid=1
    action = request.args.get("action")
    appid = request.args.get("appid")  #appid
    http_url = request.args.get("http_url")  #替换域名
    pid = request.args.get("pid")  #小程序id
    version = request.args.get("version")  #版本号
    desc = request.args.get("desc") #描述
    is_plugins = request.args.get("is_plugins")  #1 需要插件  0不需有
    if is_plugins:
        print('需要插件')
    else:
        is_plugins=0
    mm={}
    a = httpwx(appid, http_url,pid,version,desc,is_plugins)
    if(action=='login'):
        mm=a.login()
    elif action=='upload':
        mm=a.upload()
    elif action=='preview':
        mm = a.preview()
    else:
        mm=a.logincheck()
    return mm
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,debug=True)
