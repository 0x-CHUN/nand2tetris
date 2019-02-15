# project 06

本project的目的实现hack汇编编译器。

## 步骤

1. parser

   语法分析器的主要功能是将汇编命令分解为器表达的内在含义。

   API：

   | 函数            | 参数     | 返回值           | 功能                         |
   | :-------------- | :------- | :--------------- | :--------------------------- |
   | 构造函数        | 文件file | void             | 打开文件，读取内容           |
   | hasMoreCommands | void     | bool             | 判读是否还有命令             |
   | advance         | void     | void             | 读取下一条命令，赋为当前命令 |
   | commandType     | void     | Parser.X_COMMAND | 返回当前命令类型             |
   | symbol          | void     | str              | 返回形如“@xx”中的“XX”        |
   | dest            | void     | str              | 返回C指令的dest              |
   | comp            | void     | str              | 返回C指令的comp              |
   | jump            | void     | str              | 返回C指令的jump              |

2. Code

   Code模块的主要目的是将助记符号转化为二进制码。

   | 函数 | 参数 | 返回值     | 功能                                |
   | ---- | ---- | ---------- | ----------------------------------- |
   | dest | str  | 3bit的str  | 返回dest的二进制码                  |
   | comp | str  | 7bit的str  | 返回comp的二进制码                  |
   | jump | str  | 3bit的str  | 返回jump的二进制码                  |
   | A    | str  | 16bit的str | 返回A类型二进制码                   |
   | C    | str  | 16bit的str | 利用上面三个函数，返回C类型二进制码 |

3. SymbolTable

   因为汇编语言中肯定包含符号，必须为符号确定实际地址，因此需维护一个**符号表**。

   API：

   | 函数       | 参数     | 返回值 | 功能                      |
   | ---------- | -------- | ------ | ------------------------- |
   | 构造函数   | void     | void   | 初始化默认符号表          |
   | addEntry   | str、int | void   | 将（sym，addr）加入符号表 |
   | contains   | str      | bool   | 是否包含指定symbol        |
   | getAddress | str      | int    | 返回symbol的地址          |

4. assembler

   对于有符号的程序来说，解决办法是读**两遍**

   第一遍：逐行读取，在符号表中建立每条命令对应的地址。

   第二遍：逐行读取，编译成二进制码。