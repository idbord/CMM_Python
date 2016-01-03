# -*- coding: utf-8 -*-
__author__ = 'idbord'


class Token:
    # int
    INT = 1
    # double
    DOUBLE = 2

    # if
    IF = 3
    # else
    ELSE = 4
    # while
    WHILE = 5
    # read
    READ = 6
    # write
    WRITE = 7
    # =
    ASSIGN = 8
    # break
    BREAK = 9

    # simple operations
    # +
    PLUS = 10
    # -
    MINUS = 11
    # *
    MUL = 12
    # /
    DIV = 13
    # %
    MODE = 14

    # logic operations
    # <
    LT = 15
    # <=
    LET = 16
    # >
    GT = 17
    # >=
    GET = 18
    # ==
    EQ = 19
    # !=
    NEQ = 20

    # (
    LPARENT = 21
    # )
    RPARENT = 22
    # [
    LBRACKET = 23
    # ]
    RBRACKET = 24
    # {
    LBRACE = 25
    # }
    RBRACE = 26

    # ;
    SEMI = 27
    # ,
    COMMA = 28

    # 标识符,由数字,字母或下划线组成,第一个字符不能是数字
    ID = 29

    # int型字面值
    LITERAL_INT = 30
    # double型字面值
    LITERAL_DOU = 31

    # 布尔型
    BOOL = 32

    # /*
    LCOM = 33
    # */
    RCOM = 34
    # //
    SCOM = 35

    # 逻辑表达式
    LOGIC_EXP = 36
    # 多项式
    ADDTIVE_EXP = 37
    # 项
    TERM_EXP = 38

    def __init__(self, t_type=None, line_num=None, value=None):
        self._type = t_type
        self._lineNum = line_num
        self._value = value

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def get_line_num(self):
        return self._lineNum

    def set_type(self, t_type):
        self._type = t_type

    def set_value(self, value):
        self._value = value

    def set_line_num(self, line_num):
        self._lineNum = line_num

    def to_string_with_line(self):
        try:
            if self._type == Token.INT:
                return "line .{0}".format(self._lineNum) + ": INT"
            if self._type == Token.DOUBLE:
                return "line .{0}".format(self._lineNum) + ": DOUBLE"
            if self._type == Token.IF:
                return "line .{0}".format(self._lineNum) + ": IF"
            if self._type == Token.ELSE:
                return "line .{0}".format(self._lineNum) + ": ELSE"
            if self._type == Token.WHILE:
                return "line .{0}".format(self._lineNum) + ": WHILE"
            if self._type == Token.READ:
                return "line .{0}".format(self._lineNum) + ": READ"
            if self._type == Token.WRITE:
                return "line .{0}".format(self._lineNum) + ": WRITE"
            if self._type == Token.ASSIGN:
                return "line .{0}".format(self._lineNum) + ": ASSIGN"
            if self._type == Token.BREAK:
                return "line .{0}".format(self._lineNum) + ": BREAK"

            if self._type == Token.PLUS:
                return "line .{0}".format(self._lineNum) + ": +"
            if self._type == Token.MINUS:
                return "line .{0}".format(self._lineNum) + ": -"
            if self._type == Token.MUL:
                return "line .{0}".format(self._lineNum) + ": *"
            if self._type == Token.DIV:
                return "line .{0}".format(self._lineNum) + ": /"
            if self._type == Token.MODE:
                return "line .{0}".format(self._lineNum) + ": %"
            if self._type == Token.LT:
                return "line .{0}".format(self._lineNum) + ": <"
            if self._type == Token.LET:
                return "line .{0}".format(self._lineNum) + ": <="
            if self._type == Token.GT:
                return "line .{0}".format(self._lineNum) + ": >="
            if self._type == Token.EQ:
                return "line .{0}".format(self._lineNum) + ": =="
            if self._type == Token.NEQ:
                return "line .{0}".format(self._lineNum) + ": !="

            if self._type == Token.LPARENT:
                return "line .{0}".format(self._lineNum) + ": ("
            if self._type == Token.RPARENT:
                return "line .{0}".format(self._lineNum) + ": )"
            if self._type == Token.LBRACKET:
                return "line .{0}".format(self._lineNum) + ": ["
            if self._type == Token.RBRACKET:
                return "line .{0}".format(self._lineNum) + ": ]"
            if self._type == Token.LBRACE:
                return "line .{0}".format(self._lineNum) + ": {"
            if self._type == Token.RBRACE:
                return "line .{0}".format(self._lineNum) + ": }"

            if self._type == Token.SEMI:
                return "line .{0}".format(self._lineNum) + ": ,"
            if self._type == Token.COMMA:
                return "line .{0}".format(self._lineNum) + ": ;"

            if self._type in [Token.LITERAL_INT, Token.LITERAL_DOU, Token.BOOL, Token.ID]:
                return "line .{0}".format(self._lineNum) + ": {0}".format(self._value)

            if self._type == Token.LCOM:
                return "line .{0}".format(self._lineNum) + ": /*"
            if self._type == Token.RCOM:
                return "line .{0}".format(self._lineNum) + ": */"
            if self._type == Token.SCOM:
                return "line .{0}".format(self._lineNum) + ": //"
        except Exception as e:
            print e

    def to_string(self):
        try:
            if self._type == Token.INT:
                return "INT"
            if self._type == Token.DOUBLE:
                return "DOUBLE"
            if self._type == Token.IF:
                return "IF"
            if self._type == Token.ELSE:
                return "ELSE"
            if self._type == Token.WHILE:
                return "WHILE"
            if self._type == Token.READ:
                return "READ"
            if self._type == Token.WRITE:
                return "WRITE"
            if self._type == Token.ASSIGN:
                return "ASSIGN"
            if self._type == Token.BREAK:
                return "BREAK"

            if self._type == Token.PLUS:
                return "+"
            if self._type == Token.MINUS:
                return "-"
            if self._type == Token.MUL:
                return "*"
            if self._type == Token.DIV:
                return "/"
            if self._type == Token.MODE:
                return "%"
            if self._type == Token.LT:
                return "<"
            if self._type == Token.LET:
                return "<="
            if self._type == Token.GT:
                return ">="
            if self._type == Token.EQ:
                return "=="
            if self._type == Token.NEQ:
                return "!="

            if self._type == Token.LPARENT:
                return "("
            if self._type == Token.RPARENT:
                return ")"
            if self._type == Token.LBRACKET:
                return "["
            if self._type == Token.RBRACKET:
                return "]"
            if self._type == Token.LBRACE:
                return "{"
            if self._type == Token.RBRACE:
                return "}"

            if self._type == Token.SEMI:
                return ","
            if self._type == Token.COMMA:
                return ";"

            if self._type in [Token.LITERAL_INT, Token.LITERAL_DOU, Token.BOOL, Token.ID]:
                return self._value

            if self._type == Token.LCOM:
                return "/*"
            if self._type == Token.RCOM:
                return "*/"
            if self._type == Token.SCOM:
                return "//"
        except Exception as e:
            print e
