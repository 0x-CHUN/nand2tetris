# project 07

project7的目的是构建一个VM翻译器的第一部分

主要有两个模块parser和codewriter。

## parser

parse的功能在于读取VM命令并解析。

* 构造函数

  构造函数的功能在于打开文件，准备进行语法分析

  ```python
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
  ```

  初始化打开文件并读取。

* hasMoreCommands

  该接口用于读取下一条命令之前，判断是否还有命令

  ```python
      def hasMoreCommands(self):
          return (self.cur_line + 1) < len(self.content)
  ```

* advance

  读取下一条命令，如果是注释：以“//”开头，则跳过。若是命令，则解析将命令的类型和arg1、arg2赋值。

  ```python
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
  ```

* 剩下三个接口用于返回command类型、arg1、arg2

  ```python
      def commandType(self):
          return self.cmdtype
      
      def _arg1(self):
          return self.arg1
  
      def _arg2(self):
          return self.arg2
  ```

## codewriter

codewriter有5个函数

* 构造函数

  设定输入文件

* setFileName

  设置翻译输出文件并打开

* writeArithmetic

  通过command类型，写入汇编代码

* writePushPop

  同上

* close

  关闭输出文件

这部分最重要的是汇编的内容😂。