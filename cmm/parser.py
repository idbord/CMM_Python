# -*- coding: utf-8 -*-
__author__ = 'idbord'
from model.bi_iterator import BiIterator

from model.token import Token
from model.node import Node
from exception.parserException import ErrorParse


class Parser:
    iterator = None
    nodeList = []
    currentToken = None

    @classmethod
    def parser_analysis(cls, token_list):
        try:
            cls.iterator = BiIterator(token_list)
            while cls.iterator.hasNext():
                cls.nodeList.append(cls.switch_stmt())
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
            raise ErrorParse(next_token_line_num, next_token_type)
        except ErrorParse as e:
            print e.content

    @classmethod
    def parse_if_stmt(cls):
        pass

    @classmethod
    def parse_while_stmt(cls):
        pass

    @classmethod
    def parse_read_stmt(cls):
        pass

    @classmethod
    def parse_write_stmt(cls):
        pass

    @classmethod
    def parse_declare_stmt(cls):
        pass

    @classmethod
    def parse_block_stmt(cls):
        pass

    @classmethod
    def parse_assign_stmt(cls):
        pass

    @classmethod
    def get_next_token(cls):
        if cls.iterator.hasNext():
            token = cls.iterator.next()
            cls.iterator.prev()
            return token
        return None

    @classmethod
    def check_next_token_type(cls, temp):
        token = cls.get_next_token()
        for i in temp:
            if token.getType() == i:
                return True
        return False

    @classmethod
    def read_token(cls, type):
        try:
            if cls.iterator.hasNext():
                cls.currentToken = cls.iterator.next()
                if cls.currentToken.get_type() == type:
                    return
            raise ErrorParse(cls.currentToken.get_line_num(), cls.currentToken.get_type())
        except ErrorParse as e:
            print e.content

