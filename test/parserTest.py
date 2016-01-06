# -*- coding: utf-8 -*-
__author__ = 'idbord'
from cmm.lexer import Lexer
from cmm.parser import Parser


def parser():
    try:
        path = "1.cmm"
        stream = open(path, 'r')
        token_list = Lexer.lexer_analysis(stream)
        node_list = Parser.parser_analysis(token_list)
        stream.close()
        for i in node_list:
            print i.to_string()
    except Exception as e:
        print e

parser()
