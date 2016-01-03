# -*- coding: utf-8 -*-
__author__ = 'idbord'
# 定义符号表元素类。


class SymbolItem:
    NULL = 0

    INT = 1
    DOUBLE = 2
    ARRAY_INT = 3
    ARRAY_DOU = 4
    BOOL = 5

    # 元素名，元素类型， 元素值， 元素层级， 指向元素下一个同名元素
    def __init__(self, s_name, s_type, s_value, s_level, s_next):
        self.name = s_name
        self.type = s_type
        self.value = s_value
        self.level = s_level
        self.next = s_next

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def get_level(self):
        return self.level

    def get_next(self):
        return self.next

    def set_name(self, s_name):
        self.name = s_name

    def set_type(self, s_type):
        self.name = s_type

    def set_value(self, s_value):
        self.name = s_value

    def set_level(self, s_level):
        self.name = s_level

    def set_next(self, s_next):
        self.name = s_next
