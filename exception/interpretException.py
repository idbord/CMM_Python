# -*- coding: utf-8 -*-
__author__ = 'idbord'


class ErrorInterpret(Exception):
    def __init__(self, content=None):
        Exception.__init__(self)
        self.content = content
