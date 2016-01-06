# -*- coding: utf-8 -*-
__author__ = 'idbord'
from model.token import Token


class ErrorParse(Exception):
    def __init__(self, line_num, t_type):
        Exception.__init__(self)
        self.content = 'line .' + str(line_num) + ':next token should be ' + Token(t_type).to_string()
