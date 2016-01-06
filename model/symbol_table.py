# -*- coding: utf-8 -*-
__author__ = 'idbord'
from model.symbol_item import SymbolItem
from model.value import Value
from exception.interpretException import ErrorInterpret


class SymbolTable:

    def __init__(self):
        pass

    TEMP_PREFIX = "*temp"

    symbolTable = __init__()
    tempNames = []
    symbolList = []


    @classmethod
    def new_table(cls):
        cls.tempNames = []
        cls.symbolList = []

    '''
    返回符号表对象
    单例，可能不完善
    '''
    @classmethod
    def get_symbol_table(cls):
        return cls.symbolTable

    '''
    清空符号表
    '''
    @classmethod
    def delete_table(cls):
        if cls.tempNames is not []:
            cls.tempNames = []
        if cls.symbolList is not []:
            cls.symbolList = []

    '''
    向符号表尾部插入新的符号对象
    '''
    @classmethod
    def insert(cls, symbol):
        try:
            for i in cls.symbolList:
                if i.get_name() == symbol.get_name():
                    if i.get_level() < symbol.get_level():
                        symbol.set_next(i)
                        cls.symbolList[cls.symbolList.index(i)] = symbol
                        return
                    raise ErrorInterpret("变量：" + symbol.get_name() + "重复声明")
            cls.symbolList.append(symbol)
        except ErrorInterpret as e:
            print(e.content)

    '''
    从符号表删除符号
    '''
    @classmethod
    def pop(cls, level):
        for i in cls.symbolList:
            if i.get_level() == level:
                cls.symbolList[cls.symbolList.index(i)] = i.get_next()
        for i in cls.symbolList:
            if i.get_next() is None:
                cls.symbolList.pop(cls.symbolList.index(i))

    '''
    返回符号对象
    '''
    @classmethod
    def get_symbol(cls, name):
        try:
            for i in cls.symbolList:
                if i.get_name() == name:
                    return i
            for j in cls.tempNames:
                if j.get_name() == name:
                    return j
            if name.startswith(cls.TEMP_PREFIX):
                k = SymbolItem(s_name=name, s_type=SymbolItem.TEMP, s_value=Value(SymbolItem.TEMP), s_level=-1)
                cls.tempNames.append(k)
                return k
            raise ErrorInterpret("变量" + name + "未定义")
        except ErrorInterpret as e:
            print e.content

    '''
    返回临时符号
    '''
    @classmethod
    def get_temp_symbol(cls):
        try:
            i = 1
            while True:
                temp = cls.TEMP_PREFIX + str(i)
                i += 1
                exist = False
                for j in cls.tempNames:
                    if j.get_name() == temp:
                        exist = True
                        break
                for k in cls.symbolList:
                    if k.get_name() == temp:
                        exist = True
                        break
                if exist:
                    continue
                s = SymbolItem(s_name=temp, s_type=SymbolItem.TEMP, s_value=Value(SymbolItem.TEMP), s_level=-1)
                cls.tempNames.append(s)
                return s
        except ErrorInterpret as e:
            print(e.content)

    '''
    清空临时符号列表
    '''
    @classmethod
    def clear_temp_name(cls):
        cls.tempNames = []

    '''
    返回符号值
    '''
    @classmethod
    def get_symbol_value(cls, name, index=-1):
        symbol = cls.get_symbol(name)
        if index == -1:
            return symbol.get_value()
        if len(symbol.get_value().get_value()) < index+1:
            raise ErrorInterpret("数组" + name + "越界")
        if symbol.get_type() in [SymbolItem.ARRAY_INT, SymbolItem.ARRAY_DOU]:
            value = Value(SymbolItem.ARRAY_INT)
            value.set_value(symbol.get_value().get_value()[index])
            return value

    '''
    返回符号类型
    '''
    @classmethod
    def get_symbol_type(cls, name):
        return cls.get_symbol(name).get_type()()

    '''
    设置符号值
    '''
    @classmethod
    def set_symbol_value(cls, name, value, index=-1):
        try:
            symbol = cls.get_symbol(name)
            if index == -1:
                symbol.set_value(value)
                return
            if len(symbol.get_value().get_value()) < index + 1:
                raise ErrorInterpret("数组" + name + "越界")
            if symbol.get_type() in [SymbolItem.ARRAY_INT, SymbolItem.ARRAY_DOU]:
                symbol.get_value().get_value()[index] = value
        except ErrorInterpret as e:
            print(e.content)

