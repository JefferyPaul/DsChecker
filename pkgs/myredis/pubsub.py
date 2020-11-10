# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 13:16
# @Author  : Jeffery Paul
# @File    : pubsub.py


from pkgs.myredis import REDIS, _pub_sub_config
from pkgs.myredis.signal import RedisSignal

import logging


# pub-sub模式中的  subscriber 订阅端，
class RedisSubTask(object):
    def __init__(self, channel):
        self.rcon = REDIS
        self.ps = self.rcon.pubsub()
        self.ps.subscribe(channel)

    def listen_task(self):
        print('Listening')
        for sub_msg in self.ps.listen():
            if sub_msg['type'] == 'message':
                # print(sub_msg)
                print(sub_msg['data'].decode())


# pub-sub 模式中的 publish 功能
def pub_msg(
        msg,
        script_name='',
        levelname=''
):
    if _pub_sub_config:
        pass
    else:
        raise KeyError
    REDIS.publish(
        _pub_sub_config['channel'],
        str(RedisSignal(
            address=_pub_sub_config['my_address'], script_name=script_name, msg=msg, levelname=levelname
        ))
    )

# ================== ========================


# logger
# 配合logger使用， 在logger记录时，发送redis pub
class RedisLoggerHandler(logging.Handler):
    def __init__(self, script_name, level=logging.WARNING,  *args, **kwargs):
        super(RedisLoggerHandler, self).__init__(*args, **kwargs)
        self.script_name = script_name
        self.setLevel(level)

        # format_string =
        # self.setFormatter(logging.Formatter(format_string))

    def emit(self, record):
        pub_msg(
            msg=record.message,
            script_name=self.script_name,
            levelname=record.levelname
        )
