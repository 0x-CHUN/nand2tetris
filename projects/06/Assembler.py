from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable

class Assembler:

    def __init__(self):
        self.symboltable = SymbolTable()
        self.address = 16

    def assembler(self, file):
        self.file = file
        self.outputFile = file.replace(".asm", ".hack")
        self.firstStep()
        self.secondStep()
    
    def firstStep(self):
        p = Parser(self.file)
        cur_addr = 0
        while p.hasMoreCommands():
            p.advance()
            if p.commandType() == p.A_COMMAND or p.commandType() == p.C_COMMAND:
                cur_addr += 1
            elif p.commandType() == p.L_COMMAND:
                self.symboltable.addEntry(p.symbol(), cur_addr)
    
    def secondStep(self):
        p = Parser(self.file)
        outFile = open(self.outputFile, 'w')
        code = Code()
        while p.hasMoreCommands():
            p.advance()
            if p.commandType() == p.A_COMMAND:
                outFile.write(code.A(self.getAddr(p.symbol())) + '\n')
            elif p.commandType() == p.C_COMMAND:
                outFile.write(code.C(p.comp(), p.dest(), p.jump()) + '\n')
            elif p.commandType() == p.L_COMMAND:
                pass
        outFile.close()

    def getAddr(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self.symboltable.contains(symbol):
                self.symboltable.addEntry(symbol, self.address)
                self.address += 1
            return self.symboltable.getAddress(symbol)

if __name__ == "__main__":
    a = Assembler()
    a.assembler("max/Max.asm")
    a.assembler("max/MaxL.asm")
    a.assembler("pong/Pong.asm")
    a.assembler("pong/PongL.asm")
    a.assembler("rect/Rect.asm")
    a.assembler("rect/RectL.asm")