# -*- coding: utf-8 -*-
__author__ = 'idbord'

from cmm.lexer import Lexer


def lexer(path):
    result = []
    try:
        stream = open(path, 'r')
        token_list = Lexer.lexer_analysis(stream)
        stream.close()
        for i in token_list:
            result.append(i.to_string_with_line())
        return result
    except Exception as e:
        print e
