import Lex
from config import *

class Parser:
    CMDTYPE = {
        'add':C_ARITHMETIC, 'sub':C_ARITHMETIC, 'neg':C_ARITHMETIC,
        'eq' :C_ARITHMETIC, 'gt' :C_ARITHMETIC, 'lt' :C_ARITHMETIC,
        'and':C_ARITHMETIC, 'or' :C_ARITHMETIC, 'not':C_ARITHMETIC,
        'label':C_LABEL,    'goto':C_GOTO,      'if-goto':C_IF, 
        'push':C_PUSH,      'pop':C_POP, 'call':C_CALL, 
        'return':C_RETURN, 'function':C_FUNCTION
    }

    NULLARY = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'return']
    UNARY = ['label', 'goto', 'if-goto']
    BINARY = ['push', 'pop', 'function', 'call']

    def __init__(self, file):
        self.lex = Lex.Lex(file)

    def initCMD(self):
        self.cmdType = C_ERROR
        self._arg1 = ''
        self._arg2 = 0

    def hasMoreCommand(self):
        return self.lex.hasMoreCommand()

    def advance(self):
        self.initCMD()
        self.lex.nextCommand()
        token, val = self.lex.curToken

        if token != Lex.ID:
            pass
        if val in self.NULLARY:
            self.nullaryCMD(val)
        elif val in self.UNARY:
            self.unaryCMD(val)
        elif val in self.BINARY:
            self.binaryCMD(val)

    def setCmdType(self, id):
        self.cmdType = self.CMDTYPE[id]

    def nullaryCMD(self, id):
        self.setCmdType(id)
        if self.cmdType == C_ARITHMETIC:
            self._arg1 = id
    
    def unaryCMD(self, id):
        self.setCmdType(id)
        token, val = self.lex.nextToken()
        self._arg1 = val

    def binaryCMD(self, id):
        self.setCmdType(id)
        token, val = self.lex.nextToken()
        self._arg2 = int(val)

    def commandType(self):
        return self.cmdType

    def arg1(self):
        return self._arg1

    def arg2(self):
        return self._arg2
