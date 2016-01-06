# -*- coding: utf-8 -*-
__author__ = 'idbord'


class Quaternion:
    GO = "go"
    READ = "read"
    WRITE = "write"
    IN = "in"
    OUT = "out"
    INT = "int"
    DOUBLE = "double"
    ASSIGN = "assign"
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    GT = ">"
    GET = ">="
    LT = "<"
    LET = "<="
    EQ = "=="
    NEQ = "!="

    def __init__(self, first=None, second=None, third=None, forth=None):
        self._first = first
        self._second = second
        self._third = third
        self._forth = forth

    def get_first(self):
        return self._first

    def get_second(self):
        return self._second

    def get_third(self):
        return self._third

    def get_forth(self):
        return self._forth

    def set_first(self, first):
        self._first = first

    def set_second(self, second):
        self._second = second

    def set_third(self, third):
        self._third = third

    def set_forth(self, forth):
        self._forth = forth
