# -*- coding: utf-8 -*-
__author__ = 'idbord'
from exception.interpretException import ErrorInterpret
from model.symbol_table import SymbolTable
from model.token import Token
from model.node import Node
from model.value import Value
from model.symbol_item import SymbolItem
from model.quaternion import Quaternion


class Generator:

    def __init__(self):
        pass

    symbol_table = SymbolTable()
    codes = []
    lineCount = -1
    scope_level = 0

    @classmethod
    def generate(cls, node_list):
        cls.symbol_table.new_table()
        for i in node_list:
            cls.translate_switch(i)
        cls.symbol_table.delete_table()
        temp = cls.codes
        cls.codes = []
        return temp

    @classmethod
    def translate_switch(cls, node):
        while True:
            node_type = node.get_type()
            if node_type == Node.IF_STMT:
                cls.translate_if(node)
            elif node_type == Node.WHILE_STMT:
                cls.translate_while(node)
            elif node_type == Node.READ_STMT:
                cls.translate_read(node)
            elif node_type == Node.WRITE_STMT:
                cls.translate_write(node)
            elif node_type == Node.DECLARE_STMT:
                cls.translate_declare(node)
            elif node_type == Node.ASSIGN_STMT:
                cls.translate_assign(node)
            cls.symbol_table.clear_temp_name()
            if node.get_next() is not None:
                node = node.get_next()
                continue
            break

    @classmethod
    def translate_if(cls, node):
        false_go = Quaternion(Quaternion.GO, cls.translate_exp(node.get_left()))
        cls.codes.append(false_go)
        cls.lineCount += 1
        cls.codes.append(Quaternion(Quaternion.IN))
        # 进入语句块
        cls.lineCount += 1
        # 代码层级加一
        cls.scope_level += 1
        # 处理这一层级
        cls.translate_switch(node.get_middle())
        # 清除局部变量
        cls.symbol_table.pop(cls.scope_level)
        # 代码层级恢复
        cls.scope_level -= 1
        cls.codes.append(Quaternion(Quaternion.OUT))
        cls.lineCount += 1
        # 判断else部分子节点是否存在
        if node.get_right() is not None:
            out_go = Quaternion(Quaternion.GO)
            cls.codes.append(out_go)
            cls.lineCount += 1
            false_go.set_forth(str(cls.lineCount+1))
            cls.codes.append(Quaternion(Quaternion.IN))
            cls.lineCount += 1
            cls.scope_level += 1
            cls.translate_switch(node.get_right())
            cls.symbol_table.pop(cls.scope_level)
            cls.scope_level -= 1
            cls.codes.append(Quaternion(Quaternion.OUT))
            cls.lineCount += 1
            out_go.set_forth(str(cls.lineCount+1))
        else:
            false_go.set_forth(str(cls.lineCount+1))

    @classmethod
    def translate_while(cls, node):
        go_line = cls.lineCount + 1
        false_go = Quaternion(Quaternion.GO, cls.translate_exp(node.get_left()))
        cls.codes.append(false_go)
        cls.lineCount += 1
        cls.codes.append(Quaternion(Quaternion.IN))
        cls.lineCount += 1
        cls.scope_level += 1
        cls.translate_switch(node.get_middle())
        cls.symbol_table.pop(cls.scope_level)
        cls.scope_level -= 1
        cls.codes.append(Quaternion(Quaternion.OUT))
        cls.lineCount += 1
        cls.codes.append(Quaternion(Quaternion.GO, None, None, go_line))
        cls.lineCount += 1
        false_go.set_forth(cls.lineCount + 1)

    @classmethod
    def translate_read(cls, node):
        try:
            # 变量类型
            var_type = cls.symbol_table.get_symbol_type(node.get_left().get_value())
            if var_type in [SymbolItem.INT, SymbolItem.DOUBLE]:
                cls.codes.append(Quaternion(first=Quaternion.READ, forth=node.get_left().get_value()))
                cls.lineCount += 1
                return
            elif var_type in [SymbolItem.ARRAY_INT, SymbolItem.ARRAY_DOU]:
                cls.codes.append(Quaternion(first=Quaternion.READ, forth=node.get_left().get_left() + "[" + cls.translate_exp(node.get_left().get_left()) + "]"))
                cls.lineCount += 1
                return
            raise ErrorInterpret("语句有误")
        except ErrorInterpret as e:
            print(e.content)

    @classmethod
    def translate_write(cls, node):
        cls.codes.append(Quaternion(first=Quaternion.WRITE, forth=cls.translate_exp(node.get_left())))
        cls.lineCount += 1

    @classmethod
    def translate_declare(cls, node):
        var = node.get_left()
        if var.get_left() is None:
            value = None
            if node.get_middle() is not None:
                value = cls.translate_exp(node.get_middle())
            if var.get_data_type() == Token.INT:
                cls.codes.append(Quaternion(Quaternion.INT, value, None, var.get_value()))
                cls.lineCount += 1
                symbol = SymbolItem(s_name=var.get_value(), s_type=SymbolItem.INT, s_level=cls.scope_level)
                cls.symbol_table.insert(symbol)
            elif var.get_data_type() == Token.DOUBLE:
                cls.codes.append(Quaternion(Quaternion.DOUBLE, value, None, var.get_value()))
                cls.lineCount += 1
                symbol = SymbolItem(s_name=var.get_value(), s_type=SymbolItem.DOUBLE, s_level=cls.scope_level)
                cls.symbol_table.insert(symbol)
        else:
            # 数组
            len = cls.translate_exp(var.get_left())
            if var.get_data_type() == Token.INT:
                cls.codes.append(Quaternion(Quaternion.INT, None, len, var.get_value()))
                cls.lineCount += 1
                symbol = SymbolItem(s_name=var.get_value(), s_type=SymbolItem.ARRAY_INT, s_level=cls.scope_level)
                cls.symbol_table.insert(symbol)
            elif var.get_data_type() == Token.DOUBLE:
                cls.codes.append(Quaternion(Quaternion.DOUBLE, None, len, var.get_value()))
                cls.lineCount += 1
                symbol = SymbolItem(s_name=var.get_value(), s_type=SymbolItem.ARRAY_DOU, s_level=cls.scope_level)
                cls.symbol_table.insert(symbol)

    # 赋值
    @classmethod
    def translate_assign(cls, node):
        value = cls.translate_exp(node.get_middle())
        var = node.get_left()
        if var.get_left() is None:
            cls.codes.append(Quaternion(Quaternion.ASSIGN, value, None, var.get_value()))
            cls.lineCount += 1
        else:
            index = cls.translate_exp(var.get_left())
            cls.codes.append(Quaternion(Quaternion.ASSIGN, value, None, var.get_value() + "[" + index + "]"))
            cls.lineCount += 1

    @classmethod
    def translate_exp(cls, sub_node):
        try:
            if sub_node.get_type() == Node.EXP:
                data_type = sub_node.get_data_type()
                if data_type == Token.LOGIC_EXP:
                    return cls.translate_logic_exp(sub_node)
                elif data_type == Token.MULTI_TERM_EXP:
                    return cls.translate_multi_term_exp(sub_node)
                elif data_type == Token.TERM_EXP:
                    return cls.translate_term_exp(sub_node)
                raise ErrorInterpret("表达式非法")
            elif sub_node.get_type() == Node.FACTOR:
                if sub_node.get_data_type() == Token.MINUS:
                    temp = cls.symbol_table.get_temp_symbol().get_name()
                    cls.codes.append(Quaternion(Quaternion.MINUS, cls.translate_exp(sub_node.get_left()), None, temp))
                    cls.lineCount += 1
                    return temp
                return cls.translate_exp(sub_node.get_left())
            elif sub_node.get_type() == Node.VAR:
                if sub_node.get_left() is None:
                    if cls.symbol_table.get_symbol_type(sub_node.get_value()) in [SymbolItem.INT, SymbolItem.DOUBLE]:
                        return sub_node.get_value()
                # 数组
                else:
                    if cls.symbol_table.get_symbol_type(sub_node.get_value()) in [SymbolItem.ARRAY_INT, SymbolItem.ARRAY_DOU]:
                        temp = cls.symbol_table.get_temp_symbol().get_name()
                        index = cls.translate_exp(sub_node.get_left())
                        cls.codes.append(Quaternion(Quaternion.ASSIGN, sub_node.get_value() + "[" + index + "]", None, temp))
                        cls.lineCount += 1
                        return temp
            elif sub_node.get_type() == Node.LITERAL:
                return sub_node.get_value()
            raise ErrorInterpret("表达式非法")
        except ErrorInterpret as e:
            print(e.content)

    @classmethod
    def translate_logic_exp(cls, node):
        try:
            temp = cls.symbol_table.get_temp_symbol().get_name()
            data_type = node.get_middle().get_data_type()
            if data_type == Token.GT:
                cls.codes.append(Quaternion(Quaternion.GT, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            elif data_type == Token.GET:
                cls.codes.append(Quaternion(Quaternion.GET, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            elif data_type == Token.LT:
                cls.codes.append(Quaternion(Quaternion.LT, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            elif data_type == Token.LET:
                cls.codes.append(Quaternion(Quaternion.LET, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            elif data_type == Token.EQ:
                cls.codes.append(Quaternion(Quaternion.EQ, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            elif data_type == Token.NEQ:
                cls.codes.append(Quaternion(Quaternion.NEQ, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            else:
                raise ErrorInterpret("逻辑运算非法")
            cls.lineCount += 1
            return temp
        except ErrorInterpret as e:
            print(e.content)

    @classmethod
    def translate_multi_term_exp(cls, node):
        try:
            temp = cls.symbol_table.get_temp_symbol().get_name()
            data_type = node.get_middle().get_data_type()
            if data_type == Token.PLUS:
                cls.codes.append(Quaternion(Quaternion.PLUS, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            elif data_type == Token.MINUS:
                cls.codes.append(Quaternion(Quaternion.MINUS, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
            else:
                raise ErrorInterpret("算数运算错误")
            cls.lineCount += 1
            return temp
        except ErrorInterpret as e:
            print(e.content)

    @classmethod
    def translate_term_exp(cls, node):
        try:
            op = cls.get_op(node.get_middle().get_data_type())
            temp = cls.symbol_table.get_temp_symbol().get_name()
            if node.get_right().get_type() == Node.FACTOR:
                cls.codes.append(Quaternion(op, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_right()), temp))
                cls.lineCount += 1
            else:
                cls.codes.append(Quaternion(op, cls.translate_exp(node.get_left()), cls.translate_exp(node.get_left().get_right()),temp))
                cls.lineCount += 1
                node = node.get_right()
                while node.get_right() is not None and node.get_right().get_type() != Node.FACTOR:
                    op = cls.get_op(node.get_middle().get_data_type())
                    temp2 = cls.symbol_table.get_temp_symbol().get_name()
                    cls.codes.append(Quaternion(op, temp, cls.translate_exp(node.get_right().get_left()), temp2))
                    cls.lineCount += 1
                    node = node.get_right()
                    temp = temp2
                op = cls.get_op(node.get_middle().get_data_type())
                temp2 = cls.symbol_table.get_temp_symbol().get_name()
                cls.codes.append(Quaternion(op, temp, cls.translate_exp(node.get_right()), temp2))
                cls.lineCount += 1
                temp = temp2
            return temp
        except ErrorInterpret as e:
            print(e.content)

    @classmethod
    def get_op(cls, op):
        if op == Token.MUL:
            return Quaternion.MUL
        elif op == Token.DIV:
            return Quaternion.DIV


