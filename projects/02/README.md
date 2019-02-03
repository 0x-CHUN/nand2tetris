# Project 02

第二个project是实现ALU，其中最基础的就是加法器，加法器分为两种：

* 半加器

  用来进行两位加法，布尔函数。

  | a    | b    | carry | sum  |
  | ---- | ---- | ----- | ---- |
  | 0    | 0    | 0     | 0    |
  | 0    | 1    | 0     | 1    |
  | 1    | 0    | 0     | 1    |
  | 1    | 1    | 1     | 0    |

  利用卡诺图，由上表格可得：

  carry = a * b

  sum = a + b

  因此半加器的实现：

  ```vhdl
  CHIP HalfAdder {
      IN a, b;    // 1-bit inputs
      OUT sum,    // Right bit of a + b 
          carry;  // Left bit of a + b
  
      PARTS:
      // Put you code here:
  		Xor(a=a,b=b,out=sum);
  		And(a=a,b=b,out=carry);
  }
  ```

* 全加器

  用来进行三位加法

  | a    | b    | c    | carry | sum  |
  | ---- | ---- | ---- | ----- | ---- |
  | 0    | 0    | 0    | 0     | 0    |
  | 0    | 0    | 1    | 0     | 1    |
  | 0    | 1    | 0    | 0     | 1    |
  | 0    | 1    | 1    | 1     | 0    |
  | 1    | 0    | 0    | 0     | 1    |
  | 1    | 0    | 1    | 1     | 0    |
  | 1    | 1    | 0    | 1     | 0    |
  | 1    | 1    | 1    | 1     | 1    |

  由上表得:

  carry = ~a * b * c + a * ~b * c + a * b * ~c + a * b * c

  sum = ~a * ~b * c + ~a  * b * ~c + a * ~b * ~c + a * b * c

  从原理上看，输入的c是上一位的进位，sum应为三位直接加起来，因此 sum = HalfAdder ( HalfAdder(a, b)的sum ，c)的sum。carry的还，应判断这两个HalfAdder是否由进位，因此carry = HalfAdder(a ,b)的carry + HalfAdder（~~，c)的carry

  ```vhdl
  CHIP FullAdder {
      IN a, b, c;  // 1-bit inputs
      OUT sum,     // Right bit of a + b + c
          carry;   // Left bit of a + b + c
  
      PARTS:
      // Put you code here:
  	HalfAdder(a=a,b=b,sum=aplusb,carry=c1);
  	HalfAdder(a=aplusb,b=c,sum=sum,carry=c2);
  	Or(a=c1,b=c2,out=carry);
  }
  ```

* Add16

  即16位加法器，利用FullAdder即可。

  ```vhdl
  CHIP Add16 {
      IN a[16], b[16];
      OUT out[16];
  
      PARTS:
     // Put you code here:
          HalfAdder(a=a[0], b=b[0], sum=out[0], carry=carry0);
          FullAdder(a=a[1], b=b[1], c=carry0, sum=out[1], carry=carry1);
          FullAdder(a=a[2], b=b[2], c=carry1, sum=out[2], carry=carry2);
          FullAdder(a=a[3], b=b[3], c=carry2, sum=out[3], carry=carry3);
          FullAdder(a=a[4], b=b[4], c=carry3, sum=out[4], carry=carry4);
          FullAdder(a=a[5], b=b[5], c=carry4, sum=out[5], carry=carry5);
          FullAdder(a=a[6], b=b[6], c=carry5, sum=out[6], carry=carry6);
          FullAdder(a=a[7], b=b[7], c=carry6, sum=out[7], carry=carry7);
          FullAdder(a=a[8], b=b[8], c=carry7, sum=out[8], carry=carry8);
          FullAdder(a=a[9], b=b[9], c=carry8, sum=out[9], carry=carry9);
          FullAdder(a=a[10], b=b[10], c=carry9, sum=out[10], carry=carry10);
          FullAdder(a=a[11], b=b[11], c=carry10, sum=out[11], carry=carry11);
          FullAdder(a=a[12], b=b[12], c=carry11, sum=out[12], carry=carry12);
          FullAdder(a=a[13], b=b[13], c=carry12, sum=out[13], carry=carry13);
          FullAdder(a=a[14], b=b[14], c=carry13, sum=out[14], carry=carry14);
          FullAdder(a=a[15], b=b[15], c=carry14, sum=out[15], carry=carry15);
  }
  ```

