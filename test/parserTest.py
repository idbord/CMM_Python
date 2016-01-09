# -*- coding: utf-8 -*-
__author__ = 'idbord'
from cmm.lexer import Lexer
from cmm.parser import Parser


def parser(path):
    result = []
    try:
        stream = open(path, 'r')
        token_list = Lexer.lexer_analysis(stream)
        node_list = Parser.parser_analysis(token_list)
        stream.close()
        for i in node_list:
            result.append(i.to_string())
        return result
    except Exception as e:
        print e

