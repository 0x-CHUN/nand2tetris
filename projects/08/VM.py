import Parser, CodeWriter
from config import *

class VM:

    def __init__(self):
        print("init")

    def translate_all(self, infiles, outfile):
        print(infiles)
        code_writer = CodeWriter.CodeWriter(outfile)
        code_writer.write_init()
        for infile in infiles:
            self._translate(infile, code_writer)
        code_writer.close_file()
    
    def _translate(self, infile, code_writer):
        parser = Parser.Parser(infile)
        code_writer.set_file_name(infile)
        while parser.hasMoreCommand():
            parser.advance()
            self._gen_code(parser, code_writer)

    def _gen_code(self, parser, code_writer):
        cmd = parser.commandType()
        if cmd == C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())
        elif cmd == C_PUSH or cmd == C_POP:
            code_writer.write_push_pop(cmd, parser.arg1(), parser.arg2())
        elif cmd == C_LABEL:
            code_writer.write_label(parser.arg1())
        elif cmd == C_GOTO:
            code_writer.write_goto(parser.arg1())
        elif cmd == C_IF:
            code_writer.write_if(parser.arg1())
        elif cmd == C_FUNCTION:
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif cmd == C_RETURN:
            code_writer.write_return()
        elif cmd == C_CALL:
            code_writer.write_call(parser.arg1(), parser.arg2())

if __name__ == "__main___":
    trans = VM()
    trans.translate_all(["ProgramFlow\BasicLoop\BasicLoop.vm"], "ProgramFlow\BasicLoop\BasicLoop.asm")