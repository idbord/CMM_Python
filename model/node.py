# -*- coding: utf-8 -*-
__author__ = 'idbord'


class Node:
    def __init__(self):
        pass

    IF_STMT = 1
    '''
    if语句，left存exp表达式，middle存条件为True的子节点，right存条件为False时的子节点
    '''

    WHILE_STMT = 2
    '''
    while语句，left存exp表达式，middle存循环体
    '''

    BREAK_STMT = 3
    '''
    break语句，
    '''

    READ_STMT = 4
    '''
    read语句，left存exp表达式
    '''

    WRITE_STMT = 5
    '''
    write语句，left存exp表达式
    '''

    ASSIGN_STMT = 6
    '''
    赋值语句，left存var，middle存exp节点
    '''

    DECLARE_STMT = 7
    '''
    声明语句，left存var，middle存exp节点
    '''

    EXP = 8
    '''
    复合语句，
    '''

    VAR = 9
    '''
    变量，
    dataType存数据类型，Token.INT 或者 Token.DOUBLE
    value存放变量名
    声明语句中，left表示变量长度exp，调用中表示索引exp，默认为None，不表示数组
    '''

    OP = 10
    '''
    运算符，
    dataType存操作符类型，Token.PLUS，Token.MINUS，Token.MUL，Token.DIV，Token.MODE
    '''

    FACTOR = 11
    '''
    因子，有符号。
    dataType存类型，Toke.PLUS或Token.MINUS
    left存一个节点
    若为VAR，代表变量或数组
    若为LITERAL，代表该LITERAL的value中存的值
    EXP为因子时，mDataType存PLUS或MINUS
    '''

    LITERAL = 12
    '''
    字面值，无符号
    dataType存类型
    '''

    def __init__(self, n_type, value, m_next, m_data_type, m_left, m_middle, m_right):
        self._type = n_type
        self._value = value
        self._mNext = m_next
        self._mDataType = m_data_type
        self._mLeft = m_left
        self._mMiddle = m_middle
        self._mRight = m_right

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def get_next(self):
        return self._mNext

    def get_data_type(self):
        return self._mDataType

    def get_left(self):
        return self._mLeft

    def get_middle(self):
        return self._mMiddle

    def get_right(self):
        return self._mRight

    def set_type(self, n_type):
        self._type = n_type

    def set_value(self, value):
        self._value = value

    def set_next(self, m_next):
        self._mNext = m_next

    def set_data_type(self, m_data_type):
        self._mDataType = m_data_type

    def set_left(self, left):
        self._mLeft = left

    def set_middle(self, middle):
        self._mMiddle = middle

    def set_right(self, right):
        self._mRight = right

    def to_string(self):
        try:
            if self._type == Node.IF_STMT:
                return "IF_STMT"
            if self._type == Node.WHILE_STMT:
                return "WHILE_STMT"
            if self._type == Node.READ_STMT:
                return "READ_STMT"
            if self._type == Node.WRITE_STMT:
                return "WRITE_STMT"
            if self._type == Node.ASSIGN_STMT:
                return "ASSIGN_STMT"
            if self._type == Node.DECLARE_STMT:
                return "DECLARE_STMT"
            if self._type == Node.EXP:
                return "EXP"
            if self._type == Node.VAR:
                return "VAR"
            if self._type == Node.OP:
                return "OP"
            if self._type == Node.FACTOR:
                return "FACTOR"
            if self._type == Node.LITERAL:
                return "LITERAL"
        except Exception as e:
            print e
