# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 17:38
# @Author  : Jeffery Paul
# @File    : running.py.py


import os
import subprocess


"""
方便在调用py中调用外部的 TradingPlatform.WarningBoard 工具
"""

PATH_EXE = os.path.join(
    os.path.dirname(__file__),
    'TradingPlatform.WarningBoard',
    'TradingPlatform.WarningBoard.exe'
)
PATH_CONFIG = os.path.join(
    os.path.dirname(__file__),
    'TradingPlatform.WarningBoard',
    'Configuration',
    'TradingPlatform.WarningBoard.txt'
)


# 修改配置文件
# TradingPlatform.WarningBoard//Configuration//TradingPlatform.WarningBoard.txt
def set_wb_config(container_name='', label_text=''):
    def write():
        with open(PATH_CONFIG, 'w', encoding='utf-8') as f:
            f.write('ContainerName=%s\nLabelText=%s' % (d['ContainerName'], d['LabelText']))

    d = dict()
    if container_name:
        d['ContainerName'] = container_name
    if label_text:
        d['LabelText'] = label_text
    if container_name and label_text:
        write()
    else:
        with open(PATH_CONFIG, 'r') as f:
            init_lines = f.readlines()
        d_f = {}
        for line in init_lines:
            line = line.strip()
            if line == '':
                continue
            d_f[line.split('=')[0]] = line.split('=')[1]
        # 读取信息
        if not container_name:
            d['ContainerName'] = d_f['ContainerName']
        if not label_text:
            d['LabelText'] = d_f['LabelText']
        write()


def run_warning_board(container_name='', label_text=''):
    if container_name or label_text:
        set_wb_config(container_name=container_name, label_text=label_text)

    try:
        p = subprocess.Popen(
            PATH_EXE,
            stdout=subprocess.PIPE, shell=True,
            cwd=os.path.dirname(PATH_EXE)
        )
        output_s = p.stdout.read().decode('utf-8', 'ignore')
    except Exception as e:
        print('\n调用 TradingPlatform.WarningBoard 失败:\n')
        print(e)
        raise e
    else:
        if 'Exception' in output_s:
            print('\n调用 TradingPlatform.WarningBoard 失败:\n')
            raise Exception
