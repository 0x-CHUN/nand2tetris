# Project 04

本次project的目的是熟悉hack语言。

* Mult

  Mult的要求是计算R0*R1，存入R2中。没有Mul指令，可以通过加R0次R1即可。

  ```text
      @2
      M=0 //将R2置为0
      @i
      M=0 //将i置为0，i为计算R1的次数
  (LOOP)
      @i
      D=M // i存入寄存器D
      @0
      D=D-M // D = i- R[0],判断是否计算了R[0]个R[1]
      @END
      D;JGE // D==0？，yes就跳转至END
  
      @1 
      D=M // D=R[1]
      @2
      M=M+D // R[2] = R[2] + R[1]
      @i
      M=M+1 // i ++
      @LOOP
      0;JMP // 跳转至LOOP
  (END)
      @END
      0;JMP
  ```

  ```text
      @SCREEN
      D=A // D加载SCREEN的地址
      @i
      M=D-1 //memory中的i存入screen的地址-1
  
      @KBD
      D=A // D加载KBD的地址
      @j
      M=D //j存入KBD的地址
  
  //Counter 
      @i
      D=M //D存入i的内容即screen的地址-1
      @k
      M=D //k存入D中内容，即Screen地址-1
  
  (LOOP) 
      @KBD
      D=M //读取KBD的内容存入D
  
      @WHITE
      D;JEQ //D==0，没有摁下就跳转至white
      @BLACK
      0;JMP //D!=0，就跳转至black
  
  
  (BLACK) 
  
      @j
      D=M //读取j即KBD的地址
      @k
      D=D-M //判断是否到了screen的top
      @LOOP
      D;JEQ
  
      @k
      A=M //A存入，Screen地址
      M=-1 // M置为0即变黑
      @k
      M=M+1 // 下个像素点
  
      @LOOP
      0;JMP
  
  (WHITE)
  
      @i
      D=M
      @k
      D=D-M
      @LOOP
      D;JEQ
  
  	@k
      M=M-1
      A=M
      M=0
  
      @LOOP
      0;JMP
  ```

  