# coding=utf-8
from src import SrcUnit
from dest import DesUnit
import zxz_utils
import os


def main():
    try:
        src = SrcUnit()
        task = src.get_tasks(zxz_utils.get_last_day())
        out = DesUnit()
        for i in task:
            out.insert_day_task(i)
        print("搞定了")
    except:
        print("出错了，检查后台以后，自己手动添加或重新来一次")
        pass


if __name__ == '__main__':
    main()
    os.system('pause')
    pass


