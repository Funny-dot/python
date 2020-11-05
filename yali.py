#!/usr/bin/python
#encoding=utf-8
import requests
import threading

#保存线程id
threadId=[]
def requesd():
    #认养
    url = "http://www.baidu.com"
    payload = {
        'type': 1,
    }
    files = [

    ]
    headers = {
        
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
#终结线程
def _async_raise(self,tid, exctype):
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            print('错误的线程ID')
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            print('PyThreadState_SetAsyncExc failed')
if __name__ == '__main__':
    i=1
    tread=[]
    while i<300:
        name = threading.Thread(target=requesd)
        name.setDaemon(True)
        tread.append(name)
        print('运行次数:'+str(i))
        i = i+1
    for mm in tread:
        print('启动'+str(mm))
        mm.start()
		ident = name.ident
        threadId.append(ident)
	for a in threadId:
		_async_raise(m, SystemExit)



