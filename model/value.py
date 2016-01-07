# -*- coding: utf-8 -*-
__author__ = 'idbord'
import re

from model.symbol_item import SymbolItem
from exception.semanticException import ErrorSemantic

# 存储符号表中符号对应的值,包括int real 以及数组符号对应的值


class Value:
    # 存储该值对象的类型，常量存储在符号表中
    # 值对象
    def __init__(self, v_type=SymbolItem.TEMP, v_value=None):
        self._v_type = v_type
        self._v_value = v_value

    def get_type(self):
        return self._v_type

    def get_value(self):
        return self._v_value

    def set_type(self, v_type):
        self._v_type = v_type

    def set_value(self, v_value):
        self._v_value = v_value

    def plus(self, value_obj):
        try:
            if self._v_type == SymbolItem.INT:
                if value_obj.get_type() == SymbolItem.DOUBLE:
                    v_o = Value(SymbolItem.DOUBLE, self._v_value + value_obj.get_value())
                    return v_o
                elif value_obj.get_type() == SymbolItem.INT:
                    v_o = Value(SymbolItem.INT, self._v_value + value_obj.get_value())
                    return v_o
            elif self._v_type == SymbolItem.DOUBLE:
                v_o = Value(SymbolItem.DOUBLE, self._v_value + value_obj.get_value())
                return v_o
        except ErrorSemantic("运算错误") as e:
            print e.content

    def minus(self, value_obj):
        try:
            if self._v_type == SymbolItem.INT and value_obj.get_type() == SymbolItem.INT:
                v_o = Value(SymbolItem.INT, self._v_value - value_obj.get_value())
                return v_o
            v_o = Value(SymbolItem.DOUBLE, self._v_value - value_obj.get_value())
            return v_o
        except ErrorSemantic("运算错误") as e:
            print e.content

    def multiple(self, value_obj):
        try:
            if self._v_type == SymbolItem.INT and value_obj.get_type() == SymbolItem.INT:
                v_o = Value(SymbolItem.INT, self._v_value * value_obj.get_value())
                return v_o
            to_add_value = value_obj.get_value()
            mul_length = len(re.search('[0-9]+[.](\d+)', str(to_add_value)).group(1)) + len(re.search('[0-9]+[.](\d+)', str(self._v_value)).group(1))
            result = self._v_value * value_obj.get_value()
            result_length = len(re.search('[0-9]+[.](\d+)', str(result)).group(1))
            result_value = round(result_length, mul_length) if result_length > mul_length else result
            v_o = Value(SymbolItem.DOUBLE, result_value)
            return v_o
        except ErrorSemantic("运算错误") as e:
            print e.content

    def division(self, value_obj):
        try:
            if value_obj.get_value() == 0:
                raise ErrorSemantic("语法错误，不能除以0")
            elif self._v_type == SymbolItem.INT and value_obj.get_type() == SymbolItem.INT:
                v_o = Value(SymbolItem.INT, self._v_value / value_obj.get_value())
                return v_o
            v_o = Value(SymbolItem.DOUBLE, self._v_value / value_obj.get_value())
            return v_o
        except ErrorSemantic as e:
            print e.content

    def equal(self, value_obj):
        try:
            v_o = Value(SymbolItem.BOOL, self._v_value == value_obj.get_value())
            return v_o
        except ErrorSemantic("逻辑运算错误") as e:
            print e.content

    def greater(self, value_obj):
        try:
            v_o = Value(SymbolItem.BOOL, self._v_value > value_obj.get_value())
            return v_o
        except ErrorSemantic("逻辑运算错误") as e:
            print e.content

    def greater_equal(self, value_obj):
        try:
            v_o = Value(SymbolItem.BOOL, self.greater(value_obj) or self.equal(value_obj))
            return v_o
        except ErrorSemantic("逻辑运算错误") as e:
            print e.content

    @classmethod
    def negative(cls, value_obj):
        try:
            value_obj_type = value_obj.get_type()
            if value_obj_type == SymbolItem.BOOL:
                value = False if value_obj.get_value() else True
                value_obj.set_value(value)
                return value_obj
            elif value_obj_type in [SymbolItem.INT, SymbolItem.DOUBLE, SymbolItem.ARRAY_INT, SymbolItem.ARRAY_DOU]:
                value_obj.set_value(value_obj.get_value() * -1)
                return value_obj
        except ErrorSemantic("负号使用错误") as e:
            print e.content

    def not_equal(self, value_obj):
        return Value.negative(self.equal(value_obj))

    def less(self, value_obj):
        return Value.negative(self.greater(value_obj))

    def less_equal(self, value_obj):
        return Value.negative(self.greater_equal(value_obj))

    def to_string(self):
        return str(self._v_value)
