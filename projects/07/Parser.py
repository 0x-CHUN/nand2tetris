import re
from config import *

class Parser:
    command_type = {'add':C_ARITHMETIC, 'sub':C_ARITHMETIC, 'neg':C_ARITHMETIC,
                     'eq' :C_ARITHMETIC, 'gt' :C_ARITHMETIC, 'lt' :C_ARITHMETIC,
                     'and':C_ARITHMETIC, 'or' :C_ARITHMETIC, 'not':C_ARITHMETIC,
                     'label':C_LABEL,    'goto':C_GOTO,      'if-goto':C_IF, 
                     'push':C_PUSH,      'pop':C_POP, 
                    'call':C_CALL, 'return':C_RETURN, 'function':C_FUNCTION}
    
    def __init__(self, file):
        with open(file, 'r') as f:
            self.content = f.readlines()
        self.command = ''
        self.cur_line = 0
        self.cmdtype = C_ERROR
        self.arg1 = ''
        self.arg2 = 0

    def hasMoreCommands(self):
        return (self.cur_line + 1) < len(self.content)

    def advance(self):
        self.cur_line += 1
        command = self.content[self.cur_line]
        pattern = re.compile(r'//.*$')
        command = pattern.sub('', command)
        if command == '\n':
            self.advance()
        else:
            self.command = command.strip()
        token = self.command.split()
        self.cmdtype = self.command_type.get(token[0])
        self.arg1 = ''
        self.arg2 = 0
        if len(token) == 2:
            self.arg1 = token[1]
        elif len(token) == 3:
            self.arg1 = token[1]
            self.arg2 = int(token[2])

    def commandType(self):
        return self.cmdtype
    
    def _arg1(self):
        return self.arg1

    def _arg2(self):
        return self.arg2

if __name__ == "__main__":
    p = Parser('MemoryAccess/BasicTest/BasicTest.vm')
    while p.hasMoreCommands():
        p.advance()
        print(p.commandType(), end=" ")
        print(p.arg1, end=" ")
        print(p.arg2)
