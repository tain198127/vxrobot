# -*- coding: utf-8 -*-
import configparser

import itchat
from snownlp import SnowNLP

# 需要监控的群
ChatRoomUserNames = []

import logging

# logging.basicConfig()
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
chatroomsNames = cf.get('wechat', 'chatrooms')
itchat.auto_login(hotReload=True, enableCmdQR=2)


def checker(fn):
    def run(*args, **kwargs):
        global ChatRoomUserNames
        msg = args[0]
        if msg is not None and msg.User is not None and msg.User.UserName is not None and msg.User.UserName in ChatRoomUserNames:
            try:
                result = fn(*args, **kwargs)

                return result
            except Exception as e:
                pass
                # logger.error(e)

    return run


# 欢迎信息

@itchat.msg_register([itchat.content.NOTE, itchat.content.SYSTEM], isGroupChat=True)
def welcomemsg(msg):
    sysInfo(msg)


# 询问信息

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
def ask(msg):
    nlpAnalise(msg)


@checker
def sysInfo(msg):
    logger.info(msg)

@checker
def nlpAnalise(msg):
    logger.info(msg)

    s = SnowNLP(msg.Content)
    print('群id:{},群:{},userid{}，用户:{},时间:{}, 内容:{}, 情感:{},状态:{}'.format(msg.User.UserName, msg.User.NickName,
                                                                        msg.ActualUserName,
                                                                        msg.ActualNickName, msg.CreateTime, msg.Content,
                                                                        s.sentiments, msg.Status))

# 初始化聊天室监控信息
def initChatRoom(isUpdate):
    global ChatRoomUserNames
    chatrooms = itchat.get_chatrooms(update=isUpdate, contactOnly=True)
    for room in chatrooms:
        if room['NickName'] in chatroomsNames:
            ChatRoomUserNames.append(room['UserName'])
            print("群名称:{:<}       唯一识别号:{:>}".format(room['NickName'], room['UserName']))


initChatRoom(True)

itchat.run(True)
