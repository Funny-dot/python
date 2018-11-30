# coding:utf-8
import json
from wxpy import *
# 指定图片文件的路径
image_path = "./time.png"
# 初始化微信机器人
bot = Bot()
#给机器的好友列表
robotFriendList = []
#群聊列表
robotGooupsList = []
#需要发送的消息
infos=[
    {
        'type': 'image',  #消息类型
        'info': './time.png' #消息
    },
    {
        'type': 'text',
        'info': '1'
    },
]
#群聊成员
groupList = []
def getmy_friends():
    # 获取所有好友
    global robotFriendList,robotGooupsList
    friend_search = bot.friends()
    for i in friend_search:
        # 保存好友进list
        robotFriendList.append(i)

def getmy_groups():
    # 获取所有的群列表
    gooupsm = bot.groups(update=False, contact_only=False).search()
    print(gooupsm)
    for i in gooupsm:
        # 保存群进list
        robotGooupsList.append(i)
    print(robotGooupsList)
#给朋友发送消息 事件1
def Friend_send_code():
    #给好友发送消息
    for m in infos:
        send_msg(m['type'], m['info'])

#给朋友发送消息 事件2
def send_msg(type,val):
    if type == 'image':
        for i in robotFriendList:
            i.send_image(val)
    elif type == 'text':
        for i in robotFriendList:
            i.send_image(val)
#群发消息
#获取某一个群聊中的成员
def getGroupsList(all=True, groupName=1):
    global  groupList
    if all:
        groupList = []  # 初始化
        #获取所有群中的成员
        for i in robotGooupsList:
            found = i.search()
            for m in found:
                groupList.append(m)
    else:
        groupList = []  # 初始化
        found = groupName.search()
        for m in found:
            #保存进list
            groupList.append(m)
    print(groupList)
getmy_friends()
