# coding=utf-8
from src import SrcUnit
from dest import DesUnit
import zxz_utils
import os
from requests.exceptions import ConnectionError


def main():
    try:
        config = zxz_utils.get_config()
        src = SrcUnit()
        task = src.get_tasks(zxz_utils.get_last_day())
        out = DesUnit(config['username'], config['password'])
        for i in task:
            out.insert_day_task(i)
        print("搞定了")
    except ConnectionError:
        print("连不上Google翻译，自己手动添加或重新来一次")
    except:
        print("出错了，检查后台以后，自己手动添加或重新来一次")
        pass


if __name__ == '__main__':
    main()
    os.system('pause')
    pass


