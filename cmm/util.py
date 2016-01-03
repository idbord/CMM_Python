# -*- coding: utf-8 -*-
__author__ = 'idbord'
from cmm.lexer import Lexer
from cmm.parser import Parser


class Util:
    @classmethod
    def get_token_list(cls, path):
        try:
            stream = open(path, 'r')
            token_list = Lexer.lexer_analysis(stream)
            stream.close()
            return token_list
        except IOError as e:
            print e

    @classmethod
    def get_node_list(cls, token_list):
        try:
            nodelist = Parser.parser_analysis(token_list)
            return nodelist
        except Exception as e:
            print e
