# -*- coding: utf-8 -*-
__author__ = 'idbord'

from cmm.lexer import Lexer


def lexer():
    try:
        path = "1.cmm"
        stream = open(path, 'r')
        token_list = Lexer.lexer_analysis(stream)
        stream.close()
        for i in token_list:
            print i.to_string_with_line()
    except Exception as e:
        print e

lexer()
