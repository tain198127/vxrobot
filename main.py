# -*- coding: utf-8 -*-
import itchat
import sys
import time
import  configparser
# 需要监控的群
ChatRoomUserNames=[]

from itchat.content import *
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
formatter = logging.Formatter("%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
# newInstance = itchat.new_instance()
#
# newInstance.auto_login(enableCmdQR=2)

cf = configparser.ConfigParser()
cf.read('./conf/application.conf')
chatroomsNames = cf.get('wechat','chatrooms')
itchat.auto_login(hotReload=True, enableCmdQR=2)

# 欢迎信息
@itchat.msg_register([itchat.content.MAP, itchat.content.CARD, itchat.content.NOTE, itchat.content.SHARING, itchat.content.PICTURE,
                      itchat.content.RECORDING, itchat.content.VOICE, itchat.content.ATTACHMENT, itchat.content.VIDEO, itchat.content.FRIENDS, itchat.content.SYSTEM],isGroupChat=True)
def welcomemsg(msg):
    global ChatRoomUserNames
    if msg is not None and msg.User is not None and msg.User.UserName is not None and msg.User.UserName in ChatRoomUserNames:
        logger.info(msg)

# 询问信息
@itchat.msg_register([itchat.content.TEXT],isGroupChat=True)
def ask(msg):
    global ChatRoomUserNames
    if msg is not None and msg.User is not None and msg.User.UserName is not None and msg.User.UserName in ChatRoomUserNames:
        logger.info(msg)

#定时广播
def broadcast():
    logger.info("定时广播")

# 初始化聊天室监控信息
def initChatRoom(isUpdate):
    global ChatRoomUserNames
    chatrooms = itchat.get_chatrooms(update=isUpdate, contactOnly=True)
    for room in chatrooms:
        if room['NickName'] in chatroomsNames:
            ChatRoomUserNames.append(room['UserName'])
            print("群名称:{:<}       唯一识别号:{:>}".format(room['NickName'],room['UserName']))

initChatRoom(True)

itchat.run(True)