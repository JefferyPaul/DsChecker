# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 14:10
# @Author  : Jeffery Paul
# @File    : signal.py


import datetime


# TODO 可以参考 logger.format 进行优化

# SignalGroup = namedtuple()


class RedisSignal(object):
    def __init__(
            self,
            address,
            script_name,
            msg,
            levelname=''
    ):
        self._level = levelname
        self._signal = '%s,%s,%s,%s:%s' % (
            datetime.datetime.now().strftime('%Y%m%d %H%M%S'),
            str(self._level),
            str(address),
            str(script_name),
            str(msg)
        )

    def __str__(self):
        return self._signal

    def __repr__(self) -> str:
        return self._signal

