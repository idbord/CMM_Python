# -*- coding: utf-8 -*-
__author__ = 'idbord'
# 定义符号类。


class SymbolItem:
    TEMP = 0

    INT = 1
    DOUBLE = 2
    ARRAY_INT = 3
    ARRAY_DOU = 4
    BOOL = 5

    # 元素名，元素类型， 元素值， 元素层级， 指向元素下一个同名元素
    def __init__(self, s_name=None, s_type=None, s_value=None, s_level=None, s_next=None):
        self._name = s_name
        self._type = s_type
        self._value = s_value
        self._level = s_level
        self._next = s_next

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def get_level(self):
        return self._level

    def get_next(self):
        return self._next

    def set_name(self, s_name):
        self._name = s_name

    def set_type(self, s_type):
        self._type = s_type

    def set_value(self, s_value):
        self._value = s_value

    def set_level(self, s_level):
        self._level = s_level

    def set_next(self, s_next):
        self._next = s_next
