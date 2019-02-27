import re

NUM     = 1
ID      = 2
ERROR   = 3 

class Lex:

    def __init__(self, filename):
        file = open(filename, 'r')
        self.lines = file.read()
        self.tokens = self.tokenize(self.lines.split('\n'))
        self.curCMD = []
        self.curToken = (ERROR, 0)
    
    def hasMoreCommand(self):
        return len(self.tokens) != 0

    def nextCommand(self):
        self.curCMD = self.tokens.pop(0)
        self.nextToken()
        return self.curCMD

    def hasMoreToken(self):
        return len(self.curCMD) != 0

    def nextToken(self):
        if self.hasMoreToken():
            self.curToken = self.curCMD.pop(0)
        else:
            self.curToken = (ERROR, 0)
        return self.curToken

    def peekToken(self):
        if self.hasMoreToken():
            return self.curCMD[0]
        else:
            return (ERROR, 0)
    
    def tokenize(self, lines):
        return [t for t in [self.lineTokenize(line) for line in lines] if t != []]

    def lineTokenize(self, line):
        return [self.token(word) for word in self.splitLine(self.removeComment(line))]

    def removeComment(self, line):
        return re.compile('//.*$').sub('', line)

    def splitLine(self, line):
        return re.compile(r'\d+' + '|' + r'[\w\-.]+').findall(line)

    def token(self, word):
        if self.isNum(word):
            return (NUM, word)
        elif self.isId(word):
            return (ID, word)
        else:
            return (ERROR, word)
    
    def isNum(self, word):
        return re.match(r'\d+' , word) != None

    def isId(self, word):
        return re.match(r'[\w\-.]+', word) != None

if __name__ == "__main__":
    lex = Lex("FunctionCalls/FibonacciElement/Sys.vm")
    print(lex.tokens)