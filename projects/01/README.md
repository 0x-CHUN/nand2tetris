# Project 01

最基础的门就是nand，可以通过nand构造其他所有逻辑门。nand不需要实现。

**nand门：nand(a, b) = not ( and (a,b))**

以下是实现的chip：

* Not

  实现原理：not(a) = nand(a, a) = not( and (a, a)) = not (a)

  ```vhdl
  CHIP Not {
      IN in;
      OUT out;
  
      PARTS:
      // Put your code here:
  		Nand(a=in, b=in, out=out);
  }
  ```

* And

  实现原理：and(a, b) = not( nand(a, b) ) = not( not (and (a, b) ) ) = and (a, b)

  ```vhdl
  CHIP And {
      IN a, b;
      OUT out;
  
      PARTS:
      // Put your code here:
  		Nand (a=a, b=b, out=notab);
  		Not(in=notab, out=out);
  }
  ```

* Or

  实现原理：or(a) = nand(not(a), not(b))

  ```vhdl
  CHIP Or {
      IN a, b;
      OUT out;
  
      PARTS:
      // Put your code here:
  		Not(in=a, out=nota);
  		Not(in=b, out=notb);
  		Nand(a=nota, b=notb, out=out);
  }
  ```

* Xor

  实现原理：xor = a * not (b) + not(a) * b (*代表and ，+代表 or)。

  ```vhdl
  CHIP Xor {
      IN a, b;
      OUT out;
  
      PARTS:
      // Put your code here:
  		Not(in=a, out=nota);
  		Not(in=b, out=notb);
  		And(a=a, b=notb,out= anotb);
  		And(a=nota, b=b, out=notab);
  		Or(a=anotb, b=notab, out=out);
  }
  ```

* Mux

  实现原理：

  ```text
  Multiplexor:
      if sel == 0 
          out = a 
      otherwise
          out = b
  ```

  ```vhdl
  CHIP Mux {
      IN a, b, sel;
      OUT out;
  
      PARTS:
          Not(in=sel, out=notS);
          Not(in=a, out=notA);
          Not(in=b, out=notB);
  
          Or(a=sel, b=a, out=notSImpliesA);
          Or(a=notS, b=b, out=sImpliesB);
  
          And(a=notSImpliesA, b=sImpliesB, out=out);
  }
  ```

* DMux

  实现原理：

  ```text
  {a, b} = {in, 0} if sel == 0
   		 {0, in} if sel == 1
  ```

  ```vhdl
  CHIP DMux {
      IN in, sel;
      OUT a, b;
  
      PARTS:
      // Put your code here:
  	    Not(in=sel, out=selIS0);
          And(a=in, b=selIS0, out=a);
          And(a=in, b=sel, out=b);
  }
  ```

* Not16

  16-bit Not：按位not就行。

  ```vhdl
  CHIP Not16 {
      IN in[16];
      OUT out[16];
  
      PARTS:
      // Put your code here:
  	    Not(in=in[0], out=out[0]);
          Not(in=in[1], out=out[1]);
          Not(in=in[2], out=out[2]);
          Not(in=in[3], out=out[3]);
          Not(in=in[4], out=out[4]);
          Not(in=in[5], out=out[5]);
          Not(in=in[6], out=out[6]);
          Not(in=in[7], out=out[7]);
          Not(in=in[8], out=out[8]);
          Not(in=in[9], out=out[9]);
          Not(in=in[10], out=out[10]);
          Not(in=in[11], out=out[11]);
          Not(in=in[12], out=out[12]);
          Not(in=in[13], out=out[13]);
          Not(in=in[14], out=out[14]);
          Not(in=in[15], out=out[15]);
  }
  ```

* And16

  16-bit And：同上，按位and就行。

* Or16

  16-bit Or：同上，按位or就行。

* Mux16

  16-bit multiplexor：同上，按位Mux就行。

* Or8Way

  8-way Or: out = (in[0] or in[1] or ... or in[7])

  ```vhdl
  CHIP Or8Way {
      IN in[8];
      OUT out;
  
      PARTS:
      // Put your code here:
  		Or(a=in[0], b=in[1], out=out1);
  		Or(a=in[2], b=out1, out=out2);
  		Or(a=in[3], b=out2, out=out3);
  		Or(a=in[4], b=out3, out=out4);
  		Or(a=in[5], b=out4, out=out5);
  		Or(a=in[6], b=out5, out=out6);
  		Or(a=in[7], b=out6, out=out);
  }
  ```

* Mux4Way16

  ```text
  16-bit/4-way mux:
  out = a if sel == 00
         b if sel == 01
         c if sel == 10
         d if sel == 11
  利用2个16mux，然后sel[0]为sel1，输出a或b。sel[1]为sel2，输出c或d。
  ```

  ```vhdl
  CHIP Mux4Way16 {
      IN a[16], b[16], c[16], d[16], sel[2];
      OUT out[16];
  
      PARTS:
      // Put your code here:
          Mux16(a=a,b=b, sel=sel[0], out=aOrb);
          Mux16(a=c,b=d, sel=sel[0], out=cOrd);
          Mux16(a=aOrb, b=cOrd, sel=sel[1], out=out);
  }
  ```

* Mux8Way16

  ```text
   8-way 16-bit multiplexor:
   	out = a if sel == 000
      b if sel == 001
      etc.
      h if sel == 111
   思路同Mux4Way16，利用2个Mux4Way16实现Mux8Way16。
  ```

  ```vhdl
  CHIP Mux8Way16 {
      IN a[16], b[16], c[16], d[16],
         e[16], f[16], g[16], h[16],
         sel[3];
      OUT out[16];
  
      PARTS:
      // Put your code here:
  		Mux4Way16(a=a, b=b, c=c, d=d, sel=sel[0..1], out=atod);
  		Mux4Way16(a=e, b=f, c=g, d=h, sel=sel[0..1], out=etoh);
  		Mux16(a=atod, b=etoh, sel=sel[2], out=out);
  }
  ```

* DMux4Way

  ```text
  4-way demultiplexor:
  {a, b, c, d} = {in, 0, 0, 0} if sel == 00
                 {0, in, 0, 0} if sel == 01
                 {0, 0, in, 0} if sel == 10
                 {0, 0, 0, in} if sel == 11
  思路同Mux416Way，利用2个DMux实现即可。
  ```

  ```vhdl
  CHIP DMux4Way {
      IN in, sel[2];
      OUT a, b, c, d;
  
      PARTS:
      // Put your code here:
  		DMux(in=in, sel=sel[0], a=x1or3, b=x2or4);
  		DMux(in=in, sel=sel[1], a=x1or2, b=x3or4);
  		And(a=x1or2, b=x1or3, out=a);
          And(a=x1or2, b=x2or4, out=b);
          And(a=x1or3, b=x3or4, out=c);
          And(a=x2or4, b=x3or4, out=d);
  }
  ```

* DMux8Way

  ```text
  8-way demultiplexor:
  {a, b, c, d, e, f, g, h} = {in, 0, 0, 0, 0, 0, 0, 0} if sel == 000
                             {0, in, 0, 0, 0, 0, 0, 0} if sel == 001
                             etc.
                             {0, 0, 0, 0, 0, 0, 0, in} if sel == 111
  思路同上，利用2个DMux4Way实现。
  ```

  