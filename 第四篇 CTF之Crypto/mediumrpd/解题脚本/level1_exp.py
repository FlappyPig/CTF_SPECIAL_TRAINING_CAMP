from zio import *
import time
import random
target=("106.14.204.93",5001)

io=zio(target)

v1=int(io.readline().strip())
v2=int(io.readline().strip())
def liner(seed):
    return ((seed*25214903917+11) & 0xffffffffffff)

for i in range(0xffff+1):
    seed=v1*65536+i
    if  liner(seed)>>16 == v2:
        print seed
        print liner(liner(seed))>>16
        io.writeline(str(liner(liner(seed))>>16))
        print io.readline()