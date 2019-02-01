# relations-derivator
Derive the relationship of the simplified logical text
(SOP)

Python ~ 3.6

## Example Problem

### base problem

A circuit has four inputs D,C,B,A encoded in natural binary form where A is the least significant bit. The inputs <br />
in the range  0000=0  to  1011=11  represents  the  months  of  the  year  from  January  (0)  to  December  (11).<br />
Input in  the  range   1100-1111(i.e.12 to 15) cannot occur. The output of the circuit is true if the month <br />
represented by the input has 31 days. Otherwise the output is false. The output for inputs in the range <br />
1100 to 1111is undefined.

-Draw the truth table to represent the problem and obtain the function F as a Sum of minterm.


### input (first phase)



### input (second phase)
IA=0, IB=0, IC=0 and ID=0 then OZ=1. <br />
IA=0, IB=0, IC=1 and ID=0 then OZ=1. <br />
IA=0, IB=1, IC=0 and ID=0 then OZ=1. <br />
IA=0, IB=1, IC=1 and ID=0 then OZ=1. <br />
IA=0, IB=1, IC=1 and ID=1 then OZ=1. <br />
IA=1, IB=0, IC=0 and ID=1 then OZ=1. <br />
IA=1, IB=0, IC=1 and ID=1 then OZ=1. <br />

Note: No need ordered inputs or outputs, Inputs outputs can be separate by ',' or 'and'.
<br /> Ex :- IB=0 and IA=1, IC=0, ID=1 then OZ=1

### output
Z = A'B'C'D' + A'B'CD' + A'BC'D' + A'BCD' + A'BCD + AB'C'D + AB'CD