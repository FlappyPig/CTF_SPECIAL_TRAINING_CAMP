from z3 import *
import base64

s2 = [151, 130, 175, 190, 163, 189, 149, 132, 192, 188, 159, 162, 131, 99, 168, 197, 151, 151, 164, 164, 152, 166, 205, 188, 163, 162, 146, 161, 162, 135, 149, 156, 180, 218, 229, 192, 159, 185, 202, 22]
s1 = [BitVec('s1_%d' % i, 8) for i in range(41)]

s = Solver()
for i in range(39):
    s.add(s1[i]+s1[i+1] == s2[i])
s.add(s1[9] - s1[20] == 22)
s.add(s1[40] == 0)

s3 = ''
if s.check() == z3.sat:
    m = s.model()
    for i in range(40):
        s3 += chr(m[s1[i]].as_long())

s4 = ''.join([chr(ord(s3[i])+3) for i in range(len(s3))])
flag = base64.b64decode(s4)
print flag
#XPlAy4fUNcOnTeSTwhITEhaT2k15ha
