import os
import json
import datetime
import time
import collections
import csv
import sys

# 第三方库
import redis

# 设置项目目录
PATH_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PATH_ROOT)
os.chdir(PATH_ROOT)
PATH_CONFIG = os.path.join(PATH_ROOT, 'Config', 'Config.json')
FILE_NAME = os.path.basename(__file__).replace('.py', '')

# 导入我的模块
from pkgs.tradingsession.atsts import TradingSession
from pkgs.logger import MyLogger
from pkgs.atsdata import ticker_to_product
from pkgs.TradingPlatform_WarningBoard import run_warning_board

# 改变标准输出的默认编码，cmd
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


"""
"""


# redis


# 检查 bar 数据
def check_bar_data(file_path, product_trading_session: TradingSession, s_date):
    with open(file_path) as f:
        l_lines = f.readlines()

    # 记录bar data file 中bar的时
    l_s_trading_session = []
    for line in l_lines:
        try:
            l_split = line.split(',')
            time = l_split[0]
            o = l_split[1]
            h = l_split[2]
            l = l_split[3]
            c = l_split[4]
            v = l_split[5]
            p = l_split[6]
            oi = l_split[7]
        except:
            logger.error(f'{file_path} \t file parse error')
            return
        else:
            l_s_trading_session.append(time)
    obj_trading_session = TradingSession.from_str_list(l_s_trading_session, format='%H:%M:%S')
        
    # 对比
    d_trading_session = product_trading_session.difference(obj_trading_session)

    # 报错
    if len(d_trading_session) > 0:
        logger.warning(f'缺少数据，{file_path}, 共 %s 条,\t %s' % (
            len(d_trading_session),
            ','.join([TradingSession.timestamp_to_time(ts).strftime('%H:%M:%S') for ts in d_trading_session])
        ))
        

# 读取mostActiveTicker.csv
# -> d_target_ticker = { product: {date: ticker}, }
def get_target_ticker(most_act_ticker_file, target_exchange, skip_product) -> dict:
    d_target_ticker = collections.defaultdict(dict)

    with open(most_act_ticker_file, encoding='gb2312') as f:
        l_lines = f.readlines()
    for line in l_lines:
        line = line.strip()
        if line == '':
            continue
        l_split = line.split(',')
        if len(l_split) < 3:
            continue

        s_date = l_split[0]
        s_product = l_split[1]
        s_ticker = l_split[2]

        s_exchange = s_product.split('.')[-1]
        if s_exchange not in target_exchange:
            continue
        if s_product in skip_product:
            continue

        d_target_ticker[s_product][s_date] = s_ticker
    
    return d_target_ticker


# 读取product trading_session
# { product: TradingSession }
def get_trading_session(path_trading_session) -> dict:
    d_product_ts = {}
    with open(path_trading_session) as f:
        f.readline()    # 去掉首行
        reader = csv.reader(f)
        # 逐行读取
        # eg: 20010101,a.DCE,090000-101500&103000-113000&133000-150000,,210,DCE
        for l_line in reader:
            l_trading_session = []
            if len(l_line) < 3:
                continue
            product_name = l_line[1]
            s_trading_session = l_line[2]
            
            l_trading_session = [
                [s_e.split('-')[0], s_e.split('-')[-1]]
                for s_e in s_trading_session.split('&')
            ]
            d_product_ts[product_name] = TradingSession.from_session_range(l_trading_session)
    return d_product_ts


