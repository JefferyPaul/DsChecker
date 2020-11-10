# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 14:37
# @Author  : Jeffery Paul
# @File    : t_redis_pub.py


from pkgs.myredis.pubsub import pub_msg
import time


def t1():
    pub_msg(
        msg='hello',
        script_name='_test.py'
    )
    time.sleep(1)

    pub_msg(
        msg='1',
        script_name='_test.py'
    )
    time.sleep(1)

    pub_msg(
        msg='3',
        script_name='1.py'
    )
    time.sleep(1)
    pub_msg(
        msg='5',
        script_name='_test.py'
    )

    time.sleep(1)
    pub_msg(
        msg='4',
        script_name='_test.py'
    )
    time.sleep(1)
    pub_msg(
        msg='9',
        script_name='_test1.py'
    )


def t2():
    from pkgs.myredis.pubsub import RedisLoggerHandler
    from pkgs.logger import MyLogger

    logger = MyLogger(name='test', is_file=True, output_root='.\\')
    logger.addHandler(RedisLoggerHandler(script_name='test1'))
    logger.info('In')
    logger.warning('HelloWord')
    logger.error('Error')


if __name__ == '__main__':
    t2()
