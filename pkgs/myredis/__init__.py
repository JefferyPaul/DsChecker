# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 13:16
# @Author  : Jeffery Paul
# @File    : __init__.py.py


import os
import sys
import json
import redis


"""
myredis模块内，统一使用同一个redis连接
    当调用myredis模块时，初始化redis连接（REDIS实例）
    模块内均通过调用 REDIS 来进行连接

实现功能：
pubsub
    RedisSubTask(channel)
        subscriber 端
    pub_msg(msg, script_name, level)        
        publish 功能
    RedisLoggerHandler(script_name)     
        logging.logger.addHandler(RedisLoggerHandler())
        loggerHandler，与logger一同使用 
"""


# 配置/参数
path_chdir = os.getcwd()
PATH_ROOT = os.path.dirname(__file__)
sys.path.append(PATH_ROOT)
os.chdir(PATH_ROOT)         # 改变当前路径

_path = os.path.join(
    os.path.dirname(__file__),
    'Config',
    'Config.json'
)
_path_config = os.path.abspath(json.loads(open(_path, encoding='utf-8').read())['config'])
# print(_path_config)
_d_config = json.loads(open(_path_config, encoding='utf-8').read())['redis']


# redis 连接配置
_redis_config: dict = _d_config['redis_server']
# pub-sub 配置
_pub_sub_config: dict or None = _d_config.get('pubsub')
#

# 初始化  redis连接
# POOL = redis.ConnectionPool(
#     host=str(_redis_config['host']),
#     port=int(_redis_config['port']),
#     db=int(_redis_config['db'])
# )
REDIS = redis.StrictRedis(
    host=str(_redis_config['host']),
    port=int(_redis_config['port']),
    db=int(_redis_config['db'])
)


# 导入
# from .pubsub import RedisLoggerHandler, RedisSubTask


# ============  重要   ============
# 恢复‘当前路径’
os.chdir(path_chdir)
