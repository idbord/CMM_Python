# -*- coding: utf-8 -*-
__author__ = 'idbord'
from model.bi_iterator import BiIterator

from model.token import Token
from model.node import Node
from exception.parserException import ErrorParse


class Parser:
    def __init__(self):
        pass

    iterator = None
    nodeList = []
    currentToken = None

    @classmethod
    def parser_analysis(cls, token_list):
        try:
            cls.iterator = BiIterator(token_list)
            while cls.iterator.has_next():
                node = cls.switch_stmt()
                if node:
                    cls.nodeList.append(node)
            temp = cls.nodeList
            cls.nodeList = []
            return temp
        except Exception as e:
            print e

    @classmethod
    def switch_stmt(cls):
        try:
            next_token = cls.get_next_token()
            next_token_type = next_token.get_type()
            next_token_line_num = next_token.get_line_num()
            if next_token_type == Token.IF:
                return cls.parse_if_stmt()
            elif next_token_type == Token.WHILE:
                return cls.parse_while_stmt()
            elif next_token_type == Token.READ:
                return cls.parse_read_stmt()
            elif next_token_type == Token.WRITE:
                return cls.parse_write_stmt()
            elif next_token_type in [Token.INT, Token.DOUBLE]:
                return cls.parse_declare_stmt()
            elif next_token_type == Token.LBRACE:
                return cls.parse_block_stmt()
            elif next_token_type == Token.ID:
                return cls.parse_assign_stmt()
            elif next_token_type in [Token.LCOM, Token.RCOM, Token.SCOM]:
                cls.read_token(next_token_type)
                return None
            raise ErrorParse(next_token_line_num, next_token_type)
        except ErrorParse as e:
            print e.content

    @classmethod
    def parse_if_stmt(cls):
        try:
            node = Node(Node.IF_STMT)
            cls.read_token(Token.IF)
            cls.read_token(Token.LPARENT)
            node.set_left(cls.parse_exp())
            cls.read_token(Token.RPARENT)
            node.set_middle(cls.switch_stmt())
            if cls.iterator.has_next() and cls.get_next_token().get_type() == Token.ELSE:
                cls.read_token(Token.ELSE)
                node.set_right(cls.switch_stmt())
            return node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    @classmethod
    def parse_while_stmt(cls):
        try:
            node = Node(Node.WHILE_STMT)
            cls.read_token(Token.WHILE)
            cls.read_token(Token.LPARENT)
            node.set_left(cls.parse_exp())
            cls.read_token(Token.RPARENT)
            node.set_middle(cls.switch_stmt())
            return node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    @classmethod
    def parse_read_stmt(cls):
        try:
            node = Node(Node.READ_STMT)
            cls.read_token(Token.READ)
            node.set_left(cls.identifier())
            cls.read_token(Token.SEMI)
            return node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    @classmethod
    def parse_write_stmt(cls):
        try:
            node = Node(Node.WRITE_STMT)
            cls.read_token(Token.WRITE)
            node.set_left(cls.parse_exp())
            cls.read_token(Token.SEMI)
            return node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    @classmethod
    def parse_declare_stmt(cls):
        try:
            node = Node(Node.DECLARE_STMT)
            var_node = Node(Node.VAR)
            if cls.get_next_token().get_type() in [Token.INT, Token.DOUBLE]:
                current_token = cls.iterator.next()
                data_type = Token.INT if current_token.get_type() == Token.INT else Token.DOUBLE
                var_node.set_data_type(data_type)
            else:
                next_token = cls.get_next_token()
                raise ErrorParse(next_token.get_line_num(), next_token.get_type())
            if cls.get_next_token().get_type() == Token.ID:
                current_token = cls.iterator.next()
                var_node.set_value(current_token.get_value())
            else:
                next_token = cls.get_next_token()
                raise ErrorParse(next_token.get_line_num(), next_token.get_type())
            if cls.get_next_token().get_type() == Token.ASSIGN:
                cls.read_token(Token.ASSIGN)
                node.set_middle(cls.parse_exp())
            elif cls.get_next_token().get_type() == Token.LBRACKET:
                cls.read_token(Token.LBRACKET)
                var_node.set_left(cls.parse_exp())
                cls.read_token(Token.RBRACKET)
            cls.read_token(Token.SEMI)
            node.set_left(var_node)
            return node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    @classmethod
    def parse_block_stmt(cls):
        try:
            node = Node(Node.NULL)
            header = node
            cls.read_token(Token.LBRACE)
            while cls.get_next_token().get_type() != Token.RBRACE:
                temp = cls.switch_stmt()
                node.set_next(temp)
                node = temp
            cls.read_token(Token.RBRACE)
            return header
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    @classmethod
    def parse_assign_stmt(cls):
        try:
            node = Node(Node.ASSIGN_STMT)
            node.set_left(cls.identifier())
            cls.read_token(Token.ASSIGN)
            node.set_middle(cls.parse_exp())
            cls.read_token(Token.SEMI)
            return node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    # 表达式
    @classmethod
    def parse_exp(cls):
        try:
            node = Node(Node.EXP)
            node.set_data_type(Token.LOGIC_EXP)
            left_node = cls.parse_multi_term_exp()
            if cls.get_next_token().get_type() in [Token.GT, Token.GET, Token.LT, Token.LET, Token.EQ, Token.NEQ]:
                node.set_left(left_node)
                node.set_middle(cls.parse_logic_op())
                node.set_right(cls.parse_multi_term_exp())
                return node
            return left_node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    # 多项式
    @classmethod
    def parse_multi_term_exp(cls):
        try:
            node = Node(Node.EXP)
            node.set_data_type(Token.MULTI_TERM_EXP)
            left_node = cls.parse_term_exp()
            next_token_type = cls.get_next_token().get_type()
            if next_token_type == Token.PLUS:
                node.set_left(left_node)
                node.set_middle(cls.parse_add_minus_op())
                node.set_right(cls.parse_multi_term_exp())
            elif next_token_type == Token.MINUS:
                node.set_left(left_node)
                node.set_middle(Node(Node.OP, m_data_type=Token.PLUS))
                node.set_right(cls.parse_multi_term_exp())
            else:
                return left_node
            return node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    # 项
    @classmethod
    def parse_term_exp(cls):
        try:
            node = Node(Node.EXP)
            node.set_data_type(Token.TERM_EXP)
            left_node = cls.parse_factor()
            if cls.get_next_token().get_type() in [Token.MUL, Token.DIV]:
                node.set_left(left_node)
                node.set_middle(cls.parse_mul_div_op())
                node.set_right(cls.parse_term_exp())
                return node
            return left_node
        except ErrorParse(cls.get_next_token().get_line_num(), cls.get_next_token().get_type()) as e:
            print e.content

    # 因子
    @classmethod
    def parse_factor(cls):
        try:
            if cls.iterator.has_next():
                node = Node(Node.FACTOR)
                next_token_type = cls.get_next_token().get_type()
                if next_token_type in [Token.LITERAL_INT, Token.LITERAL_DOU]:
                    node.set_left(cls.parse_literal())
                elif next_token_type == Token.LPARENT:
                    cls.read_token(Token.LBRACKET)
                    node.set_middle(cls.parse_exp())
                    cls.read_token(Token.RPARENT)
                elif next_token_type == Token.MINUS:
                    node.set_data_type(Token.MINUS)
                    cls.currentToken = cls.iterator.next()
                    node.set_left(cls.parse_term_exp())
                elif next_token_type == Token.PLUS:
                    cls.currentToken == cls.iterator.next()
                    node.set_left(cls.parse_term_exp())
                elif next_token_type == Token.ID:
                    return cls.identifier()
                return node
            raise ErrorParse(cls.get_next_token().get_line_num(), "factor")
        except ErrorParse as e:
            print e.content

    @classmethod
    def parse_literal(cls):
        try:
            if cls.iterator.has_next():
                cls.currentToken = cls.iterator.next()
                current_token_type = cls.currentToken.get_type()
                node = Node(Node.LITERAL)
                node.set_data_type(current_token_type)
                node.set_value(cls.currentToken.get_value())
                if current_token_type in [Token.LITERAL_INT, Token.LITERAL_DOU]:
                    return node
            raise ErrorParse(cls.get_next_token().get_line_num(), "literal")
        except ErrorParse as e:
            print e.content

    # 逻辑运算符
    @classmethod
    def parse_logic_op(cls):
        try:
            if cls.iterator.has_next():
                cls.currentToken = cls.iterator.next()
                current_token_type = cls.currentToken.get_type()
                if current_token_type in [Token.GT, Token.GET, Token.LT, Token.LET, Token.EQ, Token.NEQ]:
                    node = Node(Node.OP)
                    node.set_data_type(current_token_type)
                    return node
            ErrorParse(cls.get_next_token().get_line_num(), "logical operation!")
        except ErrorParse as e:
            print e.content

    # 加减运算符
    @classmethod
    def parse_add_minus_op(cls):
        try:
            if cls.iterator.has_next():
                cls.currentToken = cls.iterator.next()
                current_token_type = cls.currentToken.get_type()
                if current_token_type in [Token.PLUS, Token.MINUS]:
                    node = Node(Node.OP)
                    node.set_data_type(current_token_type)
                    return node
            raise ErrorParse(cls.get_next_token().get_line_num(), "additive operation")
        except ErrorParse as e:
            print e.content

    # 乘除运算符
    @classmethod
    def parse_mul_div_op(cls):
        try:
            if cls.iterator.has_next():
                cls.currentToken = cls.iterator.next()
                current_token_type = cls.currentToken.get_type()
                if current_token_type in [Token.MUL, Token.DIV]:
                    node = Node(Node.OP)
                    node.set_data_type(current_token_type)
                    return node
            raise ErrorParse(cls.get_next_token().get_line_num(), "multiple operation")
        except ErrorParse as e:
            print e.content

    # 变量名，单个变量或数组
    @classmethod
    def identifier(cls):
        try:
            node = Node(Node.VAR)
            next_token_type = cls.get_next_token().get_type()
            if next_token_type == Token.ID:
                node.set_value(cls.iterator.next().get_value())
            else:
                raise ErrorParse(cls.get_next_token().get_line_num(), "identifier")
            if cls.get_next_token().get_type() == Token.LBRACKET:
                cls.read_token(Token.LBRACKET)
                node.set_left(cls.parse_exp())
                cls.read_token(Token.RBRACKET)
            return node
        except ErrorParse as e:
            print e.content

    @classmethod
    def get_next_token(cls):
        if cls.iterator.has_next():
            token = cls.iterator.next()
            cls.iterator.prev()
            return token
        return None

    @classmethod
    def read_token(cls, t_type):
        try:
            if cls.iterator.has_next():
                cls.currentToken = cls.iterator.next()
                if cls.currentToken.get_type() == t_type:
                    return
            raise ErrorParse(cls.currentToken.get_line_num(), cls.currentToken.get_type())
        except ErrorParse as e:
            print e.content
