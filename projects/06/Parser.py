import re

class Parser:
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

    def __init__(self, file):
        with open(file, 'r') as f:
            self.content = f.readlines()
        self.command = ''
        self.cur_line = 0

    def hasMoreCommands(self):
        return (self.cur_line + 1) < len(self.content)

    def advance(self):
        if self.hasMoreCommands():
            self.cur_line += 1
            command = self.content[self.cur_line]
            pattern = re.compile(r'//.*$')
            command = pattern.sub('', command)
            if command == '\n':
                self.advance()
            else:
                self.command = command.strip()
    
    def commandType(self):
        if re.match(r'^@.*', self.command):
            return Parser.A_COMMAND
        elif re.match(r'^\(.*',self.command):
            return Parser.L_COMMAND
        else:
            return Parser.C_COMMAND
    
    def symbol(self):
        if self.commandType() == Parser.A_COMMAND or self.commandType() == Parser.L_COMMAND:
            matching = re.match(r'^[@\(](.*?)\)?$', self.command)
            symbol = matching.group(1)
            return symbol

    def dest(self):
        if self.commandType() == Parser.C_COMMAND:
            matching = re.match(r'^(.*?)=.*$', self.command)
            if not matching:
                dest = ''
            else:
                dest = matching.group(1)
            return dest

    def comp(self):
        if self.commandType() == Parser.C_COMMAND:
            comp = re.sub(r'^.*?=', '', self.command)
            comp = re.sub(r';\w+$', '', comp)
            return comp.strip()
    
    def jump(self):
        matching = re.match(r'^.*;(\w+)$', self.command)
        if not matching:
            jump = ''
        else:
            jump = matching.group(1)
        return jump

if __name__ == "__main__":
    p = Parser("max\Max.asm")
    p.advance()
    print(p.command)
    print(p.commandType())
    print(p.symbol())
    p.advance()
    print(p.command)
    print(p.commandType())
    print(p.dest())
    print(p.comp())
    # p.advance()
    # print(p.command)
    # print(p.commandType())
    # p.advance()
    # print(p.command)
    # print(p.commandType())
    # p.advance()
    # print(p.command)
    # print(p.commandType())
    # p.advance()
    # print(p.command)
    # print(p.commandType())