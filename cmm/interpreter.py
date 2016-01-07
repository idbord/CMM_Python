# -*- coding: utf-8 -*-
__author__ = 'idbord'
import string

from model.symbol_table import SymbolTable
from model.quaternion import Quaternion
from exception.interpretException import ErrorInterpret


class Interpreter:

    def __init__(self):
        pass

    symbol_table = SymbolTable()
    scope_level = 0
    pc = 0

    @classmethod
    def quaternion_analysis(cls, quaternion):
        try:
            instr_type = quaternion.get_first()
            # 跳转
            if instr_type == Quaternion.GO:
                # 符合跳转条件
                if quaternion.get_second() is None or cls.symbol_table.get_symbol_value(quaternion.get_second().get_type()) == False:
                    cls.pc

        except ErrorInterpret("") as e:
            print(e.content)

    # 取值，1 , b[1]
    @classmethod
    def get_value(cls, str_id):
        try:
            if cls.is_array(str_id):
                return cls.symbol_table.get_symbol_value(cls.get_array_identify(str_id))
            elif str_id.__contains__('.'):
                return string.atof(str_id)
            else:
                return string.atoi(str_id)
        except ErrorInterpret as e:
            print(e.content)

    # 赋值，a = 2  a[2] = 2
    @classmethod
    def set_value(cls, str_id, value):
        try:
            index = cls.get_array_index(str_id) if cls.is_array(str_id) else -1
            symbol_type = cls.symbol_table.get_symbol_type(cls.get_identify(str_id))
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
        return int(str_id[0 : str_id.index("[")])
