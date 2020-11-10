import os
import datetime
import time
from collections.abc import Iterable
# import logger


class TradingSession:

    def __init__(self, data: list):
        if _check_is_timestamp(data):
            self._data: list = list(set(data))
            self._data.sort()
        else:
            raise TypeError()
    
    @property
    def data(self):
        return self._data

    def __getitem__(self, position):
        return self._data[position]

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return self._data.__repr__()

    # 可迭代，列表
    def __iter__(self):
        return iter(self._data)

    # 可加减
    def __add__(self, other):
        if type(other) is not TradingSession:
            raise TypeError
        else:
            return TradingSession(data=list(set(self.data+other.data)))
    __radd__ = __add__

    # def __sub__(self, other):
    #     if type(other) is not TradingSession:
    #         raise TypeError
    #     else:
    #         pass

    def difference(self, other):
        return TradingSession(
            data=list(set(self.data).difference(other.data))
        )

    # [time, ] -> TradingSession
    @classmethod
    def from_str_list(cls, l, format='%H%M%S'):
        l_ts = [
            TradingSession.to_timestamp(datetime.datetime.strptime(s_t, format).time())
            for s_t in l
        ]
        return TradingSession(l_ts)

    # start= end=, -> TradingSession
    @classmethod
    def from_session_range(cls, l_start_end_range: list, format='%H%M%S', freq='M', right_close=False, left_close=False):
        l_ts = []
        for range_i in l_start_end_range:
            start = range_i[0]
            end = range_i[-1]
            t_start = datetime.datetime.strptime(start, format).time()
            t_end = datetime.datetime.strptime(end, format).time()

            ts_start = TradingSession.to_timestamp(t=t_start)
            ts_end = TradingSession.to_timestamp(t=t_end)

            ts_step = {
                'H': 60 * 60,
                'M': 60,
                'S': 1
            }[freq]

            if right_close:
                ts_end_c = ts_end + ts_step
            else:
                ts_end_c = ts_end
            if left_close:
                ts_start_c = ts_start
            else:
                ts_start_c = ts_start + ts_step
            l_ts = list(set(l_ts + [i for i in range(ts_start_c, ts_end_c - 1, ts_step)]))
        return TradingSession(l_ts)

    @classmethod
    def to_timestamp(cls, t: datetime.datetime.time) -> int:
        return t.hour * 60 * 60 + t.minute * 60 + t.second

    @classmethod
    def timestamp_to_time(cls, t: int) -> datetime.datetime.time:
        hour = int(t / 60 / 60)
        minute = int((t - hour * 60 * 60) / 60)
        second = int(t - hour * 60 * 60 - minute * 60)
        return datetime.time(hour=hour, minute=minute, second=second)


def _check_is_timestamp(l) -> bool:
    if type(l) is str:
        return False
    elif type(l) is int or type(l) is float:
        return 0 <= (l / 60 / 60) <= 24
    if isinstance(l, Iterable):
        return all([0 <= (i / 60 / 60) <= 24 for i in l])
    else:
        return False


# if __name__ == "__main__":
#     d = TradingSession.from_str_list(['090000', '090100', '091032'])
#     for i in d:
#         print(i)
