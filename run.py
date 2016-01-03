# -*- coding: utf-8 -*-
__author__ = 'idbord'
from cmm.util import Util
from exception import *
from model.token import Token


def run():
    try:
        # path = raw_input("输入文件路径")
        path = "test/1.cmm"
        token_list = Util.get_token_list(path)
        for i in token_list:
            print i.to_string_with_line()
    except Exception as e:
        print e

if __name__ == '__main__':
    run()
