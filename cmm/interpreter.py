# -*- coding: utf-8 -*-
__author__ = 'idbord'
import string
import re

from model.symbol_table import SymbolTable
from model.quaternion import Quaternion
from model.symbol_item import SymbolItem
from model.value import Value
from exception.interpretException import ErrorInterpret


class Interpreter:

    def __init__(self):
        pass

    symbol_table = SymbolTable()
    scope_level = 0
    pc = 0
    result = []

    @classmethod
    def interpret(cls, quaternions):
        try:
            cls.symbol_table.new_table()
            while cls.pc < len(quaternions):
                cls.quaternion_analysis(quaternions[cls.pc])
            cls.symbol_table.delete_table()
            temp = cls.result
            cls.pc = 0
            cls.scope_level = 0
            cls.result = []
            return temp
        except Exception as e:
            print(e)

    @classmethod
    def quaternion_analysis(cls, quaternion):
        try:
            instr_type = quaternion.get_first()
            # 跳转
            if instr_type == Quaternion.GO:
                # 符合跳转条件
                if quaternion.get_second() is None or cls.symbol_table.get_symbol_value(quaternion.get_second()).get_value() == False:
                    cls.pc = cls.get_value(quaternion.get_forth()).get_value()
                    return
            elif instr_type == Quaternion.READ:
                input_content = raw_input()
                req_type = cls.symbol_table.get_symbol_type(cls.get_identify(quaternion.get_forth()))
                if req_type in [SymbolItem.INT, SymbolItem.ARRAY_INT]:
                    value = cls.parse_input(input_content)
                    if value.get_type() == SymbolItem.INT:
                        cls.set_value(quaternion.get_forth(), value)
                    else:
                        raise ErrorInterpret("输入类型不匹配")
                elif req_type in [SymbolItem.DOUBLE, SymbolItem.ARRAY_DOU]:
                    value = cls.parse_input(input_content)
                    cls.set_value(quaternion.get_forth(), value)
            elif instr_type == Quaternion.WRITE:
                index = -1
                if cls.is_array(quaternion.get_forth()):
                    index = cls.get_array_index(quaternion.get_forth())
                cls.result.append(cls.symbol_table.get_symbol_value(quaternion.get_forth(), index).get_value())
            elif instr_type == Quaternion.IN:
                cls.scope_level += 1
            elif instr_type == Quaternion.OUT:
                cls.symbol_table.pop(cls.scope_level)
                cls.scope_level -= 1
            elif instr_type == Quaternion.INT:
                if quaternion.get_third() is not None:
                    symbol = SymbolItem(quaternion.get_forth(), SymbolItem.ARRAY_INT, s_level=cls.scope_level)
                    symbol.get_value().set_value(quaternion.get_third())  # maybe not work
                    cls.symbol_table.insert(symbol)
                else:
                    int_value = 0
                    if quaternion.get_second() is not None:
                        int_value = Value(SymbolItem.INT, int(quaternion.get_second()))
                    symbol = SymbolItem(quaternion.get_forth(), SymbolItem.INT, int_value, cls.scope_level)
                cls.symbol_table.insert(symbol)
            elif instr_type == Quaternion.DOUBLE:
                if quaternion.get_third() is not None:
                    symbol = SymbolItem(quaternion.get_forth(), SymbolItem.ARRAY_DOU, s_level=cls.scope_level)
                    symbol.get_value().set_value(quaternion.get_third())  # maybe not work
                    cls.symbol_table.insert(symbol)
                else:
                    int_value = 0
                    if quaternion.get_second() is not None:
                        int_value = Value(SymbolItem.INT, int(quaternion.get_second()))
                    symbol = SymbolItem(quaternion.get_forth(), SymbolItem.DOUBLE, int_value, cls.scope_level)
                cls.symbol_table.insert(symbol)
            elif instr_type == Quaternion.ASSIGN:
                value = cls.get_value(quaternion.get_second())
                cls.set_value(quaternion.get_forth(), value)
            elif instr_type == Quaternion.PLUS:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).plus(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.MINUS:
                if quaternion.get_third() is not None:
                    cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).minus(cls.get_value(quaternion.get_third())))
                else:
                    cls.set_value(quaternion.get_forth(), Value.negative(cls.get_value(quaternion.get_second())))
            elif instr_type == Quaternion.MUL:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).multiple(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.DIV:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).division(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.GT:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).greater(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.GET:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).greater_equal(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.LT:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).less(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.LET:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).less_equal(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.EQ:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).equal(cls.get_value(quaternion.get_third())))
            elif instr_type == Quaternion.NEQ:
                cls.set_value(quaternion.get_forth(), cls.get_value(quaternion.get_second()).not_equal(cls.get_value(quaternion.get_third())))
            cls.pc += 1
        except ErrorInterpret as e:
            print(e.content)

    # 取值，1 , b[1]
    @classmethod
    def get_value(cls, str_id):
        try:

            if type(str_id) == float:
                value = Value(SymbolItem.DOUBLE, str_id)
                return value
            elif type(str_id) == int:
                value = Value(SymbolItem.INT, str_id)
                return value
            index = -1
            if cls.is_array(str_id):
                index = cls.get_array_index(str_id)
            return cls.symbol_table.get_symbol_value(cls.get_identify(str_id), index)
        except ErrorInterpret as e:
            print(e.content)

    # 赋值，a = 2  a[2] = 2
    @classmethod
    def set_value(cls, str_id, value):
        try:
            index = cls.get_array_index(str_id) if cls.is_array(str_id) else -1
            ident = cls.get_identify(str_id)
            symbol_type = cls.symbol_table.get_symbol_type(ident)
            if symbol_type == SymbolItem.INT:
                if value.get_type() == SymbolItem.INT:
                    cls.symbol_table.set_symbol_value(ident, value)
                elif value.get_type() == SymbolItem.DOUBLE:
                    raise ErrorInterpret("表达式{0}与变量类型不匹配".format(str_id))
            elif symbol_type == SymbolItem.DOUBLE:
                cls.symbol_table.set_symbol_value(ident, value.to_double())
            elif symbol_type == SymbolItem.ARRAY_INT:
                if cls.symbol_table.get_symbol_value(ident, index).get_type() == SymbolItem.ARRAY_INT:
                    cls.symbol_table.set_symbol_value(ident, value.get_value(), index)
                else:
                    raise ErrorInterpret("表达式{0}与变量类型不匹配".format(str_id))
            elif symbol_type == SymbolItem.ARRAY_DOU:
                cls.symbol_table.set_symbol_value(ident, float(value.get_value()), index)
            elif symbol_type == SymbolItem.TEMP:
                cls.symbol_table.set_symbol_value(ident, value)
        except ErrorInterpret as e:
            print(e.content)

    @classmethod
    def is_array(cls, str_id):
        return str_id.endswith("]")

    @classmethod
    def get_array_index(cls, str_id):
        return int(str_id[str_id.index("[") + 1: str_id.index("]")])

    @classmethod
    def get_identify(cls, str_id):
        if cls.is_array(str_id):
            return int(str_id[0: str_id.index("[")])
        return str_id

    @classmethod
    def parse_input(cls, content):
        try:
            if re.match('-?([0-9]+.[0-9]+)', content):
                value = Value(SymbolItem.DOUBLE, string.atof(content))
                return value
            elif re.match('-?[0-9]+]', content):
                value = Value(SymbolItem.INT, string.atoi(content))
                return value
            raise ErrorInterpret("输入非法")
        except ErrorInterpret as e:
            print(e.content)