* Inc16

  增量器，即在16位数字的基础上加1。

  利用Add16直接加0000000000000001即可。

  ```vhdl
  CHIP Inc16 {
      IN in[16];
      OUT out[16];
  
      PARTS:
          // true populates a bus with all 1s
          Add16(a=in, b[0]=true, b[1..15]=false, out=out);
  }
  ```

  ## ALU

上述的加法器具有通用性，每个计算机都实用。而ALU则不同，Hack的ALU计算一组固定的函数：

```text
输入：
x[16],y[16]
zx, //x输入置0
nx, //x输入取反
zy, //y输入置0
ny, //y输入取反
f, //功能码：1代表add，0代表and
no, // out输出取反
输出：
out[16]
zr, //out=0，则为true
ng, //out<0，则为true
即：
if (zx == 1) set x = 0        // 16-bit constant
if (nx == 1) set x = !x       // bitwise not
if (zy == 1) set y = 0        // 16-bit constant
if (ny == 1) set y = !y       // bitwise not
if (f == 1)  set out = x + y  // integer 2's complement addition
if (f == 0)  set out = x & y  // bitwise and
if (no == 1) set out = !out   // bitwise not
if (out == 0) set zr = 1
if (out < 0) set ng = 1
```

实现：

```vhdl
CHIP ALU {
    IN  
        x[16], y[16],  // 16-bit inputs        
        zx, // zero the x input?
        nx, // negate the x input?
        zy, // zero the y input?
        ny, // negate the y input?
        f,  // compute out = x + y (if 1) or x & y (if 0)
        no; // negate the out output?

    OUT 
        out[16], // 16-bit output
        zr, // 1 if (out == 0), 0 otherwise
        ng; // 1 if (out < 0),  0 otherwise

    PARTS:
        // zx，利用Mux，若sel=zx=1，选b输出，out就全部位都为0
        Mux16(a=x, b=false, sel=zx, out=xAfterZx);

        // nx，同样利用Mux，sel=nx=1，选b输出，输入b的先16位取反即可。
        Not16(in=xAfterZx, out=negatedXAfterZx);
        Mux16(a=xAfterZx, b=negatedXAfterZx, sel=nx, out=xAfterNx);

        // zy，同zx
        Mux16(a=y, b=false, sel=zy, out=yAfterZy);

        // ny，同nx
        Not16(in=yAfterZy, out=negatedYAfterZy);
        Mux16(a=yAfterZy, b=negatedYAfterZy, sel=ny, out=yAfterNy);

        // f，利用Mux，sel=f=1，则输出a+b，反之输出a*b。
        Add16(a=xAfterNx, b=yAfterNy, out=fAdds);
        And16(a=xAfterNx, b=yAfterNy, out=fAnds);
        Mux16(a=fAnds, b=fAdds, sel=f, out=afterF);

        // no (and ng); store upper and lower output separate to help calc zr
        // 同上，利用Mux选通是否取反.out的最高位即符号位，ng = out[15]
        Not16(in=afterF, out=negatedAfterF);
        Mux16(a=afterF, b=negatedAfterF, sel=no, out=out, out[0..7]=lowerOutput, out[8..15]=upperOutput, out[15]=ng);

        // zr，判断是否为0
        Or8Way(in=lowerOutput, out=lowerOutputOrd);
        Or8Way(in=upperOutput, out=upperOutputOrd);
        Or(a=lowerOutputOrd, b=upperOutputOrd, out=zeroOnlyIfOutIsZero);
        Not(in=zeroOnlyIfOutIsZero, out=zr);
}
```

