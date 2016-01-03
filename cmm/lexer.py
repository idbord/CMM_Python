# -*- coding: utf-8 -*-
__author__ = 'idbord'

from model.token import Token
import string


class Lexer:
    def __init__(self):
        pass

    bufferStream = None
    currentStr = ""
    lineNum = 1

    @classmethod
    def lexer_analysis(cls, stream):
        Lexer.bufferStream = stream
        token_list = []
        try:
            Lexer.read_char()
            while Lexer.currentStr != '':
                # 消除特殊符号
                if Lexer.currentStr in ['\n', '\t', '\f', '\r', ' ']:
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == '+':
                    token_list.append(Token(Token.PLUS, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == '-':
                    token_list.append(Token(Token.MINUS, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == '*':
                    token_list.append(Token(Token.MUL, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == '%':
                    token_list.append(Token(Token.MODE, Lexer.lineNum))
                    Lexer.read_char()
                    continue

                elif Lexer.currentStr == '(':
                    token_list.append(Token(Token.LPARENT, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == ')':
                    token_list.append(Token(Token.RPARENT, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == '[':
                    token_list.append(Token(Token.LBRACKET, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == ']':
                    token_list.append(Token(Token.RBRACKET, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == '{':
                    token_list.append(Token(Token.LBRACE, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == '}':
                    token_list.append(Token(Token.RBRACE, Lexer.lineNum))
                    Lexer.read_char()
                    continue

                elif Lexer.currentStr == ',':
                    token_list.append(Token(Token.SEMI, Lexer.lineNum))
                    Lexer.read_char()
                    continue
                elif Lexer.currentStr == ';':
                    token_list.append(Token(Token.COMMA, Lexer.lineNum))
                    Lexer.read_char()
                    continue

                elif Lexer.currentStr == '/':
                    Lexer.read_char()
                    if Lexer.currentStr == '*':
                        token_list.append(Token(Token.LCOM, Lexer.lineNum))
                        Lexer.read_char()
                        while Lexer.currentStr != '':
                            if Lexer.currentStr == '*':
                                Lexer.read_char()
                                if Lexer.currentStr == '/':
                                    token_list.append(Token(Token.RCOM, Lexer.lineNum))
                                    Lexer.read_char()
                                    break
                            Lexer.read_char()
                        continue
                    elif Lexer.currentStr == '/':
                        while Lexer.currentStr is not '\n' and Lexer.currentStr != '':
                            Lexer.read_char()
                        token_list.append(Token(Token.SCOM, Lexer.lineNum))
                        continue
                    token_list.append(Token(Token.DIV, Lexer.lineNum))
                    continue

                elif Lexer.currentStr == '=':
                    Lexer.read_char()
                    if Lexer.currentStr == '=':
                        token_list.append(Token(Token.EQ, Lexer.lineNum))
                        Lexer.read_char()
                        continue
                    token_list.append(Token(Token.ASSIGN, Lexer.lineNum))
                    continue

                elif Lexer.currentStr == '<':
                    Lexer.read_char()
                    if Lexer.currentStr == '=':
                        token_list.append(Token(Token.LET, Lexer.lineNum))
                        continue
                    token_list.append(Token(Token.LT, Lexer.lineNum))
                    continue

                elif Lexer.currentStr == '>':
                    Lexer.read_char()
                    if Lexer.currentStr == '=':
                        token_list.append(Token(Token.GET, Lexer.lineNum))
                        continue
                    token_list.append(Token(Token.GT, Lexer.lineNum))
                    continue

                elif Lexer.currentStr == '!':
                    Lexer.read_char()
                    if Lexer.currentStr == '=':
                        token_list.append(Token(Token.NEQ, Lexer.lineNum))
                        continue

                elif 'a' <= Lexer.currentStr <= 'z' or 'A' <= Lexer.currentStr <= 'Z':
                    string_temp = Lexer.currentStr
                    Lexer.read_char()
                    while ('a' <= Lexer.currentStr <= 'z') or ('A' <= Lexer.currentStr <= 'Z') or \
                            ('0' <= Lexer.currentStr <= '9') or (Lexer.currentStr == '_'):
                        string_temp += Lexer.currentStr
                        Lexer.read_char()
                    token = Token(line_num=Lexer.lineNum)
                    if string_temp == 'int':
                        token.set_type(Token.INT)
                    elif string_temp == 'double':
                        token.set_type(Token.DOUBLE)
                    elif string_temp == 'if':
                        token.set_type(Token.IF)
                    elif string_temp == 'else':
                        token.set_type(Token.ELSE)
                    elif string_temp == 'while':
                        token.set_type(Token.WHILE)
                    elif string_temp == 'read':
                        token.set_type(Token.READ)
                    elif string_temp == 'write':
                        token.set_type(Token.WRITE)
                    elif string_temp == 'break':
                        token.set_type(Token.BREAK)
                    elif string_temp in ['True', 'False']:
                        token.set_type(Token.BOOL)
                        value = True if string_temp == 'True' else False
                        token.set_value(value)
                    else:
                        token.set_type(Token.ID)
                        token.set_value(string_temp)
                    token_list.append(token)
                    continue

                elif '0' <= Lexer.currentStr <= '9':
                    is_double = False
                    int_temp = Lexer.currentStr
                    Lexer.read_char()
                    while '0' <= Lexer.currentStr <= '9' or Lexer.currentStr == '.':
                        if Lexer.currentStr == '.':
                            is_double = True
                        int_temp += Lexer.currentStr
                        Lexer.read_char()
                    if is_double:
                        token_list.append(Token(Token.LITERAL_DOU, Lexer.lineNum, string.atof(int_temp)))
                        continue
                    token_list.append(Token(Token.LITERAL_INT, Lexer.lineNum, string.atoi(int_temp)))
                    continue

            return token_list

        except Exception as e:
            print e

    @classmethod
    def read_char(cls):
        try:
            Lexer.currentStr = str(Lexer.bufferStream.read(1))
            if Lexer.currentStr == '\n':
                Lexer.lineNum += 1
        except IOError as e:
            print e
