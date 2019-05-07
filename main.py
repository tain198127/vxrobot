# -*- coding: utf-8 -*-
import configparser

import itchat
from snownlp import SnowNLP

# 需要监控的群
ChatRoomUserNames = []
# 本机器人的信息
robotnickname = ''
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


def loginCbk():
    info = itchat.show_mobile_login()

    logger.info(info)


def checker(fn):
    def run(*args, **kwargs):
        global ChatRoomUserNames
        msg = args[0]
        if msg is not None and msg.User is not None and msg.User.UserName is not None and msg.User.UserName in ChatRoomUserNames:
            try:
                result = fn(*args, **kwargs)

                return result
            except Exception as e:
                logger.error(e)

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
    # 表明是在艾特我
    if msg.ToUserName == msg.User.Self.UserName:
        if '语义分析' in msg.Content:
            realContent = msg.Content.split('语义分析')[1:][0]
            s = SnowNLP(realContent)
            # 情感指数
            emocode = s.sentiments
            emosentence = ''
            if emocode >= 0.69:
                emosentence = '偏正能量'
            elif emocode <= 0.39:
                emosentence = '偏负能量'
            else:
                emosentence = '靠近中性'

            print('群id:{},群:{},userid{}，用户:{},时间:{}, 内容:{}, 情感:{},状态:{}'.format(msg.User.UserName, msg.User.NickName,
                                                                                msg.ActualUserName,
                                                                                msg.ActualNickName, msg.CreateTime,
                                                                                realContent,
                                                                                emocode, msg.Status))

            msg.user.send('@{} 情感指数:{}, 语言{}哦'.format(msg.ActualNickName, emocode,emosentence))


# 初始化聊天室监控信息
def initChatRoom(isUpdate):
    global ChatRoomUserNames
    chatrooms = itchat.get_chatrooms(update=isUpdate, contactOnly=True)

    for room in chatrooms:
        if room['NickName'] in chatroomsNames:
            ChatRoomUserNames.append(room['UserName'])
            print("群名称:{:<}       唯一识别号:{:>}".format(room['NickName'], room['UserName']))


logininfo = itchat.auto_login(hotReload=True, enableCmdQR=2, loginCallback=loginCbk)
print(logininfo)

initChatRoom(True)

itchat.run(True)
