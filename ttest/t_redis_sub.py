import os
import json
import sys

# 第三方库


# 设置项目目录
PATH_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PATH_ROOT)
os.chdir(PATH_ROOT)
PATH_CONFIG = os.path.join(PATH_ROOT, 'Config', 'Config.json')
FILE_NAME = os.path.basename(__file__).replace('.py', '')
#
from pkgs.myredis.pubsub import RedisSubTask

# 改变标准输出的默认编码，cmd
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def main():
    # =============   读取config      =============
    d_config = json.loads(open(PATH_CONFIG, encoding='utf-8').read())
    # 是否发送redis
    is_warning_redis = d_config['is_use_redis']
    # 是否使用redis
    if is_warning_redis:
        # 实例化 redis subscriber
        redis_sub = RedisSubTask(channel=d_config['redis']['redis_server']['channel'])
        redis_sub.listen_task()


if __name__ == "__main__":
    # 启动
    main()