# 检查流程
def check(
        path, start_date: int, product_trading_session, d_target_ticker,
        end_date: int or None = None, **kwargs
):
    # 遍历ds-bar目录
    # 不同日期，folder_name_date
    # print(end_date)
    for folder_name_date in os.listdir(path):
        path_date_folder = os.path.join(path, folder_name_date)
        if not os.path.isdir(path_date_folder):
            continue
        if not folder_name_date.isdigit():
            continue
        if int(folder_name_date) < start_date:
            continue
        if end_date:
            if int(folder_name_date) > end_date:
                continue
        s_date = str(folder_name_date)
        
        logger.info(f'Checking {folder_name_date}')
        # 这一天我应该检查哪一些ticker
        l_td_target_ticker = []
        for product, d_date_ticker in d_target_ticker.items():
            l_date = [mat_d for mat_d in d_date_ticker.keys() if mat_d <= folder_name_date]
            if len(l_date) == 0:
                continue
            key_date = max(l_date)
            l_td_target_ticker.append(d_date_ticker[key_date])
        
        # 遍历这一天所有的 ticker的 bar data
        for n, td_target_ticker in enumerate(l_td_target_ticker):
            path_target_file = os.path.join(
                path_date_folder,
                '%s.csv' % td_target_ticker
            )
            if not os.path.exists(path_target_file):
                continue
            product = ticker_to_product(td_target_ticker)

            # 单个file检查
            check_bar_data(
                file_path=path_target_file, 
                product_trading_session=product_trading_session[product],
                s_date=s_date
            )


def main():
    # =============   读取config      =============
    d_config = json.loads(open(PATH_CONFIG, encoding='utf-8').read())

    check_exchange = d_config.get('check_exchange')     # 检查哪些 交易所
    skip_product = d_config.get('skip_product')         # 需要跳过的product
    # 检查时间    检查'今天' 或   规定 起始日期
    is_today = d_config.get('today')
    if is_today is True:
        start_date = int(datetime.datetime.today().strftime('%Y%m%d'))
        end_date = start_date
    else:
        start_date = int(d_config.get('start_date'))
        end_date = d_config.get('end_date')
    # 路径目录
    path_ds = os.path.abspath(d_config.get('ds_root'))
    path_mat = os.path.abspath(d_config.get('path_mat'))        # 主力合约 MostActiveTicker.csv
    path_trading_session = os.path.abspath(d_config.get('path_trading_session'))        # TradingSession.csv
    # 是否弹框报错
    is_warning_board = d_config['is_warning_board']
    # 是否发送redis
    is_warning_redis = d_config['is_use_redis']
    if is_warning_redis:
        from pkgs.myredis.pubsub import RedisLoggerHandler
        logger.addHandler(RedisLoggerHandler(script_name=FILE_NAME))         # 添加到  logger

    # ============= 主程序      =============
    # 【1】读取MostActTicker.csv
    # 只检查主力合约
    # d_target_ticker = { product: {date: ticker}, }
    d_target_ticker: dict = get_target_ticker(
        most_act_ticker_file=path_mat,
        target_exchange=check_exchange,
        skip_product=skip_product
    )
    # 【2】读取tradingSession.csv
    # 规定不同product的 交易时间
    # { product: TradingSession }
    d_product_ts: dict = get_trading_session(path_trading_session=path_trading_session)

    # 【3】检查
    d = {}
    if end_date:
        d['end_date'] = int(end_date)
    check(
        path=path_ds,
        start_date=start_date,
        d_target_ticker=d_target_ticker,
        product_trading_session=d_product_ts,
        **d
    )

    t_e = time.time()
    logger.info('Finished')
    logger.info('用时: %s s' % round(t_e - t_s))

    # ===============    警告  ======================
    # 检测是否有warning，有则弹框
    if is_warning_board:
        count_warning = logger.count.get('WARNING')
        if count_warning:
            if count_warning > 0:
                run_warning_board(container_name='DSBarChecker', label_text='DS Bar Error')


if __name__ == "__main__":
    path_logs = os.path.join(PATH_ROOT, 'logs')
    if not os.path.exists(path_logs):
        os.makedirs(path_logs)

    # 配置logging
    logger = MyLogger(name=FILE_NAME, is_file=True, output_root=path_logs)

    # 启动
    t_s = time.time()
    logger.info('Start')
    main()
