# -*- coding: utf-8 -*-
__author__ = 'idbord'
from cmm.lexer import Lexer
from cmm.parser import Parser
from cmm.generator import Generator
from cmm.interpreter import Interpreter


def interpreter(path):
    try:
        stream = open(path, 'r')
        codes = Generator.generate(Parser.parser_analysis(Lexer.lexer_analysis(stream)))
        stream.close()
        return Interpreter.interpret(codes)
    except Exception as e:
        print e

# interpreter()
