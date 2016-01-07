# -*- coding: utf-8 -*-
__author__ = 'idbord'
from cmm.lexer import Lexer
from cmm.parser import Parser
from cmm.generator import Generator


def generator():
    try:
        path = "1.cmm"
        stream = open(path, 'r')
        codes = Generator.generate(Parser.parser_analysis(Lexer.lexer_analysis(stream)))
        stream.close()
        for i in codes:
            print i.to_string()
    except Exception as e:
        print e

generator()
